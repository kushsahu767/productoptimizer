@echo off
REM Product Price Optimiser - One-Click Startup Script

echo.
echo ================================================
echo   Product Price Optimiser - Unified Server
echo ================================================
echo.

cd /d "%~dp0"

echo [*] Starting unified server on http://localhost:3000
echo [*] Press Ctrl+C to stop the server
echo.

timeout /t 2 > nul

REM Start the Python server
python server.py

pause
