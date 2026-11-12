# SEHAYAK (सहायक)

**Early-Warning Dyslexia Screening, Counselor Triage & Study Support Platform**

SEHAYAK helps schools detect learning difficulties early, support students with weak question-level marks, and coordinate teachers, school counselors, and parents in one accessible workspace—without stigmatizing labels.

---

## Key Capabilities

- **Early Risk Screening & Explainability:** Hybrid Random Forest + deterministic pedagogical rule engine scoring 300 seeded student profiles (`Low`, `Medium`, `High` tiers) with human-readable factor explanations.
- **School Counselor Triage & Exercises:** Mark students as `Priority`, `Monitoring`, or `Not Priority`; assign interactive online exercises; share curated guidance backed by IDA, Understood.org, and NCERT PRASHAST citations; and handle teacher/parent referrals.
- **Student Study Hub & AI Logic Tutor:** Breaks down low-scoring exam questions into step-by-step solving logic paired with interactive **30-mark CBSE practice tests** (15 MCQs + 5 typed/voice-dictated responses) and a quick-access tabbed layout.
- **Dual Student & Parent AI Chatbots:** Offline real-time Q&A assistants helping students with study strategies and parents with home scaffolding and counselor coordination.
- **CBSE Answer-Sheet Grading (Q1–Q30):** Upload scanned answer sheets, record per-question marks, and publish teacher weakness/improvement remarks directly to student and parent views.
- **Dyslexia Accessibility Suite:** *Lexend* & *OpenDyslexic* font toggle, interactive reading ruler, Irlen color-tint overlays, and adjustable text-to-speech pacing.
- **Privacy Safeguard:** Teacher-parent and counselor consultations are excluded from the Principal overview dashboard.

---

## Multi-Role Demo Credentials

*(One-click quick login buttons are also available on `/login`.)*

| Role | Username | Password | Scope / Notes |
| :--- | :--- | :--- | :--- |
| **Principal** | `principal` | `principal123` | School-wide analytics (all 300 students; private chats excluded) |
| **School Counselor** | `counselor1` | `counselor123` | Priority triage, online exercises, references, counselor inbox |
| **Teacher (Class 7–9)** | `teacher1` / `teacher2` / `teacher3` | `teacher123` | 100-student cohort each, CBSE paper marking, parent queries |
| **Student** | `student1` / `student2` / `student3` | `student123` | Question-level AI Logic Tutor, 30-mark quizzes, Student Chatbot |
| **Parent** | `parent1` / `parent2` / `parent3` | `parent123` | Child progress, remarks, research citations, counselor/teacher chat, Parent Chatbot |

---

## Quick Start

1. **Run the server** from `C:\Narsim`:
   ```bash
   python app.py
   ```
2. **Open in browser:** `http://127.0.0.1:5000`

---

## Automated Tests

Run all unit and route tests:
```bash
python -m unittest discover -s tests -p "test_*.py"
```
*(Verified: **33 tests** passing across authentication, RBAC, ML screening, AI Logic Tutor, counselor priority triage, exercises, and chatbots.)*

---

## Project Layout

```text
app.py          # Flask routes & role-based access control
config.py       # App paths, thresholds & upload configuration
models/         # RandomForest risk model, rule engine & explainability
remedial/       # AI Logic Tutor, test bank, exercises, resources & chatbots
utils/          # SQLite schema & CRUD (db.py), CSV cleaner & cohort seeder
templates/      # Accessible Jinja2 role templates
static/         # Stylesheets, accessibility JS & uploaded answer sheets
data/           # SQLite DB (sehayak.db) & serialized risk model
tests/          # Automated unittest suite
```

