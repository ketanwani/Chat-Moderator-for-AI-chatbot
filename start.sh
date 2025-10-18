#!/bin/bash

echo "========================================"
echo "Real-Time Moderation Engine"
echo "========================================"
echo ""

# Check Python
echo "Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed or not in PATH"
    exit 1
fi
python3 --version

# Check Node.js
echo ""
echo "Checking Node.js..."
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed or not in PATH"
    exit 1
fi
node --version

# Backend setup
echo ""
echo "Starting Backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

echo "Initializing database..."
python init_db.py

echo "Starting FastAPI server..."
gnome-terminal -- bash -c "cd $(pwd) && source venv/bin/activate && uvicorn main:app --reload; exec bash" 2>/dev/null || \
xterm -e "cd $(pwd) && source venv/bin/activate && uvicorn main:app --reload" 2>/dev/null || \
osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"' && source venv/bin/activate && uvicorn main:app --reload"' 2>/dev/null || \
(uvicorn main:app --reload &)

cd ..

# Frontend setup
echo ""
echo "Starting Frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
fi

echo "Starting React development server..."
gnome-terminal -- bash -c "cd $(pwd) && npm start; exec bash" 2>/dev/null || \
xterm -e "cd $(pwd) && npm start" 2>/dev/null || \
osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"' && npm start"' 2>/dev/null || \
(npm start &)

cd ..

echo ""
echo "========================================"
echo "Application started!"
echo "========================================"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop"

wait
