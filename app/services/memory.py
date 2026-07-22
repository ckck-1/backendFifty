"""In-memory session store for agent context sharing (Redis-optional)."""
from __future__ import annotations

import json
import logging
from typing import Any, Optional
from uuid import UUID

logger = logging.getLogger(__name__)


class MemoryService:
    """Lightweight key-value store for passing context between agents.

    Falls back to an in-process dict when Redis is unavailable.
    """

    def __init__(self) -> None:
        self._store: dict[str, str] = {}
        self._redis_client = None
        self._try_connect()

    # ── Redis bootstrap (optional) ────────────────────────────────

    def _try_connect(self) -> None:
        try:
            import redis
            from app.config import get_settings

            settings = get_settings()
            if settings.REDIS_URL:
                self._redis_client = redis.Redis.from_url(
                    settings.REDIS_URL, decode_responses=True
                )
                self._redis_client.ping()
                logger.info("Connected to Redis")
        except Exception:
            logger.info("Redis unavailable — using in-memory store")
            self._redis_client = None

    # ── CRUD ──────────────────────────────────────────────────────

    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """Store a JSON-serialisable value."""
        payload = json.dumps(value, default=str)
        if self._redis_client:
            self._redis_client.setex(key, ttl, payload)
        else:
            self._store[key] = payload

    def get(self, key: str) -> Optional[Any]:
        """Retrieve a stored value."""
        payload: Optional[str] = None
        if self._redis_client:
            payload = self._redis_client.get(key)
        else:
            payload = self._store.get(key)
        if payload is None:
            return None
        return json.loads(payload)

    def delete(self, key: str) -> None:
        """Remove a key."""
        if self._redis_client:
            self._redis_client.delete(key)
        else:
            self._store.pop(key, None)

    def clear(self) -> None:
        """Flush all keys."""
        if self._redis_client:
            self._redis_client.flushdb()
        else:
            self._store.clear()


memory_service = MemoryService()
