# Import Python standard packages 
import os
from pathlib import Path

# Import Python third-party packages
from dotenv import load_dotenv
from sqlalchemy import create_engine


# Let's load our .env file
env_path = Path(__file__).parents[3] / "config" / "cafe.env" # Our cafe.env file is three level directory away from this file
print("env_exists:", env_path.exists())
load_dotenv(env_path)

# We are dowloading data from Kaggle so let's load our Kaggle Credentials
KAGGLE_USERNAME = os.getenv("KAGGLE_USERNAME")
KAGGLE_API_TOKEN = os.getenv("KAGGLE_API_TOKEN")

#Ingestion of the data once
CAFE_DATASET_KAGGLE = os.getenv("CAFE_DATASET_KAGGLE") # Reference to the dataset on Kaggle (author/dataset)
SALES_DATA_DOWNLOAD_PATH = os.getenv("SALES_DATA_DOWNLOAD_PATH")
CAFE_SALES_DATASET = os.getenv("CAFE_SALES_DATASET") 
# We included the empty string so that an error would not be thrown, because the first time config runs the dataset would not exist
# We would verify that the daatset exists in a different function # See extract_sales_data

# For extraction step
EXTRACT_PATH = SALES_DATA_DOWNLOAD_PATH
# We create a path for the dataset if the dataset exists or have none if it does not exist


# Pipeline behaviour
MAX_RETRIES = 3
TIMEOUT_SECONDS = 60
FILE_DOWNLOAD_FORMAT = "csv"

# For the database 

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("SALES_DATA_WAREHOUSE")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

sales_dw_engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")




