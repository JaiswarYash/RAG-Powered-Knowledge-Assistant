# configuration file
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
MODEL = os.getenv("MODEL", "")

data_folder = "data/"
if not os.path.exists(data_folder):
    os.makedirs(data_folder)
    