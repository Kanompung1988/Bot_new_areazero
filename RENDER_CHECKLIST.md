# ✅ Render Deployment Checklist

> ใช้ checklist นี้เพื่อให้แน่ใจว่า deploy ครบทุกขั้นตอน

---

## 📋 Pre-Deployment

### 1. Local Setup
- [ ] Code ทำงานถูกต้องใน local
- [ ] ทดสอบ: `python run_bot.py`
- [ ] Bot online ใน Discord (local)
- [ ] ไฟล์ `.env` มีค่าครบถ้วน
- [ ] ไฟล์ `.gitignore` มี `.env` อยู่ (อย่า commit secrets!)

### 2. Discord Configuration
- [ ] Discord Developer Portal setup เสร็จ
- [ ] Bot Token ได้แล้ว
- [ ] Intents เปิดแล้ว:
  - [ ] MESSAGE CONTENT INTENT
  - [ ] SERVER MEMBERS INTENT
- [ ] Bot invite เข้า server แล้ว
- [ ] Channel ID ได้แล้ว (right-click → Copy ID)

### 3. API Keys
- [ ] Gemini API Key ได้แล้ว (https://ai.google.dev/)
- [ ] Test Gemini API ใน local แล้ว
- [ ] Keys ทั้งหมดเก็บปลอดภัย

### 4. Repository
- [ ] Code push ขึ้น GitHub แล้ว
- [ ] Repository เป็น public หรือ Render มีสิทธิ์เข้าถึง
- [ ] Branch `main` มีอยู่
- [ ] ไฟล์สำคัญครบ:
  - [ ] `Dockerfile`
  - [ ] `render.yaml`
  - [ ] `requirements.txt`
  - [ ] `api.py`
  - [ ] `run_api.py`

---

## 🚀 Render Setup

### 5. Create Service
- [ ] สมัคร Render.com แล้ว
- [ ] GitHub เชื่อมต่อกับ Render แล้ว
- [ ] สร้าง Web Service แล้ว
- [ ] เลือก repository ถูกต้อง
- [ ] Branch: `main`
- [ ] Environment: `Docker`

### 6. Basic Configuration
- [ ] Name: `ai-research-bot` (หรือชื่อที่ต้องการ)
- [ ] Region: `Singapore`
- [ ] Plan: `Free`
- [ ] Root Directory: (leave blank)

### 7. Environment Variables (สำคัญที่สุด!)

**Required (ต้องมี):**
- [ ] `DISCORD_TOKEN` = [your_token]
- [ ] `GEMINI_API_KEY` = [your_key]
- [ ] `DISCORD_CHANNEL_ID` = [channel_id]

**Recommended:**
- [ ] `GEMINI_MODEL` = gemini-2.5-flash
- [ ] `DISCORD_HEARTBEAT_TIMEOUT` = 60.0
- [ ] `DISCORD_KEEPALIVE_INTERVAL` = 300
- [ ] `DAILY_RUN_TIME` = 08:00
- [ ] `TIMEZONE` = Asia/Bangkok

**Optional:**
- [ ] `DISCORD_APPLICATION_ID`
- [ ] `DISCORD_PUBLIC_KEY`
- [ ] `DISCORD_COMMAND_CHANNEL_ID`
- [ ] `MAX_NEWS_ARTICLES` = 10
- [ ] `SELECTED_PAPERS_COUNT` = 10

### 8. Advanced Settings
- [ ] Health Check Path: `/health`
- [ ] Auto-Deploy: `Yes`
- [ ] Docker Command: (use default)

### 9. Deploy
- [ ] คลิก "Create Web Service"
- [ ] รอ build (3-5 นาที)
- [ ] ดู build logs ไม่มี errors

---

## ✅ Post-Deployment Verification

### 10. Build & Deploy Status
- [ ] Build status: ✅ Success
- [ ] Deploy status: ✅ Live
- [ ] Service running: 🟢 Active
- [ ] No errors in logs

### 11. Logs Check
เปิด Render Dashboard → Logs, ควรเห็น:
- [ ] `Starting Discord bot...`
- [ ] `ResearchBot: Bot is ready!`
- [ ] `Logged in as: [BotName]`
- [ ] `Connected to X guild(s)`
- [ ] `Keep-alive loop started`
- [ ] Keep-alive pings ทุก 5 นาที

### 12. Health Endpoint
เปิด browser: `https://[your-app].onrender.com/health`
- [ ] Status code: 200
- [ ] Response: `{"status": "healthy", "bot": {...}}`
- [ ] `bot.ready`: true
- [ ] `bot.connected`: true

### 13. Discord Bot Status
ใน Discord Server:
- [ ] Bot แสดงสถานะ 🟢 Online
- [ ] Bot มี role/permissions ถูกต้อง
- [ ] ทดสอบคำสั่ง: `!ping` ได้
- [ ] ทดสอบคำสั่ง: `!status` ได้

### 14. API Endpoints
- [ ] `/` - Root endpoint ตอบกลับ
- [ ] `/health` - Health check ผ่าน
- [ ] `/ping` - Ping endpoint ทำงาน

---

## 🔄 Keep-Alive Setup (สำคัญมาก!)

### 15. UptimeRobot Configuration
- [ ] สมัคร UptimeRobot.com แล้ว (ฟรี)
- [ ] เพิ่ม Monitor ใหม่
- [ ] Monitor Type: HTTP(s)
- [ ] URL: `https://[your-app].onrender.com/health`
- [ ] Interval: 5 minutes
- [ ] Monitor สถานะ: 🟢 Up

### 16. Alert Setup (Optional)
- [ ] เพิ่ม Alert Contact (email)
- [ ] ทดสอบ alert
- [ ] ตั้งค่า notification preferences

---

## 🧪 Testing

### 17. Functionality Tests
- [ ] `!help` - แสดงคำสั่งทั้งหมด
- [ ] `!ping` - ตอบกลับด้วย latency
- [ ] `!status` - แสดงสถานะบอท
- [ ] `!config` - แสดง configuration
- [ ] `!research` - รัน research (ถ้ามี)

### 18. Performance Tests
- [ ] Response time < 1 วินาที
- [ ] Memory usage < 400 MB
- [ ] CPU usage reasonable
- [ ] No memory leaks

### 19. Stability Tests
- [ ] Bot อยู่ online > 1 ชั่วโมง
- [ ] Keep-alive pings ทำงานต่อเนื่อง
- [ ] ไม่มี unexpected restarts
- [ ] Health checks ผ่านทุกครั้ง

---

## 📊 Monitoring

### 20. Setup Monitoring
- [ ] เข้า Render Dashboard ได้
- [ ] ดู Metrics tab ได้
- [ ] ดู Logs tab ได้
- [ ] เข้า UptimeRobot Dashboard ได้

### 21. Regular Checks
- [ ] Uptime percentage > 99%
- [ ] Average response time noted
- [ ] Log ไม่มี recurring errors
- [ ] Memory usage stable

---

## 🔧 Troubleshooting Prep

### 22. Backup & Documentation
- [ ] บันทึก Render app URL
- [ ] บันทึก GitHub repo URL
- [ ] เก็บ Environment Variables ไว้ปลอดภัย
- [ ] เก็บ Discord Bot Token
- [ ] เก็บ Gemini API Key

### 23. Rollback Plan
- [ ] รู้วิธี rollback deploy ใน Render
- [ ] มี git tag/branch สำหรับ stable version
- [ ] มี backup ของ .env file
- [ ] รู้วิธี manual deploy

---

## 🎓 Optional Enhancements

### 24. Advanced Features (Optional)
- [ ] Custom domain setup
- [ ] SSL certificate (auto by Render)
- [ ] Webhook notifications
- [ ] Database persistence (if needed)
- [ ] PM2 integration (not needed on Render)

### 25. Documentation
- [ ] อ่าน RENDER_SETUP.md แล้ว
- [ ] อ่าน RENDER_VISUAL_GUIDE.md แล้ว
- [ ] อ่าน KEEP_ALIVE_SOLUTIONS.md แล้ว
- [ ] Bookmark Render Dashboard
- [ ] Bookmark UptimeRobot Dashboard

---

## 🎉 Success Criteria

ถ้าทุกข้อด้านล่างเป็นจริง = **Deploy สำเร็จ 100%!**

- [x] ✅ Bot online in Discord (🟢)
- [x] ✅ Health endpoint responds (200 OK)
- [x] ✅ UptimeRobot monitoring active
- [x] ✅ No errors in logs
- [x] ✅ Commands work (!ping, !status)
- [x] ✅ Keep-alive pings every 5 minutes
- [x] ✅ Service uptime > 99%
- [x] ✅ Auto-deploy from GitHub works

---

## 📝 Notes & Issues

Use this space to note any issues or customizations:

```
Date: _______________
Issues encountered:
_____________________________________
_____________________________________

Solutions applied:
_____________________________________
_____________________________________

Custom configurations:
_____________________________________
_____________________________________
```

---

## 🆘 Need Help?

If any check fails:

1. **Read documentation:**
   - [RENDER_SETUP.md](RENDER_SETUP.md) - Full guide
   - [RENDER_VISUAL_GUIDE.md](RENDER_VISUAL_GUIDE.md) - Visual steps
   - [BOT_OFFLINE_FIX.md](BOT_OFFLINE_FIX.md) - Offline issues

2. **Check logs:**
   - Render Dashboard → Logs
   - Look for errors/warnings

3. **Verify configuration:**
   - Environment variables correct?
   - Discord intents enabled?
   - API keys valid?

4. **Test locally first:**
   - `python check_bot_health.py`
   - `python run_bot.py`

---

**Good luck with your deployment! 🚀**

Print this checklist and check off each item as you complete it!
