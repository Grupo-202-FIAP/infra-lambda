import os
import json
import logging
from typing import Optional, Dict

_configured = False

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "time": self.formatTime(record, datefmt="%Y-%m-%dT%H:%M:%S"),
            "module": record.module,
            "func": record.funcName,
            "line": record.lineno,
        }
        extra = getattr(record, "__dict__", {})
        for k in ("request_id", "correlation_id"):
            if k in extra:
                payload[k] = extra[k]
        return json.dumps(payload, ensure_ascii=False)

def _configure_root_logger():
    global _configured
    if _configured:
        return
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    root = logging.getLogger()
    root.setLevel(level)
    if not root.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        root.addHandler(handler)
    _configured = True

class _Adapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        if "extra" not in kwargs:
            kwargs["extra"] = {}
        kwargs["extra"].update(self.extra or {})
        return msg, kwargs

def get_logger(name: Optional[str] = None, extra: Optional[Dict] = None) -> logging.Logger:
    _configure_root_logger()
    logger = logging.getLogger(name or __name__)
    return _Adapter(logger, extra or {})
