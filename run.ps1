# SEHAYAK (सहायक) - Launch Script for PowerShell
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "  SEHAYAK (सहायक) - Launching Application...       " -ForegroundColor Yellow
Write-Host "  Problem Statement ID: PSB152                     " -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan

if (-not (Test-Path ".venv")) {
    Write-Host "Creating Python virtual environment (.venv)..." -ForegroundColor Green
    python -m venv .venv
}

Write-Host "Activating virtual environment..." -ForegroundColor Green
& .\.venv\Scripts\Activate.ps1

Write-Host "Verifying dependencies..." -ForegroundColor Green
pip install -r requirements.txt

Write-Host "Verifying synthetic dataset..." -ForegroundColor Green
python utils/data_generator.py

Write-Host "Starting SEHAYAK server on http://127.0.0.1:5000..." -ForegroundColor Yellow
python app.py
