"""
SEHAYAK (सहायक) - CBSE 30-Marks Assessment Bank & Evaluation Engine
Provides 30-mark comprehensive curriculum tests for:
 - Mathematics
 - Science
 - Social Science
 - English
 - Hindi

Format per subject:
 - Section A: 15 Multiple Choice Questions (1 mark each = 15 marks)
 - Section B: 5 Conceptual Short Written/Typed Questions (3 marks each = 15 marks)
 Total = 30 Marks

Features dyslexia-tolerant keyword matching, audio read-aloud prompts, and positive reinforcement.
"""

CBSE_TESTS = {
    "mathematics": {
        "title": "Mathematics (CBSE Foundations & Problem Solving)",
        "subject_key": "math",
        "description": "30 Marks Assessment covering Number Systems, Fractions, Basic Algebra & Geometry.",
        "icon": "MATH",
        "mcqs": [
            {
                "id": "m_mcq_1",
                "question": "What is the product of (-5) and (-8)?",
                "options": ["-40", "+40", "-13", "+13"],
                "correct_index": 1,
                "hint": "When multiplying two negative numbers, the answer becomes positive!",
                "explanation": "Negative multiplied by negative gives positive: (-5) × (-8) = +40."
            },
            {
                "id": "m_mcq_2",
                "question": "Which fraction is equivalent to 3/4?",
                "options": ["6/8", "5/8", "9/16", "6/12"],
                "correct_index": 0,
                "hint": "Multiply both numerator and denominator by 2.",
                "explanation": "3/4 = (3×2)/(4×2) = 6/8."
            },
            {
                "id": "m_mcq_3",
                "question": "What is the value of x if 2x + 6 = 18?",
                "options": ["4", "6", "8", "12"],
                "correct_index": 1,
                "hint": "Subtract 6 from 18, then divide by 2.",
                "explanation": "2x = 18 - 6 = 12 => x = 12 / 2 = 6."
            },
            {
                "id": "m_mcq_4",
                "question": "The sum of all angles in any triangle is always:",
                "options": ["90°", "180°", "270°", "360°"],
                "correct_index": 1,
                "hint": "A flat straight line is 180°.",
                "explanation": "The angle sum property states that triangle interior angles add up to 180°."
            },
            {
                "id": "m_mcq_5",
                "question": "What is 25% of 200?",
                "options": ["25", "40", "50", "100"],
                "correct_index": 2,
                "hint": "25% is one-quarter (1/4) of the total.",
                "explanation": "200 divided by 4 equals 50."
            },
            {
                "id": "m_mcq_6",
                "question": "Which number is a prime number?",
                "options": ["9", "15", "17", "21"],
                "correct_index": 2,
                "hint": "A prime number can only be divided evenly by 1 and itself.",
                "explanation": "17 has only two factors: 1 and 17."
            },
            {
                "id": "m_mcq_7",
                "question": "The perimeter of a square with side 7 cm is:",
                "options": ["14 cm", "21 cm", "28 cm", "49 cm"],
                "correct_index": 2,
                "hint": "Perimeter = 4 × side length.",
                "explanation": "4 × 7 cm = 28 cm."
            },
            {
                "id": "m_mcq_8",
                "question": "What is the decimal representation of 1/2?",
                "options": ["0.2", "0.5", "0.05", "1.2"],
                "correct_index": 1,
                "hint": "Half of 1.0 is zero point five.",
                "explanation": "1 divided by 2 is 0.5."
            },
            {
                "id": "m_mcq_9",
                "question": "Evaluate: 10 - 3 × 2 using BODMAS order of operations.",
                "options": ["14", "4", "7", "6"],
                "correct_index": 1,
                "hint": "Multiply before subtracting: 3 × 2 = 6, then 10 - 6.",
                "explanation": "Multiplication precedes subtraction: 10 - 6 = 4."
            },
            {
                "id": "m_mcq_10",
                "question": "What is the additive inverse of -15?",
                "options": ["-15", "+15", "0", "1/15"],
                "correct_index": 1,
                "hint": "What number added to -15 results in 0?",
                "explanation": "(-15) + (+15) = 0."
            },
            {
                "id": "m_mcq_11",
                "question": "The area of a rectangle with length 8 cm and breadth 5 cm is:",
                "options": ["13 cm²", "26 cm²", "40 cm²", "80 cm²"],
                "correct_index": 2,
                "hint": "Area = Length × Breadth.",
                "explanation": "8 cm × 5 cm = 40 cm²."
            },
            {
                "id": "m_mcq_12",
                "question": "Which of these angles is an obtuse angle?",
                "options": ["45°", "90°", "120°", "180°"],
                "correct_index": 2,
                "hint": "Obtuse is greater than 90° but less than 180°.",
                "explanation": "120° is strictly between 90° and 180°."
            },
            {
                "id": "m_mcq_13",
                "question": "What is the square of 9 (9²)?",
                "options": ["18", "27", "72", "81"],
                "correct_index": 3,
                "hint": "Multiply 9 by 9.",
                "explanation": "9 × 9 = 81."
            },
            {
                "id": "m_mcq_14",
                "question": "If a car travels 120 km in 2 hours, what is its average speed?",
                "options": ["50 km/h", "60 km/h", "70 km/h", "240 km/h"],
                "correct_index": 1,
                "hint": "Speed = Distance ÷ Time.",
                "explanation": "120 km ÷ 2 h = 60 km/h."
            },
            {
                "id": "m_mcq_15",
                "question": "What is the median of the numbers: 3, 5, 7, 9, 11?",
                "options": ["5", "7", "9", "11"],
                "correct_index": 1,
                "hint": "The median is the exact middle number in ordered data.",
                "explanation": "7 is right in the center of the 5 numbers."
            }
        ],
        "written": [
            {
                "id": "m_w_1",
                "marks": 3,
                "question": "Explain the difference between a Prime number and a Composite number with one example of each.",
                "hint": "Mention factors: how many numbers can divide them?",
                "keywords": ["factor", "one", "itself", "prime", "composite", "two"],
                "model_answer": "A Prime number has only two factors (1 and itself), e.g., 5. A Composite number has more than two factors, e.g., 6 (factors 1, 2, 3, 6)."
            },
            {
                "id": "m_w_2",
                "marks": 3,
                "question": "Rohan bought a book for Rs. 200 and sold it for Rs. 250. Calculate his profit and explain the formula used.",
                "hint": "Profit = Selling Price - Cost Price.",
                "keywords": ["50", "profit", "selling", "cost", "sp", "cp"],
                "model_answer": "Profit = Selling Price - Cost Price = 250 - 200 = Rs. 50 profit."
            },
            {
                "id": "m_w_3",
                "marks": 3,
                "question": "State the Pythagorean theorem and write its formula for a right-angled triangle.",
                "hint": "Think of hypotenuse squared equals sum of the squares of other two sides.",
                "keywords": ["hypotenuse", "square", "sum", "right", "a2", "b2", "c2"],
                "model_answer": "In a right triangle, the square of the hypotenuse is equal to the sum of the squares of the other two sides: a² + b² = c²."
            },
            {
                "id": "m_w_4",
                "marks": 3,
                "question": "What is a Bar Graph? Mention two benefits of using a bar graph over a raw table of numbers.",
                "hint": "Why do visual pictures help us compare amounts easily?",
                "keywords": ["visual", "compare", "easy", "data", "bars", "clear"],
                "model_answer": "A bar graph represents data using rectangular bars. Benefits: 1. Easy visual comparison at a glance; 2. Trends are immediately visible without calculating numbers."
            },
            {
                "id": "m_w_5",
                "marks": 3,
                "question": "Solve and explain the steps: Find the area of a triangular garden with base 12 meters and height 8 meters.",
                "hint": "Area of triangle = 1/2 × base × height.",
                "keywords": ["48", "half", "base", "height", "1/2", "meters"],
                "model_answer": "Area = 1/2 × base × height = 1/2 × 12 × 8 = 6 × 8 = 48 square meters."
            }
        ]
    },

    "science": {
        "title": "Science (CBSE Concepts & Observation)",
        "subject_key": "science",
        "description": "30 Marks Assessment covering Living Organisms, Photosynthesis, Forces, and Matter.",
        "icon": "SCI",
        "mcqs": [
            {
                "id": "s_mcq_1",
                "question": "Which green pigment in leaves captures light energy for photosynthesis?",
                "options": ["Chlorophyll", "Hemoglobin", "Carotene", "Melanin"],
                "correct_index": 0,
                "hint": "It gives leaves their vibrant green color.",
                "explanation": "Chlorophyll absorbs sunlight required to combine water and CO2."
            },
            {
                "id": "s_mcq_2",
                "question": "What gas do humans inhale for cellular respiration?",
                "options": ["Nitrogen", "Carbon Dioxide", "Oxygen", "Hydrogen"],
                "correct_index": 2,
                "hint": "It makes up about 21% of Earth's atmosphere.",
                "explanation": "Our cells use oxygen to break down glucose and release energy."
            },
            {
                "id": "s_mcq_3",
                "question": "Water boils at standard atmospheric pressure at:",
                "options": ["0°C", "50°C", "100°C", "212°C"],
                "correct_index": 2,
                "hint": "In Celsius, freezing is 0 and boiling is...",
                "explanation": "100°C is the boiling point of pure water."
            },
            {
                "id": "s_mcq_4",
                "question": "The force that pulls all objects towards the center of Earth is:",
                "options": ["Friction", "Magnetism", "Gravity", "Electrostatic"],
                "correct_index": 2,
                "hint": "Discovered by Sir Isaac Newton when an apple fell.",
                "explanation": "Gravity is the attractive force exerted by Earth's mass."
            },
            {
                "id": "s_mcq_5",
                "question": "Which organ pumps blood throughout the human body?",
                "options": ["Brain", "Lungs", "Heart", "Stomach"],
                "correct_index": 2,
                "hint": "A muscular organ beating inside your chest.",
                "explanation": "The heart acts as a continuous muscular pump."
            },
            {
                "id": "s_mcq_6",
                "question": "Which of these is an example of an electrical conductor?",
                "options": ["Rubber", "Copper wire", "Wood", "Plastic"],
                "correct_index": 1,
                "hint": "Metals allow electric current to pass easily.",
                "explanation": "Copper has free electrons and is a brilliant conductor."
            },
            {
                "id": "s_mcq_7",
                "question": "The powerhouse of a cell is known as the:",
                "options": ["Nucleus", "Ribosome", "Mitochondria", "Cell wall"],
                "correct_index": 2,
                "hint": "Organelle that produces ATP energy packets.",
                "explanation": "Mitochondria release cellular energy through respiration."
            },
            {
                "id": "s_mcq_8",
                "question": "Sound cannot travel through which of the following?",
                "options": ["Air", "Water", "Steel", "Vacuum"],
                "correct_index": 3,
                "hint": "Sound waves need physical particles to vibrate.",
                "explanation": "A vacuum has no particles, so sound cannot propagate."
            },
            {
                "id": "s_mcq_9",
                "question": "Which vitamin is synthesized in our body when exposed to morning sunlight?",
                "options": ["Vitamin A", "Vitamin B", "Vitamin C", "Vitamin D"],
                "correct_index": 3,
                "hint": "Crucial for calcium absorption and healthy bones.",
                "explanation": "Skin cells synthesize Vitamin D in response to UV sunlight."
            },
            {
                "id": "s_mcq_10",
                "question": "Which gas turns lime water milky?",
                "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"],
                "correct_index": 1,
                "hint": "The gas produced when vinegar reacts with baking soda.",
                "explanation": "Carbon dioxide reacts with calcium hydroxide to form insoluble calcium carbonate."
            },
            {
                "id": "s_mcq_11",
                "question": "What is the chemical formula of common salt?",
                "options": ["H2O", "NaCl", "CO2", "CaCO3"],
                "correct_index": 1,
                "hint": "Sodium Chloride.",
                "explanation": "NaCl is the chemical symbol for table salt."
            },
            {
                "id": "s_mcq_12",
                "question": "Which part of the plant absorbs water and minerals from soil?",
                "options": ["Stem", "Leaves", "Flowers", "Roots"],
                "correct_index": 3,
                "hint": "The underground anchor system with fine hair cells.",
                "explanation": "Root hairs take in moisture and dissolved nutrients."
            },
            {
                "id": "s_mcq_13",
                "question": "A mirror that curves outward, like a car side mirror, is a:",
                "options": ["Convex mirror", "Concave mirror", "Plane mirror", "Lens"],
                "correct_index": 0,
                "hint": "It provides a wider field of view.",
                "explanation": "Convex mirrors curve outward and form smaller, upright images."
            },
            {
                "id": "s_mcq_14",
                "question": "The process of water vapor cooling and changing into liquid water is:",
                "options": ["Evaporation", "Condensation", "Sublimation", "Freezing"],
                "correct_index": 1,
                "hint": "Seen on the outside of a cold glass of water.",
                "explanation": "Condensation transforms vapor into droplets."
            },
            {
                "id": "s_mcq_15",
                "question": "Which organism is an example of a decomposer in an ecosystem?",
                "options": ["Lion", "Mushroom / Fungi", "Deer", "Mango Tree"],
                "correct_index": 1,
                "hint": "Breaks down dead matter and recycles nutrients back to soil.",
                "explanation": "Fungi and bacteria recycle organic matter."
            }
        ],
        "written": [
            {
                "id": "s_w_1",
                "marks": 3,
                "question": "What is Photosynthesis? Write the basic word equation for this vital process.",
                "hint": "Carbon dioxide + Water + Sunlight -> Glucose + Oxygen.",
                "keywords": ["carbon", "dioxide", "water", "sunlight", "glucose", "oxygen", "chlorophyll"],
                "model_answer": "Photosynthesis is the process by which green plants make food using carbon dioxide, water, and sunlight energy. Word equation: Carbon Dioxide + Water + Sunlight -> Glucose + Oxygen."
            },
            {
                "id": "s_w_2",
                "marks": 3,
                "question": "Explain Newton's First Law of Motion (Law of Inertia) with a daily life example.",
                "hint": "Why do passengers jerk forward when a moving bus brakes suddenly?",
                "keywords": ["inertia", "rest", "motion", "force", "bus", "external"],
                "model_answer": "An object remains at rest or in uniform motion unless acted upon by an external force. Example: When a bus suddenly stops, passengers lurch forward because their body tends to maintain forward motion due to inertia."
            },
            {
                "id": "s_w_3",
                "marks": 3,
                "question": "Describe two differences between Physical changes and Chemical changes.",
                "hint": "Can it be reversed? Is a new substance created?",
                "keywords": ["reversible", "new", "substance", "chemical", "physical", "ice", "rust"],
                "model_answer": "1. In physical changes, no new substance is formed and it is usually reversible (e.g., melting ice). 2. In chemical changes, a new substance with different properties is formed and it is irreversible (e.g., rusting iron)."
            },
            {
                "id": "s_w_4",
                "marks": 3,
                "question": "Why is pure drinking water essential for human health? Mention two diseases spread by contaminated water.",
                "hint": "Water carries nutrients and removes waste; dirty water spreads cholera or typhoid.",
                "keywords": ["cholera", "typhoid", "health", "hydration", "clean", "bacteria"],
                "model_answer": "Clean water is required for cell hydration, digestion, and waste elimination. Contaminated water can transmit water-borne diseases such as Cholera, Typhoid, and Dysentery."
            },
            {
                "id": "s_w_5",
                "marks": 3,
                "question": "Explain what friction is. Give one example where friction is helpful and one where it is harmful.",
                "hint": "Walking requires grip (friction); engine wear is caused by friction.",
                "keywords": ["friction", "force", "opposes", "walking", "wear", "grip", "heat"],
                "model_answer": "Friction is the contact force that opposes relative motion between two surfaces. Helpful: Allows our shoes to grip the ground for walking. Harmful: Causes wear and tear and energy loss in machine engines."
            }
        ]
    },

    "english": {
        "title": "English (CBSE Reading, Vocabulary & Grammar)",
        "subject_key": "english",
        "description": "30 Marks Assessment covering Reading Comprehension, Tenses, Parts of Speech & Expression.",
        "icon": "ENG",
        "mcqs": [
            {
                "id": "e_mcq_1",
                "question": "Identify the noun in this sentence: 'The courageous doctor arrived early.'",
                "options": ["Courageous", "Doctor", "Arrived", "Early"],
                "correct_index": 1,
                "hint": "A noun names a person, place, or thing.",
                "explanation": "'Doctor' is a person, hence a common noun."
            },
            {
                "id": "e_mcq_2",
                "question": "What is the synonym of the word 'BENEVOLENT'?",
                "options": ["Cruel", "Kind / Generous", "Cautious", "Proud"],
                "correct_index": 1,
                "hint": "A benevolent person loves helping others selflessly.",
                "explanation": "Benevolent means kindly, charitable, and generous."
            },
            {
                "id": "e_mcq_3",
                "question": "Choose the correct past tense: 'She _______ to the library yesterday.'",
                "options": ["go", "goes", "went", "gone"],
                "correct_index": 2,
                "hint": "Irregular past tense of 'to go'.",
                "explanation": "'Went' is the simple past tense of 'go'."
            },
            {
                "id": "e_mcq_4",
                "question": "What is the antonym (opposite) of 'EXPAND'?",
                "options": ["Grow", "Contract / Shrink", "Stretch", "Widen"],
                "correct_index": 1,
                "hint": "When things get smaller or pull inward.",
                "explanation": "Contract means to decrease in size, opposite of expand."
            },
            {
                "id": "e_mcq_5",
                "question": "Identify the conjunction: 'He worked hard, but he missed the bus.'",
                "options": ["Worked", "Hard", "But", "Missed"],
                "correct_index": 2,
                "hint": "A connecting word that joins two clauses.",
                "explanation": "'But' connects the two contrasting clauses."
            },
            {
                "id": "e_mcq_6",
                "question": "Choose the correct article: 'Rohan saw ______ owl sitting on the bough.'",
                "options": ["a", "an", "the", "no article"],
                "correct_index": 1,
                "hint": "'Owl' begins with an open vowel sound.",
                "explanation": "We use 'an' before words beginning with a vowel sound."
            },
            {
                "id": "e_mcq_7",
                "question": "Which sentence is written in the Passive Voice?",
                "options": [
                    "Aarav wrote a beautiful poem.",
                    "The teacher explained the lesson.",
                    "A beautiful poem was written by Aarav.",
                    "The students listened attentively."
                ],
                "correct_index": 2,
                "hint": "The object receives the action with 'was written by'.",
                "explanation": "'was written by' shifts the emphasis to the poem."
            },
            {
                "id": "e_mcq_8",
                "question": "What does the idiom 'Piece of cake' mean?",
                "options": ["A birthday celebration", "Something very easy", "A difficult task", "A bakery item"],
                "correct_index": 1,
                "hint": "'This exam was a piece of cake!'",
                "explanation": "It signifies an easy and straightforward task."
            },
            {
                "id": "e_mcq_9",
                "question": "Select the correct plural form of 'CHILD':",
                "options": ["Childs", "Childrens", "Children", "Childes"],
                "correct_index": 2,
                "hint": "An irregular plural without an 's'.",
                "explanation": "Child becomes Children in plural."
            },
            {
                "id": "e_mcq_10",
                "question": "Identify the adjective: 'The little puppy jumped excitedly.'",
                "options": ["Little", "Puppy", "Jumped", "Excitedly"],
                "correct_index": 0,
                "hint": "Describes the size of the puppy.",
                "explanation": "'Little' describes the noun puppy."
            },
            {
                "id": "e_mcq_11",
                "question": "Which punctuation mark is used to show direct speech or quotations?",
                "options": ["Colon (:)", "Quotation marks (\"\")", "Hyphen (-)", "Semicolon (;)"],
                "correct_index": 1,
                "hint": "Surrounds the exact words someone spoke.",
                "explanation": "Quotation marks encapsulate spoken dialogue."
            },
            {
                "id": "e_mcq_12",
                "question": "Complete the proverb: 'Honesty is the best _______.'",
                "options": ["Virtue", "Policy", "Habit", "Reward"],
                "correct_index": 1,
                "hint": "A famous traditional moral saying.",
                "explanation": "The proverb is 'Honesty is the best policy.'"
            },
            {
                "id": "e_mcq_13",
                "question": "Choose the adverb: 'The diligent girl solved the riddle easily.'",
                "options": ["Diligent", "Girl", "Solved", "Easily"],
                "correct_index": 3,
                "hint": "Answers 'how' the riddle was solved (-ly ending).",
                "explanation": "'Easily' modifies the verb solved."
            },
            {
                "id": "e_mcq_14",
                "question": "What is the feminine gender of 'HERO'?",
                "options": ["Heroess", "Heroine", "Heroic", "Heroette"],
                "correct_index": 1,
                "hint": "The female protagonist of a story.",
                "explanation": "Heroine is the feminine form of hero."
            },
            {
                "id": "e_mcq_15",
                "question": "Choose the correctly spelt word:",
                "options": ["Accomodation", "Acommodation", "Accommodation", "Accomadation"],
                "correct_index": 2,
                "hint": "Double 'c' and double 'm'.",
                "explanation": "Accommodation has double c and double m."
            }
        ],
        "written": [
            {
                "id": "e_w_1",
                "marks": 3,
                "question": "Read and reflect: 'Books are quiet and faithful friends.' Write 2-3 sentences explaining why reading books is valuable.",
                "hint": "Think about imagination, vocabulary, and knowledge.",
                "keywords": ["knowledge", "imagination", "vocabulary", "friend", "learn", "mind"],
                "model_answer": "Books introduce us to diverse worlds, stimulate our imagination, and expand our vocabulary. They teach us empathy and provide reliable companionship wherever we go."
            },
            {
                "id": "e_w_2",
                "marks": 3,
                "question": "Write a short 3-sentence note to your class teacher requesting one day of sick leave.",
                "hint": "Mention reason, date, and respectful sign-off.",
                "keywords": ["request", "leave", "sick", "fever", "teacher", "thanking", "sincerely"],
                "model_answer": "Respected Teacher, I kindly request you to grant me one day of leave on 30th October as I am down with fever. I will ensure all missed notes are completed. Thanking you, Yours sincerely."
            },
            {
                "id": "e_w_3",
                "marks": 3,
                "question": "Explain the difference between a Simile and a Metaphor with an example for each.",
                "hint": "Simile uses 'like' or 'as'; Metaphor states something IS something else.",
                "keywords": ["simile", "metaphor", "like", "as", "comparison", "example"],
                "model_answer": "A Simile compares two things using 'like' or 'as' (e.g., 'He is as brave as a lion'). A Metaphor states a direct comparison without 'like' or 'as' (e.g., 'Time is a thief')."
            },
            {
                "id": "e_w_4",
                "marks": 3,
                "question": "Describe your favorite hobby and explain how practicing it makes you feel.",
                "hint": "Mention drawing, reading, cycling, or music, and how it relaxes you.",
                "keywords": ["hobby", "feel", "happy", "relax", "creative", "enjoy"],
                "model_answer": "My favorite hobby is sketching nature landscapes. It allows me to express my creativity peacefully, relieves daily school stress, and brings immense joy whenever a sketch is completed."
            },
            {
                "id": "e_w_5",
                "marks": 3,
                "question": "Rewrite the sentence correctly by correcting all grammatical errors: 'She dont have no pencils for writing.' Explain what was wrong.",
                "hint": "Fix 'dont' and double negative 'no pencils'.",
                "keywords": ["does", "not", "any", "doesn't", "pencils", "double", "negative"],
                "model_answer": "Correct sentence: 'She does not have any pencils for writing.' Explanation: 'She' requires singular 'does not' (doesn't), and 'dont have no' is a double negative which is corrected to 'any pencils'."
            }
        ]
    },

    "hindi": {
        "title": "हिन्दी (CBSE व्याकरण, बोध एवं अभिव्यक्ति)",
        "subject_key": "hindi",
        "description": "30 अंकों का मूल्यांकन: अपठित बोध, व्याकरण (संज्ञा, सर्वनाम, विलोम) एवं रचनात्मक अभिव्यक्ति।",
        "icon": "HIN",
        "mcqs": [
            {
                "id": "h_mcq_1",
                "question": "इनमें से कौन सा शब्द 'सूर्य' का पर्यायवाची (समानार्थी) नहीं है?",
                "options": ["रवि", "दिनकर", "भास्कर", "निशाकर"],
                "correct_index": 3,
                "hint": "'निशा' का अर्थ रात होता है, निशाकर चंद्रमा को कहते हैं।",
                "explanation": "निशाकर चंद्रमा का नाम है, सूर्य का नहीं।"
            },
            {
                "id": "h_mcq_2",
                "question": "'सत्य' का विलोम शब्द कौन सा है?",
                "options": ["असत्य", "झूठा", "कठोर", "बुरा"],
                "correct_index": 0,
                "hint": "सत्य के आगे 'अ' उपसर्ग लगाएं।",
                "explanation": "सत्य का शुद्ध विलोम असत्य है।"
            },
            {
                "id": "h_mcq_3",
                "question": "संज्ञा के स्थान पर प्रयोग होने वाले शब्दों को क्या कहते हैं?",
                "options": ["विशेषण", "क्रिया", "सर्वनाम", "अव्यय"],
                "correct_index": 2,
                "hint": "जैसे: वह, तुम, मैं, आप।",
                "explanation": "संज्ञा के स्थान पर आने वाले शब्द सर्वनाम कहलाते हैं।"
            },
            {
                "id": "h_mcq_4",
                "question": "मुहावरे 'आँखों का तारा' का क्या अर्थ है?",
                "options": ["अत्यधिक प्रिय होना", "कम दिखाई देना", "तारे गिनना", "नाराज होना"],
                "correct_index": 0,
                "hint": "जैसे: 'हर बच्चा अपनी माँ की आँखों का तारा होता है।'",
                "explanation": "आँखों का तारा होना यानी बहुत अधिक प्यारा होना।"
            },
            {
                "id": "h_mcq_5",
                "question": "निम्न में से कौन सा शब्द भाववाचक संज्ञा है?",
                "options": ["लड़का", "सुंदरता", "दिल्ली", "पेड़"],
                "correct_index": 1,
                "hint": "जो गुण, भाव या दशा का बोध कराए।",
                "explanation": "सुंदरता एक भाववाचक संज्ञा है।"
            },
            {
                "id": "h_mcq_6",
                "question": "'विद्या + आलय' की संधि क्या होगी?",
                "options": ["विद्यलय", "विद्यालय", "विद्याल्य", "विद्याआलय"],
                "correct_index": 1,
                "hint": "दीर्घ स्वर संधि: आ + आ = आ।",
                "explanation": "विद्या + आलय = विद्यालय।"
            },
            {
                "id": "h_mcq_7",
                "question": "शुद्ध वर्तनी वाले शब्द का चयन कीजिए:",
                "options": ["उज्वल", "उज्जवल", "उज्ज्वल", "उजवल"],
                "correct_index": 2,
                "hint": "दो बार आधा 'ज' आता है।",
                "explanation": "उज्ज्वल में दो बार आधा 'ज' प्रयुक्त होता है।"
            },
            {
                "id": "h_mcq_8",
                "question": "'घोड़ा दौड़ रहा है।' वाक्य में क्रिया शब्द कौन सा है?",
                "options": ["घोड़ा", "दौड़ रहा है", "है", "तेज"],
                "correct_index": 1,
                "hint": "कार्य होने का बोध कराने वाला शब्द।",
                "explanation": "'दौड़ रहा है' कार्य संपन्न होने का बोध कराता है।"
            },
            {
                "id": "h_mcq_9",
                "question": "हिन्दी वर्णमाला में कुल कितने स्वर होते हैं?",
                "options": ["9", "11", "13", "15"],
                "correct_index": 1,
                "hint": "अ से औ तक।",
                "explanation": "मानक हिन्दी वर्णमाला में 11 स्वर होते हैं।"
            },
            {
                "id": "h_mcq_10",
                "question": "'पेड़ से फल गिरा।' वाक्य में कौन सा कारक है?",
                "options": ["करण कारक", "अपादान कारक", "कर्म कारक", "संबोधन कारक"],
                "correct_index": 1,
                "hint": "जब कोई वस्तु किसी स्थान से अलग होती है (से अलग होना)।",
                "explanation": "अलगाव का बोध कराने वाला कारक अपादान कारक कहलाता है।"
            },
            {
                "id": "h_mcq_11",
                "question": "'दशमलव' और गणित का महत्व समझाने वाले प्राचीन भारतीय विद्वान कौन थे?",
                "options": ["आर्यभट्ट", "कालिदास", "तुलसीदास", "चाणक्य"],
                "correct_index": 0,
                "hint": "शून्य और खगोल विज्ञान के प्रणेता।",
                "explanation": "आर्यभट्ट महान गणितज्ञ एवं खगोलशास्त्री थे।"
            },
            {
                "id": "h_mcq_12",
                "question": "'जल' का पर्यायवाची शब्द है:",
                "options": ["नीर", "पवन", "अनल", "गगन"],
                "correct_index": 0,
                "hint": "अमृत तुल्य तरल जो प्यास बुझाता है।",
                "explanation": "नीर, वारि, सलिल जल के पर्यायवाची हैं।"
            },
            {
                "id": "h_mcq_13",
                "question": "'प्रत्येक' शब्द का संधि विच्छेद क्या है?",
                "options": ["प्रति + एक", "प्र + प्रत्येक", "प्रत + एक", "प्रत्य + एक"],
                "correct_index": 0,
                "hint": "यण संधि: इ + ए = ये।",
                "explanation": "प्रति + एक = प्रत्येक।"
            },
            {
                "id": "h_mcq_14",
                "question": "जो सब कुछ जानता हो, उसे क्या कहते हैं?",
                "options": ["अल्पज्ञ", "सर्वज्ञ", "विद्वान", "ज्ञानी"],
                "correct_index": 1,
                "hint": "सर्व = सब, ज्ञ = जानने वाला।",
                "explanation": "सब कुछ जानने वाले को 'सर्वज्ञ' कहा जाता है।"
            },
            {
                "id": "h_mcq_15",
                "question": "'कमल' शब्द का पर्यायवाची कौन सा है?",
                "options": ["पंकज", "बादल", "सूरज", "समुद्र"],
                "correct_index": 0,
                "hint": "पंक (कीचड़) में जन्म लेने वाला।",
                "explanation": "पंकज कमल का सुप्रसिद्ध पर्यायवाची है।"
            }
        ],
        "written": [
            {
                "id": "h_w_1",
                "marks": 3,
                "question": "'परिश्रम ही सफलता की कुंजी है' - इस विचार पर 2-3 पंक्तियाँ लिखकर समझाइए।",
                "hint": "मेहनत, लक्ष्य, लगन और सफलता के बारे में लिखें।",
                "keywords": ["परिश्रम", "मेहनत", "सफलता", "लक्ष्य", "कुंजी", "लगन"],
                "model_answer": "कठिन परिश्रम और लगन के बिना कोई भी लक्ष्य हासिल नहीं किया जा सकता। जीवन में जो व्यक्ति नियमित अभ्यास और मेहनत करता है, सफलता उसके कदम चूमती है।"
            },
            {
                "id": "h_w_2",
                "marks": 3,
                "question": "संज्ञा की परिभाषा दीजिए तथा इसके तीन प्रमुख भेदों के नाम उदाहरण सहित लिखिए।",
                "hint": "किसी व्यक्ति, वस्तु, स्थान या भाव के नाम को संज्ञा कहते हैं।",
                "keywords": ["संज्ञा", "व्यक्तिवाचक", "जातिवाचक", "भाववाचक", "परिभाषा", "उदाहरण"],
                "model_answer": "किसी व्यक्ति, वस्तु, स्थान या भाव के नाम को संज्ञा कहते हैं। तीन भेद: 1. व्यक्तिवाचक (राम, दिल्ली); 2. जातिवाचक (नदी, पुस्तक); 3. भाववाचक (बचपन, मिठास)।"
            },
            {
                "id": "h_w_3",
                "marks": 3,
                "question": "पेड़-पौधों के संरक्षण का हमारे जीवन में क्या महत्व है? दो प्रमुख कारण लिखिए।",
                "hint": "ऑक्सीजन, वर्षा, पर्यावरण संतुलन और छाया।",
                "keywords": ["पेड़", "ऑक्सीजन", "पर्यावरण", "वर्षा", "प्रदूषण", "छाया"],
                "model_answer": "1. पेड़ हमें जीवनदायिनी ऑक्सीजन प्रदान करते हैं और वायु प्रदूषण घटाते हैं। 2. पेड़ वर्षा लाने और भूमि कटाव रोकने में सहायक होते हैं।"
            },
            {
                "id": "h_w_4",
                "marks": 3,
                "question": "मुहावरा 'दाँतों तले उँगली दबाना' का अर्थ स्पष्ट करते हुए एक वाक्य में प्रयोग कीजिए।",
                "hint": "अर्थ: अत्यधिक आश्चर्यचकित या दंग रह जाना।",
                "keywords": ["आश्चर्य", "दंग", "हैरान", "वाक्य", "सर्कस", "जादू"],
                "model_answer": "अर्थ: अत्यधिक आश्चर्यचकित या दंग रह जाना। वाक्य: जादूगर के हैरतअंगेज करतब देखकर सभी दर्शकों ने दाँतों तले उँगली दबा ली।"
            },
            {
                "id": "h_w_5",
                "marks": 3,
                "question": "अपने मित्र को जन्मदिन की बधाई देते हुए एक संक्षिप्त शुभकामना संदेश (2-3 पंक्तियों में) लिखिए।",
                "hint": "मित्र का नाम, शुभकामना और दीर्घायु की प्रार्थना।",
                "keywords": ["जन्मदिन", "शुभकामनाएं", "बधाई", "मित्र", "खुशी", "प्रार्थना"],
                "model_answer": "प्रिय मित्र, तुम्हें जन्मदिन की हार्दिक बधाई और शुभकामनाएं! ईश्वर तुम्हें उत्तम स्वास्थ्य, सफलता और जीवन में अपार खुशियाँ प्रदान करें।"
            }
        ]
    },

    "social science": {
        "title": "Social Science (CBSE Heritage, Geography & Civics)",
        "subject_key": "social",
        "description": "30 Marks Assessment covering Indian Constitution, Earth & Climate, History, and Democratic Values.",
        "icon": "SST",
        "mcqs": [
            {
                "id": "ss_mcq_1",
                "question": "Who is known as the 'Father of the Indian Constitution'?",
                "options": ["Mahatma Gandhi", "Dr. B.R. Ambedkar", "Jawaharlal Nehru", "Sardar Patel"],
                "correct_index": 1,
                "hint": "Chairman of the Drafting Committee of India's Constitution.",
                "explanation": "Dr. Bhimrao Ramji Ambedkar chaired the drafting committee."
            },
            {
                "id": "ss_mcq_2",
                "question": "Which imaginary line divides the Earth into the Northern and Southern Hemispheres?",
                "options": ["Tropic of Cancer", "Prime Meridian", "Equator (0°)", "Tropic of Capricorn"],
                "correct_index": 2,
                "hint": "The central zero-degree latitude belt.",
                "explanation": "The Equator sits at 0° latitude."
            },
            {
                "id": "ss_mcq_3",
                "question": "What is the primary source of all weather and climate changes on Earth?",
                "options": ["Ocean tides", "The Sun", "Earth's core", "Volcanoes"],
                "correct_index": 1,
                "hint": "Provides unequal solar heating of atmosphere and seas.",
                "explanation": "Solar radiant energy drives wind circulation and water evaporation."
            },
            {
                "id": "ss_mcq_4",
                "question": "In a democracy, the ultimate governing power rests with:",
                "options": ["The Military", "The People / Citizens", "The Monarch", "The Courts"],
                "correct_index": 1,
                "hint": "'Government of the people, by the people, for the people.'",
                "explanation": "Citizens elect their representatives through adult franchise."
            },
            {
                "id": "ss_mcq_5",
                "question": "Which of these is the largest ocean on planet Earth?",
                "options": ["Atlantic Ocean", "Indian Ocean", "Pacific Ocean", "Arctic Ocean"],
                "correct_index": 2,
                "hint": "Spans between Asia/Australia and the Americas.",
                "explanation": "The Pacific Ocean is the largest and deepest ocean."
            },
            {
                "id": "ss_mcq_6",
                "question": "The Qutub Minar was originally initiated in Delhi by which Sultan?",
                "options": ["Qutb-ud-din Aibak", "Alauddin Khilji", "Akbar", "Babur"],
                "correct_index": 0,
                "hint": "Founder of the Delhi Mamluk Sultanate.",
                "explanation": "Qutb-ud-din Aibak laid the foundation in 1199."
            },
            {
                "id": "ss_mcq_7",
                "question": "What is the minimum voting age for Indian citizens in general elections?",
                "options": ["16 years", "18 years", "21 years", "25 years"],
                "correct_index": 1,
                "hint": "Universal Adult Suffrage threshold in India.",
                "explanation": "Every citizen aged 18 or above has the right to vote."
            },
            {
                "id": "ss_mcq_8",
                "question": "Which layer of the atmosphere contains the protective Ozone layer?",
                "options": ["Troposphere", "Stratosphere", "Mesosphere", "Thermosphere"],
                "correct_index": 1,
                "hint": "Just above the troposphere where commercial jets fly.",
                "explanation": "The Stratosphere hosts the ozone layer that shields UV rays."
            },
            {
                "id": "ss_mcq_9",
                "question": "The ancient Indus Valley Civilization is world-famous for its:",
                "options": ["Pyramids", "Planned Town Planning & Drainage", "Colosseum", "Cuneiform tablets"],
                "correct_index": 1,
                "hint": "Grid pattern streets, covered brick drains, and granaries.",
                "explanation": "Harappa and Mohenjo-daro had remarkable urban sanitation."
            },
            {
                "id": "ss_mcq_10",
                "question": "Which planet in our solar system is known as the 'Blue Planet'?",
                "options": ["Mars", "Earth", "Neptune", "Venus"],
                "correct_index": 1,
                "hint": "Over 71% of its surface is covered by oceans.",
                "explanation": "Earth appears brilliant blue from space."
            },
            {
                "id": "ss_mcq_11",
                "question": "How many Fundamental Rights are guaranteed by the Constitution of India?",
                "options": ["5", "6", "7", "10"],
                "correct_index": 1,
                "hint": "Includes Right to Equality, Freedom, Education, etc.",
                "explanation": "The Indian Constitution guarantees 6 Fundamental Rights."
            },
            {
                "id": "ss_mcq_12",
                "question": "Which natural resource is considered a renewable source of energy?",
                "options": ["Coal", "Petroleum", "Solar / Sunlight", "Natural Gas"],
                "correct_index": 2,
                "hint": "Inexhaustible clean energy from above.",
                "explanation": "Solar energy replenishes naturally every day."
            },
            {
                "id": "ss_mcq_13",
                "question": "The highest peak in India (and second-highest in the world) is:",
                "options": ["Mount Everest", "K2 (Godwin-Austen)", "Kanchenjunga", "Nanda Devi"],
                "correct_index": 1,
                "hint": "Located in the Karakoram range.",
                "explanation": "K2 stands at 8,611 meters."
            },
            {
                "id": "ss_mcq_14",
                "question": "What is the official tenure of the President of India?",
                "options": ["4 years", "5 years", "6 years", "Life term"],
                "correct_index": 1,
                "hint": "Same length as the Lok Sabha term.",
                "explanation": "The President is elected for a term of 5 years."
            },
            {
                "id": "ss_mcq_15",
                "question": "Which compass direction is directly opposite to West?",
                "options": ["North", "South", "East", "North-East"],
                "correct_index": 2,
                "hint": "The direction from which the sun rises.",
                "explanation": "East is directly opposite to West on the compass."
            }
        ],
        "written": [
            {
                "id": "ss_w_1",
                "marks": 3,
                "question": "What is the Preamble to the Indian Constitution? Mention three core values stated in it.",
                "hint": "Introduction to the Constitution: Justice, Liberty, Equality, Fraternity.",
                "keywords": ["preamble", "constitution", "justice", "liberty", "equality", "fraternity", "sovereign", "democratic"],
                "model_answer": "The Preamble is the guiding introduction to the Constitution of India, outlining its core philosophy. Three key values: 1. Justice (social, economic, and political); 2. Liberty of thought and belief; 3. Equality of status and opportunity."
            },
            {
                "id": "ss_w_2",
                "marks": 3,
                "question": "Explain the difference between Weather and Climate with appropriate examples.",
                "hint": "Weather is day-to-day; climate is the long-term pattern over 30 years.",
                "keywords": ["weather", "climate", "day", "long", "pattern", "years", "rainy", "tropical"],
                "model_answer": "Weather is the day-to-day atmospheric condition at a specific time (e.g., today is cloudy and windy). Climate is the average weather pattern recorded over a prolonged duration of 30+ years (e.g., India has a tropical monsoon climate)."
            },
            {
                "id": "ss_w_3",
                "marks": 3,
                "question": "Why is water conservation vital for future generations? Suggest two practical methods to save water at home.",
                "hint": "Rainwater harvesting, fixing leaky taps, turning off taps while brushing.",
                "keywords": ["conservation", "scarcity", "rainwater", "harvesting", "tap", "waste", "save"],
                "model_answer": "Freshwater is finite and crucial for survival. Methods: 1. Turn off taps while brushing teeth and fix leaking faucets immediately; 2. Implement rooftop rainwater harvesting to recharge ground water."
            },
            {
                "id": "ss_w_4",
                "marks": 3,
                "question": "Describe what a Gram Panchayat is and mention two of its main responsibilities in rural areas.",
                "hint": "Village level local self-government: village roads, clean water, schools.",
                "keywords": ["panchayat", "village", "local", "roads", "water", "health", "sarpanch"],
                "model_answer": "The Gram Panchayat is the foundational local self-government body at the village level. Responsibilities: 1. Maintenance of village roads, drainage, and clean drinking water; 2. Promotion of village primary health centers and schools."
            },
            {
                "id": "ss_w_5",
                "marks": 3,
                "question": "Explain how the invention of the wheel transformed ancient human civilization.",
                "hint": "Transport of goods, pottery, travel, and trade.",
                "keywords": ["wheel", "transport", "pottery", "trade", "travel", "civilization", "movement"],
                "model_answer": "The wheel revolutionized human civilization by: 1. Enabling wheeled carts for faster transport of goods and humans; 2. Powering the potter's wheel for storing grain and water; 3. Fostering trade between distant early settlements."
            }
        ]
    }
}

def get_test_for_subject(subject_name):
    """Retrieve test structure for chosen CBSE subject."""
    key = subject_name.lower().strip()
    if key in CBSE_TESTS:
        return CBSE_TESTS[key]
    # Fallback to math
    return CBSE_TESTS["mathematics"]

def grade_test_submission(subject_name, mcq_answers, written_answers):
    """
    Evaluates a 30-marks CBSE assessment:
     - 15 MCQs: exact index matching (1 mark each = 15 marks)
     - 5 Written Questions: conceptual keyword matching (3 marks each = 15 marks)
    Returns:
     - total_score (float out of 30)
     - mcq_score (int out of 15)
     - written_score (float out of 15)
     - percentage (float)
     - detailed_results (list of question feedbacks)
     - encouraging_badge (str)
    """
    test_data = get_test_for_subject(subject_name)
    mcq_specs = test_data["mcqs"]
    written_specs = test_data["written"]

    mcq_score = 0
    detailed_mcq = []

    # 1. Evaluate MCQs (15 marks)
    for idx, q in enumerate(mcq_specs):
        q_id = q["id"]
        chosen_str = mcq_answers.get(q_id)
        chosen_idx = int(chosen_str) if chosen_str is not None and chosen_str != "" else -1

        is_correct = (chosen_idx == q["correct_index"])
        if is_correct:
            mcq_score += 1

        detailed_mcq.append({
            "id": q_id,
            "type": "MCQ",
            "number": idx + 1,
            "question": q["question"],
            "chosen_index": chosen_idx,
            "correct_index": q["correct_index"],
            "chosen_text": q["options"][chosen_idx] if 0 <= chosen_idx < len(q["options"]) else "Not Attempted",
            "correct_text": q["options"][q["correct_index"]],
            "is_correct": is_correct,
            "marks_awarded": 1 if is_correct else 0,
            "explanation": q["explanation"]
        })

    # 2. Evaluate Written Conceptual Responses (15 marks)
    written_score = 0.0
    detailed_written = []

    for idx, w in enumerate(written_specs):
        w_id = w["id"]
        student_text = str(written_answers.get(w_id, "")).strip().lower()
        required_keywords = w.get("keywords", [])

        # Count matched keywords
        matched = sum(1 for kw in required_keywords if kw in student_text)

        if len(student_text) < 5:
            awarded = 0.0
            feedback = "Answer was left blank or was too brief to evaluate."
        elif matched >= 3 or (len(student_text) > 30 and matched >= 2):
            awarded = 3.0
            feedback = "Superb conceptual explanation! Thorough grasp demonstrated."
        elif matched >= 1 or len(student_text) > 20:
            awarded = 2.0
            feedback = "Good effort! Core idea is present with room for more detail."
        else:
            awarded = 1.0
            feedback = "Fair attempt! Review the model explanation to strengthen keywords."

        written_score += awarded

        detailed_written.append({
            "id": w_id,
            "type": "Written",
            "number": idx + 1,
            "question": w["question"],
            "student_answer": written_answers.get(w_id, "Not Attempted"),
            "model_answer": w["model_answer"],
            "marks_awarded": awarded,
            "max_marks": w["marks"],
            "feedback": feedback
        })

    total_score = round(mcq_score + written_score, 1)
    percentage = round((total_score / 30.0) * 100, 1)

    # Award encouragement badge
    if percentage >= 80:
        badge = "CBSE Concept Champion"
    elif percentage >= 60:
        badge = "Dedicated Knowledge Explorer"
    elif percentage >= 40:
        badge = "Steady Growth Learner"
    else:
        badge = "Resilient Effort Badge"

    return {
        "subject_name": test_data["title"],
        "subject_key": test_data["subject_key"],
        "total_score": total_score,
        "max_score": 30,
        "percentage": percentage,
        "mcq_score": mcq_score,
        "written_score": round(written_score, 1),
        "badge": badge,
        "detailed_mcq": detailed_mcq,
        "detailed_written": detailed_written
    }
