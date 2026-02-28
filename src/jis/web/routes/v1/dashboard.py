from fastapi import APIRouter, Request

from ... import jinja_templates


router = APIRouter(tags=["Dashboard"])

@router.get("/dashboard", name="get_dashboard")
async def get_dashboard(request: Request):
    return jinja_templates.TemplateResponse(
        "dashboard/dashboard.html", {"request": request}
    )
