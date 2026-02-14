# Pre-flight Check - ตรวจสอบทุกอย่างก่อนรันบอท
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 Pre-Flight Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# 1. Check Python
Write-Host "1️⃣ Checking Python..." -ForegroundColor Yellow
$python = Get-Command python -ErrorAction SilentlyContinue
if ($python) {
    $pythonVersion = python --version
    Write-Host "   ✓ $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "   ❌ Python not found" -ForegroundColor Red
    $allGood = $false
}

# 2. Check .env file
Write-Host "2️⃣ Checking .env file..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "   ✓ .env file exists" -ForegroundColor Green
    
    # Check for required keys
    $envContent = Get-Content ".env" -Raw
    
    $hasGemini = $envContent -match "GEMINI_API_KEY=(?!your_)"
    $hasDiscord = $envContent -match "DISCORD_TOKEN=(?!your_)"
    
    if ($hasGemini) {
        Write-Host "   ✓ GEMINI_API_KEY configured" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  GEMINI_API_KEY not set" -ForegroundColor Yellow
        $allGood = $false
    }
    
    if ($hasDiscord) {
        Write-Host "   ✓ DISCORD_TOKEN configured" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  DISCORD_TOKEN not set" -ForegroundColor Yellow
        $allGood = $false
    }
} else {
    Write-Host "   ❌ .env file not found" -ForegroundColor Red
    Write-Host "   Copy .env.example to .env and configure" -ForegroundColor Gray
    $allGood = $false
}

# 3. Check required directories
Write-Host "3️⃣ Checking directories..." -ForegroundColor Yellow
$dirs = @("data", "logs", "output")
foreach ($dir in $dirs) {
    if (Test-Path $dir) {
        Write-Host "   ✓ $dir exists" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Creating $dir..." -ForegroundColor Yellow
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "   ✓ $dir created" -ForegroundColor Green
    }
}

# 4. Check Python packages
Write-Host "4️⃣ Checking Python packages..." -ForegroundColor Yellow
$packagesToCheck = @(
    "discord.py",
    "fastapi",
    "google-generativeai",
    "feedparser"
)

$missingPackages = @()
foreach ($package in $packagesToCheck) {
    $installed = python -c "import importlib.util; print(importlib.util.find_spec('$($package.Replace('.', '_').Replace('-', '_'))') is not None)" 2>$null
    
    if ($installed -eq "True") {
        Write-Host "   ✓ $package installed" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $package not installed" -ForegroundColor Red
        $missingPackages += $package
    }
}

if ($missingPackages.Count -gt 0) {
    Write-Host ""
    Write-Host "   Installing missing packages..." -ForegroundColor Yellow
    pip install -r requirements.txt
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✓ Packages installed" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Failed to install packages" -ForegroundColor Red
        $allGood = $false
    }
}

# 5. Test Discord connection
Write-Host "5️⃣ Testing Discord connection..." -ForegroundColor Yellow
if ($hasDiscord) {
    Write-Host "   Running health check..." -ForegroundColor Gray
    python check_bot_health.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✓ Discord connection OK" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Discord connection failed" -ForegroundColor Red
        Write-Host "   Check Discord intents in Developer Portal" -ForegroundColor Gray
        $allGood = $false
    }
} else {
    Write-Host "   ⏭️  Skipped (no token)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

if ($allGood) {
    Write-Host "✅ Pre-Flight Check: PASSED" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Ready to launch! Choose your deployment method:" -ForegroundColor White
    Write-Host ""
    Write-Host "Option 1: PM2 (Recommended)" -ForegroundColor Yellow
    Write-Host "  .\start_with_pm2.ps1" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Option 2: Windows Service" -ForegroundColor Yellow
    Write-Host "  .\install_service_enhanced.ps1" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Option 3: Docker" -ForegroundColor Yellow
    Write-Host "  docker-compose up -d" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Option 4: Manual" -ForegroundColor Yellow
    Write-Host "  python run_bot.py" -ForegroundColor Gray
    Write-Host ""
    Write-Host "See KEEP_ALIVE_SOLUTIONS.md for details" -ForegroundColor Cyan
} else {
    Write-Host "❌ Pre-Flight Check: FAILED" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Please fix the issues above before launching" -ForegroundColor Yellow
}

Write-Host ""
