@echo off
title SEHAYAK - Slow Learner Support System
echo ===================================================
echo   SEHAYAK (सहायक) - Launching Application...
echo   Problem Statement ID: PSB152
echo ===================================================

if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate.bat
echo Installing requirements...
pip install -r requirements.txt

echo Initializing database and synthetic dataset if needed...
python utils/data_generator.py

echo Starting SEHAYAK Web Server...
python app.py
pause
