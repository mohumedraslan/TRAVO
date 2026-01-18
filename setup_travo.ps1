
<#
.SYNOPSIS
    TRAVO Universal Setup & Startup Script
.DESCRIPTION
    Automates the setup and execution of Backend, Frontend, and Mobile.
    Supports Windows Terminal (wt) tabs to keep everything in one window.
#>

param (
    [string]$Mode = "All" # Options: All, Backend, Web, Mobile
)

$ErrorActionPreference = "Continue" # Don't stop on minor errors like "Process not found"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "      TRAVO SETUP & STARTUP MANAGER       " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# --- 1. CLEANUP OLD PROCESSES ---
Write-Host "[0/3] Cleaning up old TRAVO processes..." -ForegroundColor Yellow

function Stop-ProcessOnPort {
    param([int]$Port)
    $ProcessId = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -First 1
    if ($ProcessId) {
        Write-Host "Stopping process on port $Port (PID: $ProcessId)..." -ForegroundColor Gray
        Stop-Process -Id $ProcessId -Force -ErrorAction SilentlyContinue
    }
}

Stop-ProcessOnPort 8000  # Backend
Stop-ProcessOnPort 3000  # Web
Stop-ProcessOnPort 8081  # Expo (Mobile)

# --- 2. PREREQUISITES ---
if (-not (Get-Command "npm" -ErrorAction SilentlyContinue)) { Write-Error "Node.js (npm) is not installed."; exit }
if (-not (Get-Command "python" -ErrorAction SilentlyContinue)) { Write-Error "Python is not installed."; exit }

# Detect Windows Terminal (Check Path + Common Store Path)
$WTPath = Get-Command "wt" -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source
if (-not $WTPath) {
    $StorePath = "$env:LOCALAPPDATA\Microsoft\WindowsApps\wt.exe"
    if (Test-Path $StorePath) { $WTPath = $StorePath }
}

# Function to run command
function Start-ServiceWindow {
    param([string]$Command, [string]$Title, [string]$Dir, [bool]$First = $false)
    
    if ($WTPath) {
        # Use Windows Terminal Tabs
        if ($First) {
            Start-Process "$WTPath" -ArgumentList "-w", "0", "nt", "-d", "$Dir", "--title", "$Title", "powershell", "-NoExit", "-Command", "$Command"
        }
        else {
            Start-Sleep -Seconds 1
            Start-Process "$WTPath" -ArgumentList "-w", "0", "nt", "-d", "$Dir", "--title", "$Title", "powershell", "-NoExit", "-Command", "$Command"
        }
    }
    else {
        # NO WINDOWS TERMINAL: Run as Background Job to avoid terminal clutter
        Write-Host "Starting $Title in background..." -ForegroundColor Green
        # Use Start-Job so it stays in THIS terminal window
        Start-Job -Name "$Title" -ScriptBlock {
            param($d, $c)
            Set-Location "$d"
            powershell -Command "$c"
        } -ArgumentList $Dir, $Command
    }
}

# Paths
$BackendDir = "$PSScriptRoot\travo\backend"
$WebDir = "$PSScriptRoot\trovaweb"
$MobileDir = "$PSScriptRoot\trovaMobile"

# --- 3. BACKEND ---
if ($Mode -eq "All" -or $Mode -eq "Backend") {
    Write-Host "`n[1/3] Preparing Backend..." -ForegroundColor Yellow
    if (Test-Path $BackendDir) {
        if (-not (Test-Path "$BackendDir\venv")) {
            Write-Host "Creating Python venv..."
            python -m venv "$BackendDir\venv"
        }
        
        # ALWAYS check/install requirements to ensure uvicorn exists
        Write-Host "Verifying Backend dependencies..." -ForegroundColor Gray
        & "$BackendDir\venv\Scripts\pip" install -q -r "$BackendDir\requirements.txt"
        
        # Ensure PYTHONPATH is set and use correct uvicorn invocation
        $BackendCmd = "`$env:PYTHONPATH='.'; .\venv\Scripts\python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
        Start-ServiceWindow -Command $BackendCmd -Title "TRAVO-Backend" -Dir $BackendDir -First $true
    }
}

# --- 4. WEB ---
if ($Mode -eq "All" -or $Mode -eq "Web") {
    Write-Host "`n[2/3] Preparing Web..." -ForegroundColor Yellow
    if (Test-Path $WebDir) {
        if (-not (Test-Path "$WebDir\node_modules")) {
            Write-Host "Installing Web modules..."
            Push-Location $WebDir; npm install; Pop-Location
        }
        Start-ServiceWindow -Command "npm run dev" -Title "TRAVO-Web" -Dir $WebDir
    }
}

# --- 5. MOBILE ---
if ($Mode -eq "All" -or $Mode -eq "Mobile") {
    Write-Host "`n[3/3] Preparing Mobile..." -ForegroundColor Yellow
    if (Test-Path $MobileDir) {
        if (-not (Test-Path "$MobileDir\node_modules")) {
            Write-Host "Installing Mobile modules..."
            Push-Location $MobileDir; npm install; Pop-Location
        }
        Start-ServiceWindow -Command "npx expo start -c" -Title "TRAVO-Mobile" -Dir $MobileDir
    }
}

Write-Host "`n[SUCCESS] Startup initiated!" -ForegroundColor Green
if ($WTPath) {
    Write-Host "Processes are running in Windows Terminal tabs."
}
else {
    Write-Host "Processes are running in the BACKGROUND of this window."
    Write-Host "To see logs: 'Get-Job | Receive-Job -Keep'"
    Write-Host "To stop: 'Get-Job | Stop-Job'"
}
