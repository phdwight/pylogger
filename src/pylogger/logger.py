"""Main logger implementation."""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

from .config import LoggerConfig
from .formatters import JsonFormatter


class ConfigurableLogger:
    """A configurable logger with rotation and flexible output options.
    
    This logger provides:
    - Rotating file logs with configurable size and backup count
    - Console output option for containers
    - JSON and text formatting options
    - Environment-based configuration
    - Thread-safe operation
    
    Example:
        Basic usage:
        >>> logger = ConfigurableLogger()
        >>> logger.info("Application started")
        
        Custom configuration:
        >>> config = LoggerConfig(
        ...     level=LogLevel.INFO,
        ...     log_file_path=Path("my_app.log"),
        ...     max_file_size_mb=10
        ... )
        >>> logger = ConfigurableLogger(config=config)
        
        Container-optimized:
        >>> config = LoggerConfig.for_container()
        >>> logger = ConfigurableLogger(config=config)
    """
    
    def __init__(
        self,
        name: str = "app",
        config: LoggerConfig | None = None,
    ) -> None:
        """Initialize the configurable logger.
        
        Args:
            name: Logger name (used for logger hierarchy)
            config: Logger configuration (uses defaults if None)
        """
        self._config = config or LoggerConfig()
        self._logger = logging.getLogger(name)
        self._setup_logger()
    
    def _setup_logger(self) -> None:
        """Set up the logger with handlers and formatters."""
        # Clear any existing handlers
        self._logger.handlers.clear()
        
        # Set log level
        self._logger.setLevel(self._config.level.value)
        
        # Prevent propagation to avoid duplicate logs
        self._logger.propagate = False
        
        # Set up formatters
        if self._config.enable_json_format:
            formatter = JsonFormatter(extra_fields=self._config.extra_fields)
        else:
            formatter = logging.Formatter(
                fmt=self._config.format_string,
                datefmt=self._config.date_format,
            )
        
        # Add console handler if enabled
        if self._config.log_to_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self._logger.addHandler(console_handler)
        
        # Add file handler if enabled
        if self._config.log_to_file:
            self._setup_file_handler(formatter)
    
    def _setup_file_handler(self, formatter: logging.Formatter) -> None:
        """Set up rotating file handler.
        
        Args:
            formatter: The formatter to use for file logs
        """
        # Ensure log directory exists
        self._config.log_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Calculate max bytes from MB
        max_bytes = self._config.max_file_size_mb * 1024 * 1024
        
        # Create rotating file handler
        file_handler = RotatingFileHandler(
            filename=self._config.log_file_path,
            maxBytes=max_bytes,
            backupCount=self._config.backup_count,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)
    
    def debug(self, message: str, **kwargs: Any) -> None:
        """Log a debug message.
        
        Args:
            message: The message to log
            **kwargs: Additional fields to include in the log
        """
        self._logger.debug(message, extra=kwargs)
    
    def info(self, message: str, **kwargs: Any) -> None:
        """Log an info message.
        
        Args:
            message: The message to log
            **kwargs: Additional fields to include in the log
        """
        self._logger.info(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs: Any) -> None:
        """Log a warning message.
        
        Args:
            message: The message to log
            **kwargs: Additional fields to include in the log
        """
        self._logger.warning(message, extra=kwargs)
    
    def error(self, message: str, **kwargs: Any) -> None:
        """Log an error message.
        
        Args:
            message: The message to log
            **kwargs: Additional fields to include in the log
        """
        self._logger.error(message, extra=kwargs)
    
    def critical(self, message: str, **kwargs: Any) -> None:
        """Log a critical message.
        
        Args:
            message: The message to log
            **kwargs: Additional fields to include in the log
        """
        self._logger.critical(message, extra=kwargs)
    
    def exception(self, message: str, **kwargs: Any) -> None:
        """Log an exception with traceback.
        
        Args:
            message: The message to log
            **kwargs: Additional fields to include in the log
        """
        self._logger.exception(message, extra=kwargs)
    
    def log(self, level: int, message: str, **kwargs: Any) -> None:
        """Log a message at the specified level.
        
        Args:
            level: Numeric log level
            message: The message to log
            **kwargs: Additional fields to include in the log
        """
        self._logger.log(level, message, extra=kwargs)
    
    def get_logger(self) -> logging.Logger:
        """Get the underlying logger instance.
        
        Returns:
            The configured logger instance
        """
        return self._logger
    
    def update_config(self, new_config: LoggerConfig) -> None:
        """Update logger configuration at runtime.
        
        Args:
            new_config: New configuration to apply
        """
        self._config = new_config
        self._setup_logger()
    
    @property
    def config(self) -> LoggerConfig:
        """Get current logger configuration.
        
        Returns:
            Current LoggerConfig instance
        """
        return self._config
