from fastapi import APIRouter, Request

from ... import jinja_templates


router = APIRouter(tags=["Responses"])


@router.get("/responses", name="get_responses")
async def get_responses(request: Request):
    return jinja_templates.TemplateResponse(
        "dashboard/dashboard.html", {"request": request}
    )

@router.get("/templates", name="get_templates")
async def get_templates(request: Request):
    return jinja_templates.TemplateResponse(
        "dashboard/dashboard.html", {"request": request}
    )

@router.get("/auto_responses", name="get_auto_responses")
async def get_auto_responses(request: Request):
    return jinja_templates.TemplateResponse(
        "dashboard/dashboard.html", {"request": request}
    )
