# src/jis/database.py

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from typing import Generator

from .config import config
from .logger import get_logger


logger = get_logger(__name__)


class DatabaseManager:
    """Менеджер для работы с базой данных"""
    
    def __init__(self):
        self._engine = None
        self._session_factory = None
        self._database_url = config.DATABASE_URL
    
    def init_engine(self):
        """Инициализация движка БД"""
        try:
            logger.info(f"Initializing database engine...")
            
            self._engine = create_engine(
                self._database_url,
                echo=config.DEBUG,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600,
                poolclass=QueuePool,
            )
            
            # Проверяем подключение
            with self._engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                logger.info("Database connection test successful!")
            
            self._session_factory = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine
            )
            
            logger.info("Database initialized successfully!")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    @property
    def engine(self):
        if not self._engine:
            self.init_engine()
        return self._engine
    
    @property
    def session_factory(self):
        if not self._session_factory:
            self.init_engine()
        return self._session_factory
    
    def create_session(self) -> Session:
        """Создать новую сессию"""
        return self.session_factory()
    
    def get_db(self) -> Generator[Session, None, None]:
        """Dependency для получения сессии БД"""
        db = self.create_session()
        try:
            yield db
        finally:
            db.close()
    
    def health_check(self) -> bool:
        """Проверка здоровья БД"""
        try:
            with self.engine.connect() as conn:
                # Используем text() для выполнения сырого SQL
                conn.execute(text("SELECT 1"))
            logger.debug("Database health check passed!")
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False

# Создаем глобальный экземпляр
db_manager = DatabaseManager()