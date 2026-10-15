@echo off
setlocal

echo ==============================================================================
echo Fake Job Detection ^& Verification Platform - Launcher
echo ==============================================================================
echo.
echo Starting FastAPI Backend on http://localhost:8000 ...
echo Starting React Vite Frontend on http://localhost:5173 ...
echo.

:: Launch Backend in a separate window
start "FakeJobDetection - Backend (FastAPI)" cmd /k "cd /d "%~dp0\..\backend" && if exist venv\Scripts\activate.bat (call venv\Scripts\activate.bat) && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

:: Launch Frontend in a separate window
start "FakeJobDetection - Frontend (Vite)" cmd /k "cd /d "%~dp0\..\frontend" && npm run dev"

echo Backend API:  http://localhost:8000
echo API Docs:     http://localhost:8000/docs
echo Frontend App: http://localhost:5173
echo.
echo Both services are now running in separate terminal windows.
echo Press any key to exit this launcher window.
pause >nul
