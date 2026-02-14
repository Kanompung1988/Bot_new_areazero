# AI Research Bot - Windows Service Installer
# ติดตั้ง bot เป็น Windows Service ด้วย NSSM

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "AI Research Bot - Service Installer" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script requires Administrator privileges!" -ForegroundColor Red
    Write-Host "Please right-click and 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Set paths
$botPath = "c:\Users\User\OneDrive - Mahidol University\Desktop\Work Areazero\Bot_new_areazero_R&D"
$nssmPath = Join-Path $botPath "nssm.exe"
$pythonExe = (Get-Command python).Path
$scriptPath = Join-Path $botPath "run_api.py"
$serviceName = "AIResearchBot"

Write-Host "Bot Path: $botPath" -ForegroundColor Gray
Write-Host "Python: $pythonExe" -ForegroundColor Gray
Write-Host "Script: $scriptPath" -ForegroundColor Gray
Write-Host ""

# Check if NSSM exists
if (-not (Test-Path $nssmPath)) {
    Write-Host "NSSM not found. Downloading..." -ForegroundColor Yellow
    
    $nssmUrl = "https://nssm.cc/ci/nssm-2.24-101-g897c7ad.zip"
    $zipPath = Join-Path $env:TEMP "nssm.zip"
    $extractPath = Join-Path $env:TEMP "nssm"
    
    try {
        # Download NSSM
        Write-Host "Downloading NSSM..." -ForegroundColor Yellow
        Invoke-WebRequest -Uri $nssmUrl -OutFile $zipPath -UseBasicParsing
        
        # Extract
        Write-Host "Extracting..." -ForegroundColor Yellow
        Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force
        
        # Copy to bot directory (use 64-bit version)
        $nssmExe = Get-ChildItem -Path $extractPath -Recurse -Filter "nssm.exe" | Where-Object { $_.Directory.Name -eq "win64" } | Select-Object -First 1
        Copy-Item $nssmExe.FullName -Destination $nssmPath -Force
        
        Write-Host "NSSM installed successfully!" -ForegroundColor Green
        
        # Cleanup
        Remove-Item $zipPath -Force -ErrorAction SilentlyContinue
        Remove-Item $extractPath -Recurse -Force -ErrorAction SilentlyContinue
    }
    catch {
        Write-Host "ERROR: Failed to download NSSM" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        Write-Host ""
        Write-Host "Please download manually from: https://nssm.cc/download" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host "NSSM found!" -ForegroundColor Green
Write-Host ""

# Check if service already exists
$existingService = Get-Service -Name $serviceName -ErrorAction SilentlyContinue

if ($existingService) {
    Write-Host "Service '$serviceName' already exists!" -ForegroundColor Yellow
    $response = Read-Host "Do you want to reinstall? (y/n)"
    
    if ($response -eq 'y' -or $response -eq 'Y') {
        Write-Host "Removing existing service..." -ForegroundColor Yellow
        
        # Stop service if running
        if ($existingService.Status -eq 'Running') {
            Stop-Service -Name $serviceName -Force
            Start-Sleep -Seconds 2
        }
        
        # Remove service
        & $nssmPath remove $serviceName confirm
        Start-Sleep -Seconds 2
        Write-Host "Service removed!" -ForegroundColor Green
    }
    else {
        Write-Host "Installation cancelled." -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 0
    }
}

# Install service
Write-Host ""
Write-Host "Installing service..." -ForegroundColor Cyan

& $nssmPath install $serviceName $pythonExe "-u `"$scriptPath`""
& $nssmPath set $serviceName AppDirectory $botPath
& $nssmPath set $serviceName DisplayName "AI Research Bot"
& $nssmPath set $serviceName Description "AI Research Bot with Discord integration - Auto research daily"
& $nssmPath set $serviceName Start SERVICE_AUTO_START
& $nssmPath set $serviceName AppStdout "$botPath\logs\service_stdout.log"
& $nssmPath set $serviceName AppStderr "$botPath\logs\service_stderr.log"
& $nssmPath set $serviceName AppRotateFiles 1
& $nssmPath set $serviceName AppRotateOnline 1
& $nssmPath set $serviceName AppRotateBytes 10485760  # 10MB

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Service installed successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Service Name: $serviceName" -ForegroundColor White
Write-Host "Display Name: AI Research Bot" -ForegroundColor White
Write-Host "Status: Installed (not started)" -ForegroundColor White
Write-Host ""

$startNow = Read-Host "Do you want to start the service now? (y/n)"

if ($startNow -eq 'y' -or $startNow -eq 'Y') {
    Write-Host ""
    Write-Host "Starting service..." -ForegroundColor Cyan
    Start-Service -Name $serviceName
    Start-Sleep -Seconds 3
    
    $service = Get-Service -Name $serviceName
    Write-Host ""
    Write-Host "Service Status: $($service.Status)" -ForegroundColor $(if ($service.Status -eq 'Running') { 'Green' } else { 'Red' })
    
    if ($service.Status -eq 'Running') {
        Write-Host ""
        Write-Host "Bot is now running as a Windows Service!" -ForegroundColor Green
        Write-Host "It will auto-start on Windows boot." -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Useful Commands:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Start:   Start-Service $serviceName" -ForegroundColor White
Write-Host "Stop:    Stop-Service $serviceName" -ForegroundColor White
Write-Host "Restart: Restart-Service $serviceName" -ForegroundColor White
Write-Host "Status:  Get-Service $serviceName" -ForegroundColor White
Write-Host "Remove:  nssm remove $serviceName" -ForegroundColor White
Write-Host ""
Write-Host "Logs: $botPath\logs\" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to exit"
