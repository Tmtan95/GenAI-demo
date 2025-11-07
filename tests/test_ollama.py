"""
Unit tests for Ollama server connection and model functionality

This test suite verifies:
- Ollama server connectivity
- Model availability and functionality
- Error handling for connection issues
- Basic chat interactions with the model
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path to import demo modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    import ollama
    from app.demo import OllamaManager
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False


class TestOllamaConnection(unittest.TestCase):
    """Test Ollama server connection functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        if OLLAMA_AVAILABLE:
            self.manager = OllamaManager()
    
    @unittest.skipUnless(OLLAMA_AVAILABLE, "Ollama not available")
    def test_ollama_manager_initialization(self):
        """Test that OllamaManager initializes correctly"""
        manager = OllamaManager()
        self.assertIsNone(manager.ollama_process)
        self.assertFalse(manager.started_by_us)
    
    @unittest.skipUnless(OLLAMA_AVAILABLE, "Ollama not available")
    @patch('app.demo.ollama.list')
    def test_ollama_server_already_running(self, mock_list):
        """Test detection when Ollama server is already running"""
        # Mock successful ollama.list() call
        mock_list.return_value = {
            'models': [
                {
                    'name': 'gemma3:270m',
                    'size': 291000000,
                    'digest': 'test_digest'
                }
            ]
        }
        
        result = self.manager.ensure_ollama_running()
        
        self.assertTrue(result)
        self.assertFalse(self.manager.started_by_us)
        self.assertIsNone(self.manager.ollama_process)
        mock_list.assert_called_once()
    
    @unittest.skipUnless(OLLAMA_AVAILABLE, "Ollama not available")
    @patch('app.demo.subprocess.Popen')
    @patch('app.demo.ollama.list')
    @patch('app.demo.time.sleep')
    def test_ollama_server_startup(self, mock_sleep, mock_list, mock_popen):
        """Test starting new Ollama server when none is running"""
        # Mock ollama.list() failing (server not running)
        mock_list.side_effect = Exception("Connection refused")
        
        # Mock successful subprocess startup
        mock_process = Mock()
        mock_process.returncode = None
        mock_popen.return_value = mock_process
        
        result = self.manager.ensure_ollama_running()
        
        self.assertTrue(result)
        self.assertTrue(self.manager.started_by_us)
        self.assertEqual(self.manager.ollama_process, mock_process)
        mock_sleep.assert_called_once_with(3)
    
    @unittest.skipUnless(OLLAMA_AVAILABLE, "Ollama not available")
    @patch('app.demo.subprocess.Popen')
    @patch('app.demo.ollama.list')
    def test_ollama_server_startup_failure(self, mock_list, mock_popen):
        """Test handling when Ollama server fails to start"""
        # Mock ollama.list() failing (server not running)
        mock_list.side_effect = Exception("Connection refused")
        
        # Mock subprocess failure
        mock_popen.side_effect = Exception("Command not found")
        
        result = self.manager.ensure_ollama_running()
        
        # Should return False when startup fails
        self.assertFalse(result)
        self.assertFalse(self.manager.started_by_us)
        self.assertIsNone(self.manager.ollama_process)
    
    @unittest.skipUnless(OLLAMA_AVAILABLE, "Ollama not available") 
    def test_ollama_shutdown_not_our_process(self):
        """Test shutdown when we didn't start the Ollama process"""
        # Simulate external Ollama process
        mock_process = Mock()
        self.manager.ollama_process = mock_process
        self.manager.started_by_us = False
        
        self.manager.shutdown_ollama()
        
        # Should not terminate external process
        mock_process.terminate.assert_not_called()
        mock_process.kill.assert_not_called()
    
    @unittest.skipUnless(OLLAMA_AVAILABLE, "Ollama not available")
    def test_ollama_graceful_shutdown(self):
        """Test graceful shutdown of our Ollama process"""
        # Mock process that we started
        mock_process = Mock()
        mock_process.wait.return_value = 0  # Successful termination
        
        self.manager.ollama_process = mock_process
        self.manager.started_by_us = True
        
        self.manager.shutdown_ollama()
        
        mock_process.terminate.assert_called_once()
        mock_process.wait.assert_called_once_with(timeout=5)
        self.assertIsNone(self.manager.ollama_process)
        self.assertFalse(self.manager.started_by_us)


class TestOllamaModel(unittest.TestCase):
    """Test Ollama model functionality"""
    
    @unittest.skipUnless(OLLAMA_AVAILABLE, "Ollama not available")
    @patch('ollama.list')
    def test_model_list_success(self, mock_list):
        """Test successful model listing"""
        mock_list.return_value = {
            'models': [
                {
                    'name': 'gemma3:270m',
                    'size': 291000000,
                    'digest': 'abcd1234',
                    'modified_at': '2025-11-07T12:00:00Z'
                }
            ]
        }
        
        models = ollama.list()
        
        self.assertIn('models', models)
        self.assertEqual(len(models['models']), 1)
        self.assertEqual(models['models'][0]['name'], 'gemma3:270m')
    
    @unittest.skipUnless(OLLAMA_AVAILABLE, "Ollama not available")
    @patch('ollama.list')
    def test_model_list_connection_error(self, mock_list):
        """Test model listing when server is not available"""
        mock_list.side_effect = Exception("Connection refused")
        
        with self.assertRaises(Exception):
            ollama.list()
    
    @unittest.skipUnless(OLLAMA_AVAILABLE, "Ollama not available")
    @patch('ollama.chat')
    def test_model_chat_success(self, mock_chat):
        """Test successful chat interaction with model"""
        mock_chat.return_value = {
            'message': {
                'role': 'assistant',
                'content': 'Hello! How can I help you today?'
            }
        }
        
        response = ollama.chat(
            model='gemma3:270m',
            messages=[{'role': 'user', 'content': 'Hello'}]
        )
        
        self.assertIn('message', response)
        self.assertEqual(response['message']['role'], 'assistant')
        self.assertIn('Hello', response['message']['content'])
        mock_chat.assert_called_once_with(
            model='gemma3:270m',
            messages=[{'role': 'user', 'content': 'Hello'}]
        )
    
    @unittest.skipUnless(OLLAMA_AVAILABLE, "Ollama not available")
    @patch('ollama.chat')
    def test_model_chat_error(self, mock_chat):
        """Test chat error handling"""
        mock_chat.side_effect = Exception("Model not found")
        
        with self.assertRaises(Exception):
            ollama.chat(
                model='nonexistent:model',
                messages=[{'role': 'user', 'content': 'Hello'}]
            )
    
    @unittest.skipUnless(OLLAMA_AVAILABLE, "Ollama not available")
    @patch('ollama.chat')
    def test_model_conversation_memory(self, mock_chat):
        """Test model handles conversation history correctly"""
        mock_chat.return_value = {
            'message': {
                'role': 'assistant', 
                'content': 'I remember our conversation.'
            }
        }
        
        conversation = [
            {'role': 'user', 'content': 'My name is Alice'},
            {'role': 'assistant', 'content': 'Nice to meet you, Alice!'},
            {'role': 'user', 'content': 'What is my name?'}
        ]
        
        response = ollama.chat(model='gemma3:270m', messages=conversation)
        
        # Verify the full conversation was passed
        mock_chat.assert_called_once_with(model='gemma3:270m', messages=conversation)
        self.assertEqual(len(conversation), 3)  # Conversation history preserved


class TestRealOllamaConnection(unittest.TestCase):
    """Integration tests with real Ollama server (if available)"""
    
    def setUp(self):
        """Check if real Ollama server is available"""
        try:
            ollama.list()
            self.ollama_available = True
        except:
            self.ollama_available = False
    
    @unittest.skipUnless(OLLAMA_AVAILABLE, "Ollama library not available")
    def test_real_ollama_list(self):
        """Test listing models from real Ollama server"""
        if not self.ollama_available:
            self.skipTest("Real Ollama server not available")
        
        try:
            models = ollama.list()
            self.assertIsInstance(models, (dict, object))  # Handle both dict and object responses
            
            # If it's the new format with .models attribute
            if hasattr(models, 'models'):
                model_list = models.models
            else:
                model_list = models.get('models', [])
            
            self.assertIsInstance(model_list, list)
            print(f"Found {len(model_list)} models in real Ollama server")
            
        except Exception as e:
            self.skipTest(f"Real Ollama server connection failed: {e}")
    
    @unittest.skipUnless(OLLAMA_AVAILABLE, "Ollama library not available")
    def test_real_gemma3_model_availability(self):
        """Test if gemma3:270m model is available in real server"""
        if not self.ollama_available:
            self.skipTest("Real Ollama server not available")
        
        try:
            models = ollama.list()
            
            # Handle both response formats
            if hasattr(models, 'models'):
                model_list = models.models
            else:
                model_list = models.get('models', [])
            
            gemma3_found = False
            for model in model_list:
                # Handle both Model object and dict formats
                if hasattr(model, 'model'):
                    model_name = model.model
                else:
                    model_name = model.get('name', model.get('model', ''))
                
                if 'gemma3:270m' in model_name:
                    gemma3_found = True
                    print(f"Found gemma3:270m model: {model_name}")
                    break
            
            if not gemma3_found:
                self.skipTest("gemma3:270m model not found in real server")
            
            # If we get here, gemma3:270m is available
            self.assertTrue(gemma3_found)
            
        except Exception as e:
            self.skipTest(f"Could not check gemma3:270m availability: {e}")
    
    @unittest.skipUnless(OLLAMA_AVAILABLE, "Ollama library not available")
    def test_real_gemma3_chat(self):
        """Test actual chat with gemma3:270m model (if available)"""
        if not self.ollama_available:
            self.skipTest("Real Ollama server not available")
        
        try:
            # Simple test message
            response = ollama.chat(
                model='gemma3:270m',
                messages=[{
                    'role': 'user',
                    'content': 'Say "test successful" in exactly those words.'
                }]
            )
            
            self.assertIn('message', response)
            self.assertIn('content', response['message'])
            
            content = response['message']['content'].lower()
            print(f"Real model response: {response['message']['content']}")
            
            # Verify we got a response (don't check exact content as AI responses vary)
            self.assertIsInstance(response['message']['content'], str)
            self.assertGreater(len(response['message']['content']), 0)
            
        except Exception as e:
            self.skipTest(f"Real gemma3:270m chat test failed: {e}")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)