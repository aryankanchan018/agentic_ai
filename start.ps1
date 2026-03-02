# University Timetable Management System - Startup Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  University Timetable System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[1/5] Checking Python..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Python not found. Please install Python 3.10+" -ForegroundColor Red
    exit 1
}

# Check Node
Write-Host "[2/5] Checking Node.js..." -ForegroundColor Yellow
node --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Node.js not found. Please install Node.js 18+" -ForegroundColor Red
    exit 1
}

# Install Backend
Write-Host "[3/5] Installing Backend..." -ForegroundColor Yellow
Set-Location backend
pip install -r requirements.txt -q
python seed_data.py

# Install Frontend
Write-Host "[4/5] Installing Frontend..." -ForegroundColor Yellow
Set-Location ..\frontend
npm install --silent

# Start Services
Write-Host "[5/5] Starting Services..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Starting Backend Server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\..\backend'; python main.py"

Start-Sleep -Seconds 2

Write-Host "Starting Frontend Server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; npm run dev"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  System Started Successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
