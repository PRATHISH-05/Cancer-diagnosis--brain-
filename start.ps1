# Cancer Detection Platform - Quick Start Script
# This script starts both backend and frontend servers

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Starting Cancer Detection Platform" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$projectRoot = $PSScriptRoot

# Start Backend
Write-Host "Starting backend server..." -ForegroundColor Yellow
$backendPath = Join-Path $projectRoot "backend"

Start-Process powershell -ArgumentList @"
    -NoExit
    -Command "& {
        Set-Location '$backendPath'
        Write-Host 'Activating virtual environment...' -ForegroundColor Yellow
        & '.\venv\Scripts\Activate.ps1'
        Write-Host 'Starting Flask backend...' -ForegroundColor Green
        python app.py
    }"
"@

Start-Sleep -Seconds 2

# Start Frontend
Write-Host "Starting frontend server..." -ForegroundColor Yellow
$frontendPath = Join-Path $projectRoot "frontend"

Start-Process powershell -ArgumentList @"
    -NoExit
    -Command "& {
        Set-Location '$frontendPath'
        Write-Host 'Starting React frontend...' -ForegroundColor Green
        npm run dev
    }"
"@

Start-Sleep -Seconds 3

Write-Host "`n✓ Both servers are starting..." -ForegroundColor Green
Write-Host "`nWait a few seconds, then open:" -ForegroundColor Yellow
Write-Host "http://localhost:3000" -ForegroundColor Cyan
Write-Host "`nPress Ctrl+C in each terminal window to stop the servers.`n" -ForegroundColor White
