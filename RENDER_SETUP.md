# 🚀 Render Deployment Guide - คู่มือฉบับสมบูรณ์

> Deploy Discord Bot ไปที่ Render.com ให้ online 24/7 ฟรี!

---

## ⚡ Quick Start (5 นาที)

### 1️⃣ Push Code ไป GitHub

```powershell
# ใน PowerShell
cd "C:\Users\User\OneDrive - Mahidol University\Desktop\Work Areazero\Bot_new_areazero_R&D"

git add .
git commit -m "Deploy to Render with keep-alive fix"
git push
```

### 2️⃣ Connect กับ Render

1. ไปที่: **https://dashboard.render.com/**
2. Login/Sign up (ฟรี)
3. คลิก **New** → **Web Service**
4. เชื่อมต่อ GitHub → เลือก repository ของคุณ
5. คลิก **Connect**

---

## 🔧 Render Configuration

### Basic Settings:

```
Name: ai-research-bot
Region: Singapore (ใกล้ Thailand ที่สุด)
Branch: main
Root Directory: (leave blank)
```

### Build & Deploy Settings:

```
Environment: Docker
Dockerfile Path: ./Dockerfile
Docker Command: (ใช้ default จาก Dockerfile)
```

### Health Check:

```
Health Check Path: /health
```

### Auto Deploy:

```
☑️ Auto-Deploy: Yes (deploy อัตโนมัติเมื่อ push)
```

---

## 🔐 Environment Variables (สำคัญมาก!)

กดที่ **Environment** tab แล้วเพิ่มตัวแปรเหล่านี้:

### Discord Configuration:

| Key | Value | Note |
|-----|-------|------|
| `DISCORD_TOKEN` | `YOUR_TOKEN` | ⚠️ จาก Discord Developer Portal |
| `DISCORD_CHANNEL_ID` | `YOUR_CHANNEL_ID` | ⚠️ Right-click channel → Copy ID |
| `DISCORD_COMMAND_CHANNEL_ID` | `YOUR_CHANNEL_ID` | Optional - ถ้าต้องการแยก channel |
| `DISCORD_APPLICATION_ID` | `YOUR_APP_ID` | Optional |
| `DISCORD_PUBLIC_KEY` | `YOUR_KEY` | Optional |

### Gemini API:

| Key | Value | Note |
|-----|-------|------|
| `GEMINI_API_KEY` | `YOUR_KEY` | ⚠️ จาก https://ai.google.dev/ |
| `GEMINI_MODEL` | `gemini-2.5-flash` | หรือ model ที่ต้องการ |

### Bot Configuration:

| Key | Value | Note |
|-----|-------|------|
| `DAILY_RUN_TIME` | `08:00` | เวลารัน auto (24hr format) |
| `TIMEZONE` | `Asia/Bangkok` | |
| `MAX_NEWS_ARTICLES` | `10` | |
| `MAX_PAPERS_TO_ANALYZE` | `100` | |
| `SELECTED_PAPERS_COUNT` | `10` | |
| `DEFAULT_DAYS_BACK` | `7` | |
| `AI_TOPICS` | `LLM,Computer Vision,NLP,Machine Learning` | คั่นด้วย comma |

### Keep-Alive Configuration (สำคัญ!):

| Key | Value | Note |
|-----|-------|------|
| `DISCORD_HEARTBEAT_TIMEOUT` | `60.0` | WebSocket timeout |
| `DISCORD_KEEPALIVE_INTERVAL` | `300` | Update presence ทุก 5 นาที |

---

## 📋 วิธีหา Discord Token & IDs

### Discord Token:
1. ไปที่: https://discord.com/developers/applications
2. เลือก application ของคุณ
3. ไปที่ **Bot** tab
4. คลิก **Reset Token** → Copy token
5. ⚠️ **อย่าแชร์** token นี้กับใครเลย!

### Channel ID:
1. เปิด Discord
2. ไปที่ **User Settings** → **Advanced**
3. เปิด **Developer Mode**
4. Right-click ที่ channel → **Copy ID**

### Application ID:
1. ไปที่: https://discord.com/developers/applications
2. เลือก application
3. **General Information** → คัดลอก **Application ID**

---

## 🚀 Deploy!

1. กรอก Environment Variables ครบทุกตัวที่จำเป็น
2. คลิก **Create Web Service**
3. รอ build ~3-5 นาที
4. ดู logs ว่ามี: `✅ Bot is ready!`

---

## 🔄 Keep-Alive Setup (ป้องกัน Sleep)

**ปัญหา:** Render Free tier จะ sleep หลัง 15 นาที ไม่มี traffic

**วิธีแก้:** ใช้ UptimeRobot ping ทุก 5 นาที (ฟรี!)

### ขั้นตอน:

1. **สมัคร UptimeRobot:**
   - ไปที่: https://uptimerobot.com/
   - Sign up (ฟรี)

2. **สร้าง Monitor:**
   - คลิก **Add New Monitor**
   - Monitor Type: **HTTP(s)**
   - Friendly Name: `AI Research Bot`
   - URL: `https://YOUR-APP-NAME.onrender.com/health`
   - Monitoring Interval: **5 minutes**
   - คลิก **Create Monitor**

3. **ตั้ง Alert (Optional):**
   - Alert Contacts: เพิ่ม email
   - จะได้รับแจ้งเตือนถ้า bot down

**ผลลัพธ์:**
- ✅ Bot จะไม่ sleep
- ✅ Online 24/7
- ✅ ได้รับแจ้งเตือนถ้ามีปัญหา

---

## ✅ ตรวจสอบว่า Deploy สำเร็จ

### 1. ตรวจสอบ Render Logs:

```
Logs ควรแสดง:
✅ Starting Discord bot...
✅ ResearchBot: Bot is ready!
✅ Bot Name: Your Bot Name
✅ Connected to X guild(s)
✅ Keep-alive loop started
```

### 2. ตรวจสอบ Health Endpoint:

เปิด browser ไปที่:
```
https://YOUR-APP-NAME.onrender.com/health
```

ควรเห็น:
```json
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

### 3. ตรวจสอบ Discord:

- Bot ควร **online** (สีเขียว)
- ลองใช้คำสั่ง: `!ping` หรือ `!status`

---

## 🎯 Best Practices

### 1. ใช้ Environment Variables แทน Hardcode
```python
# ❌ แบบผิด
token = "MTIzNDU2..."

# ✅ แบบถูก  
token = os.getenv('DISCORD_TOKEN')
```

### 2. ตั้ง Health Check
- Render จะตรวจสอบ `/health` ทุก 60 วินาที
- ถ้า unhealthy จะ restart อัตโนมัติ

### 3. Monitor Logs
- เข้า Render Dashboard → Logs
- ดู keep-alive pings ทุก 5 นาที
- ดู errors/warnings

### 4. Deploy Strategy
```yaml
# render.yaml มีอยู่แล้ว
autoDeploy: true    # Auto-deploy on git push
```

---

## 🛠️ Troubleshooting

### ❌ Bot Offline หลัง Deploy

**สาเหตุ 1:** Token ไม่ถูกต้อง
```
Solution:
1. ตรวจสอบ DISCORD_TOKEN ใน Environment Variables
2. Reset token ใน Discord Developer Portal
3. Update ใน Render
4. Manual Deploy
```

**สาเหตุ 2:** Intents ไม่เปิด
```
Solution:
1. ไปที่ Discord Developer Portal
2. Bot tab → Privileged Gateway Intents
3. เปิด:
   ✅ MESSAGE CONTENT INTENT
   ✅ SERVER MEMBERS INTENT
4. Save Changes
```

**สาเหตุ 3:** Build Failed
```
Solution:
1. ดู build logs ใน Render
2. ตรวจสอบ requirements.txt
3. ตรวจสอบ Dockerfile
4. ลอง build local: docker build -t bot .
```

### ❌ Bot Sleep หลัง 15 นาที

```
Solution:
✅ ตั้ง UptimeRobot (ดูด้านบน)
✅ Keep-alive loop ใน bot (มีอยู่แล้ว)
✅ Health check endpoint (มีอยู่แล้ว)
```

### ❌ Health Check Failed

```
Solution:
1. ตรวจสอบว่า api.py รัน port 8000
2. ตรวจสอบว่ามี /health endpoint
3. ดู logs: "Uvicorn running on http://0.0.0.0:8000"
```

### ❌ Memory Limit Exceeded

```
Solution:
1. Render Free: 512MB RAM
2. ถ้าเกิน → upgrade plan
3. หรือ optimize code:
   - ลด MAX_PAPERS_TO_ANALYZE
   - Clear cache บ่อยขึ้น
```

### ❌ High Latency

```
Solution:
1. เปลี่ยน Region: Singapore (ใกล้ที่สุด)
2. เพิ่ม DISCORD_HEARTBEAT_TIMEOUT=90.0
```

---

## 📊 Monitoring & Logs

### Render Dashboard:

```
Logs tab:
- ดู real-time logs
- Filter by severity
- Download logs

Metrics tab:
- CPU usage
- Memory usage
- Response time
```

### Discord Logs:

```python
# Bot จะ log ทุก 5 นาที
[DEBUG] ResearchBot: Keep-alive ping - Latency: 45ms, Guilds: 1
```

### UptimeRobot:

```
Dashboard:
- Uptime percentage
- Response time chart
- Downtime alerts
```

---

## 🔄 Update & Maintenance

### Auto-Deploy:

```bash
# แก้โค้ด แล้ว push
git add .
git commit -m "Update bot features"
git push

# Render จะ auto-deploy (ถ้าเปิด autoDeploy)
```

### Manual Deploy:

```
1. ไปที่ Render Dashboard
2. เลือก service
3. คลิก "Manual Deploy"
4. เลือก branch: main
5. คลิก "Deploy"
```

### Rollback:

```
1. ไปที่ Render Dashboard
2. เลือก service
3. Deploys tab
4. หา deploy ที่ต้องการ rollback
5. คลิก "..." → "Redeploy"
```

---

## 💰 Pricing

### Free Tier:

```
✅ 750 hours/month (enough for 24/7)
✅ 512 MB RAM
✅ 0.1 CPU
✅ Auto-sleep after 15 min (แก้ด้วย UptimeRobot)
✅ Custom domain
✅ Auto SSL
```

### Paid Plans:

```
Starter: $7/month
- Always on (no sleep)
- 512 MB RAM
- 0.5 CPU

Standard: $25/month  
- 2 GB RAM
- 1 CPU
```

**Recommendation:** Free tier + UptimeRobot = **ฟรี 100%** และใช้งานได้ดี!

---

## 📚 Resources

### Documentation:
- Render Docs: https://render.com/docs
- Discord.py Docs: https://discordpy.readthedocs.io/
- UptimeRobot: https://uptimerobot.com/

### Support:
- Render Community: https://community.render.com/
- Discord: Server ของคุณเอง

### Related Files:
- [KEEP_ALIVE_SOLUTIONS.md](KEEP_ALIVE_SOLUTIONS.md) - ทุกวิธีรัน 24/7
- [BOT_OFFLINE_FIX.md](BOT_OFFLINE_FIX.md) - แก้ปัญหา offline
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - คำสั่งด่วน

---

## 🎉 Summary Checklist

Deploy ใน Render สำเร็จ ต้องมีทั้งหมด:

- [ ] Code push ขึ้น GitHub
- [ ] Render service สร้างแล้ว
- [ ] Environment Variables ครบ (DISCORD_TOKEN, GEMINI_API_KEY)
- [ ] Discord Intents เปิดแล้ว (MESSAGE CONTENT, SERVER MEMBERS)
- [ ] Build สำเร็จ (ดู logs)
- [ ] Health check pass (เข้า /health ได้)
- [ ] Bot online ใน Discord (สีเขียว)
- [ ] UptimeRobot monitor ตั้งแล้ว
- [ ] ทดสอบคำสั่ง (!ping, !status) ใช้งานได้

ถ้าครบทุกข้อ = **🎊 Deploy สำเร็จ! Bot จะ online 24/7**

---

**Updated:** February 14, 2026  
**Version:** 2.0
