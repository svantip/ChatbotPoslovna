"""
Script 1: Setup - Parse PDFs, chunk text, embed, and store in database.
Run this once to index all your PDF documents.
"""
import os
from pypdf import PdfReader
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
PDF_FOLDER = os.getenv("PDF_FOLDER_PATH", "./pdfs")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "paraphrase-multilingual-MiniLM-L12-v2")


def load_pdfs(pdf_folder):
    """Load and extract text from all PDFs in folder."""
    documents = []
    
    if not os.path.exists(pdf_folder):
        print(f"❌ PDF folder not found: {pdf_folder}")
        return documents
    
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    
    if not pdf_files:
        print(f"❌ No PDF files found in: {pdf_folder}")
        return documents
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_folder, pdf_file)
        try:
            reader = PdfReader(pdf_path)
            for page_num, page in enumerate(reader.pages, start=1):
                text = page.extract_text()
                if text.strip():
                    documents.append({
                        "text": text,
                        "filename": pdf_file,
                        "page": page_num
                    })
            print(f"✓ Loaded {len(reader.pages)} pages from {pdf_file}")
        except Exception as e:
            print(f"❌ Error loading {pdf_file}: {e}")
    
    return documents


def chunk_text(documents, chunk_size, chunk_overlap):
    """Split documents into chunks with overlap."""
    chunks = []
    step = chunk_size - chunk_overlap
    
    for doc in documents:
        text = doc["text"]
        for i in range(0, len(text), step):
            chunk_text = text[i:i + chunk_size].strip()
            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "filename": doc["filename"],
                    "page": doc["page"]
                })
            if i + chunk_size >= len(text):
                break
    
    return chunks


def store_in_database(chunks, db_path):
    """Store chunks in ChromaDB with embeddings from multilingual model."""
    # Load embedding model
    print(f"Loading embedding model: {EMBEDDING_MODEL}")
    embedding_model = SentenceTransformer(EMBEDDING_MODEL)
    print("✓ Embedding model loaded")
    
    # Initialize ChromaDB client
    client = chromadb.PersistentClient(path=db_path)
    
    # Delete existing collection if it exists
    try:
        client.delete_collection("documents")
    except:
        pass
    
    # Create new collection without embedding function (we'll provide embeddings)
    collection = client.create_collection(
        name="documents",
        metadata={"hnsw:space": "cosine"}
    )
    
    # Prepare data
    texts = [chunk["text"] for chunk in chunks]
    metadatas = [{"filename": chunk["filename"], "page": chunk["page"]} for chunk in chunks]
    ids = [f"chunk_{i}" for i in range(len(chunks))}
    
    # Generate embeddings with multilingual model
    print(f"Generating embeddings with {EMBEDDING_MODEL}...")
    embeddings = embedding_model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    
    # Convert to list format for ChromaDB
    embeddings_list = [emb.tolist() for emb in embeddings]
    
    # Add to collection with embeddings
    collection.add(
        documents=texts,
        embeddings=embeddings_list,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"✓ Stored {len(chunks)} chunks in database")


def main():
    """Main setup function."""
    print("=" * 60)
    print("PDF INDEXING - Setup")
    print("=" * 60)
    
    # Step 1: Load PDFs
    print("\n[1/3] Loading PDF documents...")
    documents = load_pdfs(PDF_FOLDER)
    if not documents:
        print("❌ No documents to process. Exiting.")
        return
    print(f"✓ Loaded {len(documents)} pages total")
    
    # Step 2: Chunk text
    print("\n[2/3] Chunking text...")
    chunks = chunk_text(documents, CHUNK_SIZE, CHUNK_OVERLAP)
    print(f"✓ Created {len(chunks)} chunks")
    
    # Show chunks per file
    files_count = {}
    for chunk in chunks:
        files_count[chunk["filename"]] = files_count.get(chunk["filename"], 0) + 1
    print("\nChunks per file:")
    for filename, count in sorted(files_count.items()):
        print(f"  • {filename}: {count} chunks")
    
    # Step 3: Store in database
    print("\n[3/3] Storing in database...")
    store_in_database(chunks, CHROMA_DB_PATH)
    
    print("\n" + "=" * 60)
    print("✅ Setup complete! Database is ready.")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Set GEMINI_API_KEY in .env file (for response generation)")
    print("  2. Run: python api.py (for API server)")
    print("  3. Run: streamlit run app.py (for UI)")


if __name__ == "__main__":
    main()
