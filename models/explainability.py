"""
SEHAYAK (सहायक) - Explainability Engine
Translates model scores, feature weights, and pedagogical rules
into plain-language diagnostic explanations for educators and parents.
"""

def generate_student_explanation_card(student_eval, student_data, lang="en"):
    """
    Generates a structured, compassionate, and actionable diagnostic card.
    Avoids labeling words like 'deficient', 'slow', 'failing' in student-facing context.
    """
    risk_level = student_eval.get("risk_level", "LOW")
    reasons = student_eval.get("reasons_hi" if lang == "hi" else "reasons_en", [])
    strengths = student_eval.get("strengths_hi" if lang == "hi" else "strengths_en", [])
    weak_subjects = student_eval.get("weak_subjects", [])
    contributions = student_eval.get("contributions", [])

    # Metrics snapshot
    metrics = {
        "attendance": f"{float(student_data.get('attendance_rate', 0)):.1f}%",
        "assignment_rate": f"{float(student_data.get('assignment_completion_rate', 0)):.1f}%",
        "trend_slope": f"{float(student_data.get('trend_slope', 0)):+.1f}%",
        "reading_speed": f"{int(float(student_data.get('reading_speed_wpm', 120)))} WPM",
        "participation": f"{float(student_data.get('class_participation', 3)):.1f}/5.0"
    }

    if lang == "hi":
        summary_header = {
            "HIGH": "प्राथमिक उपचारात्मक सहयोग अनुशंसित (Priority Remedial Support)",
            "MODERATE": "मार्गदर्शित शैक्षणिक सहयोग अनुशंसित (Guided Academic Support)",
            "LOW": "संतोषजनक शैक्षणिक प्रगति (On-Track Learning)"
        }.get(risk_level, "शैक्षणिक समीक्षा")
        
        takeaway = (
            "यह छात्र लक्षित बहु-संवेदी शिक्षण विधियों, सहपाठी सहयोग और दृश्य सामग्री के माध्यम से तेज़ी से प्रगति कर सकता है।"
            if risk_level != "LOW" else
            "छात्र निरंतर रूप से अच्छा प्रदर्शन कर रहा है। समग्र विकास के लिए संवर्धन अभ्यास जारी रखें।"
        )
    else:
        summary_header = {
            "HIGH": "Priority Remedial Support Recommended",
            "MODERATE": "Guided Academic Support Recommended",
            "LOW": "On-Track Learning Progress"
        }.get(risk_level, "Academic Review")

        takeaway = (
            "This learner demonstrates clear potential and will benefit significantly from multisensory scaffolding, peer mentoring, and chunked learning exercises."
            if risk_level != "LOW" else
            "The student is demonstrating steady engagement and consistent learning mastery."
        )

    return {
        "summary_header": summary_header,
        "takeaway": takeaway,
        "key_reasons": reasons,
        "strengths": strengths,
        "weak_subjects": weak_subjects,
        "metrics": metrics,
        "score_value": student_eval.get("risk_score", 0.0),
        "contributions": contributions
    }
