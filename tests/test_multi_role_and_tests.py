"""
Unit tests for SEHAYAK Multi-Role Architecture, 30-Marks Test Engine & Parent-Teacher Messaging
"""

import unittest
from utils.db import (
    init_db, get_connection, get_all_students, get_principal_analytics,
    send_teacher_parent_message, reply_teacher_parent_message,
    get_messages_for_parent, get_messages_for_teacher,
    save_test_attempt_db, get_student_test_attempts
)
from utils.auth import authenticate_user
from remedial.test_bank import get_test_for_subject, grade_test_submission

class TestMultiRoleAndAssessments(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()

    def test_principal_and_3_teachers_3_students_3_parents_authentication(self):
        # 1. Principal
        principal = authenticate_user("principal", "principal123")
        self.assertIsNotNone(principal)
        self.assertEqual(principal["role"], "principal")

        # 2. At least 3 Teachers
        for t_user in ["teacher1", "teacher2", "teacher3"]:
            t = authenticate_user(t_user, "teacher123")
            self.assertIsNotNone(t, f"Failed auth for {t_user}")
            self.assertEqual(t["role"], "teacher")

        # 3. At least 3 Students
        for s_user in ["student1", "student2", "student3"]:
            s = authenticate_user(s_user, "student123")
            self.assertIsNotNone(s, f"Failed auth for {s_user}")
            self.assertEqual(s["role"], "student")

        # 4. At least 3 Parents
        for p_user in ["parent1", "parent2", "parent3"]:
            p = authenticate_user(p_user, "parent123")
            self.assertIsNotNone(p, f"Failed auth for {p_user}")
            self.assertEqual(p["role"], "parent")

    def test_teacher_100_students_isolation(self):
        # Each teacher manages exactly 100 students
        t1_students = get_all_students(teacher_id="teacher1")
        t2_students = get_all_students(teacher_id="teacher2")
        t3_students = get_all_students(teacher_id="teacher3")

        self.assertEqual(len(t1_students), 100)
        self.assertEqual(len(t2_students), 100)
        self.assertEqual(len(t3_students), 100)

        # Principal sees all 300 students
        all_students = get_all_students(teacher_id=None)
        self.assertEqual(len(all_students), 300)

    def test_cbse_30_marks_test_bank_and_grading(self):
        for sub in ["mathematics", "science", "social science", "english", "hindi"]:
            test_data = get_test_for_subject(sub)
            self.assertEqual(len(test_data["mcqs"]), 15, f"{sub} should have 15 MCQs")
            self.assertEqual(len(test_data["written"]), 5, f"{sub} should have 5 written questions")

        # Test grading function with mock inputs
        mcq_answers = {"m_mcq_1": "1", "m_mcq_2": "0"}  # 2 correct
        written_answers = {
            "m_w_1": "A prime number has only two factors 1 and itself like 5 while composite has many factors like 6.",
            "m_w_2": "Profit is selling price minus cost price so 250 minus 200 equals 50 rupees."
        }
        res = grade_test_submission("mathematics", mcq_answers, written_answers)

        self.assertEqual(res["max_score"], 30)
        self.assertGreater(res["total_score"], 0)
        self.assertIn("badge", res)
        self.assertEqual(len(res["detailed_mcq"]), 15)
        self.assertEqual(len(res["detailed_written"]), 5)

    def test_parent_teacher_messaging_and_principal_exclusion(self):
        # Parent sends query to teacher
        send_teacher_parent_message(
            student_id="SH-2026-001",
            teacher_id="teacher1",
            parent_username="parent1",
            sender_role="parent",
            sender_name="Mr. Suresh Sharma",
            subject="Reading Support Query",
            message="How is Aarav responding to the Lexend typography?"
        )

        parent_msgs = get_messages_for_parent("SH-2026-001")
        self.assertTrue(len(parent_msgs) > 0)
        latest_id = parent_msgs[0]["id"]

        # Teacher replies to query
        reply_teacher_parent_message(latest_id, "Aarav is reading with much better confidence and reduced fatigue!")
        teacher_msgs = get_messages_for_teacher("teacher1")
        self.assertTrue(any(m["id"] == latest_id and m["status"] == "Replied" for m in teacher_msgs))

        # Principal analytics does NOT include or expose messages (Privacy check)
        p_analytics = get_principal_analytics()
        self.assertNotIn("messages", p_analytics)
        self.assertNotIn("teacher_parent_messages", p_analytics)

if __name__ == "__main__":
    unittest.main()
