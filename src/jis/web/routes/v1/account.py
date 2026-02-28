from fastapi import APIRouter, Request

from ... import jinja_templates


router = APIRouter(tags=["Account"])


@router.get("/settings", name="get_settings")
async def get_settings(request: Request):
    return jinja_templates.TemplateResponse(
        "dashboard/dashboard.html", {"request": request}
    )

@router.get("/login", name="get_login")
async def get_login(request: Request):
    return jinja_templates.TemplateResponse(
        "auth/login.html", {"request": request}
    )

@router.get("/register", name="get_register")
async def get_register(request: Request):
    return jinja_templates.TemplateResponse(
        "auth/register.html", {"request": request}
    )

@router.get("/logout", name="get_logout")
async def get_logout(request: Request):
    return jinja_templates.TemplateResponse(
        "auth/logout.html", {"request": request}
    )
