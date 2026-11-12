"""
SEHAYAK (सहायक) - Slow Learner Identification & Remedial Support System
Problem Statement ID: PSB152 | Ministry of Education

Main Flask Application Entry Point with 5 Roles:
 1. Principal: School-wide leadership across all 300 students (private chats excluded)
 2. 3 Teachers: 100 students each, RTI tracking, parent chat/queries, counselor referrals
 3. School Counselor: Learning disability & early screening roster, multi-role inbox, study exercises
 4. Students: CBSE 30-Marks Assessments, AI logic clinic, counselor exercises & AI Study Buddy chatbot
 5. Parents: Child growth tracking, LD support profile, counselor connect & Family Guidance AI chatbot
"""

import os
import csv
import json
from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, Response, jsonify
)
from config import SECRET_KEY, DEBUG, PORT, HOST, SYNTHETIC_DATA_PATH
from utils.db import (
    init_db, get_all_students, get_student_by_id,
    get_class_analytics, get_principal_analytics, save_student_records,
    save_remedial_plan_db, get_remedial_plan_db,
    save_test_attempt_db, get_student_test_attempts,
    send_teacher_parent_message, reply_teacher_parent_message,
    get_messages_for_parent, get_messages_for_teacher,
    get_question_papers, get_question_paper_by_id, create_question_paper,
    get_student_answer_sheets, get_answer_sheet_by_id, save_student_answer_sheet,
    update_student_teacher_remarks,
    get_ld_screened_students, get_ld_section_summary, update_student_ld_profile,
    set_student_counselor_priority,
    send_counselor_message, reply_counselor_message, get_counselor_messages,
    get_counselor_exercises, create_counselor_exercise, increment_exercise_practice,
    LD_CATEGORIES, LD_STATUSES, COUNSELOR_PRIORITIES
)
from utils.auth import (
    authenticate_user, login_required, teacher_required,
    principal_required, counselor_required, staff_required
)
from utils.i18n import get_text
from models.risk_model import predict_student_risk
from models.explainability import generate_student_explanation_card
from remedial.plan_generator import generate_remedial_plan
from remedial.practice_bank import get_practice_questions
from remedial.test_bank import get_test_for_subject, grade_test_submission
from remedial.ai_tutor import analyze_student_paper_performance, get_question_logic_detail
from remedial.chatbot import generate_ai_chatbot_response, get_starter_chips
from remedial.resources import ONLINE_INTERACTIVE_TOOLS, INDEPENDENT_RESEARCH_REFERENCES
from utils.report_exporter import generate_students_csv

app = Flask(__name__)
app.secret_key = SECRET_KEY

TEACHER_NAMES_MAP = {
    "teacher1": "Mrs. Ananya Sharma (Grade 7 Lead)",
    "teacher2": "Mr. Vikram Iyer (Grade 8 Lead)",
    "teacher3": "Ms. Pooja Verma (Grade 9 Lead)",
    "teacher": "Mrs. Ananya Sharma (Grade 7 Lead)"
}

@app.context_processor
def inject_i18n():
    current_lang = session.get("lang", "en")
    return {
        "lang": current_lang,
        "t": lambda key: get_text(key, lang=current_lang)
    }

def marks_to_words(score):
    ones = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
            "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
            "Seventeen", "Eighteen", "Nineteen"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    try:
        score = round(float(score or 0.0), 1)
    except (ValueError, TypeError):
        score = 0.0

    int_part = int(score)
    dec_part = round(score - int_part, 1)

    if int_part < 20:
        words = ones[int_part]
    elif int_part < 100:
        words = tens[int_part // 10] + (" " + ones[int_part % 10] if int_part % 10 != 0 else "")
    else:
        words = str(int_part)

    if dec_part == 0.5:
        return f"{words} and a Half Marks Only"
    elif dec_part > 0:
        return f"{words} Point Five Marks Only"
    return f"{words} Marks Only"

def roll_to_words(roll):
    digit_words = {"0": "Zero", "1": "One", "2": "Two", "3": "Three", "4": "Four",
                   "5": "Five", "6": "Six", "7": "Seven", "8": "Eight", "9": "Nine"}
    roll_str = str(roll).strip()
    return " ".join(digit_words.get(ch, ch) for ch in roll_str)

app.jinja_env.filters["marks_to_words"] = marks_to_words
app.jinja_env.filters["roll_to_words"] = roll_to_words

@app.route("/")
def index():
    return render_template("index.html", title="SEHAYAK - Home")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "").strip()

        user = authenticate_user(username, password)
        if user:
            session["user"] = {
                "id": user["id"],
                "username": user["username"],
                "full_name": user["full_name"],
                "role": user["role"],
                "student_id": user.get("student_id")
            }
            flash(f"Welcome back, {user['full_name']}!", "success")
            if user["role"] == "principal":
                return redirect(url_for("principal_dashboard"))
            elif user["role"] == "counselor":
                return redirect(url_for("counselor_dashboard"))
            elif user["role"] == "teacher":
                return redirect(url_for("dashboard"))
            elif user["role"] == "parent":
                return redirect(url_for("parent_view"))
            return redirect(url_for("student_portal"))
        else:
            flash("Invalid credentials. Try the quick demo accounts below.", "danger")

    default_role = request.args.get("role", "teacher")
    return render_template("login.html", title="Sign In", default_role=default_role)

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for("login"))

@app.route("/language/<lang>")
def switch_language(lang):
    if lang in ["en", "hi"]:
        session["lang"] = lang
    return redirect(request.referrer or url_for("index"))

# ---------------- Principal Leadership Dashboard ----------------

@app.route("/principal/dashboard")
@principal_required
def principal_dashboard():
    """
    School-wide leadership dashboard across all 300 students and 3 teachers.
    PRIVACY ENFORCEMENT: Does not query or display private teacher-parent chats.
    """
    analytics = get_principal_analytics()
    all_students = get_all_students()

    return render_template(
        "principal_dashboard.html",
        title="Principal Institutional Dashboard",
        analytics=analytics,
        all_students=all_students
    )

# ---------------- Teacher Analytics Dashboard (100 Students) ----------------

@app.route("/dashboard")
@teacher_required
def dashboard():
    user = session.get("user", {})
    user_role = user.get("role")
    
    # If teacher, restrict to their assigned 100 students
    # If principal, allow filter by teacher or view all
    teacher_param = request.args.get("teacher")
    if user_role == "teacher":
        current_teacher_id = user.get("username")
        if current_teacher_id == "teacher": current_teacher_id = "teacher1"
    else:
        current_teacher_id = teacher_param if teacher_param else "all"

    risk_filter = request.args.get("risk", "ALL")
    ld_filter = request.args.get("ld", "ALL")
    search_query = request.args.get("search", "").strip()
    current_lang = session.get("lang", "en")

    students = get_all_students(
        risk_filter=risk_filter,
        search=search_query,
        teacher_id=current_teacher_id,
        ld_filter=ld_filter
    )
    analytics = get_class_analytics(teacher_id=current_teacher_id)
    ld_summary = get_ld_section_summary(teacher_id=current_teacher_id)
    counselor_exercises = get_counselor_exercises()[:3]
    counselor_messages = get_counselor_messages(sender_role="teacher")[:5]

    # Prepare preview reasons
    for s in students:
        try:
            reasons = json.loads(s.get("reasons_json", "{}"))
            lang_reasons = reasons.get(current_lang, reasons.get("en", []))
            s["preview_reason"] = lang_reasons[0] if lang_reasons else "Steady conceptual progress"
        except Exception:
            s["preview_reason"] = "Ongoing academic observation"

    return render_template(
        "dashboard.html",
        title="Teacher Dashboard",
        students=students,
        analytics=analytics,
        ld_summary=ld_summary,
        counselor_exercises=counselor_exercises,
        counselor_messages=counselor_messages,
        current_risk=risk_filter,
        current_ld=ld_filter,
        current_search=search_query,
        current_teacher_id=current_teacher_id
    )

@app.route("/student/<student_id>")
@staff_required
def student_detail(student_id):
    student = get_student_by_id(student_id)
    if not student:
        flash(f"Student record '{student_id}' not found.", "warning")
        if session.get("user", {}).get("role") == "counselor":
            return redirect(url_for("counselor_dashboard"))
        return redirect(url_for("dashboard"))

    current_lang = session.get("lang", "en")
    eval_res = predict_student_risk(student)
    explain_card = generate_student_explanation_card(eval_res, student, lang=current_lang)

    sheets = get_student_answer_sheets(student_id=student_id)
    answer_sheet = sheets[0] if sheets else None
    counselor_messages = get_counselor_messages(student_id=student_id)
    counselor_exercises = get_counselor_exercises(category=student.get("ld_category"))[:3]

    return render_template(
        "student_detail.html",
        title=f"Diagnostic: {student['name']}",
        student=student,
        explain=explain_card,
        eval_res=eval_res,
        answer_sheet=answer_sheet,
        answer_sheets=sheets,
        counselor_messages=counselor_messages,
        counselor_exercises=counselor_exercises,
        ld_categories=LD_CATEGORIES,
        ld_statuses=LD_STATUSES,
        counselor_priorities=COUNSELOR_PRIORITIES
    )

@app.route("/student/<student_id>/update-remarks", methods=["POST"])
@teacher_required
def update_student_remarks_view(student_id):
    weaknesses = request.form.get("teacher_weaknesses", "").strip()
    improvements = request.form.get("teacher_improvements", "").strip()
    remarks = request.form.get("teacher_remarks", "").strip()

    update_student_teacher_remarks(student_id, weaknesses, improvements, remarks)
    flash("Teacher diagnostic remarks on weaknesses and improvements successfully updated!", "success")
    return redirect(url_for("student_detail", student_id=student_id))

@app.route("/teacher/counselor-referral", methods=["POST"])
@teacher_required
def teacher_counselor_referral():
    user = session.get("user", {})
    student_id = request.form.get("student_id", "").strip()
    request_type = request.form.get("request_type", "Referral").strip() or "Referral"
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()
    ld_status = request.form.get("ld_screening_status", "").strip()
    ld_category = request.form.get("ld_category", "").strip()
    redirect_to = request.form.get("redirect_to", "dashboard").strip()

    student = get_student_by_id(student_id)
    if not student:
        flash("Please select a valid student record to message the School Counselor.", "warning")
        return redirect(url_for("dashboard"))

    if ld_status and ld_category:
        existing_notes = student.get("ld_notes") or ""
        updated_notes = existing_notes if not message else f"{existing_notes}\nTeacher Observation: {message}".strip()
        update_student_ld_profile(student_id, ld_status, ld_category, updated_notes, counselor_referred=1)

    if subject and message:
        send_counselor_message(
            student_id=student_id,
            sender_role="teacher",
            sender_username=user.get("username", "teacher1"),
            sender_name=user.get("full_name", "Classroom Teacher"),
            subject=subject,
            message=message,
            request_type=request_type
        )
        flash(f"Counselor {request_type.lower()} submitted for {student['name']}. Dr. Meera Deshmukh will review it shortly.", "success")
    else:
        flash("Please fill in both Subject and Observation details before sending to the School Counselor.", "warning")

    if redirect_to == "detail":
        return redirect(url_for("student_detail", student_id=student_id))
    return redirect(url_for("dashboard", ld="SECTIONED"))

@app.route("/student/<student_id>/remedial")
@teacher_required
def remedial_plan_view(student_id):
    student = get_student_by_id(student_id)
    if not student:
        flash("Student record not found.", "warning")
        return redirect(url_for("dashboard"))

    current_lang = session.get("lang", "en")
    eval_res = predict_student_risk(student)
    plan = generate_remedial_plan(student, eval_res, lang=current_lang)
    saved_plan = get_remedial_plan_db(student_id)

    return render_template(
        "remedial_plan.html",
        title=f"Remedial Plan: {student['name']}",
        student=student,
        plan=plan,
        saved_plan=saved_plan
    )

@app.route("/student/<student_id>/save-plan", methods=["POST"])
@teacher_required
def save_plan(student_id):
    student = get_student_by_id(student_id)
    if not student:
        flash("Student not found.", "danger")
        return redirect(url_for("dashboard"))

    eval_res = predict_student_risk(student)
    plan = generate_remedial_plan(student, eval_res, lang=session.get("lang", "en"))

    notes = request.form.get("teacher_notes", "").strip()
    buddy = request.form.get("assigned_buddy", "").strip()
    status = request.form.get("status", "Active")
    milestones = request.form.getlist("milestones")
    progress_pct = int(request.form.get("progress_pct", 0))

    post_score_raw = request.form.get("post_remedial_score", "").strip()
    post_score = float(post_score_raw) if post_score_raw else None

    save_remedial_plan_db(
        student_id=student_id,
        plan_data=plan,
        teacher_notes=notes,
        buddy=buddy,
        completed_milestones=milestones,
        progress_pct=progress_pct,
        post_remedial_score=post_score
    )

    flash("Remedial action plan, RTI milestones, and teacher notes successfully updated!", "success")
    return redirect(url_for("remedial_plan_view", student_id=student_id))

@app.route("/print/<student_id>")
@teacher_required
def print_report(student_id):
    student = get_student_by_id(student_id)
    if not student:
        flash("Student not found.", "warning")
        return redirect(url_for("dashboard"))

    current_lang = session.get("lang", "en")
    eval_res = predict_student_risk(student)
    explain_card = generate_student_explanation_card(eval_res, student, lang=current_lang)
    plan = generate_remedial_plan(student, eval_res, lang=current_lang)

    return render_template(
        "report_pdf.html",
        student=student,
        explain=explain_card,
        plan=plan
    )

# ---------------- Teacher-Parent Messaging Routes ----------------

@app.route("/teacher/messages")
@teacher_required
def teacher_messages_view():
    user = session.get("user", {})
    t_id = user.get("username", "teacher1")
    if t_id == "teacher": t_id = "teacher1"
    messages = get_messages_for_teacher(t_id)

    return render_template(
        "teacher_messages.html",
        title="Parent Queries Inbox",
        messages=messages
    )

@app.route("/teacher/message/reply", methods=["POST"])
@teacher_required
def teacher_reply_message():
    msg_id = request.form.get("message_id")
    reply_text = request.form.get("reply_text", "").strip()
    if msg_id and reply_text:
        reply_teacher_parent_message(msg_id, reply_text)
        flash("Your response has been delivered to the parent!", "success")
    return redirect(url_for("teacher_messages_view"))

# ---------------- Parent & Family Portal ----------------

@app.route("/parent/view")
def parent_view():
    if "user" not in session or session.get("user", {}).get("role") != "parent":
        flash("Please sign in as a parent.", "warning")
        return redirect(url_for("login"))

    student_id = session["user"].get("student_id") or "SH-2026-001"
    student = get_student_by_id(student_id)
    if not student:
        flash("Associated student record not found.", "warning")
        return redirect(url_for("login"))

    teacher_id = student.get("teacher_id", "teacher1")
    teacher_name = TEACHER_NAMES_MAP.get(teacher_id, "Classroom Lead Teacher")

    current_lang = session.get("lang", "en")
    eval_res = predict_student_risk(student)
    explain_card = generate_student_explanation_card(eval_res, student, lang=current_lang)
    plan = generate_remedial_plan(student, eval_res, lang=current_lang)

    test_attempts = get_student_test_attempts(student_id)
    messages = get_messages_for_parent(student_id)
    sheets = get_student_answer_sheets(student_id=student_id)
    answer_sheet = sheets[0] if sheets else None

    counselor_messages = get_counselor_messages(student_id=student_id)
    all_exercises = get_counselor_exercises(student_id=student_id)
    child_category = student.get("ld_category") or "General"
    recommended_exercises = [
        ex for ex in all_exercises
        if ex.get("assigned_student_id") == student_id
        or child_category == "General"
        or ex["target_category"] in (child_category, "All LD & Focus Learners")
    ] or all_exercises
    chatbot_chips = get_starter_chips(role="parent", student_id=student_id)

    return render_template(
        "parent_view.html",
        title=f"Family Portal: {student['name']}",
        student=student,
        teacher_name=teacher_name,
        explain=explain_card,
        plan=plan,
        test_attempts=test_attempts,
        messages=messages,
        answer_sheet=answer_sheet,
        answer_sheets=sheets,
        counselor_messages=counselor_messages,
        counselor_exercises=recommended_exercises,
        all_counselor_exercises=all_exercises,
        research_references=INDEPENDENT_RESEARCH_REFERENCES,
        interactive_tools=ONLINE_INTERACTIVE_TOOLS,
        chatbot_chips=chatbot_chips
    )

@app.route("/parent/query/send", methods=["POST"])
def parent_send_query():
    if "user" not in session or session.get("user", {}).get("role") != "parent":
        return redirect(url_for("login"))

    student_id = session["user"].get("student_id") or "SH-2026-001"
    student = get_student_by_id(student_id)
    teacher_id = student.get("teacher_id", "teacher1") if student else "teacher1"
    parent_user = session["user"].get("username", "parent")
    parent_name = session["user"].get("full_name", "Parent / Guardian")

    sub = request.form.get("subject", "").strip()
    msg = request.form.get("message", "").strip()

    if sub and msg:
        send_teacher_parent_message(
            student_id=student_id,
            teacher_id=teacher_id,
            parent_username=parent_user,
            sender_role="parent",
            sender_name=parent_name,
            subject=sub,
            message=msg
        )
        flash("Your query has been submitted to your child's teacher!", "success")
    return redirect(url_for("parent_view"))

@app.route("/parent/counselor-message", methods=["POST"])
def parent_send_counselor_message():
    if "user" not in session or session.get("user", {}).get("role") != "parent":
        flash("Please sign in as a parent to message the School Counselor.", "warning")
        return redirect(url_for("login", role="parent"))

    student_id = session["user"].get("student_id") or "SH-2026-001"
    parent_user = session["user"].get("username", "parent1")
    parent_name = session["user"].get("full_name", "Parent / Guardian")
    request_type = request.form.get("request_type", "Query").strip() or "Query"
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()

    if subject and message:
        send_counselor_message(
            student_id=student_id,
            sender_role="parent",
            sender_username=parent_user,
            sender_name=parent_name,
            subject=subject,
            message=message,
            request_type=request_type
        )
        flash("Your message has been delivered to School Counselor Dr. Meera Deshmukh!", "success")
    else:
        flash("Please enter both a subject and a short message for the counselor.", "warning")
    return redirect(url_for("parent_view") + "#counselor-support")

# ---------------- Student Portal & 30-Marks CBSE Assessments ----------------

@app.route("/portal")
@app.route("/student-portal")
def student_portal():
    subject_filter = request.args.get("subject", "all")
    paper_subject = request.args.get("paper_subject", "Mathematics")
    questions = get_practice_questions(subject=subject_filter)

    stu_id = session.get("user", {}).get("student_id") or "SH-2026-001"
    student = get_student_by_id(stu_id)
    test_attempts = get_student_test_attempts(stu_id)

    # Fetch AI Dyslexia Learning Logic & Paper Performance
    paper_performance = analyze_student_paper_performance(stu_id, target_subject=paper_subject)
    counselor_messages = get_counselor_messages(student_id=stu_id)
    counselor_exercises = get_counselor_exercises(student_id=stu_id)
    chatbot_chips = get_starter_chips(role="student", student_id=stu_id)

    return render_template(
        "student_portal.html",
        title="Student Practice & AI Logic Portal",
        student=student,
        questions=questions,
        current_subject=subject_filter,
        paper_subject=paper_subject,
        test_attempts=test_attempts,
        paper_performance=paper_performance,
        counselor_messages=counselor_messages,
        counselor_exercises=counselor_exercises,
        research_references=INDEPENDENT_RESEARCH_REFERENCES,
        interactive_tools=ONLINE_INTERACTIVE_TOOLS,
        chatbot_chips=chatbot_chips
    )

@app.route("/student/counselor-message", methods=["POST"])
def student_send_counselor_message():
    user = session.get("user", {})
    stu_id = user.get("student_id") or "SH-2026-001"
    student = get_student_by_id(stu_id)
    sender_user = user.get("username") or "student1"
    sender_name = (student.get("name") if student else None) or user.get("full_name") or "Aarav Sharma"

    request_type = request.form.get("request_type", "Check-In").strip() or "Check-In"
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()

    if subject and message:
        send_counselor_message(
            student_id=stu_id,
            sender_role="student",
            sender_username=sender_user,
            sender_name=sender_name,
            subject=subject,
            message=message,
            request_type=request_type
        )
        flash("Your message was sent safely to School Counselor Dr. Meera Deshmukh!", "success")
    else:
        flash("Please type a topic and message before sending.", "warning")
    return redirect(url_for("student_portal") + "#counselor-connect")

@app.route("/exercise/<int:ex_id>/practice", methods=["POST"])
def mark_exercise_practiced(ex_id):
    updated = increment_exercise_practice(ex_id)
    if not updated:
        if request.is_json:
            return jsonify({"status": "error", "message": "Exercise not found"}), 404
        flash("Exercise not found.", "warning")
        return redirect(request.referrer or url_for("student_portal"))

    if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({
            "status": "success",
            "exercise_id": ex_id,
            "practice_count": updated["practice_count"]
        })

    flash(f"Great job practicing '{updated['title']}'! Total practice logs: {updated['practice_count']}.", "success")
    return redirect(request.referrer or url_for("student_portal"))

@app.route("/api/chatbot", methods=["POST"])
def api_chatbot():
    payload = request.get_json(silent=True) or {}
    user_msg = (payload.get("message") or request.form.get("message") or "").strip()
    requested_role = (payload.get("role") or request.form.get("role") or "").strip().lower()

    user = session.get("user", {})
    session_role = user.get("role", "")
    if session_role in ("parent", "student"):
        chat_role = session_role
    elif requested_role in ("parent", "student"):
        chat_role = requested_role
    else:
        chat_role = "student"

    stu_id = user.get("student_id") or "SH-2026-001"
    if not user_msg:
        return jsonify({
            "status": "success",
            "answer": "Please type any question about your marks, study techniques, learning support, or reaching the School Counselor.",
            "highlights": ["Ready to Help"],
            "suggested_questions": get_starter_chips(chat_role, stu_id)[:4]
        })

    result = generate_ai_chatbot_response(user_msg, role=chat_role, student_id=stu_id)
    return jsonify({
        "status": "success",
        **result
    })

@app.route("/api/ai-explain-question")
def api_ai_explain_question():
    q_num = request.args.get("q", 3)
    subject = request.args.get("subject", "Mathematics")
    logic_detail = get_question_logic_detail(q_num, subject=subject)
    return jsonify({
        "status": "success",
        "data": logic_detail
    })

# ---------------- School Counselor Workspace Routes ----------------

@app.route("/counselor/dashboard")
@counselor_required
def counselor_dashboard():
    status_filter = request.args.get("ld_status", "ALL")
    category_filter = request.args.get("ld_category", "ALL")
    priority_filter = request.args.get("priority", "ALL")
    scope = request.args.get("scope", "sectioned")
    msg_role_filter = request.args.get("msg_role", "ALL")
    search_query = request.args.get("search", "").strip()

    include_all = (scope == "all") or (priority_filter == "Not Priority") or bool(search_query)
    screened_students = get_ld_screened_students(
        status_filter=status_filter,
        category_filter=category_filter,
        priority_filter=priority_filter,
        search=search_query,
        include_all=include_all
    )
    all_students = get_all_students()
    ld_summary = get_ld_section_summary()
    messages = get_counselor_messages(sender_role=msg_role_filter)
    pending_count = sum(1 for m in messages if m.get("status") == "Pending")
    exercises = get_counselor_exercises()

    return render_template(
        "counselor_dashboard.html",
        title="School Counselor Workspace",
        screened_students=screened_students,
        all_students=all_students,
        ld_summary=ld_summary,
        messages=messages,
        pending_count=pending_count,
        exercises=exercises,
        ld_statuses=LD_STATUSES,
        ld_categories=LD_CATEGORIES,
        counselor_priorities=COUNSELOR_PRIORITIES,
        interactive_tools=ONLINE_INTERACTIVE_TOOLS,
        research_references=INDEPENDENT_RESEARCH_REFERENCES,
        current_ld_status=status_filter,
        current_ld_category=category_filter,
        current_priority=priority_filter,
        current_scope=scope,
        current_msg_role=msg_role_filter,
        current_search=search_query
    )


@app.route("/counselor/set-priority", methods=["POST"])
@counselor_required
def counselor_set_priority():
    data = request.get_json(silent=True) or request.form
    student_id = (data.get("student_id") or "").strip()
    priority_level = (data.get("counselor_priority") or "").strip()
    redirect_to = (data.get("redirect_to") or "roster").strip()

    student = get_student_by_id(student_id)
    if not student or priority_level not in COUNSELOR_PRIORITIES:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json:
            return jsonify({"status": "error", "message": "Invalid student or priority selection."}), 400
        flash("Please choose a valid student and priority option (Priority, Monitoring, or Not Priority).", "warning")
        return redirect(url_for("counselor_dashboard") + "#ld-roster")

    saved_priority = set_student_counselor_priority(student_id, priority_level)
    if request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json:
        return jsonify({
            "status": "success",
            "student_id": student_id,
            "counselor_priority": saved_priority,
            "summary": get_ld_section_summary()
        })

    flash(f"Marked {student['name']} ({student_id}) as {saved_priority}.", "success")
    if redirect_to == "detail":
        return redirect(url_for("student_detail", student_id=student_id) + "#counselor-teacher-connect")
    return redirect(url_for(
        "counselor_dashboard",
        ld_status=data.get("ld_status", "ALL"),
        ld_category=data.get("ld_category", "ALL"),
        priority=data.get("priority", "ALL"),
        scope=data.get("scope", "sectioned"),
        search=data.get("search", "")
    ) + "#ld-roster")

@app.route("/counselor/reply", methods=["POST"])
@counselor_required
def counselor_reply_message():
    msg_id = request.form.get("message_id")
    reply_text = request.form.get("reply_text", "").strip()
    if msg_id and reply_text:
        reply_counselor_message(msg_id, reply_text)
        flash("Your guidance reply has been sent and is visible in the Student/Parent/Teacher portal!", "success")
    else:
        flash("Please type a clear supportive reply before sending.", "warning")
    return redirect(url_for("counselor_dashboard") + "#counselor-inbox")

@app.route("/counselor/exercises/add", methods=["POST"])
@counselor_required
def counselor_add_exercise():
    title = request.form.get("title", "").strip()
    target_category = request.form.get("target_category", "All LD & Focus Learners").strip()
    target_audience = request.form.get("target_audience", "Students & Parents at Home").strip()
    difficulty_level = request.form.get("difficulty_level", "Gentle Starter").strip()
    duration_mins = request.form.get("duration_mins", 10)
    simple_goal = request.form.get("simple_goal", "").strip()
    study_technique = request.form.get("study_technique", "").strip()
    steps_raw = request.form.get("steps_raw", "").strip()
    home_tip = request.form.get("home_tip", "").strip()
    interactive_tool = request.form.get("interactive_tool", "chunk_highlighter").strip()
    assigned_student_id = request.form.get("assigned_student_id", "ALL").strip() or "ALL"
    external_practice_url = request.form.get("external_practice_url", "").strip()
    external_site_name = request.form.get("external_site_name", "").strip()
    reference_source_name = request.form.get("reference_source_name", "").strip()
    reference_url = request.form.get("reference_url", "").strip()
    reference_summary = request.form.get("reference_summary", "").strip()

    if external_practice_url and interactive_tool not in ("none", ""):
        exercise_mode = "Online Mini-Lab + External Sim"
    elif external_practice_url:
        exercise_mode = "External Interactive Practice"
    elif interactive_tool not in ("none", ""):
        exercise_mode = "Online Mini-Lab + Guide"
    else:
        exercise_mode = "Guided Routine"

    steps_list = [line.strip() for line in steps_raw.splitlines() if line.strip()]
    if title and simple_goal and steps_list:
        counselor_name = session.get("user", {}).get("full_name", "Dr. Meera Deshmukh (School Counselor)")
        create_counselor_exercise(
            title=title,
            target_category=target_category,
            target_audience=target_audience,
            difficulty_level=difficulty_level,
            duration_mins=duration_mins,
            simple_goal=simple_goal,
            steps_list=steps_list,
            study_technique=study_technique or "Visual Step Practice",
            home_tip=home_tip or "Practice calmly for 10 minutes with encouragement.",
            updated_by=counselor_name,
            exercise_mode=exercise_mode,
            interactive_tool=interactive_tool,
            assigned_student_id=assigned_student_id,
            external_practice_url=external_practice_url,
            external_site_name=external_site_name,
            reference_source_name=reference_source_name,
            reference_url=reference_url,
            reference_summary=reference_summary
        )
        flash(f"New online study exercise '{title}' assigned and published across Student, Parent, and Teacher portals!", "success")
    else:
        flash("Please provide an Exercise Title, Simple Goal, and at least one Step.", "warning")
    return redirect(url_for("counselor_dashboard") + "#exercise-publisher")

@app.route("/counselor/update-student-ld", methods=["POST"])
@counselor_required
def counselor_update_student_ld():
    student_id = request.form.get("student_id", "").strip()
    ld_status = request.form.get("ld_screening_status", "Possibility / Early Screening").strip()
    ld_category = request.form.get("ld_category", "Dyslexia / Visual Reading").strip()
    ld_notes = request.form.get("ld_notes", "").strip()
    counselor_priority = request.form.get("counselor_priority", "").strip() or None
    counselor_referred = 1 if request.form.get("counselor_referred") else 0
    redirect_to = request.form.get("redirect_to", "roster").strip()

    student = get_student_by_id(student_id)
    if not student:
        flash("Student ID not found.", "warning")
        return redirect(url_for("counselor_dashboard"))

    update_student_ld_profile(
        student_id, ld_status, ld_category, ld_notes,
        counselor_referred=counselor_referred,
        counselor_priority=counselor_priority
    )
    prio_note = f", Priority: {counselor_priority}" if counselor_priority else ""
    flash(f"Updated support profile for {student['name']} ({ld_status} - {ld_category}{prio_note}).", "success")
    if redirect_to == "detail":
        return redirect(url_for("student_detail", student_id=student_id) + "#counselor-teacher-connect")
    return redirect(url_for("counselor_dashboard") + "#ld-roster")

@app.route("/take-test")
def take_test_view():
    selected_sub = request.args.get("subject", "mathematics").lower().strip()
    test_data = get_test_for_subject(selected_sub)
    return render_template(
        "take_test.html",
        title=f"CBSE 30-Marks Test: {test_data['title']}",
        selected_subject=selected_sub,
        current_test=test_data
    )

@app.route("/student/test/submit", methods=["POST"])
def submit_test():
    sub_key = request.form.get("subject", "mathematics").lower().strip()

    # Extract MCQ answers
    mcq_answers = {}
    written_answers = {}
    for k, v in request.form.items():
        if k.startswith("mcq_"):
            mcq_answers[k[4:]] = v
        elif k.startswith("written_"):
            written_answers[k[8:]] = v

    # Grade test submission
    result = grade_test_submission(sub_key, mcq_answers, written_answers)

    # Determine student ID from session or default
    stu_id = session.get("user", {}).get("student_id", "SH-2026-001")
    save_test_attempt_db(stu_id, result)

    flash(f"Assessment completed! You scored {result['total_score']}/30 marks!", "success")
    return render_template(
        "test_results.html",
        title=f"Test Results: {result['subject_name']}",
        result=result
    )

# ---------------- Data Upload & Export ----------------

@app.route("/upload", methods=["GET", "POST"])
@teacher_required
def upload_data():
    if request.method == "POST":
        if "csv_file" not in request.files:
            flash("No file part provided.", "danger")
            return redirect(request.url)

        file = request.files["csv_file"]
        if file.filename == "":
            flash("Please choose a CSV file to upload.", "warning")
            return redirect(request.url)

        if not file.filename.endswith(".csv"):
            flash("Invalid format: please upload a .csv file.", "danger")
            return redirect(request.url)

        try:
            content = file.stream.read().decode("utf-8-sig")
            reader = list(csv.DictReader(content.splitlines()))
            if not reader:
                flash("Uploaded CSV file appears to be empty.", "warning")
                return redirect(request.url)

            stats = save_student_records(reader)
            flash(f"Successfully processed {stats['total_records']} student assessment records!", "success")
            return redirect(url_for("dashboard"))
        except Exception as e:
            flash(f"Error parsing assessment CSV: {str(e)}", "danger")
            return redirect(request.url)

    return render_template("upload.html", title="Upload Student Data")

@app.route("/export-csv")
@teacher_required
def export_students_csv():
    risk_filter = request.args.get("risk", "ALL")
    students = get_all_students(risk_filter=risk_filter)
    csv_data = generate_students_csv(students)
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename=sehayak_students_{risk_filter.lower()}.csv"}
    )

@app.route("/download-sample-csv")
def download_sample_csv():
    if not os.path.exists(SYNTHETIC_DATA_PATH):
        from utils.data_generator import generate_synthetic_dataset
        generate_synthetic_dataset(num_students=300, output_path=SYNTHETIC_DATA_PATH)

    with open(SYNTHETIC_DATA_PATH, "r", encoding="utf-8") as f:
        data = f.read()

    return Response(
        data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=sehayak_sample_300_students.csv"}
    )

# ---------------- Question Papers & Answer Sheets ----------------

@app.route("/teacher/question-papers", methods=["GET", "POST"])
@teacher_required
def question_papers_view():
    user = session.get("user", {})
    t_id = user.get("username", "teacher1")
    if t_id == "teacher": t_id = "teacher1"

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        subject = request.form.get("subject", "Mathematics").strip()
        grade = request.form.get("grade", "Class 7").strip()
        exam_name = request.form.get("exam_name", "Annual Examination").strip()

        file_path = ""
        if "paper_file" in request.files:
            pfile = request.files["paper_file"]
            if pfile and pfile.filename:
                upload_dir = os.path.join(app.static_folder, "uploads", "question_papers")
                os.makedirs(upload_dir, exist_ok=True)
                safe_name = f"qp_{grade.replace(' ', '_')}_{subject.replace(' ', '_')}_{pfile.filename}"
                saved_loc = os.path.join(upload_dir, safe_name)
                pfile.save(saved_loc)
                file_path = url_for("static", filename=f"uploads/question_papers/{safe_name}")

        questions_sequence = []
        for q in range(1, 6):
            questions_sequence.append({"q": q, "max": 1.0, "type": "VSA / MCQ (1 Mark)"})
        for q in range(6, 11):
            questions_sequence.append({"q": q, "max": 2.0, "type": "Short Answer (2 Marks)"})
        for q in range(11, 14):
            questions_sequence.append({"q": q, "max": 5.0, "type": "Long Answer (5 Marks)"})
        for q in range(14, 16):
            questions_sequence.append({"q": q, "max": 10.0, "type": "Extended / Essay (10 Marks)"})

        total_marks = 50.0
        total_questions = 15

        create_question_paper(
            title=title,
            subject=subject,
            grade=grade,
            exam_name=exam_name,
            total_marks=total_marks,
            total_questions=total_questions,
            file_path=file_path,
            questions_sequence=questions_sequence,
            teacher_id=t_id
        )
        flash("Question paper and 15-question rubric registered successfully!", "success")
        return redirect(url_for("question_papers_view"))

    papers = get_question_papers()
    return render_template(
        "question_papers.html",
        title="Question Papers Repository",
        papers=papers
    )

@app.route("/teacher/answer-sheets")
@teacher_required
def answer_sheets_list():
    sheets = get_student_answer_sheets()
    return render_template(
        "answer_sheets_list.html",
        title="Evaluated Answer Sheets",
        sheets=sheets
    )

@app.route("/teacher/answer-sheet/upload", methods=["GET", "POST"])
@teacher_required
def upload_answer_sheet_view():
    user = session.get("user", {})
    t_id = user.get("username", "teacher1")
    if t_id == "teacher": t_id = "teacher1"

    if request.method == "POST":
        student_id = request.form.get("student_id", "").strip()
        qp_id_raw = request.form.get("question_paper_id", "1").strip()
        question_paper_id = int(qp_id_raw) if qp_id_raw.isdigit() else 1
        subject = request.form.get("subject", "Mathematics").strip()
        exam_name = request.form.get("exam_name", "Half Yearly Examination (2026-2027)").strip()
        roll_no = request.form.get("roll_no", "2026001").strip()
        medium = request.form.get("medium", "English").strip()
        teacher_weaknesses = request.form.get("teacher_weaknesses", "").strip()
        teacher_improvements = request.form.get("teacher_improvements", "").strip()
        teacher_general_remarks = request.form.get("teacher_general_remarks", "").strip()
        examiner_name = request.form.get("examiner_name", user.get("full_name", "Mrs. Ananya Sharma")).strip()

        sheet_image_url = url_for("static", filename="uploads/answer_sheets/sample_cbse_front_sheet.png")
        if "sheet_image" in request.files:
            sfile = request.files["sheet_image"]
            if sfile and sfile.filename:
                upload_dir = os.path.join(app.static_folder, "uploads", "answer_sheets")
                os.makedirs(upload_dir, exist_ok=True)
                safe_name = f"sheet_{student_id}_{sfile.filename}"
                saved_loc = os.path.join(upload_dir, safe_name)
                sfile.save(saved_loc)
                sheet_image_url = url_for("static", filename=f"uploads/answer_sheets/{safe_name}")

        question_marks_dict = {}
        total_marks_obtained = 0.0
        for q in range(1, 31):
            if f"q_{q}" in request.form:
                val_str = request.form.get(f"q_{q}", "0")
                try:
                    val = float(val_str)
                except ValueError:
                    val = 0.0
                question_marks_dict[str(q)] = val
                question_marks_dict[f"q{q}"] = val
                total_marks_obtained += val

        total_marks_obtained = round(total_marks_obtained, 1)
        total_max_marks = 50.0

        sheet_id = save_student_answer_sheet(
            student_id=student_id,
            question_paper_id=question_paper_id,
            subject=subject,
            exam_name=exam_name,
            roll_no=roll_no,
            medium=medium,
            sheet_image_url=sheet_image_url,
            question_marks_dict=question_marks_dict,
            total_marks_obtained=total_marks_obtained,
            total_max_marks=total_max_marks,
            teacher_id=t_id,
            teacher_weaknesses=teacher_weaknesses,
            teacher_improvements=teacher_improvements,
            teacher_general_remarks=teacher_general_remarks,
            examiner_name=examiner_name
        )

        flash(f"Answer sheet for student {student_id} successfully saved! Total Marks: {total_marks_obtained}/{total_max_marks}", "success")
        return redirect(url_for("view_answer_sheet", sheet_id=sheet_id))

    students = get_all_students(teacher_id=t_id)
    if not students:
        students = get_all_students()
    question_papers = get_question_papers()
    return render_template(
        "upload_answer_sheet.html",
        title="Upload & Grade Answer Sheet",
        students=students,
        question_papers=question_papers
    )

@app.route("/answer-sheet/<int:sheet_id>")
def view_answer_sheet(sheet_id):
    sheet = get_answer_sheet_by_id(sheet_id)
    if not sheet:
        flash("Answer sheet record not found.", "warning")
        return redirect(url_for("dashboard"))

    return render_template(
        "view_answer_sheet.html",
        title=f"Answer Sheet: {sheet['student_name']} - {sheet['subject']}",
        sheet=sheet
    )

# ---------------- Application Initialization ----------------

def ensure_initialized():
    """Ensure database schema and dataset are loaded before servicing requests."""
    init_db()

ensure_initialized()

if __name__ == "__main__":
    print("=" * 60)
    print("  SEHAYAK (सहायक) - Slow Learner Support System")
    print("  Problem Statement ID: PSB152 | Ministry of Education")
    print(f"  Starting local server at http://{HOST}:{PORT}")
    print("=" * 60)
    app.run(host=HOST, port=PORT, debug=DEBUG)
