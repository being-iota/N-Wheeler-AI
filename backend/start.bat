@echo off
REM Start script for backend (Windows)

echo 🚀 Starting Vehicle Maintenance AI System Backend...

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found. Please run setup first.
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file not found. Creating from .env.example...
    copy .env.example .env
    echo ⚠️  Please update .env with your configuration before continuing.
)

REM Start the server
echo ✅ Starting FastAPI server...
uvicorn main:app --reload --port 8000 --host 0.0.0.0

