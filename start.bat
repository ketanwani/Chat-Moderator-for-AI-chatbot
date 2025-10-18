@echo off
echo ========================================
echo Real-Time Moderation Engine
echo ========================================
echo.

echo Checking Python...
python --version
if errorlevel 1 (
    echo Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Checking Node.js...
node --version
if errorlevel 1 (
    echo Node.js is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Starting Backend...
cd backend
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate
pip install -r requirements.txt

if not exist .env (
    echo Creating .env file...
    copy .env.example .env
)

echo Initializing database...
python init_db.py

echo Starting FastAPI server...
start cmd /k "cd /d %cd% && venv\Scripts\activate && uvicorn main:app --reload"

cd ..

echo.
echo Starting Frontend...
cd frontend
if not exist node_modules (
    echo Installing npm dependencies...
    npm install
)

echo Starting React development server...
start cmd /k "cd /d %cd% && npm start"

cd ..

echo.
echo ========================================
echo Application started!
echo ========================================
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo ========================================
echo.
echo Press any key to exit this window...
pause > nul
