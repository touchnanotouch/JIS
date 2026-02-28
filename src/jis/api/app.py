# api/app.py


from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..core import config, get_logger, db_manager, redis_manager, celery_manager

from ..models.base import Base
from .exceptions import global_exception_handler

# from ..web.middleware import (
#     DBSessionMiddleware,
#     AuthMiddleware,
#     SecurityHeadersMiddleware,
#     RequestLoggingMiddleware,
# )


logger = get_logger(__name__)


class Lifecycle:
    def __init__(self) -> None:
        self.start_time: Optional[datetime] = None
        self.app: Optional[FastAPI] = None

    def init(self, app: FastAPI) -> None:
        self.app = app

    async def startup(self) -> None:
        self.start_time = datetime.now()

        logger.info("Starting JIS...")

        logger.info(f"Startup time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Environment: {config.ENVIRONMENT}")
        logger.info(f"Version tag: {config.GIT_TAG}")
        logger.info(f"Commit hash: {config.GIT_COMMIT_HASH}")

        await self._init_database()

        await self._init_redis()

        self._init_celery()

        await self._init_parsers()

        logger.info("Application startup completed!")
        logger.info(f"API endpoint: http://{config.HOST}:{config.PORT}")

    async def shutdown(self) -> None:
        uptime = datetime.now() - self.start_time if self.start_time else None

        logger.info("Initiating application shutdown...")
        if uptime:
            logger.info(f"Application uptime: {uptime}")

        await redis_manager.disconnect()

        logger.info("Application shutdown completed!")

    async def _init_database(self):
        try:
            logger.info("Initializing database connection...")

            db_manager.init_engine()

            if config.ENVIRONMENT == "development" and config.DEBUG:
                logger.info("Creating database tables...")

                from ..models.user import User, UserSession
                from ..models.vacancy import Vacancy

                Base.metadata.create_all(bind=db_manager.engine)

                logger.info("Database tables created successfully!")

            if db_manager.health_check():
                logger.info("Database connection established!")
            else:
                logger.error("Database health check failed")

        except Exception as e:
            logger.error(f"Database initialization failed: {e}", exc_info=True)

    async def _init_redis(self) -> None:
        try:
            logger.info("Initializing Redis connection...")

            if await redis_manager.connect():
                logger.info("Redis connection established!")
            else:
                logger.warning("Redis connection failed - continuing without Redis")

        except Exception as e:
            logger.error(f"Redis initialization failed: {e}")

    def _init_celery(self) -> None:
        """Initialize Celery"""
        try:
            logger.info("Initializing Celery...")

            if config.CHECK_CELERY_ON_STARTUP:
                celery_manager.init_app()

                if celery_manager.health_check():
                    logger.info("Celery connection established!")
                else:
                    logger.warning(
                        "Celery health check failed - continuing without Celery"
                    )
            else:
                logger.info(
                    "Celery initialization skipped ( CHECK_CELERY_ON_STARTUP = False )"
                )

        except Exception as e:
            logger.error(f"Celery initialization failed: {e}")

    async def _init_parsers(self) -> None:
        try:
            if config.SCRAPING_ENABLED and config.INIT_PARSERS_ON_STARTUP:
                logger.info("Initializing data parsers...")

                # Parser initialization will be added here
                # from ..parsers import init_parsers
                # await init_parsers()

                logger.info("Data parsers initialized successfully!")
            else:
                logger.info(
                    "Parser initialization skipped ( SCRAPING_ENABLED = False or INIT_PARSERS_ON_STARTUP = False )"
                )

        except Exception as e:
            logger.error(f"Parser initialization failed: {e}")


lifecycle = Lifecycle()


@asynccontextmanager
async def lifespan(app: FastAPI):
    lifecycle.init(app)

    await lifecycle.startup()

    yield

    await lifecycle.shutdown()

def configure_middleware(app: FastAPI) -> None:
    # 1. CORS middleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ORIGINS.split(",") if config.CORS_ORIGINS else [],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # # 2. Request logging

    # app.add_middleware(RequestLoggingMiddleware)

    # # 3. Database session management

    # app.add_middleware(DBSessionMiddleware)

    # # 4. Authentication

    # app.add_middleware(
    #     AuthMiddleware,
    #     public_paths={
    #         "/login",
    #         "/register",
    #         "/static",
    #         "/favicon.ico",
    #         "/health",
    #         "/api/docs",
    #         "/api/redoc",
    #         "/api/openapi.json",
    #     },
    # )

    # # 5. Security headers

    # app.add_middleware(SecurityHeadersMiddleware)

def configure_exceptions(app: FastAPI) -> None:
    app.add_exception_handler(Exception, global_exception_handler)

def configure_routes(app: FastAPI) -> None:
    from .routes import api_router
    from ..web.routes import web_router

    app.include_router(api_router)
    app.include_router(web_router)

def create_app() -> FastAPI:
    app = FastAPI(
        title="JIS",
        description="Job Intelligence System",
        version=config.GIT_COMMIT_HASH,
        docs_url="/api/docs" if config.SHOW_DOCS else None,
        redoc_url="/api/redoc" if config.SHOW_DOCS else None,
        openapi_url="/api/openapi.json" if config.SHOW_DOCS else None,
        lifespan=lifespan,
    )

    configure_middleware(app)
    configure_exceptions(app)

    return app
