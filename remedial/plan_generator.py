"""
SEHAYAK (सहायक) - Dynamic Remedial Plan Generator
Matches student diagnostic indicators to evidence-based interventions
and generates a structured 4-week individualized remedial action plan
with deterministic task IDs for closed-loop milestone tracking (RTI).
"""

from remedial.strategy_catalog import STRATEGY_CATALOG

def generate_remedial_plan(student, student_eval, lang="en"):
    """
    Builds a complete 4-week remedial learning roadmap.
    Each activity has a unique task_id for interactive tracking.
    """
    weak_subjects = student_eval.get("weak_subjects", [])
    attendance = float(student.get("attendance_rate", 85.0))
    reading_wpm = float(student.get("reading_speed_wpm", 120.0))
    risk_level = student_eval.get("risk_level", "LOW")

    # Strategy Selection Matrix
    selected_strategies = []

    # 1. Math weakness check
    if any("math" in s.lower() for s in weak_subjects):
        selected_strategies.append(STRATEGY_CATALOG["multisensory_math"])

    # 2. Reading / Dyslexia / Language barrier check
    if reading_wpm < 95.0 or any("english" in s.lower() or "hindi" in s.lower() for s in weak_subjects):
        selected_strategies.append(STRATEGY_CATALOG["phonics_reading_dyslexia"])

    # 3. Science or Social Studies text-overload
    if any("science" in s.lower() or "social" in s.lower() for s in weak_subjects):
        selected_strategies.append(STRATEGY_CATALOG["visual_graphic_organizers"])

    # 4. Attendance gap
    if attendance < 75.0:
        selected_strategies.append(STRATEGY_CATALOG["attendance_recovery"])

    # 5. Peer tutoring is universally effective for building confidence and social engagement
    selected_strategies.append(STRATEGY_CATALOG["peer_tutoring"])

    # 6. Spaced revision for memory reinforcement
    selected_strategies.append(STRATEGY_CATALOG["spaced_revision"])

    # Remove duplicates while preserving order
    seen_ids = set()
    unique_strategies = []
    for s in selected_strategies:
        if s["id"] not in seen_ids:
            seen_ids.add(s["id"])
            unique_strategies.append(s)

    # 4-Week Structured Roadmap with explicit task items
    if lang == "hi":
        raw_weeks = [
            {
                "week": 1,
                "title": "सप्ताह 1: मूलभूत समझ एवं विश्वास निर्माण (Foundational Grounding)",
                "goal": "छात्र के मन से परीक्षा का डर दूर करना और बुनियादी अवधारणाओं को ठोस वस्तुओं/चित्रों से स्पष्ट करना।",
                "activities": [
                    "कठिन अध्यायों के लिए सरल सचित्र शब्दावली चार्ट तैयार करें।",
                    "सहयोगी सहपाठी (Study Buddy) के साथ 15 मिनट की दैनिक चर्चा शुरू करें।",
                    "बिना किसी अंक या दबाव के केवल उत्साहवर्धक मौखिक प्रतिक्रिया दें।"
                ]
            },
            {
                "week": 2,
                "title": "सप्ताह 2: बहु-संवेदी अभ्यास एवं दृश्य मानचित्र (Multisensory Scaffolding)",
                "goal": "दृश्य आरेखों, फ्लोचार्ट और ऑडियो नोट्स के माध्यम से जटिल सिद्धांतों को सिखाना।",
                "activities": [
                    "गणित और विज्ञान में रंग-आधारित नंबर लाइन और मॉडल का प्रयोग करें।",
                    "लंबी परिभाषाओं के स्थान पर 1-पेज का माइंड मैप भरवाएं।",
                    "सहायक पोर्टल पर 5 मिनट के सरल डिजिटल अभ्यास का उपयोग करें।"
                ]
            },
            {
                "week": 3,
                "title": "सप्ताह 3: अंतरालीय पुनरावृत्ति एवं छोटे अभ्यास (Spaced Micro-Drills)",
                "goal": "स्मृति को सुदृढ़ करने के लिए 1, 3 और 7वें दिन छोटे फ्लैशकार्ड द्वारा पुनरावृत्ति।",
                "activities": [
                    "प्रत्येक कक्षा के आरंभ में 3 प्रश्नों का दोस्ताना वार्म-अप प्रश्नोत्तरी।",
                    "छात्र को अपनी पसंद की गति से पाठ दोहराने की छूट दें।",
                    "अभिभावकों के साथ प्रगति की सकारात्मक समीक्षा करें।"
                ]
            },
            {
                "week": 4,
                "title": "सप्ताह 4: दक्षता समीक्षा एवं उपलब्धि प्रमाणन (Mastery & Celebration)",
                "goal": "सीखी गई अवधारणाओं का बिना तनाव के मूल्यांकन और छात्र के आत्मविश्वास को सम्मानित करना।",
                "activities": [
                    "लघु संवादात्मक खेल के माध्यम से सीखी गई बातों की समीक्षा।",
                    "'स्टार एफर्ट' प्रशंसा बैज प्रदान करें।",
                    "अगले महीने के लिए सीखने के नए लक्ष्यों का निर्धारण करें।"
                ]
            }
        ]
        parent_tips = [
            "घर पर पढ़ने के लिए शांत, तनावमुक्त वातावरण प्रदान करें।",
            "बच्चे के साथ मिलकर कहानियों और विषयों को बोलकर सुनें (ऑडियो टूल का उपयोग करें)।",
            "अंकों के बजाय बच्चे द्वारा किए गए दैनिक प्रयास की प्रशंसा करें।"
        ]
    else:
        raw_weeks = [
            {
                "week": 1,
                "title": "Week 1: Foundational Grounding & Confidence Building",
                "goal": "De-escalate academic anxiety and map core prerequisite knowledge using visual manipulatives.",
                "activities": [
                    "Introduce color-coded concept sheets and pictorial anchor charts for challenging units.",
                    "Assign a supportive, empathetic peer mentor for 15-minute bi-weekly check-ins.",
                    "Focus strictly on formative praise without graded time pressure."
                ]
            },
            {
                "week": 2,
                "title": "Week 2: Multisensory Scaffolding & Graphic Organizers",
                "goal": "Transform dense textual descriptions into branch diagrams and audio-assisted explanations.",
                "activities": [
                    "Implement Concrete-Representational-Abstract (CRA) tactile aids in math and science.",
                    "Utilize SEHAYAK's read-aloud TTS feature for all reading passages to eliminate fatigue.",
                    "Complete 5-minute interactive micro-practice sets on the student portal."
                ]
            },
            {
                "week": 3,
                "title": "Week 3: Spaced Retrieval & Chunked Micro-Drills",
                "goal": "Cement conceptual memory through short, non-fatiguing retrieval cues at Day 1, 3, and 7.",
                "activities": [
                    "Begin class with a low-stakes 3-question visual warm-up.",
                    "Allow student to articulate answers verbally or via graphic diagrams.",
                    "Collaborative check-in between teacher and learning support coordinator."
                ]
            },
            {
                "week": 4,
                "title": "Week 4: Low-Anxiety Mastery Review & Positive Reinforcement",
                "goal": "Validate conceptual gains, celebrate student diligence, and establish sustainable momentum.",
                "activities": [
                    "Conduct a conversational, low-anxiety mastery demonstration.",
                    "Award the 'Growth Explorer' achievement badge on the student portal.",
                    "Formulate a maintenance pacing plan for the upcoming academic cycle."
                ]
            }
        ]
        parent_tips = [
            "Establish a consistent, calm 20-minute daily home study routine without distractions.",
            "Listen to audiobooks or utilize SEHAYAK's Read-Aloud button together during reading exercises.",
            "Celebrate effort, curiosity, and consistency rather than high test scores alone."
        ]

    # Attach structured task objects with deterministic IDs
    four_week_plan = []
    total_tasks_count = 0
    for w_idx, w in enumerate(raw_weeks, start=1):
        task_objs = []
        for a_idx, act_text in enumerate(w["activities"], start=1):
            total_tasks_count += 1
            task_objs.append({
                "id": f"w{w_idx}_a{a_idx}",
                "text": act_text
            })
        four_week_plan.append({
            "week": w["week"],
            "title": w["title"],
            "goal": w["goal"],
            "tasks": task_objs
        })

    return {
        "student_name": student.get("name"),
        "student_id": student.get("student_id"),
        "grade": student.get("grade"),
        "section": student.get("section"),
        "risk_level": risk_level,
        "strategies": unique_strategies[:4],
        "four_week_plan": four_week_plan,
        "total_tasks": total_tasks_count,
        "parent_tips": parent_tips
    }
