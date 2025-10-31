@echo off
echo Windows GenAI Demo Troubleshooting
echo ===================================
echo.

echo 1. Checking if Ollama is installed...
where ollama >nul 2>&1
if errorlevel 1 (
    echo ❌ Ollama not found in PATH
    echo Please install Ollama from https://ollama.com
    echo And make sure it's added to your PATH
    pause
    exit /b 1
) else (
    echo ✅ Ollama found
)

echo.
echo 2. Checking if Python virtual environment exists...
if exist "env\Scripts\python.exe" (
    echo ✅ Virtual environment found
) else (
    echo ❌ Virtual environment not found
    echo Creating virtual environment...
    python -m venv env
    if errorlevel 1 (
        echo Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
)

echo.
echo 3. Installing/checking requirements...
call env\Scripts\activate.bat
pip install -r requirements-windows.txt

echo.
echo 4. Testing Ollama connection...
ollama list
if errorlevel 1 (
    echo ❌ Ollama service might not be running
    echo Starting Ollama service...
    start /b ollama serve
    echo Waiting 15 seconds for service to start...
    timeout /t 15 /nobreak > nul
)

echo.
echo 5. Checking for phi3:mini model...
ollama list | findstr "phi3:mini" >nul
if errorlevel 1 (
    echo ⚠ Model not found. Downloading phi3:mini...
    echo This may take several minutes...
    ollama pull phi3:mini
    if errorlevel 1 (
        echo ❌ Failed to download model
        pause
        exit /b 1
    )
)

echo.
echo ✅ All checks passed! Running GenAI Demo...
echo ==========================================
python app\demo-Win.py

echo.
echo Program finished. Press any key to exit.
pause >nul