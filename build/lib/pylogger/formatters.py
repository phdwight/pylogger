"""JSON formatter for structured logging."""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any


class JsonFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    
    def __init__(
        self,
        extra_fields: dict[str, Any] | None = None,
        *,
        ensure_ascii: bool = False,
    ) -> None:
        """Initialize JSON formatter.
        
        Args:
            extra_fields: Additional fields to include in every log record
            ensure_ascii: Whether to ensure ASCII-only output
        """
        super().__init__()
        self.extra_fields = extra_fields or {}
        self.ensure_ascii = ensure_ascii
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON.
        
        Args:
            record: The log record to format
            
        Returns:
            JSON-formatted log string
        """
        log_data: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields from configuration
        log_data.update(self.extra_fields)
        
        # Add any extra fields from the log record
        for key, value in record.__dict__.items():
            if key not in {
                "name", "msg", "args", "levelname", "levelno", "pathname",
                "filename", "module", "lineno", "funcName", "created",
                "msecs", "relativeCreated", "thread", "threadName",
                "processName", "process", "getMessage", "exc_info",
                "exc_text", "stack_info",
            } and not key.startswith("_"):
                log_data[key] = value
        
        return json.dumps(log_data, ensure_ascii=self.ensure_ascii, default=str)
