"""
SEHAYAK (सहायक) - Report Generation & Export Module
Exports student analytics to downloadable CSV datasets
and generates print-ready individual remedial dossiers for PTMs.
"""

import io
import csv

def generate_students_csv(students):
    """Generate in-memory CSV file of student analytics."""
    output = io.StringIO()
    if not students:
        return output.getvalue()

    fieldnames = [
        "student_id", "name", "grade", "section", "gender",
        "risk_level", "risk_score", "support_needed",
        "overall_avg", "trend_slope", "attendance_rate",
        "assignment_completion_rate", "reading_speed_wpm",
        "math_sa2", "science_sa2", "english_sa2", "social_sa2", "hindi_sa2"
    ]

    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for s in students:
        writer.writerow(s)

    return output.getvalue()
