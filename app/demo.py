import ollama
import subprocess
import time
import atexit
import signal
import sys

class OllamaManager:
    def __init__(self):
        self.ollama_process = None
        self.started_by_us = False
    
    def ensure_ollama_running(self):
        """Ensure Ollama server is running"""
        try:
            # Try to ping Ollama
            ollama.list()
            print("Ollama server is already running")
            return True
        except:
            print("Starting Ollama server...")
            # Start Ollama server in background (macOS optimized)
            self.ollama_process = subprocess.Popen(
                ['ollama', 'serve'], 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL
            )
            self.started_by_us = True
            # Wait a moment for server to start
            time.sleep(3)
            return True
    
    def shutdown_ollama(self):
        """Shutdown Ollama server if we started it"""
        if self.started_by_us and self.ollama_process:
            print("Shutting down Ollama server...")
            try:
                self.ollama_process.terminate()
                # Give it a moment to shutdown gracefully
                self.ollama_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Force kill if it doesn't shutdown gracefully
                self.ollama_process.kill()
                self.ollama_process.wait()
            except:
                pass
            finally:
                self.ollama_process = None
                self.started_by_us = False

# Create Ollama manager instance
ollama_manager = OllamaManager()

# Register cleanup function to run on exit
atexit.register(ollama_manager.shutdown_ollama)

# Handle Ctrl+C gracefully
def signal_handler(sig, frame):
    print("\nReceived interrupt signal, cleaning up...")
    ollama_manager.shutdown_ollama()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

try:
    # Ensure Ollama is running before making requests
    ollama_manager.ensure_ollama_running()

    response = ollama.chat(model='phi3:mini', messages=[
      {'role':'user','content':'give me a short poem about AI'}
    ])
    print(response['message']['content'])

finally:
    # Ensure cleanup happens even if there's an exception
    ollama_manager.shutdown_ollama()
