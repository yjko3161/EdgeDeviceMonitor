@echo off
if not exist .venv (
    echo [Error] Virtual environment not found. Please run setup.bat first.
    pause
    exit /b
)

echo [Run] Starting EdgeDeviceMonitor...
.venv\Scripts\python main.py
pause
