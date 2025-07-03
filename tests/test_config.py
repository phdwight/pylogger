"""Tests for the logger configuration."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest

from pylogger.config import LogLevel, LoggerConfig


class TestLogLevel:
    """Test cases for LogLevel enum."""
    
    def test_from_string_valid_levels(self) -> None:
        """Test conversion from valid string levels."""
        assert LogLevel.from_string("debug") == LogLevel.DEBUG
        assert LogLevel.from_string("DEBUG") == LogLevel.DEBUG
        assert LogLevel.from_string("Info") == LogLevel.INFO
        assert LogLevel.from_string("WARNING") == LogLevel.WARNING
        assert LogLevel.from_string("error") == LogLevel.ERROR
        assert LogLevel.from_string("CRITICAL") == LogLevel.CRITICAL
    
    def test_from_string_invalid_level(self) -> None:
        """Test conversion from invalid string level."""
        with pytest.raises(ValueError, match="Invalid log level 'INVALID'"):
            LogLevel.from_string("INVALID")


class TestLoggerConfig:
    """Test cases for LoggerConfig."""
    
    def test_default_configuration(self) -> None:
        """Test default configuration values."""
        config = LoggerConfig()
        
        assert config.level == LogLevel.DEBUG
        assert config.log_to_file is True
        assert config.log_to_console is True
        assert config.max_file_size_mb == 5
        assert config.backup_count == 5
        assert config.enable_json_format is False
        assert config.extra_fields == {}
    
    def test_custom_configuration(self) -> None:
        """Test custom configuration values."""
        custom_path = Path("custom.log")
        extra_fields = {"app": "test"}
        
        config = LoggerConfig(
            level=LogLevel.INFO,
            log_file_path=custom_path,
            max_file_size_mb=10,
            backup_count=3,
            enable_json_format=True,
            extra_fields=extra_fields,
        )
        
        assert config.level == LogLevel.INFO
        assert config.log_file_path == custom_path
        assert config.max_file_size_mb == 10
        assert config.backup_count == 3
        assert config.enable_json_format is True
        assert config.extra_fields == extra_fields
    
    def test_validation_invalid_file_size(self) -> None:
        """Test validation of invalid file size."""
        with pytest.raises(ValueError, match="max_file_size_mb must be positive"):
            LoggerConfig(max_file_size_mb=0)
    
    def test_validation_invalid_backup_count(self) -> None:
        """Test validation of invalid backup count."""
        with pytest.raises(ValueError, match="backup_count must be non-negative"):
            LoggerConfig(backup_count=-1)
    
    def test_validation_no_output_methods(self) -> None:
        """Test validation when no output methods are enabled."""
        with pytest.raises(
            ValueError, 
            match="At least one output method must be enabled"
        ):
            LoggerConfig(log_to_file=False, log_to_console=False)
    
    def test_from_env_defaults(self) -> None:
        """Test environment configuration with default values."""
        # Clear any existing environment variables
        env_vars = [
            "LOG_LEVEL", "LOG_TO_FILE", "LOG_TO_CONSOLE", 
            "LOG_FILE_PATH", "LOG_MAX_SIZE_MB", "LOG_BACKUP_COUNT",
            "LOG_JSON_FORMAT"
        ]
        
        for var in env_vars:
            os.environ.pop(var, None)
        
        config = LoggerConfig.from_env()
        
        assert config.level == LogLevel.DEBUG
        assert config.log_to_file is True
        assert config.log_to_console is True
        assert config.log_file_path == Path("logs/app.log")
        assert config.max_file_size_mb == 5
        assert config.backup_count == 5
        assert config.enable_json_format is False
    
    def test_from_env_custom_values(self) -> None:
        """Test environment configuration with custom values."""
        env_vars = {
            "LOG_LEVEL": "INFO",
            "LOG_TO_FILE": "false",
            "LOG_TO_CONSOLE": "true",
            "LOG_FILE_PATH": "custom/path.log",
            "LOG_MAX_SIZE_MB": "20",
            "LOG_BACKUP_COUNT": "10",
            "LOG_JSON_FORMAT": "true",
        }
        
        # Set environment variables
        for key, value in env_vars.items():
            os.environ[key] = value
        
        try:
            config = LoggerConfig.from_env()
            
            assert config.level == LogLevel.INFO
            assert config.log_to_file is False
            assert config.log_to_console is True
            assert config.log_file_path == Path("custom/path.log")
            assert config.max_file_size_mb == 20
            assert config.backup_count == 10
            assert config.enable_json_format is True
        finally:
            # Clean up environment variables
            for key in env_vars:
                os.environ.pop(key, None)
    
    def test_for_container(self) -> None:
        """Test container-optimized configuration."""
        config = LoggerConfig.for_container()
        
        assert config.level == LogLevel.INFO
        assert config.log_to_file is False
        assert config.log_to_console is True
        assert config.enable_json_format is True
