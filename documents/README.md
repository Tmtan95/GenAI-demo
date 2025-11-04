# RAG System Setup Instructions

## 📚 **Recommended Embedding Model**

**🥇 BAAI/bge-large-en-v1.5**
- **Size**: ~1.34GB (high-quality model)
- **Dimensions**: 1024 (excellent for semantic understanding)
- **Performance**: State-of-the-art accuracy for technical documents
- **Speed**: Optimized for large PDFs (15MB+)
- **Offline**: Works completely offline after initial download
- **Best for**: Research papers, technical documentation, large documents

## 🛠️ **Installation**

1. **Install RAG dependencies:**
```bash
# Activate your virtual environment first
source env/bin/activate  # On macOS/Linux

# Install all required packages
pip install -r requirements.txt
```

2. **Add your PDF documents:**
```bash
# Place 2-3 PDF files in the documents folder
cp your_document1.pdf documents/
cp your_document2.pdf documents/
cp your_document3.pdf documents/
```

3. **Test the system:**
```bash
# Run the main demo
python app/demo.py

# Select option 2 (Document Analysis)
```

## 🎯 **RAG System Features**

### **Smart Caching**
- ✅ Processes documents once, caches results
- ⚡ Lightning-fast subsequent loads
- 🔄 Auto-detects document changes

### **Optimized for Large Documents**
- 📊 Chunk size: 500 characters (optimal for PDFs)
- 🎯 Retrieves top 3 most relevant sections
- � Handles 15MB+ PDF files efficiently
- 🎓 High-quality embeddings for better semantic search

### **Offline Operation**
- 🔒 No internet required after setup
- 🛡️ Your documents stay private
- ⚡ Fast local inference

## 📋 **Usage Example**

1. **Start the application:**
```bash
python app/demo.py
```

2. **Select Document Analysis (Option 2)**

3. **Ask questions like:**
- "What are the main topics covered in these documents?"
- "Summarize the key findings"
- "What recommendations are made?"
- "Explain the methodology used"

## 🗂️ **Project Structure**
```
GenAI-Demo/
├── documents/           # Place your PDF files here
├── cache/              # Cached embeddings (auto-generated)
├── rag_system.py       # RAG implementation
├── app/demo.py         # Main application
└── requirements.txt    # Dependencies
```

## 🔧 **Troubleshooting**

### **"No PDF files found"**
- Make sure PDFs are in the `documents/` folder
- Check file extensions are `.pdf` (lowercase)

### **Import errors**
```bash
# Install missing packages
pip install sentence-transformers faiss-cpu PyPDF2 numpy
```

### **Memory issues**
- The system is optimized for small files (2-3 PDFs)
- If you have large PDFs, consider splitting them

### **Embedding model download**
- First run downloads ~23MB model
- Subsequent runs use cached model
- No internet needed after first setup

## 🚀 **Performance Tips**

1. **PDF Quality**: Clear, text-based PDFs work best
2. **File Size**: Keep individual PDFs under 10MB for best performance  
3. **Document Count**: Optimal with 2-3 PDFs (as requested)
4. **Questions**: Be specific for better retrieval results

## 🎨 **Advanced Features**

- **Similarity Scoring**: Shows relevance of retrieved content
- **Source Attribution**: Links answers back to specific documents
- **Context Chunking**: Smart text segmentation with overlap
- **Vector Search**: Fast semantic similarity matching

## 📊 **Model Specifications**

| Feature | Specification |
|---------|---------------|
| Embedding Model | all-MiniLM-L6-v2 |
| Model Size | ~23MB |
| Embedding Dimensions | 384 |
| Chunk Size | 500 characters |
| Chunk Overlap | 50 characters |
| Top-K Retrieval | 3 chunks |
| Vector Store | FAISS (CPU) |
| PDF Parser | PyPDF2 |

Perfect for your requirements: **small, offline, efficient!** 🎯