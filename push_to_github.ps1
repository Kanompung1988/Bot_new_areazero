# Push to GitHub - Auto Script
# สคริปต์นี้จะช่วย push code ขึ้น GitHub อัตโนมัติ

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 Push Code to GitHub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    $gitVersion = git --version
    Write-Host "✅ Git installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git not installed!" -ForegroundColor Red
    Write-Host "Please install Git: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Get current directory
$repoPath = "c:\Users\User\OneDrive - Mahidol University\Desktop\Work Areazero\Bot_new_areazero_R&D"
Set-Location $repoPath

Write-Host "📁 Repository: $repoPath" -ForegroundColor Gray
Write-Host ""

# Check if git repo
if (-not (Test-Path ".git")) {
    Write-Host "⚠️ This is not a Git repository!" -ForegroundColor Yellow
    Write-Host ""
    $initRepo = Read-Host "Do you want to initialize Git? (y/n)"
    
    if ($initRepo -eq 'y' -or $initRepo -eq 'Y') {
        Write-Host ""
        Write-Host "Initializing Git repository..." -ForegroundColor Cyan
        git init
        Write-Host "✅ Git initialized!" -ForegroundColor Green
    } else {
        Write-Host "Cancelled." -ForegroundColor Yellow
        exit 0
    }
}

# Check git config
Write-Host "Checking Git configuration..." -ForegroundColor Gray

$userName = git config user.name 2>$null
$userEmail = git config user.email 2>$null

if (-not $userName) {
    Write-Host ""
    Write-Host "⚠️ Git user.name not configured" -ForegroundColor Yellow
    $inputName = Read-Host "Enter your name"
    git config --global user.name $inputName
    Write-Host "✅ Name set: $inputName" -ForegroundColor Green
}

if (-not $userEmail) {
    Write-Host ""
    Write-Host "⚠️ Git user.email not configured" -ForegroundColor Yellow
    $inputEmail = Read-Host "Enter your email"
    git config --global user.email $inputEmail
    Write-Host "✅ Email set: $inputEmail" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "📊 Current Status" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Check status
$status = git status --porcelain

if ($status) {
    Write-Host ""
    Write-Host "Modified/New files:" -ForegroundColor Yellow
    git status --short
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "✅ No changes to commit" -ForegroundColor Green
    Write-Host ""
    
    $stillPush = Read-Host "Push anyway? (y/n)"
    if ($stillPush -ne 'y' -and $stillPush -ne 'Y') {
        Write-Host "Cancelled." -ForegroundColor Yellow
        exit 0
    }
}

# Get commit message
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "📝 Commit Message" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$defaultMessage = "feat: Add bot reconnection, keep-alive, and PM2-like auto-restart"
Write-Host "Default: $defaultMessage" -ForegroundColor Gray

$commitMessage = Read-Host "Enter commit message (or press Enter for default)"

if (-not $commitMessage) {
    $commitMessage = $defaultMessage
}

Write-Host ""
Write-Host "Commit message: $commitMessage" -ForegroundColor White
Write-Host ""

# Add files
Write-Host "Adding files..." -ForegroundColor Cyan
git add .
Write-Host "✅ Files added" -ForegroundColor Green

# Commit
Write-Host "Creating commit..." -ForegroundColor Cyan
try {
    git commit -m $commitMessage
    Write-Host "✅ Commit created" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Nothing to commit (no changes)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🌐 GitHub Remote" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check remote
$remote = git remote get-url origin 2>$null

if ($remote) {
    Write-Host "✅ Remote configured: $remote" -ForegroundColor Green
} else {
    Write-Host "⚠️ No remote configured!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please create a GitHub repository first:" -ForegroundColor Yellow
    Write-Host "1. Go to: https://github.com/new" -ForegroundColor White
    Write-Host "2. Repository name: Bot_new_areazero_R&D" -ForegroundColor White
    Write-Host "3. Create repository" -ForegroundColor White
    Write-Host ""
    
    $repoUrl = Read-Host "Enter repository URL (e.g., https://github.com/username/Bot_new_areazero_R&D.git)"
    
    if ($repoUrl) {
        Write-Host ""
        Write-Host "Adding remote..." -ForegroundColor Cyan
        git remote add origin $repoUrl
        Write-Host "✅ Remote added!" -ForegroundColor Green
    } else {
        Write-Host "❌ No URL provided. Cancelled." -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "⬆️ Pushing to GitHub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set branch to main
Write-Host "Setting branch to main..." -ForegroundColor Cyan
git branch -M main

# Push
Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
Write-Host ""

try {
    git push -u origin main
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✅ Push Successful!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    
    if ($remote) {
        $repoWebUrl = $remote -replace '\.git$', ''
        Write-Host "🌐 View on GitHub: $repoWebUrl" -ForegroundColor Cyan
    }
    
    Write-Host ""
    Write-Host "📝 Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Go to: https://render.com/" -ForegroundColor White
    Write-Host "2. Create new Web Service" -ForegroundColor White
    Write-Host "3. Connect your GitHub repository" -ForegroundColor White
    Write-Host "4. Follow: RENDER_DEPLOYMENT_GUIDE.md" -ForegroundColor White
    Write-Host ""
    
} catch {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "❌ Push Failed!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host ""
    
    Write-Host "💡 Common issues:" -ForegroundColor Yellow
    Write-Host "1. Authentication failed:" -ForegroundColor White
    Write-Host "   - Use Personal Access Token instead of password" -ForegroundColor Gray
    Write-Host "   - Create at: https://github.com/settings/tokens" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. Repository doesn't exist:" -ForegroundColor White
    Write-Host "   - Create at: https://github.com/new" -ForegroundColor Gray
    Write-Host ""
    Write-Host "3. Permission denied:" -ForegroundColor White
    Write-Host "   - Check repository URL is correct" -ForegroundColor Gray
    Write-Host "   - Make sure you have write access" -ForegroundColor Gray
    Write-Host ""
}

Write-Host ""
Read-Host "Press Enter to exit"
