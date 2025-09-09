from datetime import datetime
from typing import Dict, Optional
import time
import logging
from .models import MetricsData

logger = logging.getLogger(__name__)

class Metrics:
    def __init__(self):
        self.data = MetricsData()
        self._start_times: Dict[str, float] = {}

    def start_request(self, request_id: str) -> None:
        """Registra o início de uma requisição"""
        self._start_times[request_id] = time.time()
        self.data.request_count += 1

    def end_request(self, request_id: str, error: Optional[str] = None) -> None:
        """Registra o fim de uma requisição"""
        if request_id in self._start_times:
            duration = time.time() - self._start_times[request_id]
            self.data.avg_response_time = (
                (self.data.avg_response_time * (self.data.request_count - 1) + duration)
                / self.data.request_count
            )
            del self._start_times[request_id]

        if error:
            self.data.error_count += 1
            logger.error(f"Request {request_id} failed: {error}")

    def record_cache_hit(self) -> None:
        """Registra um hit no cache"""
        self.data.cache_hits += 1

    def record_cache_miss(self) -> None:
        """Registra um miss no cache"""
        self.data.cache_misses += 1

    def get_metrics(self) -> Dict:
        """Retorna as métricas atuais"""
        self.data.last_updated = datetime.utcnow()
        return self.data.dict()

    def reset_metrics(self) -> None:
        """Reseta todas as métricas"""
        self.data = MetricsData()
        self._start_times.clear()


class HealthCheck:
    def __init__(self):
        self._services_status = {}
        self._last_check = {}

    async def check_service(self, service_name: str, check_fn) -> bool:
        """Verifica a saúde de um serviço"""
        try:
            is_healthy = await check_fn()
            self._services_status[service_name] = is_healthy
            self._last_check[service_name] = datetime.utcnow()
            return is_healthy
        except Exception as e:
            logger.error(f"Health check failed for {service_name}: {str(e)}")
            self._services_status[service_name] = False
            return False

    def get_status(self) -> Dict:
        """Retorna o status de todos os serviços"""
        return {
            "status": "healthy" if all(self._services_status.values()) else "unhealthy",
            "services": {
                name: {
                    "status": "healthy" if status else "unhealthy",
                    "last_check": self._last_check.get(name)
                }
                for name, status in self._services_status.items()
            },
            "timestamp": datetime.utcnow()
        }
