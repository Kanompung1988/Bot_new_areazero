@echo off
REM AI Research Bot - Auto-restart Script
REM รันแบบ PM2 - auto-restart เมื่อ crash

title AI Research Bot - Running

:start
echo ========================================
echo AI Research Bot Starting...
echo Time: %date% %time%
echo ========================================
echo.

REM Run the bot
python run_api.py

REM If bot exits, wait 5 seconds and restart
echo.
echo ========================================
echo Bot stopped! Auto-restarting in 5 seconds...
echo Press Ctrl+C to stop completely
echo ========================================
timeout /t 5 /nobreak

goto start
