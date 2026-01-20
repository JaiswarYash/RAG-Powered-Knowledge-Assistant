import os
from typing import List
from pathlib import Path
from document_loader import document_loader, multiple_document_loader
from langchain_text_splitters import RecursiveCharacterTextSplitter   
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RagLogic:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", chunk_size: int = 1000, chunk_overlap: int = 200,):
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

        chunk_counter = {}
        for chunk in chunks: # assign chunk ids based on source
            source = chunk.metadata.get("source","unknown") # get source from metadata, else use 'unknown'

            if source not in chunk_counter: # initialize counter for new source and assign chunk ids
                chunk_counter[source] = 0
            chunk.metadata["chunk_id"] = chunk_counter[source] 
            chunk_counter[source] += 1

        return chunks
    
    # load and split documents
    def process_file(self, file_path: str) -> List[Document]:
        """Process a single file into chunks."""
        documents = document_loader(file_path)
        
        if not documents:
            logger.warning(f"No documents loaded from {file_path}")
            return []
        
        return self.split_documents(documents)

    def process_files(self, file_paths: List[str]) -> List[Document]:
        """Process multiple files into chunks."""
        documents = multiple_document_loader(file_paths)
        
        if not documents:
            logger.warning("No documents loaded from provided files")
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