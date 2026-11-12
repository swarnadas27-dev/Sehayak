"""
Unit tests for SEHAYAK Remedial Recommendation Engine & Practice Bank
"""

import unittest
from remedial.plan_generator import generate_remedial_plan
from remedial.strategy_catalog import STRATEGY_CATALOG
from remedial.practice_bank import get_practice_questions

class TestRemedialEngine(unittest.TestCase):

    def test_plan_includes_multisensory_math_for_math_struggles(self):
        student = {
            "student_id": "STU-MTH",
            "name": "Math Student",
            "grade": "8",
            "section": "A",
            "attendance_rate": 88.0,
            "assignment_completion_rate": 80.0,
            "reading_speed_wpm": 130.0
        }
        student_eval = {
            "risk_level": "MODERATE",
            "weak_subjects": ["Mathematics"]
        }

        plan = generate_remedial_plan(student, student_eval, lang="en")
        strat_ids = [s["id"] for s in plan["strategies"]]
        self.assertIn("MS-MTH", strat_ids)  # Multisensory math
        self.assertEqual(len(plan["four_week_plan"]), 4)
        # Check task structure with deterministic IDs
        first_week = plan["four_week_plan"][0]
        self.assertIn("tasks", first_week)
        self.assertTrue(len(first_week["tasks"]) > 0)
        self.assertTrue(first_week["tasks"][0]["id"].startswith("w1_a"))

    def test_plan_includes_phonics_for_reading_barriers(self):
        student = {
            "student_id": "STU-READ",
            "name": "Reading Student",
            "grade": "7",
            "section": "B",
            "attendance_rate": 85.0,
            "assignment_completion_rate": 70.0,
            "reading_speed_wpm": 75.0  # Slow reading speed (<95)
        }
        student_eval = {
            "risk_level": "MODERATE",
            "weak_subjects": ["English"]
        }

        plan = generate_remedial_plan(student, student_eval, lang="en")
        strat_ids = [s["id"] for s in plan["strategies"]]
        self.assertIn("DY-PHN", strat_ids)  # Structured Phonics & Dyslexia support

    def test_bilingual_plan_generation(self):
        student = {"student_id": "STU-HI", "name": "Aarav", "grade": "8", "section": "A"}
        student_eval = {"risk_level": "HIGH", "weak_subjects": ["Mathematics"]}
        plan_hi = generate_remedial_plan(student, student_eval, lang="hi")

        self.assertEqual(len(plan_hi["four_week_plan"]), 4)
        self.assertIn("सप्ताह 1", plan_hi["four_week_plan"][0]["title"])

    def test_practice_bank_returns_questions(self):
        all_q = get_practice_questions("all")
        self.assertGreaterEqual(len(all_q), 5)

        math_q = get_practice_questions("mathematics")
        self.assertGreaterEqual(len(math_q), 1)
        self.assertEqual(math_q[0]["subject"], "Mathematics")
        self.assertIn("options_en", math_q[0])
        self.assertIn("correct_index", math_q[0])

if __name__ == "__main__":
    unittest.main()
