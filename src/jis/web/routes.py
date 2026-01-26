from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


web_router = APIRouter()
jinja_templates = Jinja2Templates(directory="src/jis/web/templates")


# Main Panel

@web_router.get("/dashboard", name="dashboard")
async def dashboard(request: Request):
    return jinja_templates.TemplateResponse("dashboard/dashboard.html", {"request": request})

# Vacancies

@web_router.get("/favorites", name="favorites")
async def favorites(request: Request):
    return jinja_templates.TemplateResponse("dashboard/dashboard.html", {"request": request})

@web_router.get("/search", name="search")
async def search(request: Request):
    return jinja_templates.TemplateResponse("dashboard/dashboard.html", {"request": request})

# Responses

@web_router.get("/responses", name="responses")
async def responses(request: Request):
    return jinja_templates.TemplateResponse("dashboard/dashboard.html", {"request": request})

@web_router.get("/templates", name="templates")
async def templates(request: Request):
    return jinja_templates.TemplateResponse("dashboard/dashboard.html", {"request": request})

@web_router.get("/auto_responses", name="auto_responses")
async def auto_responses(request: Request):
    return jinja_templates.TemplateResponse("dashboard/dashboard.html", {"request": request})

# Analytics

@web_router.get("/statistics", name="statistics")
async def statistics(request: Request):
    return jinja_templates.TemplateResponse("dashboard/dashboard.html", {"request": request})

# System

@web_router.get("/sources", name="sources")
async def sources(request: Request):
    return jinja_templates.TemplateResponse("dashboard/dashboard.html", {"request": request})

@web_router.get("/parser", name="parser")
async def parser(request: Request):
    return jinja_templates.TemplateResponse("dashboard/dashboard.html", {"request": request})

@web_router.get("/notifications", name="notifications")
async def notifications(request: Request):
    return jinja_templates.TemplateResponse("dashboard/dashboard.html", {"request": request})

# Account

@web_router.get("/settings", name="settings")
async def settings(request: Request):
    return jinja_templates.TemplateResponse("dashboard/dashboard.html", {"request": request})

@web_router.get("/login", name="login")
async def login(request: Request):
    return jinja_templates.TemplateResponse("auth/login.html", {"request": request})

@web_router.get("/register", name="register")
async def register(request: Request):
    return jinja_templates.TemplateResponse("auth/register.html", {"request": request})

@web_router.get("/logout", name="logout")
async def logout(request: Request):
    return jinja_templates.TemplateResponse("dashboard/dashboard.html", {"request": request})


# @web_router.get("/help", name="help")
# async def help(request: Request):
#     return jinja_templates.TemplateResponse("dashboard/dashboard.html", {"request": request})
