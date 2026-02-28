from fastapi import APIRouter, Request

from ... import jinja_templates


router = APIRouter(tags=["Vacancies"])


@router.get("/favorites", name="get_favorites")
async def get_favorites(request: Request):
    return jinja_templates.TemplateResponse(
        "dashboard/dashboard.html", {"request": request}
    )

@router.get("/search", name="get_search")
async def get_search(request: Request):
    return jinja_templates.TemplateResponse(
        "dashboard/dashboard.html", {"request": request}
    )
