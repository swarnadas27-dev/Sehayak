"""
SEHAYAK (सहायक) - Synthetic Student Assessment Data Generator
Generates realistic Indian school assessment datasets (300 students)
distributed evenly across 3 teachers (100 students per teacher):
 - Teacher 1 (teacher1): Class 7 (100 students)
 - Teacher 2 (teacher2): Class 8 (100 students)
 - Teacher 3 (teacher3): Class 9 (100 students)

Reflects 4 distinct learning profiles:
 1. Typical / On-Track Learners (~55%)
 2. Reading/Language Support Profile / Dyslexia indicator (~15%)
 3. Attendance-Driven Academic Lag (~15%)
 4. Specific STEM / Foundation Concept Barrier (~15%)
"""

import os
import random
import csv
import math

FIRST_NAMES_M = [
    "Aarav", "Vihaan", "Aditya", "Rohan", "Kabir", "Mohammed", "Arjun",
    "Sai", "Reyansh", "Krishna", "Ishaan", "Dhruv", "Dev", "Atharva",
    "Aryan", "Tanmay", "Ayush", "Harsh", "Pranav", "Nikhil", "Gautam"
]

FIRST_NAMES_F = [
    "Diya", "Ananya", "Saanvi", "Priya", "Isha", "Aanya", "Zara",
    "Meera", "Fatima", "Sneha", "Kavya", "Riya", "Aditi", "Anushka",
    "Pooja", "Tanya", "Neha", "Shreya", "Deepika", "Bhavna", "Kriti"
]

LAST_NAMES = [
    "Sharma", "Verma", "Patel", "Singh", "Iyer", "Nair", "Khan",
    "Gupta", "Chatterjee", "Reddy", "Rao", "Joshi", "Mishra", "Deshmukh",
    "Choudhury", "Bose", "Mehta", "Bhat", "Kulkarni", "Das", "Yadav"
]

SUBJECTS = ["math", "science", "english", "social", "hindi"]

def clamp(val, low=0, high=100):
    return max(low, min(high, round(val, 1)))

def generate_synthetic_dataset(num_students=300, output_path=None):
    if output_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_path = os.path.join(base_dir, "data", "synthetic", "students_sample_250.csv")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    random.seed(42)

    students = []

    for i in range(1, num_students + 1):
        student_id = f"SH-2026-{i:03d}"
        
        # Determine Teacher & Grade (100 students each)
        if i <= 100:
            grade = 7
            teacher_id = "teacher1"
        elif i <= 200:
            grade = 8
            teacher_id = "teacher2"
        else:
            grade = 9
            teacher_id = "teacher3"

        # Explicit showcase students for demo:
        if i == 1:
            name = "Aarav Sharma"
            gender = "Male"
        elif i == 101:
            name = "Diya Patel"
            gender = "Female"
        elif i == 201:
            name = "Mohammed Faizan"
            gender = "Male"
        else:
            gender = random.choice(["Male", "Female"])
            first_name = random.choice(FIRST_NAMES_M if gender == "Male" else FIRST_NAMES_F)
            last_name = random.choice(LAST_NAMES)
            name = f"{first_name} {last_name}"

        section = "A" if (i % 3 == 1) else ("B" if (i % 3 == 2) else "C")

        # Decide student learning archetype
        archetype_prob = random.random()

        if archetype_prob < 0.55:
            # 1. On-Track / Stable Learner
            archetype = "On-Track"
            attendance = clamp(random.gauss(88, 5), 76, 99)
            assignment_rate = clamp(random.gauss(88, 6), 75, 100)
            homework_accuracy = clamp(random.gauss(82, 8), 70, 98)
            participation = random.choice([3, 4, 5])
            reading_wpm = clamp(random.gauss(135, 18), 105, 175)
            visual_pref = random.choice(["Standard", "Moderate", "High"])

            scores = {}
            for sub in SUBJECTS:
                base = random.gauss(72, 10)
                scores[f"{sub}_fa1"] = clamp(base + random.uniform(-4, 4))
                scores[f"{sub}_sa1"] = clamp(base + random.uniform(-4, 5))
                scores[f"{sub}_fa2"] = clamp(base + random.uniform(-3, 6))
                scores[f"{sub}_sa2"] = clamp(base + random.uniform(-2, 7))

            risk_level = "LOW"
            support_needed = 0

        elif archetype_prob < 0.70:
            # 2. Reading / Dyslexia Profile (Language & Phonics Gap, High Effort)
            archetype = "Reading/Language Barrier"
            attendance = clamp(random.gauss(86, 6), 75, 96)
            assignment_rate = clamp(random.gauss(68, 10), 45, 85)
            homework_accuracy = clamp(random.gauss(55, 9), 40, 70)
            participation = random.choice([3, 4, 5])
            reading_wpm = clamp(random.gauss(78, 12), 52, 98)
            visual_pref = "High"

            scores = {}
            for sub in SUBJECTS:
                if sub in ["english", "hindi"]:
                    base = random.gauss(42, 8)
                elif sub == "social":
                    base = random.gauss(48, 7)
                else:
                    base = random.gauss(62, 9)

                scores[f"{sub}_fa1"] = clamp(base + random.uniform(-4, 3))
                scores[f"{sub}_sa1"] = clamp(base + random.uniform(-5, 2))
                scores[f"{sub}_fa2"] = clamp(base + random.uniform(-4, 3))
                scores[f"{sub}_sa2"] = clamp(base + random.uniform(-3, 3))

            risk_level = "MODERATE"
            support_needed = 1

        elif archetype_prob < 0.85:
            # 3. Attendance / Disengagement Deficit
            archetype = "Attendance Deficit"
            attendance = clamp(random.gauss(62, 8), 45, 74)
            assignment_rate = clamp(random.gauss(48, 11), 30, 64)
            homework_accuracy = clamp(random.gauss(50, 10), 32, 65)
            participation = random.choice([1, 2, 3])
            reading_wpm = clamp(random.gauss(110, 20), 80, 140)
            visual_pref = random.choice(["Moderate", "High"])

            scores = {}
            for sub in SUBJECTS:
                base = random.gauss(52, 8)
                scores[f"{sub}_fa1"] = clamp(base + 6)
                scores[f"{sub}_sa1"] = clamp(base)
                scores[f"{sub}_fa2"] = clamp(base - 6)
                scores[f"{sub}_sa2"] = clamp(base - 12)

            risk_level = "HIGH"
            support_needed = 1

        else:
            # 4. Specific STEM / Foundation Concept Barrier
            archetype = "STEM Foundation Gap"
            attendance = clamp(random.gauss(82, 7), 75, 94)
            assignment_rate = clamp(random.gauss(65, 9), 50, 80)
            homework_accuracy = clamp(random.gauss(52, 8), 38, 66)
            participation = random.choice([2, 3])
            reading_wpm = clamp(random.gauss(125, 15), 100, 155)
            visual_pref = "High"

            scores = {}
            for sub in SUBJECTS:
                if sub in ["math", "science"]:
                    base = random.gauss(38, 7)
                else:
                    base = random.gauss(66, 8)

                scores[f"{sub}_fa1"] = clamp(base + random.uniform(-3, 3))
                scores[f"{sub}_sa1"] = clamp(base + random.uniform(-4, 2))
                scores[f"{sub}_fa2"] = clamp(base + random.uniform(-4, 2))
                scores[f"{sub}_sa2"] = clamp(base + random.uniform(-3, 3))

            risk_level = "MODERATE" if scores["math_sa2"] >= 35 else "HIGH"
            support_needed = 1

        # Composite aggregates
        term1_avg = sum(scores[f"{s}_sa1"] for s in SUBJECTS) / len(SUBJECTS)
        term2_avg = sum(scores[f"{s}_sa2"] for s in SUBJECTS) / len(SUBJECTS)
        overall_avg = round((term1_avg + term2_avg) / 2, 1)
        trend_slope = round(term2_avg - term1_avg, 1)

        row = {
            "student_id": student_id,
            "name": name,
            "grade": grade,
            "section": section,
            "teacher_id": teacher_id,
            "gender": gender,
            "archetype": archetype,
            "attendance_rate": attendance,
            "assignment_completion_rate": assignment_rate,
            "homework_accuracy": homework_accuracy,
            "class_participation": participation,
            "reading_speed_wpm": reading_wpm,
            "visual_preference": visual_pref,
            "term1_avg": round(term1_avg, 1),
            "term2_avg": round(term2_avg, 1),
            "overall_avg": overall_avg,
            "trend_slope": trend_slope,
            **scores,
            "risk_level": risk_level,
            "support_needed": support_needed
        }
        students.append(row)

    # Save to CSV
    fieldnames = list(students[0].keys())
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(students)

    print(f"Successfully generated {len(students)} student records at: {output_path}")
    return output_path

if __name__ == "__main__":
    generate_synthetic_dataset(num_students=300)
