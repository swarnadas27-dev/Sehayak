"""
SEHAYAK (सहायक) - Machine Learning Risk Classifier
Uses Scikit-Learn (Random Forest & Logistic Regression) to assess academic risk,
extract feature importances, and compute SHAP-style local factor contributions.
Seamlessly falls back to rule_engine if uninstalled.
"""

import os
import csv
from config import MODEL_FILE, SCALER_FILE, SYNTHETIC_DATA_PATH
from models.rule_engine import evaluate_student_rules

# Feature definition
FEATURE_COLUMNS = [
    "attendance_rate",
    "assignment_completion_rate",
    "homework_accuracy",
    "class_participation",
    "reading_speed_wpm",
    "overall_avg",
    "trend_slope",
    "math_sa2",
    "science_sa2",
    "english_sa2",
    "social_sa2",
    "hindi_sa2"
]

def extract_features(student):
    """Convert student dict to numerical feature list."""
    row = []
    for col in FEATURE_COLUMNS:
        val = student.get(col, 0.0)
        try:
            row.append(float(val))
        except (ValueError, TypeError):
            row.append(0.0)
    return row

def train_and_save_model(data_path=SYNTHETIC_DATA_PATH):
    """Train Random Forest classifier on dataset and persist with joblib."""
    try:
        import joblib
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.preprocessing import StandardScaler
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score
    except ImportError:
        print("[WARNING] scikit-learn or joblib not installed in environment. Using Rule-Based fallback engine.")
        return False

    if not os.path.exists(data_path):
        from utils.data_generator import generate_synthetic_dataset
        generate_synthetic_dataset(output_path=data_path)

    # Load data from CSV
    X, y = [], []
    with open(data_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            feat = extract_features(row)
            target = int(float(row.get("support_needed", 0)))
            X.append(feat)
            y.append(target)

    if len(X) < 20:
        print("[WARNING] Insufficient data for ML training. Falling back to rule engine.")
        return False

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )

    clf = RandomForestClassifier(
        n_estimators=100,
        max_depth=5,
        random_state=42,
        class_weight="balanced"
    )
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"[SEHAYAK ML] Model trained with test accuracy: {acc * 100:.2f}%")

    # Persist model and scaler
    os.makedirs(os.path.dirname(MODEL_FILE), exist_ok=True)
    joblib.dump(clf, MODEL_FILE)
    joblib.dump(scaler, SCALER_FILE)
    print(f"[SEHAYAK ML] Saved trained model to {MODEL_FILE}")
    return True

def auto_ensure_trained_model():
    """Ensure trained model artifact exists; if not, triggers training."""
    if not (os.path.exists(MODEL_FILE) and os.path.exists(SCALER_FILE)):
        train_and_save_model()

# Auto ensure on module import
auto_ensure_trained_model()

def calculate_feature_contributions(student):
    """
    Computes local factor contributions (SHAP-style attribution) for a given student.
    Returns list of dicts: [{'name': 'Attendance Deficit', 'impact': +18.5}, ...]
    Positive impact pushes toward support tier; Negative impact is protective.
    """
    factors = []

    # 1. Attendance Impact (Benchmark 75%)
    att = float(student.get("attendance_rate", 85.0))
    if att < 75.0:
        att_impact = round((75.0 - att) * 0.9, 1)
        factors.append({"name": "Attendance Deficit", "impact": att_impact})
    elif att >= 90.0:
        factors.append({"name": "Consistent Attendance", "impact": -14.0})

    # 2. Assignment / Homework Compliance (Benchmark 70%)
    assign = float(student.get("assignment_completion_rate", 80.0))
    if assign < 60.0:
        assign_impact = round((60.0 - assign) * 0.7, 1)
        factors.append({"name": "Incomplete Homework", "impact": assign_impact})
    elif assign >= 85.0:
        factors.append({"name": "High Task Diligence", "impact": -12.0})

    # 3. Term Trend Drop (Term 1 -> Term 2)
    slope = float(student.get("trend_slope", 0.0))
    if slope < -5.0:
        slope_impact = round(abs(slope) * 1.1, 1)
        factors.append({"name": "Score Trajectory Decline", "impact": slope_impact})
    elif slope > 5.0:
        factors.append({"name": "Positive Learning Momentum", "impact": -round(slope * 1.0, 1)})

    # 4. Reading Fluency & Dyslexia Indicator (Benchmark 110 WPM)
    wpm = float(student.get("reading_speed_wpm", 120.0))
    if wpm < 90.0:
        wpm_impact = round((90.0 - wpm) * 0.5, 1)
        factors.append({"name": "Reading Decodability Pacing", "impact": wpm_impact})

    # 5. Subject Specific Deficits (Math & Science benchmarks)
    math_sa2 = float(student.get("math_sa2", 60.0))
    if math_sa2 < 40.0:
        m_impact = round((40.0 - math_sa2) * 0.8, 1)
        factors.append({"name": "Math Foundation Gap", "impact": m_impact})
    elif math_sa2 >= 75.0:
        factors.append({"name": "Math Mastery", "impact": -10.0})

    sci_sa2 = float(student.get("science_sa2", 60.0))
    if sci_sa2 < 40.0:
        s_impact = round((40.0 - sci_sa2) * 0.7, 1)
        factors.append({"name": "Science Comprehension Gap", "impact": s_impact})

    eng_sa2 = float(student.get("english_sa2", 60.0))
    if eng_sa2 < 40.0:
        e_impact = round((40.0 - eng_sa2) * 0.6, 1)
        factors.append({"name": "Language Barrier", "impact": e_impact})

    # If list is empty or minimal, provide baseline balance
    if not factors:
        factors.append({"name": "Overall Stable Academic Performance", "impact": -15.0})

    # Sort by absolute impact descending
    factors.sort(key=lambda x: abs(x["impact"]), reverse=True)
    return factors[:6]

def predict_student_risk(student):
    """
    Predict risk level for a single student.
    Combines ML prediction with rule-based explainability and local contributions.
    """
    rule_result = evaluate_student_rules(student)
    contributions = calculate_feature_contributions(student)

    # Attempt ML inference if artifact is present
    ml_prob = None
    try:
        import joblib
        if os.path.exists(MODEL_FILE) and os.path.exists(SCALER_FILE):
            clf = joblib.load(MODEL_FILE)
            scaler = joblib.load(SCALER_FILE)
            feats = extract_features(student)
            feats_scaled = scaler.transform([feats])
            probs = clf.predict_proba(feats_scaled)[0]
            ml_prob = float(probs[1]) if len(probs) > 1 else float(probs[0])
    except Exception as e:
        ml_prob = None

    if ml_prob is not None:
        combined_score = round(0.6 * ml_prob + 0.4 * rule_result["risk_score"], 2)
        if combined_score >= 0.55 or rule_result["risk_level"] == "HIGH":
            final_risk = "HIGH"
            support_needed = 1
        elif combined_score >= 0.35 or rule_result["risk_level"] == "MODERATE":
            final_risk = "MODERATE"
            support_needed = 1
        else:
            final_risk = "LOW"
            support_needed = 0
    else:
        combined_score = rule_result["risk_score"]
        final_risk = rule_result["risk_level"]
        support_needed = rule_result["support_needed"]

    return {
        "student_id": student.get("student_id"),
        "name": student.get("name"),
        "risk_level": final_risk,
        "risk_score": combined_score,
        "support_needed": support_needed,
        "ml_probability": round(ml_prob, 2) if ml_prob is not None else combined_score,
        "reasons_en": rule_result["reasons_en"],
        "reasons_hi": rule_result["reasons_hi"],
        "strengths_en": rule_result["strengths_en"],
        "strengths_hi": rule_result["strengths_hi"],
        "weak_subjects": rule_result["weak_subjects"],
        "strong_subjects": rule_result["strong_subjects"],
        "contributions": contributions
    }

if __name__ == "__main__":
    train_and_save_model()
