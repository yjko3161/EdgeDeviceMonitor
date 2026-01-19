@echo off
echo [Setup] Creating virtual environment (.venv)...
python -m venv .venv

echo [Setup] Activating .venv and installing dependencies...
call .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

echo [Setup] Done. You can now run the application using run.bat
pause
