# Test Auto-Restart - ทดสอบว่า bot restart อัตโนมัติจริงไหม

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🧪 ทดสอบ Auto-Restart Mechanism" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$botPath = "c:\Users\User\OneDrive - Mahidol University\Desktop\Work Areazero\Bot_new_areazero_R&D"

# Function to check if bot is running
function Test-BotRunning {
    $pythonProcess = Get-Process python -ErrorAction SilentlyContinue
    if ($pythonProcess) {
        Write-Host "✅ Bot กำลังรัน (PID: $($pythonProcess.Id))" -ForegroundColor Green
        return $true
    } else {
        Write-Host "❌ Bot ไม่ได้รัน" -ForegroundColor Red
        return $false
    }
}

# Function to test API
function Test-BotAPI {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ API ตอบสนอง: 200 OK" -ForegroundColor Green
            return $true
        }
    } catch {
        Write-Host "❌ API ไม่ตอบสนอง" -ForegroundColor Red
        return $false
    }
    return $false
}

Write-Host "📋 การทดสอบจะทำดังนี้:" -ForegroundColor Yellow
Write-Host "1. ตรวจสอบว่า bot รันอยู่" -ForegroundColor White
Write-Host "2. Kill bot process" -ForegroundColor White
Write-Host "3. รอ 10 วินาที" -ForegroundColor White
Write-Host "4. ตรวจสอบว่า bot กลับมารันอีกครั้ง" -ForegroundColor White
Write-Host ""

$continue = Read-Host "ดำเนินการต่อ? (y/n)"

if ($continue -ne 'y' -and $continue -ne 'Y') {
    Write-Host "ยกเลิกการทดสอบ" -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Step 1: ตรวจสอบสถานะเริ่มต้น" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

if (-not (Test-BotRunning)) {
    Write-Host ""
    Write-Host "⚠️ Bot ไม่ได้รัน!" -ForegroundColor Yellow
    Write-Host "กรุณา start bot ก่อน:" -ForegroundColor Yellow
    Write-Host "  .\start_bot_background.vbs" -ForegroundColor White
    Write-Host ""
    exit 1
}

Write-Host ""
Write-Host "กำลังตรวจสอบ API..." -ForegroundColor Gray
Start-Sleep 2

if (-not (Test-BotAPI)) {
    Write-Host ""
    Write-Host "⚠️ API ยังไม่พร้อม - รอ 10 วินาที..." -ForegroundColor Yellow
    Start-Sleep 10
    
    if (-not (Test-BotAPI)) {
        Write-Host "❌ API ยังไม่ตอบสนอง - bot อาจมีปัญหา" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Step 2: Kill Bot Process" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$beforePID = (Get-Process python -ErrorAction SilentlyContinue).Id
Write-Host "PID ก่อน kill: $beforePID" -ForegroundColor Gray

Write-Host "กำลัง kill python process..." -ForegroundColor Yellow
Stop-Process -Name python -Force -ErrorAction SilentlyContinue

Start-Sleep 2

if (Test-BotRunning) {
    Write-Host "⚠️ ยังมี process อยู่ - ลอง kill อีกครั้ง" -ForegroundColor Yellow
    Stop-Process -Name python -Force -ErrorAction SilentlyContinue
    Start-Sleep 2
}

Write-Host "✅ Kill process สำเร็จ" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Step 3: รอ Auto-Restart" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "รอ 10 วินาทีเพื่อให้ bot restart..." -ForegroundColor Yellow

for ($i = 10; $i -gt 0; $i--) {
    Write-Host "⏰ เหลืออีก $i วินาที..." -NoNewline
    Start-Sleep 1
    Write-Host "`r" -NoNewline
}

Write-Host ""
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Step 4: ตรวจสอบผลลัพธ์" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "ตรวจสอบ process..." -ForegroundColor Gray
$isRunning = Test-BotRunning

Write-Host ""
Write-Host "ตรวจสอบ API..." -ForegroundColor Gray
Start-Sleep 3  # รอให้ API พร้อม

$apiWorking = Test-BotAPI

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "📊 ผลการทดสอบ" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($isRunning -and $apiWorking) {
    $afterPID = (Get-Process python -ErrorAction SilentlyContinue).Id
    
    Write-Host "PID ก่อน kill: $beforePID" -ForegroundColor Gray
    Write-Host "PID หลัง restart: $afterPID" -ForegroundColor Gray
    Write-Host ""
    
    if ($beforePID -ne $afterPID) {
        Write-Host "✅ Auto-Restart ทำงาน!" -ForegroundColor Green
        Write-Host "✅ Process ID เปลี่ยน (restart จริง)" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Process ID เหมือนเดิม (อาจไม่ restart)" -ForegroundColor Yellow
    }
    
    Write-Host "✅ Bot ทำงาน" -ForegroundColor Green
    Write-Host "✅ API ตอบสนอง" -ForegroundColor Green
    Write-Host ""
    Write-Host "🎉 การทดสอบผ่าน! Bot restart อัตโนมัติได้" -ForegroundColor Green
    Write-Host ""
    
} elseif ($isRunning -and -not $apiWorking) {
    Write-Host "⚠️ Bot รัน แต่ API ยังไม่พร้อม" -ForegroundColor Yellow
    Write-Host "ลองรอ 30 วินาทีแล้วเช็คอีกครั้ง" -ForegroundColor Yellow
    Write-Host ""
    
} else {
    Write-Host "❌ การทดสอบล้มเหลว! Bot ไม่ restart" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔍 วิธีตรวจสอบ:" -ForegroundColor Yellow
    Write-Host "1. เช็คว่า start_bot_background.vbs รันอยู่หรือไม่" -ForegroundColor White
    Write-Host "2. เช็ค logs ใน logs\bot.log" -ForegroundColor White
    Write-Host "3. ลอง start ใหม่: .\start_bot_background.vbs" -ForegroundColor White
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Read-Host "กด Enter เพื่อออก"
