# Import standard python packages 
import os 
import sys
import json 
import subprocess 
import importlib.util 
import logging 

# Import third party python languages 
import pandas as pd 

# Import local customised packages
from restaurant_sales_pipeline import config_restaurant_sales as config 
from sales_data_logs.sales_data_logging_config import setup_logging                                             # personalised module that outputs logs in single-line json format 

# Set up the logger 
logger = logging.getLogger(__name__)                                                                            # __name__ should resolve to the modules name

# Extraction 
# Download the data 

def download_kaggle_dataset(retries = config.MAX_RETRIES):

    # 1.1 Check if we have the file already in our local directory 
    restaurant_sales_file_path = os.path.join (config.SALES_DATA_DOWNLOAD_PATH, config.RESTAURANT_SALES_DATASET)
    if os.path.exists (restaurant_sales_path):
        logger.info(f"Restaurant Sales Dataset already exists at '{restaurant_sales_file_path}'. Skipping....")
        return True                                                                                               # The function would signal success and end here if the above confitions are met. 
    

    # 1.2 If the file does not exist 
    # I validate the kaggle credentaisl before doing anything else 
    if not config.KAGGLE_USERNAME or not config.KAGGLE_API_TOKEN:
        logger.error("Missing KAGGLE_USERNAME or KAGGLE_API_TOKEN in environment variab;le file. Please fix.")
        return False                                                                                              # The function would signal failure and stop here if the above condition is satisfied (no kaggle api token or username is valiable )

    # 1.3 set credentials to environment vairable. 
    os.environ["KAGGLE_USERNAME"] = config.KAGGLE_USERNAME
    os.environ["KAGGLE_API_TOKEN"] = config.KAGGLE_API_TOKEN

    # 1.4 I check if kaggle ispath of the import. if it isn't, I try to install it 
    if importlib.util.find_spac("kaggle") is None:
        logger.warning("kaggle not found")
        # 1st Attempt 
        try:
            logger.info("installing Kaggle...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "kaggle", "-q"])

            logger.info("Successfully installed Kaggle with all its dependencies.")

        except subprocess.CalledProcessError as e:
            logger.exception (f"Failed to install Kaggle with dependencies: {e} Attempting to install Kaggle without dependencies...")

            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "kaggle", "-q", "--no-deps"])
                logger.info("Successfully installed Kaggle without dependies.")
            except subprocess.CalledProcessError as g:
                raise logger.exception (f"Failed to install Kagg;e without dependencies: {g}")

        try:
            import kaggle 
            logger.info("Kaggle is succesfully imported after installation.")
        except Exception as e:
            raise logger.exception (f"Failed to import kaggle after succesfully installing Kaggle: {e}.")

    # 1.4.2 Kaggle can be found in the import library 
    else:
        try:
            import kaggle 

            logger.info("kaggle is available in the import library. Kaggle is succesfully imported.")
        except Exception as e:
            raise logger.exception(f"Kaggle is available in the import library. But there is an import error. 
            As the first step in trouble shooting, please check the folder stipulated in Vscode workspace.")

    # 1.5 We download with retries 
    os.makedirs(config.SALES_DATA_DOWNLOAD_PATH, exist_ok = True)

    for attempt in range (1, retries + 1):
        if os.path.exists(restaurant_sales_file_path):
            logger.info(f"File already exists at: '{config.SALES_DATA_DOWNLOAD_PATH}'")
            break

        try:
            logger.info(f"Attempt {attempt} / {retries} - Dowbloading '{config.RESTAURANT_DATASET_KAGGLE}'") 
            import kaggle
            kaggle.api.authenticate()
            kaggle.api.dataset_download_files(config.RESTAURANT_DATASET_KAGGLE, path = config.SALES_DATA_DOWNLOAD_PATH, unzip = True)

        except Exception as e:
            logger.exception (f"Attempt {attempt} failed : {type{e}.__name__} : {e}")

        # diagnostic for failed downloads and the commencement of another attempt. 
        if not os.path.exists(restaurant_sales_file_path):
            logger.warning(f"Attempt {attempt} failed. Retrying...")                                                                # The script would rerun based on the loop

        # Break if the download is complete 
        if os.path.exists(restaurant_sales_file_path):
            logger.info(f"Download complete. Files saved to : '{config.SALES_DATA_DOWNLOAD_PATH}'")
            break

    # When all the attempts have been completed. We check if the file now exists. 
    if not os.path.exists(restaurant_sales_file_path):
        raise logger.error(f"All attempt to download {config.RESTAURANT_DATASET_KAGGLE} failed.")

    return True 


def extract():
    # 1. We confirm whether the file exists at the file path
    restaurant_sales_file_path = os.path.join (config.EXTRACT_PATH, config.RESTAURANT_SALES_DATASET) 
    if not os.path.exists(restaurant_sales_file_path):
        logger.error(f"Restaurant Sales Dataset not found :  '{restaurant_sales_file_path}' does not exist")
        return None                                                                                         # We return None so that the function sigals failaure and stops and also the run_extract_sequence() does not run

    logger.info("Starting extraction...")
    logger.info(f"Reading dataset  from {restaurant_sales_file_path}...")

    restaurant_sales = pd.read_csv(cafe_sales_file_path)
    logger.info(f"Dataset extracted successfully...")

    return restaurant_sales                                                                                 # The dataframe would become the parameter for our transformations . 


def run_extract_sequence() -> pd.DataFrame:
    logger.info("Starting Downbload Step and Extraction Step...")

    if download_kaggle_dataset():                                                                           # This runs first 
        restaurant_sales = extract()                                                                        # If the above is successfully, this runs next.  

    
        if restaurant_sales is not None:
            logger.info(f"Extraction sequence complete. Dataset is ready for transofrmation sequence.")
            return restaurant_sales

        else:
            logger.error("\nExtraction failed.")
            raise FileNotFoundError
    
    else:
        logger.error("\nDownload failed...")
        raise RuntimeError

# Script guard (This controls when the code runs, helping us ensure the code runs if we call it directly.)

if __name__ == "__main__":
    setup_logging()
    run_extract_sequence()





    



        
            



