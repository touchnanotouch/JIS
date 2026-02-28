from fastapi import APIRouter, Request

from ... import jinja_templates


router = APIRouter(tags=["System"])


@router.get("/sources", name="get_sources")
async def get_sources(request: Request):
    return jinja_templates.TemplateResponse(
        "dashboard/dashboard.html", {"request": request}
    )

@router.get("/parser", name="get_parser")
async def get_parser(request: Request):
    return jinja_templates.TemplateResponse(
        "dashboard/dashboard.html", {"request": request}
    )

@router.get("/notifications", name="get_notifications")
async def get_notifications(request: Request):
    return jinja_templates.TemplateResponse(
        "dashboard/dashboard.html", {"request": request}
    )
