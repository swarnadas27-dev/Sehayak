"""
SEHAYAK (सहायक) - Configuration Module
Problem Statement ID: PSB152
"""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Data paths
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
SYNTHETIC_DATA_DIR = os.path.join(DATA_DIR, "synthetic")
SYNTHETIC_DATA_PATH = os.path.join(SYNTHETIC_DATA_DIR, "students_sample_250.csv")
DB_PATH = os.path.join(DATA_DIR, "sehayak.db")

# Vercel Serverless Support: Copy DB to writable /tmp directory if running on Vercel
if os.environ.get("VERCEL"):
    import shutil
    TMP_DIR = "/tmp/sehayak_data"
    os.makedirs(TMP_DIR, exist_ok=True)
    TMP_DB = os.path.join(TMP_DIR, "sehayak.db")
    ORIGINAL_DB = os.path.join(DATA_DIR, "sehayak.db")
    if not os.path.exists(TMP_DB) and os.path.exists(ORIGINAL_DB):
        shutil.copyfile(ORIGINAL_DB, TMP_DB)
    DB_PATH = TMP_DB

# Models path
MODELS_DIR = os.path.join(BASE_DIR, "models", "trained")
MODEL_FILE = os.path.join(MODELS_DIR, "risk_classifier.joblib")
SCALER_FILE = os.path.join(MODELS_DIR, "scaler.joblib")

# Ensure required directories exist
try:
    for folder in [RAW_DATA_DIR, SYNTHETIC_DATA_DIR, MODELS_DIR]:
        os.makedirs(folder, exist_ok=True)
except OSError:
    pass

# Flask Configuration
SECRET_KEY = os.environ.get("SECRET_KEY", "sehayak-psb152-edtech-secret-key-2026")
DEBUG = True
PORT = 5000
HOST = "127.0.0.1"

# Pedagogical & Risk Thresholds
SUBJECTS = ["Mathematics", "Science", "Social Science", "English", "Hindi"]
ASSESSMENTS = ["FA1", "SA1", "FA2", "SA2"]

# Risk scoring benchmarks
FAILING_MARK_THRESHOLD = 35.0          # Below 35% is considered needing academic intervention
CRITICAL_ATTENDANCE_THRESHOLD = 75.0   # Mandatory 75% CBSE/State board threshold
LOW_ASSIGNMENT_THRESHOLD = 60.0        # Less than 60% completion indicates study habit barrier
HIGH_RISK_PROB_THRESHOLD = 0.65        # ML probability threshold for Priority Support
MODERATE_RISK_PROB_THRESHOLD = 0.40    # ML probability threshold for Guided Support

# Ethical & Non-Stigmatizing Terminology
SUPPORT_LEVEL_LABELS = {
    "HIGH": "Priority Remedial Support",
    "MODERATE": "Guided Academic Support",
    "LOW": "On-Track / General Reinforcement"
}

SUPPORT_LEVEL_BADGES = {
    "HIGH": "badge-priority",
    "MODERATE": "badge-guided",
    "LOW": "badge-ontrack"
}
