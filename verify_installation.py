#!/usr/bin/env python3
"""
Installation Verification Script
"""

import sys
from pathlib import Path

REQUIRED_DIRS = ['backend', 'frontend', 'config', 'logs', 'data', 'models']
REQUIRED_FILES = [
    'backend/main.py',
    'frontend/index.html',
    'firmware/ESP32_RECEIVER.ino',
    'config/system_config.json',
    'requirements.txt'
]

def check_packages():
    """Check if required packages installed"""
    print("[CHECK] Verifying Python packages...")
    
    packages = ['flask', 'flask_cors', 'flask_socketio', 'numpy', 'scipy', 'psutil']
    missing = []
    
    for pkg in packages:
        try:
            __import__(pkg)
            print(f"  ✓ {pkg}")
        except ImportError:
            print(f"  ✗ {pkg}")
            missing.append(pkg)
    
    return len(missing) == 0

def check_files():
    """Check if required files exist"""
    print("\n[CHECK] Verifying files...")
    
    all_ok = True
    for filepath in REQUIRED_FILES:
        if Path(filepath).exists():
            print(f"  ✓ {filepath}")
        else:
            print(f"  ✗ {filepath}")
            all_ok = False
    
    return all_ok

def check_dirs():
    """Check if required directories exist"""
    print("\n[CHECK] Verifying directories...")
    
    all_ok = True
    for dirname in REQUIRED_DIRS:
        path = Path(dirname)
        if path.exists() and path.is_dir():
            print(f"  ✓ {dirname}/")
        else:
            print(f"  ✗ {dirname}/")
            all_ok = False
    
    return all_ok

def main():
    print("\n" + "="*60)
    print("Tech-Interactives Installation Verification")
    print("="*60 + "\n")
    
    dirs_ok = check_dirs()
    files_ok = check_files()
    packages_ok = check_packages()
    
    print("\n" + "="*60)
    
    if dirs_ok and files_ok and packages_ok:
        print("✓ Installation VERIFIED - System ready!")
        print("\nRun: python backend/main.py")
        print("Open: http://localhost:5000")
        print("="*60)
        return 0
    else:
        print("✗ Installation incomplete")
        print("="*60)
        return 1

if __name__ == '__main__':
    sys.exit(main())
