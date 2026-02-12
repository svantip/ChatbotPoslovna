"""PDF processing utilities for loading and extracting text from PDF documents."""
import os
from typing import List, Dict
from pypdf import PdfReader


class PDFDocument:
    """Represents a loaded PDF document with metadata."""
    
    def __init__(self, filename: str, text: str, page_number: int):
        self.filename = filename
        self.text = text
        self.page_number = page_number
    
    def to_dict(self) -> Dict:
        """Convert to dictionary format."""
        return {
            "filename": self.filename,
            "text": self.text,
            "page_number": self.page_number
        }


class PDFLoader:
    """Loads and extracts text from PDF files."""
    
    def __init__(self, pdf_folder: str):
        """
        Initialize PDF loader.
        
        Args:
            pdf_folder: Path to folder containing PDF files
        """
        self.pdf_folder = pdf_folder
    
    def load_pdfs(self) -> List[PDFDocument]:
        """
        Load all PDF files from the specified folder.
        
        Returns:
            List of PDFDocument objects with extracted text
        """
        documents = []
        
        if not os.path.exists(self.pdf_folder):
            print(f"PDF folder does not exist: {self.pdf_folder}")
            return documents
        
        # Get all PDF files
        pdf_files = [f for f in os.listdir(self.pdf_folder) if f.endswith('.pdf')]
        
        if not pdf_files:
            print(f"No PDF files found in: {self.pdf_folder}")
            return documents
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(self.pdf_folder, pdf_file)
            
            try:
                reader = PdfReader(pdf_path)
                
                # Extract text from each page
                for page_num, page in enumerate(reader.pages, start=1):
                    text = page.extract_text()
                    
                    if text.strip():  # Only add if there's actual text
                        doc = PDFDocument(
                            filename=pdf_file,
                            text=text,
                            page_number=page_num
                        )
                        documents.append(doc)
                
                print(f"Loaded {len(reader.pages)} pages from {pdf_file}")
            
            except Exception as e:
                print(f"Error loading {pdf_file}: {e}")
        
        print(f"Total documents loaded: {len(documents)}")
        return documents
