"""
SEHAYAK (सहायक) - Data Cleaning and Validation Module
Cleans incoming CSV assessment data, handles missing values,
validates schema boundaries, and computes derived pedagogical indicators.
"""

import math
from config import SUBJECTS, FAILING_MARK_THRESHOLD, CRITICAL_ATTENDANCE_THRESHOLD, LOW_ASSIGNMENT_THRESHOLD

REQUIRED_IDENTIFIERS = ["student_id", "name"]
DEFAULT_SUBJECTS = ["math", "science", "english", "social", "hindi"]

def safe_float(val, default=0.0):
    """Convert value to float safely; handles empty strings and None."""
    if val is None or val == "":
        return default
    try:
        f = float(val)
        return 0.0 if math.isnan(f) else f
    except (ValueError, TypeError):
        return default

def clean_student_records(records):
    """
    Clean a list of student dictionary records or uploaded CSV rows.
    Returns:
        cleaned_records (list of dict): standardized, validated, and enriched records.
        summary_stats (dict): stats about anomalies, missing values, and rows processed.
    """
    cleaned = []
    anomalies_detected = 0

    for idx, raw in enumerate(records):
        student_id = str(raw.get("student_id", f"STU-{idx+1:04d}")).strip()
        name = str(raw.get("name", f"Student {idx+1}")).strip()
        grade = str(raw.get("grade", "Class 8")).strip()
        section = str(raw.get("section", "A")).strip().upper()
        gender = str(raw.get("gender", "Unspecified")).strip()
        teacher_id = str(raw.get("teacher_id", "teacher1")).strip()

        # Engagement and Behavioral attributes
        attendance = safe_float(raw.get("attendance_rate", raw.get("attendance", 85.0)), 85.0)
        attendance = max(0.0, min(100.0, attendance))

        assignment_rate = safe_float(raw.get("assignment_completion_rate", raw.get("assignment_rate", 80.0)), 80.0)
        assignment_rate = max(0.0, min(100.0, assignment_rate))

        homework_acc = safe_float(raw.get("homework_accuracy", 75.0), 75.0)
        homework_acc = max(0.0, min(100.0, homework_acc))

        participation = safe_float(raw.get("class_participation", 3.0), 3.0)
        participation = max(1.0, min(5.0, participation))

        reading_wpm = safe_float(raw.get("reading_speed_wpm", 120.0), 120.0)
        visual_pref = str(raw.get("visual_preference", "Standard")).capitalize()

        # Subject scores
        scores = {}
        subject_averages = {}
        failing_subjects = []

        for sub in DEFAULT_SUBJECTS:
            fa1 = safe_float(raw.get(f"{sub}_fa1"), None)
            sa1 = safe_float(raw.get(f"{sub}_sa1"), None)
            fa2 = safe_float(raw.get(f"{sub}_fa2"), None)
            sa2 = safe_float(raw.get(f"{sub}_sa2"), None)

            # If specific assessment columns are missing, check generic subject column
            if sa2 is None and sub in raw:
                sa2 = safe_float(raw.get(sub), 60.0)
            if sa1 is None: sa1 = sa2 if sa2 is not None else 60.0
            if fa1 is None: fa1 = sa1
            if fa2 is None: fa2 = sa2 if sa2 is not None else sa1

            scores[f"{sub}_fa1"] = round(fa1, 1)
            scores[f"{sub}_sa1"] = round(sa1, 1)
            scores[f"{sub}_fa2"] = round(fa2, 1)
            scores[f"{sub}_sa2"] = round(sa2, 1)

            sub_avg = (fa1 + sa1 + fa2 + sa2) / 4.0
            subject_averages[sub] = round(sub_avg, 1)

            if sa2 < FAILING_MARK_THRESHOLD or sub_avg < FAILING_MARK_THRESHOLD:
                failing_subjects.append(sub)

        # Aggregate calculations
        term1_avg = sum(scores[f"{s}_sa1"] for s in DEFAULT_SUBJECTS) / len(DEFAULT_SUBJECTS)
        term2_avg = sum(scores[f"{s}_sa2"] for s in DEFAULT_SUBJECTS) / len(DEFAULT_SUBJECTS)
        overall_avg = round((term1_avg + term2_avg) / 2.0, 1)
        trend_slope = round(term2_avg - term1_avg, 1)

        # Learning gap indicators
        attendance_flag = 1 if attendance < CRITICAL_ATTENDANCE_THRESHOLD else 0
        assignment_flag = 1 if assignment_rate < LOW_ASSIGNMENT_THRESHOLD else 0
        reading_lag_flag = 1 if reading_wpm < 95.0 else 0
        failing_count = len(failing_subjects)

        cleaned_row = {
            "student_id": student_id,
            "name": name,
            "grade": grade,
            "section": section,
            "teacher_id": teacher_id,
            "gender": gender,
            "attendance_rate": attendance,
            "assignment_completion_rate": assignment_rate,
            "homework_accuracy": homework_acc,
            "class_participation": participation,
            "reading_speed_wpm": reading_wpm,
            "visual_preference": visual_pref,
            **scores,
            **{f"{k}_avg": v for k, v in subject_averages.items()},
            "term1_avg": round(term1_avg, 1),
            "term2_avg": round(term2_avg, 1),
            "overall_avg": overall_avg,
            "trend_slope": trend_slope,
            "failing_subjects_count": failing_count,
            "failing_subjects_list": failing_subjects,
            "attendance_flag": attendance_flag,
            "assignment_flag": assignment_flag,
            "reading_lag_flag": reading_lag_flag,
            "archetype": raw.get("archetype", "General")
        }
        cleaned.append(cleaned_row)

    stats = {
        "total_records": len(cleaned),
        "anomalies_detected": anomalies_detected,
        "avg_attendance": round(sum(r["attendance_rate"] for r in cleaned) / max(1, len(cleaned)), 1),
        "avg_score": round(sum(r["overall_avg"] for r in cleaned) / max(1, len(cleaned)), 1)
    }

    return cleaned, stats
