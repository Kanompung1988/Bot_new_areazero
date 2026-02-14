# Quick Deploy to Render
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deploy to Render" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check git status
Write-Host "Checking git status..." -ForegroundColor Yellow
$gitStatus = git status --porcelain

if ($gitStatus) {
    Write-Host "Changes detected:" -ForegroundColor Green
    git status --short
    Write-Host ""
    
    $commit = Read-Host "Enter commit message (or press Enter for default)"
    if ([string]::IsNullOrWhiteSpace($commit)) {
        $commit = "Update bot - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    }
    
    Write-Host ""
    Write-Host "Committing changes..." -ForegroundColor Yellow
    git add .
    git commit -m $commit
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Changes committed" -ForegroundColor Green
    } else {
        Write-Host "Commit failed" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "No changes to commit" -ForegroundColor Green
}

Write-Host ""
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git push

if ($LASTEXITCODE -eq 0) {
    Write-Host "Pushed to GitHub successfully" -ForegroundColor Green
} else {
    Write-Host "Push failed" -ForegroundColor Red
    Write-Host ""
    Write-Host "If this is first push, run:" -ForegroundColor Yellow
    Write-Host "  git remote add origin YOUR_GITHUB_REPO_URL" -ForegroundColor Gray
    Write-Host "  git push -u origin main" -ForegroundColor Gray
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Code pushed to GitHub!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Setup Render (first time only):" -ForegroundColor Yellow
Write-Host "   Go to: https://dashboard.render.com/" -ForegroundColor Gray
Write-Host "   New -> Web Service" -ForegroundColor Gray
Write-Host "   Connect your GitHub repo" -ForegroundColor Gray
Write-Host "   Follow RENDER_SETUP.md" -ForegroundColor Gray
Write-Host ""
Write-Host "2. If already setup:" -ForegroundColor Yellow
Write-Host "   Render will auto-deploy!" -ForegroundColor Gray
Write-Host "   Check: https://dashboard.render.com/" -ForegroundColor Gray
Write-Host "   View deployment logs" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Setup UptimeRobot (important!):" -ForegroundColor Yellow
Write-Host "   Go to: https://uptimerobot.com/" -ForegroundColor Gray
Write-Host "   Add monitor for: https://YOUR-APP.onrender.com/health" -ForegroundColor Gray
Write-Host "   Interval: 5 minutes" -ForegroundColor Gray
Write-Host ""
Write-Host "Full guide: RENDER_SETUP.md" -ForegroundColor Cyan
Write-Host ""

$openDocs = Read-Host "Open Render dashboard in browser? (Y/N)"
if ($openDocs -eq 'Y' -or $openDocs -eq 'y') {
    Start-Process "https://dashboard.render.com/"
}

Write-Host ""
