"""
Unit tests for SEHAYAK Risk Engine, Explainability & SHAP-Style Attributions
"""

import unittest
from models.rule_engine import evaluate_student_rules
from models.risk_model import predict_student_risk, calculate_feature_contributions
from models.explainability import generate_student_explanation_card

class TestRiskEngine(unittest.TestCase):

    def test_high_risk_flagged_for_critical_attendance(self):
        student = {
            "student_id": "TEST-CRIT-ATT",
            "name": "Absentee Learner",
            "attendance_rate": 55.0,  # Critical attendance deficit (<65)
            "assignment_completion_rate": 45.0,
            "math_sa2": 45.0,
            "science_sa2": 45.0,
            "english_sa2": 50.0,
            "social_sa2": 50.0,
            "hindi_sa2": 50.0
        }

        result = evaluate_student_rules(student)
        self.assertEqual(result["risk_level"], "HIGH")
        self.assertEqual(result["support_needed"], 1)
        self.assertTrue(any("attendance" in r.lower() for r in result["reasons_en"]))

    def test_feature_contributions_attribution(self):
        student = {
            "student_id": "TEST-ATTR",
            "attendance_rate": 62.0,  # Below 75% -> should produce positive risk impact
            "assignment_completion_rate": 50.0,
            "reading_speed_wpm": 72.0,
            "math_sa2": 32.0,
            "trend_slope": -14.0
        }
        factors = calculate_feature_contributions(student)
        self.assertTrue(len(factors) > 0)
        names = [f["name"] for f in factors]
        self.assertIn("Attendance Deficit", names)
        # Check that attendance impact is positive (risk driver)
        att_factor = next(f for f in factors if f["name"] == "Attendance Deficit")
        self.assertGreater(att_factor["impact"], 0)

    def test_low_risk_for_stable_student(self):
        student = {
            "student_id": "TEST-OK",
            "name": "Steady Learner",
            "attendance_rate": 94.0,
            "assignment_completion_rate": 92.0,
            "class_participation": 4.5,
            "reading_speed_wpm": 140.0,
            "math_sa2": 82.0,
            "science_sa2": 85.0,
            "english_sa2": 78.0,
            "social_sa2": 80.0,
            "hindi_sa2": 79.0
        }

        result = evaluate_student_rules(student)
        self.assertEqual(result["risk_level"], "LOW")
        self.assertEqual(result["support_needed"], 0)
        self.assertTrue(len(result["strengths_en"]) > 0)

    def test_explainability_card_generation(self):
        student = {
            "student_id": "EX-01",
            "name": "Sample Student",
            "attendance_rate": 80.0,
            "assignment_completion_rate": 75.0,
            "trend_slope": -5.0,
            "reading_speed_wpm": 110.0,
            "class_participation": 3.0
        }
        eval_res = predict_student_risk(student)
        card_en = generate_student_explanation_card(eval_res, student, lang="en")
        card_hi = generate_student_explanation_card(eval_res, student, lang="hi")

        self.assertIn("summary_header", card_en)
        self.assertIn("takeaway", card_en)
        self.assertIn("contributions", card_en)
        self.assertIn("summary_header", card_hi)
        self.assertIn("takeaway", card_hi)

if __name__ == "__main__":
    unittest.main()
