"""
SEHAYAK (सहायक) - Student Practice Bank
Bite-sized, zero-anxiety, multisensory practice questions
designed for children with dyslexia and learning differences.
Features visual anchors, clear typography, and encouraging feedback.
"""

PRACTICE_QUESTIONS = [
    {
        "id": "Q-MTH-01",
        "subject": "Mathematics",
        "topic": "Visual Fractions & Parts of Whole",
        "question_en": "Look at a pizza sliced into 4 equal slices. If you and your best friend eat 1 slice each, what fraction of the pizza is eaten?",
        "question_hi": "एक पिज़्ज़ा के 4 बराबर टुकड़े हैं। यदि आप और आपका मित्र 1-1 टुकड़ा खाते हैं, तो पिज़्ज़ा का कितना भाग खाया गया?",
        "icon": "MATH",
        "options_en": ["1/4 (One Quarter)", "2/4 or 1/2 (Half)", "3/4 (Three Quarters)", "4/4 (Whole)"],
        "options_hi": ["1/4 (एक चौथाई)", "2/4 या 1/2 (आधा)", "3/4 (तीन चौथाई)", "4/4 (पूरा)"],
        "correct_index": 1,
        "hint_en": "You ate 1 slice + your friend ate 1 slice = 2 slices out of 4 total!",
        "hint_hi": "आपने 1 टुकड़ा खाया + मित्र ने 1 टुकड़ा खाया = कुल 4 में से 2 टुकड़े!",
        "encouraging_feedback_en": "Spot on! 2 out of 4 is exactly half! You have a brilliant eye for shapes.",
        "encouraging_feedback_hi": "बिल्कुल सही! 4 में से 2 टुकड़े यानी ठीक आधा। आपकी समझ बहुत तेज है!"
    },
    {
        "id": "Q-SCI-01",
        "subject": "Science",
        "topic": "Plant Life & Sunlight",
        "question_en": "Plants act like green solar panels. What do leaves absorb from sunlight to help prepare their food?",
        "question_hi": "पौधे धूप से ऊर्जा लेते हैं। पत्तियाँ भोजन बनाने के लिए सूर्य के प्रकाश से क्या अवशोषित करती हैं?",
        "icon": "SCI",
        "options_en": ["Light Energy", "Rain Drops", "Soil Stones", "Moonlight"],
        "options_hi": ["प्रकाश ऊर्जा (Light Energy)", "बारिश की बूंदें", "मिट्टी के पत्थर", "चांदनी"],
        "correct_index": 0,
        "hint_en": "Think of what gives you bright warmth when standing outside on a sunny afternoon.",
        "hint_hi": "सोचिए कि धूप में खड़े होने पर आपको क्या गर्म ऊर्जा मिलती है?",
        "encouraging_feedback_en": "Fantastic! Leaves have green chlorophyll that captures sunlight energy like a battery!",
        "encouraging_feedback_hi": "शानदार! पत्तियों में क्लोरोफिल होता है जो सूरज की रोशनी से ऊर्जा सोखता है!"
    },
    {
        "id": "Q-ENG-01",
        "subject": "English",
        "topic": "Word Families & Rhyming Sounds",
        "question_en": "Which of these words rhymes with the word 'BRIGHT' and shares the same sound?",
        "question_hi": "अंग्रेजी शब्द 'BRIGHT' (ब्राइट) के साथ कौन सा शब्द मिलती-जुलती ध्वनि (Rhyme) बनाता है?",
        "icon": "ENG",
        "options_en": ["Breeze", "Light", "Cloud", "Shadow"],
        "options_hi": ["Breeze (हवा)", "Light (प्रकाश)", "Cloud (बादल)", "Shadow (छाया)"],
        "correct_index": 1,
        "hint_en": "Listen to the ending: -IGHT. Br-ight, L-ight!",
        "hint_hi": "शब्द के अंत की आवाज़ सुनें: ब्राइट (Br-ight), लाइट (L-ight)।",
        "encouraging_feedback_en": "Super job! Bright and Light both share the -ight sound! Excellent listening ears.",
        "encouraging_feedback_hi": "बहुत खूब! Bright और Light दोनों में एक जैसी लय और ध्वनि है!"
    },
    {
        "id": "Q-HIN-01",
        "subject": "Hindi",
        "topic": "समानार्थी शब्द (Synonyms)",
        "question_en": "What is another friendly Hindi word for 'जल' (Jal / Water)?",
        "question_hi": "'जल' का दूसरा समान अर्थ वाला शब्द कौन सा है?",
        "icon": "HIN",
        "options_en": ["पानी (Paani)", "आग (Aag)", "हवा (Hawa)", "पेड़ (Ped)"],
        "options_hi": ["पानी", "आग", "हवा", "पेड़"],
        "correct_index": 0,
        "hint_en": "The clear liquid that we drink when we are thirsty.",
        "hint_hi": "वह निर्मल पेय जो हम प्यास लगने पर पीते हैं।",
        "encouraging_feedback_en": "Marvelous! 'जल' और 'पानी' दोनों का अर्थ एक ही अमृत तुल्य तरल है!",
        "encouraging_feedback_hi": "अद्भुत! 'जल' और 'पानी' दोनों एक ही अर्थ रखते हैं। शाबाश!"
    },
    {
        "id": "Q-SOC-01",
        "subject": "Social Science",
        "topic": "Map Reading & Cardinal Directions",
        "question_en": "When you look at a wall map facing forward, which direction is always at the top of the map?",
        "question_hi": "जब आप दीवार पर टंगे नक्शे (मानचित्र) को देखते हैं, तो सबसे ऊपर कौन सी दिशा होती है?",
        "icon": "SST",
        "options_en": ["North (उत्तर)", "South (दक्षिण)", "East (पूर्व)", "West (पश्चिम)"],
        "options_hi": ["उत्तर दिशा (North)", "दक्षिण दिशा (South)", "पूर्व दिशा (East)", "पश्चिम दिशा (West)"],
        "correct_index": 0,
        "hint_en": "Think of the Himalayas resting at the top crown of India's map.",
        "hint_hi": "भारत के नक्शे में सबसे ऊपर हिमालय पर्वत की दिशा याद कीजिए।",
        "encouraging_feedback_en": "Spot on, navigator! North points straight up on almost every modern map!",
        "encouraging_feedback_hi": "बिल्कुल सही! नक्शे में ऊपर हमेशा उत्तर (North) दिशा होती है!"
    }
]

def get_practice_questions(subject=None):
    """Return practice questions, optionally filtered by subject."""
    if not subject or subject.lower() == "all":
        return PRACTICE_QUESTIONS
    return [q for q in PRACTICE_QUESTIONS if q["subject"].lower() == subject.lower()]
