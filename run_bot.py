"""
Run Discord Bot - Convenience script
"""
# Fix for Python 3.13+ cgi module removal
import cgi_fix

from discord_bot.bot import run_bot
from utils.logger import setup_logging
from utils.helpers import create_directories

if __name__ == "__main__":
    setup_logging()
    create_directories()
    run_bot()
