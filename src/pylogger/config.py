"""Configuration classes for the logger."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class LogLevel(Enum):
    """Available log levels with their numeric values."""
    
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

    @classmethod
    def from_string(cls, level: str) -> LogLevel:
        """Convert string to LogLevel enum.
        
        Args:
            level: String representation of log level (case-insensitive)
            
        Returns:
            LogLevel enum value
            
        Raises:
            ValueError: If level string is not valid
        """
        level_upper = level.upper()
        try:
            return cls[level_upper]
        except KeyError:
            valid_levels = [level.name for level in cls]
            raise ValueError(
                f"Invalid log level '{level}'. "
                f"Valid options: {', '.join(valid_levels)}"
            )


@dataclass(slots=True, frozen=True)
class LoggerConfig:
    """Configuration for the logger system.
    
    This class encapsulates all configuration options for the logger,
    providing sensible defaults while allowing full customization.
    
    Attributes:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Whether to enable file logging
        log_to_console: Whether to enable console logging
        log_file_path: Path to the log file (created if doesn't exist)
        max_file_size_mb: Maximum size of each log file in MB
        backup_count: Number of backup files to keep
        format_string: Custom log format string
        date_format: Date format for log timestamps
        enable_json_format: Whether to use JSON formatting
        extra_fields: Additional fields to include in logs
    """
    
    # Core logging settings
    level: LogLevel = LogLevel.DEBUG
    log_to_file: bool = True
    log_to_console: bool = True
    
    # File logging settings
    log_file_path: Path = field(default_factory=lambda: Path("logs/app.log"))
    max_file_size_mb: int = 5
    backup_count: int = 5
    
    # Formatting settings
    format_string: str = (
        "%(asctime)s - %(name)s - %(levelname)s - "
        "%(filename)s:%(lineno)d - %(message)s"
    )
    date_format: str = "%Y-%m-%d %H:%M:%S"
    enable_json_format: bool = False
    
    # Additional configuration
    extra_fields: dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        if self.max_file_size_mb <= 0:
            raise ValueError("max_file_size_mb must be positive")
        
        if self.backup_count < 0:
            raise ValueError("backup_count must be non-negative")
        
        if not self.log_to_file and not self.log_to_console:
            raise ValueError("At least one output method must be enabled")
    
    @classmethod
    def from_env(cls) -> LoggerConfig:
        """Create configuration from environment variables.
        
        Environment variables:
            LOG_LEVEL: Log level (default: DEBUG)
            LOG_TO_FILE: Enable file logging (default: true)
            LOG_TO_CONSOLE: Enable console logging (default: true)
            LOG_FILE_PATH: Path to log file (default: logs/app.log)
            LOG_MAX_SIZE_MB: Max file size in MB (default: 5)
            LOG_BACKUP_COUNT: Number of backup files (default: 5)
            LOG_JSON_FORMAT: Enable JSON formatting (default: false)
            
        Returns:
            LoggerConfig instance with environment-based settings
        """
        def get_bool(key: str, default: bool) -> bool:
            value = os.getenv(key, str(default)).lower()
            return value in ("true", "1", "yes", "on")
        
        def get_int(key: str, default: int) -> int:
            try:
                return int(os.getenv(key, str(default)))
            except ValueError:
                return default
        
        level_str = os.getenv("LOG_LEVEL", "DEBUG")
        try:
            level = LogLevel.from_string(level_str)
        except ValueError:
            level = LogLevel.DEBUG
        
        return cls(
            level=level,
            log_to_file=get_bool("LOG_TO_FILE", True),
            log_to_console=get_bool("LOG_TO_CONSOLE", True),
            log_file_path=Path(os.getenv("LOG_FILE_PATH", "logs/app.log")),
            max_file_size_mb=get_int("LOG_MAX_SIZE_MB", 5),
            backup_count=get_int("LOG_BACKUP_COUNT", 5),
            enable_json_format=get_bool("LOG_JSON_FORMAT", False),
        )
    
    @classmethod
    def for_container(cls) -> LoggerConfig:
        """Create configuration optimized for container environments.
        
        Returns:
            LoggerConfig with console-only logging and JSON format
        """
        return cls(
            level=LogLevel.INFO,
            log_to_file=False,
            log_to_console=True,
            enable_json_format=True,
        )
