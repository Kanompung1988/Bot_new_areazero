# 🚀 Render Setup - Visual Guide

## ขั้นตอนที่ 1: เตรียม Code

```
📁 Project
├── 📄 render.yaml ✅ (มีแล้ว)
├── 📄 Dockerfile ✅ (มีแล้ว)
├── 📄 requirements.txt ✅ (มีแล้ว)
└── 📄 .env ⚠️ (อย่า commit!)
```

## ขั้นตอนที่ 2: Push ไป GitHub

```powershell
# รันคำสั่งนี้
.\deploy_to_render.ps1
```

หรือ manual:
```bash
git add .
git commit -m "Deploy to Render"
git push
```

## ขั้นตอนที่ 3: Setup Render

### 3.1 สร้าง Web Service

```
1. ไปที่: https://dashboard.render.com/
2. คลิก: [New +] → [Web Service]
3. Connect GitHub repository
4. เลือก: Bot_new_areazero_R&D
5. คลิก: [Connect]
```

### 3.2 Basic Settings

```
┌─────────────────────────────────────┐
│ Name: ai-research-bot               │
│ Region: Singapore                   │
│ Branch: main                        │
│ Environment: Docker                 │
└─────────────────────────────────────┘
```

### 3.3 Environment Variables

**คลิก "Advanced" → เพิ่มตัวแปรเหล่านี้:**

```
🔐 Secret (ห้ามแชร์):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DISCORD_TOKEN=MTIzNDU2Nzg5MC4... ⚠️
GEMINI_API_KEY=AIzaSyC...        ⚠️
DISCORD_CHANNEL_ID=1234567890    ⚠️

⚙️ Configuration:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GEMINI_MODEL=gemini-2.5-flash
DAILY_RUN_TIME=08:00
TIMEZONE=Asia/Bangkok
DISCORD_HEARTBEAT_TIMEOUT=60.0
DISCORD_KEEPALIVE_INTERVAL=300
```

### 3.4 Deploy!

```
[Create Web Service] ← คลิกปุ่มนี้
```

## ขั้นตอนที่ 4: รอ Build (3-5 นาที)

```
Building... ⏳
┌────────────────────────────────────┐
│ Step 1/8 : FROM python:3.11-slim  │
│ Step 2/8 : WORKDIR /app            │
│ Step 3/8 : COPY requirements.txt   │
│ Step 4/8 : RUN pip install...      │
│ ...                                │
│ ✅ Build successful!                │
└────────────────────────────────────┘

Deploying... 🚀
┌────────────────────────────────────┐
│ Starting service...                │
│ ✅ Service started                  │
│ ✅ Health check passed              │
└────────────────────────────────────┘
```

## ขั้นตอนที่ 5: ตรวจสอบ

### Check 1: Logs
```
Render Dashboard → Logs tab

ควรเห็น:
✅ Starting Discord bot...
✅ ResearchBot: Bot is ready!
✅ Logged in as: YourBot (ID: 123...)
✅ Connected to 1 guild(s)
✅ Keep-alive loop started
```

### Check 2: Health Endpoint
```
เปิด browser:
https://ai-research-bot.onrender.com/health

ควรเห็น:
{
  "status": "healthy",
  "bot": {
    "ready": true,
    "connected": true,
    "guilds": 1,
    "latency": 45
  }
}
```

### Check 3: Discord
```
Discord Server → Members list

Bot status:
🟢 Online ← ควรเป็นสีเขียว!
```

## ขั้นตอนที่ 6: Keep-Alive (สำคัญ! 🔴)

### Setup UptimeRobot

```
1. ไปที่: https://uptimerobot.com/
2. Sign up (ฟรี)
3. Dashboard → [Add New Monitor]

Settings:
┌─────────────────────────────────────┐
│ Monitor Type: HTTP(s)               │
│ Friendly Name: AI Research Bot      │
│ URL: https://YOUR-APP.onrender.com  │
│      /health                        │
│ Monitoring Interval: 5 minutes      │
│                                     │
│ [Create Monitor] ← คลิก             │
└─────────────────────────────────────┘
```

### ผลลัพธ์:

```
Before UptimeRobot:
🟢 Online → 🔴 Offline (after 15 min)

After UptimeRobot:
🟢 Online → 🟢 Online (24/7) ✅
```

## 📊 Status Dashboard

```
┌──────────────────────────────────────────┐
│ Render Dashboard                         │
├──────────────────────────────────────────┤
│ Service: ai-research-bot          🟢 Live│
│ Region: Singapore                        │
│ Last Deploy: 2 minutes ago               │
│                                          │
│ [Logs] [Metrics] [Events] [Settings]    │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│ UptimeRobot Dashboard                    │
├──────────────────────────────────────────┤
│ Monitor: AI Research Bot         🟢 Up   │
│ Uptime: 99.99%                           │
│ Response Time: 45 ms                     │
│ Last Check: 1 minute ago                 │
└──────────────────────────────────────────┘
```

## 🎯 Quick Commands

```bash
# Update & Deploy
git add .
git commit -m "Update features"
git push  # Auto-deploy ใน Render!

# View Logs
# ไปที่ Render Dashboard → Logs

# Restart Service
# Render Dashboard → Manual Deploy → Deploy

# Check Status
curl https://YOUR-APP.onrender.com/health
```

## 🆘 Common Issues

### ❌ Bot Offline

```
Problem: Bot แสดง offline ใน Discord

Solutions:
✅ Check DISCORD_TOKEN in Render
✅ Check Discord Intents (Developer Portal)
✅ View logs in Render
✅ Manual Deploy in Render
```

### ❌ Build Failed

```
Problem: Build ล้มเหลว

Solutions:
✅ Check requirements.txt
✅ Check Dockerfile syntax
✅ View build logs
✅ Test locally: docker build -t bot .
```

### ❌ Health Check Failed

```
Problem: /health endpoint ไม่ตอบ

Solutions:
✅ Check api.py running
✅ Check port 8000
✅ View logs for uvicorn
```

## ✅ Success Checklist

เมื่อ deploy สำเร็จ คุณจะเห็น:

- [x] ✅ Build completed
- [x] ✅ Service running
- [x] ✅ Health check passed
- [x] ✅ Bot online in Discord (🟢)
- [x] ✅ UptimeRobot monitoring
- [x] ✅ `/health` endpoint responds
- [x] ✅ Discord commands work (!ping)
- [x] ✅ Logs show keep-alive pings

## 🎉 Done!

```
╔══════════════════════════════════════╗
║   🎊 Bot deployed successfully! 🎊   ║
║                                      ║
║   Your bot is now online 24/7!      ║
║                                      ║
║   URL: https://YOUR-APP.onrender.com ║
╚══════════════════════════════════════╝
```

---

**Need help?** Read full guide: [RENDER_SETUP.md](RENDER_SETUP.md)

**Last Updated:** February 14, 2026
