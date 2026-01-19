from dotenv import load_dotenv
import os

load_dotenv()

def get_config(key: str, default: str = None) -> str:
    return os.getenv(key, default)
