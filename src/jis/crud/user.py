from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from datetime import datetime, timedelta, timezone
import uuid

from ..models.user import User, UserSession
from ..schemas.user import UserCreate
from ..utils.security import hash_password, verify_password, generate_session_token

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(db: Session, user_id: uuid.UUID) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def authenticate_user(db: Session, email_or_username: str, password: str) -> Optional[User]:
    user = db.query(User).filter(
        or_(
            User.email == email_or_username,
            User.username == email_or_username
        )
    ).first()
    
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    if not user.is_active:
        return None
    
    return user

def create_user(db: Session, user_data: UserCreate) -> User:
    hashed_password = hash_password(user_data.password)
    db_user = User(
        u_email=user_data.email,
        u_username=user_data.username,
        u_hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: User, update_data: dict) -> User:
    for field, value in update_data.items():
        if hasattr(user, field):
            setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user

def increment_login_count(db: Session, user: User):
    user.login_count += 1
    user.last_login = datetime.now(timezone.utc)
    db.commit()
    db.refresh(user)

# Session management
def create_session(db: Session, user_id: uuid.UUID, user_agent: Optional[str] = None, 
                   ip_address: Optional[str] = None, remember_me: bool = False) -> UserSession:
    from ..config import config
    
    session_token = generate_session_token()
    if remember_me:
        expires_at = datetime.now(timezone.utc) + timedelta(days=30)  # 30 дней
    else:
        expires_at = datetime.now(timezone.utc) + timedelta(hours=12)  # 12 часов
    
    db_session = UserSession(
        s_user_id=user_id,
        s_session_token=session_token,
        s_user_agent=user_agent,
        s_ip_address=ip_address,
        s_expires_at=expires_at
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_session_by_token(db: Session, token: str) -> Optional[UserSession]:
    return db.query(UserSession).filter(
        UserSession.s_session_token == token,
        UserSession.s_expires_at > datetime.now(timezone.utc)
    ).first()

def delete_session(db: Session, session: UserSession):
    db.delete(session)
    db.commit()

def delete_all_user_sessions(db: Session, user_id: uuid.UUID):
    db.query(UserSession).filter(UserSession.s_user_id == user_id).delete()
    db.commit()