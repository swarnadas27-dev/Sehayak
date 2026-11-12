"""
Unit tests for SEHAYAK AI Dyslexia Learning Logic & Paper Improvement Engine.
Validates:
 1. Weak question mark detection from evaluated 15-question front sheets
 2. Dyslexia-specific logic rules (CRA models, visual metaphors, step-by-step thinking)
 3. Targeted mirror practice drills with zero-anxiety feedback
 4. AI-guided paper coaching and exam hacks
 5. API endpoint (/api/ai-explain-question) and Student Portal rendering
"""

import unittest
from app import app
from utils.db import init_db, get_student_answer_sheets
from remedial.ai_tutor import (
    MATH_15Q_LOGIC_BANK,
    get_question_logic_detail,
    analyze_student_paper_performance
)

class TestAITutorAndLogic(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()

    def setUp(self):
        self.app = app
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_math_15q_logic_bank_integrity(self):
        """Ensure all 15 questions have complete dyslexia logic, steps, and valid drills."""
        self.assertEqual(len(MATH_15Q_LOGIC_BANK), 15)
        for q_num in range(1, 16):
            item = get_question_logic_detail(q_num, "Mathematics")
            self.assertEqual(item["q"], q_num)
            self.assertIn("concept", item)
            self.assertIn("logic_name", item)
            self.assertIn("visual_metaphor", item)
            self.assertIn("dyslexia_barrier", item)
            self.assertGreaterEqual(len(item["steps"]), 3)

            # Drill verification
            drill = item["drill"]
            self.assertIn("prompt", drill)
            self.assertIn("options", drill)
            self.assertGreaterEqual(len(drill["options"]), 2)
            self.assertIn("correct_index", drill)
            self.assertTrue(0 <= drill["correct_index"] < len(drill["options"]))
            self.assertIn("hint", drill)
            self.assertIn("explanation", drill)

    def test_analyze_student_paper_performance(self):
        """Test paper diagnostics correctly identifies dropped marks and generates improvement plan."""
        res = analyze_student_paper_performance(student_id="SH-2026-001", target_subject="Mathematics")
        coaching = res["coaching"]

        self.assertIn("Mathematics", coaching["subject"])
        self.assertGreater(coaching["total_obtained"], 0)
        self.assertEqual(coaching["total_max"], 50.0)
        self.assertGreater(coaching["total_recoverable_marks"], 0)
        self.assertGreater(coaching["target_next_score"], coaching["total_obtained"])
        self.assertEqual(len(coaching["exam_hacks"]), 4)

        # Check weak vs strong separation
        self.assertGreater(len(res["weak_questions"]), 0)
        self.assertGreater(len(res["strong_questions"]), 0)

        # Confirm weak questions have lost marks and associated logic
        first_weak = res["weak_questions"][0]
        self.assertGreater(first_weak["lost_marks"], 0)
        self.assertIn("logic", first_weak)
        self.assertIn("logic_name", first_weak["logic"])

    def test_ai_explain_api_endpoint(self):
        """Test API endpoint returns valid JSON structure for requested questions."""
        # Test Question 3 (Fraction Division / KCF Model)
        res_q3 = self.client.get("/api/ai-explain-question?q=3&subject=Mathematics")
        self.assertEqual(res_q3.status_code, 200)
        data3 = res_q3.get_json()
        self.assertEqual(data3["status"], "success")
        self.assertEqual(data3["data"]["q"], 3)
        self.assertIn("KCF", data3["data"]["logic_name"])
        self.assertIn("drill", data3["data"])

        # Test Question 14 (Data Handling / Finger Ruler Protocol)
        res_q14 = self.client.get("/api/ai-explain-question?q=14&subject=Mathematics")
        self.assertEqual(res_q14.status_code, 200)
        data14 = res_q14.get_json()
        self.assertEqual(data14["status"], "success")
        self.assertEqual(data14["data"]["q"], 14)
        self.assertIn("Axis", data14["data"]["logic_name"])

    def test_student_portal_renders_ai_paper_clinic(self):
        """Test student portal renders the AI paper improvement coach and logic practice cards."""
        # Log in as student
        with self.client.session_transaction() as sess:
            sess["user"] = {
                "username": "student1",
                "role": "student",
                "full_name": "Aarav Sharma",
                "student_id": "SH-2026-001"
            }

        response = self.client.get("/portal")
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")

        # Check core section headings
        self.assertIn("AI Learning Logic & Paper Clinic", html)
        self.assertIn("How to Improve on Your Mathematics Paper", html)
        self.assertIn("Questions Where Marks Were Dropped", html)
        self.assertIn("Apply This Logic", html)
        self.assertIn("Practice This Logic (Instant Check)", html)
        self.assertIn("4 AI Dyslexia Hacks to Improve Your Next Paper", html)
        self.assertIn("Explore AI Thinking Logic for Any Question (Q1 to Q15)", html)

        # Test alias route /student-portal also works identically
        res_alias = self.client.get("/student-portal")
        self.assertEqual(res_alias.status_code, 200)

if __name__ == "__main__":
    unittest.main()
