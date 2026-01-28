import os

from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()


class Config(BaseSettings):
    # Project settings

    PROJECT_ROOT: Path = Path(__file__).parent.parent.parent

    # Environment settings

    VERSION: str = os.getenv("VERSION", "0.1.0")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    # Server settings

    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    RELOAD: bool = os.getenv("RELOAD", "True").lower() == "true"

    # PostgreSQL

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://user:pass@localhost:5432/jis"
    )

    # Redis

    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Celery

    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/1")
    CELERY_RESULT_BACKEND: str = os.getenv(
        "CELERY_RESULT_BACKEND", "redis://localhost:6379/2"
    )

    # Security

    SECRET_KEY: str = os.getenv("SECRET_KEY", "secret123")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "secret321")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )

    # Parsers settings

    SCRAPING_ENABLED: bool = os.getenv("SCRAPING_ENABLED", "True").lower() == "true"
    SCRAPING_DELAY_MIN: float = float(os.getenv("SCRAPING_DELAY_MIN", "1.0"))
    SCRAPING_DELAY_MAX: float = float(os.getenv("SCRAPING_DELAY_MAX", "3.0"))

    # Logs

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # CORS

    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "http://localhost:8000")

    # Docs

    SHOW_DOCS: bool = os.getenv("SHOW_DOCS", "True").lower() == "true"

    # Init flags

    INIT_PARSERS_ON_STARTUP: bool = (
        os.getenv("INIT_PARSERS_ON_STARTUP", "True").lower() == "true"
    )
    CHECK_CELERY_ON_STARTUP: bool = (
        os.getenv("CHECK_CELERY_ON_STARTUP", "True").lower() == "true"
    )

    # Consts (limits)

    MAX_VACANCIES_PER_SEARCH: int = int(os.getenv("MAX_VACANCIES_PER_SEARCH", "100"))
    MAX_APPLICATIONS_PER_DAY: int = int(os.getenv("MAX_APPLICATIONS_PER_DAY", "50"))

    class Config:
        env_file = ".env"
        case_sensitive = True


config = Config()
