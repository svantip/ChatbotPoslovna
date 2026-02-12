"""Document indexing functionality."""
from pdf_loader import PDFLoader
from text_chunker import TextChunker
from embeddings import EmbeddingGenerator
from vector_db import VectorDatabase
from config import config


class DocumentIndexer:
    """Indexes PDF documents into the vector database."""
    
    def __init__(self):
        """Initialize the document indexer."""
        self.pdf_loader = PDFLoader(config.PDF_FOLDER_PATH)
        self.chunker = TextChunker(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )
        self.embedding_generator = EmbeddingGenerator()
        self.vector_db = VectorDatabase()
    
    def index_documents(self, clear_existing: bool = False):
        """
        Index all PDF documents.
        
        Args:
            clear_existing: Whether to clear existing documents before indexing
        """
        print("Starting document indexing...")
        
        # Clear existing documents if requested
        if clear_existing:
            print("Clearing existing documents...")
            self.vector_db.clear()
        
        # Load PDFs
        print("Loading PDF documents...")
        documents = self.pdf_loader.load_pdfs()
        
        if not documents:
            print("No documents to index")
            return
        
        # Chunk documents
        print("Chunking documents...")
        chunks = self.chunker.chunk_documents(documents)
        
        if not chunks:
            print("No chunks created")
            return
        
        # Extract texts and metadata
        texts = [chunk.text for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        
        # Generate embeddings
        print("Generating embeddings...")
        embeddings = self.embedding_generator.generate_embeddings_batch(texts)
        
        # Add to vector database
        print("Adding to vector database...")
        self.vector_db.add_documents(texts, embeddings, metadatas)
        
        print(f"Indexing complete! Total documents in DB: {self.vector_db.count()}")
    
    def get_document_count(self) -> int:
        """Get the number of indexed documents."""
        return self.vector_db.count()


if __name__ == "__main__":
    # Run indexing if executed directly
    import os
    
    # Create PDFs directory if it doesn't exist
    os.makedirs(config.PDF_FOLDER_PATH, exist_ok=True)
    
    indexer = DocumentIndexer()
    indexer.index_documents(clear_existing=True)
