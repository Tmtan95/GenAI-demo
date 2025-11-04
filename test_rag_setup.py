#!/usr/bin/env python3
"""
Test script for the RAG system functionality
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_rag_imports():
    """Test if RAG system can be imported"""
    try:
        from rag_system import RAGSystem
        print("✅ RAG system imports successfully")
        return True
    except ImportError as e:
        print(f"❌ RAG import failed: {e}")
        return False

def test_dependencies():
    """Test if required dependencies are available"""
    required_packages = [
        'sentence_transformers',
        'faiss',
        'PyPDF2', 
        'numpy'
    ]
    
    missing = []
    for package in required_packages:
        try:
            if package == 'faiss':
                import faiss
            elif package == 'sentence_transformers':
                import sentence_transformers
            else:
                __import__(package)
            print(f"✅ {package} available")
        except ImportError:
            print(f"❌ {package} missing")
            missing.append(package)
    
    return len(missing) == 0

def test_rag_initialization():
    """Test RAG system initialization"""
    try:
        from rag_system import RAGSystem
        
        rag = RAGSystem()
        print(f"✅ RAG initialized - Documents: {rag.documents_folder}")
        
        # Test finding PDFs (should return empty list if none exist)
        pdf_files = rag.find_pdf_files()
        print(f"📄 Found {len(pdf_files)} PDF files")
        
        return True
    except Exception as e:
        print(f"❌ RAG initialization failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing RAG System Setup")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_rag_imports),
        ("Dependencies Test", test_dependencies),
        ("Initialization Test", test_rag_initialization)
    ]
    
    passed = 0
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}:")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 40)
    print(f"📊 Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! RAG system is ready to use.")
        print("\n💡 Next steps:")
        print("1. Add PDF files to the 'documents/' folder")
        print("2. Run: python app/demo.py")
        print("3. Select option 2 (Document Analysis)")
    else:
        print("⚠️ Some tests failed. Please check the dependencies.")
        print("\n🔧 To install missing dependencies:")
        print("pip install sentence-transformers faiss-cpu PyPDF2 numpy")

if __name__ == "__main__":
    main()