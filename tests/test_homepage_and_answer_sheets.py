"""
Unit Tests for Homepage, Demographic Portals, CBSE Front-Cover Answer Sheet Rubric,
and Teacher Qualitative Remarks (Weaknesses & Improvements).
Ministry of Education - Problem Statement #PSB152
"""

import unittest
from app import app
from utils.db import init_db, get_student_by_id, get_question_papers, get_student_answer_sheets

class TestHomepageAndAnswerSheets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()

    def setUp(self):
        self.app = app
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def login(self, username, password):
        return self.client.post("/login", data={
            "username": username,
            "password": password
        }, follow_redirects=True)

    def test_homepage_rendering_and_demographics(self):
        """Verify public landing page describes features and demographics with 4 login buttons."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")

        # Check App Title and MoE Statement ID
        self.assertIn("SEHAYAK", html)
        self.assertIn("PSB152", html)

        # Check 4 Role Login Buttons
        self.assertIn("Login as Teacher", html)
        self.assertIn("Login as Student", html)
        self.assertIn("Login as Parent", html)
        self.assertIn("Login as Principal", html)

        # Check demographic descriptions
        self.assertIn("For Classroom Teachers", html)
        self.assertIn("For Students & Children", html)
        self.assertIn("For Parents & Families", html)
        self.assertIn("For School Leadership", html)

        # Check specific feature highlights
        self.assertIn("CBSE Front-Sheet Grading", html)
        self.assertIn("Dual-Engine Explainable AI", html)
        self.assertIn("WCAG 2.1 AA/AAA Dyslexia Suite", html)

    def test_login_role_preselection(self):
        """Verify login page supports role parameter for pre-selecting demographic tabs."""
        response = self.client.get("/login?role=parent")
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")
        self.assertIn("Sign In as Parent", html)

        response_student = self.client.get("/login?role=student")
        self.assertEqual(response_student.status_code, 200)
        self.assertIn("Sign In as Student", response_student.data.decode("utf-8"))

    def test_question_papers_flow(self):
        """Test teacher can view and register question papers with 30-question sequence."""
        self.login("teacher1", "teacher123")

        # GET Question Papers
        res_get = self.client.get("/teacher/question-papers")
        self.assertEqual(res_get.status_code, 200)
        self.assertIn("Curriculum Question Papers Repository", res_get.data.decode("utf-8"))

        # POST New Question Paper
        res_post = self.client.post("/teacher/question-papers", data={
            "title": "Unit Test 2 - Mathematics",
            "subject": "Mathematics",
            "grade": "Class 7",
            "exam_name": "Unit Test 2026-27"
        }, follow_redirects=True)
        self.assertEqual(res_post.status_code, 200)
        self.assertIn("Unit Test 2 - Mathematics", res_post.data.decode("utf-8"))

    def test_answer_sheet_upload_and_rubric_view(self):
        """Test answer sheet front-page upload, 1-15 marks tabulation, and teacher remarks."""
        self.login("teacher1", "teacher123")

        # GET Upload Page
        res_get = self.client.get("/teacher/answer-sheet/upload")
        self.assertEqual(res_get.status_code, 200)
        self.assertIn("Upload & Grade Student Answer Sheet Front-Cover", res_get.data.decode("utf-8"))

        # Prepare 1 to 15 question marks according to rubric:
        # Q1-Q5: 1M each, Q6-Q10: 2M each, Q11-Q13: 5M each, Q14-Q15: 10M each
        form_data = {
            "student_id": "SH-2026-001",
            "question_paper_id": "1",
            "subject": "Mathematics",
            "exam_name": "Mid-Term Examination 2026",
            "roll_no": "2026001",
            "medium": "English",
            "teacher_weaknesses": "Questions 4, 9, 14: Misapplied fractional division rules; signs of reading fatigue.",
            "teacher_improvements": "Questions 1-3, 6, 11: Clear improvement in geometry calculations and neat step layout.",
            "teacher_general_remarks": "Provide visual fraction bars for homework; pair with study buddy.",
            "examiner_name": "Mrs. Ananya Sharma"
        }
        for q in range(1, 16):
            if q <= 5:
                form_data[f"q_{q}"] = "1.0"
            elif q <= 10:
                form_data[f"q_{q}"] = "1.5"
            elif q <= 13:
                form_data[f"q_{q}"] = "4.0"
            else:
                form_data[f"q_{q}"] = "8.5"

        # POST Answer Sheet
        res_post = self.client.post("/teacher/answer-sheet/upload", data=form_data, follow_redirects=True)
        self.assertEqual(res_post.status_code, 200)
        post_html = res_post.data.decode("utf-8")

        # Verify Front Cover Rubric Elements
        self.assertIn("CENTRAL MODEL SENIOR SECONDARY SCHOOL", post_html)
        self.assertIn("Candidate's Roll No.", post_html)
        self.assertIn("Total Marks Obtained", post_html)
        # Verify marks are rendered (not blank or dashes)
        self.assertIn("1.0", post_html)
        self.assertIn("1.5", post_html)

        # Verify Teacher Qualitative Remarks
        self.assertIn("Where Weaknesses & Gaps Were Observed:", post_html)
        self.assertIn("Misapplied fractional division rules", post_html)
        self.assertIn("Where Improvements & Growth Were Observed:", post_html)
        self.assertIn("Clear improvement in geometry calculations", post_html)

    def test_student_detail_remarks_update(self):
        """Test teacher can directly update observed weaknesses and improvements on student dossier."""
        self.login("teacher1", "teacher123")

        res_update = self.client.post("/student/SH-2026-001/update-remarks", data={
            "teacher_weaknesses": "Needs extra practice in decimal multiplication.",
            "teacher_improvements": "Pronunciation and reading speed have increased by 12 WPM.",
            "teacher_remarks": "Continue encouraging paired oral reading."
        }, follow_redirects=True)
        self.assertEqual(res_update.status_code, 200)

        # Verify database update
        student = get_student_by_id("SH-2026-001")
        self.assertEqual(student["teacher_weaknesses"], "Needs extra practice in decimal multiplication.")
        self.assertEqual(student["teacher_improvements"], "Pronunciation and reading speed have increased by 12 WPM.")

    def test_parent_portal_answer_sheet_and_remarks_display(self):
        """Test parent portal displays child's answer sheet link and teacher observed weaknesses/improvements."""
        # Login as Parent 1 (associated with student SH-2026-001)
        self.login("parent1", "parent123")

        res = self.client.get("/parent/view")
        self.assertEqual(res.status_code, 200)
        html = res.data.decode("utf-8")

        # Check that answer sheet & remarks section is rendered
        self.assertIn("Evaluated Examination Answer Sheet", html)
        self.assertIn("Teacher Observed Weaknesses & Learning Gaps:", html)
        self.assertIn("Teacher Observed Improvements & Growth:", html)

if __name__ == "__main__":
    unittest.main()
