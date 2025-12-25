"""Application configuration."""
import os
from dotenv import load_dotenv

load_dotenv()

# Data directory for persistent storage (Railway volume mount point)
DATA_DIR = os.getenv("DATA_DIR", "/app/data")

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


def ensure_data_dir():
    """Ensure data directory exists. Call this at app startup."""
    os.makedirs(DATA_DIR, exist_ok=True)
