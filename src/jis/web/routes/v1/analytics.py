from fastapi import APIRouter, Request

from ... import jinja_templates


router = APIRouter(tags=["Analytics"])


@router.get("/statistics", name="get_statistics")
async def get_statistics(request: Request):
    return jinja_templates.TemplateResponse(
        "dashboard/dashboard.html", {"request": request}
    )
