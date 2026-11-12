"""
SEHAYAK Local Context-Aware AI Assistant (`remedial/chatbot.py`)
Supports both:
 - Student Portal ("SEHAYAK Study Buddy AI")
 - Parent Portal ("SEHAYAK Family Guidance AI")

Combines live SQLite student records, evaluated 15-question answer sheets,
CRA learning logic (`remedial/ai_tutor.py`), Learning Disability screening profiles,
and live Counselor-updated study exercises into warm, simple, zero-jargon answers.
"""

import re
from remedial.ai_tutor import analyze_student_paper_performance, get_question_logic_detail
from remedial.resources import INDEPENDENT_RESEARCH_REFERENCES
from utils.db import (
    get_student_by_id,
    get_counselor_exercises,
    get_counselor_messages,
    get_messages_for_parent,
)


def get_starter_chips(role="student", student_id="SH-2026-001"):
    """Return role-appropriate quick-question chips for the chatbot UI."""
    if role == "parent":
        return [
            "Which trusted websites and research references can I read?",
            "How is my child doing overall and where are marks dropping?",
            "What does my child's learning support profile mean?",
            "Which 10-minute exercises can we practice together at home?",
            "How do I contact the School Counselor or book a session?",
        ]
    return [
        "Show me an interactive online exercise I can try right now",
        "Which maths questions am I weak in and what trick should I use?",
        "Explain Question 9 logic in simple steps",
        "Give me an easy 10-minute study technique from Counselor Ma'am",
        "How do I get extra help from the School Counselor?",
    ]


def _extract_question_number(text_lower):
    match = re.search(r"\bq\s*[-]?\s*(\d{1,2})\b|\bquestion\s*(?:no\.?|number)?\s*(\d{1,2})\b", text_lower)
    if match:
        num = int(match.group(1) or match.group(2))
        if 1 <= num <= 15:
            return num
    return None


def _format_exercise_block(ex, is_parent=False):
    steps = ex.get("steps") or []
    step_lines = "\n".join([f"   {idx}. {st}" for idx, st in enumerate(steps[:4], 1)])
    lines = [
        f"Exercise: {ex['title']} ({ex['duration_mins']} mins | Technique: {ex['study_technique']})",
        f"Goal: {ex['simple_goal']}",
        f"Simple Steps:\n{step_lines}",
    ]
    if is_parent and ex.get("home_tip"):
        lines.append(f"Parent Home Tip: {ex['home_tip']}")
    return "\n".join(lines)


def generate_ai_chatbot_response(user_message, role="student", student_id="SH-2026-001"):
    """
    Produce a structured, plain-language AI reply grounded in the student's live record.
    Returns dict with keys: answer, highlights (list[str]), suggested_questions (list[str]).
    """
    msg = (user_message or "").strip()
    msg_lower = msg.lower()
    is_parent = role == "parent"

    student = get_student_by_id(student_id) or {
        "student_id": student_id,
        "name": "Student",
        "grade": "7",
        "section": "A",
        "overall_avg": 62.0,
        "attendance_rate": 85.0,
        "ld_screening_status": "Possibility / Early Screening",
        "ld_category": "Dyslexia / Visual Reading",
        "ld_notes": "Benefits from chunked reading and step-by-step visual maths.",
    }
    first_name = student["name"].split()[0]
    ld_cat = student.get("ld_category") or "General"
    ld_status = student.get("ld_screening_status") or "None"
    ld_notes = student.get("ld_notes") or ""

    paper_perf = analyze_student_paper_performance(student_id, target_subject="Mathematics")
    weak_qs = paper_perf.get("weak_questions", [])
    exercises = get_counselor_exercises(category=ld_cat if ld_cat != "General" else None, student_id=student_id)
    if not exercises:
        exercises = get_counselor_exercises(student_id=student_id)
    counselor_msgs = get_counselor_messages(student_id=student_id)

    # 0. Research References, Independent Websites & Interactive Online Exercises
    if any(k in msg_lower for k in ["reference", "research", "website", "site", "source", "proof", "understood", "reading rockets", "phet", "khan", "math learning center", "interactive", "online"]):
        ref_lines = "\n".join([
            f"- {r['name']} ({r['url']})\n  Why referenced: {r['used_for']}"
            for r in INDEPENDENT_RESEARCH_REFERENCES[:5]
        ])
        online_ex_lines = "\n".join([
            f"- {ex['title']} ({ex.get('exercise_mode', 'Online Mini-Lab')})"
            + (f" — External App: {ex['external_site_name']} ({ex['external_practice_url']})" if ex.get("external_practice_url") else "")
            for ex in exercises[:3]
        ])
        if is_parent:
            answer = (
                f"Parents are warmly encouraged to read the exact independent organizations SEHAYAK and Dr. Meera Deshmukh used as references:\n\n"
                f"Trusted Independent Research & Practice Websites:\n{ref_lines}\n\n"
                f"Online Exercises Currently Assigned for {first_name}:\n{online_ex_lines}\n\n"
                f"You can open any interactive exercise or read these reference articles right from the 'Home Exercises & LD Support' tab on your Parent Portal."
            )
        else:
            answer = (
                f"You can try Counselor Ma'am's online exercises right inside the Practice Sessions tab OR open free interactive visual apps!\n\n"
                f"Interactive Exercises Ready for You:\n{online_ex_lines}\n\n"
                f"Tap 'Launch Online Exercise Here' inside the Study Techniques card to practice with color highlighters, algebra balance boxes, or the calm focus timer right on your screen!"
            )
        return {
            "answer": answer,
            "highlights": [
                "Understood.org",
                "Reading Rockets & IDA",
                "PhET & Math Learning Center",
            ],
            "suggested_questions": get_starter_chips(role, student_id)[:4],
        }

    # 1. Specific question explanation (Q1..Q15)
    q_num = _extract_question_number(msg_lower)
    if q_num is not None:
        detail = get_question_logic_detail(q_num, subject="Mathematics")
        steps_text = "\n".join([f"{i}. {s}" for i, s in enumerate(detail.get("steps", []), 1)])
        if is_parent:
            answer = (
                f"Here is a simple breakdown of Question {q_num} ({detail['concept']}) so you can guide {first_name} calmly at home.\n\n"
                f"Logic Method Used: {detail['logic_name']}\n"
                f"Visual Idea: {detail['visual_metaphor']}\n\n"
                f"Step-by-Step Walkthrough:\n{steps_text}\n\n"
                f"5-Minute Starter Check at Home:\n{detail.get('drill', '')}"
            )
        else:
            answer = (
                f"Let us unlock Question {q_num} ({detail['concept']}) step by step—no stress!\n\n"
                f"Best Brain Trick: {detail['logic_name']}\n"
                f"Picture It Like This: {detail['visual_metaphor']}\n\n"
                f"Follow These Easy Steps:\n{steps_text}\n\n"
                f"Quick Warm-Up Drill:\n{detail.get('drill', '')}"
            )
        return {
            "answer": answer,
            "highlights": [
                f"Logic: {detail['logic_name']}",
                f"Topic: {detail['concept']}",
                f"Pattern: {detail.get('marks_label', '')}",
            ],
            "suggested_questions": get_starter_chips(role, student_id)[:4],
        }

    # 2. School Counselor / appointment / contact / messaging
    if any(k in msg_lower for k in ["counselor", "counsellor", "meera", "appointment", "meet", "refer", "talk to", "contact"]):
        latest_c = counselor_msgs[0] if counselor_msgs else None
        latest_note = ""
        if latest_c and latest_c.get("reply"):
            latest_note = f"\n\nLatest Counselor Update on File ({latest_c['subject']}):\n\"{latest_c['reply']}\""
        elif latest_c:
            latest_note = f"\n\nOpen Request on File: \"{latest_c['subject']}\" (Status: {latest_c['status']}). Dr. Meera Deshmukh reviews requests daily."

        if is_parent:
            answer = (
                f"You can reach School Counselor Dr. Meera Deshmukh directly right from this Parent Portal—no outside paperwork needed.\n\n"
                f"How Parents Connect in 3 Easy Steps:\n"
                f"1. Scroll to the 'Connect with School Counselor' box on this page.\n"
                f"2. Pick 'Appointment Request' or 'Home Study Guidance' and write your question in plain words.\n"
                f"3. Click 'Send to School Counselor'. Her reply and new home exercises appear right here on your screen.{latest_note}"
            )
        else:
            answer = (
                f"Talking to our School Counselor Dr. Meera Deshmukh is completely safe, private, and friendly.\n\n"
                f"How to Message Counselor Ma'am:\n"
                f"1. Go to the 'Talk to Your School Counselor' card on this page.\n"
                f"2. Write what feels tricky (for example: 'Numbers blur in long maths questions' or 'I feel nervous before tests').\n"
                f"3. Click 'Send Check-In'. You will see her reply right below it.{latest_note}"
            )
        return {
            "answer": answer,
            "highlights": [
                "School Counselor: Dr. Meera Deshmukh",
                "Reply Channel: Direct inside Portal Inbox",
                "Privacy: Confidential support",
            ],
            "suggested_questions": [
                "Which 10-minute exercises can we practice right now?",
                "What does the learning support profile mean?",
                "Which maths questions need attention?",
            ],
        }

    # 3. Learning Disability / Dyslexia / Dyscalculia / Dysgraphia / CBSE Accommodations / Profile
    if any(k in msg_lower for k in [
        "dyslex", "dyscalcul", "dysgraph", "disability", "learning", "screening",
        "possibility", "accommodation", "cbse", "extra time", "scribe", "profile", "attention", "adhd", "focus"
    ]):
        status_explain = (
            f"{first_name} is currently listed under '{ld_status}' ({ld_cat}). "
            f"Note from school: {ld_notes or 'Focused visual and chunked-step guidance is active.'}"
            if ld_status != "None"
            else f"{first_name} does not currently have a flagged screening profile, though our visual study techniques help every student learn calmer and faster."
        )
        top_ex = _format_exercise_block(exercises[0], is_parent=is_parent) if exercises else ""

        if is_parent:
            answer = (
                f"Understanding {first_name}'s Support Profile (In Simple Words):\n"
                f"{status_explain}\n\n"
                f"What 'Possibility' or 'Support Profile' Means:\n"
                f"It is NOT a medical label or failure. It simply means your child thinks better with clear visual chunks, audio support, and unhurried steps rather than crowded walls of text.\n\n"
                f"CBSE Supportive Provisions Available via School Counselor:\n"
                f"- Extra compensatory time (up to 20 minutes per hour) when certified.\n"
                f"- Clean, wide-spaced question formatting and oral read-aloud check-ins.\n\n"
                f"Recommended Starting Routine:\n{top_ex}"
            )
        else:
            answer = (
                f"Your brain simply learns best through pictures, color-chunks, and step-by-step blocks instead of walls of tiny text!\n\n"
                f"Your Current Support Focus: {ld_cat}\n\n"
                f"Best 3 Habits for You:\n"
                f"1. Use the Accessibility Drawer (top bar) to turn on Dyslexia Font & Read Aloud.\n"
                f"2. Slide a finger or pencil under ONE sentence at a time in long questions.\n"
                f"3. Try Counselor Ma'am's top exercise today:\n\n{top_ex}"
            )
        return {
            "answer": answer,
            "highlights": [
                f"Support Group: {ld_status}",
                f"Focus Style: {ld_cat}",
                "Approach: Visual + Audio + Unhurried Steps",
            ],
            "suggested_questions": [
                "How do I contact the School Counselor?",
                "Which maths questions need attention?",
                "Give me another study technique for home practice",
            ],
        }

    # 4. Study techniques & Counselor-updated exercises
    if any(k in msg_lower for k in ["exercise", "technique", "study", "practice", "routine", "habit", "tip", "home", "read", "word problem"]):
        top_two = exercises[:2]
        blocks = "\n\n---\n\n".join([_format_exercise_block(ex, is_parent=is_parent) for ex in top_two])
        if is_parent:
            answer = (
                f"Here are the latest simple 10-minute study techniques updated by School Counselor Dr. Meera Deshmukh for {first_name}:\n\n"
                f"{blocks}\n\n"
                f"Golden Rule at Home: Keep sessions under 12 minutes, praise effort and neat steps first, and mark 'Practiced' on the Counselor Exercises card so the school sees progress."
            )
        else:
            answer = (
                f"Here are 2 easy study exercises picked for you by Counselor Ma'am:\n\n"
                f"{blocks}\n\n"
                f"Tip: Pick just ONE exercise below, try it for 10 minutes, and click 'Mark Practiced Today' to build your streak!"
            )
        return {
            "answer": answer,
            "highlights": [ex["study_technique"] for ex in top_two],
            "suggested_questions": [
                "Which maths questions am I weak in?" if not is_parent else "Where are my child's exam marks dropping?",
                "How do I contact the School Counselor?",
                "Explain Question 9 logic in simple steps",
            ],
        }

    # 5. Performance / Weak questions / Marks / Exam paper / Improvement
    if any(k in msg_lower for k in ["weak", "mark", "score", "improve", "paper", "exam", "test", "math", "doing", "progress", "teacher", "remark"]):
        if weak_qs:
            q_list = ", ".join([f"Q{q['q_num']} ({q['concept']} — {q['obtained']}/{q['max']})" for q in weak_qs[:3]])
            first_weak = weak_qs[0]
            first_steps = "\n".join([f"   {i}. {s}" for i, s in enumerate(first_weak.get("steps", [])[:3], 1)])
            weak_summary = (
                f"Focus Questions from Latest Evaluated Paper ({paper_perf.get('total_obtained')}/{paper_perf.get('total_max')} Marks):\n"
                f"{q_list}\n\n"
                f"Quickest Win First — Question {first_weak['q_num']} ({first_weak['logic_name']}):\n"
                f"{first_steps}"
            )
        else:
            weak_summary = (
                f"No weak questions detected in the latest evaluated sheet ({paper_perf.get('total_obtained')}/{paper_perf.get('total_max')} Marks)! "
                f"Focus on steady revision using the 10-2 Calm Focus Sprint."
            )

        teacher_rem = student.get("teacher_improvements") or student.get("teacher_remarks") or ""
        rem_line = f"\n\nTeacher Note: {teacher_rem}" if teacher_rem else ""

        if is_parent:
            answer = (
                f"Here is {first_name}'s friendly progress snapshot (Class {student.get('grade', '7')}-{student.get('section', 'A')}):\n"
                f"- Overall Average: {student.get('overall_avg', 0):.1f}% | Attendance: {student.get('attendance_rate', 0):.1f}%\n"
                f"- Support Profile: {ld_status} ({ld_cat})\n\n"
                f"{weak_summary}{rem_line}\n\n"
                f"Next Best Step: Practice just the first weak question using visual steps for 10 minutes today—no cramming!"
            )
        else:
            answer = (
                f"Good news {first_name}—your marks show strong effort, and fixing just 2 small question patterns will boost your total fast!\n\n"
                f"{weak_summary}{rem_line}\n\n"
                f"Ask me 'Explain Question {weak_qs[0]['q_num'] if weak_qs else 9}' anytime if you want an even slower walkthrough."
            )
        return {
            "answer": answer,
            "highlights": [
                f"Paper Total: {paper_perf.get('total_obtained')}/{paper_perf.get('total_max')}",
                f"Focus Questions: {len(weak_qs)} spotted",
                f"Best Logic: {weak_qs[0]['logic_name'] if weak_qs else 'Steady Revision'}",
            ],
            "suggested_questions": [
                f"Explain Question {weak_qs[0]['q_num'] if weak_qs else 9} in simple steps",
                "Which 10-minute exercises should we practice?",
                "How do I contact the School Counselor?",
            ],
        }

    # 6. Warm Contextual Fallback for any other general question
    top_ex = exercises[0] if exercises else None
    ex_hint = f"Try '{top_ex['title']}' ({top_ex['duration_mins']} mins)" if top_ex else "Explore the Study Techniques section below"
    weak_hint = f"Question {weak_qs[0]['q_num']} ({weak_qs[0]['concept']})" if weak_qs else "visual maths revision"

    if is_parent:
        answer = (
            f"Hello! I am SEHAYAK Family Guidance AI supporting {first_name} (Class {student.get('grade', '7')}-{student.get('section', 'A')}).\n\n"
            f"I understood your question about: \"{msg}\".\n\n"
            f"Right now, here are the 3 most helpful things on {first_name}'s file:\n"
            f"1. Support Profile: {ld_status} ({ld_cat}).\n"
            f"2. Top Exam Focus: {weak_hint}.\n"
            f"3. Recommended Home Exercise: {ex_hint}.\n\n"
            f"You can ask me about any Maths Question (Q1 to Q15), daily 10-minute home routines, CBSE accommodations, or how to message School Counselor Dr. Meera Deshmukh."
        )
    else:
        answer = (
            f"Hi {first_name}! I am your SEHAYAK Study Buddy AI.\n\n"
            f"Here is a quick plan based on your portal right now:\n"
            f"1. Exam Quick-Win: Let us practice {weak_hint} using visual steps.\n"
            f"2. Counselor Pick Today: {ex_hint}.\n"
            f"3. Stuck on something personal or test nerves? You can message Counselor Ma'am below anytime.\n\n"
            f"Try tapping one of the question chips below—like asking me to explain any question number (e.g. 'Explain Q9')!"
        )

    return {
        "answer": answer,
        "highlights": [
            f"Student: {student['name']}",
            f"Focus: {weak_hint}",
            f"Profile: {ld_status}",
        ],
        "suggested_questions": get_starter_chips(role, student_id)[:4],
    }
