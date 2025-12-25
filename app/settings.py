"""Production-ready settings using Pydantic Settings."""
from functools import lru_cache
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application
    app_name: str = Field(default="GeoPolitics Watch", description="Application name")
    app_description: str = Field(default="Your window to world geopolitics", description="App description")
    debug: bool = Field(default=False, description="Debug mode")
    environment: str = Field(default="development", description="Environment (development/staging/production)")
    
    # Server
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    workers: int = Field(default=1, description="Number of worker processes")
    
    # Database
    database_url: str = Field(default="sqlite:///./geopolitics_news.db", description="Database connection URL")
    db_pool_size: int = Field(default=5, description="Database connection pool size")
    db_max_overflow: int = Field(default=10, description="Max overflow connections")
    
    # Security
    secret_key: str = Field(default="change-me-in-production-use-strong-key", description="Secret key for signing")
    allowed_origins: List[str] = Field(default=["*"], description="CORS allowed origins")
    rate_limit_requests: int = Field(default=100, description="Rate limit requests per minute")
    
    # News API (optional)
    news_api_key: Optional[str] = Field(default=None, description="NewsAPI.org API key")
    
    # Feed settings
    feed_update_interval: int = Field(default=30, description="Feed update interval in minutes")
    feed_timeout: int = Field(default=30, description="Feed fetch timeout in seconds")
    max_articles_per_feed: int = Field(default=50, description="Max articles to fetch per feed")
    
    # Caching
    cache_ttl: int = Field(default=300, description="Cache TTL in seconds")
    cache_enabled: bool = Field(default=True, description="Enable caching")
    
    # Logging
    log_level: str = Field(default="INFO", description="Log level")
    log_json: bool = Field(default=False, description="Use JSON logging format")
    log_file: Optional[str] = Field(default=None, description="Log file path")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Convenience access
settings = get_settings()
