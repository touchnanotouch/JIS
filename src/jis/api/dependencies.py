from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from ..core import db_manager
from ..crud.user import get_user_by_id, get_session_by_token
from ..utils.security import decode_token
from ..models.user import User

security = HTTPBearer(auto_error=False)

async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(db_manager.get_db),
) -> Optional[User]:
    # 1. Проверка JWT токена из заголовка (для API)
    if credentials:
        payload = decode_token(credentials.credentials)
        if payload and "sub" in payload:
            user_id = payload.get("sub")
            user = get_user_by_id(db, user_id)
            if user and user.is_active:
                return user
    
    # 2. Проверка сессионного токена из cookies (для веб-интерфейса)
    session_token = request.cookies.get("session_token")
    if session_token:
        session = get_session_by_token(db, session_token)
        if session:
            user = get_user_by_id(db, session.user_id)
            if user and user.is_active:
                return user
    
    return None

async def get_current_active_user(
    current_user: Optional[User] = Depends(get_current_user)
) -> User:
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Необходима авторизация",
        )
    return current_user

def get_current_active_superuser(
    current_user: User = Depends(get_current_active_user)
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав"
        )
    return current_user