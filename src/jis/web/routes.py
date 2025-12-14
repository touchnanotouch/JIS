from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


web_router = APIRouter()
templates = Jinja2Templates(directory="src/jis/web/templates")


@web_router.get("/dashboard", name="dashboard")
async def home_page(request: Request):
    return templates.TemplateResponse("dashboard/dashboard.html", {"request": request})
