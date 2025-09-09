from datetime import datetime, timedelta
from typing import Any, Optional
import hashlib
import json
from .models import CacheEntry


class Cache:
    def __init__(self, ttl_seconds: int = 3600):
        self._cache = {}
        self._ttl_seconds = ttl_seconds

    def _generate_key(self, data: Any) -> str:
        """Gera uma chave única para os dados"""
        if isinstance(data, str):
            content = data
        else:
            content = json.dumps(data, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """Recupera um item do cache se ainda estiver válido"""
        entry = self._cache.get(key)
        if not entry:
            return None

        if datetime.utcnow() > entry.expires_at:
            del self._cache[key]
            return None

        return entry.value

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Armazena um item no cache"""
        expires_at = datetime.utcnow() + timedelta(seconds=ttl or self._ttl_seconds)
        self._cache[key] = CacheEntry(
            key=key,
            value=value,
            expires_at=expires_at
        )

    def invalidate(self, key: str) -> None:
        """Remove um item específico do cache"""
        if key in self._cache:
            del self._cache[key]

    def clear(self) -> None:
        """Limpa todo o cache"""
        self._cache.clear()

    def cleanup(self) -> None:
        """Remove entradas expiradas do cache"""
        now = datetime.utcnow()
        expired_keys = [
            key for key, entry in self._cache.items()
            if now > entry.expires_at
        ]
        for key in expired_keys:
            del self._cache[key]
