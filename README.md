# GenAI Demo - Cross-Platform AI Assistant

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows-lightgrey.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A cross-platform AI chat application using Ollama with the Phi-3 Mini model. Features interactive ChatGPT-like conversations with platform-specific optimizations.

## 🚀 Features

- 💬 **Interactive Chat**: ChatGPT-like conversation with memory
- 🖥️ **Cross-platform**: Optimized for both macOS and Windows  
- 🤖 **AI-Powered**: Uses Phi-3 Mini model via Ollama
- 🎨 **Enhanced UI**: Colored output and professional interface
- � **Document Analysis**: Coming soon - PDF-based instruction generation

## 📁 Project Structure
```
GenAI-Demo/
├── app/
│   ├── demo.py              # macOS/Linux version (with server management)
│   └── demo-Win.py          # Windows version (uses system Ollama)
├── model/                   # Model storage (local only, not in git)
├── requirements.txt         # Python dependencies
├── requirements-windows.txt # Windows-enhanced dependencies  
└── README.md               # This file
```

## 🔧 Setup

### Prerequisites
- **Python 3.9+** 
- **Ollama** - Download from [ollama.com](https://ollama.com)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tmtan95/GenAI-Demo.git
   cd GenAI-Demo
   ```

2. **Set up Python environment:**
   
   **macOS/Linux:**
   ```bash
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```
   
   **Windows:**
   ```cmd
   python -m venv env
   env\Scripts\activate
   pip install -r requirements-windows.txt
   ```

3. **Install AI model:**
   ```bash
   ollama pull phi3:mini
   ```

4. **Run the application:**
   
   **macOS/Linux:**
   ```bash
   python app/demo.py
   ```
   
   **Windows:**
   ```cmd
   python app/demo-Win.py
   ```

## 🖥️ Platform Differences

### macOS/Linux (`demo.py`)
- **Server Management**: Automatically starts/stops Ollama server
- **Model Storage**: `GenAI-Demo/model/ollama_models/`
- **Process Control**: Full lifecycle management

### Windows (`demo-Win.py`)  
- **System Integration**: Uses system Ollama service
- **Model Storage**: `C:/Users/.ollama/models/`
- **Simplified Design**: No server management needed

## 🔍 Usage

Both versions provide the same features:

1. **Interactive Chat** - ChatGPT-like conversation with context memory
2. **Document Analysis** - Coming soon (PDF-based instruction generation)  
3. **Clean Interface** - Professional menus and colored output

Navigate through options using the numbered menu system.

## ⚠️ Troubleshooting

### Model Issues
```bash
# Check if model exists
ollama list

# Download model if missing  
ollama pull phi3:mini
```

### Connection Issues
```bash
# Ensure Ollama is running
ollama serve

# Test connection
ollama list
```

### Windows-Specific
- Make sure Ollama is added to PATH
- Try running as Administrator if needed
- Restart Ollama service if connection fails

## 📦 Dependencies

### Basic (`requirements.txt`)
- `ollama==0.6.0` - Core AI functionality

### Windows Enhanced (`requirements-windows.txt`)  
- `ollama==0.6.0` - Core AI functionality
- `colorama==0.4.6` - Colored console output
- `psutil==5.9.6` - Enhanced process management  
- `requests==2.31.0` - HTTP reliability
- `urllib3==2.0.7` - Network compatibility

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🔮 Roadmap

- [x] Interactive ChatGPT-like interface
- [x] Cross-platform compatibility  
- [x] Colored console output
- [ ] PDF document analysis and instruction generation
- [ ] Multiple AI model support
- [ ] Web interface option