"""Production middleware for security and performance."""
import time
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Callable, Dict
from fastapi import Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from .settings import settings
from .logging_config import logger


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple rate limiting middleware."""
    
    def __init__(self, app, requests_per_minute: int = 100):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            client_ip = forwarded.split(",")[0].strip()
        
        # Clean old requests
        now = datetime.utcnow()
        minute_ago = now - timedelta(minutes=1)
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if req_time > minute_ago
        ]
        
        # Check rate limit
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            logger.warning(f"Rate limit exceeded for {client_ip}")
            return Response(
                content='{"detail": "Rate limit exceeded. Try again later."}',
                status_code=429,
                media_type="application/json",
                headers={"Retry-After": "60"}
            )
        
        # Record request
        self.requests[client_ip].append(now)
        
        return await call_next(request)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests with timing information."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Get request info
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = (time.time() - start_time) * 1000  # ms
        
        # Log request
        logger.info(
            f"{method} {path} - {response.status_code} - {duration:.2f}ms",
            extra={
                "client_ip": client_ip,
                "method": method,
                "path": path,
                "status_code": response.status_code,
                "duration_ms": round(duration, 2)
            }
        )
        
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Cache control for static assets
        if request.url.path.startswith("/static"):
            response.headers["Cache-Control"] = "public, max-age=31536000"
        
        return response


def setup_middleware(app):
    """Configure all middleware for the application."""
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Security headers
    app.add_middleware(SecurityHeadersMiddleware)
    
    # Rate limiting (skip in debug mode)
    if not settings.debug:
        app.add_middleware(
            RateLimitMiddleware,
            requests_per_minute=settings.rate_limit_requests
        )
    
    # Request logging
    app.add_middleware(RequestLoggingMiddleware)
