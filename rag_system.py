"""
RAG (Retrieval-Augmented Generation) System for GenAI Demo

This module implements a simple but effective RAG system using:
- sentence-transformers for embeddings (all-MiniLM-L6-v2)
- FAISS for vector similarity search
- PyPDF2 for PDF text extraction
- Ollama phi3:mini for text generation

Features:
- Offline operation (after initial model download)
- Small memory footprint
- Fast inference
- Optimized for 2-3 PDF documents
"""

import os
import pickle
import numpy as np
from typing import List, Tuple, Optional
import ollama


class RAGSystem:
    """RAG system for document-based question answering"""
    
    def __init__(self, documents_folder: str = "documents", cache_folder: str = "cache"):
        self.documents_folder = documents_folder
        self.cache_folder = cache_folder
        self.chunk_size = 500  # Characters per chunk
        self.chunk_overlap = 50  # Overlap between chunks
        self.top_k = 3  # Number of relevant chunks to retrieve
        
        # Initialize components
        self.embeddings_model = None
        self.vector_store = None
        self.chunks = []
        self.chunk_metadata = []
        
        # Ensure folders exist
        os.makedirs(documents_folder, exist_ok=True)
        os.makedirs(cache_folder, exist_ok=True)
    
    def _load_embedding_model(self):
        """Load the sentence transformer model"""
        try:
            from sentence_transformers import SentenceTransformer
            
            print("📥 Loading embedding model (all-MiniLM-L6-v2)...")
            # This model is small (~23MB) and good for general text
            self.embeddings_model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✅ Embedding model loaded successfully!")
            return True
        except ImportError:
            print("❌ sentence-transformers not installed. Run: pip install sentence-transformers")
            return False
        except Exception as e:
            print(f"❌ Failed to load embedding model: {e}")
            return False
    
    def _load_vector_store(self):
        """Initialize FAISS vector store"""
        try:
            import faiss
            
            # We'll initialize this when we have embeddings
            self.faiss = faiss
            return True
        except ImportError:
            print("❌ FAISS not installed. Run: pip install faiss-cpu")
            return False
    
    def find_pdf_files(self) -> List[str]:
        """Find PDF files in the documents folder"""
        pdf_files = []
        if os.path.exists(self.documents_folder):
            for file in os.listdir(self.documents_folder):
                if file.lower().endswith('.pdf'):
                    pdf_files.append(os.path.join(self.documents_folder, file))
        return pdf_files
    
    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        try:
            import PyPDF2
            
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except ImportError:
            print("❌ PyPDF2 not installed. Run: pip install PyPDF2")
            return ""
        except Exception as e:
            print(f"❌ Error reading PDF {pdf_path}: {e}")
            return ""
    
    def _chunk_text(self, text: str, filename: str) -> List[dict]:
        """Split text into overlapping chunks"""
        chunks = []
        
        # Simple chunking by characters
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunk_text = text[i:i + self.chunk_size]
            
            # Skip very short chunks
            if len(chunk_text.strip()) < 50:
                continue
            
            chunks.append({
                'text': chunk_text.strip(),
                'source': filename,
                'chunk_id': len(chunks)
            })
        
        return chunks
    
    def _get_cache_path(self, pdf_files: List[str]) -> str:
        """Generate cache path based on PDF files and modification times"""
        # Create a hash of filenames and modification times
        import hashlib
        
        files_info = []
        for pdf_file in pdf_files:
            if os.path.exists(pdf_file):
                mtime = str(os.path.getmtime(pdf_file))
                files_info.append(f"{pdf_file}:{mtime}")
        
        cache_key = hashlib.md5("|".join(files_info).encode()).hexdigest()
        return os.path.join(self.cache_folder, f"rag_cache_{cache_key}.pkl")
    
    def _load_from_cache(self, cache_path: str) -> bool:
        """Load processed documents from cache"""
        try:
            if os.path.exists(cache_path):
                print("📋 Loading from cache...")
                with open(cache_path, 'rb') as f:
                    cache_data = pickle.load(f)
                
                self.chunks = cache_data['chunks']
                self.chunk_metadata = cache_data['metadata']
                
                # Recreate vector store
                if cache_data['embeddings'] is not None:
                    embeddings = cache_data['embeddings']
                    dimension = embeddings.shape[1]
                    self.vector_store = self.faiss.IndexFlatIP(dimension)  # Inner product for similarity
                    self.vector_store.add(embeddings.astype('float32'))
                
                print("✅ Cache loaded successfully!")
                return True
        except Exception as e:
            print(f"⚠️ Could not load cache: {e}")
        
        return False
    
    def _save_to_cache(self, cache_path: str, embeddings: np.ndarray):
        """Save processed documents to cache"""
        try:
            cache_data = {
                'chunks': self.chunks,
                'metadata': self.chunk_metadata,
                'embeddings': embeddings
            }
            
            with open(cache_path, 'wb') as f:
                pickle.dump(cache_data, f)
            
            print("💾 Results cached for faster future loading.")
        except Exception as e:
            print(f"⚠️ Could not save cache: {e}")
    
    def process_documents(self, pdf_files: List[str]) -> bool:
        """Process PDF documents and build vector store"""
        try:
            # Load required models
            if not self._load_embedding_model():
                return False
            
            if not self._load_vector_store():
                return False
            
            # Check cache first
            cache_path = self._get_cache_path(pdf_files)
            if self._load_from_cache(cache_path):
                return True
            
            print("📖 Extracting text from PDFs...")
            
            # Process each PDF
            all_chunks = []
            for pdf_file in pdf_files:
                print(f"   Processing: {os.path.basename(pdf_file)}")
                
                text = self._extract_text_from_pdf(pdf_file)
                if not text.strip():
                    print(f"⚠️ No text extracted from {pdf_file}")
                    continue
                
                chunks = self._chunk_text(text, os.path.basename(pdf_file))
                all_chunks.extend(chunks)
                print(f"   Created {len(chunks)} text chunks")
            
            if not all_chunks:
                print("❌ No text chunks created from PDFs")
                return False
            
            self.chunks = [chunk['text'] for chunk in all_chunks]
            self.chunk_metadata = all_chunks
            
            print(f"🔤 Generating embeddings for {len(self.chunks)} chunks...")
            
            # Generate embeddings
            embeddings = self.embeddings_model.encode(
                self.chunks,
                show_progress_bar=True,
                convert_to_numpy=True
            )
            
            print("🗃️ Building vector store...")
            
            # Create FAISS index
            dimension = embeddings.shape[1]
            self.vector_store = self.faiss.IndexFlatIP(dimension)  # Inner product similarity
            
            # Normalize embeddings for cosine similarity
            embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
            self.vector_store.add(embeddings.astype('float32'))
            
            # Save to cache
            self._save_to_cache(cache_path, embeddings)
            
            return True
            
        except Exception as e:
            print(f"❌ Error processing documents: {e}")
            return False
    
    def _retrieve_relevant_chunks(self, query: str) -> List[dict]:
        """Retrieve most relevant chunks for a query"""
        try:
            # Generate query embedding
            query_embedding = self.embeddings_model.encode([query], convert_to_numpy=True)
            query_embedding = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
            
            # Search vector store
            scores, indices = self.vector_store.search(query_embedding.astype('float32'), self.top_k)
            
            # Return relevant chunks with metadata
            relevant_chunks = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(self.chunk_metadata):
                    chunk_info = self.chunk_metadata[idx].copy()
                    chunk_info['similarity_score'] = float(score)
                    relevant_chunks.append(chunk_info)
            
            return relevant_chunks
            
        except Exception as e:
            print(f"❌ Error retrieving chunks: {e}")
            return []
    
    def query(self, question: str) -> str:
        """Answer a question using RAG"""
        try:
            # Retrieve relevant context
            relevant_chunks = self._retrieve_relevant_chunks(question)
            
            if not relevant_chunks:
                return "❌ No relevant information found in the documents."
            
            # Build context from relevant chunks
            context_parts = []
            sources = set()
            
            for chunk in relevant_chunks:
                context_parts.append(f"From {chunk['source']}:\n{chunk['text']}")
                sources.add(chunk['source'])
            
            context = "\n\n".join(context_parts)
            
            # Create prompt for Ollama
            prompt = f"""Based on the following document excerpts, please answer the question thoroughly and accurately.

CONTEXT:
{context}

QUESTION: {question}

Please provide a detailed answer based solely on the information in the provided context. If the context doesn't contain enough information to answer the question completely, please mention what additional information would be helpful.

ANSWER:"""
            
            # Get response from Ollama
            print("🤔 Generating answer...")
            response = ollama.chat(
                model='phi3:mini',
                messages=[{'role': 'user', 'content': prompt}]
            )
            
            answer = response['message']['content']
            
            # Add source information
            sources_list = ", ".join(sources)
            answer += f"\n\n📚 Sources: {sources_list}"
            
            return answer
            
        except Exception as e:
            return f"❌ Error generating answer: {e}"


# Convenience functions for direct use
def setup_rag_system():
    """Set up RAG system with example usage"""
    print("🚀 Setting up RAG system...")
    
    rag = RAGSystem()
    
    # Create documents folder if it doesn't exist
    if not os.path.exists(rag.documents_folder):
        os.makedirs(rag.documents_folder)
        print(f"📁 Created '{rag.documents_folder}' folder for your PDF files.")
    
    return rag


if __name__ == "__main__":
    # Example usage
    rag = setup_rag_system()
    
    pdf_files = rag.find_pdf_files()
    if pdf_files:
        print(f"Found {len(pdf_files)} PDF files:")
        for pdf in pdf_files:
            print(f"  - {pdf}")
        
        if rag.process_documents(pdf_files):
            while True:
                question = input("\nAsk a question (or 'quit' to exit): ")
                if question.lower() in ['quit', 'exit']:
                    break
                
                answer = rag.query(question)
                print(f"\nAnswer: {answer}")
    else:
        print("No PDF files found. Please add some PDFs to the 'documents' folder.")