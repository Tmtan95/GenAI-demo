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
        except Exception as e:
            print("Starting Ollama server...")
            try:
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
            except Exception as startup_error:
                print(f"Failed to start Ollama server: {startup_error}")
                return False
    
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

def chat():
    """Interactive chat function similar to ChatGPT"""
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
                print("\n👋 Goodbye! Thanks for chatting!")
                break
            
            # Skip empty inputs
            if not user_input:
                print("Please enter a message or 'quit' to exit.")
                continue
            
            # Add user message to conversation
            conversation.append({'role': 'user', 'content': user_input})
            
            # Get AI response
            print("🤖 AI: ", end="", flush=True)
            response = ollama.chat(model='phi3:mini', messages=conversation)
            ai_response = response['message']['content']
            
            # Print AI response
            print(ai_response)
            
            # Add AI response to conversation history
            conversation.append({'role': 'assistant', 'content': ai_response})
            
        except KeyboardInterrupt:
            print("\n\n👋 Chat interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again or type 'quit' to exit.")

def generative():
    """Generate instructions based on PDF documents using RAG"""
    print("📄 Generative Document Analysis with RAG")
    print("=" * 50)
    
    try:
        # Import required libraries
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from rag_system import RAGSystem
        
        # Initialize RAG system
        print("� Initializing RAG system...")
        rag = RAGSystem()
        
        # Check for PDF documents
        pdf_files = rag.find_pdf_files()
        if not pdf_files:
            print("❌ No PDF files found in the 'documents' folder.")
            print("💡 Please add 2-3 PDF files to 'documents/' folder and try again.")
            input("\nPress Enter to return to main menu...")
            return
        
        print(f"� Found {len(pdf_files)} PDF file(s):")
        for i, pdf in enumerate(pdf_files, 1):
            print(f"   {i}. {pdf}")
        
        # Process documents
        print("\n🔄 Processing documents and building knowledge base...")
        success = rag.process_documents(pdf_files)
        
        if not success:
            print("❌ Failed to process documents. Please check the PDF files.")
            input("\nPress Enter to return to main menu...")
            return
        
        print("✅ Documents processed successfully!")
        print("\n" + "=" * 50)
        print("🤖 RAG-Powered Q&A System Ready!")
        print("Ask questions about your documents or request analysis.")
        print("Type 'quit', 'exit', or 'q' to return to main menu.")
        print("=" * 50)
        
        # Interactive Q&A loop
        while True:
            try:
                question = input("\n❓ Your Question: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Returning to main menu...")
                    break
                
                if not question:
                    print("Please enter a question or 'quit' to exit.")
                    continue
                
                print("\n🔍 Searching documents...")
                answer = rag.query(question)
                
                print(f"\n🤖 AI Analysis:\n{answer}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Document analysis interrupted. Returning to menu...")
                break
            except Exception as e:
                print(f"\n❌ Error processing question: {e}")
                print("Please try again or type 'quit' to exit.")
    
    except ImportError:
        print("❌ RAG system dependencies not installed.")
        print("\n📦 Required packages:")
        print("   pip install sentence-transformers PyPDF2 faiss-cpu numpy")
        print("\n💡 Run the installation command and try again.")
        input("\nPress Enter to return to main menu...")
    except Exception as e:
        print(f"❌ Error initializing RAG system: {e}")
        input("\nPress Enter to return to main menu...")

def main_menu():
    """Display main menu and handle user selection"""
    while True:
        print("\n" + "=" * 50)
        print("🚀 GenAI Demo - Choose an option:")
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
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

try:
    # Ensure Ollama is running before making requests
    ollama_manager.ensure_ollama_running()
    
    # Start the main menu
    main_menu()

finally:
    # Ensure cleanup happens even if there's an exception
    ollama_manager.shutdown_ollama()
