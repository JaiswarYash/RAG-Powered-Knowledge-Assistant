import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Configuration variables
def get_config(key: str, default: str = None) -> str:
    return os.getenv(key, default)

# API Keys
HUGGINGFACE_API_KEY = get_config("HUGGING_FACE_API_KEY")
def get_groq_api_key():
    return st.secrets.get("GROQ_API_KEY")


# Model Configuration
EMBEDDING_MODEL = get_config("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
LLM_PROVIDER = get_config("LLM_PROVIDER", "groq")
LLM_MODEL = get_config("LLM_MODEL", "llama-3.1-8b-instant")
LLM_TEMPERATURE = 0.7

# Paths
PERSIST_DIRECTORY = get_config("PERSIST_DIRECTORY", "./chroma_db")
PDF_PATH = get_config("PDF_PATH", "./data/pdfs")

def validate_config():
    """Validate required configuration based on provider."""
    errors = []
    
    if LLM_PROVIDER == "google" and not get_groq_api_key():
        errors.append("Groq_API_KEY required for Google provider")
    elif LLM_PROVIDER == "huggingface" and not HUGGINGFACE_API_KEY:
        errors.append("HUGGINGFACE_API_KEY required for HuggingFace Embeddings provider")
    
    if not LLM_PROVIDER:
        errors.append("LLM_PROVIDER must be set")
    
    if errors:
        raise ValueError("Configuration errors:\n" + "\n".join(f"  - {e}" for e in errors))

# Run validation when config is imported
validate_config()