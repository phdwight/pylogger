"""Example usage of the configurable logger."""

from __future__ import annotations

from pathlib import Path

# Try to import from installed package first, fallback to local development
try:
    from pylogger import ConfigurableLogger, LoggerConfig, LogLevel
except ImportError:
    # Development mode - add src to path
    import sys
    sys.path.insert(0, str(Path(__file__).parent / "src"))
    from pylogger import ConfigurableLogger, LoggerConfig, LogLevel


def main() -> None:
    """Demonstrate various logger configurations and usage patterns."""
    
    print("=== Basic Logger Usage ===")
    # Basic usage with defaults
    logger = ConfigurableLogger()
    logger.info("Application started with default configuration")
    logger.debug("This is a debug message")
    logger.warning("This is a warning")
    logger.error("This is an error")
    
    print("\n=== Custom Configuration ===")
    # Custom configuration
    custom_config = LoggerConfig(
        level=LogLevel.INFO,
        log_file_path=Path("logs/custom_app.log"),
        max_file_size_mb=10,
        backup_count=3,
        enable_json_format=True,
        extra_fields={"app_name": "demo", "version": "1.0.0"},
    )
    
    custom_logger = ConfigurableLogger("custom_app", config=custom_config)
    custom_logger.info("Custom logger initialized", user_id=12345)
    custom_logger.error("Sample error with context", operation="file_read")
    
    print("\n=== Container-Optimized Logger ===")
    # Container-optimized configuration
    container_config = LoggerConfig.for_container()
    container_logger = ConfigurableLogger("container_app", config=container_config)
    container_logger.info("Container application started")
    container_logger.warning("Memory usage high", memory_percent=85.2)
    
    print("\n=== Environment-Based Configuration ===")
    # Environment-based configuration
    env_config = LoggerConfig.from_env()
    env_logger = ConfigurableLogger("env_app", config=env_config)
    env_logger.info("Environment-configured logger initialized")
    
    print("\n=== Exception Logging ===")
    # Exception logging example
    try:
        result = 1 / 0
    except ZeroDivisionError:
        logger.exception("Division by zero occurred")
    
    print("\n=== Log Level Examples ===")
    # Demonstrate all log levels
    for level in LogLevel:
        logger.log(level.value, f"This is a {level.name} message")
    
    print("\nLogs have been written to the logs directory.")
    print("Check the following files:")
    print("- logs/app.log (default logger)")
    print("- logs/custom_app.log (custom logger)")


if __name__ == "__main__":
    main()
