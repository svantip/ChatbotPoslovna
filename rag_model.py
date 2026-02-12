"""
Script 2: RAG Model - Similarity search + Gemini response generation.
This holds the core RAG logic.
"""
import os
import chromadb
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
TOP_K = int(os.getenv("TOP_K", "3"))


class RAGModel:
    """RAG model for Croatian chatbot."""
    
    def __init__(self):
        """Initialize the RAG model."""
        # Initialize Gemini
        if not GEMINI_API_KEY:
            raise ValueError("❌ GEMINI_API_KEY is not set in .env file")
        
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        
        # Initialize ChromaDB
        client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        self.collection = client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
        
        print(f"✓ RAG Model initialized")
        print(f"  - Gemini Model: {GEMINI_MODEL}")
        print(f"  - Documents in DB: {self.collection.count()}")
    
    def respond(self, user_query, top_k=None):
        """
        Generate response for user query using RAG.
        
        Args:
            user_query: User's question
            top_k: Number of similar chunks to retrieve
        
        Returns:
            dict with response and sources
        """
        if top_k is None:
            top_k = TOP_K
        
        # Step 1: Generate query embedding with Gemini
        query_embedding = genai.embed_content(
            model="models/text-embedding-004",
            content=user_query
        )['embedding']
        
        # Step 2: Similarity search in database
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Step 3: Extract context and sources
        context_parts = []
        sources = []
        
        if results['documents'] and results['documents'][0]:
            for i, (doc, metadata) in enumerate(zip(
                results['documents'][0],
                results['metadatas'][0]
            )):
                context_parts.append(f"[{i+1}] {doc}")
                sources.append({
                    "filename": metadata.get("filename", "Unknown"),
                    "page": metadata.get("page", "Unknown")
                })
        
        if not context_parts:
            return {
                "response": "Nisam pronašao relevantne informacije u dokumentima.",
                "sources": []
            }
        
        context = "\n\n".join(context_parts)
        
        # Step 3: Create prompt for Gemini
        prompt = f"""Ti si pomoćnik koji odgovara na pitanja na temelju dostavljenog konteksta.

Kontekst iz dokumenata:
{context}

Korisničko pitanje: {user_query}

Molim te odgovori na pitanje koristeći informacije iz konteksta. Odgovori na hrvatskom jeziku.
Ako informacija nije u kontekstu, jasno to naznači.
"""
        
        # Step 4: Generate response with Gemini
        try:
            response = self.model.generate_content(prompt)
            return {
                "response": response.text,
                "sources": sources
            }
        except Exception as e:
            return {
                "response": f"Greška pri generiranju odgovora: {str(e)}",
                "sources": sources
            }


# Test if run directly
if __name__ == "__main__":
    print("Testing RAG Model...")
    
    try:
        rag = RAGModel()
        
        test_query = "Koja je adresa tvrtke?"
        print(f"\nTest pitanje: {test_query}")
        
        result = rag.respond(test_query)
        
        print(f"\nOdgovor: {result['response']}")
        print(f"\nIzvori:")
        for source in result['sources']:
            print(f"  • {source['filename']}, stranica {source['page']}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
