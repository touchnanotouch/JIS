# api/routes/v1/auth.py
# TODO: raw


from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from ....web import jinja_templates
from ....core import config, db_manager
from ...dependencies import get_current_user
from ....crud.user import authenticate_user, create_user, create_session, increment_login_count
from ....schemas.user import UserLogin, UserCreate


router = APIRouter(tags=["Account"])

@router.post("/login", name="post_login")
async def post_login(
    request: Request,
    db: Session = Depends(db_manager.get_db)
):
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    
    return response

@router.post("/register", name="post_register")
async def post_register(
    request: Request,
    db: Session = Depends(db_manager.get_db)
):
    form_data = await request.form()
    
    print(form_data)

    try:
        user_data = UserCreate(
            email=form_data.get("email"),
            username=form_data.get("username"),
            password=form_data.get("password"),
            password_confirm=form_data.get("password_confirm")
        )
    except ValueError as e:
        return jinja_templates.TemplateResponse(
            "auth/register.html",
            {
                "request": request,
                "error": str(e),
                "config": config
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # TODO: Проверить существование пользователя
    
    # Создаем пользователя

    user = create_user(db, user_data)
    
    # Сразу логиним

    user_agent = request.headers.get("user-agent")
    ip_address = request.client.host if request.client else None
    
    session = create_session(db, user.u_id, user_agent, ip_address, remember_me=False)
    
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key="session_token",
        value=session.s_session_token,
        httponly=True,
        secure=not config.DEBUG if hasattr(config, 'DEBUG') else False,
        samesite="lax"
    )
    
    return response
