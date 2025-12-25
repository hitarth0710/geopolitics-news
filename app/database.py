"""Database setup and session management."""
import os
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import DATABASE_URL, DATA_DIR

# Create Base first
Base = declarative_base()

# Engine and SessionLocal will be created lazily
_engine = None
_SessionLocal = None


def _ensure_data_dir_with_retry(max_retries=5, delay=1):
    """Ensure data directory exists, with retries for volume mounting."""
    for attempt in range(max_retries):
        try:
            os.makedirs(DATA_DIR, exist_ok=True)
            # Test if we can write to the directory
            test_file = os.path.join(DATA_DIR, ".write_test")
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
            return True
        except (OSError, IOError) as e:
            if attempt < max_retries - 1:
                print(f"Waiting for volume mount (attempt {attempt + 1}/{max_retries})...")
                time.sleep(delay)
            else:
                print(f"Could not access data directory after {max_retries} attempts: {e}")
                return False
    return False


def get_engine():
    """Get or create the database engine."""
    global _engine
    if _engine is None:
        # Ensure data directory exists with retry
        if not _ensure_data_dir_with_retry():
            # Fallback to local directory
            local_data_dir = "/tmp/geopolitics_data"
            os.makedirs(local_data_dir, exist_ok=True)
            db_url = f"sqlite:///{local_data_dir}/geopolitics_news.db"
            print(f"Using fallback database at {db_url}")
        else:
            db_url = DATABASE_URL
            print(f"Using primary database at {db_url}")
        
        _engine = create_engine(
            db_url, 
            connect_args={"check_same_thread": False} if "sqlite" in db_url else {}
        )
    return _engine


def get_session_local():
    """Get or create the session factory."""
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return _SessionLocal


# Alias for backwards compatibility
def SessionLocal():
    """Create a new database session (backwards compatible)."""
    return get_session_local()()


def get_db():
    """Dependency for getting database session."""
    session_factory = get_session_local()
    db = session_factory()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    from . import models  # noqa
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
