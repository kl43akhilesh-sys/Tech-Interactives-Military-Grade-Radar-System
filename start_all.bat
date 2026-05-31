@echo off

echo.
echo ==========================================
echo Tech-Interactives System Startup
echo ==========================================
echo.

call venv\Scripts\activate.bat

echo [STARTUP] Starting Tech-Interactives Backend...
echo [FRONTEND] Dashboard: http://localhost:5000
echo [WEBSOCKET] Real-time: ws://localhost:5001
echo.
echo Press Ctrl+C to stop
echo.

python backend/main.py

pause
