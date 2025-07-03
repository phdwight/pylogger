#!/usr/bin/env python3
"""Script to publish PyLogger to PyPI."""

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
        if result.stdout.strip():
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
    """Main publishing function."""
    print("📦 Publishing PyLogger to PyPI...")
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ Error: pyproject.toml not found. Run this from the project root.")
        sys.exit(1)
    
    # Clean previous builds
    print("🧹 Cleaning previous builds...")
    for dir_name in ["build", "dist", "src/configurable_pylogger.egg-info"]:
        dir_path = Path(dir_name)
        if dir_path.exists():
            import shutil
            shutil.rmtree(dir_path)
    
    # Run tests first
    run_command(
        ["python", "-m", "pytest", "tests/", "-v"],
        "Running tests"
    )
    
    # Build the package
    run_command(
        ["python", "-m", "build"],
        "Building package"
    )
    
    # Check the package
    run_command(
        ["python", "-m", "twine", "check", "dist/*"],
        "Checking package"
    )
    
    # Upload to TestPyPI first (optional)
    print("\n🤔 Upload to TestPyPI first? (y/n): ", end="")
    if input().lower().startswith('y'):
        run_command(
            ["python", "-m", "twine", "upload", "--repository", "testpypi", "dist/*"],
            "Uploading to TestPyPI"
        )
        print("\n✅ Uploaded to TestPyPI successfully!")
        print("🔗 Check: https://test.pypi.org/project/configurable-pylogger/")
        print("\n🤔 Continue with PyPI upload? (y/n): ", end="")
        if not input().lower().startswith('y'):
            print("🛑 PyPI upload cancelled.")
            return
    
    # Upload to PyPI
    run_command(
        ["python", "-m", "twine", "upload", "dist/*"],
        "Uploading to PyPI"
    )
    
    print("\n🎉 Package published successfully!")
    print("🔗 Check: https://pypi.org/project/configurable-pylogger/")
    print("\n📝 Install with: pip install configurable-pylogger")


if __name__ == "__main__":
    main()
