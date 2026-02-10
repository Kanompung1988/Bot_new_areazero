# 🚀 Deployment Guide

## การ Deploy บน Render

### ขั้นตอนที่ 1: Push Code ขึ้น GitHub

```bash
git init
git add .
git commit -m "Initial commit: AI Research Bot with Discord integration"
git branch -M main
git remote add origin https://github.com/Kanompung1988/Bot_new_areazero.git
git push -u origin main
```

### ขั้นตอนที่ 2: ตั้งค่า Render

1. ไปที่ [Render Dashboard](https://dashboard.render.com/)
2. คลิก **New** → **Web Service**
3. เชื่อมต่อกับ GitHub repository: `Kanompung1988/Bot_new_areazero`
4. เลือก branch: `main`

### ขั้นตอนที่ 3: กำหนด Settings

**Basic Settings:**
- **Name**: `ai-research-bot`
- **Region**: Singapore (ใกล้ที่สุด)
- **Branch**: `main`
- **Runtime**: Docker

**Environment Variables (⚠️ สำคัญ):**

ไปที่ **Environment** tab และเพิ่ม (ใช้ค่าจริงจาก .env ของคุณ):

```
GEMINI_API_KEY=your_actual_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash
DISCORD_TOKEN=your_actual_discord_bot_token
DISCORD_APPLICATION_ID=your_application_id
DISCORD_PUBLIC_KEY=your_public_key
DISCORD_CHANNEL_ID=your_auto_schedule_channel_id
DISCORD_COMMAND_CHANNEL_ID=your_command_channel_id
DAILY_RUN_TIME=08:00
TIMEZONE=Asia/Bangkok
MAX_NEWS_ARTICLES=10
MAX_PAPERS_TO_ANALYZE=100
SELECTED_PAPERS_COUNT=10
DEFAULT_DAYS_BACK=7
```

**Advanced Settings:**
- **Auto-Deploy**: Yes
- **Health Check Path**: `/health`
- **Docker Command**: (ใช้ default จาก Dockerfile)

### ขั้นตอนที่ 4: Deploy

1. คลิก **Create Web Service**
2. รอ build ~5-10 นาที
3. ตรวจสอบ logs ว่า bot เริ่มทำงาน

### ขั้นตอนที่ 5: ตรวจสอบ

**ตรวจสอบว่า Bot Online:**
- ดูที่ Discord server → Bot ควร online (สีเขียว)
- เข้า: `https://your-app-name.onrender.com/health`
- ควรเห็น: `{"status": "ok"}`

**ทดสอบ Commands:**
```
!status      # ดูสถานะ bot
!research 7  # รัน research
!help        # ดูคำสั่งทั้งหมด
```

---

## ⚙️ การตั้งค่าเพิ่มเติม

### Free Plan Limitations

Render Free Plan มีข้อจำกัด:
- **Sleep after 15 min** - Service จะ sleep ถ้าไม่มีการใช้งาน
- **750 hours/month** - ประมาณ 31 วัน
- **512MB RAM** - พอสำหรับ bot นี้

### ป้องกัน Sleep

เพิ่ม cron job ที่ ping health check ทุก 10 นาที:

1. ใช้ [cron-job.org](https://cron-job.org)
2. เพิ่ม URL: `https://your-app-name.onrender.com/health`
3. ตั้งเวลา: Every 10 minutes

### Monitoring

**ดู Logs:**
```bash
# ใน Render Dashboard → Logs tab
# จะเห็น real-time logs
```

**ดู Metrics:**
```bash
# ใน Render Dashboard → Metrics tab
# CPU, Memory usage
```

---

## 🔧 Troubleshooting

### Bot ไม่ Online
1. ตรวจสอบ Environment Variables ใน Render
2. ตรวจสอบ Logs ว่ามี error อะไร
3. ตรวจสอบ Discord Token ยังใช้งานได้อยู่

### Build Failed
1. ตรวจสอบ `requirements.txt` ถูกต้อง
2. ตรวจสอบ `Dockerfile` syntax
3. ดู Build Logs ว่า error ตรงไหน

### Out of Memory
1. ลด `MAX_PAPERS_TO_ANALYZE` จาก 100 → 50
2. Upgrade เป็น Paid Plan ($7/month)

---

## 📊 Cost Estimation

| Plan | Price | RAM | Features |
|------|-------|-----|----------|
| **Free** | $0 | 512MB | Sleep after 15 min |
| **Starter** | $7/mo | 512MB | Always on |
| **Standard** | $25/mo | 2GB | More resources |

**แนะนำ:** เริ่มจาก Free Plan ก่อน ถ้าใช้งานบ่อย upgrade เป็น Starter

---

## 🔄 การอัพเดทโค้ด

เมื่อแก้ไขโค้ด:

```bash
git add .
git commit -m "Update: your changes"
git push
```

Render จะ auto-deploy ใหม่ทันที (ถ้าเปิด Auto-Deploy)

---

## 🔒 Security Best Practices

1. **ใช้ Environment Variables** - ไม่ hardcode API keys
2. **Enable 2FA** - บน GitHub และ Render
3. **Rotate Tokens** - เปลี่ยน Discord token เป็นระยะ
4. **Monitor Logs** - ตรวจสอบ logs เป็นประจำ

---

## 📞 Support

หากมีปัญหา:
1. ตรวจสอบ [Render Docs](https://render.com/docs)
2. ดู [Discord.py Docs](https://discordpy.readthedocs.io/)
3. ตรวจสอบ GitHub Issues

---

## ✅ Checklist

- [ ] Push code ขึ้น GitHub
- [ ] สร้าง Web Service บน Render
- [ ] ตั้งค่า Environment Variables
- [ ] Deploy สำเร็จ
- [ ] Bot online ใน Discord
- [ ] ทดสอบ commands
- [ ] ตั้งค่า cron job (optional)
- [ ] Monitor logs

**เสร็จแล้ว!** Bot พร้อมรันบน Render 24/7 🎉
