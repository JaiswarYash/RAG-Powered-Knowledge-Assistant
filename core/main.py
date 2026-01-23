import os
import logging
from typing import List, Dict
from prompt import prompt_template
from Rag_logic import RagLogic
from vector_db import VectorDB
from config import LLM_MODEL,  GOOGLE_API_KEY
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RAGSystem:
    def __init__(self, model_name: str = LLM_MODEL):
        # Components
        self.rag_logic = RagLogic()
        self.vector_db = VectorDB(self.rag_logic)
        
        # LLM
        api_key = os.getenv(GOOGLE_API_KEY)
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not set")
        
        self.LLM = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0,
            google_api_key=api_key
        )
    
        PROMPT = ChatPromptTemplate(template=prompt_template, input_variables=["context", "question"])
        DOCUMENT_CHAIN = create_stuff_documents_chain(self.LLM,PROMPT)
        retrieval = self.vector_db.vector_store.as_retriever(search_kwargs={"k": 4})
        self.qa_chian = create_retrieval_chain(retrieval, DOCUMENT_CHAIN)
        logger.info(f"MainApp initialized with model: {model_name}")
    
    def add_documents(self, file_path: List[str]) -> None:
        '''Add documents to vector store'''
        return self.vector_db.process_and_add_file(file_path)
    
    def add_directory(self, directory_path: str, glob_pattern: str = "**/*.{pdf,docx,doc,txt}") -> None:
        '''Add all documents from a directory to vector store'''
        return self.vector_db.process_and_add_directory(directory_path, glob_pattern=glob_pattern)
    
    def ask(self, query: str) -> str:
        '''Ask a question'''
        result = self.qa_chian.invoke({"question": query})
        return result['answer']
    
    def ask_with_sources(self, query: str) -> Dict:
        '''Ask a question with sources'''
        result = self.qa_chian.invoke({"question": query})
        return {
            'answer': result['answer'],
            'sources': [
                f"{doc.metadata.get('filename', 'Unknown')}: {doc.page_content[:100]}..."
                for doc in result.get('context', [])
            ]
        }
    
    def get_stats(self) -> Dict:
        '''Get vector store stats'''
        return self.vector_db.vector_store.get_stats()
    

if __name__ == "__main__":
    rag = RAGSystem()
    
    # Example usage:
    rag.add_document("data/sample.pdf")
    answer = rag.ask("What is this document about?")
    print(answer)
    
    print(rag.stats()) 