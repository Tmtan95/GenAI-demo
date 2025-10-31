@echo off
echo Starting GenAI Demo for Windows...
echo.

REM Check if virtual environment exists
if not exist "env\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv env
    if errorlevel 1 (
        echo Failed to create virtual environment. Please check Python installation.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call env\Scripts\activate.bat

REM Install requirements if needed
echo Checking dependencies...
if exist "requirements-windows.txt" (
    pip install -r requirements-windows.txt >nul 2>&1
) else (
    pip install -r requirements.txt >nul 2>&1
)

REM Start Ollama service if not running
echo Checking Ollama service...
ollama list >nul 2>&1
if errorlevel 1 (
    echo Starting Ollama service...
    start /b ollama serve
    echo Waiting for service to start...
    timeout /t 10 /nobreak >nul
)

REM Check if model exists
echo Checking for AI model...
ollama list | findstr "phi3:mini" >nul
if errorlevel 1 (
    echo Model not found. Downloading phi3:mini model...
    echo This may take a few minutes depending on your internet connection.
    ollama pull phi3:mini
    if errorlevel 1 (
        echo Failed to download model. Please check Ollama installation.
        echo Try running troubleshoot-windows.bat for detailed diagnostics.
        pause
        exit /b 1
    )
)

REM Run the demo
echo.
echo Running GenAI Demo...
echo.
python app\demo-Win.py

echo.
echo Demo completed. Press any key to exit.
pause >nul