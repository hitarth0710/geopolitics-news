"""Production-ready Main FastAPI application."""
import asyncio
import os
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from fastapi import FastAPI, Request, Query, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from .settings import settings
from .logging_config import logger, setup_logging
from .database import init_db, SessionLocal, get_db
from .models import Article, Category, Region, Source, ReadingHistory
from .routes.articles import router as articles_router
from .routes.auth_routes import router as auth_router
from .routes.profile_routes import router as profile_router
from .routes.bookmarks import router as bookmarks_router
from .services import init_sources, init_categories, init_regions, store_articles
from .feeds.rss_parser import fetch_all_feeds
from .middleware import setup_middleware
from .exceptions import setup_exception_handlers
from .cache import cache
from .schemas import DetailedHealthStatus, HealthStatus
from .auth import get_current_user, cleanup_expired_sessions

# Reconfigure logging based on settings
setup_logging(
    level=settings.log_level,
    json_logs=settings.log_json,
    log_file=settings.log_file
)

# Scheduler for background tasks
scheduler = AsyncIOScheduler()

# Track last feed update
last_feed_update: datetime = None


async def update_feeds():
    """Background task to fetch and store new articles."""
    global last_feed_update
    
    logger.info("Starting feed update...")
    start_time = datetime.utcnow()
    
    try:
        articles = await fetch_all_feeds()
        
        db = SessionLocal()
        try:
            new_count = store_articles(db, articles)
            last_feed_update = datetime.utcnow()
            
            # Clear article cache after update
            await cache.clear()
            
            duration = (datetime.utcnow() - start_time).total_seconds()
            logger.info(
                f"Feed update complete: {new_count} new articles in {duration:.2f}s",
                extra={"new_articles": new_count, "duration": duration}
            )
        finally:
            db.close()
    except Exception as e:
        logger.exception(f"Feed update failed: {e}")


async def cleanup_cache():
    """Periodic cache cleanup."""
    removed = await cache.cleanup_expired()
    if removed > 0:
        logger.debug(f"Cache cleanup: removed {removed} expired entries")


async def cleanup_sessions():
    """Periodic session cleanup."""
    db = SessionLocal()
    try:
        cleanup_expired_sessions(db)
        logger.debug("Expired sessions cleaned up")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    logger.info(f"Starting {settings.app_name} in {settings.environment} mode...")
    
    # Initialize database
    init_db()
    logger.info("Database initialized")
    
    # Initialize reference data
    db = SessionLocal()
    try:
        init_sources(db)
        init_categories(db)
        init_regions(db)
        logger.info("Reference data initialized")
    finally:
        db.close()
    
    # Start scheduler for periodic updates (initial fetch happens after startup)
    scheduler.add_job(
        update_feeds, 
        'interval', 
        minutes=settings.feed_update_interval,
        id='feed_update',
        replace_existing=True
    )
    scheduler.add_job(
        cleanup_cache,
        'interval',
        minutes=5,
        id='cache_cleanup',
        replace_existing=True
    )
    scheduler.add_job(
        cleanup_sessions,
        'interval',
        hours=1,
        id='session_cleanup',
        replace_existing=True
    )
    scheduler.start()
    logger.info(f"Scheduler started - feeds update every {settings.feed_update_interval} minutes")
    
    # Schedule initial feed fetch to run after startup (delayed by 5 seconds to let health checks pass)
    scheduler.add_job(
        update_feeds,
        'date',
        run_date=datetime.now() + timedelta(seconds=5),
        id='initial_feed_fetch'
    )
    logger.info("Initial feed fetch scheduled")
    
    yield
    
    # Shutdown
    scheduler.shutdown(wait=False)
    await cache.clear()
    logger.info("Application shutdown complete")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version="1.0.0",
    docs_url="/api/docs" if settings.debug else None,
    redoc_url="/api/redoc" if settings.debug else None,
    lifespan=lifespan
)

# Setup middleware
setup_middleware(app)

# Setup exception handlers
setup_exception_handlers(app)

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Templates
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

# Include API routers
app.include_router(articles_router)
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(bookmarks_router)


# ============= Health Check Endpoints =============

@app.get("/health", response_model=HealthStatus, tags=["health"])
async def health_check():
    """Basic health check endpoint."""
    return HealthStatus(
        status="healthy",
        environment=settings.environment,
        version="1.0.0",
        timestamp=datetime.utcnow()
    )


@app.get("/health/detailed", response_model=DetailedHealthStatus, tags=["health"])
async def detailed_health_check(db: Session = Depends(get_db)):
    """Detailed health check with component status."""
    try:
        article_count = db.query(func.count(Article.id)).scalar()
        source_count = db.query(func.count(Source.id)).scalar()
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "unhealthy"
        article_count = 0
        source_count = 0
    
    scheduler_status = "healthy" if scheduler.running else "stopped"
    
    return DetailedHealthStatus(
        status="healthy" if db_status == "healthy" else "degraded",
        environment=settings.environment,
        version="1.0.0",
        timestamp=datetime.utcnow(),
        database=db_status,
        scheduler=scheduler_status,
        last_feed_update=last_feed_update,
        total_articles=article_count,
        total_sources=source_count
    )


@app.post("/api/refresh", tags=["admin"])
async def trigger_refresh():
    """Manually trigger feed refresh."""
    asyncio.create_task(update_feeds())
    return {"message": "Feed refresh triggered", "status": "pending"}


# ============= Page Routes =============

@app.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    category: str = Query(None, description="Filter by category"),
    region: str = Query(None, description="Filter by region"),
    search: str = Query(None, description="Search query"),
    date: str = Query(None, description="Filter by date (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="Page number"),
    db: Session = Depends(get_db)
):
    """Home page with article listing."""
    from datetime import timedelta
    
    per_page = 20
    offset = (page - 1) * per_page
    
    # Get filter options
    categories = db.query(Category).all()
    regions = db.query(Region).all()
    sources = db.query(Source).filter(Source.is_active == True).all()
    
    # Build query
    query = db.query(Article).order_by(desc(Article.published_at))
    
    if category:
        cat = db.query(Category).filter(Category.slug == category).first()
        if cat:
            query = query.filter(Article.category_id == cat.id)
    
    if region:
        reg = db.query(Region).filter(Region.slug == region).first()
        if reg:
            query = query.filter(Article.region_id == reg.id)
    
    if search:
        query = query.filter(
            Article.title.ilike(f"%{search}%") | 
            Article.summary.ilike(f"%{search}%")
        )
    
    # Date filtering
    if date:
        try:
            filter_date = datetime.strptime(date, "%Y-%m-%d")
            next_date = filter_date + timedelta(days=1)
            query = query.filter(
                Article.published_at >= filter_date,
                Article.published_at < next_date
            )
        except ValueError:
            date = None  # Invalid date format, ignore
    
    # Get total count for pagination
    total = query.count()
    total_pages = (total + per_page - 1) // per_page
    
    articles = query.offset(offset).limit(per_page).all()
    
    # Get current user if logged in
    user = get_current_user(db, request)
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "app_name": settings.app_name,
        "articles": articles,
        "categories": categories,
        "regions": regions,
        "sources": sources,
        "current_category": category,
        "current_region": region,
        "search_query": search,
        "current_date": date,
        "current_page": page,
        "total_pages": total_pages,
        "total_articles": total,
        "user": user,
    })


@app.get("/article/{article_id}", response_class=HTMLResponse)
async def article_detail(
    request: Request, 
    article_id: int,
    db: Session = Depends(get_db)
):
    """Article detail page."""
    article = db.query(Article).filter(Article.id == article_id).first()
    
    if not article:
        return templates.TemplateResponse("404.html", {
            "request": request,
            "app_name": settings.app_name,
        }, status_code=404)
    
    # Get related articles
    related = db.query(Article).filter(
        Article.id != article_id,
        (Article.category_id == article.category_id) | 
        (Article.region_id == article.region_id)
    ).order_by(desc(Article.published_at)).limit(5).all()
    
    # Get current user and check bookmark status
    user = get_current_user(db, request)
    is_saved = False
    if user:
        is_saved = article in user.saved_articles
        # Add to reading history
        history = ReadingHistory(user_id=user.id, article_id=article_id)
        db.add(history)
        db.commit()
    
    return templates.TemplateResponse("article.html", {
        "request": request,
        "app_name": settings.app_name,
        "article": article,
        "related": related,
        "user": user,
        "is_saved": is_saved,
    })


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request, db: Session = Depends(get_db)):
    """About page."""
    sources = db.query(Source).filter(Source.is_active == True).all()
    article_count = db.query(func.count(Article.id)).scalar()
    user = get_current_user(db, request)
    
    return templates.TemplateResponse("about.html", {
        "request": request,
        "app_name": settings.app_name,
        "sources": sources,
        "article_count": article_count,
        "last_update": last_feed_update,
        "user": user,
    })
