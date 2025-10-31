# GenAI Demo - Cross-Platform AI Assistant

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows-lightgrey.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A cross-platform AI demonstration project using Ollama with the Phi-3 Mini model. Features automatic server management, graceful shutdown, and platform-specific optimizations for both macOS and Windows.

## 🚀 Features

- ✅ **Cross-platform compatibility** (macOS, Windows)
- ✅ **Automatic Ollama server management**
- ✅ **Graceful startup and shutdown**
- ✅ **Self-contained AI model storage**
- ✅ **Enhanced Windows support** with colored output
- ✅ **One-click launchers** for both platforms
- ✅ **Robust error handling and cleanup**

## 📋 Quick Start

### Option 1: One-Click Launch
- **macOS/Linux**: `./run-macos.sh`
- **Windows**: Double-click `run-windows.bat`

### Option 2: Manual Setup
See detailed setup instructions below.

## Files Structure
```
GenAI-Demo/
├── app/
│   ├── demo.py              # macOS/Linux optimized version
│   └── demo-Win.py          # Windows optimized version
├── model/
│   └── ollama_models/       # Model storage directory
├── env/                     # Python virtual environment
├── requirements.txt         # Basic Python dependencies
├── requirements-windows.txt # Windows-specific dependencies
├── run-macos.sh            # One-click macOS launcher
├── run-windows.bat         # One-click Windows launcher
├── troubleshoot-windows.bat # Windows troubleshooting tool
└── README.md               # This file
```

## Prerequisites

### For macOS:
1. **Install Ollama**: Download from [https://ollama.com](https://ollama.com)
2. **Install Python 3.9+**: Use Homebrew or download from python.org
3. **Install Xcode Command Line Tools** (if not already installed):
   ```bash
   xcode-select --install
   ```

### For Windows:
1. **Install Ollama**: Download from [https://ollama.com](https://ollama.com)
2. **Install Python 3.9+**: Download from [https://python.org](https://python.org)
3. **Add Ollama to PATH**: Ensure `ollama.exe` is accessible from command line

## Setup Instructions

### macOS Setup:
```bash
# Navigate to project directory
cd GenAI-Demo

# Create virtual environment (if not exists)
python3 -m venv env

# Activate virtual environment
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Pull the AI model (will be stored in model/ollama_models/)
ollama pull phi3:mini

# Run the demo
python app/demo.py
```

### Windows Setup:
```cmd
# Navigate to project directory
cd GenAI-Demo

# Create virtual environment (if not exists)
python -m venv env

# Activate virtual environment
env\Scripts\activate

# Install dependencies (Windows-optimized)
pip install -r requirements-windows.txt

# Pull the AI model (will be stored in model/ollama_models/)
ollama pull phi3:mini

# Run the Windows-optimized demo
python app/demo-Win.py
```

## Key Differences Between Versions

### demo.py (macOS/Linux):
- Uses Unix-style process management
- Optimized signal handling for POSIX systems
- Faster startup times
- Uses `terminate()` and `kill()` for process cleanup

### demo-Win.py (Windows):
- Uses Windows-specific process creation flags
- Handles both Ctrl+C and Ctrl+Break interrupts
- Uses `taskkill` command for reliable process termination
- Longer startup timeouts to accommodate Windows behavior
- Fallback mechanisms for different Windows configurations
- **Enhanced features with Windows requirements:**
  - Colored output with `colorama` (if installed)
  - Advanced process management with `psutil` (if installed)
  - Better error handling and user feedback

## Troubleshooting

### Windows-Specific Issues:

**"Server not ready yet, waiting..." Error:**
This is common on Windows due to slower startup times. Solutions:

1. **Use the troubleshooting tool:**
   ```cmd
   troubleshoot-windows.bat
   ```

2. **Manual steps:**
   - Ensure Ollama service is running: `ollama serve`
   - Wait 15-30 seconds before running the demo
   - Try running `ollama list` to verify connection

3. **If still having issues:**
   - Restart your computer
   - Reinstall Ollama from [ollama.com](https://ollama.com)
   - Make sure Windows Defender isn't blocking Ollama

### Common Issues:

1. **"ollama command not found"**
   - **macOS**: Restart terminal after installing Ollama
   - **Windows**: Add Ollama installation directory to PATH or reinstall Ollama

2. **Model not found error**
   - Run `ollama pull phi3:mini` to download the model
   - Ensure the model directory exists: `model/ollama_models/`

3. **Connection refused error**
   - The program automatically starts Ollama server
   - If issues persist, manually run: `ollama serve`

4. **Process not shutting down (Windows)**
   - The Windows version uses `taskkill` for reliable cleanup
   - If needed, manually kill with: `taskkill /F /IM ollama.exe`

5. **Permission errors**
   - **macOS**: Use `sudo` if needed for model directory access
   - **Windows**: Run Command Prompt as Administrator

## Features

Both versions include:
- ✅ Automatic Ollama server management
- ✅ Graceful startup and shutdown
- ✅ Error handling and cleanup
- ✅ Interrupt signal handling (Ctrl+C)
- ✅ Model stored in project directory
- ✅ Self-contained operation

## Model Location

The AI model is stored in your project directory:
- **Location**: `GenAI-Demo/model/ollama_models/`
- **Size**: ~2.2 GB for phi3:mini
- **Benefit**: Portable with your project, no system-wide installation

## Usage Examples

Both programs will:
1. Check if Ollama server is running
2. Start server if needed
3. Load the phi3:mini model
4. Generate an AI response
5. Cleanly shutdown the server

You can modify the chat message in either file to customize the AI interaction.

## Windows-Specific Enhancements

The `requirements-windows.txt` includes additional packages for better Windows experience:

- **colorama**: Provides colored console output for better visual feedback
- **psutil**: Enhanced process management for more reliable cleanup
- **requests & urllib3**: Ensure compatibility with Windows networking

These packages are optional but recommended for the best Windows experience.

## Support

- **macOS/Linux**: Use `demo.py` with `requirements.txt`
- **Windows**: Use `demo-Win.py` with `requirements-windows.txt`
- Both versions maintain the same functionality with platform-specific optimizations