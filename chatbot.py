"""RAG chatbot functionality."""
from typing import List, Dict
import google.generativeai as genai
from embeddings import EmbeddingGenerator
from vector_db import VectorDatabase
from config import config


class RAGChatbot:
    """RAG-based chatbot using Gemini."""
    
    def __init__(self):
        """Initialize the RAG chatbot."""
        if not config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set")
        
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(config.GEMINI_MODEL)
        self.embedding_generator = EmbeddingGenerator()
        self.vector_db = VectorDatabase()
    
    def retrieve_context(self, query: str, top_k: int = None) -> tuple[str, List[Dict]]:
        """
        Retrieve relevant context for a query.
        
        Args:
            query: User query
            top_k: Number of chunks to retrieve
        
        Returns:
            Tuple of (context_text, sources)
        """
        if top_k is None:
            top_k = config.TOP_K
        
        # Generate query embedding
        query_embedding = self.embedding_generator.generate_query_embedding(query)
        
        # Query vector database
        results = self.vector_db.query(query_embedding, top_k=top_k)
        
        # Extract context and sources
        context_parts = []
        sources = []
        
        if results['documents'] and results['documents'][0]:
            for i, (doc, metadata) in enumerate(zip(
                results['documents'][0],
                results['metadatas'][0]
            )):
                context_parts.append(f"[{i+1}] {doc}")
                sources.append({
                    "chunk_id": i + 1,
                    "filename": metadata.get("filename", "Unknown"),
                    "page_number": metadata.get("page_number", "Unknown")
                })
        
        context_text = "\n\n".join(context_parts)
        return context_text, sources
    
    def generate_response(self, query: str, context: str) -> str:
        """
        Generate a response using Gemini.
        
        Args:
            query: User query
            context: Retrieved context
        
        Returns:
            Generated response
        """
        prompt = f"""Ti si pomoćnik koji odgovara na pitanja na temelju dostavljenog konteksta.

Kontekst iz dokumenata:
{context}

Korisničko pitanje: {query}

Molim te odgovori na pitanje koristeći informacije iz konteksta. Odgovori na hrvatskom jeziku.
Ako informacija nije u kontekstu, jasno to naznači.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"Greška pri generiranju odgovora: {str(e)}"
    
    def chat(self, query: str, top_k: int = None) -> Dict:
        """
        Complete RAG pipeline: retrieve context and generate response.
        
        Args:
            query: User query
            top_k: Number of chunks to retrieve
        
        Returns:
            Dictionary with response and sources
        """
        # Retrieve context
        context, sources = self.retrieve_context(query, top_k)
        
        if not context:
            return {
                "response": "Nisam pronašao relevantne informacije u dokumentima.",
                "sources": []
            }
        
        # Generate response
        response = self.generate_response(query, context)
        
        return {
            "response": response,
            "sources": sources
        }
