"""
Configuration module for AI Research Bot
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gemini Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

# Discord Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_APPLICATION_ID = os.getenv('DISCORD_APPLICATION_ID')
DISCORD_PUBLIC_KEY = os.getenv('DISCORD_PUBLIC_KEY')
DISCORD_CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')  # Auto-schedule channel
DISCORD_COMMAND_CHANNEL_ID = os.getenv('DISCORD_COMMAND_CHANNEL_ID')  # Manual command channel
DISCORD_COMMAND_PREFIX = '!'

# Scheduling Configuration
DAILY_RUN_TIME = os.getenv('DAILY_RUN_TIME', '08:00')
TIMEZONE = os.getenv('TIMEZONE', 'Asia/Bangkok')

# Research Configuration
MAX_NEWS_ARTICLES = int(os.getenv('MAX_NEWS_ARTICLES', 10))
MAX_PAPERS_TO_ANALYZE = int(os.getenv('MAX_PAPERS_TO_ANALYZE', 100))
SELECTED_PAPERS_COUNT = int(os.getenv('SELECTED_PAPERS_COUNT', 10))
DEFAULT_DAYS_BACK = int(os.getenv('DEFAULT_DAYS_BACK', 7))
AI_TOPICS = os.getenv('AI_TOPICS', 'LLM,Computer Vision,NLP,Graph Neural Networks,Reinforcement Learning').split(',')

# API Endpoints
ARXIV_API_URL = "http://export.arxiv.org/api/query"
SEMANTIC_SCHOLAR_API_URL = "https://api.semanticscholar.org/graph/v1"

# News Sources
NEWS_SOURCES = [
    "https://www.artificialintelligence-news.com/feed/",
    "https://hai.stanford.edu/news/rss.xml",
    "https://openai.com/blog/rss/",
    "https://blog.google/technology/ai/rss/",
]

# Database
DATABASE_PATH = "data/research_bot.db"

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = "logs/bot.log"
