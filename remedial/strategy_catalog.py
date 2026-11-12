"""
SEHAYAK (सहायक) - Pedagogical Strategy Catalog
Comprehensive repository of evidence-based remedial interventions
tailored to subject deficits, learning differences (dyslexia), and engagement patterns.
"""

STRATEGY_CATALOG = {
    "multisensory_math": {
        "id": "MS-MTH",
        "title_en": "Multisensory Concrete-Representational-Abstract (CRA) Math",
        "title_hi": "बहु-संवेदी गणित शिक्षण (CRA विधि)",
        "category": "Mathematics",
        "description_en": "Introduce concepts using physical manipulatives (counters, base-10 blocks), transition to visual diagrams (number lines, bar models), and finally to abstract symbols.",
        "description_hi": "पहले ठोस वस्तुओं (ब्लॉक्स, टोकन) से सिखाएं, फिर चित्र एवं रेखा आरेखों से, और अंत में प्रतीकों से हल कराएं।",
        "teacher_actions": [
            "Use color-coded number lines for integer operations.",
            "Deconstruct word problems into pictorial bar models before writing equations.",
            "Provide a formula visual anchor sheet to eliminate working memory strain."
        ],
        "target_gap": "Conceptual difficulty in arithmetic, algebra, or fractions."
    },
    "phonics_reading_dyslexia": {
        "id": "DY-PHN",
        "title_en": "Structured Phonics & Color-Coded Orthographic Support",
        "title_hi": "संरचित ध्वनि-विज्ञान (Phonics) एवं रंग-आधारित पठन सहयोग",
        "category": "Reading / Dyslexia",
        "description_en": "Support decoding difficulties using syllables highlighted in alternating colors, enlarged Lexend font, and synchronized audio read-aloud.",
        "description_hi": "कठिन शब्दों को रंग-बिरंगे अक्षरों में बांटकर पढ़ें, बड़े अक्षरों और टेक्स्ट-टू-स्पीच ध्वनि सहयोग का उपयोग करें।",
        "teacher_actions": [
            "Provide reading material with 1.8x line spacing and left alignment.",
            "Permit oral assessment or speech-to-text for essay questions.",
            "Avoid asking the student to read unfamiliar passages aloud in front of peers."
        ],
        "target_gap": "Reading fatigue, slow decodability, dyslexia-like pacing."
    },
    "peer_tutoring": {
        "id": "PR-TUT",
        "title_en": "Reciprocal Structured Peer Tutoring",
        "title_hi": "सहयोगी सहपाठी शिक्षण (पीयर ट्यूटरिंग)",
        "category": "Social & Collaborative",
        "description_en": "Pair the student with an empathetic, high-confidence peer mentor for 15-minute collaborative review sessions twice weekly.",
        "description_hi": "सप्ताह में दो बार 15 मिनट के लिए छात्र को एक सहयोगी सहपाठी मित्र के साथ मिलकर अभ्यास करने का अवसर दें।",
        "teacher_actions": [
            "Provide structured prompt cards to both peers ('Explain Step 1', 'Check with Hint').",
            "Praise mutual teamwork and celebrate cooperative problem-solving.",
            "Alternate roles so the mentored student also explains concepts they feel confident in."
        ],
        "target_gap": "Classroom hesitation, low participation, social anxiety in asking doubts."
    },
    "spaced_revision": {
        "id": "SP-REV",
        "title_en": "Spaced Repetition & 5-Minute Micro-Drills",
        "title_hi": "अंतरालीय पुनरावृत्ति एवं 5 मिनट के लघु अभ्यास",
        "category": "Memory Retention",
        "description_en": "Distribute practice across Day 1, Day 3, Day 7, and Day 14 using bite-sized flashcards to strengthen long-term memory retrieval without fatigue.",
        "description_hi": "लंबे अभ्यास के बजाय 1, 3, 7 और 14वें दिन 5-5 मिनट के छोटे पुनरावृत्ति सत्र आयोजित करें।",
        "teacher_actions": [
            "Implement a 3-question 'Do Now' micro-quiz at the beginning of each class.",
            "Use Leitner-box flashcards for key vocabulary, formulas, and historical events.",
            "Focus each drill on one single targeted objective."
        ],
        "target_gap": "Exam retention decline, steep term-over-term score drop."
    },
    "visual_graphic_organizers": {
        "id": "VS-ORG",
        "title_en": "Visual Concept Maps & Dual-Coding Organizers",
        "title_hi": "दृश्य संकल्पना मानचित्र (Concept Maps) एवं फ्लोचार्ट",
        "category": "Science & Social Science",
        "description_en": "Replace dense blocks of text with branch diagrams, cause-effect fishbone charts, and illustrated timelines to improve comprehension.",
        "description_hi": "लंबे पैराग्राफ के स्थान पर शाखा आरेख, फ्लोचार्ट और सचित्र समय-सारणी का उपयोग करें।",
        "teacher_actions": [
            "Provide pre-structured fill-in-the-blank mind maps before starting new chapters.",
            "Encourage students to draw diagrams or sketch notes alongside definitions.",
            "Highlight core keywords with high-contrast pastel borders."
        ],
        "target_gap": "Information overload in text-heavy subjects (Science, Social Studies)."
    },
    "attendance_recovery": {
        "id": "AT-REC",
        "title_en": "Accelerated Catch-Up Modules with Audio Summaries",
        "title_hi": "ऑडियो सारांश के साथ त्वरित भरपाई मॉड्यूल",
        "category": "Attendance & Habit",
        "description_en": "Provide condensed 1-page visual study guides and short 2-minute audio summaries for lectures missed due to absence.",
        "description_hi": "अनुपस्थिति के कारण छूटे पाठों के लिए 1-पृष्ठ के दृश्य सारांश और 2 मिनट के ऑडियो नोट्स उपलब्ध कराएं।",
        "teacher_actions": [
            "Assign a 'Classroom Study Buddy' who shares notes for missed dates.",
            "Schedule a compassionate 10-minute weekly check-in with the student.",
            "Collaborate with parents to identify and resolve transport or health hurdles."
        ],
        "target_gap": "Frequent absenteeism (<75% attendance) leading to cumulative concept gaps."
    }
}
