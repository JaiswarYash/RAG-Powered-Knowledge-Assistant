import logging
import os
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

project_name = "app"

list_of_files = [
    # app
    "app/database.py",
    "app/db_models.py",
    "app/schemas.py",
    "app/routers.py",
    "app/utils.py",
    "app/main.py",
    # model
    "model/ReadMe.md",
    "model/artifacts/.gitkeep",
    "model/script/train_model.py",
    #notebooks
    "notebooks/Exploration.ipynb",
    "scripts/train_model.py",
    # UI
    "ui/streamlit_app.py",
    # data
    "data/README.md",
    "data/raw/.gitkeep",
    "data/processed/.gitkeep",
    # tests
    "tests/test_api.py",
    # docker
    ".dockerignore",
    "Dockerfile",
    "docker-compose.yml",
    # env & config
    ".env.example",
    ".env",
    ".gitignore",
    "requirements.txt",
    "README.md"
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
