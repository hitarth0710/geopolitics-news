"""Article API routes."""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, List

from ..database import get_db
from ..models import Article, Source, Category, Region

router = APIRouter(prefix="/api/articles", tags=["articles"])


@router.get("/")
async def get_articles(
    db: Session = Depends(get_db),
    category: Optional[str] = Query(None, description="Filter by category slug"),
    region: Optional[str] = Query(None, description="Filter by region slug"),
    source: Optional[str] = Query(None, description="Filter by source name"),
    search: Optional[str] = Query(None, description="Search in title/summary"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Get articles with optional filtering."""
    query = db.query(Article).order_by(desc(Article.published_at))
    
    # Apply filters
    if category:
        cat = db.query(Category).filter(Category.slug == category).first()
        if cat:
            query = query.filter(Article.category_id == cat.id)
    
    if region:
        reg = db.query(Region).filter(Region.slug == region).first()
        if reg:
            query = query.filter(Article.region_id == reg.id)
    
    if source:
        src = db.query(Source).filter(Source.name.ilike(f"%{source}%")).first()
        if src:
            query = query.filter(Article.source_id == src.id)
    
    if search:
        query = query.filter(
            Article.title.ilike(f"%{search}%") | 
            Article.summary.ilike(f"%{search}%")
        )
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    articles = query.offset(offset).limit(limit).all()
    
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "articles": [
            {
                "id": a.id,
                "title": a.title,
                "url": a.url,
                "summary": a.summary,
                "image_url": a.image_url,
                "author": a.author,
                "published_at": a.published_at.isoformat() if a.published_at else None,
                "source": a.source.name if a.source else None,
                "source_logo": a.source.logo_url if a.source else None,
                "category": {
                    "name": a.category.name,
                    "slug": a.category.slug,
                    "icon": a.category.icon
                } if a.category else None,
                "region": {
                    "name": a.region.name,
                    "slug": a.region.slug,
                    "icon": a.region.icon
                } if a.region else None,
            }
            for a in articles
        ]
    }


@router.get("/{article_id}")
async def get_article(article_id: int, db: Session = Depends(get_db)):
    """Get a single article by ID."""
    article = db.query(Article).filter(Article.id == article_id).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    return {
        "id": article.id,
        "title": article.title,
        "url": article.url,
        "summary": article.summary,
        "content": article.content,
        "image_url": article.image_url,
        "author": article.author,
        "published_at": article.published_at.isoformat() if article.published_at else None,
        "fetched_at": article.fetched_at.isoformat() if article.fetched_at else None,
        "source": {
            "name": article.source.name,
            "url": article.source.url,
            "logo_url": article.source.logo_url
        } if article.source else None,
        "category": {
            "name": article.category.name,
            "slug": article.category.slug,
            "icon": article.category.icon
        } if article.category else None,
        "region": {
            "name": article.region.name,
            "slug": article.region.slug,
            "icon": article.region.icon
        } if article.region else None,
    }


@router.get("/sources/list")
async def get_sources(db: Session = Depends(get_db)):
    """Get all available sources."""
    sources = db.query(Source).filter(Source.is_active == True).all()
    return [
        {
            "id": s.id,
            "name": s.name,
            "url": s.url,
            "logo_url": s.logo_url,
            "article_count": len(s.articles)
        }
        for s in sources
    ]


@router.get("/categories/list")
async def get_categories(db: Session = Depends(get_db)):
    """Get all categories."""
    categories = db.query(Category).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "slug": c.slug,
            "icon": c.icon,
            "description": c.description,
            "article_count": len(c.articles)
        }
        for c in categories
    ]


@router.get("/regions/list")
async def get_regions(db: Session = Depends(get_db)):
    """Get all regions."""
    regions = db.query(Region).all()
    return [
        {
            "id": r.id,
            "name": r.name,
            "slug": r.slug,
            "icon": r.icon,
            "article_count": len(r.articles)
        }
        for r in regions
    ]
