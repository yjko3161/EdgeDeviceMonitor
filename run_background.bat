@echo off
cd /d "%~dp0"
call .venv\Scripts\activate

echo Starting Edge Device Monitor in background...
start /B pythonw main.py

echo.
echo ========================================================
echo  Monitor is running in the background!
echo  You can safely close this terminal window.
echo  The logging will continue.
echo.
echo  To stop the monitor, run: stop_monitor.bat
echo ========================================================
echo.
pause
