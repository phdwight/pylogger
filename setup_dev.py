#!/usr/bin/env python3
"""Development setup script for PyLogger."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def run_command(command: list[str], description: str, check: bool = True) -> bool:
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, check=check, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"⚠️  {description} completed with warnings")
            if result.stderr:
                print(f"STDERR: {result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        if check:
            sys.exit(1)
        return False


def main() -> None:
    """Set up development environment."""
    print("🚀 Setting up PyLogger development environment...")
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ Error: pyproject.toml not found. Run this from the project root.")
        sys.exit(1)
    
    # Install development dependencies
    run_command(
        ["python", "-m", "pip", "install", "-e", ".[dev]"],
        "Installing package in development mode with dev dependencies"
    )
    
    # Install pre-commit hooks (if available)
    run_command(
        ["python", "-m", "pip", "install", "pre-commit"],
        "Installing pre-commit",
        check=False
    )
    
    # Run tests to verify installation
    run_command(
        ["python", "-c", "from pylogger import ConfigurableLogger; print('✅ Import successful')"],
        "Testing package import"
    )
    
    # Run a quick test
    run_command(
        ["python", "example.py"],
        "Running example script"
    )
    
    print("\n🎉 Development environment setup completed!")
    print("\n📝 Available commands:")
    print("  • Run tests: pytest")
    print("  • Format code: black src/ tests/")
    print("  • Sort imports: isort src/ tests/")
    print("  • Lint code: flake8 src/ tests/")
    print("  • Type check: mypy src/")
    print("  • Build package: python build.py")
    print("  • Publish package: python publish.py")
    print("  • Run as module: python -m pylogger")


if __name__ == "__main__":
    main()
