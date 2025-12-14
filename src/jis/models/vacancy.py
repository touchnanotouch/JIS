from sqlalchemy import Integer, String, Text, DateTime, Column, ForeignKey
from sqlalchemy.sql import func

from .base import Base


class Vacancy(Base):
    __tablename__ = "vacancies"

    v_id = Column(Integer, primary_key=True, index=True)
    v_name = Column(String(255), nullable=False)
    v_url = Column(String(255))
    v_salary = Column(Integer)
    v_created_at = Column(DateTime, default=func.now())
    v_description = Column(Text)
    # user_id = Column(Integer, ForeignKey("users.id"))

    # user = relationship("User", back_populates="vacancies")
