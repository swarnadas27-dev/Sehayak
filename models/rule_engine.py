"""
SEHAYAK (सहायक) - Transparent Rule-Based Risk Engine
Provides explainable, transparent, deterministic pedagogical evaluations
used as both an educational baseline and a robust fallback.
"""

from config import (
    FAILING_MARK_THRESHOLD,
    CRITICAL_ATTENDANCE_THRESHOLD,
    LOW_ASSIGNMENT_THRESHOLD
)

def evaluate_student_rules(student):
    """
    Evaluates a student record against pedagogical heuristic rules.
    Returns:
        dict with keys:
            - risk_level: 'HIGH', 'MODERATE', or 'LOW'
            - risk_score: float (0.0 to 1.0)
            - support_needed: int (0 or 1)
            - reasons_en: list of str
            - reasons_hi: list of str
            - strengths_en: list of str
            - strengths_hi: list of str
            - weak_subjects: list of str
            - strong_subjects: list of str
    """
    reasons_en = []
    reasons_hi = []
    strengths_en = []
    strengths_hi = []
    weak_subjects = []
    strong_subjects = []

    penalty_points = 0.0

    # 1. Subject-Wise Mark Evaluation
    subjects_map = {
        "math": ("Mathematics", "गणित"),
        "science": ("Science", "विज्ञान"),
        "english": ("English", "अंग्रेज़ी"),
        "social": ("Social Science", "सामाजिक विज्ञान"),
        "hindi": ("Hindi", "हिन्दी")
    }

    for sub_key, (name_en, name_hi) in subjects_map.items():
        sa2 = student.get(f"{sub_key}_sa2", 60.0)
        sa1 = student.get(f"{sub_key}_sa1", 60.0)
        avg = student.get(f"{sub_key}_avg", (sa1 + sa2) / 2.0)

        # Subject difficulty check
        if sa2 < FAILING_MARK_THRESHOLD or avg < FAILING_MARK_THRESHOLD:
            penalty_points += 0.25
            weak_subjects.append(name_en)
            reasons_en.append(f"Low achievement in {name_en} ({sa2:.1f}% in Term 2 assessment, below 35% benchmark).")
            reasons_hi.append(f"{name_hi} में कम अंक (सत्र 2 में {sa2:.1f}%, जो 35% के मानक से कम है)।")
        elif sa2 < 45.0:
            penalty_points += 0.12
            weak_subjects.append(name_en)
            reasons_en.append(f"Vulnerable grasp in {name_en} ({sa2:.1f}%), requires targeted foundational review.")
            reasons_hi.append(f"{name_hi} में कमजोर पकड़ ({sa2:.1f}%), मूलभूत पुनरावृत्ति की आवश्यकता है।")
        elif sa2 >= 70.0:
            strong_subjects.append(name_en)

        # Sharp decline check
        if (sa1 - sa2) >= 15.0:
            penalty_points += 0.15
            reasons_en.append(f"Steep decline in {name_en}: marks dropped by {(sa1 - sa2):.1f}% from Term 1 to Term 2.")
            reasons_hi.append(f"{name_hi} में गिरावट: सत्र 1 से सत्र 2 के बीच अंक {(sa1 - sa2):.1f}% घटे।")

    # 2. Overall Assessment Trend
    trend_slope = student.get("trend_slope", 0.0)
    if trend_slope <= -12.0:
        penalty_points += 0.20
        reasons_en.append(f"Overall downward academic trajectory across terms (overall drop of {abs(trend_slope):.1f}%).")
        reasons_hi.append(f"सभी विषयों में कुल मिलाकर गिरावट (कुल {abs(trend_slope):.1f}% की कमी)।")

    # 3. Attendance Evaluation
    attendance = student.get("attendance_rate", 85.0)
    if attendance < 65.0:
        penalty_points += 0.35
        reasons_en.append(f"Critical attendance deficit: {attendance:.1f}% (significantly below 75% statutory requirement).")
        reasons_hi.append(f"गंभीर उपस्थिति कमी: {attendance:.1f}% (अनिवार्य 75% की सीमा से बहुत कम)।")
    elif attendance < CRITICAL_ATTENDANCE_THRESHOLD:
        penalty_points += 0.20
        reasons_en.append(f"Attendance warning: {attendance:.1f}% (below 75% recommended minimum).")
        reasons_hi.append(f"उपस्थिति चेतावनी: {attendance:.1f}% (75% की सामान्य न्यूनतम सीमा से कम)।")
    elif attendance >= 90.0:
        strengths_en.append(f"Excellent attendance record ({attendance:.1f}%), showing high dedication.")
        strengths_hi.append(f"उत्कृष्ट उपस्थिति रिकॉर्ड ({attendance:.1f}%), सीखने के प्रति समर्पण।")

    # 4. Homework & Assignment Compliance
    assignment_rate = student.get("assignment_completion_rate", 80.0)
    if assignment_rate < 50.0:
        penalty_points += 0.25
        reasons_en.append(f"Low assignment submission rate ({assignment_rate:.1f}%), indicating study habit or home learning barriers.")
        reasons_hi.append(f"असाइनमेंट जमा करने की निम्न दर ({assignment_rate:.1f}%), अभ्यास में बाधा का संकेत।")
    elif assignment_rate < LOW_ASSIGNMENT_THRESHOLD:
        penalty_points += 0.15
        reasons_en.append(f"Incomplete assignment pattern ({assignment_rate:.1f}%), needs structured homework pacing.")
        reasons_hi.append(f"अधूरे असाइनमेंट का रुझान ({assignment_rate:.1f}%), गृहकार्य में सहयोग आवश्यक।")
    elif assignment_rate >= 88.0:
        strengths_en.append(f"High assignment diligence ({assignment_rate:.1f}% completion rate).")
        strengths_hi.append(f"गृहकार्य में निरंतरता ({assignment_rate:.1f}% कार्य पूर्ण)।")

    # 5. Reading Speed & Phonics / Dyslexia indicator proxy
    reading_wpm = student.get("reading_speed_wpm", 120.0)
    if reading_wpm < 85.0:
        reasons_en.append(f"Reading fluency pacing: {reading_wpm:.0f} words/min (text decodability and reading fatigue support needed).")
        reasons_hi.append(f"पठन गति: {reading_wpm:.0f} शब्द/मिनट (पढ़ने में अतिरिक्त समय और दृश्य सामग्री की आवश्यकता)।")
        # Note: We do NOT penalize heavily; this informs dyslexia-friendly multisensory accommodation
        penalty_points += 0.10

    # 6. Participation Strengths
    participation = student.get("class_participation", 3.0)
    if participation >= 4.0:
        strengths_en.append("High oral class participation and active conceptual curiosity.")
        strengths_hi.append("कक्षा में सक्रिय मौखिक भागीदारी और सीखने की उत्सुकता।")
    elif participation <= 2.0:
        reasons_en.append("Hesitant class engagement; child may feel diffident asking questions in front of peers.")
        reasons_hi.append("कक्षा में झिझक; सहपाठियों के सामने प्रश्न पूछने में संकोच।")

    # If student has strong subjects, note them
    if strong_subjects:
        strengths_en.append(f"Strong performance demonstrated in: {', '.join(strong_subjects)}.")
        strengths_hi.append(f"इन विषयों में अच्छी समझ प्रदर्शित की: {', '.join(strong_subjects)}।")

    if not strengths_en:
        strengths_en.append("Shows persistence and positive responsiveness to one-on-one encouragement.")
        strengths_hi.append("व्यक्तिगत मार्गदर्शन और प्रोत्साहन के प्रति सकारात्मक रुख।")

    # Compute Final Score & Tier
    risk_score = round(min(1.0, max(0.0, penalty_points)), 2)

    if risk_score >= 0.55 or len(weak_subjects) >= 2 or attendance < 65.0:
        risk_level = "HIGH"
        support_needed = 1
    elif risk_score >= 0.25 or len(weak_subjects) == 1 or attendance < 75.0 or assignment_rate < 60.0:
        risk_level = "MODERATE"
        support_needed = 1
    else:
        risk_level = "LOW"
        support_needed = 0

    if not reasons_en:
        reasons_en.append("Academic progress is steady with no critical barriers identified.")
        reasons_hi.append("शैक्षणिक प्रगति निरंतर और संतोषजनक है, कोई गंभीर बाधा नहीं पाई गई।")

    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "support_needed": support_needed,
        "reasons_en": reasons_en,
        "reasons_hi": reasons_hi,
        "strengths_en": strengths_en,
        "strengths_hi": strengths_hi,
        "weak_subjects": weak_subjects,
        "strong_subjects": strong_subjects
    }
