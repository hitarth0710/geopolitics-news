"""Application configuration."""
import os
from dotenv import load_dotenv

load_dotenv()

# Data directory for persistent storage (Railway volume mount point)
# Use /data for Railway (better permissions) or /app/data as fallback
DATA_DIR = os.getenv("DATA_DIR", "/data")

# Database - use persistent data directory
DEFAULT_DB_PATH = os.path.join(DATA_DIR, "geopolitics_news.db")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")

# News API (optional - get free key at newsapi.org)
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")

# Feed update interval in minutes
FEED_UPDATE_INTERVAL = int(os.getenv("FEED_UPDATE_INTERVAL", "30"))

# Application settings
APP_NAME = "GeoPolitics Watch"
APP_DESCRIPTION = "Your window to world geopolitics"
