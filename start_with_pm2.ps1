# Quick Start - รัน Bot ด้วย PM2 แบบง่ายๆ
# ไม่ต้องเปลี่ยนเป็น Next.js!

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Bot Quick Start - PM2 Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ตรวจสอบว่ามี Node.js หรือไม่
$nodeVersion = node --version 2>$null

if (-not $nodeVersion) {
    Write-Host "❌ Node.js not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "กรุณาติดตั้ง Node.js ก่อน:" -ForegroundColor Yellow
    Write-Host "1. Download: https://nodejs.org/" -ForegroundColor Gray
    Write-Host "2. Install (เลือก LTS version)" -ForegroundColor Gray
    Write-Host "3. Restart PowerShell" -ForegroundColor Gray
    Write-Host "4. Run this script again" -ForegroundColor Gray
    Write-Host ""
    
    $response = Read-Host "เปิด browser ไปหน้า download Node.js? (Y/N)"
    if ($response -eq 'Y' -or $response -eq 'y') {
        Start-Process "https://nodejs.org/"
    }
    
    exit 1
}

Write-Host "✓ Node.js version: $nodeVersion" -ForegroundColor Green

# ตรวจสอบว่ามี PM2 หรือไม่
$pm2Version = pm2 --version 2>$null

if (-not $pm2Version) {
    Write-Host "Installing PM2..." -ForegroundColor Yellow
    npm install -g pm2
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install PM2" -ForegroundColor Red
        exit 1
    }
    
    $pm2Version = pm2 --version 2>$null
    Write-Host "✓ PM2 version: $pm2Version installed" -ForegroundColor Green
} else {
    Write-Host "✓ PM2 version: $pm2Version" -ForegroundColor Green
}

Write-Host ""
Write-Host "Starting bot with PM2..." -ForegroundColor Green
Write-Host ""

# Start bot
pm2 start ecosystem.config.js

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to start bot" -ForegroundColor Red
    Write-Host "Try: pm2 logs bot" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Saving PM2 configuration..." -ForegroundColor Green
pm2 save

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✓ Bot Started Successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# แสดงสถานะ
pm2 status

Write-Host ""
Write-Host "Bot features:" -ForegroundColor Cyan
Write-Host "  • Auto-restart on crash" -ForegroundColor Gray
Write-Host "  • Memory monitoring (restart if > 500MB)" -ForegroundColor Gray
Write-Host "  • Log rotation" -ForegroundColor Gray
Write-Host "  • Keep-alive mechanism" -ForegroundColor Gray
Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Yellow
Write-Host "  pm2 status          - ดูสถานะ" -ForegroundColor Gray
Write-Host "  pm2 logs bot        - ดู logs แบบ real-time" -ForegroundColor Gray
Write-Host "  pm2 monit           - Monitor CPU/Memory" -ForegroundColor Gray
Write-Host "  pm2 restart bot     - Restart bot" -ForegroundColor Gray
Write-Host "  pm2 stop bot        - หยุด bot" -ForegroundColor Gray
Write-Host "  pm2 delete bot      - ลบ bot จาก PM2" -ForegroundColor Gray
Write-Host ""

$response = Read-Host "ต้องการตั้งให้ auto-start ตอน boot? (Y/N)"
if ($response -eq 'Y' -or $response -eq 'y') {
    Write-Host ""
    Write-Host "Setting up auto-start..." -ForegroundColor Green
    pm2 startup
    Write-Host ""
    Write-Host "✓ Bot will now start automatically when Windows boots!" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎉 Setup complete! Bot is now running 24/7" -ForegroundColor Green
Write-Host ""
