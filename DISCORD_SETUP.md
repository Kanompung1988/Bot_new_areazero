# 🤖 คู่มือเชิญ Bot เข้า Discord Server

## ขั้นตอนที่ 1: เชิญ Bot เข้า Server

### วิธีที่ 1: ใช้ Link พร้อมใช้งาน (แนะนำ) ⭐

คลิกที่ link นี้:

```
https://discord.com/api/oauth2/authorize?client_id=1470799266028060775&permissions=534723947584&scope=bot+applications.commands
```

หรือคัดลอก link นี้ไปวางใน browser:
```
https://discord.com/oauth2/authorize?client_id=1470799266028060775&permissions=534723947584&scope=bot%20applications.commands
```

### วิธีที่ 2: สร้าง Link เอง

1. ไปที่ [Discord Developer Portal](https://discord.com/developers/applications/1470799266028060775/oauth2/url-generator)
2. เลือก **Scopes**:
   - ✅ `bot`
   - ✅ `applications.commands`
3. เลือก **Bot Permissions**:
   - ✅ Read Messages/View Channels
   - ✅ Send Messages
   - ✅ Send Messages in Threads
   - ✅ Embed Links
   - ✅ Attach Files
   - ✅ Read Message History
   - ✅ Add Reactions
   - ✅ Use Slash Commands
4. คัดลอก Generated URL ด้านล่าง

### ขั้นตอนการเชิญ:

1. คลิก invite link ข้างบน
2. เลือก **Server** ที่ต้องการเพิ่ม bot
3. คลิก **Continue**
4. ตรวจสอบ Permissions (ควรเปิดทั้งหมด)
5. คลิก **Authorize**
6. ทำ reCAPTCHA verification
7. เสร็จแล้ว! Bot จะปรากฏใน server

---

## ขั้นตอนที่ 2: เปิดใช้งาน Bot

### ตรวจสอบว่า Bot Server รันอยู่หรือไม่

```powershell
# เปิด terminal และรัน
cd "C:\Users\User\OneDrive - Mahidol University\Desktop\Work Areazero\Bot_new_areazero_R&D"
python run_api.py
```

คุณควรเห็น:
```
✓ Discord bot started in background
✓ Bot is ready!
✓ Logged in as: Zero-R&D New paper
```

### ถ้า Bot Offline:

1. **ตรวจสอบ Token**: เช็คว่า token ใน `.env` ถูกต้อง
2. **ตรวจสอบ Intents**: ไปที่ [Bot Settings](https://discord.com/developers/applications/1470799266028060775/bot)
   - เปิด **MESSAGE CONTENT INTENT** ✅
   - เปิด **SERVER MEMBERS INTENT** (optional)
   - เปิด **PRESENCE INTENT** (optional)
3. **Save Changes** และรัน bot ใหม่

---

## ขั้นตอนที่ 3: ตั้งค่า Channel

### 1. หา Channel ID

1. เปิด **User Settings** > **Advanced** > เปิด **Developer Mode** ✅
2. คลิกขวาที่ **Channel** ที่ต้องการให้ bot ส่งข้อความ
3. คลิก **Copy ID**

### 2. ใส่ Channel ID ใน .env

แก้ไขไฟล์ `.env`:
```env
DISCORD_CHANNEL_ID=<วาง_Channel_ID_ที่_คัดลอกมา>
```

ปัจจุบัน Channel ID คือ: `1470802465031983124`

### 3. Restart Bot

กด `Ctrl+C` ใน terminal แล้วรันใหม่:
```powershell
python run_api.py
```

---

## 📝 วิธีใช้งาน Bot

### คำสั่งพื้นฐาน

#### 1. ตรวจสอบสถานะ Bot
```
!status
```
หรือ
```
!s
```

**ผลลัพธ์:**
- สถานะ bot (Online/Offline)
- จำนวน research runs ทั้งหมด
- สถิติ papers และ articles
- Configuration ปัจจุบัน

---

#### 2. รัน Research ทันที ⭐
```
!research
```
หรือ
```
!r
```

**พร้อม options:**
```
!research 1    # ค้นหาข้อมูล 1 วันย้อนหลัง
!research 3    # ค้นหาข้อมูล 3 วันย้อนหลัง
!research 7    # ค้นหาข้อมูล 7 วันย้อนหลัง
```

**ผลลัพธ์:**
- รายการข่าว AI ล่าสุด (max 10 ข่าว)
- Top 10 research papers จาก arXiv
- สรุปโดย Gemini AI

**หมายเหตุ:**
- ใช้เวลาประมาณ 1-2 นาที
- มี cooldown 5 นาทีต่อครั้ง
- ข้อความจะถูกแบ่งเป็นหลายส่วนถ้ายาวเกินไป

---

#### 3. ดูสถิติ
```
!stats
```

**พร้อม options:**
```
!stats 7     # สถิติ 7 วันย้อนหลัง
!stats 30    # สถิติ 30 วันย้อนหลัง
```

**ผลลัพธ์:**
- จำนวน papers ที่ featured
- แยกตาม categories

---

#### 4. ทดสอบระบบ (Admin Only) 🔒
```
!test
```

**ผลลัพธ์:**
- ทดสอบ Gemini API
- ทดสอบ Database
- ทดสอบ Orchestrator
- ทดสอบ agents ทั้งหมด

**หมายเหตุ:** ต้องมี Administrator permission

---

#### 5. ดูคำสั่งทั้งหมด
```
!help_research
```
หรือ
```
!rhelp
```

---

### คำสั่งแบบย่อ (Aliases)

| คำสั่งเต็ม | Alias | Alias 2 |
|-----------|-------|---------|
| !research | !r    | !run    |
| !status   | !s    | !info   |
| !help_research | !rhelp | - |

---

## 🎯 ตัวอย่างการใช้งาน

### Scenario 1: Check Bot Status
```
User: !status

Bot: 📊 AI Research Bot Status
     
     🤖 Bot Info
     Status: Online ✅
     Model: gemini-2.5-flash
     Prefix: !
     
     📊 Statistics
     Total Runs: 5
     Successful: 5
     Papers Tracked: 50
     Featured Papers: 50
     Articles Tracked: 25
     
     ⚙️ Configuration
     Daily Run Time: 08:00 Asia/Bangkok
     Max News: 10
     Selected Papers: 10
```

---

### Scenario 2: Run Research
```
User: !research 1

Bot: 🤖 Starting AI research... This may take a few minutes.
     🔍 Step 1/4: Fetching AI news...
     ✅ Research completed! Sending results...
     
     ══════════════════════════════════════════════════
     🤖 AI RESEARCH DAILY DIGEST
     📅 February 10, 2026
     ══════════════════════════════════════════════════
     
     Good morning! Here's your comprehensive AI research...
     
     ──────────────────────────────────────────────────
     📰 AI NEWS TODAY
     
     Top 3 Stories:
     
     1. OpenAI Announces GPT-5...
     2. Google DeepMind...
     3. Meta AI Research...
     
     ──────────────────────────────────────────────────
     📚 TOP 10 AI RESEARCH PAPERS
     
     #1 | LLM
     📄 Constitutional AI: Harmlessness from AI Feedback
     ...
```

---

### Scenario 3: Check Stats
```
User: !stats 7

Bot: 📈 Last 7 Days Statistics
     
     📚 Papers Featured
     10 papers
     
     📊 By Category
     • LLM: 4
     • Computer Vision: 3
     • NLP: 2
     • Other: 1
```

---

## 🔧 Troubleshooting

### Bot ไม่ตอบ

**สาเหตุที่เป็นไปได้:**

1. **Bot Offline**
   - เช็คว่า server รัน `python run_api.py` อยู่หรือไม่
   - ดู logs ใน terminal

2. **Permissions ไม่ครบ**
   - Bot ต้องมี permission: Read Messages, Send Messages
   - เช็คที่ Channel Settings > Permissions

3. **Channel ID ผิด**
   - ตรวจสอบ `DISCORD_CHANNEL_ID` ใน `.env`
   - ลองส่งคำสั่งใน channel อื่น

4. **Message Content Intent ไม่เปิด**
   - ไปที่ [Bot Settings](https://discord.com/developers/applications/1470799266028060775/bot)
   - เปิด **MESSAGE CONTENT INTENT** ✅
   - Save และ restart bot

---

### Bot ตอบช้า

**สาเหตุที่เป็นไปได้:**

1. **Research ใช้เวลานาน**
   - ปกติใช้เวลา 1-2 นาที
   - Gemini API อาจช้าบางครั้ง

2. **Rate Limiting**
   - arXiv API มี rate limit
   - รอ 3 วินาทีระหว่างแต่ละ query

---

### Commands ไม่ทำงาน

**แก้ไข:**

1. **ตรวจสอบ prefix**
   - ต้องขึ้นต้นด้วย `!`
   - เช่น `!research` ไม่ใช่ `research`

2. **ตรวจสอบ typos**
   - `!research` ไม่ใช่ `!reserch`
   - ใช้ `!help_research` ดู commands ที่ถูกต้อง

3. **Cooldown**
   - `!research` มี cooldown 5 นาที
   - รอให้ครบแล้วลองใหม่

---

## 📚 คำสั่งเพิ่มเติม (ผ่าน API)

นอกจาก Discord commands แล้ว คุณสามารถใช้ REST API ได้:

### เปิด Browser
```
http://localhost:8000/docs
```

### ใช้ curl
```powershell
# Health check
curl http://localhost:8000/health

# Get status
curl http://localhost:8000/api/status

# Trigger research
curl -X POST http://localhost:8000/api/research -H "Content-Type: application/json" -d '{\"days_back\": 1, \"send_to_discord\": true}'
```

---

## 🌟 Tips & Best Practices

1. **ตั้ง Dedicated Channel**
   - สร้าง channel เฉพาะสำหรับ bot (เช่น `#ai-research`)
   - Bot จะส่งข้อความยาว ๆ

2. **กำหนด Role สำหรับ Bot**
   - สร้าง role `@AI Research Bot`
   - ให้ permissions ที่จำเป็น

3. **ใช้ Scheduled Run**
   - Bot จะรันอัตโนมัติทุกวัน 8:00 AM
   - ไม่ต้อง trigger ด้วยตนเอง

4. **Monitor Logs**
   - เช็ค `logs/bot.log` เป็นระยะ
   - ดู errors และ warnings

5. **Backup Database**
   - สำรอง `data/research_bot.db` เป็นประจำ
   - เก็บประวัติ research runs

---

## 🎓 Resources

- **Discord Developer Portal**: https://discord.com/developers/applications/1470799266028060775
- **API Documentation**: http://localhost:8000/docs (เมื่อ server รัน)
- **Logs**: `logs/bot.log`
- **Database**: `data/research_bot.db`
- **Project README**: `README.md`

---

## 📞 Support

หากมีปัญหา:
1. เช็ค `logs/bot.log`
2. รัน `!test` เพื่อทดสอบระบบ
3. ตรวจสอบ permissions ใน Discord
4. Restart bot server

---

**Bot ID**: 1470799266028060775  
**Bot Name**: Zero-R&D New paper  
**Version**: 1.0.0

🎉 Happy Researching!
