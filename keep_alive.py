"""
Keep-Alive Script for Render Deployment
Pings the service to prevent free tier spin-down
"""
import requests
import time
import os
from datetime import datetime

# Service URL - will be set automatically on Render
SERVICE_URL = os.getenv('RENDER_EXTERNAL_URL', 'http://localhost:8000')

def ping_service():
    """Ping the health endpoint"""
    try:
        response = requests.get(f"{SERVICE_URL}/health", timeout=10)
        status = "✅ OK" if response.status_code == 200 else f"⚠️ {response.status_code}"
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ping: {status}")
        
        # Log bot status if available
        if response.status_code == 200:
            data = response.json()
            bot_status = data.get('bot', {})
            if bot_status:
                print(f"  Bot Ready: {bot_status.get('ready', False)}, "
                      f"Guilds: {bot_status.get('guilds', 0)}, "
                      f"Latency: {bot_status.get('latency', 0)}ms")
        
        return True
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ Error: {e}")
        return False

def run():
    """Run keep-alive loop"""
    print("="*70)
    print("🔄 Keep-Alive Service Started")
    print(f"📡 Target: {SERVICE_URL}")
    print("⏰ Interval: 10 minutes")
    print("="*70)
    print()
    
    while True:
        ping_service()
        # Sleep for 10 minutes (600 seconds)
        # Render free tier spins down after 15 minutes of inactivity
        time.sleep(600)

if __name__ == "__main__":
    run()
