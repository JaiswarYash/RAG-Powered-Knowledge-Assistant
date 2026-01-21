import os
import json
import logging
from Rag_logic import RagLogic 
from config import PERSIST_DIRECTORY
from langchain_community.vectorstores import Chroma
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
    def __init__(self, rag_logic, persist_directory: str = PERSIST_DIRECTORY):
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
            try:
                with open(self.indexed_files_path, "r") as f:
                    files = json.load(f)
                    logger.info(f" loaded indexed file form disk: {len(files)} files")
                    return set(files)
            except Exception as e:
                logger.error(f"Could not load indexed files: {e}")
        return set()

    def _save_indexed_file(self)-> None:
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
            persist_directory=self.persist_directory,
            embedding_function=self.rag_logic.get_embedding_model()
        )
        logger.info("✓ Vector store ready")
        return self.vector_store
    
    # Add document chunks to vector store
    def add_documents(self, chunks: List[Document]) -> None:
        """Add document chunks to vector store."""
        if not chunks:
            logger.warning("No chunks to add")
            return
        
        try:
            # Add to vector store
            self.vector_store.add_documents(chunks)

            # Track indexed files
            for chunk in chunks:
                file_source = chunk.metadata.get("source")
                if file_source:
                    self.indexed_files.add(file_source)

            # Save indexed files list
            self._save_indexed_file() 
            
            logger.info(f"✓ Added {len(chunks)} chunks")
            logger.info(f"  Total indexed files: {len(self.indexed_files)}")
            return True

        except Exception as e:
            logger.error(f"✗ Error adding documents: {e}")
            return False
    
    # Perform semantic search
    def search(self, query: str, top_k: int = 2,filter: Optional[Dict] = None) -> List[Document]:
        """Perform semantic search on the vector store."""
        if not self.vector_store:
            logger.error("initialized vector store")
            return []
        try:
            results = self.vector_store.similarity_search(query, k=top_k, filter=filter)
            logger.info(f"✓ Search completed: {len(results)} results for query '{query}'")
            return results
        except Exception as e:
            logger.error(f"✗ Error during search: {e}")
            return []
    
    def is_file_indexed(self, source: str) -> bool:
        """Check if a file has already been indexed."""
        return source in self.indexed_files
    
    def get_indexed_files(self) -> List[str]:
        """Get a list of all indexed files."""
        return list(self.indexed_files)
    
    def get_stats(self) -> Dict:
        """Get statistics about the vector store."""
        return {
            "total_files": len(self.indexed_files),
            "indexed_files": self.get_indexed_files(),
            "persist_directory": self.persist_directory
        }
    
    # load process_file from RagLogic and add to vector store
    
    def process_and_add_file(self, file_path: str) -> None:
        """Process a single file and add to vector store."""
        # Process file to get chunks
        chunks = self.rag_logic.process_file(file_path)
        
        if not chunks:
            logger.warning(f"No chunks from {file_path}")
            return
        
        # Check if already indexed (using metadata from chunk)
        file_source = chunks[0].metadata.get("source")
        if file_source and self.is_file_indexed(file_source):
            logger.info(f"Already indexed: {os.path.basename(file_source)}")
            return
        
        # Add to database
        self.add_documents(chunks)
    
    def process_and_add_files(self, file_paths: List[str]) -> None:
        """Process multiple files and add to vector store."""
        new_files = [fp for fp in file_paths if not self.is_file_indexed(fp)]
        
        if not new_files:
            logger.info("All files already indexed")
            return
        
        logger.info(f"Processing {len(new_files)} new files...")
        chunks = self.rag_logic.process_files(new_files)
        self.add_documents(chunks)
'''
# Example usage
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    from Rag_logic import RagLogic  # ← Import here, not at top
    
    # Initialize
    rag_logic = RagLogic()
    vector_db = VectorDB(rag_logic)
    
    # Show initial stats
    logger.info("\nInitial state:")
    logger.info(f"  {vector_db.get_stats()}")
    
    # Add a test file (change path)
    test_file = "data/sample.pdf"
    if os.path.exists(test_file):
        logger.info(f"\nAdding file: {test_file}")
        vector_db.process_and_add_file(test_file)
        
        # Show updated stats
        logger.info("\nUpdated state:")
        logger.info(f"  {vector_db.get_stats()}")
        
        # Test search
        logger.info("\nTesting search:")
        results = vector_db.search("what is AI", top_k=2)
        
        for i, doc in enumerate(results, 1):
            logger.info(f"\n--- Result {i} ---")
            logger.info(f"File: {doc.metadata.get('filename')}")
            logger.info(f"Content: {doc.page_content[:150]}...")
    else:
        logger.error(f"File not found: {test_file}")
'''