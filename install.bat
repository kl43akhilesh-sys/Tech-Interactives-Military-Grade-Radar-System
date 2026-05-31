@echo off
setlocal enabledelayedexpansion

echo.
echo ==========================================
echo Tech-Interactives Installation
echo Military Grade Radar System
echo ==========================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.14+
    pause
    exit /b 1
)

echo [INSTALL] Creating virtual environment...
if exist venv (
    echo [INSTALL] Virtual environment exists
) else (
    python -m venv venv
)

echo [INSTALL] Activating virtual environment...
call venv\Scripts\activate.bat

echo [INSTALL] Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1

echo [INSTALL] Installing dependencies...
pip install -r requirements.txt

echo [INSTALL] Creating directories...
if not exist logs mkdir logs
if not exist data mkdir data
if not exist data\logs mkdir data\logs
if not exist config mkdir config
if not exist models mkdir models

echo [INSTALL] Verifying installation...
python verify_installation.py

echo.
echo ==========================================
echo Installation Complete!
echo ==========================================
echo.
echo Run: .\start_all.bat
echo
pause
