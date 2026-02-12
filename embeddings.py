"""Embeddings generation using Google Gemini API."""
from typing import List
import google.generativeai as genai
from config import config


class EmbeddingGenerator:
    """Generates embeddings using Gemini API."""
    
    def __init__(self):
        """Initialize the embedding generator."""
        if not config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set")
        
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = config.GEMINI_EMBEDDING_MODEL
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
        
        Returns:
            Embedding vector as list of floats
        """
        try:
            result = genai.embed_content(
                model=self.model,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            print(f"Error generating embedding: {e}")
            raise
    
    def generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for a query.
        
        Args:
            query: Query text to embed
        
        Returns:
            Embedding vector as list of floats
        """
        try:
            result = genai.embed_content(
                model=self.model,
                content=query,
                task_type="retrieval_query"
            )
            return result['embedding']
        except Exception as e:
            print(f"Error generating query embedding: {e}")
            raise
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
        
        Returns:
            List of embedding vectors
        """
        embeddings = []
        
        for i, text in enumerate(texts):
            if i % 10 == 0:
                print(f"Generating embedding {i+1}/{len(texts)}")
            
            embedding = self.generate_embedding(text)
            embeddings.append(embedding)
        
        return embeddings
