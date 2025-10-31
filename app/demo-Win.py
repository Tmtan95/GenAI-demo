import ollama
import sys

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

def check_ollama_connection():
    """Check if Ollama is available and models are ready"""
    try:
        models_response = ollama.list()
        if COLORS_AVAILABLE:
            print(f"{Fore.GREEN}✓ Connected to Ollama service{Style.RESET_ALL}")
        else:
            print("✓ Connected to Ollama service")
        
        # Handle both new Model object format and old dict format
        if hasattr(models_response, 'models'):
            models = models_response.models
        else:
            models = models_response.get('models', [])
        
        # Check if phi3:mini model is available
        model_found = False
        for model in models:
            # Handle Model object vs dict
            if hasattr(model, 'model'):
                model_name = model.model
            else:
                model_name = model.get('name', model.get('model', ''))
            
            if 'phi3:mini' in model_name:
                model_found = True
                break
        
        if model_found:
            if COLORS_AVAILABLE:
                print(f"{Fore.GREEN}✓ phi3:mini model ready{Style.RESET_ALL}")
            else:
                print("✓ phi3:mini model ready")
            return True
        else:
            if COLORS_AVAILABLE:
                print(f"{Fore.YELLOW}⚠ phi3:mini model not found{Style.RESET_ALL}")
                print(f"{Fore.CYAN}💡 Please run: ollama pull phi3:mini{Style.RESET_ALL}")
            else:
                print("⚠ phi3:mini model not found")
                print("💡 Please run: ollama pull phi3:mini")
            return False
            
    except Exception as e:
        if COLORS_AVAILABLE:
            print(f"{Fore.RED}❌ Cannot connect to Ollama: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 Make sure Ollama is installed and running{Style.RESET_ALL}")
        else:
            print(f"❌ Cannot connect to Ollama: {e}")
            print("💡 Make sure Ollama is installed and running")
        return False

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
                    print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}💡 Make sure Ollama service is running and phi3:mini model is available{Style.RESET_ALL}")
                else:
                    print(f"❌ Error: {e}")
                    print("💡 Make sure Ollama service is running and phi3:mini model is available")
            
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

def main():
    """Main function for Windows GenAI Demo"""
    if COLORS_AVAILABLE:
        print(f"{Fore.CYAN}🚀 GenAI Demo - Windows Edition{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Uses system Ollama installation (C:/Users/.ollama/models/){Style.RESET_ALL}")
    else:
        print("🚀 GenAI Demo - Windows Edition")
        print("Uses system Ollama installation (C:/Users/.ollama/models/)")
    
    print("=" * 60)
    
    # Check Ollama connection and model availability
    if not check_ollama_connection():
        if COLORS_AVAILABLE:
            print(f"\n{Fore.RED}❌ Setup incomplete. Please fix the above issues and try again.{Style.RESET_ALL}")
        else:
            print("\n❌ Setup incomplete. Please fix the above issues and try again.")
        input("Press Enter to exit...")
        return
    
    # Start the main menu
    main_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        if COLORS_AVAILABLE:
            print(f"\n{Fore.YELLOW}👋 Program interrupted by user. Goodbye!{Style.RESET_ALL}")
        else:
            print("\n👋 Program interrupted by user. Goodbye!")
    except Exception as e:
        if COLORS_AVAILABLE:
            print(f"\n{Fore.RED}❌ An error occurred: {e}{Style.RESET_ALL}")
        else:
            print(f"\n❌ An error occurred: {e}")
        input("Press Enter to exit...")