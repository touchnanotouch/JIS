from fastapi import APIRouter

from typing import List

from ...core.parsers.hh import HHParser
from ...core.models.vacancy import Vacancy


router = APIRouter()


@router.get("/vacancies", response_model=List[Vacancy])
async def get_vacancies():
    """Получить сохраненные вакансии"""
    # Пока заглушка
    return [
        Vacancy(
            v_id="test_1",
            v_title="Python Developer",
            v_company="Test Company",
            v_salary="100000-150000 RUB",
            v_url="https://example.com",
            v_description="Test vacancy",
            v_platform="test"
        )
    ]

@router.post("/vacancies/search")
async def search_vacancies(query: str):
    """Поиск новых вакансий"""
    parser = HHParser()
    vacancies = await parser.search_vacancies(query)
    
    # TODO: сохранить в БД
    return {
        "found": len(vacancies),
        "query": query,
        "vacancies": vacancies
    }