"""Bookmark/Save article API routes."""
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, Article, ReadingHistory
from ..auth import get_current_user

router = APIRouter(prefix="/api/bookmarks", tags=["bookmarks"])


@router.post("/{article_id}")
async def save_article(
    article_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Save an article to user's bookmarks."""
    user = get_current_user(db, request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    # Get article
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Check if already saved
    if article in user.saved_articles:
        return JSONResponse({
            "status": "already_saved",
            "message": "Article already in bookmarks"
        })
    
    # Add to saved articles
    user.saved_articles.append(article)
    db.commit()
    
    return JSONResponse({
        "status": "saved",
        "message": "Article saved to bookmarks"
    })


@router.delete("/{article_id}")
async def unsave_article(
    article_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Remove an article from user's bookmarks."""
    user = get_current_user(db, request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    # Get article
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Check if saved
    if article not in user.saved_articles:
        return JSONResponse({
            "status": "not_saved",
            "message": "Article not in bookmarks"
        })
    
    # Remove from saved articles
    user.saved_articles.remove(article)
    db.commit()
    
    return JSONResponse({
        "status": "removed",
        "message": "Article removed from bookmarks"
    })


@router.get("")
async def get_bookmarks(
    request: Request,
    db: Session = Depends(get_db),
    page: int = 1,
    limit: int = 20
):
    """Get user's bookmarked articles."""
    user = get_current_user(db, request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    # Pagination
    total = len(user.saved_articles)
    start = (page - 1) * limit
    end = start + limit
    articles = user.saved_articles[start:end]
    
    return {
        "articles": [
            {
                "id": a.id,
                "title": a.title,
                "summary": a.summary,
                "source": a.source.name if a.source else None,
                "published_at": a.published_at.isoformat() if a.published_at else None,
                "image_url": a.image_url
            }
            for a in articles
        ],
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit
    }


@router.get("/check/{article_id}")
async def check_bookmark(
    article_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Check if article is bookmarked."""
    user = get_current_user(db, request)
    if not user:
        return {"is_saved": False, "authenticated": False}
    
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    is_saved = article in user.saved_articles
    
    return {"is_saved": is_saved, "authenticated": True}


@router.post("/history/{article_id}")
async def add_to_history(
    article_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Add article to user's reading history."""
    user = get_current_user(db, request)
    if not user:
        return {"status": "skipped", "message": "Not authenticated"}
    
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Add to reading history (allow duplicates for tracking)
    history = ReadingHistory(
        user_id=user.id,
        article_id=article_id
    )
    db.add(history)
    db.commit()
    
    return {"status": "added", "message": "Added to reading history"}
