import os
from typing import List
from pathlib import Path
from .document_loader import multiple_documents_loader, load_from_directory
from langchain_text_splitters import RecursiveCharacterTextSplitter   
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from .config import EMBEDDING_MODEL
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RagLogic:
    def __init__(self, model_name: str = EMBEDDING_MODEL, chunk_size: int = 1000, chunk_overlap: int = 200):

        # Validate inputs
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative")
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be less than chunk_size")
        
        # Initialize text splitter and embeddings
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len)
        # Initialize HuggingFace embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name, 
            model_kwargs={"device": "cpu"}, 
            encode_kwargs={"normalize_embeddings": True})
        
        # Logging initialization details
        logger.info(f"✓ RagLogic initialized with model: {model_name}")
        logger.info(f"  Chunk size: {chunk_size}, Overlap: {chunk_overlap}")

    
    # step 1: load documents using document loader
    # step 2: split documents into fixed size chunks

    def split_documents(self, documents: List[Document]) -> List[Document]:

        if not documents:
            logger.warning("No documents to split.")
            return []

        # Split documents
        chunks = self.text_splitter.split_documents(documents)
        
        # assing chunk id per document
        chunk_id = {}
        for chunk in chunks:
            source = chunk.metadata.get('filename', 'unknown')

            if not source in chunk_id:
                chunk_id[source] = 0
            chunk.metadata['chunk_id'] = chunk_id[source]
            chunk_id[source] += 1

        logger.info(f"✓ Split into {len(chunks)} chunks from {len(documents)} document(s)")
        return chunks
    
    # load and split documents
    def process_files(self, file_paths: str | List[str], mode: str = "single") -> List[Document]:
        documents = multiple_documents_loader(file_paths, mode=mode)  # ✅ Fixed: file_paths not file_path
    
        if not documents:
            logger.warning("No documents loaded from provided files")
            return []
        
        return self.split_documents(documents)
    
    def process_file(self, file_path: str):
        return self.process_files([file_path])
        
    # batch process files from directory
    def process_directory(self, directory_path: str, glob_pattern: str = "**/*.{pdf,docx,doc,txt}", mode: str = "single") -> List[Document]:

        # validate directory path
        if not os.path.exists(directory_path):
            logger.error(f"Directory does not exit: {directory_path}")
            return []
        
        if not os.path.isdir(directory_path):
            logger.error(f"Provided path is not a directory: {directory_path}")
            return []
        
        # load documents from directory
        documents = load_from_directory(
            directory_path, 
            glob_pattern=glob_pattern,
            mode=mode
        )
        
        if not documents:
            logger.warning(f"No documents loaded from directory {directory_path}")
            return []
        
        return self.split_documents(documents)
    

    def get_embedding_model(self):  # ← singular (recommended)
        return self.embeddings

# Usage
'''
if __name__ == "__main__":
    rag = RagLogic()
    
    # Process file
    chunks = rag.process_file("data/sample.pdf")
    
    # Create embeddings
    embeddings = rag.create_embeddings(chunks)
    
    print(f"Total chunks: {len(chunks)}")
    print(f"Total embeddings: {len(embeddings)}")
'''