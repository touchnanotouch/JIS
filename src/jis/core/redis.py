# src/jis/redis.py
# TODO: raw


import redis.asyncio as redis
from typing import Optional
import logging
from contextlib import asynccontextmanager

from .config import config

logger = logging.getLogger(__name__)

class RedisManager:
    """Менеджер для работы с Redis"""
    
    def __init__(self):
        self._client: Optional[redis.Redis] = None
        self._url = config.REDIS_URL
    
    async def connect(self) -> bool:
        """Подключение к Redis"""
        try:
            self._client = redis.from_url(
                self._url,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=5,
                socket_keepalive=True,
                health_check_interval=30
            )
            
            # Проверяем подключение
            await self._client.ping()
            logger.info("✅ Redis подключен")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка подключения к Redis: {e}")
            self._client = None
            return False
    
    async def disconnect(self):
        """Отключение от Redis"""
        if self._client:
            await self._client.close()
            self._client = None
            logger.info("🔌 Redis отключен")
    
    @property
    def client(self) -> Optional[redis.Redis]:
        """Получить клиент Redis"""
        return self._client
    
    async def health_check(self) -> bool:
        """Проверка здоровья Redis"""
        try:
            if self._client:
                await self._client.ping()
                return True
            return False
        except Exception:
            return False

# Создаем глобальный экземпляр
redis_manager = RedisManager()