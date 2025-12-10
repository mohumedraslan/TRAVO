
<#
.SYNOPSIS
    TRAVO Universal Setup & Startup Script
.DESCRIPTION
    Automates the setup and execution of Backend, Frontend (Next.js), and Mobile (Expo).
    Supports Windows Terminal (wt) tabs to keep everything in one window.
#>

param (
    [string]$Mode = "All" # Options: All, Backend, Web, Mobile
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "      TRAVO SETUP & STARTUP MANAGER       " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Check Prerequisites
if (-not (Get-Command "npm" -ErrorAction SilentlyContinue)) { Write-Error "Node.js (npm) is not installed."; exit }
if (-not (Get-Command "python" -ErrorAction SilentlyContinue)) { Write-Error "Python is not installed."; exit }

# Detect Windows Terminal
$HasWT = Get-Command "wt" -ErrorAction SilentlyContinue

# Function to run command
function Start-ServiceWindow {
    param([string]$Command, [string]$Title, [string]$Dir, [bool]$First = $false)
    
    $FullCommand = "cd '$Dir'; $Command"
    
    if ($HasWT) {
        # Use Windows Terminal Tabs
        if ($First) {
            # Start new WT window
            Start-Process wt -ArgumentList "-w", "0", "nt", "-d", "$Dir", "--title", "$Title", "powershell", "-NoExit", "-Command", "$Command"
        }
        else {
            # Add tab to existing window (assuming focused/last used)
            Start-Process wt -ArgumentList "-w", "0", "nt", "-d", "$Dir", "--title", "$Title", "powershell", "-NoExit", "-Command", "$Command"
        }
    }
    else {
        # Fallback to separate windows
        Write-Host "Starting $Title..." -ForegroundColor Green
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "$FullCommand"
    }
}

# Paths
$BackendDir = "$PSScriptRoot\travo\backend"
$WebDir = "$PSScriptRoot\trovaweb"
$MobileDir = "$PSScriptRoot\trovaMobile"

# 1. SETUP BACKEND
if ($Mode -eq "All" -or $Mode -eq "Backend") {
    Write-Host "`n[1/3] Checking Backend..." -ForegroundColor Yellow
    if (Test-Path $BackendDir) {
        Push-Location $BackendDir
        if (-not (Test-Path "venv")) {
            Write-Host "Creating Python venv..."
            python -m venv venv
            Write-Host "Installing requirements..."
            .\venv\Scripts\pip install -r requirements.txt
        }
        Pop-Location
        
        Start-ServiceWindow -Command ".\venv\Scripts\python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000" -Title "TRAVO Backend" -Dir $BackendDir -First $true
    }
}

# 2. SETUP WEB
if ($Mode -eq "All" -or $Mode -eq "Web") {
    Write-Host "`n[2/3] Checking Web..." -ForegroundColor Yellow
    if (Test-Path $WebDir) {
        Push-Location $WebDir
        if (-not (Test-Path "node_modules")) {
            Write-Host "Installing Web modules..."
            npm install
        }
        Pop-Location
        
        Start-ServiceWindow -Command "npm run dev" -Title "TRAVO Web" -Dir $WebDir
    }
}

# 3. SETUP MOBILE
if ($Mode -eq "All" -or $Mode -eq "Mobile") {
    Write-Host "`n[3/3] Checking Mobile..." -ForegroundColor Yellow
    if (Test-Path $MobileDir) {
        Push-Location $MobileDir
        if (-not (Test-Path "node_modules")) {
            Write-Host "Installing Mobile modules..."
            npm install
        }
        Pop-Location
        
        # 'npx expo start -c' usually requires interaction, but -c clears cache.
        Start-ServiceWindow -Command "npx expo start -c" -Title "TRAVO Mobile" -Dir $MobileDir
    }
}

Write-Host "`n[SUCCESS] Startup initiated!" -ForegroundColor Green
Write-Host "If you have Windows Terminal installed, look for the new tabs."
Write-Host "Otherwise, check the new popup windows."
