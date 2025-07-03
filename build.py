#!/usr/bin/env python3
"""Build script for PyLogger package."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def run_command(command: list[str], description: str) -> None:
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        sys.exit(1)


def main() -> None:
    """Main build function."""
    print("🚀 Building PyLogger package...")
    
    # Clean previous builds
    run_command(
        ["python", "-m", "pip", "uninstall", "configurable-pylogger", "-y"],
        "Uninstalling previous version"
    )
    
    # Clean build directories
    for dir_name in ["build", "dist", "src/configurable_pylogger.egg-info"]:
        dir_path = Path(dir_name)
        if dir_path.exists():
            import shutil
            shutil.rmtree(dir_path)
            print(f"🧹 Cleaned {dir_name}")
    
    # Build the package
    run_command(
        ["python", "-m", "build"],
        "Building wheel and source distribution"
    )
    
    # Install in development mode
    run_command(
        ["python", "-m", "pip", "install", "-e", "."],
        "Installing in development mode"
    )
    
    print("\n🎉 Build completed successfully!")
    print("📦 Package files created in dist/")
    print("🔧 Package installed in development mode")
    print("\n📝 Next steps:")
    print("  • Test the installation: python -c 'from pylogger import ConfigurableLogger'")
    print("  • Run tests: pytest")
    print("  • Upload to PyPI: python -m twine upload dist/*")


if __name__ == "__main__":
    main()
