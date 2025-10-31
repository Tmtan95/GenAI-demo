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
            
            # Enhanced Windows startup with longer waits and better feedback
            if COLORS_AVAILABLE:
                print(f"{Fore.CYAN}Starting Ollama server on Windows...{Style.RESET_ALL}")
            else:
                print("Starting Ollama server on Windows...")
                
            # Initial longer wait for Windows
            if COLORS_AVAILABLE:
                print(f"{Fore.CYAN}Initial startup wait (10 seconds)...{Style.RESET_ALL}")
            else:
                print("Initial startup wait (10 seconds)...")
            time.sleep(10)
            
            # Verify server with more retries and longer delays
            max_retries = 8
            wait_time = 3
            
            for i in range(max_retries):
                try:
                    # Try to connect to Ollama
                    ollama.list()
                    if COLORS_AVAILABLE:
                        print(f"{Fore.GREEN}✓ Ollama server started successfully!{Style.RESET_ALL}")
                    else:
                        print("✓ Ollama server started successfully!")
                    return True
                except Exception as e:
                    if i < max_retries - 1:
                        if COLORS_AVAILABLE:
                            print(f"{Fore.YELLOW}Server not ready yet, waiting... ({i+1}/{max_retries}) - {wait_time}s{Style.RESET_ALL}")
                        else:
                            print(f"Server not ready yet, waiting... ({i+1}/{max_retries}) - {wait_time}s")
                        time.sleep(wait_time)
                        # Increase wait time progressively
                        wait_time = min(wait_time + 1, 6)
                    else:
                        if COLORS_AVAILABLE:
                            print(f"{Fore.YELLOW}⚠ Server startup taking longer than expected.{Style.RESET_ALL}")
                            print(f"{Fore.CYAN}Attempting to continue - the server might still be starting...{Style.RESET_ALL}")
                        else:
                            print("⚠ Server startup taking longer than expected.")
                            print("Attempting to continue - the server might still be starting...")
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

def chat():
    """Interactive chat function similar to ChatGPT (Windows optimized)"""
    if COLORS_AVAILABLE:
        print(f"{Fore.CYAN}🤖 Welcome to GenAI Chat! (Type 'quit', 'exit', or 'q' to stop){Style.RESET_ALL}")
    else:
        print("🤖 Welcome to GenAI Chat! (Type 'quit', 'exit', or 'q' to stop)")
    print("=" * 50)
    
    # Initialize conversation history
    conversation = []
    
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            # Check for quit commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                if COLORS_AVAILABLE:
                    print(f"\n{Fore.GREEN}👋 Goodbye! Thanks for chatting!{Style.RESET_ALL}")
                else:
                    print("\n👋 Goodbye! Thanks for chatting!")
                break
            
            # Skip empty inputs
            if not user_input:
                print("Please enter a message or 'quit' to exit.")
                continue
            
            # Add user message to conversation
            conversation.append({'role': 'user', 'content': user_input})
            
            # Get AI response with Windows-specific error handling
            if COLORS_AVAILABLE:
                print(f"{Fore.CYAN}🤖 AI: {Style.RESET_ALL}", end="", flush=True)
            else:
                print("🤖 AI: ", end="", flush=True)
                
            try:
                response = ollama.chat(model='phi3:mini', messages=conversation)
                ai_response = response['message']['content']
                
                # Print AI response
                print(ai_response)
                
                # Add AI response to conversation history
                conversation.append({'role': 'assistant', 'content': ai_response})
                
            except Exception as e:
                if COLORS_AVAILABLE:
                    print(f"{Fore.RED}❌ Error connecting to AI: {e}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}💡 Try waiting a moment for the server to fully start, then try again.{Style.RESET_ALL}")
                else:
                    print(f"❌ Error connecting to AI: {e}")
                    print("💡 Try waiting a moment for the server to fully start, then try again.")
            
        except KeyboardInterrupt:
            if COLORS_AVAILABLE:
                print(f"\n\n{Fore.GREEN}👋 Chat interrupted. Goodbye!{Style.RESET_ALL}")
            else:
                print("\n\n👋 Chat interrupted. Goodbye!")
            break
        except Exception as e:
            if COLORS_AVAILABLE:
                print(f"\n{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
            else:
                print(f"\n❌ Error: {e}")
            print("Please try again or type 'quit' to exit.")

def generative():
    """Generate instructions based on PDF documents (Windows version - to be implemented)"""
    if COLORS_AVAILABLE:
        print(f"{Fore.CYAN}📄 Generative Document Analysis{Style.RESET_ALL}")
    else:
        print("📄 Generative Document Analysis")
    print("=" * 40)
    if COLORS_AVAILABLE:
        print(f"{Fore.YELLOW}🚧 This feature will be implemented later.{Style.RESET_ALL}")
    else:
        print("🚧 This feature will be implemented later.")
    print("📋 Planned functionality:")
    print("   • Read 2-3 PDF documents")
    print("   • Analyze document content")
    print("   • Generate instructions based on the documents")
    print("   • Provide document-based Q&A")
    
    # Placeholder for future implementation
    input("\nPress Enter to return to main menu...")

def main_menu():
    """Display main menu and handle user selection (Windows optimized)"""
    while True:
        print("\n" + "=" * 50)
        if COLORS_AVAILABLE:
            print(f"{Fore.CYAN}🚀 GenAI Demo - Windows Edition - Choose an option:{Style.RESET_ALL}")
        else:
            print("🚀 GenAI Demo - Windows Edition - Choose an option:")
        print("=" * 50)
        print("1. 💬 Interactive Chat")
        print("2. 📄 Document Analysis (Coming Soon)")
        print("3. 🚪 Exit")
        print("-" * 50)
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            chat()
        elif choice == '2':
            generative()
        elif choice == '3':
            if COLORS_AVAILABLE:
                print(f"\n{Fore.GREEN}👋 Goodbye!{Style.RESET_ALL}")
            else:
                print("\n👋 Goodbye!")
            break
        else:
            if COLORS_AVAILABLE:
                print(f"{Fore.RED}❌ Invalid choice. Please enter 1, 2, or 3.{Style.RESET_ALL}")
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")

try:
    # Ensure Ollama is running before making requests
    if COLORS_AVAILABLE:
        print(f"{Fore.CYAN}🚀 Starting GenAI Demo for Windows...{Style.RESET_ALL}")
    else:
        print("🚀 Starting GenAI Demo for Windows...")
        
    ollama_manager.ensure_ollama_running()
    
    # Start the main menu
    main_menu()

except KeyboardInterrupt:
    if COLORS_AVAILABLE:
        print(f"\n{Fore.YELLOW}Program interrupted by user{Style.RESET_ALL}")
    else:
        print("\nProgram interrupted by user")
except Exception as e:
    if COLORS_AVAILABLE:
        print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 If this is a connection error, try running the program again in a few moments.{Style.RESET_ALL}")
    else:
        print(f"An error occurred: {e}")
        print("💡 If this is a connection error, try running the program again in a few moments.")
finally:
    # Ensure cleanup happens even if there's an exception
    ollama_manager.shutdown_ollama()