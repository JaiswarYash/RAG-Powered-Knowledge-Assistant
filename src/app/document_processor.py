import logging
import os
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from typing import List
import docx2txt

# define class
class DocumentProcessor:

    # define init method for chunking configuration
    def __init__(self, chunk_size: int = 560, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size= self.chunk_size,
            chunk_overlap = self.chunk_overlap,
            length_function=len
        )
        self.logger = logging.getLogger(__name__)

        self.supported_formats = {'.pdf', '.docx', '.doc'}
    
    # method to load and process .PDF and .doc files
    def load_source_file(self, file_path: str) -> str:

        # validate file path
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not os.path.isfile(file_path):
            raise ValueError(f"Not a valid file: {file_path}")
        
        # check if file format is supported
        file_ext = os.path.splitext(file_path)[1].lower()

        if file_ext not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_ext}",
                            f"Supported formats are: {self.supported_formats}")
        
        extracted_text = []
        try:
            if file_ext == '.pdf':
                extracted_text = self._extract_text_from_pdf(file_path)
            elif file_ext in {'.docx', '.doc'}:
                extracted_text = self._extract_text_from_doc(file_path)

        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {e}")
            return ""
        
        return "\n".join(extracted_text).strip()
    
    
    
        
        