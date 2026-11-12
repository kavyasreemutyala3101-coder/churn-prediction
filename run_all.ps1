Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host " Running Telco Customer Churn Project from Start to Finish" -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

$pythonExe = Join-Path $projectRoot "venv\Scripts\python.exe"
if (-not (Test-Path $pythonExe)) {
    Write-Host "[INFO] Creating virtual environment with Python 3.11..." -ForegroundColor Yellow
    py -3.11 -m venv venv
    if (-not (Test-Path $pythonExe)) {
        python -m venv venv
    }
    Write-Host "[INFO] Installing requirements..." -ForegroundColor Yellow
    & $pythonExe -m pip install -r requirements.txt
    & $pythonExe -m pip install pytest
}

& $pythonExe run_all.py
