import httpx

from typing import List, Optional

from ..models.vacancy import Vacancy


class HHParser:
    def __init__(self):
        self.base_url = "https://api.hh.ru"
        self.headers = {
            "User-Agent": "JIS"
        }
    
    async def search_vacancies(self, query: str, area: int = 1) -> List[Vacancy]:
        """Поиск вакансий на HH.ru"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/vacancies",
                params={"text": query, "area": area, "per_page": 50},
                headers=self.headers
            )
            return self._parse_response(response.json())
    
    def _parse_response(self, data: dict) -> List[Vacancy]:
        vacancies = []
        for item in data.get("items", []):
            vacancy = Vacancy(
                id=f"hh_{item['id']}",
                title=item.get('name'),
                company=item.get('employer', {}).get('name'),
                salary=self._parse_salary(item.get('salary')),
                url=item.get('alternate_url'),
                description=item.get('snippet', {}).get('requirement', ''),
                platform="hh"
            )
            vacancies.append(vacancy)
        return vacancies
    
    def _parse_salary(self, salary_data: Optional[dict]) -> str:
        if not salary_data:
            return "Не указана"
        
        salary_from = salary_data.get('from')
        salary_to = salary_data.get('to')
        currency = salary_data.get('currency', 'RUR')
        
        if salary_from and salary_to:
            return f"{salary_from} - {salary_to} {currency}"
        elif salary_from:
            return f"от {salary_from} {currency}"
        elif salary_to:
            return f"до {salary_to} {currency}"
        return "Не указана"