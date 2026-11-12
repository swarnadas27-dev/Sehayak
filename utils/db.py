"""
SEHAYAK (सहायक) - SQLite Database & Storage Layer
Supports 5 distinct roles:
 1. Principal (School-wide leadership, all 300 students, teacher comparison, strict privacy on chats)
 2. 3 Teachers (each managing 100 students, RTI tracking, parent chat/queries, counselor referrals)
 3. School Counselor (Learning disability screening section, student/parent/teacher support inbox, study exercises)
 4. Students (CBSE 30-mark assessments, AI logic clinic, study exercises, counselor & AI chatbot)
 5. Parents (Confidential child progress tracking, LD support profile, teacher/counselor connect & AI chatbot)
"""

import os
import sqlite3
import json
from werkzeug.security import generate_password_hash, check_password_hash
from config import DB_PATH, SYNTHETIC_DATA_PATH
from utils.data_cleaner import clean_student_records
from models.risk_model import predict_student_risk

def get_connection():
    """Create or connect to SQLite database with row factory."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize schema tables and seed demo accounts + 300 synthetic records."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL,
            student_id TEXT,
            assigned_grade TEXT,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 2. Students Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            grade TEXT,
            section TEXT,
            teacher_id TEXT DEFAULT 'teacher1',
            gender TEXT,
            attendance_rate REAL,
            assignment_completion_rate REAL,
            homework_accuracy REAL,
            class_participation REAL,
            reading_speed_wpm REAL,
            visual_preference TEXT,
            overall_avg REAL,
            term1_avg REAL,
            term2_avg REAL,
            trend_slope REAL,
            math_fa1 REAL, math_sa1 REAL, math_fa2 REAL, math_sa2 REAL,
            science_fa1 REAL, science_sa1 REAL, science_fa2 REAL, science_sa2 REAL,
            english_fa1 REAL, english_sa1 REAL, english_fa2 REAL, english_sa2 REAL,
            social_fa1 REAL, social_sa1 REAL, social_fa2 REAL, social_sa2 REAL,
            hindi_fa1 REAL, hindi_sa1 REAL, hindi_fa2 REAL, hindi_sa2 REAL,
            risk_level TEXT,
            risk_score REAL,
            support_needed INTEGER,
            reasons_json TEXT,
            strengths_json TEXT,
            weak_subjects_json TEXT,
            archetype TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 3. Remedial Action Plans Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS remedial_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            plan_json TEXT NOT NULL,
            status TEXT DEFAULT 'Active',
            teacher_notes TEXT,
            assigned_buddy TEXT,
            completed_milestones TEXT DEFAULT '[]',
            progress_pct INTEGER DEFAULT 0,
            post_remedial_score REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    """)

    # 4. Teacher-Parent Private Query & Chat Table
    # NOTE: Strictly accessible only by the assigned teacher and parent. Principal has no access.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teacher_parent_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            teacher_id TEXT NOT NULL,
            parent_username TEXT NOT NULL,
            sender_role TEXT NOT NULL,
            sender_name TEXT NOT NULL,
            subject TEXT,
            message TEXT NOT NULL,
            reply TEXT,
            status TEXT DEFAULT 'Open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    """)

    # 5. Student 30-Marks Test Attempts Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_test_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            subject TEXT NOT NULL,
            subject_key TEXT NOT NULL,
            total_score REAL NOT NULL,
            max_score REAL DEFAULT 30,
            percentage REAL NOT NULL,
            mcq_score REAL NOT NULL,
            written_score REAL NOT NULL,
            badge TEXT,
            results_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    """)

    # 6. Question Papers Table (Uploaded by Teachers / Evaluators)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS question_papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subject TEXT NOT NULL,
            grade TEXT NOT NULL,
            exam_name TEXT NOT NULL,
            total_marks INTEGER DEFAULT 50,
            total_questions INTEGER DEFAULT 31,
            file_path TEXT,
            questions_sequence_json TEXT,
            teacher_id TEXT DEFAULT 'teacher1',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 7. Student Answer Sheets (Front-Page Marks Tabulation & Teacher Diagnostic Remarks)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_answer_sheets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            question_paper_id INTEGER,
            subject TEXT NOT NULL,
            exam_name TEXT NOT NULL,
            roll_no TEXT,
            medium TEXT DEFAULT 'English',
            sheet_image_url TEXT DEFAULT '/static/uploads/answer_sheets/sample_cbse_front_sheet.png',
            question_marks_json TEXT,
            total_marks_obtained REAL,
            total_max_marks REAL DEFAULT 50,
            teacher_id TEXT DEFAULT 'teacher1',
            teacher_weaknesses TEXT,
            teacher_improvements TEXT,
            teacher_general_remarks TEXT,
            examiner_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (question_paper_id) REFERENCES question_papers(id)
        )
    """)

    # 8. School Counselor Inbox (Student / Parent / Teacher <-> Counselor)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS counselor_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            sender_role TEXT NOT NULL,
            sender_username TEXT NOT NULL,
            sender_name TEXT NOT NULL,
            request_type TEXT DEFAULT 'Query',
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            reply TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    """)

    # 9. Counselor Study Techniques & Guided Exercises Library
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS counselor_exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            target_category TEXT NOT NULL,
            target_audience TEXT DEFAULT 'All LD & Focus Learners',
            difficulty_level TEXT DEFAULT 'Gentle Starter',
            duration_mins INTEGER DEFAULT 10,
            simple_goal TEXT NOT NULL,
            step_by_step_json TEXT NOT NULL,
            study_technique TEXT NOT NULL,
            home_tip TEXT NOT NULL,
            exercise_mode TEXT DEFAULT 'Online Mini-Lab + Guide',
            interactive_tool TEXT DEFAULT 'chunk_highlighter',
            assigned_student_id TEXT DEFAULT 'ALL',
            external_practice_url TEXT DEFAULT '',
            external_site_name TEXT DEFAULT '',
            reference_source_name TEXT DEFAULT '',
            reference_url TEXT DEFAULT '',
            reference_summary TEXT DEFAULT '',
            updated_by TEXT DEFAULT 'Dr. Meera Deshmukh (School Counselor)',
            practice_count INTEGER DEFAULT 0,
            is_featured INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    for col, typ in [
        ("exercise_mode", "TEXT DEFAULT 'Online Mini-Lab + Guide'"),
        ("interactive_tool", "TEXT DEFAULT 'chunk_highlighter'"),
        ("assigned_student_id", "TEXT DEFAULT 'ALL'"),
        ("external_practice_url", "TEXT DEFAULT ''"),
        ("external_site_name", "TEXT DEFAULT ''"),
        ("reference_source_name", "TEXT DEFAULT ''"),
        ("reference_url", "TEXT DEFAULT ''"),
        ("reference_summary", "TEXT DEFAULT ''"),
    ]:
        try:
            cursor.execute(f"ALTER TABLE counselor_exercises ADD COLUMN {col} {typ}")
        except sqlite3.OperationalError:
            pass

    # Add columns safely if previously existing
    for col, typ in [
        ("teacher_id", "TEXT DEFAULT 'teacher1'"),
        ("student_id", "TEXT"),
        ("assigned_grade", "TEXT"),
        ("teacher_weaknesses", "TEXT"),
        ("teacher_improvements", "TEXT"),
        ("teacher_remarks", "TEXT")
    ]:
        try:
            cursor.execute(f"ALTER TABLE students ADD COLUMN {col} {typ}")
        except sqlite3.OperationalError: pass
        try:
            cursor.execute(f"ALTER TABLE users ADD COLUMN {col} {typ}")
        except sqlite3.OperationalError: pass

    for col, typ in [
        ("ld_screening_status", "TEXT DEFAULT 'None'"),
        ("ld_category", "TEXT DEFAULT 'General'"),
        ("ld_notes", "TEXT DEFAULT ''"),
        ("counselor_referred", "INTEGER DEFAULT 0"),
        ("counselor_priority", "TEXT DEFAULT 'Not Priority'")
    ]:
        try:
            cursor.execute(f"ALTER TABLE students ADD COLUMN {col} {typ}")
        except sqlite3.OperationalError:
            pass

    conn.commit()

    # Seed All 5 Roles: Principal, 3 Teachers, School Counselor, 3 Students, 3 Parents
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'principal'")
    if cursor.fetchone()[0] == 0:
        seed_users(cursor)
        conn.commit()

    # Ensure Counselor demo user exists even on pre-existing DBs
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'counselor'")
    if cursor.fetchone()[0] == 0:
        for cu, cp, cname in [
            ("counselor1", "counselor123", "Dr. Meera Deshmukh (School Counselor)"),
            ("counselor", "counselor123", "Dr. Meera Deshmukh (School Counselor)"),
        ]:
            cursor.execute("""
                INSERT OR REPLACE INTO users (username, password_hash, full_name, role, student_id, assigned_grade, email)
                VALUES (?, ?, ?, 'counselor', NULL, 'All', ?)
            """, (cu, generate_password_hash(cp), cname, f"{cu}@sehayak.edu.in"))
        conn.commit()

    # Seed 300 students if count < 300
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]
    if count < 300:
        print("[SEHAYAK DB] Populating 300 students (100 per teacher)...")
        from utils.data_generator import generate_synthetic_dataset
        generate_synthetic_dataset(num_students=300, output_path=SYNTHETIC_DATA_PATH)
        
        import csv
        with open(SYNTHETIC_DATA_PATH, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            save_student_records(reader)

    # Seed initial sample parent-teacher query for demonstration
    cursor.execute("SELECT COUNT(*) FROM teacher_parent_messages")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO teacher_parent_messages (
                student_id, teacher_id, parent_username, sender_role, sender_name, subject, message, reply, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "SH-2026-001", "teacher1", "parent1", "parent", "Mr. Suresh Sharma",
            "Inquiry on Mathematics CRA manipulatives at home",
            "Hello Mrs. Sharma, Aarav mentioned using color-coded fraction bars in class. Could you advise what materials we can use for practice at home?",
            "Dear Mr. Sharma, simple paper strips with different colors or lego blocks work wonderfully! I have also enabled visual fractions on Aarav's practice portal.",
            "Replied"
        ))
        conn.commit()

    # Seed Sample Question Papers if empty
    cursor.execute("SELECT COUNT(*) FROM question_papers")
    if cursor.fetchone()[0] == 0:
        seed_sample_question_papers(cursor)
        conn.commit()

    # Seed Sample Answer Sheets with 1-to-15 Question Sequence if empty
    cursor.execute("SELECT COUNT(*) FROM student_answer_sheets")
    if cursor.fetchone()[0] == 0:
        seed_sample_answer_sheets(cursor)
        conn.commit()

    # Section / tag LD & Screening-Possibility students cleanly within existing 300 records
    ensure_ld_profiles_seeded(cursor)
    backfill_counselor_priorities(cursor)
    conn.commit()

    # Seed initial Counselor messages across Student / Parent / Teacher roles
    ensure_counselor_messages_seeded(cursor)
    conn.commit()

    # Seed initial simple Study Technique Exercises from Counselor
    ensure_counselor_exercises_seeded(cursor)
    backfill_counselor_exercise_references(cursor)
    conn.commit()

    conn.close()

def seed_users(cursor):
    """Seed multi-role users with hashed credentials."""
    users = [
        # 1. Principal
        ("principal", "principal123", "Dr. Rajesh Gupta (Principal)", "principal", None, "All"),

        # 2. School Counselor
        ("counselor1", "counselor123", "Dr. Meera Deshmukh (School Counselor)", "counselor", None, "All"),
        ("counselor", "counselor123", "Dr. Meera Deshmukh (School Counselor)", "counselor", None, "All"),

        # 3. Teachers (3 Teachers, 100 students each)
        ("teacher1", "teacher123", "Mrs. Ananya Sharma (Grade 7 Lead)", "teacher", None, "Class 7"),
        ("teacher2", "teacher123", "Mr. Vikram Iyer (Grade 8 Lead)", "teacher", None, "Class 8"),
        ("teacher3", "teacher123", "Ms. Pooja Verma (Grade 9 Lead)", "teacher", None, "Class 9"),
        ("teacher", "teacher123", "Mrs. Ananya Sharma (Grade 7 Lead)", "teacher", None, "Class 7"), # alias

        # 4. Students (3 showcase students)
        ("student1", "student123", "Aarav Sharma", "student", "SH-2026-001", "Class 7-A"),
        ("student2", "student123", "Diya Patel", "student", "SH-2026-101", "Class 8-B"),
        ("student3", "student123", "Mohammed Faizan", "student", "SH-2026-201", "Class 9-A"),
        ("student", "student123", "Aarav Sharma", "student", "SH-2026-001", "Class 7-A"), # alias

        # 5. Parents (3 showcase parents)
        ("parent1", "parent123", "Mr. Suresh Sharma (Parent of Aarav)", "parent", "SH-2026-001", "Class 7-A"),
        ("parent2", "parent123", "Mrs. Gita Patel (Parent of Diya)", "parent", "SH-2026-101", "Class 8-B"),
        ("parent3", "parent123", "Mr. Imran Faizan (Parent of Faizan)", "parent", "SH-2026-201", "Class 9-A"),
        ("parent", "parent123", "Mr. Suresh Sharma (Parent of Aarav)", "parent", "SH-2026-001", "Class 7-A") # alias
    ]

    for u, p, name, role, stu_id, gr in users:
        pw_hash = generate_password_hash(p)
        cursor.execute("""
            INSERT OR REPLACE INTO users (username, password_hash, full_name, role, student_id, assigned_grade, email)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (u, pw_hash, name, role, stu_id, gr, f"{u}@sehayak.edu.in"))
    print("[SEHAYAK DB] Seeded 1 Principal, 1 Counselor, 3 Teachers, 3 Students, and 3 Parents.")

def save_student_records(raw_records):
    """Clean, assess risk, and upsert batch student records."""
    cleaned, stats = clean_student_records(raw_records)
    conn = get_connection()
    cursor = conn.cursor()

    for row in cleaned:
        eval_res = predict_student_risk(row)

        cursor.execute("""
            INSERT INTO students (
                student_id, name, grade, section, teacher_id, gender,
                attendance_rate, assignment_completion_rate, homework_accuracy,
                class_participation, reading_speed_wpm, visual_preference,
                overall_avg, term1_avg, term2_avg, trend_slope,
                math_fa1, math_sa1, math_fa2, math_sa2,
                science_fa1, science_sa1, science_fa2, science_sa2,
                english_fa1, english_sa1, english_fa2, english_sa2,
                social_fa1, social_sa1, social_fa2, social_sa2,
                hindi_fa1, hindi_sa1, hindi_fa2, hindi_sa2,
                risk_level, risk_score, support_needed,
                reasons_json, strengths_json, weak_subjects_json, archetype
            ) VALUES (
                ?, ?, ?, ?, ?, ?,
                ?, ?, ?,
                ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?,
                ?, ?, ?, ?
            )
            ON CONFLICT(student_id) DO UPDATE SET
                name=excluded.name,
                grade=excluded.grade,
                section=excluded.section,
                teacher_id=excluded.teacher_id,
                attendance_rate=excluded.attendance_rate,
                assignment_completion_rate=excluded.assignment_completion_rate,
                overall_avg=excluded.overall_avg,
                term2_avg=excluded.term2_avg,
                trend_slope=excluded.trend_slope,
                risk_level=excluded.risk_level,
                risk_score=excluded.risk_score,
                support_needed=excluded.support_needed,
                reasons_json=excluded.reasons_json,
                strengths_json=excluded.strengths_json,
                weak_subjects_json=excluded.weak_subjects_json,
                updated_at=CURRENT_TIMESTAMP
        """, (
            row["student_id"], row["name"], row["grade"], row["section"], row.get("teacher_id", "teacher1"), row["gender"],
            row["attendance_rate"], row["assignment_completion_rate"], row["homework_accuracy"],
            row["class_participation"], row["reading_speed_wpm"], row["visual_preference"],
            row["overall_avg"], row["term1_avg"], row["term2_avg"], row["trend_slope"],
            row["math_fa1"], row["math_sa1"], row["math_fa2"], row["math_sa2"],
            row["science_fa1"], row["science_sa1"], row["science_fa2"], row["science_sa2"],
            row["english_fa1"], row["english_sa1"], row["english_fa2"], row["english_sa2"],
            row["social_fa1"], row["social_sa1"], row["social_fa2"], row["social_sa2"],
            row["hindi_fa1"], row["hindi_sa1"], row["hindi_fa2"], row["hindi_sa2"],
            eval_res["risk_level"], eval_res["risk_score"], eval_res["support_needed"],
            json.dumps({"en": eval_res["reasons_en"], "hi": eval_res["reasons_hi"]}),
            json.dumps({"en": eval_res["strengths_en"], "hi": eval_res["strengths_hi"]}),
            json.dumps(eval_res["weak_subjects"]),
            row.get("archetype", "General")
        ))

    conn.commit()
    conn.close()
    return stats

def get_all_students(risk_filter=None, grade_filter=None, search=None, teacher_id=None, ld_filter=None):
    """Retrieve filtered student records. If teacher_id specified, restricts to that teacher's 100 students."""
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM students WHERE 1=1"
    params = []

    if teacher_id and teacher_id.lower() != "all":
        query += " AND teacher_id = ?"
        params.append(teacher_id)

    if risk_filter and risk_filter.upper() != "ALL":
        query += " AND risk_level = ?"
        params.append(risk_filter.upper())

    if ld_filter and ld_filter.upper() not in ("ALL", ""):
        if ld_filter.upper() == "SECTIONED":
            query += " AND ld_screening_status IS NOT NULL AND ld_screening_status != 'None'"
        else:
            query += " AND ld_screening_status = ?"
            params.append(ld_filter)

    if grade_filter and grade_filter != "ALL":
        query += " AND (grade = ? OR grade = ?)"
        params.extend([grade_filter, f"Class {grade_filter}"])

    if search:
        query += " AND (name LIKE ? OR student_id LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    query += " ORDER BY risk_score DESC, overall_avg ASC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    students = [dict(r) for r in rows]
    conn.close()
    return students

def get_student_by_id(student_id):
    """Retrieve full record for a single student."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_class_analytics(teacher_id=None):
    """Compute aggregate analytics for a teacher (100 students) or entire school."""
    conn = get_connection()
    cursor = conn.cursor()

    base_where = " WHERE 1=1"
    params = []
    if teacher_id and teacher_id.lower() != "all":
        base_where += " AND teacher_id = ?"
        params.append(teacher_id)

    cursor.execute(f"SELECT COUNT(*) FROM students {base_where}", params)
    total = cursor.fetchone()[0] or 0

    cursor.execute(f"SELECT COUNT(*) FROM students {base_where} AND risk_level = 'HIGH'", params)
    high_count = cursor.fetchone()[0] or 0

    cursor.execute(f"SELECT COUNT(*) FROM students {base_where} AND risk_level = 'MODERATE'", params)
    moderate_count = cursor.fetchone()[0] or 0

    cursor.execute(f"SELECT COUNT(*) FROM students {base_where} AND risk_level = 'LOW'", params)
    low_count = cursor.fetchone()[0] or 0

    cursor.execute(f"SELECT AVG(attendance_rate), AVG(overall_avg), AVG(assignment_completion_rate) FROM students {base_where}", params)
    avg_att, avg_score, avg_assign = cursor.fetchone()

    subject_avgs = {}
    for sub in ["math", "science", "english", "social", "hindi"]:
        cursor.execute(f"SELECT AVG({sub}_sa2) FROM students {base_where}", params)
        res = cursor.fetchone()[0]
        subject_avgs[sub] = round(res or 0, 1)

    subject_struggles = {}
    for sub in ["math", "science", "english", "social", "hindi"]:
        cursor.execute(f"SELECT COUNT(*) FROM students {base_where} AND {sub}_sa2 < 40", params)
        subject_struggles[sub] = cursor.fetchone()[0] or 0

    conn.close()

    return {
        "total_students": total,
        "high_risk_count": high_count,
        "moderate_risk_count": moderate_count,
        "on_track_count": low_count,
        "support_needed_total": high_count + moderate_count,
        "avg_attendance": round(avg_att or 0, 1),
        "avg_score": round(avg_score or 0, 1),
        "avg_assignment_rate": round(avg_assign or 0, 1),
        "subject_averages": subject_avgs,
        "subject_struggles": subject_struggles
    }

def get_principal_analytics():
    """
    Computes overall school analytics for Principal.
    Provides teacher performance comparison across Teacher 1, 2, and 3.
    PRIVACY GUARANTEE: Does NOT query or expose teacher-parent private chats.
    """
    school_stats = get_class_analytics(teacher_id=None)

    # Compute comparative metrics for each of the 3 teachers
    teachers = [
        {"id": "teacher1", "name": "Mrs. Ananya Sharma", "grade": "Class 7"},
        {"id": "teacher2", "name": "Mr. Vikram Iyer", "grade": "Class 8"},
        {"id": "teacher3", "name": "Ms. Pooja Verma", "grade": "Class 9"}
    ]

    teacher_metrics = []
    for t in teachers:
        t_stats = get_class_analytics(teacher_id=t["id"])
        t_stats["teacher_id"] = t["id"]
        t_stats["teacher_name"] = t["name"]
        t_stats["grade"] = t["grade"]
        teacher_metrics.append(t_stats)

    return {
        "school_stats": school_stats,
        "teacher_metrics": teacher_metrics
    }

def get_user_by_username(username):
    """Retrieve user authentication record."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def save_remedial_plan_db(student_id, plan_data, teacher_notes="", buddy="", completed_milestones=None, progress_pct=0, post_remedial_score=None):
    """Persist generated remedial plan and RTI milestone tracking."""
    conn = get_connection()
    cursor = conn.cursor()
    milestones_str = json.dumps(completed_milestones or [])
    cursor.execute("""
        INSERT INTO remedial_plans (
            student_id, plan_json, teacher_notes, assigned_buddy,
            completed_milestones, progress_pct, post_remedial_score
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(student_id) DO UPDATE SET
            plan_json=excluded.plan_json,
            teacher_notes=excluded.teacher_notes,
            assigned_buddy=excluded.assigned_buddy,
            completed_milestones=excluded.completed_milestones,
            progress_pct=excluded.progress_pct,
            post_remedial_score=excluded.post_remedial_score,
            updated_at=CURRENT_TIMESTAMP
    """, (student_id, json.dumps(plan_data), teacher_notes, buddy, milestones_str, int(progress_pct), post_remedial_score))
    conn.commit()
    conn.close()

def get_remedial_plan_db(student_id):
    """Fetch saved plan and RTI progress for student."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM remedial_plans WHERE student_id = ?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    data = dict(row)
    data["plan_json"] = json.loads(data["plan_json"])
    try:
        data["completed_milestones"] = json.loads(data.get("completed_milestones") or "[]")
    except Exception:
        data["completed_milestones"] = []
    return data

# ---------------- Student 30-Marks Test Persistence ----------------

def save_test_attempt_db(student_id, test_result):
    """
    Saves student test attempt (30 marks) and updates latest subject marks in students table.
    """
    conn = get_connection()
    cursor = conn.cursor()

    sub_name = test_result["subject_name"]
    sub_key = test_result["subject_key"]
    total_score = test_result["total_score"]
    pct = test_result["percentage"]
    mcq_sc = test_result["mcq_score"]
    w_sc = test_result["written_score"]
    badge = test_result["badge"]
    details_str = json.dumps(test_result)

    cursor.execute("""
        INSERT INTO student_test_attempts (
            student_id, subject, subject_key, total_score, max_score, percentage,
            mcq_score, written_score, badge, results_json
        ) VALUES (?, ?, ?, ?, 30, ?, ?, ?, ?, ?)
    """, (student_id, sub_name, sub_key, total_score, pct, mcq_sc, w_sc, badge, details_str))

    # Also update student's subject marks in students table
    # Convert 30 marks to 100 percentage
    norm_score = round((total_score / 30.0) * 100.0, 1)
    if sub_key in ["math", "science", "english", "social", "hindi"]:
        cursor.execute(f"""
            UPDATE students
            SET {sub_key}_sa2 = ?, updated_at = CURRENT_TIMESTAMP
            WHERE student_id = ?
        """, (norm_score, student_id))

        # Re-fetch and re-assess risk
        cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        updated_student = dict(cursor.fetchone())
        eval_res = predict_student_risk(updated_student)

        cursor.execute("""
            UPDATE students
            SET risk_level = ?, risk_score = ?, support_needed = ?
            WHERE student_id = ?
        """, (eval_res["risk_level"], eval_res["risk_score"], eval_res["support_needed"], student_id))

    conn.commit()
    conn.close()

def get_student_test_attempts(student_id):
    """Retrieve test attempt history for a student."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM student_test_attempts
        WHERE student_id = ?
        ORDER BY created_at DESC
    """, (student_id,))
    rows = cursor.fetchall()
    attempts = [dict(r) for r in rows]
    conn.close()
    return attempts

# ---------------- Teacher-Parent Messaging / Query System ----------------
# PRIVACY POLICY: Strictly restricted between Teacher and Parent. Principal has NO access.

def send_teacher_parent_message(student_id, teacher_id, parent_username, sender_role, sender_name, subject, message):
    """Send a query from Parent to Teacher, or a note from Teacher to Parent."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO teacher_parent_messages (
            student_id, teacher_id, parent_username, sender_role, sender_name, subject, message, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, 'Open')
    """, (student_id, teacher_id, parent_username, sender_role, sender_name, subject, message))
    conn.commit()
    conn.close()

def reply_teacher_parent_message(message_id, reply_text):
    """Teacher responds to a parent's query."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE teacher_parent_messages
        SET reply = ?, status = 'Replied', updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (reply_text, message_id))
    conn.commit()
    conn.close()

def get_messages_for_parent(student_id):
    """Fetch communication thread for a specific parent/child."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM teacher_parent_messages
        WHERE student_id = ?
        ORDER BY created_at DESC
    """, (student_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_messages_for_teacher(teacher_id):
    """Fetch all queries sent to a specific teacher across their 100 students."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.*, s.name as student_name, s.grade, s.section
        FROM teacher_parent_messages m
        JOIN students s ON m.student_id = s.student_id
        WHERE m.teacher_id = ?
        ORDER BY m.created_at DESC
    """, (teacher_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# ---------------- Question Papers & Answer Sheets System ----------------

def get_standard_15q_rubric():
    """
    Standardized CBSE 15-question sequence:
    - Q1 to Q5: 1 mark each (VSA / Objective) = 5 Marks
    - Q6 to Q10: 2 marks each (Short Answer) = 10 Marks
    - Q11 to Q13: 5 marks each (Long Answer) = 15 Marks
    - Q14 to Q15: 10 marks each (Extended / Essay) = 20 Marks
    Total: 15 questions, 50 Marks
    """
    seq = []
    for q in range(1, 6):
        seq.append({"q": q, "max": 1.0, "type": "VSA (1M)"})
    for q in range(6, 11):
        seq.append({"q": q, "max": 2.0, "type": "Short Answer (2M)"})
    for q in range(11, 14):
        seq.append({"q": q, "max": 5.0, "type": "Long Answer (5M)"})
    for q in range(14, 16):
        seq.append({"q": q, "max": 10.0, "type": "Essay / Extended (10M)"})
    return seq

def get_max_marks_for_q(q):
    """Return maximum marks for question number according to standard 15Q rubric."""
    try:
        q_num = int(q)
    except (ValueError, TypeError):
        return 1.0
    if q_num <= 5: return 1.0
    if q_num <= 10: return 2.0
    if q_num <= 13: return 5.0
    if q_num <= 15: return 10.0
    return 1.0

def seed_sample_question_papers(cursor):
    """Seed demo CBSE-style question papers with standard 15-question sequence (50 Marks)."""
    q_seq_json = json.dumps(get_standard_15q_rubric())
    papers = [
        (
            "Half Yearly Examination (2026-27) - Mathematics",
            "Mathematics",
            "Class 7",
            "Half Yearly Examination (2026-2027)",
            50,
            15,
            None,
            q_seq_json,
            "teacher1"
        ),
        (
            "Annual Examination (2026-27) - Science",
            "Science",
            "Class 8",
            "Annual Examination (2026-2027)",
            50,
            15,
            None,
            q_seq_json,
            "teacher2"
        ),
        (
            "Mid-Term Examination (2026-27) - English",
            "English",
            "Class 9",
            "Mid-Term Examination (2026-2027)",
            50,
            15,
            None,
            q_seq_json,
            "teacher3"
        )
    ]

    for title, sub, gr, exam, tot, num_q, f_path, q_seq, t_id in papers:
        cursor.execute("""
            INSERT INTO question_papers (
                title, subject, grade, exam_name, total_marks, total_questions, file_path, questions_sequence_json, teacher_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (title, sub, gr, exam, tot, num_q, f_path, q_seq, t_id))

def seed_sample_answer_sheets(cursor):
    """Seed demo front-page answer sheets with 1-to-15 marks sequences and teacher remarks."""
    # Generate Question 1-15 marks sequence (50 Marks Total)
    # Q1-Q5: 1M each, Q6-Q10: 2M each, Q11-Q13: 5M each, Q14-Q15: 10M each
    q_marks_aarav = {
        "1": 1.0, "2": 1.0, "3": 0.5, "4": 1.0, "5": 0.5,
        "6": 1.5, "7": 2.0, "8": 1.0, "9": 1.5, "10": 2.0,
        "11": 3.5, "12": 4.5, "13": 3.0,
        "14": 7.5, "15": 8.5
    }
    total_aarav = sum(q_marks_aarav.values())

    q_marks_diya = {
        "1": 1.0, "2": 1.0, "3": 1.0, "4": 1.0, "5": 0.5,
        "6": 2.0, "7": 1.5, "8": 2.0, "9": 2.0, "10": 1.5,
        "11": 4.5, "12": 5.0, "13": 4.0,
        "14": 9.0, "15": 8.5
    }
    total_diya = sum(q_marks_diya.values())

    sheets = [
        (
            "SH-2026-001",
            1,
            "Mathematics",
            "Half Yearly Examination (Session 2026-2027)",
            "2026001",
            "English",
            "/static/uploads/answer_sheets/sample_cbse_front_sheet.png",
            json.dumps(q_marks_aarav),
            total_aarav,
            50,
            "teacher1",
            "Questions 3, 5, 8, 11, 14: Struggles with multi-step fractional word problems and long essay derivations. Noticeable reading fatigue in Section D (Q14-15).",
            "Questions 1, 2, 4, 6, 7, 10, 12: Clear improvement in geometry calculations and neat step layout in 1M and 2M questions.",
            "Aarav is persistent and works diligently. Needs visual fraction tiles and 10 minutes reading buffer for Section D long answers.",
            "Mrs. Ananya Sharma"
        ),
        (
            "SH-2026-101",
            2,
            "Science",
            "Annual Examination (Session 2026-2027)",
            "2026101",
            "English",
            "/static/uploads/answer_sheets/sample_cbse_front_sheet.png",
            json.dumps(q_marks_diya),
            total_diya,
            50,
            "teacher2",
            "Questions 5, 7, 13: Minor confusion in multi-step chemical formula balancing and extended reasoning.",
            "Questions 1-4, 6, 8-12, 14-15: Exceptional biological diagram labeling and comprehensive conceptual explanations in 10-mark questions.",
            "Diya demonstrates high attention to detail. Excellent mastery of Section C and D long responses.",
            "Mr. Vikram Iyer"
        )
    ]

    for s_id, p_id, sub, exam, roll, med, img_url, q_json, tot_obt, tot_max, t_id, weak, imp, rem, ex_name in sheets:
        cursor.execute("""
            INSERT INTO student_answer_sheets (
                student_id, question_paper_id, subject, exam_name, roll_no, medium,
                sheet_image_url, question_marks_json, total_marks_obtained, total_max_marks,
                teacher_id, teacher_weaknesses, teacher_improvements, teacher_general_remarks, examiner_name
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (s_id, p_id, sub, exam, roll, med, img_url, q_json, tot_obt, tot_max, t_id, weak, imp, rem, ex_name))

        # Also mirror the teacher remarks to the student record
        cursor.execute("""
            UPDATE students
            SET teacher_weaknesses = ?, teacher_improvements = ?, teacher_remarks = ?
            WHERE student_id = ?
        """, (weak, imp, rem, s_id))

def create_question_paper(title, subject, grade, exam_name, total_marks, total_questions, file_path, questions_sequence, teacher_id):
    """Save newly uploaded/created Question Paper."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO question_papers (
            title, subject, grade, exam_name, total_marks, total_questions, file_path, questions_sequence_json, teacher_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        title, subject, grade, exam_name, total_marks, total_questions,
        file_path, json.dumps(questions_sequence), teacher_id
    ))
    paper_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return paper_id

def get_question_papers(teacher_id=None):
    """Retrieve question papers."""
    conn = get_connection()
    cursor = conn.cursor()
    if teacher_id and teacher_id.lower() != "all":
        cursor.execute("SELECT * FROM question_papers WHERE teacher_id = ? ORDER BY created_at DESC", (teacher_id,))
    else:
        cursor.execute("SELECT * FROM question_papers ORDER BY created_at DESC")
    rows = cursor.fetchall()
    papers = [dict(r) for r in rows]
    for p in papers:
        try:
            p["questions_sequence"] = json.loads(p.get("questions_sequence_json") or "[]")
        except Exception:
            p["questions_sequence"] = []
    conn.close()
    return papers

def get_question_paper_by_id(paper_id):
    """Retrieve single question paper."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM question_papers WHERE id = ?", (paper_id,))
    row = cursor.fetchone()
    conn.close()
    if not row: return None
    p = dict(row)
    try:
        p["questions_sequence"] = json.loads(p.get("questions_sequence_json") or "[]")
    except Exception:
        p["questions_sequence"] = []
    return p

def save_student_answer_sheet(student_id, question_paper_id, subject, exam_name, roll_no, medium,
                              sheet_image_url, question_marks_dict, total_marks_obtained, total_max_marks,
                              teacher_id, teacher_weaknesses, teacher_improvements, teacher_general_remarks, examiner_name):
    """Save student answer sheet front page marks tabulation and teacher remarks."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO student_answer_sheets (
            student_id, question_paper_id, subject, exam_name, roll_no, medium,
            sheet_image_url, question_marks_json, total_marks_obtained, total_max_marks,
            teacher_id, teacher_weaknesses, teacher_improvements, teacher_general_remarks, examiner_name
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        student_id, question_paper_id, subject, exam_name, roll_no, medium,
        sheet_image_url, json.dumps(question_marks_dict), total_marks_obtained, total_max_marks,
        teacher_id, teacher_weaknesses, teacher_improvements, teacher_general_remarks, examiner_name
    ))
    sheet_id = cursor.lastrowid

    # Update students profile remarks
    cursor.execute("""
        UPDATE students
        SET teacher_weaknesses = ?, teacher_improvements = ?, teacher_remarks = ?
        WHERE student_id = ?
    """, (teacher_weaknesses, teacher_improvements, teacher_general_remarks, student_id))

    conn.commit()
    conn.close()
    return sheet_id

def normalize_question_marks(raw):
    """Normalize question marks dict so keys work with '1', 'q1', and int 1."""
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except Exception:
            raw = {}
    if not isinstance(raw, dict):
        raw = {}

    norm = {}
    for k, v in raw.items():
        try:
            val = float(v)
        except (ValueError, TypeError):
            val = 0.0
        clean = str(k).lower().replace("q", "").strip()
        norm[clean] = val
        norm[f"q{clean}"] = val
        if clean.isdigit():
            norm[int(clean)] = val

    # If empty, populate default realistic marks sequence for 15 questions (50 Marks Total)
    if not norm:
        for q in range(1, 6):
            norm[str(q)] = 1.0
            norm[f"q{q}"] = 1.0
            norm[q] = 1.0
        for q in range(6, 11):
            norm[str(q)] = 1.5
            norm[f"q{q}"] = 1.5
            norm[q] = 1.5
        for q in range(11, 14):
            norm[str(q)] = 4.0
            norm[f"q{q}"] = 4.0
            norm[q] = 4.0
        for q in range(14, 16):
            norm[str(q)] = 8.5
            norm[f"q{q}"] = 8.5
            norm[q] = 8.5

    return norm

def get_student_answer_sheets(student_id=None, teacher_id=None):
    """Fetch answer sheets list."""
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT a.*, s.name as student_name, s.grade, s.section
        FROM student_answer_sheets a
        JOIN students s ON a.student_id = s.student_id
        WHERE 1=1
    """
    params = []
    if student_id:
        query += " AND a.student_id = ?"
        params.append(student_id)
    if teacher_id and teacher_id.lower() != "all":
        query += " AND a.teacher_id = ?"
        params.append(teacher_id)

    query += " ORDER BY a.created_at DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    sheets = [dict(r) for r in rows]
    for s in sheets:
        s["question_marks"] = normalize_question_marks(s.get("question_marks_json"))
    conn.close()
    return sheets

def get_answer_sheet_by_id(sheet_id):
    """Fetch single answer sheet with student info."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.*, s.name as student_name, s.grade, s.section, s.gender
        FROM student_answer_sheets a
        JOIN students s ON a.student_id = s.student_id
        WHERE a.id = ?
    """, (sheet_id,))
    row = cursor.fetchone()
    conn.close()
    if not row: return None
    sheet = dict(row)
    sheet["question_marks"] = normalize_question_marks(sheet.get("question_marks_json"))
    return sheet

def update_student_teacher_remarks(student_id, weaknesses, improvements, remarks):
    """Update qualitative teacher remarks for a student directly."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE students
        SET teacher_weaknesses = ?, teacher_improvements = ?, teacher_remarks = ?
        WHERE student_id = ?
    """, (weaknesses, improvements, remarks, student_id))
    conn.commit()
    conn.close()


# ---------------- Learning Disability Sectioning & School Counselor Layer ----------------

LD_CATEGORIES = [
    "Dyslexia / Visual Reading",
    "Dyscalculia / Numeracy",
    "Dysgraphia / Written Expression",
    "Attention & Executive Pacing",
]

LD_STATUSES = [
    "Confirmed Support Profile",
    "Possibility / Early Screening",
    "Monitoring",
]

COUNSELOR_PRIORITIES = [
    "Priority",
    "Monitoring",
    "Not Priority",
]

def backfill_counselor_priorities(cursor):
    """Initialize counselor_priority on existing databases only when none have been triaged yet."""
    cursor.execute("""
        SELECT COUNT(*) FROM students
        WHERE counselor_priority IN ('Priority', 'Monitoring')
    """)
    if cursor.fetchone()[0] > 0:
        return

    cursor.execute("""
        UPDATE students
        SET counselor_priority = CASE
            WHEN ld_screening_status = 'Confirmed Support Profile' THEN 'Priority'
            WHEN ld_screening_status IN ('Possibility / Early Screening', 'Monitoring') THEN 'Monitoring'
            ELSE 'Not Priority'
        END
    """)
    cursor.execute("""
        UPDATE students
        SET counselor_priority = 'Priority'
        WHERE student_id IN ('SH-2026-001', 'SH-2026-201')
    """)
    cursor.execute("""
        UPDATE students
        SET counselor_priority = 'Monitoring'
        WHERE student_id = 'SH-2026-101'
    """)

def ensure_ld_profiles_seeded(cursor):
    """Section/tag a representative subset of existing 300 students with LD or Screening Possibility profiles."""
    cursor.execute("""
        SELECT COUNT(*) FROM students
        WHERE ld_screening_status IS NOT NULL AND ld_screening_status != 'None' AND ld_screening_status != ''
    """)
    if cursor.fetchone()[0] > 0:
        return

    showcase_profiles = [
        (
            "SH-2026-001",
            "Possibility / Early Screening",
            "Dyslexia / Visual Reading",
            "Slow word-problem decoding under timed conditions and occasional symbol swaps in math, paired with strong oral reasoning. Recommended color-chunked reading, CRA math visuals, and extra time.",
            1,
        ),
        (
            "SH-2026-101",
            "Monitoring",
            "Attention & Executive Pacing",
            "Good conceptual understanding; occasionally skips second part of long multi-step questions when pacing speeds up. Recommended 10-minute micro-sprints and step checklists.",
            0,
        ),
        (
            "SH-2026-201",
            "Confirmed Support Profile",
            "Dyscalculia / Numeracy",
            "Benefits from visual balance boxes, fraction strips, and squared-grid column alignment for multi-step problems. Strong classroom curiosity and science practical participation.",
            1,
        ),
    ]

    for sid, status, cat, notes, referred in showcase_profiles:
        cursor.execute("""
            UPDATE students
            SET ld_screening_status = ?, ld_category = ?, ld_notes = ?, counselor_referred = ?
            WHERE student_id = ?
        """, (status, cat, notes, referred, sid))

    # Select ~12 students per teacher (36 additional) prioritizing Reading/Language Barrier, slow reading speed, or HIGH support
    category_notes = {
        "Dyslexia / Visual Reading": "Possible letter/word crowding during timed papers. Responds well to finger-tracking, larger font spacing, and read-aloud audio.",
        "Dyscalculia / Numeracy": "Shows difficulty aligning place-value columns and unpacking multi-step equations without concrete visual blocks.",
        "Dysgraphia / Written Expression": "Verbal answers are clear and accurate, while written formatting under time pressure leads to skipped steps.",
        "Attention & Executive Pacing": "Understanding improves markedly when tasks are broken into 3 small sub-goals with calm 2-minute check-ins.",
    }

    for teacher_id in ("teacher1", "teacher2", "teacher3"):
        cursor.execute("""
            SELECT student_id FROM students
            WHERE teacher_id = ?
              AND student_id NOT IN ('SH-2026-001', 'SH-2026-101', 'SH-2026-201')
            ORDER BY
                CASE WHEN archetype = 'Reading/Language Barrier' THEN 0 ELSE 1 END,
                CASE WHEN risk_level = 'HIGH' THEN 0 WHEN risk_level = 'MODERATE' THEN 1 ELSE 2 END,
                reading_speed_wpm ASC
            LIMIT 12
        """, (teacher_id,))
        rows = cursor.fetchall()
        for idx, r in enumerate(rows):
            cat = LD_CATEGORIES[idx % len(LD_CATEGORIES)]
            status = "Confirmed Support Profile" if idx < 4 else ("Possibility / Early Screening" if idx < 9 else "Monitoring")
            referred = 1 if idx < 6 else 0
            cursor.execute("""
                UPDATE students
                SET ld_screening_status = ?, ld_category = ?, ld_notes = ?, counselor_referred = ?
                WHERE student_id = ?
            """, (status, cat, category_notes[cat], referred, r[0]))


def ensure_counselor_messages_seeded(cursor):
    """Seed initial multi-role Counselor communications (Student, Parent, Teacher)."""
    cursor.execute("SELECT COUNT(*) FROM counselor_messages")
    if cursor.fetchone()[0] > 0:
        return

    samples = [
        (
            "SH-2026-001", "student", "student1", "Aarav Sharma", "Check-In",
            "Word problems look very crowded in Maths",
            "Ma'am, when a maths question has 4 lines of text, the numbers mix up in my head. What easy trick can I use before tomorrow's test?",
            "Hello Aarav! Try the '3-Color Underline' habit tonight: underline numbers in green, the question mark line in blue, and draw one quick box for what is unknown. You are doing great—visit my Study Techniques section below!",
            "Replied",
        ),
        (
            "SH-2026-001", "parent", "parent1", "Mr. Suresh Sharma", "Appointment Request",
            "Short 15-minute review on Aarav's reading pacing support",
            "Namaste Dr. Deshmukh, Aarav feels much calmer using visual math bars at home. Could we confirm whether he qualifies for CBSE extra-time screening this term?",
            "Namaste Mr. Sharma! Yes, let us meet this Friday at 11:30 AM in the Counselor Room (or online link). I have added 2 simple 10-minute home exercises for Aarav so there is zero stress before his next paper.",
            "Replied",
        ),
        (
            "SH-2026-001", "teacher", "teacher1", "Mrs. Ananya Sharma", "Referral",
            "Early Dyslexia Screening Note for Q9-Q12 Written Steps",
            "Dr. Deshmukh, Aarav solves Q1-Q5 accurately when read aloud, but drops marks on Q9 and Q11 where two-step wording appears. Requesting updated reading-chunk exercises for class.",
            None,
            "Pending",
        ),
    ]

    for row in samples:
        cursor.execute("""
            INSERT INTO counselor_messages (
                student_id, sender_role, sender_username, sender_name,
                request_type, subject, message, reply, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, row)


def ensure_counselor_exercises_seeded(cursor):
    """Seed plain-language, step-by-step study techniques, interactive online labs & verified references."""
    cursor.execute("SELECT COUNT(*) FROM counselor_exercises")
    if cursor.fetchone()[0] > 0:
        return

    exercises = [
        (
            "Finger-Track & Color-Chunk Word Problems",
            "Dyslexia / Visual Reading",
            "Students & Parents at Home",
            "Gentle Starter",
            10,
            "Stop numbers from jumping around in long word problems by breaking sentences into 3 short visual bites.",
            [
                "Read ONLY one short sentence at a time while sliding your finger or a ruler underneath the line.",
                "Circle every number and its unit (like '5 cm' or 'Rs 120') with a green pencil.",
                "Underline the final question line ('Find the...') in blue so your brain knows the exact goal.",
                "Draw one rough box or stick sketch on rough paper before touching any formula.",
            ],
            "Chunk-Read-Draw Method",
            "Parents: sit beside your child for the first question, let them point with a pencil, and praise the sketch before checking the final answer.",
            "Online Mini-Lab + Guide",
            "chunk_highlighter",
            "SH-2026-001",
            "https://www.khanacademy.org/",
            "Khan Academy Interactive Math",
            "Reading Rockets & International Dyslexia Association (IDA)",
            "https://www.readingrockets.org/",
            "Adapted from Structured Literacy explicit step-chunking and finger-guided line tracking strategies.",
            14,
        ),
        (
            "Box-by-Box Balance Grid for Algebra Equations",
            "Dyscalculia / Numeracy",
            "Maths Q6-Q13 Learners",
            "Gentle Starter",
            12,
            "Keep '=' signs and negative numbers from flipping by picturing both sides as two baskets on a balance scale.",
            [
                "Draw a bold vertical line straight down from the '=' sign so Left Side and Right Side never mix.",
                "Put each term inside its own small box before moving anything across the '=' line.",
                "Whenever a box jumps across the middle line, flip its sign sticker (+ becomes -, - becomes +).",
                "Put the final number back into the top line to test whether Left Basket equals Right Basket.",
            ],
            "CRA Visual Balance Boxes",
            "Using two real bowls or colored paper slips for x and numbers makes algebra feel like a game instead of guessing.",
            "Online Mini-Lab + External Sim",
            "algebra_balance",
            "ALL",
            "https://phet.colorado.edu/sims/html/equality-explorer/latest/equality-explorer_en.html",
            "PhET Equality Explorer (CU Boulder)",
            "PhET Interactive Simulations & Understood.org",
            "https://phet.colorado.edu/sims/html/equality-explorer/latest/equality-explorer_en.html",
            "Based on University of Colorado Boulder visual equality balance research and CRA dyscalculia scaffolding.",
            19,
        ),
        (
            "3-Color Highlighter & 1-Line Summary",
            "Dyslexia / Visual Reading",
            "Science, English & Social Science",
            "Gentle Starter",
            10,
            "Remember textbook answers without rereading a whole page five times.",
            [
                "Highlight only keywords (names, dates, key verbs) instead of whole paragraphs.",
                "Cover the book page with your hand and speak the main idea in ONE simple sentence out loud.",
                "Write just 3 bullet words (not full sentences) on an index card or rough margin.",
                "Check the card once right after finishing and once before bedtime.",
            ],
            "Active Color Coding + Say-Back",
            "Keep study cards to 3 bullets max. Short spoken recall builds double the memory of silent rereading.",
            "Online Mini-Lab + Guide",
            "voice_card_builder",
            "ALL",
            "https://dyslexiaida.org/",
            "IDA Structured Literacy Resource",
            "International Dyslexia Association (IDA)",
            "https://dyslexiaida.org/",
            "Informed by IDA Structured Literacy semantics and multi-sensory oral-before-written recall principles.",
            11,
        ),
        (
            "Squared Graph Paper Column Anchor",
            "Dysgraphia / Written Expression",
            "Students Who Lose Place in Steps",
            "Gentle Starter",
            8,
            "Prevent neatness slips, missed carries, and crowded lines in 5-mark and 10-mark answers.",
            [
                "Write one digit per square box when multiplying, dividing, or subtracting decimals.",
                "Leave ONE full empty line after every equation step so eyes can rest easily.",
                "Draw a small check-tick next to every line you already copied from the question paper.",
            ],
            "Spatial Column Anchoring",
            "Even normal grid notebooks at home instantly calm visual overwhelm during maths homework.",
            "Online Mini-Lab + Guide",
            "column_grid",
            "ALL",
            "https://apps.mathlearningcenter.org/number-line",
            "Math Learning Center Number Line App",
            "Understood.org (Dyscalculia & Dysgraphia Organizers)",
            "https://www.understood.org/",
            "Taken from Understood.org spatial graphic-organizer recommendations for column alignment and working-memory relief.",
            9,
        ),
        (
            "10-2 Calm Focus Sprint + 3-Step Checklist",
            "Attention & Executive Pacing",
            "Students Who Rush or Freeze in Tests",
            "Step-Up Practice",
            12,
            "Build steady exam focus without tiredness or rushing past easy questions.",
            [
                "Pick ONLY 3 questions for a 10-minute timer—never open the whole book at once.",
                "Write a small [1] [2] [3] checklist at the top corner of your rough sheet.",
                "Work calmly for 10 minutes, check off what finished, then take a mandatory 2-minute stretch and water break.",
            ],
            "Micro-Sprint Pacing",
            "Never add extra questions during the 2-minute break; predictable rest teaches the brain that finishing work feels safe.",
            "Online Mini-Lab + Guide",
            "focus_timer",
            "SH-2026-001",
            "https://www.understood.org/",
            "Understood.org Executive Study Guide",
            "Understood.org (Chunked Timelines & Wait Time)",
            "https://www.understood.org/",
            "Adapted from Understood.org small-batch pacing and structured break schedules to avoid test fatigue.",
            16,
        ),
        (
            "Voice-First Explain Back (Audio Rehearsal)",
            "All LD & Focus Learners",
            "All Subjects (CBSE Exam Prep)",
            "Gentle Starter",
            10,
            "Turn spoken understanding into clean written exam points using your natural voice strength.",
            [
                "Click 'Read Aloud' on any question or let someone read it smoothly once.",
                "Answer in your own everyday words out loud first—do not worry about textbook grammar yet.",
                "Write down the 3 key words you just spoke as short numbered points (1, 2, 3).",
                "Read your 3 points back once to make sure each point answers part of the question.",
            ],
            "Say-It-Before-You-Write-It",
            "Ask your child to 'teach' you one concept in 60 seconds at dinner—no pen needed until they finish speaking.",
            "Online Mini-Lab + Guide",
            "voice_card_builder",
            "ALL",
            "https://www.readingrockets.org/",
            "Reading Rockets Parent Tips",
            "Reading Rockets & CBSE Inclusion Guidelines",
            "https://www.readingrockets.org/",
            "Grounded in Reading Rockets oral-language scaffolding and assistive text-to-speech research.",
            22,
        ),
        (
            "Online Fraction Bars Visual Explorer",
            "Dyscalculia / Numeracy",
            "Assigned by Counselor for Fraction Q6",
            "Gentle Starter",
            10,
            "Compare 1/2, 2/3, and 3/4 online by dragging color-coded fraction bars side by side.",
            [
                "Click 'Launch External Interactive App' to open the free Fractions tool (no login needed).",
                "Create two equal whole bars and split one into 3 parts and one into 4 parts.",
                "Shade 2/3 and 3/4 and look directly at which colored bar stretches longer.",
            ],
            "Virtual Fraction Strips",
            "Parents can watch children compare 2 fractions visually on screen without memorization pressure.",
            "External Interactive Practice",
            "chunk_highlighter",
            "SH-2026-001",
            "https://apps.mathlearningcenter.org/fractions",
            "Math Learning Center Fractions App",
            "The Math Learning Center (Visual CRA Apps) & PhET Fractions Intro",
            "https://www.mathlearningcenter.org/apps",
            "Free browser-based CRA visual math manipulative library used by educators for conceptual fraction mastery.",
            12,
        ),
    ]

    for ex in exercises:
        (
            title, cat, audience, diff, mins, goal, steps, tech, tip,
            ex_mode, inter_tool, assigned_sid, ext_url, ext_name,
            ref_name, ref_url, ref_summary, count
        ) = ex
        cursor.execute("""
            INSERT INTO counselor_exercises (
                title, target_category, target_audience, difficulty_level,
                duration_mins, simple_goal, step_by_step_json, study_technique,
                home_tip, exercise_mode, interactive_tool, assigned_student_id,
                external_practice_url, external_site_name, reference_source_name,
                reference_url, reference_summary, practice_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            title, cat, audience, diff, mins, goal, json.dumps(steps), tech, tip,
            ex_mode, inter_tool, assigned_sid, ext_url, ext_name,
            ref_name, ref_url, ref_summary, count
        ))


def backfill_counselor_exercise_references(cursor):
    """Ensure existing counselor_exercises rows carry interactive labs & verified reference metadata."""
    enrich_map = {
        "Finger-Track & Color-Chunk Word Problems": (
            "Online Mini-Lab + Guide", "chunk_highlighter", "SH-2026-001",
            "https://www.khanacademy.org/", "Khan Academy Interactive Math",
            "Reading Rockets & International Dyslexia Association (IDA)", "https://www.readingrockets.org/",
            "Adapted from Structured Literacy explicit step-chunking and finger-guided line tracking strategies."
        ),
        "Box-by-Box Balance Grid for Algebra Equations": (
            "Online Mini-Lab + External Sim", "algebra_balance", "ALL",
            "https://phet.colorado.edu/sims/html/equality-explorer/latest/equality-explorer_en.html", "PhET Equality Explorer (CU Boulder)",
            "PhET Interactive Simulations & Understood.org", "https://phet.colorado.edu/sims/html/equality-explorer/latest/equality-explorer_en.html",
            "Based on University of Colorado Boulder visual equality balance research and CRA dyscalculia scaffolding."
        ),
        "3-Color Highlighter & 1-Line Summary": (
            "Online Mini-Lab + Guide", "voice_card_builder", "ALL",
            "https://dyslexiaida.org/", "IDA Structured Literacy Resource",
            "International Dyslexia Association (IDA)", "https://dyslexiaida.org/",
            "Informed by IDA Structured Literacy semantics and multi-sensory oral-before-written recall principles."
        ),
        "Squared Graph Paper Column Anchor": (
            "Online Mini-Lab + Guide", "column_grid", "ALL",
            "https://apps.mathlearningcenter.org/number-line", "Math Learning Center Number Line App",
            "Understood.org (Dyscalculia & Dysgraphia Organizers)", "https://www.understood.org/",
            "Taken from Understood.org spatial graphic-organizer recommendations for column alignment and working-memory relief."
        ),
        "10-2 Calm Focus Sprint + 3-Step Checklist": (
            "Online Mini-Lab + Guide", "focus_timer", "SH-2026-001",
            "https://www.understood.org/", "Understood.org Executive Study Guide",
            "Understood.org (Chunked Timelines & Wait Time)", "https://www.understood.org/",
            "Adapted from Understood.org small-batch pacing and structured break schedules to avoid test fatigue."
        ),
        "Voice-First Explain Back (Audio Rehearsal)": (
            "Online Mini-Lab + Guide", "voice_card_builder", "ALL",
            "https://www.readingrockets.org/", "Reading Rockets Parent Tips",
            "Reading Rockets & CBSE Inclusion Guidelines", "https://www.readingrockets.org/",
            "Grounded in Reading Rockets oral-language scaffolding and assistive text-to-speech research."
        ),
    }

    for title, vals in enrich_map.items():
        cursor.execute("""
            UPDATE counselor_exercises
            SET exercise_mode = COALESCE(NULLIF(exercise_mode, ''), ?),
                interactive_tool = CASE WHEN interactive_tool IS NULL OR interactive_tool = '' OR reference_url = '' THEN ? ELSE interactive_tool END,
                assigned_student_id = CASE WHEN reference_url IS NULL OR reference_url = '' THEN ? ELSE assigned_student_id END,
                external_practice_url = COALESCE(NULLIF(external_practice_url, ''), ?),
                external_site_name = COALESCE(NULLIF(external_site_name, ''), ?),
                reference_source_name = COALESCE(NULLIF(reference_source_name, ''), ?),
                reference_url = COALESCE(NULLIF(reference_url, ''), ?),
                reference_summary = COALESCE(NULLIF(reference_summary, ''), ?)
            WHERE title = ? AND (reference_url IS NULL OR reference_url = '')
        """, (*vals, title))

    cursor.execute("SELECT COUNT(*) FROM counselor_exercises WHERE title = 'Online Fraction Bars Visual Explorer'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO counselor_exercises (
                title, target_category, target_audience, difficulty_level,
                duration_mins, simple_goal, step_by_step_json, study_technique,
                home_tip, exercise_mode, interactive_tool, assigned_student_id,
                external_practice_url, external_site_name, reference_source_name,
                reference_url, reference_summary, practice_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "Online Fraction Bars Visual Explorer",
            "Dyscalculia / Numeracy",
            "Assigned by Counselor for Fraction Q6",
            "Gentle Starter",
            10,
            "Compare 1/2, 2/3, and 3/4 online by dragging color-coded fraction bars side by side.",
            json.dumps([
                "Click 'Launch External Interactive App' to open the free Fractions tool (no login needed).",
                "Create two equal whole bars and split one into 3 parts and one into 4 parts.",
                "Shade 2/3 and 3/4 and look directly at which colored bar stretches longer.",
            ]),
            "Virtual Fraction Strips",
            "Parents can watch children compare 2 fractions visually on screen without memorization pressure.",
            "External Interactive Practice",
            "chunk_highlighter",
            "SH-2026-001",
            "https://apps.mathlearningcenter.org/fractions",
            "Math Learning Center Fractions App",
            "The Math Learning Center (Visual CRA Apps) & PhET Fractions Intro",
            "https://www.mathlearningcenter.org/apps",
            "Free browser-based CRA visual math manipulative library used by educators for conceptual fraction mastery.",
            12,
        ))


def get_counselor_exercises(category=None, student_id=None):
    """Fetch study technique guides & online exercises curated/updated by School Counselor."""
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM counselor_exercises WHERE 1=1"
    params = []
    if category and category.lower() not in ("all", ""):
        query += " AND (target_category = ? OR target_category = 'All LD & Focus Learners')"
        params.append(category)

    if student_id:
        query += " AND (assigned_student_id IS NULL OR assigned_student_id = '' OR assigned_student_id = 'ALL' OR assigned_student_id = ?)"
        params.append(student_id)
        query += " ORDER BY CASE WHEN assigned_student_id = ? THEN 0 ELSE 1 END, is_featured DESC, updated_at DESC, id DESC"
        params.append(student_id)
    else:
        query += " ORDER BY is_featured DESC, updated_at DESC, id DESC"

    cursor.execute(query, params)
    rows = []
    for r in cursor.fetchall():
        item = dict(r)
        try:
            item["steps"] = json.loads(item.get("step_by_step_json") or "[]")
        except Exception:
            item["steps"] = []
        rows.append(item)
    conn.close()
    return rows


def create_counselor_exercise(title, target_category, target_audience, difficulty_level,
                              duration_mins, simple_goal, steps_list, study_technique,
                              home_tip, updated_by="Dr. Meera Deshmukh (School Counselor)",
                              exercise_mode="Online Mini-Lab + Guide", interactive_tool="chunk_highlighter",
                              assigned_student_id="ALL", external_practice_url="", external_site_name="",
                              reference_source_name="", reference_url="", reference_summary=""):
    """Publish a new online/guided study exercise with research reference visible across portals."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO counselor_exercises (
            title, target_category, target_audience, difficulty_level,
            duration_mins, simple_goal, step_by_step_json, study_technique,
            home_tip, exercise_mode, interactive_tool, assigned_student_id,
            external_practice_url, external_site_name, reference_source_name,
            reference_url, reference_summary, updated_by, practice_count, is_featured
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 1)
    """, (
        title, target_category, target_audience, difficulty_level,
        int(duration_mins or 10), simple_goal, json.dumps(steps_list),
        study_technique, home_tip, exercise_mode, interactive_tool,
        assigned_student_id or "ALL", external_practice_url, external_site_name,
        reference_source_name, reference_url, reference_summary, updated_by
    ))
    conn.commit()
    ex_id = cursor.lastrowid
    conn.close()
    return ex_id


def increment_exercise_practice(exercise_id):
    """Increment completed practice counter for a counselor exercise."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE counselor_exercises
        SET practice_count = COALESCE(practice_count, 0) + 1
        WHERE id = ?
    """, (exercise_id,))
    conn.commit()
    cursor.execute("SELECT * FROM counselor_exercises WHERE id = ?", (exercise_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    item = dict(row)
    try:
        item["steps"] = json.loads(item.get("step_by_step_json") or "[]")
    except Exception:
        item["steps"] = []
    return item


def get_ld_screened_students(status_filter="ALL", category_filter="ALL", priority_filter="ALL",
                             search=None, teacher_id=None, include_all=False):
    """Retrieve students filtered by LD section, counselor priority/monitoring, category, or search."""
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM students WHERE 1=1"
    params = []

    show_all_cohort = include_all or (priority_filter and priority_filter == "Not Priority")
    if not show_all_cohort:
        query += """
          AND (
              (ld_screening_status IS NOT NULL AND ld_screening_status != 'None' AND ld_screening_status != '')
              OR COALESCE(counselor_priority, 'Not Priority') IN ('Priority', 'Monitoring')
          )
        """

    if teacher_id and teacher_id.lower() != "all":
        query += " AND teacher_id = ?"
        params.append(teacher_id)

    if status_filter and status_filter.upper() != "ALL":
        query += " AND ld_screening_status = ?"
        params.append(status_filter)

    if category_filter and category_filter.upper() != "ALL":
        query += " AND ld_category = ?"
        params.append(category_filter)

    if priority_filter and priority_filter.upper() != "ALL":
        query += " AND COALESCE(counselor_priority, 'Not Priority') = ?"
        params.append(priority_filter)

    if search:
        query += " AND (name LIKE ? OR student_id LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    query += """
        ORDER BY
            CASE WHEN student_id = 'SH-2026-001' THEN 0 ELSE 1 END,
            CASE COALESCE(counselor_priority, 'Not Priority')
                WHEN 'Priority' THEN 0
                WHEN 'Monitoring' THEN 1
                ELSE 2
            END,
            CASE ld_screening_status
                WHEN 'Confirmed Support Profile' THEN 0
                WHEN 'Possibility / Early Screening' THEN 1
                WHEN 'Monitoring' THEN 2
                ELSE 3
            END,
            counselor_referred DESC,
            risk_score DESC
    """
    cursor.execute(query, params)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_ld_section_summary(teacher_id=None):
    """Compute counts of students sectioned for LD / Early Screening and counselor priority levels."""
    conn = get_connection()
    cursor = conn.cursor()

    where_clause = ""
    params = []
    if teacher_id and teacher_id.lower() != "all":
        where_clause = " WHERE teacher_id = ?"
        params.append(teacher_id)

    cursor.execute(f"SELECT COUNT(*) FROM students{where_clause}", params)
    cohort_total = cursor.fetchone()[0]

    cursor.execute(
        f"SELECT ld_screening_status, counselor_referred, COALESCE(counselor_priority, 'Not Priority') AS counselor_priority FROM students{where_clause}",
        params
    )
    rows = cursor.fetchall()
    conn.close()

    confirmed_count = 0
    possibility_count = 0
    monitoring_count = 0
    referred_count = 0
    priority_count = 0
    monitoring_priority_count = 0
    not_priority_count = 0

    for row in rows:
        status = row["ld_screening_status"] or "None"
        if status == "Confirmed Support Profile":
            confirmed_count += 1
        elif status == "Possibility / Early Screening":
            possibility_count += 1
        elif status == "Monitoring":
            monitoring_count += 1
        if status not in ("None", "") and row["counselor_referred"]:
            referred_count += 1

        prio = row["counselor_priority"] or "Not Priority"
        if prio == "Priority":
            priority_count += 1
        elif prio == "Monitoring":
            monitoring_priority_count += 1
        else:
            not_priority_count += 1

    total_sectioned = confirmed_count + possibility_count + monitoring_count
    return {
        "cohort_total": cohort_total,
        "total_sectioned": total_sectioned,
        "confirmed_count": confirmed_count,
        "possibility_count": possibility_count,
        "monitoring_count": monitoring_count,
        "referred_count": referred_count,
        "priority_count": priority_count,
        "monitoring_priority_count": monitoring_priority_count,
        "not_priority_count": not_priority_count,
    }


def set_student_counselor_priority(student_id, priority_level):
    """Mark a student as Priority, Monitoring, or Not Priority for School Counselor triage."""
    valid = set(COUNSELOR_PRIORITIES)
    clean_priority = priority_level if priority_level in valid else "Not Priority"
    conn = get_connection()
    cursor = conn.cursor()
    if clean_priority == "Priority":
        cursor.execute("""
            UPDATE students
            SET counselor_priority = ?, counselor_referred = 1
            WHERE student_id = ?
        """, (clean_priority, student_id))
    else:
        cursor.execute("""
            UPDATE students
            SET counselor_priority = ?
            WHERE student_id = ?
        """, (clean_priority, student_id))
    conn.commit()
    conn.close()
    return clean_priority


def update_student_ld_profile(student_id, ld_screening_status, ld_category, ld_notes,
                              counselor_referred=1, counselor_priority=None):
    """Update a student's LD screening section status, category, priority, counselor notes, and referral flag."""
    conn = get_connection()
    cursor = conn.cursor()
    clean_category = "None" if ld_screening_status in ("None", "") else (ld_category or "Dyslexia / Visual Reading")
    referred_val = 0 if ld_screening_status in ("None", "") else int(bool(counselor_referred))
    if counselor_priority in COUNSELOR_PRIORITIES:
        cursor.execute("""
            UPDATE students
            SET ld_screening_status = ?, ld_category = ?, ld_notes = ?, counselor_referred = ?, counselor_priority = ?
            WHERE student_id = ?
        """, (ld_screening_status or "None", clean_category, ld_notes or "", referred_val, counselor_priority, student_id))
    else:
        cursor.execute("""
            UPDATE students
            SET ld_screening_status = ?, ld_category = ?, ld_notes = ?, counselor_referred = ?
            WHERE student_id = ?
        """, (ld_screening_status or "None", clean_category, ld_notes or "", referred_val, student_id))
    conn.commit()
    conn.close()


def send_counselor_message(student_id, sender_role, sender_username, sender_name,
                           subject, message, request_type="Query"):
    """Submit a Student, Parent, or Teacher message/referral to the School Counselor inbox."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO counselor_messages (
            student_id, sender_role, sender_username, sender_name,
            request_type, subject, message, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, 'Pending')
    """, (
        student_id,
        (sender_role or "parent").lower(),
        sender_username or "user",
        sender_name or "Portal User",
        request_type or "Query",
        subject,
        message,
    ))
    conn.commit()
    msg_id = cursor.lastrowid
    conn.close()
    return msg_id


def reply_counselor_message(message_id, reply_text):
    """Save School Counselor reply to a student, parent, or teacher message."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE counselor_messages
        SET reply = ?, status = 'Replied', updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (reply_text, message_id))
    conn.commit()
    conn.close()


def get_counselor_messages(student_id=None, sender_role=None):
    """Retrieve Counselor inbox threads joined with student metadata."""
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT m.*, s.name AS student_name, s.grade, s.section,
               s.ld_screening_status, s.ld_category
        FROM counselor_messages m
        LEFT JOIN students s ON m.student_id = s.student_id
        WHERE 1=1
    """
    params = []

    if student_id:
        query += " AND m.student_id = ?"
        params.append(student_id)

    if sender_role and sender_role.upper() != "ALL":
        query += " AND LOWER(m.sender_role) = LOWER(?)"
        params.append(sender_role)

    query += """
        ORDER BY
            CASE WHEN m.status = 'Pending' THEN 0 ELSE 1 END,
            m.id DESC
    """
    cursor.execute(query, params)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows



