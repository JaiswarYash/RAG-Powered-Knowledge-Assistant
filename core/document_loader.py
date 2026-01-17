import os
from typing import List
from pathlib import Path
from langchain.schema import Document
from langchain_community.document_loaders import (
    PyMuPDFLoader as PDFLoader,
    Docx2txtLoader,
    UnstructuredWordDocumentLoader,
    TextLoader
)
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

extensions_mapping = {
    ".pdf": "PDFLoader",
    ".docx": "Docx2txtLoader",
    ".doc": "UnstructuredWordDocumentLoader",
    ".txt": "TextLoader"
}

def document_loader(file_path:str) -> List[Document]:

    # check file exist or not
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return []
    
    file_path = os.path.abspath(file_path)
    filename = os.path.basename(file_path)
    file_ext = Path(file_path).suffix.lower()

    if file_ext not in extensions_mapping:
        logger.error(f"Unsupported file extension: {file_ext}")
        return []
    try:
        if file_ext == ".pdf":
            loader = PDFLoader(file_path)
        elif file_ext == ".docx":
            loader = Docx2txtLoader(file_path)
        elif file_ext == ".doc":
            loader = UnstructuredWordDocumentLoader(file_path)
        elif file_ext == ".txt":
            loader = TextLoader(file_path)
        else:
            logger.error(f"Unsupported file extension: {file_ext}")
            return []
        
        documents = loader.load()

        # add metadata
        for doc in documents:
           doc.metadata.update({
                'filename': filename,
                'filepath': file_path,
                'file_type': file_ext
            })
        logger.info(f"✓ Loaded {len(documents)} pages from {filename}")
        return documents
    
    except Exception as e:
        logger.error(f"Error loading document {filename}: {e}")
        return []

'''
if __name__ == "__main__":
    sample_file = "data/sample.pdf"  # Replace with your sample file path
    documents = document_loader(sample_file)
    if documents:
        logger.info(f"Loaded {len(documents)} documents from {sample_file}")
    else:
        logger.info("No documents loaded.")
'''