# GenAI Demo - Test Suite

This folder contains unit tests for the GenAI Demo application, specifically focused on testing Ollama server connection and model functionality.

## 📁 Test Files

- **`test_ollama.py`** - Main test suite for Ollama functionality
- **`run_tests.py`** - Test runner script with various options
- **`__init__.py`** - Package initialization

## 🧪 Test Categories

### 1. **TestOllamaConnection**
Tests the OllamaManager class functionality:
- ✅ Manager initialization
- ✅ Server connection detection  
- ✅ Server startup/shutdown
- ✅ Error handling for startup failures
- ✅ Process management

### 2. **TestOllamaModel** 
Tests Ollama model interactions (mocked):
- ✅ Model listing
- ✅ Chat functionality  
- ✅ Error handling
- ✅ Conversation memory

### 3. **TestRealOllamaConnection**
Integration tests with real Ollama server:
- ✅ Real server connection
- ✅ gemma3:270m model availability
- ✅ Actual chat interactions
- ⚠️ Skipped if server unavailable

## 🚀 Running Tests

### Basic Usage
```bash
# Run all tests
python tests/run_tests.py

# Run with verbose output
python tests/run_tests.py -v

# Run only mocked tests (no real server needed)
python tests/run_tests.py --mock-only
```

### Using unittest directly
```bash
# Run all tests in the module
python -m unittest tests.test_ollama -v

# Run specific test class
python -m unittest tests.test_ollama.TestOllamaConnection -v

# Run specific test method
python -m unittest tests.test_ollama.TestOllamaConnection.test_ollama_manager_initialization -v
```

## 📊 Test Results

The tests use mocking to isolate functionality and avoid interfering with running Ollama services. 

**Expected Results:**
- ✅ **11 mocked tests** - Should always pass
- ⏭️ **3 real server tests** - May skip if Ollama server not running
- 🎯 **Total: 14 tests**

## 🔧 Test Features

### **Mocking**
- Uses `unittest.mock` to simulate Ollama responses
- No dependency on actual Ollama server for core tests
- Safe to run without disrupting running services

### **Real Server Detection**
- Automatically detects if real Ollama server is available
- Gracefully skips integration tests if server unavailable
- Provides helpful skip messages

### **Error Testing**
- Tests connection failures
- Tests startup failures  
- Tests graceful error handling

### **Process Management**
- Tests proper resource cleanup
- Tests graceful vs force shutdown
- Tests external vs managed processes

## 🛠️ Troubleshooting

### Tests Failing
```bash
# Check if ollama library is installed
pip install ollama

# Verify Python path
python -c "import sys; print(sys.path)"

# Run with maximum verbosity
python tests/run_tests.py -v
```

### Real Server Tests Skipping
This is normal! The real server tests are designed to skip when:
- Ollama server is not running
- Connection fails
- gemma3:270m model not available

### Import Errors
Make sure you're running from the project root directory:
```bash
cd /path/to/GenAI-Demo
python tests/run_tests.py
```

## 🎯 Test Coverage

The test suite covers:
- ✅ **OllamaManager class** - All public methods
- ✅ **Connection handling** - Success and failure cases
- ✅ **Process management** - Startup, shutdown, cleanup
- ✅ **Model interactions** - List, chat, error handling
- ✅ **Error scenarios** - Network, startup, model failures
- ✅ **Resource management** - Proper cleanup and isolation

## 📝 Adding New Tests

To add new tests:

1. **Add to existing class:**
```python
def test_new_functionality(self):
    """Test description"""
    # Test code here
    self.assertTrue(result)
```

2. **Create new test class:**
```python
class TestNewFeature(unittest.TestCase):
    def test_feature(self):
        # Test code here
        pass
```

3. **Use appropriate decorators:**
```python
@unittest.skipUnless(OLLAMA_AVAILABLE, "Ollama not available")
@patch('app.demo.ollama.chat')
def test_with_mocking(self, mock_chat):
    # Test code here
```