# Bot Offline Fix - การแก้ไขปัญหาบอทไป Offline

## ปัญหาที่พบ 🔴
บอท Discord จะไป offline เมื่อไม่มีการใช้งานนานๆ เนื่องจาก:
1. Discord WebSocket connection ไม่มี keep-alive mechanism
2. ไม่มีการอัพเดท presence เป็นระยะ
3. ไม่ได้เปิด intents ที่จำเป็นทั้งหมด
4. ไม่มีการจัดการ reconnection อย่างเหมาะสม

## การแก้ไข ✅

### 1. เพิ่ม Discord Intents ที่จำเป็น
```python
# ใน discord_bot/bot.py
intents.guild_messages = True  # รับ message events
intents.members = True         # ติดตาม member presence
```

### 2. เพิ่ม Heartbeat Timeout
```python
super().__init__(
    command_prefix=config.DISCORD_COMMAND_PREFIX,
    intents=intents,
    heartbeat_timeout=config.DISCORD_HEARTBEAT_TIMEOUT  # เพิ่มเวลา timeout
)
```

### 3. สร้าง Keep-Alive Loop
เพิ่ม background task ที่:
- รันทุก 5 นาที (ตั้งค่าได้ผ่าน `DISCORD_KEEPALIVE_INTERVAL`)
- อัพเดท presence เพื่อแสดงว่าบอทยัง active
- ตรวจสอบ latency และ connection status
- บันทึก log เมื่อไม่มี activity นาน > 30 นาที

```python
async def _keep_alive_loop(self):
    while not self.is_closed():
        await asyncio.sleep(self._keepalive_interval)
        
        if self.is_ready():
            # อัพเดท presence
            await self.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name="AI Research | !help"
                )
            )
```

### 4. ติดตาม Activity
บันทึกเวลาของ activity ล่าสุดเมื่อ:
- มี message เข้ามา
- มี command
- บอท ready

### 5. Auto-Reconnect
```python
bot.run(config.DISCORD_TOKEN, reconnect=True)  # เปิดใช้ auto-reconnect
```

### 6. Enhanced Monitoring ใน api.py
เพิ่มการตรวจสอบ bot health ทุก 10 นาที:
- ตรวจสอบสถานะ ready และ closed
- นับจำนวนครั้งที่ health check ล้มเหลวติดต่อกัน
- Log warning เมื่อบอท offline นาน > 30 นาที

## การตั้งค่าใน .env

เพิ่มการตั้งค่าเหล่านี้ (optional):
```env
# Discord Bot Settings
DISCORD_HEARTBEAT_TIMEOUT=60.0      # WebSocket heartbeat timeout (วินาที)
DISCORD_KEEPALIVE_INTERVAL=300      # Presence update interval (วินาที) - ค่า default 5 นาที
```

## วิธีใช้งาน

### รันบอทแบบ standalone:
```bash
python run_bot.py
```

### รันบอทพร้อม API server (แนะนำสำหรับ production):
```bash
python main.py --api
```

## สิ่งที่ต้องตรวจสอบ ⚠️

1. **Discord Bot Intents** - ตรวจสอบว่าเปิด intents ที่จำเป็นใน Discord Developer Portal:
   - MESSAGE CONTENT INTENT ✅
   - SERVER MEMBERS INTENT ✅
   - PRESENCE INTENT (optional)

2. **Network/Firewall** - ตรวจสอบว่า:
   - WebSocket connections (wss://) ไม่ถูก block
   - Port 443 สามารถใช้งานได้

3. **Memory/Resources** - ตรวจสอบว่า:
   - Server มี memory เพียงพอ
   - Process ไม่ถูก kill โดย OOM killer

## Log Monitoring

ตรวจสอบ logs เพื่อ monitor:
```bash
# Keep-alive pings (ทุก 5 นาที)
[DEBUG] ResearchBot: Keep-alive ping - Latency: 45ms, Guilds: 3, Last activity: 120s ago

# Warnings
[WARNING] ResearchBot: No activity for 30.0 minutes

# Errors
[ERROR] ResearchBot: Max reconnection attempts reached
```

## Performance

- **Memory**: เพิ่มขึ้นเล็กน้อย (~1-2 MB) เนื่องจาก keep-alive task
- **Network**: เพิ่ม traffic เล็กน้อย (presence update ทุก 5 นาที)
- **Benefits**: บอทจะ online ตลอดเวลาแม้ไม่มีการใช้งาน

## Troubleshooting

### บอทยังไป offline อยู่:
1. ตรวจสอบ logs ใน `logs/bot.log`
2. ลด `DISCORD_KEEPALIVE_INTERVAL` เป็น 180 (3 นาที)
3. ตรวจสอบ Discord API status: https://discordstatus.com
4. ตรวจสอบ intents ใน Discord Developer Portal

### Latency สูง:
1. เพิ่ม `DISCORD_HEARTBEAT_TIMEOUT`
2. ตรวจสอบ network connection
3. พิจารณาใช้ server ใกล้กับ Discord region ของคุณมากขึ้น

## อ้างอิง
- Discord.py Documentation: https://discordpy.readthedocs.io/
- Discord Gateway: https://discord.com/developers/docs/topics/gateway
- Best Practices: https://discord.com/developers/docs/topics/gateway#gateway-intents
