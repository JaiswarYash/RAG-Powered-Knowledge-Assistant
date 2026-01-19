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

        # using build-in text splitter for splitting documents into chunks and preseving metadata
        chunks = self.text_splitter.split_documents(documents)

        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_id"] = i
        logger.info(f"✓ Split {len(documents)} documents into {len(chunks)} chunks.")
        return chunks
    
    # load and split documents
    def process_file(self, file_path: str) -> List[Document]:
        
        # load documents
        documents = document_loader(file_path)

        if not documents:
            logger.warning(f"No documents loaded from {file_path}.")
            return []
        # split documents into chunks
        chunks = self.split_documents(documents)
        return chunks
    
    # load and split multiple documents
    def process_files(self, file_path: List[str]) -> List[Document]:

        # load multiple documents
        documents = multiple_document_loader(file_path)

        if not documents:
            logger.warning("No documents loaded from the provided file paths.")
            return []
        # split documents into chunks
        chunks = self.split_documents(documents)
        return chunks

    def create_embeddings(self, chunks: List[Document]) -> List[List[float]]:
        if not chunks:
            logger.warning("No chunks provided for embedding.")
            return []
        texts = [chunk.page_content for chunk in chunks]

        try:
            logger.info(f"Creating embeddings for {len(texts)} text(s)...")
            
            embeddings = self.embeddings.embed_documents(texts)
            logger.info(f"✓ Created {len(embeddings)} embeddings")
            return embeddings
        except Exception as e:
            logger.error(f"Error creating embeddings: {e}")
            return []

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