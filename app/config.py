"""Application configuration."""
import os
from dotenv import load_dotenv

load_dotenv()

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./geopolitics_news.db")

# News API (optional - get free key at newsapi.org)
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")

# Feed update interval in minutes
FEED_UPDATE_INTERVAL = int(os.getenv("FEED_UPDATE_INTERVAL", "30"))

# Application settings
APP_NAME = "GeoPolitics Watch"
APP_DESCRIPTION = "Your window to world geopolitics"
