import ollama
import subprocess
import time
import atexit
import signal
import sys
import os

# Windows-specific imports with fallbacks
try:
    import colorama # type: ignore
    from colorama import Fore, Style, init # pyright: ignore[reportMissingModuleSource]
    init(autoreset=True)  # Auto-reset colors after each print
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    # Define dummy color constants if colorama isn't available
    class Fore:
        GREEN = ""
        YELLOW = ""
        RED = ""
        CYAN = ""
    class Style:
        RESET_ALL = ""

try:
    import psutil # type: ignore
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

class OllamaManagerWindows:
    def __init__(self):
        self.ollama_process = None
        self.started_by_us = False
    
    def ensure_ollama_running(self):
        """Ensure Ollama server is running (Windows optimized)"""
        try:
            # Try to ping Ollama
            ollama.list()
            if COLORS_AVAILABLE:
                print(f"{Fore.GREEN}Ollama server is already running{Style.RESET_ALL}")
            else:
                print("Ollama server is already running")
            return True
        except:
            if COLORS_AVAILABLE:
                print(f"{Fore.YELLOW}Starting Ollama server...{Style.RESET_ALL}")
            else:
                print("Starting Ollama server...")
            # Start Ollama server in background (Windows optimized)
            try:
                # Use CREATE_NEW_PROCESS_GROUP to avoid console signal propagation issues
                self.ollama_process = subprocess.Popen(
                    ['ollama.exe', 'serve'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                )
            except FileNotFoundError:
                # Fallback if ollama.exe is not found, try without .exe
                self.ollama_process = subprocess.Popen(
                    ['ollama', 'serve'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                )
            
            self.started_by_us = True
            # Longer wait for Windows (can be slower to start)
            if COLORS_AVAILABLE:
                print(f"{Fore.CYAN}Waiting for Ollama server to start...{Style.RESET_ALL}")
            else:
                print("Waiting for Ollama server to start...")
            time.sleep(7)
            
            # Verify server actually started
            max_retries = 5
            for i in range(max_retries):
                try:
                    ollama.list()
                    if COLORS_AVAILABLE:
                        print(f"{Fore.GREEN}Ollama server started successfully!{Style.RESET_ALL}")
                    else:
                        print("Ollama server started successfully!")
                    return True
                except:
                    if i < max_retries - 1:
                        print(f"Server not ready yet, waiting... ({i+1}/{max_retries})")
                        time.sleep(2)
                    else:
                        print("Warning: Server may not have started properly")
                        return True
    
    def shutdown_ollama(self):
        """Shutdown Ollama server if we started it (Windows optimized)"""
        if self.started_by_us and self.ollama_process:
            if COLORS_AVAILABLE:
                print(f"{Fore.YELLOW}Shutting down Ollama server...{Style.RESET_ALL}")
            else:
                print("Shutting down Ollama server...")
            try:
                # Enhanced process management with psutil if available
                if PSUTIL_AVAILABLE:
                    try:
                        # Use psutil for more reliable process management
                        parent = psutil.Process(self.ollama_process.pid)
                        children = parent.children(recursive=True)
                        
                        # Terminate children first
                        for child in children:
                            child.terminate()
                        
                        # Terminate parent
                        parent.terminate()
                        
                        # Wait for processes to terminate
                        psutil.wait_procs([parent] + children, timeout=5)
                        
                        if COLORS_AVAILABLE:
                            print(f"{Fore.GREEN}Ollama server terminated successfully (psutil){Style.RESET_ALL}")
                        else:
                            print("Ollama server terminated successfully (psutil)")
                        return
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                        # Fall through to taskkill method
                        pass
                
                # Method 1: Use taskkill for reliable Windows process termination
                try:
                    result = subprocess.run(
                        ['taskkill', '/F', '/T', '/PID', str(self.ollama_process.pid)],
                        check=False,
                        capture_output=True,
                        timeout=10
                    )
                    if result.returncode == 0:
                        if COLORS_AVAILABLE:
                            print(f"{Fore.GREEN}Ollama server terminated successfully{Style.RESET_ALL}")
                        else:
                            print("Ollama server terminated successfully")
                    else:
                        # Fallback to Python's terminate
                        self.ollama_process.terminate()
                        time.sleep(2)
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    # Method 2: Fallback to standard termination
                    self.ollama_process.terminate()
                    time.sleep(3)
                
                # Wait for process to actually end
                try:
                    self.ollama_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    print("Process took longer than expected to shutdown")
                
            except Exception as e:
                print(f"Note: Cleanup completed with minor issues: {type(e).__name__}")
            finally:
                self.ollama_process = None
                self.started_by_us = False
                if COLORS_AVAILABLE:
                    print(f"{Fore.GREEN}Ollama server shutdown complete{Style.RESET_ALL}")
                else:
                    print("Ollama server shutdown complete")

# Create Ollama manager instance
ollama_manager = OllamaManagerWindows()

# Register cleanup function to run on exit
atexit.register(ollama_manager.shutdown_ollama)

# Handle Ctrl+C and Ctrl+Break gracefully (Windows optimized)
def signal_handler(sig, frame):
    print("\nReceived interrupt signal, cleaning up...")
    ollama_manager.shutdown_ollama()
    sys.exit(0)

# Register Windows-compatible signal handlers
signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
if hasattr(signal, 'SIGBREAK'):
    signal.signal(signal.SIGBREAK, signal_handler)  # Ctrl+Break (Windows)

try:
    # Ensure Ollama is running before making requests
    ollama_manager.ensure_ollama_running()

    response = ollama.chat(model='phi3:mini', messages=[
      {'role':'user','content':'give me a short poem about AI'}
    ])
    print(response['message']['content'])

except KeyboardInterrupt:
    print("\nProgram interrupted by user")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Ensure cleanup happens even if there's an exception
    ollama_manager.shutdown_ollama()