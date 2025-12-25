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
_db_url = None


def _wait_for_volume(max_wait_seconds=30):
    """Wait for the Railway volume to be mounted."""
    # Railway volume can be at /data or custom path from env
    mount_path = os.environ.get("RAILWAY_VOLUME_MOUNT_PATH") or os.environ.get("DATA_DIR") or "/data"
    start_time = time.time()
    
    print(f"🔄 Waiting for volume at {mount_path}...")
    
    while time.time() - start_time < max_wait_seconds:
        try:
            # Check if the mount path exists and is writable
            os.makedirs(mount_path, exist_ok=True)
            test_file = os.path.join(mount_path, ".volume_test")
            
            with open(test_file, "w") as f:
                f.write(f"test-{time.time()}")
            
            # Verify we can read it back
            with open(test_file, "r") as f:
                content = f.read()
            
            os.remove(test_file)
            
            if content:
                print(f"✅ Volume mounted successfully at {mount_path}")
                return mount_path
                
        except (OSError, IOError, PermissionError) as e:
            elapsed = int(time.time() - start_time)
            print(f"⏳ Waiting for volume... ({elapsed}s) - {e}")
            time.sleep(1)
    
    print(f"⚠️ Volume not available after {max_wait_seconds}s")
    return None


def get_database_url():
    """Get the database URL, waiting for volume if needed."""
    global _db_url
    
    if _db_url is not None:
        return _db_url
    
    # Check if we're on Railway with a volume
    volume_mount = os.environ.get("RAILWAY_VOLUME_MOUNT_PATH")
    
    if volume_mount:
        # Wait for Railway volume to be ready
        ready_path = _wait_for_volume(max_wait_seconds=30)
        
        if ready_path:
            _db_url = f"sqlite:///{ready_path}/geopolitics_news.db"
            print(f"📀 Database: {_db_url}")
            return _db_url
    
    # Check if DATA_DIR is accessible (for local development)
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        test_file = os.path.join(DATA_DIR, ".test")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        _db_url = DATABASE_URL
        print(f"📀 Database (local): {_db_url}")
        return _db_url
    except (OSError, IOError, PermissionError):
        pass
    
    # Last resort fallback - NOT persistent but allows app to start
    print("⚠️ WARNING: Using non-persistent /tmp database!")
    fallback_dir = "/tmp/geopolitics_data"
    os.makedirs(fallback_dir, exist_ok=True)
    _db_url = f"sqlite:///{fallback_dir}/geopolitics_news.db"
    return _db_url


def get_engine():
    """Get or create the database engine."""
    global _engine
    if _engine is None:
        db_url = get_database_url()
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
