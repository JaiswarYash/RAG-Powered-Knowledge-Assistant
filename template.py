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
    f"core/__init__.py",
    f"core/document_loder.py", # document loading and processing
    f"core/Rag_logic.py"
    f"core/config.py", # configuration settings
    "data/.gitkeep",
    "notebooks/rag_experimentation.ipynb", # Jupyter notebook for experimentation
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
