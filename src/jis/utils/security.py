from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
import secrets
import logging

from ..config import config


logger = logging.getLogger(__name__)

pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    deprecated="auto",
    argon2__time_cost=2,
    argon2__memory_cost=102400,
    argon2__parallelism=8,
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.warning(f"Password verification failed: {e}")

        return False

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# JWT tokens

def create_access_token(
    subject: Union[str, int], 
    data: Optional[Dict[str, Any]] = None,
    expires_delta: Optional[timedelta] = None,
    token_type: str = "access"
) -> str:
    """
    Создание JWT токена.
    
    Args:
        subject: Идентификатор пользователя (sub claim)
        data: Дополнительные данные
        expires_delta: Время жизни токена
        token_type: Тип токена (access/refresh)
    """
    to_encode = {"sub": str(subject), "type": token_type, "iat": datetime.now(timezone.utc)}
    
    if data:
        to_encode.update(data)
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({
        "exp": expire,
        "jti": secrets.token_urlsafe(16),
    })
    
    # Заголовок с явным указанием типа
    headers = {
        "typ": "JWT",
        "alg": config.JWT_ALGORITHM
    }
    
    encoded_jwt = jwt.encode(
        to_encode, 
        config.JWT_SECRET_KEY, 
        algorithm=config.JWT_ALGORITHM,
        headers=headers
    )
    return encoded_jwt

def decode_token(
    token: str,
    token_type: str = "access",
    leeway: int = 30  # Допуск времени в секундах для exp/iat проверок
) -> Optional[Dict[str, Any]]:
    """
    Декодирование и валидация JWT токена.
    
    Args:
        token: JWT токен
        token_type: Ожидаемый тип токена
        leeway: Допуск времени для проверки exp/iat
    """
    try:
        payload = jwt.decode(
            token, 
            config.JWT_SECRET_KEY, 
            algorithms=[config.JWT_ALGORITHM],
            options={
                "require": ["exp", "iat", "sub", "type", "jti"],  # ✅ Обязательные claims
                "verify_aud": hasattr(config, 'JWT_AUDIENCE'),  # Проверяем audience если настроено
                "leeway": leeway,
            }
        )
        
        # Дополнительная проверка типа токена
        if payload.get("type") != token_type:
            logger.warning(f"Invalid token type: expected {token_type}, got {payload.get('type')}")
            return None
            
        return payload
        
    except JWTError as e:
        logger.debug(f"JWT decode error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error decoding token: {e}")
        return None

def create_refresh_token(
    subject: Union[str, int],
    data: Optional[Dict[str, Any]] = None
) -> str:
    """Создание refresh токена."""
    # TODO: JWT_REFRESH_DAYS
    expires_delta = timedelta(days=30)
    return create_access_token(
        subject=subject,
        data=data,
        expires_delta=expires_delta,
        token_type="refresh"
    )

# Session tokens с улучшенной безопасностью
def generate_session_token(length: int = 64) -> str:
    """
    Генерация криптографически безопасного session токена.
    
    Args:
        length: Длина токена в байтах (рекомендуется >= 64)
    """
    return secrets.token_urlsafe(length)

def verify_session_token(token: str, stored_token_hash: str) -> bool:
    """
    Верификация session токена с использованием constant-time сравнения.
    """
    try:
        # Используем constant-time сравнение для предотвращения timing attacks
        return secrets.compare_digest(
            pwd_context.hash(token),  # Хешируем предоставленный токен
            stored_token_hash  # Сравниваем с хранимым хешем
        )
    except Exception:
        return False