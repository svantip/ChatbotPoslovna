"""Text chunking utilities for splitting documents into smaller pieces."""
from typing import List, Dict


class TextChunk:
    """Represents a text chunk with metadata."""
    
    def __init__(self, text: str, metadata: Dict):
        self.text = text
        self.metadata = metadata
    
    def to_dict(self) -> Dict:
        """Convert to dictionary format."""
        return {
            "text": self.text,
            "metadata": self.metadata
        }


class TextChunker:
    """Splits text into overlapping chunks."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize text chunker.
        
        Args:
            chunk_size: Maximum size of each chunk in characters
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_text(self, text: str, metadata: Dict) -> List[TextChunk]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Text to split
            metadata: Metadata to attach to each chunk
        
        Returns:
            List of TextChunk objects
        """
        chunks = []
        
        if not text.strip():
            return chunks
        
        # Calculate step size
        step = self.chunk_size - self.chunk_overlap
        
        # Split text into chunks
        for i in range(0, len(text), step):
            chunk_text = text[i:i + self.chunk_size]
            
            if chunk_text.strip():
                chunk = TextChunk(
                    text=chunk_text.strip(),
                    metadata=metadata.copy()
                )
                chunks.append(chunk)
            
            # If we've reached the end, break
            if i + self.chunk_size >= len(text):
                break
        
        return chunks
    
    def chunk_documents(self, documents: List) -> List[TextChunk]:
        """
        Chunk multiple documents.
        
        Args:
            documents: List of PDFDocument objects
        
        Returns:
            List of TextChunk objects
        """
        all_chunks = []
        
        for doc in documents:
            metadata = {
                "filename": doc.filename,
                "page_number": doc.page_number
            }
            
            chunks = self.chunk_text(doc.text, metadata)
            all_chunks.extend(chunks)
        
        print(f"Created {len(all_chunks)} chunks from {len(documents)} documents")
        return all_chunks
