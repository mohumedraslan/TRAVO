# Start TRAVO Backend
# This script starts the FastAPI backend server

Write-Host "🚀 Starting TRAVO Backend..." -ForegroundColor Cyan

# Navigate to backend directory
Set-Location -Path "$PSScriptRoot\travo\backend"

# Check if virtual environment exists
if (Test-Path ".venv") {
    Write-Host "✅ Activating virtual environment..." -ForegroundColor Green
    & .\.venv\Scripts\Activate.ps1
}
elseif (Test-Path "..\..\..\.venv") {
    Write-Host "✅ Activating virtual environment..." -ForegroundColor Green
    & ..\..\..\..\.venv\Scripts\Activate.ps1
}

# Check if main.py exists
if (-not (Test-Path "main.py")) {
    Write-Host "❌ Error: main.py not found in current directory" -ForegroundColor Red
    Write-Host "Current directory: $(Get-Location)" -ForegroundColor Yellow
    exit 1
}

Write-Host "📡 Starting FastAPI server on http://localhost:8001" -ForegroundColor Yellow
Write-Host "📚 API Documentation will be available at http://localhost:8001/docs" -ForegroundColor Yellow
Write-Host "" 
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

# Start the server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
