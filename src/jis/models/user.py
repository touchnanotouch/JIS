from sqlalchemy import Integer, String, Boolean, DateTime, Column, ForeignKey
from sqlalchemy.sql import func

from .base import Base


class User(Base):
    __tablename__ = "users"
    
    u_id = Column(Integer, primary_key=True, index=True)
    u_email = Column(String(255), unique=True, index=True, nullable=False)
    u_hashed_password = Column(String(255), nullable=False)
    u_is_active = Column(Boolean, default=True)
    u_created_at = Column(DateTime, default=func.now())

    # vacancies = relationship("Vacancy", back_populates="user")
