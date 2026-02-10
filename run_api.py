"""
Run API Server - Convenience script
"""
# Fix for Python 3.13+ cgi module removal
import cgi_fix

import signal
import sys
import asyncio

from api import run_api
from utils.logger import setup_logging
from utils.helpers import create_directories


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    print("\n" + "="*70)
    print("🚫 Shutting down gracefully...")
    print("="*70)
    sys.exit(0)


if __name__ == "__main__":
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    setup_logging()
    create_directories()
    
    print("="*70)
    print("🚀 Starting AI Research Bot API Server")
    print("="*70)
    print("📡 API will be available at: http://localhost:8000")
    print("📚 API docs at: http://localhost:8000/docs")
    print("🤖 Discord bot will start automatically")
    print("💡 Press Ctrl+C to stop")
    print("="*70)
    print()
    
    try:
        run_api(host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        print("\n✅ Bot stopped successfully.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
