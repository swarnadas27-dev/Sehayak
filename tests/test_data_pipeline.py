"""
Unit tests for SEHAYAK Data Generation and Cleaning Pipeline
"""

import unittest
import os
import tempfile
import csv
from utils.data_generator import generate_synthetic_dataset
from utils.data_cleaner import clean_student_records, safe_float

class TestDataPipeline(unittest.TestCase):

    def test_safe_float(self):
        self.assertEqual(safe_float("85.5"), 85.5)
        self.assertEqual(safe_float("", 10.0), 10.0)
        self.assertEqual(safe_float(None, 0.0), 0.0)
        self.assertEqual(safe_float("invalid", 5.0), 5.0)

    def test_synthetic_generator_creates_dataset(self):
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            generate_synthetic_dataset(num_students=30, output_path=tmp_path)
            self.assertTrue(os.path.exists(tmp_path))

            with open(tmp_path, "r", encoding="utf-8") as f:
                reader = list(csv.DictReader(f))
                self.assertEqual(len(reader), 30)
                # Verify required columns exist
                first_row = reader[0]
                self.assertIn("student_id", first_row)
                self.assertIn("name", first_row)
                self.assertIn("attendance_rate", first_row)
                self.assertIn("math_sa2", first_row)
                self.assertIn("overall_avg", first_row)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_data_cleaner_clamps_and_computes_metrics(self):
        raw_samples = [
            {
                "student_id": "TEST-001",
                "name": "Test Student",
                "grade": "8",
                "attendance_rate": "120",  # Out of range, should clamp to 100
                "assignment_completion_rate": "-10",  # Clamps to 0
                "math_sa1": "50",
                "math_sa2": "30",
                "science_sa1": "60",
                "science_sa2": "60",
                "english_sa1": "70",
                "english_sa2": "70",
                "social_sa1": "65",
                "social_sa2": "65",
                "hindi_sa1": "80",
                "hindi_sa2": "80"
            }
        ]

        cleaned, stats = clean_student_records(raw_samples)
        self.assertEqual(len(cleaned), 1)
        record = cleaned[0]

        self.assertEqual(record["attendance_rate"], 100.0)
        self.assertEqual(record["assignment_completion_rate"], 0.0)
        self.assertEqual(record["failing_subjects_count"], 1)  # math_sa2 is 30 (< 35)
        self.assertIn("math", record["failing_subjects_list"])

if __name__ == "__main__":
    unittest.main()
