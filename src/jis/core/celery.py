# celery.py
# TODO: raw


from celery import Celery
from celery.result import AsyncResult
from typing import Optional


from .config import config
from .logger import get_logger


logger = get_logger(__name__)


class CeleryManager:
    """Менеджер для работы с Celery"""
    
    def __init__(self):
        self._app: Optional[Celery] = None
        self._broker_url = config.CELERY_BROKER_URL
        self._result_backend = config.CELERY_RESULT_BACKEND
    
    def init_app(self) -> Celery:
        """Инициализация Celery приложения"""
        self._app = Celery(
            "jis",
            broker=self._broker_url,
            backend=self._result_backend,
            include=["jis.tasks"]  # Путь к задачам
        )
        
        # Настройки Celery
        self._app.conf.update(
            task_serializer="json",
            accept_content=["json"],
            result_serializer="json",
            timezone="UTC",
            enable_utc=True,
            task_track_started=True,
            task_time_limit=30 * 60,  # 30 минут
            task_soft_time_limit=25 * 60,  # 25 минут
            worker_prefetch_multiplier=1,
            task_acks_late=True,
            task_reject_on_worker_lost=True,
            result_expires=3600,  # 1 час
        )
        
        logger.info("✅ Celery инициализирован")
        return self._app
    
    @property
    def app(self) -> Optional[Celery]:
        """Получить Celery приложение"""
        return self._app
    
    def get_task_info(self, task_id: str) -> Optional[dict]:
        """Получить информацию о задаче"""
        if not self._app:
            return None
        
        task_result = AsyncResult(task_id, app=self._app)
        
        return {
            "task_id": task_id,
            "status": task_result.status,
            "result": task_result.result if task_result.ready() else None,
        }
    
    def health_check(self) -> bool:
        """Проверка здоровья Celery"""
        try:
            if self._app:
                # Простая проверка - отправляем тестовую задачу
                inspect = self._app.control.inspect()
                stats = inspect.stats()
                return bool(stats)
            return False
        except Exception as e:
            logger.error(f"Celery health check failed: {e}")
            return False


celery_manager = CeleryManager()
