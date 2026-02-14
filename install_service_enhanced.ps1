# AI Research Bot - Enhanced Windows Service Installer with Auto-Restart
# ติดตั้ง bot เป็น Windows Service ด้วย NSSM พร้อม auto-restart และ keep-alive

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "AI Research Bot - Enhanced Service Installer" -ForegroundColor Cyan
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
$botPath = $PSScriptRoot
$nssmPath = Join-Path $botPath "nssm.exe"
$pythonExe = (Get-Command python -ErrorAction SilentlyContinue).Path
$scriptPath = Join-Path $botPath "run_api.py"
$serviceName = "AIResearchBot"

Write-Host "Bot Path: $botPath" -ForegroundColor Gray
Write-Host "Python: $pythonExe" -ForegroundColor Gray
Write-Host "Script: $scriptPath" -ForegroundColor Gray
Write-Host ""

# Check Python
if (-not $pythonExe) {
    Write-Host "ERROR: Python not found in PATH!" -ForegroundColor Red
    Write-Host "Please install Python and add it to PATH" -ForegroundColor Yellow
    exit 1
}

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
        
        # Copy appropriate version
        $arch = if ([Environment]::Is64BitOperatingSystem) { "win64" } else { "win32" }
        $nssmSource = Get-ChildItem -Path $extractPath -Filter "nssm.exe" -Recurse | Where-Object { $_.FullName -like "*\$arch\*" } | Select-Object -First 1
        
        if ($nssmSource) {
            Copy-Item $nssmSource.FullName $nssmPath
            Write-Host "NSSM downloaded successfully" -ForegroundColor Green
        } else {
            throw "Could not find NSSM executable in archive"
        }
        
        # Cleanup
        Remove-Item $zipPath -Force -ErrorAction SilentlyContinue
        Remove-Item $extractPath -Recurse -Force -ErrorAction SilentlyContinue
        
    } catch {
        Write-Host "ERROR: Failed to download NSSM: $_" -ForegroundColor Red
        Write-Host "Please download NSSM manually from https://nssm.cc/download" -ForegroundColor Yellow
        exit 1
    }
}

# Check if service already exists
$existingService = Get-Service -Name $serviceName -ErrorAction SilentlyContinue

if ($existingService) {
    Write-Host "Service '$serviceName' already exists" -ForegroundColor Yellow
    $response = Read-Host "Do you want to remove and reinstall? (Y/N)"
    
    if ($response -eq 'Y' -or $response -eq 'y') {
        Write-Host "Stopping service..." -ForegroundColor Yellow
        Stop-Service -Name $serviceName -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2
        
        Write-Host "Removing service..." -ForegroundColor Yellow
        & $nssmPath remove $serviceName confirm
        Start-Sleep -Seconds 2
    } else {
        Write-Host "Installation cancelled" -ForegroundColor Yellow
        exit 0
    }
}

# Install service
Write-Host ""
Write-Host "Installing service..." -ForegroundColor Green

& $nssmPath install $serviceName $pythonExe $scriptPath

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install service" -ForegroundColor Red
    exit 1
}

# Configure service
Write-Host "Configuring service..." -ForegroundColor Green

# Set working directory
& $nssmPath set $serviceName AppDirectory $botPath

# Set display name and description
& $nssmPath set $serviceName DisplayName "AI Research Bot"
& $nssmPath set $serviceName Description "Automated AI research bot that monitors papers and news, with Discord integration"

# Set startup type to automatic
& $nssmPath set $serviceName Start SERVICE_AUTO_START

# Set output files
$logPath = Join-Path $botPath "logs"
if (-not (Test-Path $logPath)) {
    New-Item -Path $logPath -ItemType Directory -Force | Out-Null
}

& $nssmPath set $serviceName AppStdout (Join-Path $logPath "service-out.log")
& $nssmPath set $serviceName AppStderr (Join-Path $logPath "service-error.log")

# Enable log file rotation
& $nssmPath set $serviceName AppRotateFiles 1
& $nssmPath set $serviceName AppRotateOnline 1
& $nssmPath set $serviceName AppRotateSeconds 86400  # Rotate daily
& $nssmPath set $serviceName AppRotateBytes 10485760  # 10MB

# Set process priority
& $nssmPath set $serviceName AppPriority NORMAL_PRIORITY_CLASS

# Configure auto-restart behavior
Write-Host "Configuring auto-restart..." -ForegroundColor Green

# Exit actions
& $nssmPath set $serviceName AppExit Default Restart  # Restart on any exit
& $nssmPath set $serviceName AppExit 0 Restart  # Restart even on clean exit

# Throttle - prevent rapid restart loops
& $nssmPath set $serviceName AppThrottle 5000  # Wait 5 seconds before restart

# Set restart delay
& $nssmPath set $serviceName AppRestartDelay 5000  # 5 seconds

# Set environment variables
Write-Host "Setting environment variables..." -ForegroundColor Green
& $nssmPath set $serviceName AppEnvironmentExtra PYTHONUNBUFFERED=1

# Configure process management
& $nssmPath set $serviceName AppStopMethodSkip 0
& $nssmPath set $serviceName AppStopMethodConsole 1500  # Try console stop for 1.5s
& $nssmPath set $serviceName AppStopMethodWindow 1500   # Try window stop for 1.5s  
& $nssmPath set $serviceName AppStopMethodThreads 1500  # Try thread stop for 1.5s
& $nssmPath set $serviceName AppKillProcessTree 1       # Kill child processes

# Start service
Write-Host ""
Write-Host "Starting service..." -ForegroundColor Green

Start-Service -Name $serviceName

# Wait a moment for service to start
Start-Sleep -Seconds 3

# Check service status
$service = Get-Service -Name $serviceName

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Service Name: $serviceName" -ForegroundColor Cyan
Write-Host "Status: $($service.Status)" -ForegroundColor $(if ($service.Status -eq 'Running') { 'Green' } else { 'Yellow' })
Write-Host "Startup Type: Automatic" -ForegroundColor Cyan
Write-Host ""
Write-Host "The bot will now:" -ForegroundColor White
Write-Host "  • Start automatically when Windows boots" -ForegroundColor Gray
Write-Host "  • Restart automatically if it crashes" -ForegroundColor Gray
Write-Host "  • Stay online 24/7" -ForegroundColor Gray
Write-Host ""
Write-Host "Useful Commands:" -ForegroundColor Yellow
Write-Host "  • View status:  Get-Service $serviceName" -ForegroundColor Gray
Write-Host "  • Stop:         Stop-Service $serviceName" -ForegroundColor Gray
Write-Host "  • Start:        Start-Service $serviceName" -ForegroundColor Gray
Write-Host "  • Restart:      Restart-Service $serviceName" -ForegroundColor Gray
Write-Host "  • View logs:    Get-Content logs\service-out.log -Tail 50 -Wait" -ForegroundColor Gray
Write-Host "  • Uninstall:    .\uninstall_service.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "Log files location: $logPath" -ForegroundColor Cyan
Write-Host ""

if ($service.Status -eq 'Running') {
    Write-Host "✓ Bot is now running as a Windows Service!" -ForegroundColor Green
} else {
    Write-Host "⚠ Service installed but not running. Check logs for details." -ForegroundColor Yellow
    Write-Host "Run: Get-Content logs\service-error.log -Tail 20" -ForegroundColor Gray
}

Write-Host ""
Read-Host "Press Enter to exit"
