"""Profile and user account routes."""
from datetime import datetime
from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from ..models import User, Article, ReadingHistory, saved_articles, Category, Region
from ..auth import get_current_user, validate_password

router = APIRouter(prefix="/profile", tags=["profile"])
templates = Jinja2Templates(directory="app/templates")


def require_auth(db: Session, request: Request) -> User:
    """Helper to require authentication."""
    user = get_current_user(db, request)
    if not user:
        raise HTTPException(status_code=302, headers={"Location": "/login?next=/profile"})
    return user


@router.get("", response_class=HTMLResponse)
async def profile_page(
    request: Request,
    db: Session = Depends(get_db)
):
    """Render user profile page."""
    user = get_current_user(db, request)
    if not user:
        return RedirectResponse(url="/login?next=/profile", status_code=302)
    
    # Get saved articles count
    saved_count = len(user.saved_articles)
    
    # Get reading history count
    history_count = db.query(ReadingHistory).filter(
        ReadingHistory.user_id == user.id
    ).count()
    
    # Get recent saved articles (last 5)
    recent_saved = user.saved_articles[:5]
    
    # Get account age in days
    account_age = (datetime.utcnow() - user.created_at).days
    
    # Get categories and regions for preferences
    categories = db.query(Category).all()
    regions = db.query(Region).all()
    
    return templates.TemplateResponse(
        "profile/dashboard.html",
        {
            "request": request,
            "user": user,
            "saved_count": saved_count,
            "history_count": history_count,
            "recent_saved": recent_saved,
            "account_age": account_age,
            "categories": categories,
            "regions": regions,
            "success": request.query_params.get("success"),
            "error": request.query_params.get("error")
        }
    )


@router.get("/saved", response_class=HTMLResponse)
async def saved_articles_page(
    request: Request,
    db: Session = Depends(get_db),
    page: int = 1
):
    """Render saved articles page."""
    user = get_current_user(db, request)
    if not user:
        return RedirectResponse(url="/login?next=/profile/saved", status_code=302)
    
    per_page = 12
    
    # Get saved articles with pagination
    total = len(user.saved_articles)
    total_pages = (total + per_page - 1) // per_page
    
    # Manual pagination on the relationship
    start = (page - 1) * per_page
    end = start + per_page
    articles = user.saved_articles[start:end]
    
    return templates.TemplateResponse(
        "profile/saved.html",
        {
            "request": request,
            "user": user,
            "articles": articles,
            "page": page,
            "total_pages": total_pages,
            "total": total
        }
    )


@router.get("/history", response_class=HTMLResponse)
async def reading_history_page(
    request: Request,
    db: Session = Depends(get_db),
    page: int = 1
):
    """Render reading history page."""
    user = get_current_user(db, request)
    if not user:
        return RedirectResponse(url="/login?next=/profile/history", status_code=302)
    
    per_page = 20
    
    # Get reading history with pagination
    total = db.query(ReadingHistory).filter(
        ReadingHistory.user_id == user.id
    ).count()
    
    total_pages = (total + per_page - 1) // per_page
    
    history_items = db.query(ReadingHistory).filter(
        ReadingHistory.user_id == user.id
    ).order_by(ReadingHistory.read_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
    
    return templates.TemplateResponse(
        "profile/history.html",
        {
            "request": request,
            "user": user,
            "history_items": history_items,
            "page": page,
            "total_pages": total_pages,
            "total": total
        }
    )


@router.get("/settings", response_class=HTMLResponse)
async def settings_page(
    request: Request,
    db: Session = Depends(get_db)
):
    """Render account settings page."""
    user = get_current_user(db, request)
    if not user:
        return RedirectResponse(url="/login?next=/profile/settings", status_code=302)
    
    # Get categories and regions for preferences
    categories = db.query(Category).all()
    regions = db.query(Region).all()
    
    return templates.TemplateResponse(
        "profile/settings.html",
        {
            "request": request,
            "user": user,
            "categories": categories,
            "regions": regions,
            "success": request.query_params.get("success"),
            "error": request.query_params.get("error")
        }
    )


@router.post("/settings/profile")
async def update_profile(
    request: Request,
    db: Session = Depends(get_db),
    full_name: str = Form(""),
    bio: str = Form("")
):
    """Update user profile information."""
    user = get_current_user(db, request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    user.full_name = full_name.strip() if full_name else None
    user.bio = bio.strip() if bio else None
    user.updated_at = datetime.utcnow()
    
    db.commit()
    
    return RedirectResponse(
        url="/profile/settings?success=Profile+updated+successfully",
        status_code=302
    )


@router.post("/settings/preferences")
async def update_preferences(
    request: Request,
    db: Session = Depends(get_db),
    dark_mode: bool = Form(True),
    email_digest: bool = Form(False),
    categories: list = Form([]),
    regions: list = Form([])
):
    """Update user preferences."""
    user = get_current_user(db, request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    form_data = await request.form()
    categories = form_data.getlist("categories")
    regions = form_data.getlist("regions")
    
    user.dark_mode = "dark_mode" in form_data
    user.email_digest = "email_digest" in form_data
    user.preferred_categories = ",".join(categories) if categories else None
    user.preferred_regions = ",".join(regions) if regions else None
    user.updated_at = datetime.utcnow()
    
    db.commit()
    
    return RedirectResponse(
        url="/profile/settings?success=Preferences+updated+successfully",
        status_code=302
    )


@router.post("/settings/password")
async def change_password(
    request: Request,
    db: Session = Depends(get_db),
    current_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...)
):
    """Change user password."""
    user = get_current_user(db, request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    # Verify current password
    if not user.verify_password(current_password):
        return RedirectResponse(
            url="/profile/settings?error=Current+password+is+incorrect",
            status_code=302
        )
    
    # Validate new password
    valid, msg = validate_password(new_password)
    if not valid:
        return RedirectResponse(
            url=f"/profile/settings?error={msg.replace(' ', '+')}",
            status_code=302
        )
    
    # Check confirmation
    if new_password != confirm_password:
        return RedirectResponse(
            url="/profile/settings?error=Passwords+do+not+match",
            status_code=302
        )
    
    # Update password
    user.set_password(new_password)
    user.updated_at = datetime.utcnow()
    
    db.commit()
    
    return RedirectResponse(
        url="/profile/settings?success=Password+changed+successfully",
        status_code=302
    )


@router.post("/settings/delete-account")
async def delete_account(
    request: Request,
    db: Session = Depends(get_db),
    confirm_password: str = Form(...)
):
    """Delete user account."""
    user = get_current_user(db, request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    # Verify password
    if not user.verify_password(confirm_password):
        return RedirectResponse(
            url="/profile/settings?error=Password+is+incorrect",
            status_code=302
        )
    
    # Delete user (cascade will handle related records)
    db.delete(user)
    db.commit()
    
    # Clear session and redirect
    from ..auth import clear_session_cookie
    response = RedirectResponse(url="/?deleted=true", status_code=302)
    clear_session_cookie(response)
    
    return response
