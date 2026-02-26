import uuid

from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class User(Base):
    __tablename__ = "users"

    # Main Info

    u_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    u_email = Column(String(255), unique=True, index=True, nullable=False)
    u_username = Column(String(50), unique=True, index=True, nullable=False)
    u_hashed_password = Column(String(255), nullable=False)

    u_is_active = Column(Boolean, default=True)
    u_is_superuser = Column(Boolean, default=False)
    u_is_email_verified = Column(Boolean, default=False)

    # Notifications

    u_notification_email = Column(Boolean, default=True)
    u_notification_telegram = Column(Boolean, default=False)
    u_telegram_id = Column(String(100), nullable=True)
    u_daily_digest = Column(Boolean, default=True)

    # Statistics

    u_last_login = Column(DateTime(timezone=True), nullable=True)
    u_login_count = Column(Integer, default=0)
    
    # Timestamps

    u_created_at = Column(DateTime(timezone=True), server_default=func.now())
    u_updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class UserSession(Base):
    __tablename__ = "user_sessions"
    
    s_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    s_user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    s_session_token = Column(String(255), unique=True, index=True, nullable=False)
    s_user_agent = Column(Text, nullable=True)
    s_ip_address = Column(String(45), nullable=True)
    s_expires_at = Column(DateTime(timezone=True), nullable=False)
    s_created_at = Column(DateTime(timezone=True), server_default=func.now())
