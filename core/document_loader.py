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

def document_loader(file_path:str, mode: str = "single") -> List[Document]:
    
    # check file exist or not
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return []
    
    # Convert to absolute path
    file_path = os.path.abspath(file_path)
    filename = os.path.basename(file_path)
    file_type = Path(file_path).suffix.lstrip(".")

    try:
        loader = UnstructuredLoader(file_path,mode=mode)

        documents = loader.load()

        # add metadata
        for doc in documents:
            doc.metadata.update({
                "source": file_path,
                "filename": filename,
                "file_type": file_type
            })
        logger.info(f"✓ Loaded {len(documents)} document(s) from {filename}")
        return documents
    
    except Exception as e:
        logger.error(f"Error loading document {file_path}: {e}")
        return []

# mutiple documents loader
def multiple_documents_loader(file_paths:str, mode: str = "single")-> List[Document]:

    all_documents = []

    for file_path in file_paths:
        docs = document_loader(file_path, mode=mode)
        all_documents.extend(docs)
    logger.info(f"✓ Total documents loaded: {len(all_documents)}")
    return all_documents

# for batch processing of files in a directory
def load_from_directory(directory_path: str, glob_pattern: str = "**/*.{pdf,docx,doc,txt}") -> List[Document]:
    try:
        loader = DirectoryLoader(
            path=directory_path,
            glob=glob_pattern, # pattern to match files
            loader_cls=UnstructuredLoader, # specify the loader class
            show_progress=True, # to show loading progress
            silent_errors=True # to skip files that cause errors
        )
        documents = loader.load()

        # add metadata
        for doc in documents:
            file_path = doc.metadata.get("source", "unknown")
            filename = os.path.basename(file_path)
            file_type = Path(file_path).suffix.lstrip(".") or "unknown"
            doc.metadata.update({
                "filename": filename,
                "file_type": file_type,
                "source": file_path
            })

        logger.info(f"✓ Loaded {len(documents)} document(s)")
        return documents
    
    except Exception as e:
        logger.error(f"Error loading documents from directory {directory_path}: {e}")
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