# 🚀 Keep-Alive Solutions - วิธีรันบอทให้ Online ตลอด 24/7

> **ปัญหา**: บอท Discord ไป offline เมื่อไม่มีการใช้งานนานๆ  
> **สาเหตุ**: Process หยุดทำงาน, Computer sleep, Hosting timeout, Network disconnect

มี **4 วิธีหลัก** ในการแก้ปัญหา ไม่จำเป็นต้องเปลี่ยนเป็น Next.js!

---

## 🎯 วิธีที่ 1: PM2 Process Manager (แนะนำ!)

PM2 สามารถใช้กับ Python ได้เลย มีฟีเจอร์:
- ✅ Auto-restart เมื่อ crash
- ✅ Keep process alive 24/7
- ✅ Monitor memory usage
- ✅ Auto-start on system boot
- ✅ Log management

### การติดตั้ง:

```bash
# 1. ติดตั้ง Node.js (ถ้ายังไม่มี)
# Download จาก: https://nodejs.org/

# 2. ติดตั้ง PM2
npm install -g pm2

# 3. รัน bot ด้วย PM2
pm2 start ecosystem.config.js

# 4. ตั้งให้ start ตอน boot
pm2 startup
pm2 save
```

### คำสั่ง PM2 ที่ใช้บ่อย:

```bash
# ดู status
pm2 status
pm2 list

# ดู logs
pm2 logs bot
pm2 logs bot --lines 100

# Monitor real-time
pm2 monit

# Restart
pm2 restart bot

# Stop
pm2 stop bot

# Delete process
pm2 delete bot

# Reload config
pm2 reload ecosystem.config.js
```

### ข้อดี:
- ✅ ใช้งานง่าย
- ✅ Auto-restart ทันที
- ✅ Support ทั้ง Windows, Linux, macOS
- ✅ มี Web dashboard (PM2 Plus)

### ข้อเสีย:
- ⚠️ ต้องติดตั้ง Node.js

---

## 🎯 วิธีที่ 2: Windows Service (สำหรับ Windows)

ติดตั้งบอทเป็น Windows Service โดยใช้ NSSM (Non-Sucking Service Manager)

### การติดตั้ง:

```powershell
# Run PowerShell as Administrator
.\install_service_enhanced.ps1
```

Script จะทำให้:
- ✅ Auto-start เมื่อ Windows boot
- ✅ Auto-restart เมื่อ crash
- ✅ รันใน background
- ✅ Automatic log rotation

### คำสั่งจัดการ Service:

```powershell
# ดู status
Get-Service AIResearchBot

# Start
Start-Service AIResearchBot

# Stop
Stop-Service AIResearchBot

# Restart
Restart-Service AIResearchBot

# ดู logs
Get-Content logs\service-out.log -Tail 50 -Wait

# Uninstall
.\uninstall_service.ps1
```

### ข้อดี:
- ✅ Native Windows solution
- ✅ รันแม้ไม่ login Windows
- ✅ Very stable
- ✅ ไม่ต้องติดตั้งเพิ่ม (มี NSSM ใน script)

### ข้อเสีย:
- ⚠️ Windows only
- ⚠️ ต้อง Admin rights

---

## 🎯 วิธีที่ 3: Docker with Restart Policy

ใช้ Docker container พร้อม `restart: always` policy

### การติดตั้ง:

```bash
# 1. ติดตั้ง Docker Desktop
# Download: https://www.docker.com/products/docker-desktop/

# 2. Build และ run
docker-compose up -d

# 3. ดู status
docker-compose ps

# 4. ดู logs
docker-compose logs -f bot
```

### Docker compose มี:
- ✅ Auto-restart always
- ✅ Health check ทุก 60 วินาที
- ✅ Resource limits (512MB RAM)
- ✅ Log rotation
- ✅ Isolated environment

### คำสั่ง Docker:

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Restart
docker-compose restart

# Logs
docker-compose logs -f bot
docker-compose logs --tail=100 bot

# Rebuild
docker-compose up -d --build

# ดู resource usage
docker stats
```

### ข้อดี:
- ✅ Portable (ใช้ได้ทุก OS)
- ✅ Isolated environment
- ✅ Easy deployment
- ✅ Resource control

### ข้อเสีย:
- ⚠️ ต้องติดตั้ง Docker
- ⚠️ ใช้ resource มากกว่า

---

## 🎯 วิธีที่ 4: Cloud Hosting (Production)

Deploy บน cloud platform ที่มี always-on service

### 4.1 Render (Free tier)
```yaml
# render.yaml มีอยู่แล้ว
# Features:
- ✅ Free tier available
- ✅ Auto-deploy from GitHub
- ✅ Auto-restart
- ⚠️ Free tier sleeps after 15 min inactivity
- ✅ มี keep_alive.py แก้ไข
```

### 4.2 Railway.app
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

**Features:**
- ✅ $5 free credit/month
- ✅ Always online
- ✅ Auto-deploy from GitHub
- ✅ Easy setup

### 4.3 Fly.io
```bash
# Install flyctl
# Windows: iwr https://fly.io/install.ps1 -useb | iex

# Login
fly auth login

# Deploy
fly launch
```

**Features:**
- ✅ Free tier: 3 VMs
- ✅ Always online
- ✅ Global deployment

### 4.4 DigitalOcean / AWS / Azure
**Production-grade:**
- ✅ 100% uptime
- ✅ Scalable
- ✅ Full control
- ⚠️ Paid (starting ~$5/month)

---

## 🏆 แนะนำตามกรณีใช้งาน

### 1. รัน Local บน Windows 💻
**แนะนำ: Windows Service**
```powershell
.\install_service_enhanced.ps1
```
- เหมาะกับ PC/Laptop ที่เปิดตลอด
- รันแม้ไม่ login
- ไม่ต้องติดตั้งเพิ่ม

### 2. รัน Local ทุก OS (Windows/Mac/Linux) 🌍
**แนะนำ: PM2**
```bash
npm install -g pm2
pm2 start ecosystem.config.js
pm2 startup
pm2 save
```
- Cross-platform
- Easy management
- Web dashboard

### 3. Deploy Production 🚀
**แนะนำ: Railway.app หรือ Fly.io**
```bash
# Railway
railway up

# Or Fly.io  
fly launch
```
- Always online
- Auto-deploy
- Low cost

### 4. Development / Testing 🧪
**แนะนำ: Docker**
```bash
docker-compose up -d
```
- Clean environment
- Easy cleanup

---

## 📊 เปรียบเทียบ

| วิธี | Setup | ราคา | Uptime | ความยาก | Cross-Platform |
|------|-------|------|--------|---------|----------------|
| PM2 | ง่าย | Free | 99%* | ⭐⭐ | ✅ |
| Windows Service | ง่าย | Free | 99%* | ⭐⭐ | ❌ (Windows only) |
| Docker | กลาง | Free | 99%* | ⭐⭐⭐ | ✅ |
| Railway.app | ง่ายมาก | $5/mo | 99.9% | ⭐ | ✅ |
| Fly.io | ง่าย | Free tier | 99.9% | ⭐⭐ | ✅ |
| VPS (DO/AWS) | ยาก | $5-10/mo | 99.9% | ⭐⭐⭐⭐ | ✅ |

\* ขึ้นกับว่า computer เปิดอยู่หรือไม่

---

## 🔧 Troubleshooting

### บอทยังไป offline อยู่:

1. **ตรวจสอบ Discord Developer Portal**
   - เปิด MESSAGE CONTENT INTENT ✅
   - เปิด SERVER MEMBERS INTENT ✅
   - เปิด PRESENCE INTENT (optional) ✅

2. **ตรวจสอบ logs**
   ```bash
   # PM2
   pm2 logs bot
   
   # Windows Service
   Get-Content logs\service-error.log -Tail 50
   
   # Docker
   docker-compose logs -f bot
   ```

3. **ตรวจสอบ network**
   - Firewall block WebSocket?
   - Port 443 open?
   - Internet stable?

4. **ตรวจสอบ code**
   - Keep-alive loop ทำงานหรือไม่?
   - Check `logs/bot.log` สำหรับ keep-alive pings

5. **ลด keep-alive interval**
   ใน `.env`:
   ```
   DISCORD_KEEPALIVE_INTERVAL=180  # 3 minutes
   ```

### High latency:
```env
DISCORD_HEARTBEAT_TIMEOUT=90.0
```

### Memory leak:
```bash
# PM2 auto-restart on high memory
pm2 restart bot

# Check memory
pm2 monit
```

---

## 💡 Best Practices

### 1. ใช้ร่วมกัน
```bash
# Local: PM2
pm2 start ecosystem.config.js

# Production: Railway + PM2
railway up
```

### 2. Monitoring
```bash
# PM2 Plus (free)
pm2 link <secret> <public>

# Or ใช้ Discord webhook แจ้งเตือน
```

### 3. Backup logs
```bash
# Auto-rotate logs
pm2 install pm2-logrotate
pm2 set pm2-logrotate:max_size 10M
```

### 4. Health checks
```python
# ใช้ /health endpoint
curl http://localhost:8000/health
```

---

## 📝 สรุป

**ไม่จำเป็นต้องเปลี่ยนเป็น Next.js!** 

เลือกวิธีที่เหมาะกับคุณ:
- 🏠 **Local Windows**: `install_service_enhanced.ps1`
- 💻 **Local Any OS**: `pm2 start ecosystem.config.js`
- 🐳 **Docker**: `docker-compose up -d`
- ☁️ **Cloud**: Railway.app หรือ Fly.io

ทุกวิธีจะทำให้บอท **online ตลอด 24/7** โดยไม่ต้องเปลี่ยนโค้ด! 🎉

---

## 🆘 ต้องการความช่วยเหลือ?

1. ดู logs: `logs/bot.log`
2. Check Discord status: https://discordstatus.com
3. Test connection: `python test_bot_fix.py`
4. Review: `BOT_OFFLINE_FIX.md`

---

**Updated:** February 14, 2026  
**Version:** 2.0
