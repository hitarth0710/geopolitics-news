"""Authentication routes for login, register, logout."""
from datetime import datetime
from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..auth import (
    create_session, 
    set_session_cookie, 
    clear_session_cookie,
    invalidate_session,
    get_current_user,
    validate_password,
    validate_email,
    validate_username,
    SESSION_COOKIE_NAME
)

router = APIRouter(tags=["auth"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse)
async def login_page(
    request: Request, 
    db: Session = Depends(get_db),
    next: str = "/"
):
    """Render login page."""
    # If already logged in, redirect to home
    user = get_current_user(db, request)
    if user:
        return RedirectResponse(url="/", status_code=302)
    
    return templates.TemplateResponse(
        "auth/login.html",
        {
            "request": request,
            "next": next,
            "error": None
        }
    )


@router.post("/login")
async def login(
    request: Request,
    db: Session = Depends(get_db),
    email: str = Form(...),
    password: str = Form(...),
    next: str = Form("/"),
    remember: bool = Form(False)
):
    """Process login form."""
    # Find user by email
    user = db.query(User).filter(User.email == email.lower()).first()
    
    if not user or not user.verify_password(password):
        return templates.TemplateResponse(
            "auth/login.html",
            {
                "request": request,
                "next": next,
                "error": "Invalid email or password"
            },
            status_code=400
        )
    
    if not user.is_active:
        return templates.TemplateResponse(
            "auth/login.html",
            {
                "request": request,
                "next": next,
                "error": "Your account has been disabled"
            },
            status_code=400
        )
    
    # Create session
    session_id = create_session(db, user, request)
    
    # Redirect with session cookie
    response = RedirectResponse(url=next, status_code=302)
    set_session_cookie(response, session_id)
    
    return response


@router.get("/register", response_class=HTMLResponse)
async def register_page(
    request: Request,
    db: Session = Depends(get_db)
):
    """Render registration page."""
    # If already logged in, redirect to home
    user = get_current_user(db, request)
    if user:
        return RedirectResponse(url="/", status_code=302)
    
    return templates.TemplateResponse(
        "auth/register.html",
        {
            "request": request,
            "error": None,
            "form_data": {}
        }
    )


@router.post("/register")
async def register(
    request: Request,
    db: Session = Depends(get_db),
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    full_name: str = Form("")
):
    """Process registration form."""
    form_data = {
        "email": email,
        "username": username,
        "full_name": full_name
    }
    
    # Validate email
    if not validate_email(email):
        return templates.TemplateResponse(
            "auth/register.html",
            {
                "request": request,
                "error": "Please enter a valid email address",
                "form_data": form_data
            },
            status_code=400
        )
    
    # Validate username
    valid, msg = validate_username(username)
    if not valid:
        return templates.TemplateResponse(
            "auth/register.html",
            {
                "request": request,
                "error": msg,
                "form_data": form_data
            },
            status_code=400
        )
    
    # Validate password
    valid, msg = validate_password(password)
    if not valid:
        return templates.TemplateResponse(
            "auth/register.html",
            {
                "request": request,
                "error": msg,
                "form_data": form_data
            },
            status_code=400
        )
    
    # Check password confirmation
    if password != confirm_password:
        return templates.TemplateResponse(
            "auth/register.html",
            {
                "request": request,
                "error": "Passwords do not match",
                "form_data": form_data
            },
            status_code=400
        )
    
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == email.lower()).first()
    if existing_user:
        return templates.TemplateResponse(
            "auth/register.html",
            {
                "request": request,
                "error": "An account with this email already exists",
                "form_data": form_data
            },
            status_code=400
        )
    
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == username.lower()).first()
    if existing_user:
        return templates.TemplateResponse(
            "auth/register.html",
            {
                "request": request,
                "error": "This username is already taken",
                "form_data": form_data
            },
            status_code=400
        )
    
    # Create user
    user = User(
        email=email.lower(),
        username=username.lower(),
        full_name=full_name.strip() if full_name else None
    )
    user.set_password(password)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create session and log in
    session_id = create_session(db, user, request)
    
    response = RedirectResponse(url="/profile", status_code=302)
    set_session_cookie(response, session_id)
    
    return response


@router.get("/logout")
async def logout(
    request: Request,
    db: Session = Depends(get_db)
):
    """Log out current user."""
    session_id = request.cookies.get(SESSION_COOKIE_NAME)
    
    if session_id:
        invalidate_session(db, session_id)
    
    response = RedirectResponse(url="/", status_code=302)
    clear_session_cookie(response)
    
    return response
