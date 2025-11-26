from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Vacancy(BaseModel):
    v_id: str
    v_title: str
    v_company: str
    v_salary: Optional[str] = None
    v_url: str
    v_description: str
    v_platform: str
    v_created_at: Optional[datetime] = None
    v_processed: bool = False

    def __init__(self, **data):
        if "created_at" not in data:
            data["created_at"] = datetime.utcnow()

        super().__init__(**data)
