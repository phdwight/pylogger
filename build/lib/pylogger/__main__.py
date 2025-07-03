"""Main entry point for the pylogger module."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> None:
    """Run the example when module is called directly."""
    print("PyLogger - Configurable Python Logger")
    print("=" * 40)
    
    # Import and run the example
    example_file = Path(__file__).parent.parent.parent / "example.py"
    if example_file.exists():
        print(f"Running example from: {example_file}")
        print()
        
        # Execute the example file
        import runpy
        sys.path.insert(0, str(example_file.parent))
        runpy.run_path(str(example_file))
    else:
        print("Example file not found. Creating a simple demo...")
        from pylogger import ConfigurableLogger, LoggerConfig, LogLevel
        
        logger = ConfigurableLogger("demo")
        logger.info("PyLogger is working correctly!")
        logger.debug("This is a debug message")
        logger.warning("This is a warning")
        logger.error("This is an error")
        
        print("\nPyLogger demo completed successfully!")
        print("Check the logs/ directory for output files.")


if __name__ == "__main__":
    main()
