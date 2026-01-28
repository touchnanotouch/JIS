import logging
from typing import Any

from fastapi import Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from ..config import config

logger = logging.getLogger(__name__)


async def validation_exception_handler(
    request: Request, 
    exc: RequestValidationError
) -> JSONResponse:
    """Обработка ошибок валидации Pydantic"""
    logger.warning(f"Ошибка валидации: {exc.errors()}")
    
    # Упрощаем ошибки для клиента
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Ошибка валидации данных",
            "errors": errors,
            "body": exc.body if config.DEBUG else None,
        },
    )


async def sqlalchemy_exception_handler(
    request: Request, 
    exc: SQLAlchemyError
) -> JSONResponse:
    """Обработка ошибок БД"""
    logger.error(f"Ошибка БД: {exc}", exc_info=True)
    
    # Можно добавить логику для разных типов ошибок SQLAlchemy
    error_detail = str(exc) if config.DEBUG else "Ошибка базы данных"
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Ошибка базы данных",
            "error": error_detail,
        },
    )


async def global_exception_handler(
    request: Request, 
    exc: Exception
) -> Any:
    """Глобальный обработчик исключений"""
    logger.error(f"Необработанная ошибка: {exc}", exc_info=True)
    
    # Для API запросов возвращаем JSON
    if request.url.path.startswith("/api/"):
        error_detail = str(exc) if config.DEBUG else "Внутренняя ошибка сервера"
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Внутренняя ошибка сервера",
                "error": error_detail,
            }
        )
    
    # Для web запросов перенаправляем на страницу ошибки
    error_message = str(exc) if config.DEBUG else "Произошла ошибка"
    return RedirectResponse(
        url=f"/error?message={error_message}",
        status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )


class AppException(Exception):
    """Базовое исключение приложения"""
    
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: Any = None,
    ):
        self.message = message
        self.status_code = status_code
        self.detail = detail
        super().__init__(self.message)


async def app_exception_handler(
    request: Request, 
    exc: AppException
) -> JSONResponse:
    """Обработчик кастомных исключений приложения"""
    logger.warning(f"Исключение приложения: {exc.message}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message,
            "error": exc.detail,
        }
    )