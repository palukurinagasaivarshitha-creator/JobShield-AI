@echo off
setlocal EnableDelayedExpansion

echo ==============================================================================
echo Fake Job Detection ^& Verification Platform - Automated Windows Setup
echo ==============================================================================
echo.

:: 1. Check Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python 3 is not found in your PATH.
    echo Please install Python 3.10+ from https://www.python.org/
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do echo [INFO] Found %%i

:: 2. Check Node.js and NPM
node -v >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js is not found in your PATH.
    echo Please install Node.js 18+ from https://nodejs.org/
    exit /b 1
)
for /f "tokens=*" %%i in ('node -v') do echo [INFO] Found Node.js %%i
for /f "tokens=*" %%i in ('npm -v') do echo [INFO] Found NPM %%i

:: 3. Python Virtual Environment Setup
cd /d "%~dp0\..\backend"
if not exist "venv" (
    echo [INFO] Creating Python virtual environment in backend\venv...
    python -m venv venv
)

if exist "venv\Scripts\activate.bat" (
    echo [INFO] Activating virtual environment...
    call venv\Scripts\activate.bat
)

echo [INFO] Installing backend dependencies from requirements.txt...
pip install -r requirements.txt

:: 4. Train Initial Machine Learning Model
echo [INFO] Initializing and training EMSCAD Machine Learning model...
python -m app.ml.train

:: 5. Install Frontend Dependencies
cd /d "%~dp0\..\frontend"
echo [INFO] Installing frontend dependencies with npm...
call npm install

echo.
echo ==============================================================================
echo [SUCCESS] Setup completed successfully!
echo To run the platform, double-click scripts\run.bat or execute:
echo   cd scripts ^&^& run.bat
echo ==============================================================================
cd /d "%~dp0\.."
pause
