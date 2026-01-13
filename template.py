import logging
import os
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

project_name = "app"

list_of_files = [
    "app.py", # # Main Streamlit app + FastAPI server
    "requirements.txt", # Project dependencies
    ".env.example", # Example environment variables template
    ".env", # Environment variables
    "README.md", # Project documentation
    "LICENSE", # License file
    ".gitignore", # Git ignore file
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/document_processor.py", # document loading and processing
    f"src/{project_name}/vector_store.py", # vector store management
    f"src/{project_name}/retriever.py", # retrieval logic
    f"src/{project_name}/chat_engine.py", # LLM integration and chat logic
    f"src/{project_name}/config.py", # configuration settings
    f"src/{project_name}/api.py", # FastAPI endpoints
    f"src/{project_name}/utils.py", # utility functions
    "data/.gitkeep",
    "notebooks/rag_experimentation.ipynb", # Jupyter notebook for experimentation
    "tests/test_api.py",
    "tests/text_LLM.py", # Test directory
    "docs/image.png", # Documentation directory
    "chroma_db/note.txt", # Vector store database
    "dockerfile", 
    "docker-compose.yml",
    ".dockerignore",
]


for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    # Create directory if not exists
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir}")

    # Create empty file if not exists OR file is empty
    if (not os.path.exists(filepath)) or os.path.getsize(filepath) == 0:
        with open(filepath, "w") as f:
            pass
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"File already exists: {filepath}")
