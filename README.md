# 🌱 SEHAYAK (सहायक)
### Slow Learner Identification & Remedial Support System
**Ministry of Education &bull; Problem Statement ID: PSB152**  
*Theme: Smart Education | Category: Software*

> **Guiding Principle**: *"Flags are for early support and multisensory scaffolding, never for persistent diagnostic labeling. Every child learns at their own pace when taught through accessible modalities."*

---

## 📖 1. Overview & Multi-Role Architecture

**SEHAYAK** is an intelligent, ethical, and universally accessible educational web platform designed with 4 distinct demographics and portals:

1. **🎓 Principal (School Leadership)**: Oversees institutional health across all 300 students and compares educator cohort progress across 3 teachers. In compliance with student privacy guidelines, **the Principal has no access to private teacher-parent consultation chats**.
2. **👩‍🏫 3 Classroom Teachers (100 Students Each)**:
   - **Teacher 1 (Mrs. Ananya Sharma)**: Leads Class 7 (100 students, `SH-2026-001` to `SH-2026-100`).
   - **Teacher 2 (Mr. Vikram Iyer)**: Leads Class 8 (100 students, `SH-2026-101` to `SH-2026-200`).
   - **Teacher 3 (Ms. Pooja Verma)**: Leads Class 9 (100 students, `SH-2026-201` to `SH-2026-300`).
   - Features individual 100-student rosters, 4-Quadrant diagnostic maps, RTI milestone tracking, CBSE Answer Sheet grading (1-30 questions sequence), and a **Parent Query & Communication Center**.
3. **🎒 Students**: Choose between basic CBSE subjects (**Mathematics, Science, Social Science, English, Hindi**) and take **30-Marks Comprehensive Assessments** (15 MCQs + 5 Conceptual Typed/Written questions with Speech-to-Text dictation).
4. **🏡 Parents**: Review child's progress, celebrate positive strengths, monitor recent 30-mark assessment scores, inspect evaluated CBSE answer sheet front-covers with teacher remarks, and **directly chat / submit queries to their child's assigned teacher**.

---

## ✨ 2. Newly Added Core Features

### 🌐 A. Public Feature & Demographic Home Page (`/`)
- **Demographic Scaffolding**: Richly showcases how SEHAYAK serves all 4 demographics: Teachers, Students, Parents, and Principals.
- **Role Login Gateways**: Direct 1-click login gateway buttons for Teacher, Student, Parent, and Principal portals.
- **Context-Aware Header**: Recognizes active signed-in users and offers a 1-click shortcut to their role dashboard.

### 📄 B. CBSE Answer Sheet Front-Cover Upload & 1-to-30 Rubric
- **Physical Answer Sheet Twin**: Faithfully models the official CBSE answer sheet front-page format (Central Model Senior Secondary School format):
  - Candidate roll number grid boxes in figures and words.
  - Exam session, subject, medium (English/Hindi), and serial number.
  - **Two-Column Question Sequence (Q1 to Q30)**:
    - Left Column: Questions 1 to 18 (MCQs / Very Short Answers).
    - Right Column: Questions 19 to 30 (Short / Long Analytical Answers).
  - **Live Auto-Tabulation**: Calculates total marks obtained in real-time in figures and words out of 50 marks.
  - Examiner and Invigilator signatures.
  - Optional scanned answer sheet image upload with toggleable full-resolution preview.
- **Curriculum Question Papers Repository**: Upload and catalog question papers with 30-question sequence rubrics.

### 📝 C. Teacher Diagnostic Remarks: Weaknesses & Improvements
- **Observed Weaknesses & Learning Gaps**: Teacher documents question numbers (e.g. Q4, Q9, Q21), conceptual friction points (e.g. multi-step fractions), and signs of reading fatigue.
- **Observed Improvements & Growth**: Documents areas of mastery, step clarity, formula recall, and resilience.
- **Remedial Guidance**: Prescribes specific multisensory interventions (e.g. CRA fraction tiles, reading ruler, paired peer tutoring).
- **Stakeholder Transparency**: Remarks are immediately accessible on the **Student Diagnostic Dossier** and the **Parent Progress Portal**.

### 🎒 D. CBSE 30-Marks Assessment Suite (MCQ + Typed/Written)
- **Section A**: 15 Multiple-Choice Questions (1 mark each = 15 marks) with visual hints and audio read-aloud.
- **Section B**: 5 Conceptual Short Typed Responses (3 marks each = 15 marks) with keyword scoring and microphone speech-to-text voice dictation.
- Auto-grading out of 30 marks, instant dyslexia-friendly feedback, growth badges, and continuous assessment tracking.

### 💬 E. Teacher-Parent Consultation & Query Center
- Parents can submit queries about home practice, reading fatigue, or homework scaffolding.
- Teachers reply directly from their dedicated inbox.
- **Privacy Guarantee**: Principal dashboard strictly excludes these communications to preserve family-educator trust.

### 👓 F. Dyslexia & Universal Accessibility Suite (WCAG 2.1 AA/AAA)
- **Interactive Reading Ruler**: Focus guide following cursor/touch to prevent eye fatigue.
- **Irlen Syndrome Color Tint Overlays**: Rose, Aqua, Yellow, Lavender.
- **Specialized Fonts**: Google *Lexend* and *OpenDyslexic*.
- **Pacing & TTS Controls**: User-controlled speech rate (`0.7x`–`1.3x`) and gentle synthesizer audio chimes.

### 🎨 G. Visdeurbel-Inspired Design Language (https://visdeurbel.nl/en/)
- **Warm & Approachable Aesthetic**: Inspired by the famous Utrecht Fish Doorbell (*De Visdeurbel*), replacing sterile bureaucratic edtech with an inviting, tactile, community-first feel.
- **Floating Pill Navbar**: Centered pill bar with soft backdrop blur, pulsing live status dot (`LIVE • PSB152`), and rounded navigational links.
- **Tactile 3D "Doorbell" Push Buttons**: Interactive coral/vibrant action buttons with satisfying bevels, hover lifts, bell wiggle animations (`@keyframes bell-ring`), and active press states.
- **Generous Rounded Cards (`border-radius: 20px–28px`)**: Soft pastel containers with subtle 2px borders, soft drop shadows, and high-contrast Lexend typography.
- **100% WCAG 2.1 AA/AAA Compliance**: Preserves all dyslexia accommodations (reading ruler, Irlen tints, voice pacing, high contrast mode).

---

## 🔑 3. Multi-Role Demo Credentials

The platform is pre-loaded with at least 3 accounts of each role:

| Role | Username | Password | Assigned Cohort / Purpose |
| :--- | :--- | :--- | :--- |
| **🎓 Principal** | `principal` | `principal123` | Institutional Dashboard (All 300 Students, Teacher Comparison, Private Chats Excluded) |
| **👩‍🏫 Teacher 1** | `teacher1` | `teacher123` | Mrs. Ananya Sharma &bull; Class 7 (100 Students: SH-001 to SH-100), Answer Sheets & Parent Queries |
| **👨‍🏫 Teacher 2** | `teacher2` | `teacher123` | Mr. Vikram Iyer &bull; Class 8 (100 Students: SH-101 to SH-200), Answer Sheets & Parent Queries |
| **👩‍🏫 Teacher 3** | `teacher3` | `teacher123` | Ms. Pooja Verma &bull; Class 9 (100 Students: SH-201 to SH-300), Answer Sheets & Parent Queries |
| **🎒 Student 1** | `student1` | `student123` | Aarav Sharma (Class 7-A, Teacher 1) &bull; CBSE 30-Marks Tests & Practice |
| **🎒 Student 2** | `student2` | `student123` | Diya Patel (Class 8-B, Teacher 2) &bull; CBSE 30-Marks Tests & Practice |
| **🎒 Student 3** | `student3` | `student123` | Mohammed Faizan (Class 9-A, Teacher 3) &bull; CBSE 30-Marks Tests & Practice |
| **🏡 Parent 1** | `parent1` | `parent123` | Mr. Suresh Sharma &bull; View Aarav's Front Sheet, Remarks & Chat with Teacher 1 |
| **🏡 Parent 2** | `parent2` | `parent123` | Mrs. Gita Patel &bull; View Diya's Front Sheet, Remarks & Chat with Teacher 2 |
| **🏡 Parent 3** | `parent3` | `parent123` | Mr. Imran Faizan &bull; View Faizan's Front Sheet, Remarks & Chat with Teacher 3 |

*(One-click quick login buttons for all roles are available directly on the login screen).*

---

## 💻 4. Running in Visual Studio Code

### Step 1: Open in VS Code
Open Visual Studio Code, click **File &rarr; Open Folder...**, and select `C:\Narsim`.

### Step 2: Run the Server
Open the terminal (`Ctrl + ~`) and start the application:
```bash
python app.py
```
*(Or press **`F5`** for one-key debugging).*

### Step 3: Access in Browser
Navigate to:
```
http://127.0.0.1:5000
```

---

## 🧪 5. Automated Unit Tests

Run the complete 21-test suite covering all modules:
```bash
python -m unittest discover -s tests -p "test_*.py"
```

All 21 tests execute in ~17 seconds with 100% pass rate.

---

## ⚖️ 6. Ethical Compliance & Privacy Guarantee

1. **Confidentiality of Family Dialogue**: In strict adherence to Ministry of Education ethical standards, teacher-parent communication threads remain strictly private and are withheld from administrative oversight dashboards.
2. **Support Without Labeling**: All assessments and flags are early developmental scaffolding tools, never persistent diagnostic labels.
#   S e h a y a k  
 