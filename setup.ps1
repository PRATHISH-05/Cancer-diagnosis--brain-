# Cancer Detection Platform - Automated Setup Script
# For Windows PowerShell

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Cancer Detection Platform Setup" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$ErrorActionPreference = "Stop"
$projectRoot = $PSScriptRoot

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow

# Check Node.js
try {
    $nodeVersion = node --version
    Write-Host "✓ Node.js installed: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not found. Please install from https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Check Python
try {
    $pythonVersion = python --version
    Write-Host "✓ Python installed: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install from https://www.python.org/" -ForegroundColor Red
    exit 1
}

# Check npm
try {
    $npmVersion = npm --version
    Write-Host "✓ npm installed: v$npmVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ npm not found. Please reinstall Node.js" -ForegroundColor Red
    exit 1
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Step 1: Installing Frontend" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$frontendPath = Join-Path $projectRoot "frontend"
if (Test-Path $frontendPath) {
    Set-Location $frontendPath
    
    Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
    npm install
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✓ Frontend dependencies installed successfully!" -ForegroundColor Green
    } else {
        Write-Host "`n✗ Frontend installation failed!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✗ Frontend directory not found!" -ForegroundColor Red
    exit 1
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Step 2: Installing Backend" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$backendPath = Join-Path $projectRoot "backend"
if (Test-Path $backendPath) {
    Set-Location $backendPath
    
    # Create virtual environment
    Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
    if (Test-Path "venv") {
        Write-Host "Virtual environment already exists, skipping..." -ForegroundColor Yellow
    } else {
        python -m venv venv
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Virtual environment created!" -ForegroundColor Green
        } else {
            Write-Host "✗ Failed to create virtual environment!" -ForegroundColor Red
            exit 1
        }
    }
    
    # Activate virtual environment
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
    
    # Install dependencies
    Write-Host "Installing backend dependencies (this may take a few minutes)..." -ForegroundColor Yellow
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✓ Backend dependencies installed successfully!" -ForegroundColor Green
    } else {
        Write-Host "`n✗ Backend installation failed!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✗ Backend directory not found!" -ForegroundColor Red
    exit 1
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Step 3: Verifying Installation" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check models
$brainModel = Join-Path $projectRoot "brain_tumor_classifier\outputs\models\brain_tumor_classifier.h5"
$lungModel = Join-Path $projectRoot "Lung\models\ct_cancer_resnet50_best.h5"

if (Test-Path $brainModel) {
    Write-Host "✓ Brain tumor model found" -ForegroundColor Green
} else {
    Write-Host "⚠ Brain tumor model not found at: $brainModel" -ForegroundColor Yellow
}

if (Test-Path $lungModel) {
    Write-Host "✓ Lung cancer model found" -ForegroundColor Green
} else {
    Write-Host "⚠ Lung cancer model not found at: $lungModel" -ForegroundColor Yellow
}

# Test imports
Write-Host "`nTesting Python imports..." -ForegroundColor Yellow
$testScript = @"
try:
    import flask
    import tensorflow
    import cv2
    import numpy
    print('✓ All Python packages imported successfully')
except ImportError as e:
    print(f'✗ Import error: {e}')
    exit(1)
"@

$testScript | python

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Installation Complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "To start the application:" -ForegroundColor Yellow
Write-Host "`n1. Start Backend (Terminal 1):" -ForegroundColor White
Write-Host "   cd backend" -ForegroundColor Gray
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "   python app.py" -ForegroundColor Gray

Write-Host "`n2. Start Frontend (Terminal 2):" -ForegroundColor White
Write-Host "   cd frontend" -ForegroundColor Gray
Write-Host "   npm run dev" -ForegroundColor Gray

Write-Host "`n3. Open Browser:" -ForegroundColor White
Write-Host "   http://localhost:3000" -ForegroundColor Gray

Write-Host "`n========================================`n" -ForegroundColor Cyan

Set-Location $projectRoot
