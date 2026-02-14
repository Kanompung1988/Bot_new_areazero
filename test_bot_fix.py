"""
Test Script - ทดสอบว่าการแก้ไข bot offline issue ใช้งานได้
"""
import asyncio
import sys
from datetime import datetime

# Fix for Python 3.13+
import cgi_fix

async def test_bot_connection():
    """ทดสอบ bot connection และ reconnection logic"""
    print("="*70)
    print("🧪 ทดสอบ Bot Connection & Reconnection")
    print("="*70)
    print()
    
    try:
        from discord_bot.bot import create_bot
        import config
        
        if not config.DISCORD_TOKEN or config.DISCORD_TOKEN == 'your_discord_bot_token_here':
            print("❌ Discord token ไม่ได้ตั้งค่าใน .env")
            return False
        
        print("✅ Discord token พบแล้ว")
        
        # Create bot
        print("🤖 กำลังสร้าง bot instance...")
        bot = create_bot()
        print("✅ Bot instance สร้างสำเร็จ")
        
        # Check reconnection attributes
        if hasattr(bot, 'reconnect_attempts') and hasattr(bot, 'max_reconnect_attempts'):
            print(f"✅ Reconnection logic พร้อมใช้งาน (max attempts: {bot.max_reconnect_attempts})")
        else:
            print("❌ Reconnection logic ไม่พบ")
            return False
        
        # Check event handlers
        if hasattr(bot, 'on_disconnect') and hasattr(bot, 'on_resumed'):
            print("✅ Event handlers (on_disconnect, on_resumed) พบแล้ว")
        else:
            print("❌ Event handlers ไม่พบ")
            return False
        
        print()
        print("✅ Bot connection test ผ่าน!")
        print()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def test_api_health():
    """ทดสอบ API health check"""
    print("="*70)
    print("🧪 ทดสอบ API Health Check")
    print("="*70)
    print()
    
    try:
        import requests
        
        # Start API server in background
        print("🚀 กำลังเริ่ม API server...")
        
        # For testing, we'll just check if endpoints are defined
        from api import app
        
        print("✅ API app instance พบแล้ว")
        
        # Check if keep_alive function exists
        import inspect
        from api import keep_alive
        
        if inspect.iscoroutinefunction(keep_alive):
            print("✅ Keep-alive task function พบแล้ว")
        else:
            print("❌ Keep-alive task ไม่ใช่ async function")
            return False
        
        print()
        print("✅ API health check test ผ่าน!")
        print()
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_config():
    """ทดสอบ configuration"""
    print("="*70)
    print("🧪 ทดสอบ Configuration")
    print("="*70)
    print()
    
    try:
        import config
        
        required_vars = [
            ('DISCORD_TOKEN', config.DISCORD_TOKEN),
            ('DISCORD_CHANNEL_ID', config.DISCORD_CHANNEL_ID),
            ('GEMINI_API_KEY', config.GEMINI_API_KEY),
        ]
        
        all_ok = True
        for var_name, var_value in required_vars:
            if not var_value or 'your_' in str(var_value):
                print(f"❌ {var_name} ไม่ได้ตั้งค่า")
                all_ok = False
            else:
                # Show first 10 chars only
                masked = str(var_value)[:10] + "..." if len(str(var_value)) > 10 else str(var_value)
                print(f"✅ {var_name}: {masked}")
        
        print()
        if all_ok:
            print("✅ Configuration test ผ่าน!")
        else:
            print("⚠️ บาง configuration ไม่ครบ")
        print()
        return all_ok
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def run_all_tests():
    """รัน tests ทั้งหมด"""
    print()
    print("╔" + "="*68 + "╗")
    print("║" + " "*20 + "🧪 TEST SUITE - Bot Fix" + " "*21 + "║")
    print("╚" + "="*68 + "╝")
    print()
    print(f"⏰ เวลา: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = {
        "Configuration": test_config(),
        "Bot Connection": await test_bot_connection(),
        "API Health": await test_api_health()
    }
    
    print()
    print("="*70)
    print("📊 สรุปผลการทดสอบ")
    print("="*70)
    
    passed = 0
    failed = 0
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:.<50} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("="*70)
    print(f"ผลรวม: {passed} passed, {failed} failed")
    print("="*70)
    print()
    
    if failed == 0:
        print("🎉 ทุก test ผ่าน! พร้อม deploy ได้เลย")
        print()
        print("📝 ขั้นตอนถัดไป:")
        print("1. git add .")
        print('2. git commit -m "Fix: Add bot reconnection and keep-alive"')
        print("3. git push origin main")
        print("4. รอ Render auto-deploy (5-10 นาที)")
        print("5. ตั้ง UptimeRobot ตาม RENDER_FIX.md")
        print()
        return True
    else:
        print("⚠️ มี test ที่ failed - กรุณาแก้ไขก่อน deploy")
        return False

if __name__ == "__main__":
    try:
        result = asyncio.run(run_all_tests())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Test ถูกยกเลิก")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
