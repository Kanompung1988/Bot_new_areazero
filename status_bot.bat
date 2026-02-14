@echo off
REM Check AI Research Bot Status

title Bot Status Checker

echo ========================================
echo AI Research Bot Status
echo ========================================
echo.

REM Check if Python process is running
tasklist | findstr /i "python.exe" >nul
if %errorlevel% == 0 (
    echo Status: RUNNING
    echo.
    echo Python processes:
    tasklist | findstr /i "python.exe"
) else (
    echo Status: STOPPED
)

echo.
echo ========================================
echo Checking API endpoint...
echo ========================================

REM Try to ping the API
curl http://localhost:8000/health 2>nul
if %errorlevel% == 0 (
    echo.
    echo API Status: ONLINE
) else (
    echo.
    echo API Status: OFFLINE
)

echo.
pause
