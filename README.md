# GenAI Demo - AI Assistant

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-lightgrey.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

An AI chat application using Ollama with the Phi-3 Mini model. Features interactive ChatGPT-like conversations with automatic server management.

## 🚀 Features

- 💬 **Interactive Chat**: ChatGPT-like conversation with memory
- 🖥️ **macOS/Linux**: Optimized for Unix-based systems  
- 🤖 **AI-Powered**: Uses Phi-3 Mini model via Ollama
- 🎨 **Enhanced UI**: Colored output and professional interface
- � **Document Analysis**: Coming soon - PDF-based instruction generation

## 📁 Project Structure
```
GenAI-Demo/
├── app/
│   └── demo.py              # Main application with server management
├── model/                   # Model storage (local only, not in git)
├── requirements.txt         # Python dependencies
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
   ```bash
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

3. **Install AI model:**
   ```bash
   ollama pull phi3:mini
   ```

4. **Run the application:**
   ```bash
   python app/demo.py
   ```

## � Usage

The application provides:

1. **Interactive Chat** - ChatGPT-like conversation with context memory
2. **Document Analysis** - Coming soon (PDF-based instruction generation)  
3. **Clean Interface** - Professional menus and colored output
4. **Auto Management** - Automatically starts/stops Ollama server

Navigate through options using the numbered menu system.## ⚠️ Troubleshooting

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

### System-Specific
- Ensure Ollama is properly installed
- Check that port 11434 is not blocked by firewall

## 📦 Dependencies

### Core (`requirements.txt`)
- `ollama==0.6.0` - Core AI functionality and model management

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