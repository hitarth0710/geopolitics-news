"""Authentication utilities and session management."""
import secrets
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Request, Response, HTTPException
from sqlalchemy.orm import Session as DBSession

from .models import User, Session, PasswordResetToken
from .settings import settings


SESSION_COOKIE_NAME = "session_id"
SESSION_EXPIRY_DAYS = 7
PASSWORD_RESET_EXPIRY_HOURS = 1


def create_session(
    db: DBSession, 
    user: User, 
    request: Request
) -> str:
    """Create a new session for user."""
    session_id = secrets.token_urlsafe(48)
    expires_at = datetime.utcnow() + timedelta(days=SESSION_EXPIRY_DAYS)
    
    # Get client info
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent", "")[:500]
    
    # Create session record
    session = Session(
        session_id=session_id,
        user_id=user.id,
        expires_at=expires_at,
        ip_address=ip_address,
        user_agent=user_agent
    )
    db.add(session)
    
    # Update user's last login
    user.last_login = datetime.utcnow()
    
    db.commit()
    
    return session_id


def get_session(db: DBSession, session_id: str) -> Optional[Session]:
    """Get active session by ID."""
    session = db.query(Session).filter(
        Session.session_id == session_id,
        Session.is_active == True
    ).first()
    
    if session and session.is_expired:
        session.is_active = False
        db.commit()
        return None
    
    return session


def get_current_user(db: DBSession, request: Request) -> Optional[User]:
    """Get current user from session cookie."""
    session_id = request.cookies.get(SESSION_COOKIE_NAME)
    
    if not session_id:
        return None
    
    session = get_session(db, session_id)
    
    if not session:
        return None
    
    return session.user


def set_session_cookie(response: Response, session_id: str):
    """Set session cookie on response."""
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session_id,
        httponly=True,
        secure=not settings.debug,  # Secure in production
        samesite="lax",
        max_age=SESSION_EXPIRY_DAYS * 24 * 60 * 60
    )


def clear_session_cookie(response: Response):
    """Clear session cookie."""
    response.delete_cookie(key=SESSION_COOKIE_NAME)


def invalidate_session(db: DBSession, session_id: str):
    """Invalidate a session."""
    session = db.query(Session).filter(Session.session_id == session_id).first()
    if session:
        session.is_active = False
        db.commit()


def invalidate_all_user_sessions(db: DBSession, user_id: int):
    """Invalidate all sessions for a user."""
    db.query(Session).filter(
        Session.user_id == user_id,
        Session.is_active == True
    ).update({"is_active": False})
    db.commit()


def cleanup_expired_sessions(db: DBSession):
    """Clean up expired sessions from database."""
    db.query(Session).filter(
        Session.expires_at < datetime.utcnow()
    ).delete()
    db.commit()


def validate_password(password: str) -> tuple[bool, str]:
    """Validate password strength."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number"
    return True, ""


def validate_email(email: str) -> bool:
    """Basic email validation."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_username(username: str) -> tuple[bool, str]:
    """Validate username."""
    import re
    if len(username) < 3:
        return False, "Username must be at least 3 characters long"
    if len(username) > 30:
        return False, "Username must be at most 30 characters long"
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    return True, ""


def create_password_reset_token(db: DBSession, user: User) -> str:
    """Create a password reset token for user."""
    # Invalidate any existing tokens for this user
    db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == user.id,
        PasswordResetToken.is_used == False
    ).update({"is_used": True})
    
    # Create new token
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(hours=PASSWORD_RESET_EXPIRY_HOURS)
    
    reset_token = PasswordResetToken(
        token=token,
        user_id=user.id,
        expires_at=expires_at
    )
    db.add(reset_token)
    db.commit()
    
    return token


def get_password_reset_token(db: DBSession, token: str) -> Optional[PasswordResetToken]:
    """Get a valid password reset token."""
    reset_token = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == token
    ).first()
    
    if not reset_token:
        return None
    
    if not reset_token.is_valid:
        return None
    
    return reset_token


def use_password_reset_token(db: DBSession, token: PasswordResetToken, new_password: str):
    """Use a password reset token to change password."""
    user = token.user
    user.set_password(new_password)
    token.is_used = True
    
    # Invalidate all user sessions for security
    invalidate_all_user_sessions(db, user.id)
    
    db.commit()


def cleanup_expired_reset_tokens(db: DBSession):
    """Clean up expired password reset tokens."""
    db.query(PasswordResetToken).filter(
        PasswordResetToken.expires_at < datetime.utcnow()
    ).delete()
    db.commit()
