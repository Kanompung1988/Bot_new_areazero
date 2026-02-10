# AI Research Bot - แบบสมบูรณ์พร้อม Discord & FastAPI

Multi-agent AI research bot ที่ค้นหาข่าวและ papers เกี่ยวกับ AI ทุกวัน โดยใช้ Gemini AI และส่งผ่าน Discord

## ✨ Features ใหม่

- 🤖 **Discord Bot**: Bot ที่มี commands ให้ใช้งานใน Discord
- 🚀 **FastAPI**: REST API สำหรับ trigger research จาก web
- ⚡ **Manual Commands**: รัน research ทันทีด้วย `!research`
- 📊 **Real-time Status**: ตรวจสอบสถานะด้วย `!status`
- 🔧 **System Tests**: ทดสอบระบบด้วย `!test`

## 🏗️ สถาปัตยกรรม

### Multi-Agent System

```
Orchestrator
├── NewsAgent (ค้นหาและสรุปข่าว AI)
├── PaperDiscoveryAgent (ดึง papers จาก arXiv)
├── PaperSelectionAgent (เลือก top 10 papers ด้วย Gemini)
└── FormatterAgent (จัดรูปแบบเป็น Discord message)
```

## 📁 โครงสร้างโปรเจ็กต์

```
Bot_new_areazero_R&D/
├── agents/                 # AI Agents
│   ├── news_agent.py
│   ├── paper_discovery_agent.py
│   ├── paper_selection_agent.py
│   ├── formatter_agent.py
│   └── orchestrator.py
├── tools/                  # API Tools
│   ├── gemini_tool.py
│   ├── arxiv_tool.py
│   └── news_scraper.py
├── scheduler/              # Scheduling
│   └── daily_scheduler.py
├── database/               # Data persistence
│   └── models.py
├── discord_bot/            # Discord integration (TODO)
│   └── __init__.py
├── utils/                  # Utilities
│   ├── logger.py
│   └── helpers.py
├── config.py              # Configuration
├── main.py                # Entry point
├── requirements.txt
└── .env                   # API keys
```

## 🚀 การติดตั้ง

### 1. Clone และติดตั้ง dependencies

```powershell
cd "c:\Users\User\OneDrive - Mahidol University\Desktop\Work Areazero\Bot_new_areazero_R&D"
pip install -r requirements.txt
```

### 2. ตั้งค่า Environment Variables

ไฟล์ `.env` มี API key พร้อมใช้แล้ว:
```
GEMINI_API_KEY=AIzaSyAJczabSH9diysVe0ZGksxplRUYrjZLKmw
GEMINI_MODEL=gemini-3-flash-preview
DAILY_RUN_TIME=08:00
TIMEZONE=Asia/Bangkok
```

สำหรับ Discord (ทำภายหลัง):
```
DISCORD_TOKEN=your_discord_bot_token
DISCORD_CHANNEL_ID=your_channel_id
```

## 💻 การใช้งาน

### แสดงสถานะและ configuration
```powershell
python main.py --status
```

### ทดสอบระบบ
```powershell
python main.py --test
```

### รันทีละครั้ง (manual)
```powershell
python main.py --once
```

### รันแบบ scheduled (8 โมงเช้าทุกวัน)
```powershell
python main.py --schedule
```

## 📊 ผลลัพธ์

ผลลัพธ์จะถูกบันทึกใน:
- `output/research_YYYYMMDD_HHMMSS.txt` - Formatted digest
- `data/research_bot.db` - SQLite database
- `logs/bot.log` - Application logs

## 🔧 การปรับแต่ง

แก้ไขค่าต่างๆ ใน [config.py](config.py):

```python
MAX_NEWS_ARTICLES = 10          # จำนวนข่าวสูงสุด
MAX_PAPERS_TO_ANALYZE = 50      # Papers ที่จะวิเคราะห์
SELECTED_PAPERS_COUNT = 10      # จำนวน papers ที่เลือก
DAILY_RUN_TIME = '08:00'        # เวลารันอัตโนมัติ
```

## 🎯 ขั้นตอนถัดไป: Discord Integration

### 1. สร้าง Discord Bot

1. ไปที่ [Discord Developer Portal](https://discord.com/developers/applications)
2. สร้าง New Application
3. เข้า Bot section และ Reset Token
4. เปิด "MESSAGE CONTENT INTENT"
5. คัดลอก token ใส่ใน `.env`

### 2. เชิญ Bot เข้า Server

ใช้ URL (แทนที่ YOUR_CLIENT_ID):
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=274877975552&scope=bot
```

### 3. หา Channel ID

1. เปิด Developer Mode ใน Discord Settings
2. คลิกขวาที่ channel -> Copy ID
3. ใส่ใน `.env` ที่ `DISCORD_CHANNEL_ID`

### 4. Uncomment Discord code

1. Uncomment `discord.py` ใน [requirements.txt](requirements.txt)
2. Install: `pip install discord.py`
3. Implement Discord bot ใน `discord_bot/` folder

## 📖 ตัวอย่าง Output

```
══════════════════════════════════════════════════
🤖 AI RESEARCH DAILY DIGEST
📅 February 10, 2026
══════════════════════════════════════════════════

Good morning! Here's your comprehensive AI research 
digest featuring the latest breakthroughs...

──────────────────────────────────────────────────
📰 AI NEWS TODAY

Top 10 Stories:

1. OpenAI Announces GPT-5
   Revolutionary language model with enhanced...
   🔗 [OpenAI Blog](https://...)
   📅 2026-02-10

...

──────────────────────────────────────────────────
📚 TOP 10 AI RESEARCH PAPERS

Selected from 47 recent papers

#1 | LLM
📄 Constitutional AI: Harmlessness from AI Feedback
✍️ Yuntao Bai et al.
📝 We propose a method for training AI systems...
💡 Groundbreaking approach to AI alignment
🔗 [Read Paper](https://arxiv.org/...)
📅 Published: 2026-02-09

...
```

## 🐛 Troubleshooting

### Gemini API Error
```powershell
# ทดสอบ API
python -c "from tools.gemini_tool import get_gemini_api; print(get_gemini_api().generate_content('Test'))"
```

### Import Errors
```powershell
# ตรวจสอบ Python path
python -c "import sys; print('\n'.join(sys.path))"
```

### Database locked
```powershell
# ลบ database และสร้างใหม่
rm data/research_bot.db
python main.py --once
```

## 📝 Logs

ดู logs:
```powershell
Get-Content logs/bot.log -Tail 50 -Wait
```

## 🤝 Contributing

สามารถปรับปรุงได้ที่:
- เพิ่ม news sources ใน `config.py`
- ปรับ prompt ใน `tools/gemini_tool.py`
- เพิ่ม features ให้ agents

## 📄 License

MIT License

## 👤 Author

Created for Area Zero R&D

---

**หมายเหตุ**: Discord integration จะทำในขั้นตอนถัดไป หลังจากทดสอบ core functionality เรียบร้อยแล้ว
