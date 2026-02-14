# 🚀 Quick Reference - Bot Commands

## 🎯 เริ่มต้นใช้งาน (เลือก 1 วิธี)

### วิธีที่ 1: PM2 ⚡ (แนะนำ)
```powershell
.\start_with_pm2.ps1
```

### วิธีที่ 2: Windows Service 🪟
```powershell
# Run as Admin
.\install_service_enhanced.ps1
```

### วิธีที่ 3: Docker 🐳
```bash
docker-compose up -d
```

---

## 📋 PM2 Commands

```bash
# Status
pm2 status
pm2 list

# Logs
pm2 logs bot
pm2 logs bot --lines 100
pm2 logs --err          # Error logs only

# Control
pm2 restart bot
pm2 stop bot
pm2 start bot
pm2 delete bot

# Monitor
pm2 monit               # Real-time monitor
pm2 plus                # Web dashboard

# Auto-start
pm2 startup             # Setup auto-start
pm2 save               # Save current state
pm2 resurrect          # Restore saved state

# Other
pm2 flush bot          # Clear logs
pm2 reset bot          # Reset restarts counter
```

---

## 🪟 Windows Service Commands

```powershell
# Status
Get-Service AIResearchBot
Get-Service AIResearchBot | Select-Object *

# Control
Start-Service AIResearchBot
Stop-Service AIResearchBot
Restart-Service AIResearchBot

# Logs
Get-Content logs\service-out.log -Tail 50 -Wait
Get-Content logs\service-error.log -Tail 50

# Uninstall
.\uninstall_service.ps1
```

---

## 🐳 Docker Commands

```bash
# Status
docker-compose ps
docker ps

# Logs
docker-compose logs -f bot
docker-compose logs --tail=100 bot

# Control
docker-compose up -d
docker-compose down
docker-compose restart bot
docker-compose stop bot

# Rebuild
docker-compose up -d --build

# Monitor
docker stats
docker exec -it ai-research-bot /bin/bash

# Cleanup
docker-compose down -v      # Remove volumes
docker system prune -a      # Clean all
```

---

## 🤖 Discord Bot Commands

ใช้ใน Discord server:

```
!help              - แสดงคำสั่งทั้งหมด
!research [days]   - รัน research (default: 7 days)
!status            - แสดงสถานะบอท
!test              - ทดสอบระบบ
!config            - แสดง configuration
!ping              - ตรวจสอบ latency
```

---

## 🔧 Troubleshooting Commands

```powershell
# Pre-flight check
.\preflight_check.ps1

# Health check
python check_bot_health.py

# Test connection
python -c "import discord; print(discord.__version__)"

# Check Python packages
pip list | grep discord
pip list | grep fastapi

# View logs
Get-Content logs\bot.log -Tail 50 -Wait
Get-Content logs\pm2-error.log -Tail 50

# Test Gemini
python -c "from tools.gemini_tool import get_gemini_api; print(get_gemini_api().generate_content('test'))"
```

---

## 🌐 API Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Trigger research
curl -X POST http://localhost:8000/api/research \
  -H "Content-Type: application/json" \
  -d '{"days_back": 7}'

# Get status
curl http://localhost:8000/api/status

# Root
curl http://localhost:8000/
```

---

## 📊 Monitoring

```powershell
# CPU/Memory usage (PM2)
pm2 monit

# Windows Task Manager
tasklist | findstr python

# Docker stats
docker stats ai-research-bot

# Network connections
netstat -ano | findstr :8000
```

---

## 🔐 Environment Variables

```env
# Discord
DISCORD_TOKEN=your_token_here
DISCORD_CHANNEL_ID=123456789
DISCORD_HEARTBEAT_TIMEOUT=60.0
DISCORD_KEEPALIVE_INTERVAL=300

# Gemini
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash

# Schedule
DAILY_RUN_TIME=08:00
TIMEZONE=Asia/Bangkok
```

---

## 🆘 Common Issues

### Bot offline
```powershell
# Check logs
pm2 logs bot --err

# Restart
pm2 restart bot

# Health check
python check_bot_health.py
```

### High memory
```bash
# PM2 auto-restart on 500MB
pm2 restart bot
```

### Port in use
```powershell
# Find process on port 8000
netstat -ano | findstr :8000

# Kill process
taskkill /F /PID <pid>
```

### Discord intents
- Go to: https://discord.com/developers/applications
- Enable: MESSAGE CONTENT INTENT
- Enable: SERVER MEMBERS INTENT

---

## 📚 Documentation

- [KEEP_ALIVE_SOLUTIONS.md](KEEP_ALIVE_SOLUTIONS.md) - 24/7 deployment methods
- [BOT_OFFLINE_FIX.md](BOT_OFFLINE_FIX.md) - Fix offline issues
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment
- [DISCORD_SETUP.md](DISCORD_SETUP.md) - Discord setup guide

---

## 💡 Pro Tips

```bash
# Auto-update bot on git push (PM2)
pm2 start ecosystem.config.js --watch

# Export PM2 config
pm2 save
pm2 dump

# PM2 with cron restart (3 AM daily)
# Edit ecosystem.config.js: cron_restart: '0 3 * * *'

# View all PM2 processes
pm2 ls

# Filter PM2 logs
pm2 logs --lines 1000 | grep "ERROR"
```

---

**Last Updated:** February 14, 2026
