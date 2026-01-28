from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from ..config import config
from .exceptions import validation_exception_handler, sqlalchemy_exception_handler, global_exception_handler


def create_app() -> FastAPI:
    app = FastAPI(
        title="JIS",
        description="Job Search Aggregator",
        version="0.1.0",
        docs_url="/api/docs" if config.SHOW_DOCS else None,
        redoc_url="/api/redoc" if config.SHOW_DOCS else None,
        openapi_url="/api/openapi.json" if config.SHOW_DOCS else None,
    )

    configure_middleware(app)

    configure_exception_handlers(app)
    
    return app

def configure_middleware(app: FastAPI) -> None: 
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ORIGINS,
        allow_credentials=False,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

def configure_exception_handlers(app: FastAPI) -> None:
    # app.add_exception_handler(RequestValidationError, validation_exception_handler)
    # app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)

def configure_routes(app: FastAPI) -> None:
    # from .routes import api_router
    from ..web.routes import web_router
    
    app.include_router(web_router)
    # app.include_router(api_router, prefix="/api")
