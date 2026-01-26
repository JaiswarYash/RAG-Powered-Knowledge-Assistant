import os
import json
import logging
from .rag_logic import RagLogic
from .config import PERSIST_DIRECTORY
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_core.documents import Document
from typing import List, Optional, Dict

logger = logging.getLogger(__name__)

'''
1. Load or create persistent vector store
2. load chunks from RagLogic
3. Add new document chunks to vector store
4. Save vector store
5. Perform semantic similarity search on query
6. Return relevant document chunks
'''
class VectorDB:

    # Initialize VectorDB with RagLogic instance
    def __init__(self, rag_logic: RagLogic, persist_directory: str = PERSIST_DIRECTORY):
        self.rag_logic = rag_logic
        self.persist_directory = persist_directory
        self.vector_store = None
        self.indexed_files_path = os.path.join(persist_directory, "indexed_files.json")
        
        # Create persist directory if needed
        os.makedirs(persist_directory, exist_ok=True)
        
        # Load indexed files from disk
        self.indexed_files = self._load_indexed_files()
        
        self.load_vector_store()
        logger.info(f"✓ VectorDB initialized with persist directory: {persist_directory}")
    
    def _load_indexed_files(self) -> set:
        if os.path.exists(self.indexed_files_path):
            '''Load the list of indexed file from disk'''
            try:
                with open(self.indexed_files_path, "r") as f:
                    files = json.load(f)
                    logger.info(f" loaded indexed file form disk: {len(files)} files")
                    return set(files)
            except Exception as e:
                logger.error(f"Could not load indexed files: {e}")
        return set()

    def _save_indexed_files(self)-> None:
        '''Save list of indexed_file from disk'''
        try:
            with open(self.indexed_files_path, "w") as f:
                json.dump(list(self.indexed_files), f, indent = 2)
                logger.info(f"✓ Saved indexed files to disk: {len(self.indexed_files)} files")
        except Exception as e:
            logger.error(f"Could not save indexed files: {e}")
    
    # Create or load Chroma vector store
    def load_vector_store(self) -> Chroma:
        """Load or create the Chroma vector store."""
        self.vector_store = Chroma(
            collection_name="example_collection",
            embedding_function=self.rag_logic.get_embedding_model()
        )
        logger.info("✓ Vector store ready")
        return self.vector_store
    
    # Add document chunks to vector store
    def add_documents(self, chunks: List[Document]) -> bool:
        """Add document chunks to vector store in batches."""
        if not chunks:
            logger.warning("No chunks to add")
            return False
    
        try:
            # Filter complex metadata (coordinates, layouts, etc.)
            logger.info("Filtering complex metadata...")
            chunks = filter_complex_metadata(chunks)
            
            # Chroma batch size limit
            BATCH_SIZE = 5000
            
            # Add in batches
            total_chunks = len(chunks)
            num_batches = (total_chunks + BATCH_SIZE - 1) // BATCH_SIZE
            
            logger.info(f"Adding {total_chunks} chunks in {num_batches} batch(es)...")
            
            for i in range(0, total_chunks, BATCH_SIZE):
                batch = chunks[i:i + BATCH_SIZE]
                batch_num = i // BATCH_SIZE + 1
                
                logger.info(f"  Processing batch {batch_num}/{num_batches} ({len(batch)} chunks)")
                
                # Add batch to vector store
                self.vector_store.add_documents(batch)
            
            # Track indexed files
            for chunk in chunks:
                file_source = chunk.metadata.get("source")
                if file_source:
                    self.indexed_files.add(file_source)
            
            # Save indexed files list
            self._save_indexed_files()
            
            logger.info(f"✓ Successfully added {total_chunks} chunks")
            logger.info(f"  Total indexed files: {len(self.indexed_files)}")
            return True
        
        except Exception as e:
            logger.error(f"✗ Error adding documents: {e}")
            return False
        
    # Perform semantic search
    def search(self, query: str, top_k: int = 3,filter: Optional[Dict] = None) -> List[Document]:
        """Perform semantic search on the vector store."""
        if not self.vector_store:
            logger.error("Vector store not initialized")
            return []
        try:
            results = self.vector_store.similarity_search(query, k=top_k, filter = filter)
            logger.info(f"✓ Found {len(results)} results for '{query}'")
            return results
        except Exception as e:
            logger.error(f"✗ Error during search: {e}")
            return []
        
    def is_file_indexed(self, source: str) -> bool:
        """Check if a file has already been indexed."""
        abs_source = os.path.abspath(source)
        return abs_source in self.indexed_files
    
    def get_indexed_files(self) -> List[str]:
        """Get a list of all indexed files."""
        return list(self.indexed_files)
    
    def get_stats(self) -> Dict:
        """Get statistics about the vector store."""
        total_chunks = 0
        try:
            if self.vector_store and self.vector_store._collection:
                total_chunks = self.vector_store._collection.count
        except Exception as e:
            logger.error('Could not get chunk count: {e}')
        return {
            "total_files": len(self.indexed_files),
            "total_chunks": total_chunks,
            "indexed_files": self.get_indexed_files(),
            "persist_directory": self.persist_directory
        }
    
    # load process_file from RagLogic and add to vector store
    
    def process_and_add_file(self, file_path: str) -> bool:
        """Process a single file and add to vector store."""
        # Process file to get chunks
        file_path = os.path.abspath(file_path)

        if self.is_file_indexed(file_path):
            logger.warning(f"Already indexed: {os.path.basename(file_path)}")
            return False
        
        chunks = self.rag_logic.process_file(file_path)

        if not chunks:
            logger.warning(f"No chunks from {file_path}")
            return False
        
        return self.add_documents(chunks)
    
    def process_and_add_files(self, file_paths: List[str]) -> bool:
        """Process multiple files and add to vector store."""
        file_paths = [os.path.abspath(fp) for fp in file_paths]
        new_files = [fp for fp in file_paths if not self.is_file_indexed(fp)]
        
        if not new_files:
            logger.info("All files already indexed")
            return True
        
        logger.info(f"Processing {len(new_files)} new file(s)...")
        chunks = self.rag_logic.process_files(new_files)
        return self.add_documents(chunks)
    
    def process_and_add_directory(self, directory_path: str, glob_pattern: str = "**/*.{pdf,docx,doc,txt}") -> None:

        documents = self.rag_logic.load_from_directory(directory_path, glob_pattern=glob_pattern)

        if not documents:
            logger.warning(f"No documents loaded from directory {directory_path}")
            return []
        
        # Filter out already indexed files
        new_documents = [doc for doc in documents if not self.is_file_indexed(doc.metadata.get("source", ""))]

        if not new_documents:
            logger.info("All files in directory already indexed")
            return []
        logger.info(f"Processing {len(new_documents)} new documents from directory...")

        chunks = self.rag_logic.split_documents(new_documents)
        self.add_documents(chunks)
