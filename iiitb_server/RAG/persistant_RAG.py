from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.documents import Document
from typing import List, Dict, Optional, Union
from dotenv import load_dotenv


from RAG.persistant_store import PersistentVectorStore

class PersistentRAGSystem:
    """
    RAG system with persistent vector storage and incremental data addition.
    """
    
    def __init__(self,
                 store_path: str = "./vector_store",
                 model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
                 llm_model: str = "llama3.2"):
        """
        Initialize persistent RAG system.
        
        Args:
            store_path: Path for vector store persistence
            model_name: HuggingFace embedding model
            llm_model: Ollama LLM model name
        """
        load_dotenv()
        
        # Initialize persistent vector store
        self.vector_store = PersistentVectorStore(store_path, model_name)
        
        # Initialize LLM and chains
        self.llm = Ollama(model=llm_model)
        self.prompt = ChatPromptTemplate.from_template(
            """
            Answer the following question based only on the provided context:
            <context>
            {context}
            </context>
            Question: {input}
            
            If the context doesn't contain enough information to answer the question,
            please say "I don't have enough information in the knowledge base to answer this question."
            """
        )
        self.document_chain = create_stuff_documents_chain(self.llm, self.prompt)
    
    def add_csv_data(self, csv_path: str, text_column: str = 'description', source_id: str = None):
        """Add data from CSV file to the knowledge base."""
        self.vector_store.add_from_csv(csv_path, text_column, source_id)
    
    def add_text_data(self, text: str, metadata: Dict = None, source_id: str = None):
        """Add raw text to the knowledge base."""
        self.vector_store.add_text(text, metadata, source_id)
    
    def add_documents(self, documents: List[Document], source_id: str = None):
        """Add Document objects to the knowledge base."""
        self.vector_store.add_documents(documents, source_id)
    
    def query(self, question: str, k: int = 4) -> Dict:
        """
        Query the RAG system.
        
        Args:
            question: User question
            k: Number of context documents to retrieve
            
        Returns:
            Dictionary with answer and context
        """
        try:
            # Get retriever
            retriever = self.vector_store.get_retriever({"k": k})
            
            # Create retrieval chain
            retrieval_chain = create_retrieval_chain(retriever, self.document_chain)
            
            # Execute query
            response = retrieval_chain.invoke({"input": question})
            
            return {
                "answer": response["answer"],
                "context": [doc.page_content for doc in response["context"]],
                "sources": [doc.metadata for doc in response["context"]]
            }
            
        except ValueError as e:
            return {
                "answer": "No knowledge base available. Please add some data first.",
                "context": [],
                "sources": []
            }
        except Exception as e:
            return {
                "answer": f"Error processing query: {str(e)}",
                "context": [],
                "sources": []
            }
    
    def search_similar(self, query: str, k: int = 5) -> List[Document]:
        """Search for similar documents without LLM processing."""
        return self.vector_store.search(query, k)
    
    def get_knowledge_base_stats(self) -> Dict:
        """Get statistics about the knowledge base."""
        return self.vector_store.get_stats()
    
    def delete_source(self, source_id: str):
        """Delete all documents from a specific source."""
        self.vector_store.delete_by_source(source_id)
    
    def update_source(self, source_id: str, csv_path: str = None, text: str = None, 
                     text_column: str = 'description'):
        """
        Update a data source by deleting old data and adding new data.
        
        Args:
            source_id: ID of the source to update
            csv_path: Path to new CSV file (if updating from CSV)
            text: New text content (if updating from text)
            text_column: Column name for CSV text data
        """
        # Delete existing data
        self.delete_source(source_id)
        
        # Add new data
        if csv_path:
            self.add_csv_data(csv_path, text_column, source_id)
        elif text:
            self.add_text_data(text, source_id=source_id)
        else:
            print(" No new data provided for update")

# Example usage and testing
if __name__ == "__main__":
    # Initialize persistent RAG system
    rag = PersistentRAGSystem(store_path="./my_knowledge_base", llm_model="llama3.2")
    
    # Check current status
    print(" Current knowledge base stats:")
    stats = rag.get_knowledge_base_stats()
    print(f"Total documents: {stats['total_documents']}")
    print(f"Sources: {stats['sources']}")
    print(f"Store size: {stats['store_size_mb']} MB")
    print()
    
    # Add data from CSV (this will persist between runs)
    print(" Adding CSV data...")
    rag.add_csv_data("../database/data.csv", "description", "main_data")
    
    # Add some sample text data
    print(" Adding text data...")
    rag.add_text_data(
        "Our API has rate limits of 1000 requests per hour for free users and 10000 requests per hour for premium users.",
        {"type": "api_limits", "category": "usage"},
        "api_policies"
    )
    
    rag.add_text_data(
        "The maximum file size for uploads is 100MB. Supported formats include PDF, DOCX, TXT, and CSV files.",
        {"type": "file_limits", "category": "uploads"},
        "file_policies"
    )
    
    # Query the system
    print("\n Querying the system...")
    response = rag.query("What are the usage limits?")
    print("Answer:", response["answer"])
    print("\nContext sources:", len(response["sources"]))
    
    # Check updated stats
    print("\n Updated knowledge base stats:")
    stats = rag.get_knowledge_base_stats()
    print(f"Total documents: {stats['total_documents']}")
    print(f"Sources: {stats['sources']}")
    print(f"Store size: {stats['store_size_mb']} MB")
    
    # Demonstrate persistence - the next time you run this script,
    # the vector store will load the previously stored data automatically!