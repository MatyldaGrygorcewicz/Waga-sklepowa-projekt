@echo off
echo ========================================
echo   Waga Sklepowa AI - Starting...
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Install dependencies if needed
echo Checking dependencies...
pip install -q -r backend\requirements.txt
echo Dependencies OK
echo.

REM Start backend in a new window
echo Starting Backend Server...
start "Waga Sklepowa - Backend" cmd /k "cd backend && python app.py"
timeout /t 3 /nobreak >nul
echo.

REM Start frontend server
echo Starting Frontend Server...
start "Waga Sklepowa - Frontend" cmd /k "cd frontend && python -m http.server 8000"
timeout /t 2 /nobreak >nul
echo.

REM Open browser
echo Opening browser...
timeout /t 3 /nobreak >nul
start http://localhost:8000
echo.

echo ========================================
echo   Application started successfully!
echo ========================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:8000
echo.
echo Press any key to exit this window...
echo (Backend and Frontend will keep running)
pause >nul
