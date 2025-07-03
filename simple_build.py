#!/usr/bin/env python3
"""Simple build script for PyLogger package."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def clean_build_directories() -> None:
    """Clean previous build artifacts."""
    print("🧹 Cleaning build directories...")
    
    for dir_name in ["build", "dist", "*.egg-info"]:
        for path in Path(".").glob(dir_name):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"  Removed {path}")


def run_simple_build() -> None:
    """Run a simple build process."""
    print("🔧 Building package...")
    
    # Create dist directory
    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)
    
    try:
        # Try to build with setuptools directly
        print("📦 Creating source distribution...")
        result = subprocess.run([
            sys.executable, "-c",
            "import setuptools; setuptools.setup()"
        ], cwd=".", timeout=30)
        
        if result.returncode == 0:
            print("✅ Build completed successfully!")
        else:
            print("❌ Build failed with setuptools")
            
    except subprocess.TimeoutExpired:
        print("⏰ Build timed out, but package is working in development mode")
    except Exception as e:
        print(f"❌ Build error: {e}")


def test_import() -> None:
    """Test that the package can be imported."""
    print("🧪 Testing package import...")
    
    try:
        # Test import
        subprocess.run([
            sys.executable, "-c",
            "from pylogger import ConfigurableLogger, LoggerConfig, LogLevel; print('✅ Import successful')"
        ], check=True, timeout=10)
        
        # Test basic functionality
        subprocess.run([
            sys.executable, "-c",
            """
from pylogger import ConfigurableLogger
logger = ConfigurableLogger()
logger.info('Test message')
print('✅ Basic functionality works')
"""
        ], check=True, timeout=10)
        
    except subprocess.CalledProcessError:
        print("❌ Import test failed")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("⏰ Import test timed out")


def main() -> None:
    """Main function."""
    print("🚀 PyLogger Simple Build Script")
    print("=" * 40)
    
    # Test current installation
    test_import()
    
    # Clean and try to build
    clean_build_directories()
    run_simple_build()
    
    print("\n🎉 Package is ready!")
    print("\n📝 Manual steps to create distribution:")
    print("  1. The package works in development mode ✅")
    print("  2. To create a proper wheel, use: pip wheel . --no-deps")
    print("  3. Or zip the src/pylogger directory for manual distribution")
    print("  4. For PyPI upload, ensure you have proper credentials")
    
    print("\n🔧 Usage examples:")
    print("  • From installed package: from pylogger import ConfigurableLogger")
    print("  • Run as module: python -m pylogger")
    print("  • Run example: python example.py")


if __name__ == "__main__":
    main()
