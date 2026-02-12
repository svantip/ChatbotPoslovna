"""Vector database operations using ChromaDB."""
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
from config import config


class VectorDatabase:
    """Manages vector database operations using ChromaDB."""
    
    def __init__(self):
        """Initialize the vector database."""
        self.client = chromadb.PersistentClient(
            path=config.CHROMA_DB_PATH,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=config.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(
        self,
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict]
    ):
        """
        Add documents to the vector database.
        
        Args:
            texts: List of text chunks
            embeddings: List of embedding vectors
            metadatas: List of metadata dictionaries
        """
        # Generate IDs for documents
        ids = [f"doc_{i}" for i in range(len(texts))]
        
        # Add to collection
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"Added {len(texts)} documents to vector database")
    
    def query(
        self,
        query_embedding: List[float],
        top_k: int = 3
    ) -> Dict:
        """
        Query the vector database for similar documents.
        
        Args:
            query_embedding: Embedding vector of the query
            top_k: Number of results to return
        
        Returns:
            Dictionary with query results
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        return results
    
    def clear(self):
        """Clear all documents from the collection."""
        # Delete and recreate collection
        self.client.delete_collection(name=config.COLLECTION_NAME)
        self.collection = self.client.get_or_create_collection(
            name=config.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        print("Vector database cleared")
    
    def count(self) -> int:
        """Get the number of documents in the collection."""
        return self.collection.count()
