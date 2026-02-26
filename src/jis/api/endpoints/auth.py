from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ...database import get_db
from ..dependencies import get_current_user
from ...crud.user import authenticate_user, create_user, create_session, increment_login_count
from ...schemas.user import UserLogin, UserCreate

from ...web.routes import web_router, jinja_templates
from ...config import config


@web_router.post("/login")
async def login(
    request: Request,
    db: Session = Depends(get_db)
):
    form_data = await request.form()
    
    try:
        login_data = UserLogin(
            email_or_username=form_data.get("email_or_username"),
            password=form_data.get("password"),
            remember_me=form_data.get("remember_me") == "on"
        )
    except Exception as e:
        return jinja_templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": str(e),
                "config": request.state.config
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate_user(db, login_data.email_or_username, login_data.password)
    if not user:
        return jinja_templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Неверный email/логин или пароль",
                "config": request.state.config
            },
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    # Создаем сессию
    user_agent = request.headers.get("user-agent")
    ip_address = request.client.host if request.client else None
    
    session = create_session(
        db, 
        user.id, 
        user_agent, 
        ip_address, 
        login_data.remember_me
    )
    
    # Обновляем статистику
    increment_login_count(db, user)
    
    # Редирект на главную
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    
    # Устанавливаем cookie
    response.set_cookie(
        key="session_token",
        value=session.session_token,
        httponly=True,
        secure=not config.DEBUG if hasattr(config, 'DEBUG') else False,
        samesite="lax",
        max_age=2592000 if login_data.remember_me else None  # 30 дней если "запомнить меня"
    )
    
    return response

@web_router.get("/register")
async def register_page(
    request: Request,
    current_user = Depends(get_current_user)
):
    if current_user:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    
    return jinja_templates.TemplateResponse(
        "register.html",
        {
            "request": request,
            "config": request.state.config
        }
    )

@web_router.post("/register")
async def register(
    request: Request,
    db: Session = Depends(get_db)
):
    form_data = await request.form()
    
    try:
        user_data = UserCreate(
            email=form_data.get("email"),
            username=form_data.get("username"),
            password=form_data.get("password"),
            password_confirm=form_data.get("password_confirm")
        )
    except ValueError as e:
        return jinja_templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": str(e),
                "config": request.state.config
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # TODO: Проверить существование пользователя
    
    # Создаем пользователя
    user = create_user(db, user_data)
    
    # Сразу логиним
    user_agent = request.headers.get("user-agent")
    ip_address = request.client.host if request.client else None
    
    session = create_session(db, user.id, user_agent, ip_address, remember_me=False)
    
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key="session_token",
        value=session.session_token,
        httponly=True,
        secure=not config.DEBUG if hasattr(config, 'DEBUG') else False,
        samesite="lax"
    )
    
    return response
