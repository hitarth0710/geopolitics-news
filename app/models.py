"""Database models for the geopolitics news aggregator."""
from datetime import datetime
import hashlib
import secrets
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship

from .database import Base


# Association table for saved articles (many-to-many)
saved_articles = Table(
    'saved_articles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('article_id', Integer, ForeignKey('articles.id'), primary_key=True),
    Column('saved_at', DateTime, default=datetime.utcnow)
)


class User(Base):
    """User account for authentication."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    
    # Preferences
    preferred_categories = Column(String(500), nullable=True)  # Comma-separated category slugs
    preferred_regions = Column(String(500), nullable=True)  # Comma-separated region slugs
    dark_mode = Column(Boolean, default=True)
    email_digest = Column(Boolean, default=False)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    saved_articles = relationship("Article", secondary=saved_articles, backref="saved_by_users")
    reading_history = relationship("ReadingHistory", back_populates="user", cascade="all, delete-orphan")
    
    def set_password(self, password: str):
        """Hash and set password."""
        # Using SHA-256 with salt for simplicity (use bcrypt in production)
        salt = secrets.token_hex(16)
        password_hash = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
        self.password_hash = f"{salt}${password_hash}"
    
    def verify_password(self, password: str) -> bool:
        """Verify password against stored hash."""
        try:
            salt, stored_hash = self.password_hash.split('$')
            password_hash = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
            return password_hash == stored_hash
        except (ValueError, AttributeError):
            return False
    
    def get_gravatar_url(self, size: int = 80) -> str:
        """Get Gravatar URL for user's email."""
        email_hash = hashlib.md5(self.email.lower().encode()).hexdigest()
        return f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d=identicon"
    
    @property
    def display_name(self) -> str:
        """Get display name (full name or username)."""
        return self.full_name or self.username
    
    @property
    def preferred_category_list(self) -> list:
        """Get list of preferred category slugs."""
        if self.preferred_categories:
            return [c.strip() for c in self.preferred_categories.split(',')]
        return []
    
    @property
    def preferred_region_list(self) -> list:
        """Get list of preferred region slugs."""
        if self.preferred_regions:
            return [r.strip() for r in self.preferred_regions.split(',')]
        return []


class ReadingHistory(Base):
    """Track articles read by users."""
    __tablename__ = "reading_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    read_at = Column(DateTime, default=datetime.utcnow)
    read_time_seconds = Column(Integer, nullable=True)  # Estimated reading time
    
    user = relationship("User", back_populates="reading_history")
    article = relationship("Article")


class Session(Base):
    """User session for authentication."""
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(64), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    
    user = relationship("User")
    
    @property
    def is_expired(self) -> bool:
        """Check if session has expired."""
        return datetime.utcnow() > self.expires_at


class Source(Base):
    """News source (e.g., BBC, Reuters, Al Jazeera)."""
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    url = Column(String(500), nullable=False)
    feed_url = Column(String(500), nullable=True)  # RSS feed URL
    logo_url = Column(String(500), nullable=True)
    region = Column(String(50), nullable=True)  # Primary region focus
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    articles = relationship("Article", back_populates="source")


class Category(Base):
    """Article category (e.g., Diplomacy, Conflicts, Trade)."""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    slug = Column(String(50), unique=True, nullable=False)
    icon = Column(String(10), nullable=True)  # Emoji icon
    description = Column(String(200), nullable=True)

    articles = relationship("Article", back_populates="category")


class Region(Base):
    """Geographic region (e.g., Europe, Middle East, Asia-Pacific)."""
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    slug = Column(String(50), unique=True, nullable=False)
    icon = Column(String(10), nullable=True)  # Emoji flag/icon

    articles = relationship("Article", back_populates="region")


class Article(Base):
    """News article."""
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    url = Column(String(1000), unique=True, nullable=False)  # Original article URL
    summary = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    image_url = Column(String(1000), nullable=True)
    author = Column(String(200), nullable=True)
    published_at = Column(DateTime, nullable=True)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    
    # Foreign keys
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=True)

    # Relationships
    source = relationship("Source", back_populates="articles")
    category = relationship("Category", back_populates="articles")
    region = relationship("Region", back_populates="articles")

    def __repr__(self):
        return f"<Article {self.title[:50]}...>"
