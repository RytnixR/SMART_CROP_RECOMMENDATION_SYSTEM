$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$frontend = Join-Path $root "frontend"
if (-not (Get-Command npm -ErrorAction SilentlyContinue)) { throw "Node.js/npm is not installed or not on PATH. Install the current Node.js LTS release, then reopen VS Code." }
Push-Location $frontend
try {
    if (-not (Test-Path (Join-Path $frontend "node_modules"))) {
        Write-Host "Installing frontend dependencies..." -ForegroundColor Cyan
        npm install
        if ($LASTEXITCODE -ne 0) { throw "npm install failed." }
    }
    Write-Host "Starting SMART CROP RECOMMENDATION SYSTEM frontend at http://localhost:5173" -ForegroundColor Green
    npm run dev
}
finally { Pop-Location }
