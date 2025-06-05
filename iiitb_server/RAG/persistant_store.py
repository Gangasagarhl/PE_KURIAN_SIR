import os
import pandas as pd
import pickle
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Union
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.documents import Document

class PersistentVectorStore:
    """
    Persistent vector store manager with MongoDB-like functionality for FAISS.
    Handles storage, retrieval, and incremental updates of vector embeddings.
    """
    
    def __init__(self, 
                 store_path: str = "./vector_store",
                 model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
                 chunk_size: int = 200,
                 chunk_overlap: int = 50):
        """
        Initialize persistent vector store.
        
        Args:
            store_path: Directory path to store vector database files
            model_name: HuggingFace embedding model name
            chunk_size: Size of text chunks for splitting
            chunk_overlap: Overlap between consecutive chunks
        """
        self.store_path = Path(store_path)
        self.store_path.mkdir(exist_ok=True)
        
        # Vector store files
        self.faiss_index_path = self.store_path / "faiss_index"
        self.metadata_path = self.store_path / "metadata.pkl"
        self.documents_path = self.store_path / "documents.pkl"
        
        # Initialize components
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap
        )
        
        # Load or initialize vector store
        self.vectorstore = None
        self.metadata = {}
        self.stored_documents = []
        
        self._load_existing_store()
        
    def _load_existing_store(self):
        """Load existing vector store and metadata if available."""
        try:
            if self.faiss_index_path.exists():
                print(" Loading existing vector store...")
                self.vectorstore = FAISS.load_local(
                    str(self.faiss_index_path), 
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                
                # Load metadata
                if self.metadata_path.exists():
                    with open(self.metadata_path, 'rb') as f:
                        self.metadata = pickle.load(f)
                
                # Load stored documents
                if self.documents_path.exists():
                    with open(self.documents_path, 'rb') as f:
                        self.stored_documents = pickle.load(f)
                        
                print(f" Loaded vector store with {len(self.stored_documents)} documents")
            else:
                print(" Creating new vector store...")
                
        except Exception as e:
            print(f" Error loading existing store: {e}")
            print(" Creating new vector store...")
    
    def _save_store(self):
        """Save vector store and metadata to disk."""
        try:
            if self.vectorstore:
                # Save FAISS index
                self.vectorstore.save_local(str(self.faiss_index_path))
                
                # Save metadata
                with open(self.metadata_path, 'wb') as f:
                    pickle.dump(self.metadata, f)
                
                # Save documents
                with open(self.documents_path, 'wb') as f:
                    pickle.dump(self.stored_documents, f)
                
                print(" Vector store saved successfully")
        except Exception as e:
            print(f" Error saving store: {e}")
    
    def add_documents(self, documents: List[Document], source_id: str = None):
        """
        Add documents to the vector store.
        
        Args:
            documents: List of Document objects to add
            source_id: Optional identifier for the document source
        """
        if not documents:
            return
        
        # Split documents
        split_docs = self.text_splitter.split_documents(documents)
        
        # Add metadata
        timestamp = datetime.now().isoformat()
        for doc in split_docs:
            doc.metadata.update({
                'added_at': timestamp,
                'source_id': source_id or 'unknown'
            })
        
        # Create or update vector store
        if self.vectorstore is None:
            self.vectorstore = FAISS.from_documents(split_docs, self.embeddings)
        else:
            # Add to existing vector store
            new_vectorstore = FAISS.from_documents(split_docs, self.embeddings)
            self.vectorstore.merge_from(new_vectorstore)
        
        # Update stored documents and metadata
        self.stored_documents.extend(split_docs)
        if source_id:
            self.metadata[source_id] = {
                'added_at': timestamp,
                'document_count': len(split_docs),
                'total_documents': len(self.stored_documents)
            }
        
        # Save to disk
        self._save_store()
        print(f" Added {len(split_docs)} document chunks to vector store")
    
    def add_from_csv(self, csv_path: str, text_column: str = 'description', source_id: str = None):
        """
        Add documents from CSV file.
        
        Args:
            csv_path: Path to CSV file
            text_column: Column name containing text data
            source_id: Optional identifier for this CSV source
        """
        try:
            df = pd.read_csv(csv_path)
            
            if text_column not in df.columns:
                raise ValueError(f"Column '{text_column}' not found in CSV")
            
            # Create documents from CSV rows
            documents = []
            for idx, row in df.iterrows():
                text_content = str(row[text_column])
                metadata = {
                    'row_id': idx,
                    'csv_path': csv_path,
                }
                # Add other columns as metadata
                for col in df.columns:
                    if col != text_column:
                        metadata[col] = str(row[col])
                
                documents.append(Document(
                    page_content=text_content,
                    metadata=metadata
                ))
            
            source_id = source_id or f"csv_{Path(csv_path).stem}"
            self.add_documents(documents, source_id)
            
            print(f" Added {len(documents)} rows from CSV: {csv_path}")
            
        except Exception as e:
            print(f" Error adding CSV data: {e}")
    
    def add_text(self, text: str, metadata: Dict = None, source_id: str = None):
        """
        Add raw text to vector store.
        
        Args:
            text: Raw text content
            metadata: Optional metadata dictionary
            source_id: Optional source identifier
        """
        doc = Document(
            page_content=text,
            metadata=metadata or {}
        )
        self.add_documents([doc], source_id)
    
    def search(self, query: str, k: int = 4) -> List[Document]:
        """
        Search for similar documents.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of similar documents
        """
        if not self.vectorstore:
            print(" No documents in vector store")
            return []
        
        return self.vectorstore.similarity_search(query, k=k)
    
    def get_retriever(self, search_kwargs: Dict = None):
        """Get retriever for the vector store."""
        if not self.vectorstore:
            raise ValueError("Vector store is empty. Add documents first.")
        
        search_kwargs = search_kwargs or {"k": 4}
        return self.vectorstore.as_retriever(search_kwargs=search_kwargs)
    
    def delete_by_source(self, source_id: str):
        """
        Delete documents by source ID.
        Note: FAISS doesn't support direct deletion, so this recreates the store.
        """
        if source_id not in self.metadata:
            print(f" Source ID '{source_id}' not found")
            return
        
        # Filter out documents from the specified source
        remaining_docs = [
            doc for doc in self.stored_documents 
            if doc.metadata.get('source_id') != source_id
        ]
        
        if remaining_docs:
            # Recreate vector store with remaining documents
            self.vectorstore = FAISS.from_documents(remaining_docs, self.embeddings)
            self.stored_documents = remaining_docs
        else:
            # No documents left
            self.vectorstore = None
            self.stored_documents = []
        
        # Update metadata
        del self.metadata[source_id]
        
        # Save changes
        self._save_store()
        print(f" Deleted documents from source: {source_id}")
    
    def get_stats(self) -> Dict:
        """Get statistics about the vector store."""
        return {
            'total_documents': len(self.stored_documents),
            'sources': list(self.metadata.keys()),
            'store_size_mb': self._get_store_size(),
            'metadata': self.metadata
        }
    
    def _get_store_size(self) -> float:
        """Get approximate size of the vector store in MB."""
        total_size = 0
        for file_path in self.store_path.iterdir():
            if file_path.is_file():
                total_size += file_path.stat().st_size
        return round(total_size / (1024 * 1024), 2)

