"""Database setup and session management."""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import DATABASE_URL, DATA_DIR

# Create Base first
Base = declarative_base()

# Engine and SessionLocal will be created lazily
_engine = None
_SessionLocal = None


def get_engine():
    """Get or create the database engine."""
    global _engine
    if _engine is None:
        # Ensure data directory exists
        os.makedirs(DATA_DIR, exist_ok=True)
        _engine = create_engine(
            DATABASE_URL, 
            connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
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
