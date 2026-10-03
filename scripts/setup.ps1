# Digi Formation Limited — Lead Hunter Setup Script (PowerShell)
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Digi Formation Limited — Lead Hunter Setup (Windows)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir

# 1. Install Backend Requirements
Write-Host "`n[1/4] Installing Python backend dependencies..." -ForegroundColor Yellow
python -m pip install -r "$projectRootackendequirements.txt" pytest

# 2. Build Frontend Control Center
Write-Host "`n[2/4] Installing and building frontend packages..." -ForegroundColor Yellow
Set-Location "$projectRootrontend"
cmd.exe /c "npm.cmd install"
cmd.exe /c "npm.cmd run build"
Set-Location "$projectRoot"

# 3. Initialize SQLite Database
Write-Host "`n[3/4] Initializing local database..." -ForegroundColor Yellow
python "$projectRootackendpp\database.py"

# 4. Run Automated Health Checks & Tests
Write-Host "`n[4/4] Executing test suite..." -ForegroundColor Yellow
python -m pytest "$projectRoot	ests" -v

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host "  Setup completed successfully!" -ForegroundColor Green
Write-Host "  Run 'python run.py' or './scripts/start.ps1' to start." -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
