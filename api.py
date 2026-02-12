"""
API - Expose RAG model via FastAPI POST endpoint.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from rag_model import RAGModel

# Initialize FastAPI
app = FastAPI(
    title="RAG Chatbot API",
    description="Croatian chatbot using RAG with Gemini",
    version="1.0.0"
)

# Initialize RAG model
try:
    rag_model = RAGModel()
except Exception as e:
    print(f"❌ Failed to initialize RAG model: {e}")
    print("Make sure to:")
    print("  1. Run setup.py first to index documents")
    print("  2. Set GEMINI_API_KEY in .env file")
    rag_model = None


# Request/Response models
class ChatRequest(BaseModel):
    """Request body for chat endpoint."""
    prompt: str
    top_k: Optional[int] = None


class Source(BaseModel):
    """Source information."""
    filename: str
    page: int


class ChatResponse(BaseModel):
    """Response body for chat endpoint."""
    response: str
    sources: List[Source]


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "RAG Chatbot API",
        "version": "1.0.0",
        "endpoint": "/chat"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Chat endpoint - POST method.

    Body:
    {
        "prompt": "Your question here",
        "top_k": 3  // optional
    }

    Returns:
    {
        "response": "Answer from Gemini",
        "sources": [{"filename": "file.pdf", "page": 1}]
    }
    """
    if rag_model is None:
        raise HTTPException(
            status_code=503,
            detail="RAG model not initialized. Check setup and environment."
        )

    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    try:
        result = rag_model.respond(request.prompt, top_k=request.top_k)
        return ChatResponse(
            response=result["response"],
            sources=[Source(**s) for s in result["sources"]]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/health")
def health():
    """Health check endpoint."""
    if rag_model is None:
        return {"status": "unhealthy", "message": "RAG model not initialized"}

    doc_count = rag_model.collection.count()
    return {
        "status": "healthy",
        "documents": doc_count,
        "model": "gemini-1.5-flash"
    }


if __name__ == "__main__":
    import uvicorn
    print("\n" + "=" * 60)
    print("Starting RAG Chatbot API Server")
    print("=" * 60)
    print("API Documentation: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/health")
    print("=" * 60 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)
