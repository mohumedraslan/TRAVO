# TRAVO Setup Script for Windows
# This script sets up the development environment for TRAVO app

# Set error action preference
$ErrorActionPreference = "Stop"

# Function to write colored output
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] $Message" -ForegroundColor $Color
}

try {
    Write-ColorOutput "🚀 Starting TRAVO Setup..." "Cyan"
    
    # Check if Node.js is installed
    Write-ColorOutput "🔍 Checking Node.js installation..." "Yellow"
    $nodeVersion = node --version 2>$null
    if (-not $nodeVersion) {
        Write-ColorOutput "❌ Node.js is not installed. Please install Node.js from https://nodejs.org/" "Red"
        exit 1
    }
    Write-ColorOutput "✅ Node.js version: $nodeVersion" "Green"

    # Check npm version
    $npmVersion = npm --version
    Write-ColorOutput "✅ npm version: $npmVersion" "Green"

    # Install Expo CLI locally (recommended approach)
    Write-ColorOutput "📦 Installing Expo CLI locally..." "Yellow"
    npm install expo --save-dev
    $expoVersion = npx expo --version 2>$null
    if (-not $expoVersion) {
        Write-ColorOutput "❌ Failed to verify Expo CLI installation." "Red"
        exit 1
    }
    Write-ColorOutput "✅ Expo CLI version: $expoVersion" "Green"

    # Navigate to mobile app directory
    Set-Location -Path "$PSScriptRoot\trovaMobile"
    
    # Clean up previous installations (with error handling)
    Write-ColorOutput "🧹 Cleaning up previous installations..." "Yellow"
    try {
        if (Test-Path "node_modules") {
            # Try to remove node_modules with force and error action continue
            Remove-Item -Recurse -Force -ErrorAction SilentlyContinue -Path "node_modules"
        }
        if (Test-Path "package-lock.json") {
            Remove-Item -Force -ErrorAction SilentlyContinue -Path "package-lock.json"
        }
        if (Test-Path "yarn.lock") {
            Remove-Item -Force -ErrorAction SilentlyContinue -Path "yarn.lock"
        }
    } catch {
        Write-ColorOutput "⚠️  Warning: Could not clean up all previous installation files. Some files might be in use." "Yellow"
    }

    # Install dependencies with legacy peer deps
    Write-ColorOutput "📦 Installing dependencies (this may take a few minutes)..." "Yellow"
    npm install --legacy-peer-deps
    
    # Install additional required packages
    Write-ColorOutput "📦 Installing additional packages..." "Yellow"
    npm install @react-native-async-storage/async-storage --legacy-peer-deps
    npm install onnxruntime-react-native --legacy-peer-deps

    # Skip Android prebuild for web-only mode
    Write-ColorOutput "ℹ️  Skipping Android prebuild (web mode only)" "Yellow"

    # Start backend in a new PowerShell window
    Write-ColorOutput "🚀 Starting FastAPI backend..." "Yellow"
    $backendScript = @"
    try {
        Set-Location -Path "$PSScriptRoot\travo\backend"
        if (-not (Test-Path "main.py")) {
            Write-Host "❌ Error: main.py not found in $PSScriptRoot\travo\backend" -ForegroundColor Red
            exit 1
        }
        python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
    } catch {
        Write-Host "❌ Error starting backend: $_" -ForegroundColor Red
        exit 1
    }
"@
    $tempScript = [System.IO.Path]::GetTempFileName() + '.ps1'
    $backendScript | Out-File -FilePath $tempScript -Encoding utf8 -Force
    Start-Process powershell -ArgumentList "-NoExit", "-File", "`"$tempScript`"" -WindowStyle Normal

    # Give backend some time to start
    Start-Sleep -Seconds 5

    # Start Expo app
    Write-ColorOutput "🌐 Starting Expo app in web mode..." "Yellow"
    Write-ColorOutput "🔗 Expo DevTools will open in your default browser" "Cyan"
    
    # Start Expo in web mode by default
    try {
        npx expo start --web --clear
    } catch {
        Write-ColorOutput "❌ Failed to start Expo web: $_" "Red"
        Write-ColorOutput "📄 Try running manually with: cd trovaMobile && npx expo start --web" "Yellow"
        exit 1
    }

    Write-ColorOutput "✅ Setup completed successfully!" "Green"
    Write-ColorOutput "🚀 Happy coding with TRAVO!" "Cyan"

} catch {
    Write-ColorOutput "❌ An error occurred: $_" "Red"
    Write-ColorOutput "📄 Stack trace: $($_.ScriptStackTrace)" "Red"
    exit 1
}