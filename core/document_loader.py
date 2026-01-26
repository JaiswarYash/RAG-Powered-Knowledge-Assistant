import os
from typing import List
from pathlib import Path
from langchain_core.documents import Document
from langchain_unstructured import UnstructuredLoader 
from langchain_community.document_loaders import DirectoryLoader
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def document_loader(file_path: str, mode: str = "single") -> List[Document]:
    """Load a single document file using Unstructured."""
    
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return []
    
    file_path = os.path.abspath(file_path)
    filename = os.path.basename(file_path)
    
    try:
        loader = UnstructuredLoader(
            file_path=file_path,
            mode=mode
        )
        documents = loader.load()
        
        # Add custom metadata
        for doc in documents:
            doc.metadata["source"] = file_path
            doc.metadata["filename"] = filename
        
        logger.info(f"✓ Loaded {len(documents)} from {filename}")
        return documents
        
    except Exception as e:
        logger.error(f"✗ Error loading {filename}: {e}")
        return []


def multiple_documents_loader(file_paths: List[str], mode: str = "single") -> List[Document]:
    """Load multiple documents."""
    
    all_documents = []
    
    logger.info(f"Loading {len(file_paths)} file(s)...")
    
    for file_path in file_paths:
        docs = document_loader(file_path, mode=mode)
        all_documents.extend(docs)
    
    logger.info(f"✓ Total documents loaded: {len(all_documents)}")
    return all_documents


def load_from_directory(
    directory_path: str,
    glob_pattern: str = "**/*",
    mode: str = "single"
) -> List[Document]:
    """Load all documents from a directory."""
    
    from langchain_community.document_loaders import DirectoryLoader
    
    if not os.path.exists(directory_path):
        logger.error(f"Directory not found: {directory_path}")
        return []
    
    try:
        loader = DirectoryLoader(
            path=directory_path,
            glob=glob_pattern,
            loader_cls=UnstructuredLoader,
            loader_kwargs={"mode": mode},
            show_progress=True,
            use_multithreading=True,
            silent_errors=True 
        )
        
        documents = loader.load()
        
        # Add filename metadata
        for doc in documents:
            if "source" in doc.metadata:
                doc.metadata["filename"] = os.path.basename(doc.metadata["source"])
        
        logger.info(f"✓ Loaded {len(documents)} documents from directory")
        return documents
        
    except Exception as e:
        logger.error(f"✗ Error loading directory: {e}")
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