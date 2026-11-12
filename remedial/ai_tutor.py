"""
SEHAYAK (सहायक) - AI Dyslexia Learning Logic & Paper Improvement Coach
Dedicated intelligent engine for dyslexic and study-focused learners.
Translates lost assessment marks into:
 1. Multisensory / CRA (Concrete-Representational-Abstract) logic rules
 2. De-crowded, low-anxiety step-by-step thinking blueprints
 3. Targeted mirror practice drills with immediate encouraging reinforcement
 4. AI-guided paper improvement strategies and test-taking cognitive scaffolds
"""

import json
from utils.db import get_max_marks_for_q, get_student_answer_sheets

# ----------------- Comprehensive Dyslexia Logic Knowledge Base -----------------

MATH_15Q_LOGIC_BANK = {
    1: {
        "concept": "Integer Multiplication & Sign Rules",
        "question_summary": "Multiply integers with positive and negative signs (e.g., (-5) × (-8)).",
        "dyslexia_barrier": "Sign confusion and visual stress where '-' signs blend into numbers or look like subtraction dashes.",
        "logic_name": "The 'Sign Partner' Logic",
        "visual_metaphor": "Signs come in pairs. When two negative signs meet in multiplication, they turn into a '+' cross: - and - snap together to make +.",
        "steps": [
            {"step": 1, "title": "Check Signs First", "detail": "Cover the numbers with your fingers. Look ONLY at the signs: (-) × (-) = (+)."},
            {"step": 2, "title": "Multiply Raw Numbers", "detail": "Now multiply the digits normally: 5 × 8 = 40."},
            {"step": 3, "title": "Combine & Double Check", "detail": "Attach your positive sign: +40. A friend of a friend is a friend!"}
        ],
        "drill": {
            "id": "drill_q1",
            "prompt": "Apply the Sign Partner Logic: What is (-6) × (-7)?",
            "options": ["-42", "+42", "-13", "+13"],
            "correct_index": 1,
            "hint": "Two negatives snap together into a positive (+). Then 6 × 7.",
            "explanation": "(-) × (-) = (+). 6 × 7 = 42. So (-6) × (-7) = +42!"
        }
    },
    2: {
        "concept": "Angles on Parallel Lines & Transversals",
        "question_summary": "Identify alternate interior and corresponding angles across parallel lines.",
        "dyslexia_barrier": "Visual crowding when multiple crossing lines create a 'web' of confusing angle spaces.",
        "logic_name": "The 'Z-Hunter' & 'F-Hunter' Letter Shape Logic",
        "visual_metaphor": "Trace familiar bold letter shapes inside the diagram to isolate exactly two angles.",
        "steps": [
            {"step": 1, "title": "Trace the Letter Z", "detail": "Trace a letter 'Z' across the parallel lines. The two inner elbow corners are Alternate Angles—they are ALWAYS equal!"},
            {"step": 2, "title": "Trace the Letter F", "detail": "Trace a letter 'F'. The two under-arm corners are Corresponding Angles—they are ALWAYS equal!"},
            {"step": 3, "title": "Color-Code", "detail": "Use a light highlighter on the two elbow corners so they jump out from the other angles."}
        ],
        "drill": {
            "id": "drill_q2",
            "prompt": "If line L is parallel to line M and one interior alternate angle inside the 'Z' shape is 65°, what is the other angle?",
            "options": ["25°", "65°", "115°", "180°"],
            "correct_index": 1,
            "hint": "Remember the Z-Hunter rule: Alternate interior elbow angles are identical twins!",
            "explanation": "The alternate interior angles inside the 'Z' shape are equal, so the other angle is exactly 65°!"
        }
    },
    3: {
        "concept": "Fraction Division & Reciprocal Operations",
        "question_summary": "Divide one fraction by another (e.g., 3/4 ÷ 1/2) and reduce to simplest form.",
        "dyslexia_barrier": "Symbol reversal: Inverting the division sign into multiplication without flipping, or flipping the wrong fraction.",
        "logic_name": "The KCF (Keep - Change - Flip) Visual Protocol",
        "visual_metaphor": "Dividing by a fraction means seeing how many smaller slices fit inside. Dividing by 1/2 doubles your slices!",
        "steps": [
            {"step": 1, "title": "KEEP the First Fraction", "detail": "Keep 3/4 exactly as it is on the left. Do not touch it."},
            {"step": 2, "title": "CHANGE the Operation", "detail": "Change the division sign (÷) into a clean multiplication sign (×)."},
            {"step": 3, "title": "FLIP the Second Fraction", "detail": "Flip 1/2 upside down into its reciprocal: 2/1."},
            {"step": 4, "title": "Multiply Across", "detail": "Top × Top: 3 × 2 = 6. Bottom × Bottom: 4 × 1 = 4. 6/4 reduces to 3/2 (1.5)."}
        ],
        "drill": {
            "id": "drill_q3",
            "prompt": "Apply the KCF Logic: Calculate 2/3 ÷ 1/6.",
            "options": ["4", "1/9", "2/18", "12/2"],
            "correct_index": 0,
            "hint": "Keep 2/3, Change ÷ to ×, Flip 1/6 into 6/1. (2 × 6) / (3 × 1) = 12 / 3.",
            "explanation": "Keep 2/3, Change to ×, Flip to 6/1: (2 × 6)/(3 × 1) = 12/3 = 4! Perfect application of KCF logic!"
        }
    },
    4: {
        "concept": "One-Step & Two-Step Linear Equations",
        "question_summary": "Solve for the unknown variable x in equations like 2x + 6 = 18.",
        "dyslexia_barrier": "Losing track of positive/negative signs when moving terms across the equals (=) boundary.",
        "logic_name": "The 'Balance Scale' Inversion Logic",
        "visual_metaphor": "An equation is a physical two-pan balance scale. Whatever weight you remove from the left pan, you MUST remove from the right pan.",
        "steps": [
            {"step": 1, "title": "Isolate the Variable Island", "detail": "Circle '2x' with your pencil. Treat it as an untouchable island for now."},
            {"step": 2, "title": "Undo the Loose Number", "detail": "The loose number is +6. Do the exact opposite: subtract 6 from both sides: 18 - 6 = 12."},
            {"step": 3, "title": "Undo the Multiplier", "detail": "Now 2x = 12. Since 2 is multiplying x, do the opposite: divide 12 by 2 = 6."}
        ],
        "drill": {
            "id": "drill_q4",
            "prompt": "Solve using the Balance Scale Logic: 3x - 5 = 16.",
            "options": ["3", "5", "7", "21"],
            "correct_index": 2,
            "hint": "Opposite of -5 is +5 (16 + 5 = 21). Then divide 21 by 3.",
            "explanation": "3x = 16 + 5 = 21. Then x = 21 ÷ 3 = 7. You balanced both sides with zero confusion!"
        }
    },
    5: {
        "concept": "Exponents & Powers of 10",
        "question_summary": "Evaluate exponential powers and scientific notation (e.g., 10³ or 4²).",
        "dyslexia_barrier": "Multiplying the base by the exponent directly (e.g., mistakenly thinking 4² is 4 × 2 = 8 instead of 4 × 4 = 16).",
        "logic_name": "The 'Cloning Machine' Logic",
        "visual_metaphor": "The base is the person stepping into the machine. The little exponent number on top is just the counter for how many twins appear!",
        "steps": [
            {"step": 1, "title": "Spot the Big Base", "detail": "The big number is the item being multiplied. In 5³, the item is 5."},
            {"step": 2, "title": "Write Out the Clones", "detail": "The little '3' says: write three 5s with multiplication dots: 5 × 5 × 5."},
            {"step": 3, "title": "Multiply Step-by-Step", "detail": "First two: 5 × 5 = 25. Now multiply by the last clone: 25 × 5 = 125."}
        ],
        "drill": {
            "id": "drill_q5",
            "prompt": "Apply the Cloning Machine Logic: What is 2⁴?",
            "options": ["8", "16", "24", "64"],
            "correct_index": 1,
            "hint": "Write out four 2s: 2 × 2 × 2 × 2. (Not 2 × 4!).",
            "explanation": "2 × 2 = 4; 4 × 2 = 8; 8 × 2 = 16. The exponent cloned 2 four times!"
        }
    },
    6: {
        "concept": "Rational Numbers & Common Denominators",
        "question_summary": "Add or subtract fractions with unlike denominators (e.g., 1/3 + 2/5).",
        "dyslexia_barrier": "Adding straight across denominators (e.g., 1/3 + 2/5 = 3/8), which breaks fraction proportions.",
        "logic_name": "The 'Same Shoe Size' (Common Denominator) Logic",
        "visual_metaphor": "You cannot run a race with one flip-flop and one boot. Fractions must wear the exact same shoe size before they can be added!",
        "steps": [
            {"step": 1, "title": "Find the Common Shoe (LCM)", "detail": "For 3 and 5, multiply them: 3 × 5 = 15. The common shoe size is 15."},
            {"step": 2, "title": "Resize the Numerators", "detail": "1/3 becomes (1×5)/15 = 5/15. 2/5 becomes (2×3)/15 = 6/15."},
            {"step": 3, "title": "Add ONLY the Tops", "detail": "5/15 + 6/15 = 11/15. Keep the shoe size 15 intact!"}
        ],
        "drill": {
            "id": "drill_q6",
            "prompt": "What is 1/4 + 2/4?",
            "options": ["3/8", "3/4", "2/8", "1/2"],
            "correct_index": 1,
            "hint": "They already wear the same shoe size (4). Just add the top numerators: 1 + 2.",
            "explanation": "Since denominators are already 4, add tops: 1 + 2 = 3. Result: 3/4."
        }
    },
    7: {
        "concept": "Exterior Angle Theorem for Triangles",
        "question_summary": "Find unknown angles using the exterior angle property of a triangle.",
        "dyslexia_barrier": "Confusing adjacent interior angles with remote interior angles.",
        "logic_name": "The 'Two Islands & Lighthouse' Logic",
        "visual_metaphor": "The outside exterior angle is a lighthouse. It shines light on the two far-away interior island angles. The lighthouse angle equals Island A + Island B!",
        "steps": [
            {"step": 1, "title": "Find the Outside Angle", "detail": "Locate the angle sticking out outside the triangle."},
            {"step": 2, "title": "Ignore the Neighbor", "detail": "Ignore the angle right next to it on the straight line."},
            {"step": 3, "title": "Sum the Remote Islands", "detail": "Add the two opposite far-away corners: Exterior = Angle 1 + Angle 2."}
        ],
        "drill": {
            "id": "drill_q7",
            "prompt": "In a triangle, the two opposite interior angles are 45° and 75°. What is the exterior angle?",
            "options": ["120°", "60°", "180°", "30°"],
            "correct_index": 0,
            "hint": "Add the two remote island angles directly: 45° + 75°.",
            "explanation": "Exterior angle = 45° + 75° = 120°. Simple addition with zero angle confusion!"
        }
    },
    8: {
        "concept": "Percentages & Unitary Ratio Method",
        "question_summary": "Convert ratios into percentages or calculate values like 15% discount on Rs. 400.",
        "dyslexia_barrier": "Multistep mental percentage calculation and decimal shifting confusion.",
        "logic_name": "The '10% Building Block' Method",
        "visual_metaphor": "Every percentage is just a lego set made of 10% blocks. Finding 10% is effortless: just slide the decimal point one step left!",
        "steps": [
            {"step": 1, "title": "Find 10% First (Slide Left)", "detail": "For Rs. 400, slide decimal one spot left: 10% = Rs. 40."},
            {"step": 2, "title": "Find 5% (Half of 10%)", "detail": "Half of Rs. 40 is Rs. 20."},
            {"step": 3, "title": "Assemble 15%", "detail": "15% = 10% + 5% = Rs. 40 + Rs. 20 = Rs. 60. No messy formulas needed!"}
        ],
        "drill": {
            "id": "drill_q8",
            "prompt": "Using the 10% Building Block Logic: What is 20% of 350?",
            "options": ["35", "70", "50", "100"],
            "correct_index": 1,
            "hint": "10% of 350 is 35. 20% is two 10% blocks (35 + 35).",
            "explanation": "10% of 350 = 35. 20% = 35 × 2 = 70. Fast, tactile mental math!"
        }
    },
    9: {
        "concept": "Perimeter vs. Area Distinction",
        "question_summary": "Calculate perimeter and area of compound geometric figures.",
        "dyslexia_barrier": "Mixing up Perimeter (units: cm) and Area (units: cm²), or adding area formulas into boundary walks.",
        "logic_name": "The 'Fence vs. Carpet' Visual Logic",
        "visual_metaphor": "Perimeter is walking a fence around the garden boundary. Area is laying square carpet tiles to cover the entire floor inside.",
        "steps": [
            {"step": 1, "title": "Fence = Add the Boundary Edges", "detail": "Trace your finger along the outside border only. Add all outer side lengths."},
            {"step": 2, "title": "Never Walk Inside for Perimeter", "detail": "Ignore any lines or dividers inside the shape when calculating perimeter."},
            {"step": 3, "title": "Carpet = Multiply Length × Width", "detail": "For area, count the inside space: Length × Width."}
        ],
        "drill": {
            "id": "drill_q9",
            "prompt": "A rectangular playground has length 10 m and width 6 m. What is its perimeter (the outer fence)?",
            "options": ["16 m", "32 m", "60 m²", "26 m"],
            "correct_index": 1,
            "hint": "Walking the whole fence: 10 + 6 + 10 + 6 (or 2 × (10 + 6)).",
            "explanation": "Perimeter = 10 + 6 + 10 + 6 = 32 meters. The fence is 32 m long!"
        }
    },
    10: {
        "concept": "Algebraic Simplification & Like Terms",
        "question_summary": "Combine like algebraic terms (e.g., 5a + 3b - 2a + 4b).",
        "dyslexia_barrier": "Letter visual blending where 'b' and 'd' or 'p' and 'q' get mixed, or accidentally adding coefficients across different letters.",
        "logic_name": "The 'Fruit Basket' Grouping Logic",
        "visual_metaphor": "Think of 'a' as Apples and 'b' as Bananas. You can bundle Apples with Apples, but you cannot mix Apples into Bananas!",
        "steps": [
            {"step": 1, "title": "Draw Shapes around Letters", "detail": "Put a SQUARE box around all 'a' terms (with their signs: [+5a], [-2a]). Put a CIRCLE around all 'b' terms: ([+3b], [+4b])."},
            {"step": 2, "title": "Add the Squares", "detail": "5a - 2a = 3a (3 Apples)."},
            {"step": 3, "title": "Add the Circles", "detail": "+3b + 4b = +7b (7 Bananas). Final Answer: 3a + 7b."}
        ],
        "drill": {
            "id": "drill_q10",
            "prompt": "Simplify using the Fruit Basket Logic: 4x + 7y - x + 2y.",
            "options": ["3x + 9y", "5x + 9y", "12xy", "3x + 5y"],
            "correct_index": 0,
            "hint": "Group x: 4x - 1x = 3x. Group y: 7y + 2y = 9y.",
            "explanation": "4x - 1x = 3x, and 7y + 2y = 9y. Result: 3x + 9y. Clean separation!"
        }
    },
    11: {
        "concept": "Multi-Step Fraction Word Problems (5 Marks)",
        "question_summary": "Solve extended word problems involving fractions of quantities (e.g., spending 2/5 on books and 1/3 of remainder on travel).",
        "dyslexia_barrier": "Word crowding: Heavy paragraph text causes reading fatigue, leading students to lose track of what the 'remainder' means.",
        "logic_name": "The CRA 'Strip Bar Model' (Concrete-Representational-Abstract)",
        "visual_metaphor": "Draw a long candy bar strip. Cut it into equal chunks instead of holding multiple fractions in your head.",
        "steps": [
            {"step": 1, "title": "Draw the Master Bar", "detail": "Draw a clean rectangle bar representing total money or total quantity."},
            {"step": 2, "title": "Shade First Portion", "detail": "If 2/5 is spent, divide bar into 5 boxes and shade 2 boxes. 3 boxes remain."},
            {"step": 3, "title": "Handle the Remainder Separately", "detail": "Look only at the remaining 3 boxes. If 1/3 of remainder is spent, shade 1 of those 3 boxes!"},
            {"step": 4, "title": "Count Leftover Boxes", "detail": "Now 2 boxes out of 5 remain. Calculate the actual rupees per box."}
        ],
        "drill": {
            "id": "drill_q11",
            "prompt": "Using the Strip Bar Model: A farmer has 60 sheep. He sells 1/3 of them. How many sheep are LEFT?",
            "options": ["20", "40", "30", "50"],
            "correct_index": 1,
            "hint": "Divide 60 into 3 equal boxes: 20 per box. He sells 1 box (20), so 2 boxes remain.",
            "explanation": "Total 60 ÷ 3 = 20 sheep per box. Remaining = 2 boxes × 20 = 40 sheep left!"
        }
    },
    12: {
        "concept": "Geometric Proofs & Angle Sum Properties (5 Marks)",
        "question_summary": "Prove that the sum of angles in a quadrilateral is 360° or calculate multi-angle configurations.",
        "dyslexia_barrier": "Working memory overload when writing multiple algebraic steps in proofs.",
        "logic_name": "The 'Diagonal Split' Logic",
        "visual_metaphor": "Every 4-sided polygon is secretly just two triangles taped together along a diagonal line!",
        "steps": [
            {"step": 1, "title": "Draw One Diagonal", "detail": "Slice the quadrilateral from corner A to corner C with a dashed pencil line."},
            {"step": 2, "title": "Count the Triangles", "detail": "You now see Triangle 1 and Triangle 2."},
            {"step": 3, "title": "Sum Their Angles", "detail": "Triangle 1 angles = 180°. Triangle 2 angles = 180°. 180° + 180° = 360°. Proof complete!"}
        ],
        "drill": {
            "id": "drill_q12",
            "prompt": "Three angles of a quadrilateral are 90°, 85°, and 75°. What is the fourth angle?",
            "options": ["110°", "100°", "90°", "120°"],
            "correct_index": 0,
            "hint": "Total sum is 360°. Add 90 + 85 + 75 = 250°, then subtract from 360°.",
            "explanation": "360° - (90° + 85° + 75°) = 360° - 250° = 110°. Clean calculation!"
        }
    },
    13: {
        "concept": "Commercial Math: Profit, Loss & Marked Price (5 Marks)",
        "question_summary": "Calculate profit percentage, cost price, and discount markups.",
        "dyslexia_barrier": "Confusing Cost Price (CP) with Selling Price (SP) in the denominator of percentage formulas.",
        "logic_name": "The 'Starting Anchor' Logic",
        "visual_metaphor": "Cost Price (CP) is the anchor in the harbor. Everything is measured against where the shopkeeper started!",
        "steps": [
            {"step": 1, "title": "Spot CP and SP", "detail": "Label clearly in the margin: CP = Initial Buy Price; SP = Customer Price."},
            {"step": 2, "title": "Find Profit Rupees", "detail": "Profit = SP - CP (Money gained)."},
            {"step": 3, "title": "Anchor to CP for Percentage", "detail": "Profit % = (Profit / CP) × 100%. ALWAYS divide by CP, never SP!"}
        ],
        "drill": {
            "id": "drill_q13",
            "prompt": "A merchant buys a toy for Rs. 50 and sells it for Rs. 60. What is his profit percentage?",
            "options": ["10%", "20%", "25%", "16.6%"],
            "correct_index": 1,
            "hint": "Profit = 60 - 50 = Rs. 10. Anchor to CP (50): (10 / 50) × 100%.",
            "explanation": "Profit = 10. (10 / 50) × 100% = (1/5) × 100% = 20% profit!"
        }
    },
    14: {
        "concept": "Comprehensive Data Handling & Double Bar Graphs (10 Marks)",
        "question_summary": "Construct and interpret frequency tables and double bar charts from survey data.",
        "dyslexia_barrier": "Eye-jumping across table rows, uneven axis scaling, and missing labels causing large mark drops.",
        "logic_name": "The 'Finger Ruler & Axis Template' Protocol",
        "visual_metaphor": "Treat your graph page like a city grid. Build the street names (axes) before building the skyscrapers (bars)!",
        "steps": [
            {"step": 1, "title": "Label Axes First (Free Marks)", "detail": "Draw X-axis (Horizontal) and Y-axis (Vertical) with arrows. Write their names immediately."},
            {"step": 2, "title": "Choose a Friendly Scale", "detail": "Pick scales of 2, 5, or 10. Never use odd numbers like 3 or 7 that strain counting."},
            {"step": 3, "title": "Use Index Card Guide", "detail": "Place your exam ruler or index card right below the current data row so your eyes don't skip rows."},
            {"step": 4, "title": "Color/Hatch the Second Bar", "detail": "For double bar graphs, make Bar 1 plain and Bar 2 diagonal hatched. Add a tiny key legend box."}
        ],
        "drill": {
            "id": "drill_q14",
            "prompt": "When creating a double bar graph to compare girls and boys across 5 sports, what must ALWAYS be included to prevent confusing the bars?",
            "options": ["A Key / Legend showing which bar is girls vs boys", "Different colors for every single number", "A 3D drawing effect", "Writing answers in cursive"],
            "correct_index": 0,
            "hint": "A viewer must know which bar represents girls and which represents boys.",
            "explanation": "A Key / Legend is essential! It tells the examiner exactly what each bar represents."
        }
    },
    15: {
        "concept": "Advanced Mensuration & Surface Areas (10 Marks)",
        "question_summary": "Solve multi-part area, surface area, and volume problems with real-world dimensions.",
        "dyslexia_barrier": "Sentence fatigue in long paragraph problem statements and unit mismatch (mixing cm with meters).",
        "logic_name": "The 'Unit Guard & Bracket Substitution' Protocol",
        "visual_metaphor": "Put on your security guard glasses: Check all units at the gate before letting them into your formula!",
        "steps": [
            {"step": 1, "title": "Unit Guard Check", "detail": "Scan all numbers: are they all cm, or is one in meters? Convert meters to cm first (1 m = 100 cm)."},
            {"step": 2, "title": "Write the Pure Formula", "detail": "Write the pure formula on its own line: e.g., Volume = Length × Width × Height."},
            {"step": 3, "title": "Substitute in Brackets", "detail": "Put every number inside its own bracket: V = (10) × (5) × (4). This stops digits from colliding."},
            {"step": 4, "title": "One Operation Per Line", "detail": "Do not rush into one giant calculation. Write one clean line per operation."}
        ],
        "drill": {
            "id": "drill_q15",
            "prompt": "A box has length 2 meters and width 50 cm. Before multiplying to find the area, what must you do to the units?",
            "options": ["Convert 2 meters into 200 cm so both units match", "Multiply 2 × 50 directly to get 100", "Divide 50 by 2", "Ignore the units"],
            "correct_index": 0,
            "hint": "The Unit Guard rule: Never mix meters and centimeters without converting first!",
            "explanation": "2 meters = 200 cm. Now both are in cm: Area = 200 cm × 50 cm = 10,000 cm². Safety first!"
        }
    }
}

# ----------------- Core Logic Functions -----------------

def get_question_logic_detail(q_num, subject="Mathematics"):
    """Fetch the dyslexia-friendly logic breakdown and drill for a specific question number."""
    try:
        q_int = int(q_num)
    except (ValueError, TypeError):
        q_int = 1

    logic_data = MATH_15Q_LOGIC_BANK.get(q_int)
    if not logic_data:
        logic_data = MATH_15Q_LOGIC_BANK[1]

    max_marks = get_max_marks_for_q(q_int)
    return {
        "q": q_int,
        "max_marks": max_marks,
        "subject": subject,
        **logic_data
    }

def analyze_student_paper_performance(student_id="SH-2026-001", target_subject="Mathematics"):
    """
    Analyzes student answer sheets, detects questions where marks were lost,
    and returns a tailored dyslexia remediation plan for that paper.
    """
    sheets = get_student_answer_sheets(student_id)
    selected_sheet = None

    # Find the target subject sheet (or fallback to latest)
    for s in sheets:
        if s.get("subject", "").lower() == target_subject.lower():
            selected_sheet = s
            break
    if not selected_sheet and sheets:
        selected_sheet = sheets[0]

    # Default fallback data if no sheets exist in DB
    if not selected_sheet:
        selected_sheet = {
            "id": 1,
            "subject": "Mathematics",
            "exam_name": "Half Yearly Examination (2026-2027)",
            "total_marks_obtained": 39.0,
            "total_max_marks": 50.0,
            "question_marks": {
                "1": 1.0, "2": 1.0, "3": 0.5, "4": 1.0, "5": 0.5,
                "6": 1.5, "7": 2.0, "8": 1.0, "9": 1.5, "10": 2.0,
                "11": 3.5, "12": 4.5, "13": 3.0, "14": 7.5, "15": 8.5
            },
            "teacher_weaknesses": "Questions 3, 5, 8, 11, 14: Struggles with multi-step fractional word problems and long essay derivations. Noticeable reading fatigue in Section D (Q14-15).",
            "teacher_improvements": "Questions 1, 2, 4, 6, 7, 10, 12: Clear improvement in geometry calculations and neat step layout."
        }

    q_marks_raw = selected_sheet.get("question_marks", {})
    if isinstance(q_marks_raw, str):
        try:
            q_marks_raw = json.loads(q_marks_raw)
        except Exception:
            q_marks_raw = {}

    # Extract all 15 questions and evaluate performance
    questions_analysis = []
    weak_questions = []
    strong_questions = []
    total_recoverable_marks = 0.0

    for q in range(1, 16):
        max_m = get_max_marks_for_q(q)
        q_str = str(q)
        q_key = f"q{q}"
        obt = q_marks_raw.get(q_str, q_marks_raw.get(q_key, q_marks_raw.get(q, max_m)))
        try:
            obt_float = float(obt)
        except (ValueError, TypeError):
            obt_float = float(max_m)

        lost_marks = round(max(0.0, max_m - obt_float), 2)
        pct = round((obt_float / max_m) * 100, 1)

        logic_info = get_question_logic_detail(q, selected_sheet.get("subject", "Mathematics"))

        item = {
            "q": q,
            "max_marks": max_m,
            "marks_obtained": obt_float,
            "lost_marks": lost_marks,
            "percentage": pct,
            "status": "MASTERED" if lost_marks == 0 else ("NEEDS_PRACTICE" if lost_marks <= 1.5 else "PRIORITY_REPAIR"),
            "logic": logic_info
        }

        questions_analysis.append(item)

        if lost_marks > 0:
            total_recoverable_marks += lost_marks
            weak_questions.append(item)
        else:
            strong_questions.append(item)

    # Sort weak questions by recovery opportunity (highest lost marks first)
    weak_questions.sort(key=lambda x: x["lost_marks"], reverse=True)

    total_obtained = selected_sheet.get("total_marks_obtained", sum(i["marks_obtained"] for i in questions_analysis))
    total_max = selected_sheet.get("total_max_marks", 50.0)

    # Dyslexia-friendly Paper Improvement Blueprint
    paper_coaching = {
        "paper_title": f"{selected_sheet.get('subject')} - {selected_sheet.get('exam_name')}",
        "subject": selected_sheet.get("subject", "Mathematics"),
        "total_obtained": total_obtained,
        "total_max": total_max,
        "percentage": round((total_obtained / total_max) * 100, 1),
        "total_recoverable_marks": round(total_recoverable_marks, 1),
        "target_next_score": min(total_max, round(total_obtained + total_recoverable_marks, 1)),
        "weak_count": len(weak_questions),
        "strong_count": len(strong_questions),
        "teacher_notes": selected_sheet.get("teacher_weaknesses", ""),
        "teacher_growth": selected_sheet.get("teacher_improvements", ""),
        "exam_hacks": [
            {
                "title": "The 'Margin Decrowder' Pencil Line",
                "tag": "Visual Organization",
                "icon": "LINE",
                "summary": "Draw a neat vertical pencil line 4 cm from the right margin. Use this purely for rough arithmetic and number extraction so your main answer page never looks cluttered."
            },
            {
                "title": "Action-Verb Highlighting",
                "tag": "Dyslexia Comprehension",
                "icon": "HIGHLIGHT",
                "summary": "Before reading long word problems in Q11 or Q14, circle the action word (e.g., 'Find', 'Calculate', 'What fraction is left?'). This anchors your focus on the final goal."
            },
            {
                "title": "The 30-Second Sensory Eye Reset",
                "tag": "Fatigue Buster",
                "icon": "RESET",
                "summary": "Between Section B (2M) and Section C/D (5M/10M), close your eyes for 30 seconds and take two slow breaths. This resets ocular convergence and stops words from swimming."
            },
            {
                "title": "Brackets for Substituted Digits",
                "tag": "Calculation Guard",
                "icon": "BRACKETS",
                "summary": "Whenever replacing a letter with a number (e.g. in Area or Algebra), always wrap the number in brackets like 2(5) + 3. It stops numbers from running together into 25 + 3."
            }
        ]
    }

    return {
        "sheet": selected_sheet,
        "coaching": paper_coaching,
        "weak_questions": weak_questions,
        "strong_questions": strong_questions,
        "all_questions": questions_analysis
    }
