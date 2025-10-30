#!/bin/bash

echo "Starting GenAI Demo for macOS..."
echo

# Check if virtual environment exists
if [ ! -f "env/bin/activate" ]; then
    echo "Creating virtual environment..."
    python3 -m venv env
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Please check Python installation."
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source env/bin/activate

# Install requirements if needed
echo "Checking dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

# Check if model exists
echo "Checking for AI model..."
if ! ollama list | grep -q "phi3:mini"; then
    echo "Model not found. Downloading phi3:mini model..."
    echo "This may take a few minutes depending on your internet connection."
    ollama pull phi3:mini
    if [ $? -ne 0 ]; then
        echo "Failed to download model. Please check Ollama installation."
        exit 1
    fi
fi

# Run the demo
echo
echo "Running GenAI Demo..."
echo
python app/demo.py

echo
echo "Demo completed."