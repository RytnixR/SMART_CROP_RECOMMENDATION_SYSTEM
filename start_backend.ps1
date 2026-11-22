$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$pythonExe = Join-Path $root ".venv\Scripts\python.exe"

if (-not (Test-Path $pythonExe)) {
    Write-Host "Creating project virtual environment..." -ForegroundColor Cyan
    python -m venv (Join-Path $root ".venv")
}
if (-not (Test-Path $pythonExe)) { throw "Could not create .venv. Check your Python installation." }

& $pythonExe -m pip --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "Repairing pip inside .venv..." -ForegroundColor Yellow
    & $pythonExe -m ensurepip --upgrade
    if ($LASTEXITCODE -ne 0) { throw "Could not initialize pip in .venv. Remove the root .venv folder and rerun this script." }
}

Write-Host "Installing backend dependencies..." -ForegroundColor Cyan
& $pythonExe -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw "pip upgrade failed." }
& $pythonExe -m pip install -r (Join-Path $root "backend\requirements.txt")
if ($LASTEXITCODE -ne 0) { throw "Backend dependency installation failed." }

Push-Location (Join-Path $root "backend")
try {
    Write-Host "Generating demo dataset..." -ForegroundColor Cyan
    & $pythonExe generate_demo_data.py
    if ($LASTEXITCODE -ne 0) { throw "Demo dataset generation failed." }
    Write-Host "Training and comparing Decision Tree and Random Forest..." -ForegroundColor Cyan
    & $pythonExe train_model.py
    if ($LASTEXITCODE -ne 0) { throw "Model training failed." }
    Write-Host "Starting SMART CROP RECOMMENDATION SYSTEM API at http://127.0.0.1:8000" -ForegroundColor Green
    & $pythonExe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
}
finally { Pop-Location }
