# Install Python dependencies for the backend
Write-Host "Installing Python dependencies..." -ForegroundColor Cyan

# Navigate to backend directory
Set-Location "$PSScriptRoot\travo\backend"

# Install required packages
pip install -r requirements.txt
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install transformers==4.30.0

Write-Host "✅ Backend dependencies installed successfully" -ForegroundColor Green
