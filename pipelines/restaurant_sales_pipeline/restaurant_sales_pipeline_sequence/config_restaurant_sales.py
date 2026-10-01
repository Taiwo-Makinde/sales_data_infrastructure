# import Python standard library package 
import os 
from pathlib import Path

# Import Third-party packages 
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load .env file 
env_path = Path(__file__).parents[3] / "config" / "restaurant.env"
print("env_exists:", env_path.exists())
load_dotenv(env_path)

# Kaggle credentials 
KAGGLE_USERNAME = os.getenv("KAGGLE_USERNAME")
KAGGLE_API_TOKEN = os.getenv("KAGGLE_API_TOKEN")

# Details for Download
RESTAURANT_DATASET_KAGGLE = os.getenv("RESTAURANT_DATASET_KAGGLE")
SALES_DATA_DOWNLOAD_PATH = os.getenv("SALES_DATA_DOWNLOAD_PATH")

# Details for extraction
EXTRACT_PATH = SALES_DATA_DOWNLOAD_PATH
RESTAURANT_SALES_DATASET = os.getenv("RESTAURANT_SALES_DATASET")

# Pipeline Behaviour 
MAX_RETRIES = 3
TIMEOUT_SECONDS = 60
FILE_DOWNLOAD_FORMAT = "csv"

# Details for database 

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

sales_dw_engine = create_engine (f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

