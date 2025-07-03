"""Tests for the JSON formatter."""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime

import pytest

from pylogger.formatters import JsonFormatter


class TestJsonFormatter:
    """Test cases for JsonFormatter."""
    
    def test_basic_formatting(self) -> None:
        """Test basic JSON formatting."""
        formatter = JsonFormatter()
        record = logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname="/path/to/file.py",
            lineno=42,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        
        formatted = formatter.format(record)
        data = json.loads(formatted)
        
        assert data["message"] == "Test message"
        assert data["level"] == "INFO"
        assert data["logger"] == "test_logger"
        assert data["line"] == 42
        assert "timestamp" in data
    
    def test_extra_fields_from_config(self) -> None:
        """Test extra fields from formatter configuration."""
        extra_fields = {"app_name": "test_app", "version": "1.0.0"}
        formatter = JsonFormatter(extra_fields=extra_fields)
        
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="/test.py",
            lineno=1,
            msg="Test",
            args=(),
            exc_info=None,
        )
        
        formatted = formatter.format(record)
        data = json.loads(formatted)
        
        assert data["app_name"] == "test_app"
        assert data["version"] == "1.0.0"
    
    def test_extra_fields_from_record(self) -> None:
        """Test extra fields from log record."""
        formatter = JsonFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="/test.py",
            lineno=1,
            msg="Test",
            args=(),
            exc_info=None,
        )
        
        # Add extra field to record
        record.user_id = 12345  # type: ignore
        record.operation = "test_op"  # type: ignore
        
        formatted = formatter.format(record)
        data = json.loads(formatted)
        
        assert data["user_id"] == 12345
        assert data["operation"] == "test_op"
    
    def test_exception_formatting(self) -> None:
        """Test exception formatting in JSON."""
        formatter = JsonFormatter()
        
        try:
            raise ValueError("Test exception")
        except ValueError:
            exc_info = logging.sys.exc_info()
        
        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="/test.py",
            lineno=1,
            msg="Error occurred",
            args=(),
            exc_info=exc_info,
        )
        
        formatted = formatter.format(record)
        data = json.loads(formatted)
        
        assert "exception" in data
        assert "ValueError: Test exception" in data["exception"]
        assert "Traceback" in data["exception"]
    
    def test_timestamp_format(self) -> None:
        """Test timestamp formatting."""
        formatter = JsonFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="/test.py",
            lineno=1,
            msg="Test",
            args=(),
            exc_info=None,
        )
        
        formatted = formatter.format(record)
        data = json.loads(formatted)
        
        # Verify timestamp is in ISO format
        timestamp = data["timestamp"]
        datetime.fromisoformat(timestamp)  # Should not raise exception
    
    def test_ensure_ascii_option(self) -> None:
        """Test ensure_ascii option."""
        formatter = JsonFormatter(ensure_ascii=True)
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="/test.py",
            lineno=1,
            msg="Test with unicode: café",
            args=(),
            exc_info=None,
        )
        
        formatted = formatter.format(record)
        
        # With ensure_ascii=True, unicode should be escaped
        assert "caf\\u00e9" in formatted
