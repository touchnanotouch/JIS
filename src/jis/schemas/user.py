import re

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import Optional, ClassVar
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    email: EmailStr

    username: str = Field(
        min_length=3, 
        max_length=30,
        pattern=r"^[a-z0-9_]+$",
        description="Имя пользователя (только строчные буквы, цифры, подчеркивания)"
    )

    @field_validator("username")
    @classmethod
    def validate_username_format(cls, v: str) -> str:
        v = v.strip().lower()

        reserved_names = {"admin", "root", "system", "support", "info", "test"}
        if v in reserved_names:
            raise ValueError("Даноне имя пользователя запрещено")

        if v.isdigit():
            raise ValueError("Имя пользователя не может состоять только из цифр")

        return v

class UserCreate(UserBase):
    password: str = Field(
        min_length=8, 
        max_length=80,
        description="Пароль (8-80 символов, должен содержать буквы, цифры и спецсимволы)"
    )

    password_confirm: str

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        has_letter = bool(re.search(r"[a-z]", v))
        has_digit = bool(re.search(r"\d", v))
        has_special = bool(re.search(r"[!@#$%^&*(),.?':{}|<>]", v))

        if not (has_letter and has_digit and has_special):
            raise ValueError(
                "Пароль должен содержать хотя бы одну букву, одну цифру "
                "и один специальный символ"
            )

        return v

    @model_validator(mode="after")
    def check_passwords_match(self) -> "UserCreate":
        if self.password != self.password_confirm:
            raise ValueError("Пароли не совпадают")

        return self


class UserLogin(BaseModel):
    email_or_username: str = Field(
        min_length=3,
        pattern=r"^[\w@.+_-]+$",
        description="Email или имя пользователя"
    )

    password: str
    remember_me: bool = False
    
    @field_validator("email_or_username")
    @classmethod
    def normalize_and_validate_login(cls, v: str) -> str:
        v = v.strip().lower()

        if "@" not in v:
            if not re.match(r"^[a-z0-9_]+$", v):
                raise ValueError(
                    "Имя пользователя может содержать только латинские буквы, "
                    "цифры и подчеркивания"
                )
        
        return v

class UserUpdate(BaseModel):
    notification_email: Optional[bool] = None
    notification_telegram: Optional[bool] = None
    daily_digest: Optional[bool] = None

class UserResponse(UserBase):
    user_id: UUID
    is_active: bool
    email_verified: bool
    created_at: datetime
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "user@example.com",
                "username": "john_pork",
                "is_active": True,
                "email_verified": False,
                "created_at": "2026-01-01T04:30:00"
            }
        }
    }

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIs...",
                "token_type": "bearer",
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "email": "user@example.com",
                    "username": "john_pork",
                    "is_active": True,
                    "email_verified": False,
                    "created_at": "2026-01-01T04:30:00"
                }
            }
        }
    }

class UserPublic(BaseModel):
    """Схема для публичного отображения пользователя (без чувствительных данных)."""
    id: UUID
    username: str
    full_name: str
    
    model_config = {
        "from_attributes": True
    }

class UserWithStats(UserResponse):
    """Схема с дополнительной статистикой пользователя."""
    login_count: int
    last_login: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True
    }