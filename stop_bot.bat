@echo off
REM Stop AI Research Bot

echo ========================================
echo Stopping AI Research Bot...
echo ========================================
echo.

REM Kill all Python processes running run_api.py
for /f "tokens=2" %%i in ('tasklist ^| findstr /i "python.exe"') do (
    taskkill /PID %%i /F 2>nul
)

echo.
echo ========================================
echo Bot stopped successfully!
echo ========================================
pause
