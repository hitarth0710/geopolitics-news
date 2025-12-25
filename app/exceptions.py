"""Custom exceptions and error handlers."""
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import os

from .logging_config import logger
from .settings import settings

# Templates for error pages
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)


class AppException(Exception):
    """Base application exception."""
    
    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class FeedFetchError(AppException):
    """Error fetching RSS feed."""
    
    def __init__(self, feed_url: str, original_error: str):
        super().__init__(
            message=f"Failed to fetch feed: {feed_url}",
            status_code=503,
            details={"feed_url": feed_url, "error": original_error}
        )


class DatabaseError(AppException):
    """Database operation error."""
    
    def __init__(self, operation: str, original_error: str):
        super().__init__(
            message=f"Database error during {operation}",
            status_code=500,
            details={"operation": operation, "error": original_error}
        )


class ArticleNotFoundError(AppException):
    """Article not found error."""
    
    def __init__(self, article_id: int):
        super().__init__(
            message=f"Article with ID {article_id} not found",
            status_code=404,
            details={"article_id": article_id}
        )


async def app_exception_handler(request: Request, exc: AppException):
    """Handle custom application exceptions."""
    logger.error(f"{exc.message}", extra=exc.details)
    
    # Return HTML for browser requests, JSON for API
    accept = request.headers.get("accept", "")
    
    if "text/html" in accept and not request.url.path.startswith("/api"):
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "app_name": settings.app_name,
                "status_code": exc.status_code,
                "message": exc.message,
            },
            status_code=exc.status_code
        )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.message,
            "details": exc.details if settings.debug else {}
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    accept = request.headers.get("accept", "")
    
    if "text/html" in accept and not request.url.path.startswith("/api"):
        template_name = "404.html" if exc.status_code == 404 else "error.html"
        return templates.TemplateResponse(
            template_name,
            {
                "request": request,
                "app_name": settings.app_name,
                "status_code": exc.status_code,
                "message": exc.detail,
            },
            status_code=exc.status_code
        )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": True, "message": exc.detail}
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.exception(f"Unexpected error: {exc}")
    
    accept = request.headers.get("accept", "")
    
    if "text/html" in accept and not request.url.path.startswith("/api"):
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "app_name": settings.app_name,
                "status_code": 500,
                "message": "An unexpected error occurred" if not settings.debug else str(exc),
            },
            status_code=500
        )
    
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "details": {"error": str(exc)} if settings.debug else {}
        }
    )


def setup_exception_handlers(app):
    """Register exception handlers."""
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
