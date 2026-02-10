# Memory System - Paper Deduplication

## Overview
Bot จะจำ papers ที่เคยส่งไปแล้วและไม่ส่งซ้ำในวันถัดไป เพื่อให้ผู้ใช้ได้รับ papers ใหม่ๆ ตลอดเวลา

## How It Works

### 1. Database Storage
- Papers ที่ถูกส่งไปจะบันทึกลง SQLite database
- เก็บข้อมูล: paper ID, title, authors, abstract, category, publish date
- บันทึก `featured_date` เมื่อ paper ถูกส่งในระบบอัตโนมัติ

### 2. Memory Duration
- ระบบจะจำ papers ที่เคยส่งไป **30 วัน**
- Papers ที่เก่ากว่า 30 วัน จะสามารถถูกเลือกส่งอีกครั้งได้

### 3. Channel-Specific Behavior

#### Auto-Schedule Channel (1470802465031983124)
- ✅ **Memory ENABLED**
- รันอัตโนมัติทุกวันเวลา 8:00 AM Bangkok time
- กรอง papers ที่เคยส่งไปแล้วออก
- การันตี papers ใหม่ทุกวัน

#### Command Channel (1470809719819210865)
- ❌ **Memory DISABLED**
- ใช้สำหรับ manual commands (`!research`)
- แสดง papers ทั้งหมดโดยไม่กรอง
- ใช้สำหรับ testing และ ad-hoc research

## Technical Implementation

### Database Schema
```python
class Paper(Base):
    id = Column(Integer, primary_key=True)
    paper_id = Column(String(50), unique=True, index=True)  # arXiv ID
    title = Column(Text)
    authors = Column(Text)
    abstract = Column(Text)
    published_date = Column(DateTime)
    category = Column(String(50))
    pdf_url = Column(String(500))
    featured_date = Column(DateTime, nullable=True)  # When featured
    created_at = Column(DateTime, default=datetime.now)
```

### Filter Logic
```python
# In paper_selection_agent.py
if filter_featured:
    db = get_db()
    papers = [p for p in papers if not db.paper_was_featured(p.get('id'))]
    db.close()

# In database/models.py
def paper_was_featured(self, paper_id: str, days: int = 30) -> bool:
    cutoff = datetime.now() - timedelta(days=days)
    paper = self.session.query(Paper).filter_by(paper_id=paper_id).first()
    return paper is not None and paper.featured_date >= cutoff
```

### Save Featured Papers
```python
# In orchestrator.py (after successful formatting)
if filter_featured and selection_data.get('selected_papers'):
    for paper in selection_data['selected_papers']:
        self.db.add_paper(paper, featured=True)
```

## Usage

### Automatic Schedule
- No action needed
- Bot automatically uses memory filter
- Papers are saved to database after successful send

### Manual Research
```bash
# These commands do NOT use memory filter
!research              # All papers, no filtering
!research 7 LLM       # All LLM papers from last 7 days
!research 3 CV        # All CV papers from last 3 days
```

## Benefits

✅ **No Duplicate Content** - Users see fresh papers every day
✅ **Intelligent Selection** - System remembers what was sent
✅ **Flexible Testing** - Manual commands bypass filter
✅ **Automatic Cleanup** - 30-day memory window prevents database bloat

## Database Location
```
data/research_bot.db
```

## Monitoring

Check memory statistics:
```bash
!stats
```

This will show:
- Total papers in database
- Featured papers count
- Recent activity

## Configuration

Adjust memory duration in `database/models.py`:
```python
def paper_was_featured(self, paper_id: str, days: int = 30):  # Change days here
```

## Reset Memory

To clear all featured papers and start fresh:
```sql
-- Connect to database
sqlite3 data/research_bot.db

-- Clear featured dates
UPDATE papers SET featured_date = NULL;

-- Or delete all records
DELETE FROM papers;
```
