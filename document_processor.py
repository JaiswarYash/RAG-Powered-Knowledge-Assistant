import logging
import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings
import sentence_transformers
from typing import List
from dotenv import load_dotenv
import docx2txt

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# define class
class DocumentProcessor:

    # define init method for chunking configuration
    def __init__(
        self, 
        chunk_size: int = 1000, 
        chunk_overlap: int = 200,
        api_key: str = None
    ):
        # Chunking configuration
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            separator="\n",
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len
        )
        self.api_key = api_key or os.getenv('HUGGINGFACE_API_KEY')
        self.embeddings = HuggingFaceInferenceAPIEmbeddings(
            api_key=self.api_key,
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    # method to load and process .PDF and .doc files
    def load_document_file(self, file_path: str) -> str:

        # validate file path
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not os.path.isfile(file_path):
            raise ValueError(f"Not a valid file: {file_path}")
        
        # check if file format is supported
        file_ext = os.path.splitext(file_path)[1].lower()

        if file_ext not in self.supported_formats:
            raise ValueError(
                f"Unsupported file format: {file_ext}. "
                f"Supported formats are: {', '.join(self.supported_formats)}"
            )
        
        extracted_text = []

        try:
            if file_ext == '.pdf':
                extracted_text = self._extract_text_from_pdf(file_path)
            elif file_ext in {'.docx', '.doc'}:
                extracted_text = self._extract_text_from_doc(file_path)
            elif file_ext in {'.txt', '.md'}:  # Add this!
                extracted_text = self._extract_text_from_txt(file_path)
        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {e}")
            return ""
        
        return "\n".join(extracted_text).strip()
    
    def _extract_text_from_txt(self, file_path: str) -> List[str]:

        text = []
        
        try:
            with open(file_path,'r', encoding='utf-8') as file:
                text.append(file.read())
        except UnicodeError:
            with open(file_path,'r',encoding='latin-1') as file:
                text.append(file.read())
        return text
    
    # pdf extraction
    def _extract_text_from_pdf(self, file_path: str) -> List[str]:

        text = []
        try:
            reader = PdfReader(file_path)

            for page in reader.pages:
                page_text = page.extract_text()

                if page_text.strip():
                    text.append(page_text)
            
            if not text:
                self.logger.warning(f"No text extracted from PDF: {file_path}")
        except Exception as e:
            self.logger.error(f"Error extracting text from PDF {file_path}: {e}")
        return text
    
    # .doc/.docx extraction
    def _extract_text_from_doc(self, file_path: str) -> List[str]:

        text = []

        try:
            content = docx2txt.process(file_path)
            
            if content.strip():
                text.append(content)
            else:
                self.logger.warning(f"No text extracted from document: {file_path}")
                
        except Exception as e:
            self.logger.error(f"Error extracting text from {file_path}: {e}")
            return []
        return text
    
    # chunking
    def chunk_document(self, text: str, source_file: str = None) -> List[dict]:

        if not text or not text.strip():
            self.logger.warning(f"Empty text provided for chunking")
            return []
        
        chunks_doc = []

        chunks = self.text_splitter.split_text(text)

        for i, chunk in enumerate(chunks):
            chunks_doc.append({
                'content': chunk,
                'source': source_file if source_file else 'unknown',
                'chunk_id': i,
                'chunk_len': len(chunks)
            })
        self.logger.info(f"Created {len(chunks_doc)} chunks from document")
        return chunks_doc
    
    # embedding
    def create_embedding(self, chunks_doc: List[dict]) -> List[dict]:
        
        if not chunks_doc:
            self.logger.warning(f'No chunks provided for embedding')
            return []
        
        try:
            text = [chunk['content'] for chunk in chunks_doc]

            embeddings = self.embeddings.embed_documents(text)

            for chunk, embedding in zip(embeddings):
                chunk['embedding'] = embedding
            
            self.logger.info(f"Successfully created {len(embeddings)} embeddings")
            return chunks_doc
        except Exception as e:
            self.logger.error(f'Error creating Embedding:{e}')
            return []
        