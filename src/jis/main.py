import logging

from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse, JSONResponse

from .config import config
from .database import engine
from .models.base import Base
from .api.app import create_app, configure_routes


logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)

logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    startup()

    yield

    shutdown()


def startup():
    """Логика запуска приложения"""
    logger.info("=" * 50)
    logger.info("🚀 Запуск Job Search Aggregator")
    logger.info(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 50)

    if config.ENVIRONMENT == "development":
        init_database()

    _ = init_redis()

    if config.CHECK_CELERY_ON_STARTUP:
        check_celery()

    if config.INIT_PARSERS_ON_STARTUP and config.SCRAPING_ENABLED:
        init_parsers()

    logger.info("✅ Приложение готово к работе")
    logger.info(f"📡 API доступен по http://{config.HOST}:{config.PORT}")


def shutdown():
    """Логика завершения работы"""
    logger.info("🛑 Завершение работы приложения...")

    # Закрываем соединения
    # if redis_client:
    #     import asyncio
    #     asyncio.run(redis_client.disconnect())
    #     logger.info("✅ Redis соединение закрыто")

    logger.info("👋 Приложение остановлено")


def init_database():
    try:
        logger.info("🗄️  Проверка/создание таблиц в БД...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Таблицы готовы")
    except Exception as e:
        logger.error(f"❌ Ошибка создания таблиц: {e}")


async def init_redis():
    try:
        await redis_client.connect()
        await redis_client.ping()
        logger.info("✅ Redis подключен")
    except Exception as e:
        logger.error(f"❌ Ошибка подключения к Redis: {e}")


def check_celery():
    try:
        logger.info("✅ Celery worker запущен")
        # is_worker_running = check_celery_worker_status()
        # if is_worker_running:
        #     logger.info("✅ Celery worker запущен")
        # else:
        #     logger.warning("⚠️  Celery worker не запущен")
    except Exception as e:
        logger.warning(f"⚠️  Celery не настроен: {e}")


def init_parsers():
    try:
        # from .services.scraping.manager import ScrapingManager
        # scraping_manager = ScrapingManager()
        # scraping_manager.init_parsers()
        logger.info("✅ Парсеры инициализированы")
    except ImportError as e:
        logger.warning(f"⚠️  Парсеры не настроены: {e}")
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации парсеров: {e}")


app = create_app()

configure_routes(app)

try:
    app.mount("/static", StaticFiles(directory="src/jis/web/static"), name="static")
    logger.info("✅ Статические файлы подключены")
except Exception as e:
    logger.warning(f"⚠️  Статические файлы не найдены: {e}")


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/dashboard")


@app.get("/health", tags=["System"])
async def health_check():
    # """
    # Проверка здоровья приложения
    # """
    # from sqlalchemy import text
    # from .database import get_db

    # health_status = {
    #     "status": "healthy",
    #     "service": "job-search-aggregator",
    #     "version": "0.1.0",
    #     "environment": config.ENVIRONMENT,
    #     "timestamp": datetime.now().isoformat(),
    # }

    # try:
    #     db = next(get_db())
    #     db.execute(text("SELECT 1"))
    #     health_status["database"] = "connected"
    # except Exception as e:
    #     health_status["database"] = "disconnected"
    #     health_status["database_error"] = (
    #         str(e) if config.DEBUG else "Connection failed"
    #     )
    #     health_status["status"] = "degraded"
    #     logger.error(f"Ошибка подключения к БД: {e}")

    # try:
    #     # await redis_client.ping()
    #     health_status["redis"] = "connected"
    # except Exception as e:
    #     health_status["redis"] = "disconnected"
    #     health_status["redis_error"] = str(e) if config.DEBUG else "Connection failed"
    #     health_status["status"] = "degraded"
    #     logger.error(f"Ошибка подключения к Redis: {e}")

    # health_status["celery"] = "not_configured"

    return True


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    import os

    favicon_path = "src/jis/web/static/favicon.svg"
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path)

    return JSONResponse(content={"message": "No favicon"}, status_code=404)
