import json
import unittest

from app import app
from utils.db import (
    init_db,
    get_connection,
    get_all_students,
    get_student_by_id,
    get_ld_screened_students,
    get_counselor_exercises,
    get_counselor_messages,
)


class TestCounselorAndChatbot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        app.config["TESTING"] = True

    @classmethod
    def tearDownClass(cls):
        """Remove unittest-created rows so the demo SQLite DB remains spotless."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM counselor_messages WHERE subject LIKE 'UNITTEST%'")
        cursor.execute("DELETE FROM counselor_exercises WHERE title LIKE 'UNITTEST%'")
        cursor.execute("""
            UPDATE students
            SET ld_notes = 'Slow word-problem decoding under timed conditions and occasional symbol swaps in math, paired with strong oral reasoning. Recommended color-chunked reading, CRA math visuals, and extra time.'
            WHERE student_id = 'SH-2026-001'
        """)
        conn.commit()
        conn.close()

    def _login(self, client, username, password):
        return client.post(
            "/login",
            data={"username": username, "password": password},
            follow_redirects=True,
        )

    def test_01_ld_sectioning_preserves_300_student_cohort(self):
        """LD / Early Screening sectioning must tag students inside the 300-student cohort without changing totals."""
        all_students = get_all_students()
        self.assertEqual(len(all_students), 300)
        for tid in ("teacher1", "teacher2", "teacher3"):
            self.assertEqual(len(get_all_students(teacher_id=tid)), 100)

        sectioned = get_ld_screened_students()
        self.assertGreaterEqual(len(sectioned), 30)
        statuses = {s["ld_screening_status"] for s in sectioned}
        self.assertIn("Confirmed Support Profile", statuses)
        self.assertIn("Possibility / Early Screening", statuses)

    def test_02_homepage_and_login_expose_counselor_role(self):
        client = app.test_client()
        home_resp = client.get("/")
        self.assertEqual(home_resp.status_code, 200)
        home_html = home_resp.data.decode("utf-8")
        self.assertIn("Login as Counselor", home_html)
        self.assertIn("School Counselor", home_html)

        login_resp = client.get("/login?role=counselor")
        self.assertEqual(login_resp.status_code, 200)
        login_html = login_resp.data.decode("utf-8")
        self.assertIn("Dr. Meera Deshmukh", login_html)
        self.assertIn("Sign In as School Counselor", login_html)

    def test_03_counselor_rbac_and_dashboard(self):
        """Only counselor role may open /counselor/dashboard; counselor can also inspect student dossiers."""
        client = app.test_client()

        # Student denied Counselor Dashboard
        self._login(client, "student1", "student123")
        denied = client.get("/counselor/dashboard", follow_redirects=False)
        self.assertEqual(denied.status_code, 302)

        # Counselor succeeds
        resp = self._login(client, "counselor1", "counselor123")
        self.assertEqual(resp.status_code, 200)
        html = resp.data.decode("utf-8")
        self.assertIn("Dr. Meera Deshmukh", html)
        self.assertIn("Learning Disability", html)
        self.assertIn("Publish Simple Study Technique / Exercise", html)

        # Counselor can view child diagnostic sheet
        detail_resp = client.get("/student/SH-2026-001")
        self.assertEqual(detail_resp.status_code, 200)
        self.assertIn("Aarav Sharma", detail_resp.data.decode("utf-8"))

    def test_04_three_way_counselor_messaging_and_referral(self):
        """Verify Student, Parent, and Teacher can all contact School Counselor and receive replies."""
        stu_client = app.test_client()
        self._login(stu_client, "student1", "student123")
        stu_post = stu_client.post(
            "/student/counselor-message",
            data={
                "request_type": "Check-In",
                "subject": "UNITTEST Student Check-In Fractions",
                "message": "Ma'am, I mix up denominator and numerator in Q6.",
            },
            follow_redirects=True,
        )
        self.assertEqual(stu_post.status_code, 200)
        self.assertIn("UNITTEST Student Check-In Fractions", stu_post.data.decode("utf-8"))

        par_client = app.test_client()
        self._login(par_client, "parent1", "parent123")
        par_post = par_client.post(
            "/parent/counselor-message",
            data={
                "request_type": "Appointment Request",
                "subject": "UNITTEST Parent Slot Request",
                "message": "Please share Friday slot for reading fluency discussion.",
            },
            follow_redirects=True,
        )
        self.assertEqual(par_post.status_code, 200)
        self.assertIn("UNITTEST Parent Slot Request", par_post.data.decode("utf-8"))

        t_client = app.test_client()
        self._login(t_client, "teacher1", "teacher123")
        t_filter = t_client.get("/dashboard?ld=SECTIONED")
        self.assertEqual(t_filter.status_code, 200)
        self.assertIn("Aarav Sharma", t_filter.data.decode("utf-8"))

        t_ref = t_client.post(
            "/teacher/counselor-referral",
            data={
                "student_id": "SH-2026-001",
                "request_type": "Referral",
                "ld_screening_status": "Possibility / Early Screening",
                "ld_category": "Dyslexia / Visual Reading",
                "subject": "UNITTEST Teacher Visual Decoding Observation",
                "message": "Drops a step when word problems exceed 3 sentences.",
                "redirect_to": "dashboard",
            },
            follow_redirects=True,
        )
        self.assertEqual(t_ref.status_code, 200)

        # Counselor views & replies to the student's message
        c_client = app.test_client()
        self._login(c_client, "counselor1", "counselor123")
        msgs = get_counselor_messages(student_id="SH-2026-001")
        target = next((m for m in msgs if m["subject"] == "UNITTEST Student Check-In Fractions"), None)
        self.assertIsNotNone(target)

        reply_resp = c_client.post(
            "/counselor/reply",
            data={
                "message_id": target["id"],
                "reply_text": "Try drawing a pizza box with bottom denominator labeled Slices Total.",
            },
            follow_redirects=True,
        )
        self.assertEqual(reply_resp.status_code, 200)
        self.assertIn("pizza box with bottom denominator", reply_resp.data.decode("utf-8"))

    def test_05_counselor_exercise_publish_syncs_and_tracks_practice(self):
        """Counselor-published exercises must appear on Student & Parent portals and increment practice counter."""
        c_client = app.test_client()
        self._login(c_client, "counselor1", "counselor123")

        pub_resp = c_client.post(
            "/counselor/exercises/add",
            data={
                "title": "UNITTEST Rainbow Number Anchors",
                "target_category": "Dyslexia / Visual Reading",
                "target_audience": "Students & Parents",
                "duration_mins": "10",
                "difficulty_level": "Gentle Starter",
                "study_technique": "Color Anchoring",
                "simple_goal": "Keep multi-digit numbers neatly stacked with pastel color lines.",
                "steps_raw": "Draw light vertical columns.\nPut ones in green and tens in blue.\nDouble-check top row once.",
                "home_tip": "Use any lined notebook turned sideways.",
            },
            follow_redirects=True,
        )
        self.assertEqual(pub_resp.status_code, 200)
        self.assertIn("UNITTEST Rainbow Number Anchors", pub_resp.data.decode("utf-8"))

        exercises = get_counselor_exercises()
        created = next((e for e in exercises if e["title"] == "UNITTEST Rainbow Number Anchors"), None)
        self.assertIsNotNone(created)

        # Verify visible in Student Portal
        stu_client = app.test_client()
        self._login(stu_client, "student1", "student123")
        stu_html = stu_client.get("/portal").data.decode("utf-8")
        self.assertIn("UNITTEST Rainbow Number Anchors", stu_html)
        self.assertIn("SEHAYAK Study Buddy AI", stu_html)
        self.assertIn("student-workspace-tabs", stu_html)
        self.assertIn("drill-deck-nav", stu_html)

        # Verify visible in Parent Portal
        par_client = app.test_client()
        self._login(par_client, "parent1", "parent123")
        par_html = par_client.get("/parent/view").data.decode("utf-8")
        self.assertIn("UNITTEST Rainbow Number Anchors", par_html)
        self.assertIn("SEHAYAK Family Guidance AI", par_html)
        self.assertIn("parent-workspace-tabs", par_html)

        # Practice button updates counter
        before_count = created["practice_count"]
        prac_resp = stu_client.post(
            f"/exercise/{created['id']}/practice",
            headers={"X-Requested-With": "XMLHttpRequest"},
        )
        self.assertEqual(prac_resp.status_code, 200)
        payload = json.loads(prac_resp.data.decode("utf-8"))
        self.assertEqual(payload["status"], "success")
        self.assertEqual(payload["practice_count"], before_count + 1)

    def test_06_student_and_parent_ai_chatbots(self):
        """Verify contextual AI chatbot answers cleanly for both Student and Parent sessions."""
        # Student chatbot session
        stu_client = app.test_client()
        self._login(stu_client, "student1", "student123")

        q9_resp = stu_client.post(
            "/api/chatbot",
            json={"message": "Explain Question 9 logic in simple steps", "role": "student"},
        )
        self.assertEqual(q9_resp.status_code, 200)
        q9_data = json.loads(q9_resp.data.decode("utf-8"))
        self.assertEqual(q9_data["status"], "success")
        self.assertIn("Question 9", q9_data["answer"])
        self.assertGreater(len(q9_data["suggested_questions"]), 0)

        counselor_q = stu_client.post(
            "/api/chatbot",
            json={"message": "How can I talk to the school counselor?", "role": "student"},
        )
        self.assertIn("Dr. Meera Deshmukh", json.loads(counselor_q.data.decode("utf-8"))["answer"])

        # Parent chatbot session
        par_client = app.test_client()
        self._login(par_client, "parent1", "parent123")

        ld_resp = par_client.post(
            "/api/chatbot",
            json={"message": "What does my child's learning support profile mean?", "role": "parent"},
        )
        self.assertEqual(ld_resp.status_code, 200)
        ld_data = json.loads(ld_resp.data.decode("utf-8"))
        self.assertIn("Aarav", ld_data["answer"])
        self.assertIn("Dyslexia", ld_data["answer"])
        self.assertIn("CBSE", ld_data["answer"])

        ex_resp = par_client.post(
            "/api/chatbot",
            json={"message": "Which 10-minute exercises can we practice at home?", "role": "parent"},
        )
        self.assertEqual(ex_resp.status_code, 200)
        self.assertIn("Simple Steps", json.loads(ex_resp.data.decode("utf-8"))["answer"])

    def test_07_online_assigned_exercises_and_independent_references(self):
        """Counselor can assign online mini-lab exercises with verified references shown on Student & Parent portals."""
        c_client = app.test_client()
        self._login(c_client, "counselor1", "counselor123")

        pub_resp = c_client.post(
            "/counselor/exercises/add",
            data={
                "title": "UNITTEST Interactive Balance Equation Lab",
                "target_category": "Dyscalculia / Math Reasoning",
                "target_audience": "Students & Parents",
                "duration_mins": "10",
                "difficulty_level": "Gentle Starter",
                "study_technique": "Balanced Scale Logic",
                "assigned_student_id": "SH-2026-001",
                "interactive_tool": "algebra_balance",
                "external_site_name": "PhET Equality Explorer",
                "external_practice_url": "https://phet.colorado.edu/sims/html/equality-explorer/latest/equality-explorer_en.html",
                "reference_source_name": "PhET Interactive Simulations (CU Boulder)",
                "reference_url": "https://phet.colorado.edu/sims/html/equality-explorer/latest/equality-explorer_en.html",
                "reference_summary": "Visual interactive scale model showing why both sides of an equation change together.",
                "simple_goal": "Keep both sides of an equation equal using interactive tiles.",
                "steps_raw": "Place numbers on both pans.\nNotice what makes the scale tilt.\nBalance both sides step by step.",
                "home_tip": "Ask your child what happens when you take the same coin away from both hands.",
            },
            follow_redirects=True,
        )
        self.assertEqual(pub_resp.status_code, 200)
        self.assertIn("UNITTEST Interactive Balance Equation Lab", pub_resp.data.decode("utf-8"))

        # Verify Student Portal shows assigned exercise, interactive modal, and external redirect link
        stu_client = app.test_client()
        self._login(stu_client, "student1", "student123")
        stu_html = stu_client.get("/portal").data.decode("utf-8")
        self.assertIn("UNITTEST Interactive Balance Equation Lab", stu_html)
        self.assertIn("Assigned for You", stu_html)
        self.assertIn("Launch Online Exercise Here", stu_html)
        self.assertIn("online-lab-modal", stu_html)
        self.assertIn("https://apps.mathlearningcenter.org/fractions", stu_html)
        self.assertIn("https://phet.colorado.edu/sims/html/equality-explorer/latest/equality-explorer_en.html", stu_html)

        # Verify Parent Portal shows assigned badge, cited reference box, and Independent Research section
        par_client = app.test_client()
        self._login(par_client, "parent1", "parent123")
        par_html = par_client.get("/parent/view").data.decode("utf-8")
        self.assertIn("UNITTEST Interactive Balance Equation Lab", par_html)
        self.assertIn("Assigned for Aarav Sharma", par_html)
        self.assertIn("Taken as Reference From:", par_html)
        self.assertIn("PhET Interactive Simulations (CU Boulder)", par_html)
        self.assertIn("independent-research", par_html)
        for org_name in (
            "Understood.org",
            "Reading Rockets",
            "PhET",
            "The Math Learning Center",
            "CBSE Official Portal",
        ):
            self.assertIn(org_name, par_html)

        # Verify Parent AI Chatbot provides trusted independent research links
        ref_resp = par_client.post(
            "/api/chatbot",
            json={"message": "Which trusted websites and research references can I read?", "role": "parent"},
        )
        self.assertEqual(ref_resp.status_code, 200)
        ref_answer = json.loads(ref_resp.data.decode("utf-8"))["answer"]
        self.assertIn("https://www.understood.org/", ref_answer)
        self.assertIn("https://www.readingrockets.org/", ref_answer)
        self.assertIn("https://www.mathlearningcenter.org/apps", ref_answer)
        self.assertIn("https://phet.colorado.edu/sims/html/equality-explorer/latest/equality-explorer_en.html", ref_answer)

    def test_08_counselor_mark_priority_monitoring_not_priority(self):
        """Counselor can mark any student Priority, Monitoring, or Not Priority from dashboard or student dossier."""
        stu_client = app.test_client()
        self._login(stu_client, "student1", "student123")
        unauth_resp = stu_client.post(
            "/counselor/set-priority",
            data={"student_id": "SH-2026-001", "counselor_priority": "Not Priority"},
            follow_redirects=False,
        )
        self.assertEqual(unauth_resp.status_code, 302)

        c_client = app.test_client()
        self._login(c_client, "counselor1", "counselor123")
        dash_html = c_client.get("/counselor/dashboard").data.decode("utf-8")
        self.assertIn("/counselor/set-priority", dash_html)
        self.assertIn("Browse All 300 Students to Mark Priority", dash_html)
        self.assertIn("Not Priority", dash_html)

        target_stu = next(
            s for s in get_all_students()
            if (s.get("counselor_priority") or "Not Priority") == "Not Priority"
            and (s.get("ld_screening_status") or "None") == "None"
        )
        sid = target_stu["student_id"]
        orig_referred = target_stu.get("counselor_referred") or 0

        try:
            # 1. Mark previously unflagged student as Priority
            r1 = c_client.post(
                "/counselor/set-priority",
                data={"student_id": sid, "counselor_priority": "Priority", "scope": "all"},
                follow_redirects=True,
            )
            self.assertEqual(r1.status_code, 200)
            self.assertEqual(get_student_by_id(sid)["counselor_priority"], "Priority")
            self.assertIn(f"Marked {target_stu['name']} ({sid}) as Priority.", r1.data.decode("utf-8"))

            # Appears in Priority filter roster automatically
            prio_list = c_client.get("/counselor/dashboard?priority=Priority").data.decode("utf-8")
            self.assertIn(sid, prio_list)

            # 2. Switch to Monitoring via JSON/AJAX endpoint
            r2 = c_client.post(
                "/counselor/set-priority",
                json={"student_id": sid, "counselor_priority": "Monitoring"},
                headers={"X-Requested-With": "XMLHttpRequest"},
            )
            self.assertEqual(r2.status_code, 200)
            self.assertEqual(json.loads(r2.data.decode("utf-8"))["counselor_priority"], "Monitoring")
            self.assertEqual(get_student_by_id(sid)["counselor_priority"], "Monitoring")

            # 3. Switch via Student Dossier page (/student/<id>) to Not Priority
            detail_html = c_client.get(f"/student/{sid}").data.decode("utf-8")
            self.assertIn("Counselor Triage: Mark Priority, Monitoring, or Not Priority", detail_html)

            r3 = c_client.post(
                "/counselor/set-priority",
                data={"student_id": sid, "counselor_priority": "Not Priority", "redirect_to": "detail"},
                follow_redirects=True,
            )
            self.assertEqual(r3.status_code, 200)
            self.assertEqual(get_student_by_id(sid)["counselor_priority"], "Not Priority")
            self.assertIn("Counselor Status: Not Priority", r3.data.decode("utf-8"))
        finally:
            conn = get_connection()
            conn.execute(
                "UPDATE students SET counselor_priority = 'Not Priority', counselor_referred = ? WHERE student_id = ?",
                (orig_referred, sid),
            )
            conn.commit()
            conn.close()


if __name__ == "__main__":
    unittest.main()
