"""Tests for the main logger functionality."""

from __future__ import annotations

import json
import logging
import tempfile
from pathlib import Path

import pytest

from pylogger import ConfigurableLogger, LoggerConfig, LogLevel


class TestConfigurableLogger:
    """Test cases for ConfigurableLogger."""
    
    def test_default_initialization(self) -> None:
        """Test logger initialization with default configuration."""
        logger = ConfigurableLogger()
        
        assert logger.config.level == LogLevel.DEBUG
        assert isinstance(logger.get_logger(), logging.Logger)
    
    def test_custom_name_and_config(self) -> None:
        """Test logger with custom name and configuration."""
        config = LoggerConfig(level=LogLevel.INFO)
        logger = ConfigurableLogger("test_logger", config=config)
        
        assert logger.config.level == LogLevel.INFO
        assert logger.get_logger().name == "test_logger"
    
    def test_file_logging(self) -> None:
        """Test file logging functionality."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "test.log"
            config = LoggerConfig(
                log_file_path=log_file,
                log_to_console=False,
                level=LogLevel.INFO,
            )
            
            logger = ConfigurableLogger("file_test", config=config)
            logger.info("Test message")
            
            assert log_file.exists()
            content = log_file.read_text()
            assert "Test message" in content
            assert "INFO" in content
    
    def test_json_logging(self) -> None:
        """Test JSON format logging."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "test.log"
            config = LoggerConfig(
                log_file_path=log_file,
                log_to_console=False,
                enable_json_format=True,
                level=LogLevel.INFO,
                extra_fields={"app": "test"},
            )
            
            logger = ConfigurableLogger("json_test", config=config)
            logger.info("JSON test message", user_id=123)
            
            assert log_file.exists()
            content = log_file.read_text().strip()
            log_data = json.loads(content)
            
            assert log_data["message"] == "JSON test message"
            assert log_data["level"] == "INFO"
            assert log_data["app"] == "test"
            assert log_data["user_id"] == 123
    
    def test_all_log_methods(self) -> None:
        """Test all logging methods."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "test.log"
            config = LoggerConfig(
                log_file_path=log_file,
                log_to_console=False,
                level=LogLevel.DEBUG,
            )
            
            logger = ConfigurableLogger("method_test", config=config)
            
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")
            logger.critical("Critical message")
            logger.log(logging.INFO, "Custom level message")
            
            content = log_file.read_text()
            assert "Debug message" in content
            assert "Info message" in content
            assert "Warning message" in content
            assert "Error message" in content
            assert "Critical message" in content
            assert "Custom level message" in content
    
    def test_exception_logging(self) -> None:
        """Test exception logging with traceback."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "test.log"
            config = LoggerConfig(
                log_file_path=log_file,
                log_to_console=False,
                level=LogLevel.ERROR,
            )
            
            logger = ConfigurableLogger("exception_test", config=config)
            
            try:
                raise ValueError("Test exception")
            except ValueError:
                logger.exception("Exception occurred")
            
            content = log_file.read_text()
            assert "Exception occurred" in content
            assert "ValueError: Test exception" in content
            assert "Traceback" in content
    
    def test_config_update(self) -> None:
        """Test runtime configuration update."""
        logger = ConfigurableLogger()
        original_level = logger.config.level
        
        new_config = LoggerConfig(level=LogLevel.ERROR)
        logger.update_config(new_config)
        
        assert logger.config.level != original_level
        assert logger.config.level == LogLevel.ERROR
    
    def test_file_rotation_setup(self) -> None:
        """Test that file rotation is properly configured."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "rotate_test.log"
            config = LoggerConfig(
                log_file_path=log_file,
                log_to_console=False,
                max_file_size_mb=1,  # Small size for testing
                backup_count=3,
            )
            
            logger = ConfigurableLogger("rotate_test", config=config)
            
            # Check that handlers are properly configured
            file_handlers = [
                h for h in logger.get_logger().handlers 
                if hasattr(h, "maxBytes")
            ]
            
            assert len(file_handlers) == 1
            handler = file_handlers[0]
            assert handler.maxBytes == 1024 * 1024  # 1MB
            assert handler.backupCount == 3
