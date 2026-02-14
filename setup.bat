@echo off
echo ========================================
echo Resume Parser AI - Setup Script
echo ========================================
echo.

echo Setting up Backend...
cd backend
echo Creating virtual environment...
python -m venv .venv
echo Activating virtual environment...
call .venv\Scripts\activate
echo Installing Python dependencies...
pip install -r requirements.txt
echo.
echo Backend setup complete!
echo.
echo Please configure your Gemma AI API key in backend/config.env
echo.
echo Starting Backend...
start "Backend" cmd /k "cd backend && .venv\Scripts\activate && python app.py"
echo.
echo Backend started in new window!
echo.

echo Setting up Frontend...
cd ..\frontend
echo Installing Node.js dependencies...
npm install
echo.
echo Frontend setup complete!
echo.
echo Starting Frontend...
start "Frontend" cmd /k "cd frontend && npm start"
echo.
echo Frontend started in new window!
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Don't forget to:
echo 1. Configure your Gemma AI API key in backend/config.env
echo 2. Wait for both services to fully start
echo 3. Open http://localhost:3000 in your browser
echo.
pause
