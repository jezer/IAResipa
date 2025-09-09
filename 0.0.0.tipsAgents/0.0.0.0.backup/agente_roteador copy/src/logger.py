import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

class RouterLogger:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.setup_logging()

    def setup_logging(self):
        log_config = self.config["logging"]
        log_dir = Path(log_config["path"])
        log_dir.mkdir(parents=True, exist_ok=True)

        current_date = datetime.now().strftime('%Y%m%d')
        log_file = log_dir / f"router_{current_date}.ndjson"

        logging.basicConfig(
            filename=str(log_file),
            level=getattr(logging, log_config["level"].upper()),
            format='',  # Usando formato vazio pois vamos formatar manualmente
        )

        # Substituir o formatter padrão por um que use nosso formato personalizado
        for handler in logging.root.handlers:
            handler.formatter = CustomJsonFormatter(log_config["format"])

class CustomJsonFormatter(logging.Formatter):
    def __init__(self, format_dict: Dict[str, str]):
        super().__init__()
        self.format_dict = format_dict

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage()
        }

        if hasattr(record, 'request_id'):
            log_data["request_id"] = record.request_id
        if hasattr(record, 'action'):
            log_data["action"] = record.action
        if hasattr(record, 'reasoning'):
            log_data["reasoning"] = record.reasoning

        return json.dumps(log_data)

def log_routing_decision(logger: logging.Logger, decision: Dict[str, Any]):
    """
    Registra uma decisão de roteamento no log
    """
    extra = {
        "request_id": decision.get("request_id"),
        "action": decision.get("action"),
        "reasoning": decision.get("reasoning", {})
    }
    
    logger.info(
        f"Routing decision made",
        extra=extra
    )
