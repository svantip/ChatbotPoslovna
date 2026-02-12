"""FastAPI application for RAG chatbot."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from chatbot import RAGChatbot
from indexer import DocumentIndexer
from config import config


app = FastAPI(
    title="RAG Chatbot - Poslovni Asistent",
    description="RAG chatbot koji koristi Gemini za odgovaranje na pitanja iz PDF dokumenata",
    version="1.0.0"
)

# Initialize chatbot
chatbot = RAGChatbot()
indexer = DocumentIndexer()


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    query: str
    top_k: Optional[int] = None


class Source(BaseModel):
    """Source information model."""
    chunk_id: int
    filename: str
    page_number: int


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str
    sources: List[Source]


class IndexRequest(BaseModel):
    """Request model for indexing endpoint."""
    clear_existing: bool = False


class StatusResponse(BaseModel):
    """Response model for status endpoint."""
    status: str
    document_count: int
    config: Dict


@app.get("/", tags=["Status"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "RAG Chatbot API - Poslovni Asistent",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat",
            "index": "/index",
            "status": "/status"
        }
    }


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Chat endpoint for asking questions.
    
    Args:
        request: ChatRequest with query and optional top_k
    
    Returns:
        ChatResponse with answer and sources
    """
    try:
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        result = chatbot.chat(request.query, top_k=request.top_k)
        
        return ChatResponse(
            response=result["response"],
            sources=[Source(**source) for source in result["sources"]]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.post("/index", tags=["Indexing"])
async def index_documents(request: IndexRequest = IndexRequest()):
    """
    Index PDF documents from the configured folder.
    
    Args:
        request: IndexRequest with optional clear_existing flag
    
    Returns:
        Status message
    """
    try:
        indexer.index_documents(clear_existing=request.clear_existing)
        count = indexer.get_document_count()
        
        return {
            "message": "Indexing completed successfully",
            "document_count": count
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error indexing documents: {str(e)}")


@app.get("/status", response_model=StatusResponse, tags=["Status"])
async def get_status():
    """
    Get system status and configuration.
    
    Returns:
        StatusResponse with system information
    """
    try:
        count = indexer.get_document_count()
        
        return StatusResponse(
            status="operational",
            document_count=count,
            config={
                "chunk_size": config.CHUNK_SIZE,
                "chunk_overlap": config.CHUNK_OVERLAP,
                "top_k": config.TOP_K,
                "pdf_folder": config.PDF_FOLDER_PATH,
                "model": config.GEMINI_MODEL
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting status: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
