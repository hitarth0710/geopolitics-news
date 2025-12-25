"""Simple in-memory caching layer."""
import asyncio
from datetime import datetime, timedelta
from typing import Any, Optional, Dict, Callable
from functools import wraps
import hashlib
import json

from .settings import settings


class SimpleCache:
    """Thread-safe in-memory cache with TTL support."""
    
    def __init__(self, default_ttl: int = 300):
        self._cache: Dict[str, tuple[Any, datetime]] = {}
        self._default_ttl = default_ttl
        self._lock = asyncio.Lock()
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired."""
        if not settings.cache_enabled:
            return None
        
        async with self._lock:
            if key in self._cache:
                value, expires_at = self._cache[key]
                if datetime.utcnow() < expires_at:
                    return value
                else:
                    del self._cache[key]
        return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache with TTL."""
        if not settings.cache_enabled:
            return
        
        ttl = ttl or self._default_ttl
        expires_at = datetime.utcnow() + timedelta(seconds=ttl)
        
        async with self._lock:
            self._cache[key] = (value, expires_at)
    
    async def delete(self, key: str) -> None:
        """Delete key from cache."""
        async with self._lock:
            self._cache.pop(key, None)
    
    async def clear(self) -> None:
        """Clear all cached data."""
        async with self._lock:
            self._cache.clear()
    
    async def cleanup_expired(self) -> int:
        """Remove expired entries. Returns count of removed items."""
        now = datetime.utcnow()
        removed = 0
        
        async with self._lock:
            expired_keys = [
                key for key, (_, expires_at) in self._cache.items()
                if now >= expires_at
            ]
            for key in expired_keys:
                del self._cache[key]
                removed += 1
        
        return removed
    
    @property
    def size(self) -> int:
        """Get current cache size."""
        return len(self._cache)


# Global cache instance
cache = SimpleCache(default_ttl=settings.cache_ttl)


def make_cache_key(*args, **kwargs) -> str:
    """Generate a cache key from arguments."""
    key_data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True, default=str)
    return hashlib.md5(key_data.encode()).hexdigest()


def cached(ttl: Optional[int] = None, prefix: str = ""):
    """Decorator for caching async function results.
    
    Usage:
        @cached(ttl=60, prefix="articles")
        async def get_articles(category: str):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not settings.cache_enabled:
                return await func(*args, **kwargs)
            
            # Generate cache key
            key = f"{prefix}:{func.__name__}:{make_cache_key(*args, **kwargs)}"
            
            # Try to get from cache
            cached_value = await cache.get(key)
            if cached_value is not None:
                return cached_value
            
            # Call function and cache result
            result = await func(*args, **kwargs)
            await cache.set(key, result, ttl)
            
            return result
        
        return wrapper
    return decorator
