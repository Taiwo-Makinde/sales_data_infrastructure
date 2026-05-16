# Import Python Standard Packages
import os 
import sys 
import json
import subprocess
import importlib

#Import third-party python packages 
import pandas as pd



# Import local customised packages 
from cafe_sales_pipeline_sequence import config_cafe_sales as config

#The first step is to download the data from Kaggle. this should happen once. 
def download_kaggle_dataset(retries=config.MAX_RETRIES):

    # 1.1 Check if we already have the file downloaded. 
    # We want to make sure that if we rerun the pipeline it does not redownload the file
    cafe_sales_file_path= os.path.join(config.SALES_DATA_DOWNLOAD_PATH, config.CAFE_SALES_DATASET)
    if os.path.exists(cafe_sales_file_path):
        print(f"cafe Sales Dataset already exists at '{cafe_sales_file_path}'. Skipping.")
        return True # Stops here. Signals success
    
    # If the file does not exist, we attempt to download the file from Kaggle

    # 1.2 Validate Kaggle credentials first before doing anything else 
    if not config.KAGGLE_USERNAME or not config.KAGGLE_API_TOKEN:
        print ("Missing KAGGLE_USERNAME or KAGGLE_API_KEY in cafe.env")
        return False # Stops here. Signals failure.

    # 1.3
    # We use importlib because importlib bypasses importerror to check if a package is available. 
    # Why are we bypassing import error? because there are several reasons why import error can be thrown.
    # Because import error occurs due to any missing dependencies, import error could still occur when kaggle is installed.
    # 1.3.1 We check if kaggle is installed using importlib (import library).
    if importlib.util.find_spec("kaggle") is None: #kaggle is third-party Python package for accessing kaggle features locally
        print("kaggle not found")
        # 1st Attempt - Normal 
        try: 
            print("Installing Kaggle...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "kaggle", "-q"]) 
        except subprocess.CalledProcessError as e:
            print("Installation of Kaggle failed {e}. Proceeding to install Kaggle without dependencies...")
            # 2nd Attempt - No dep installation as last resort
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "kaggle", "-q", "--no-deps"])
            except subprocess.CalledProcessError as f:
                print("installation without dependencies failed.")
                return False
            else:
                    print("Kaggle succesfully installed with no dependencies.")
            finally:
                    print("No-dep install attempt completed.")
        else: 
            print("kaggle fully installed, with all dependencies.")
        finally:
            print("Our installation attempt completed.")
        # After installatiomn attempt, we try to import kaggle 
        # This code tries to import kaggle and if it fails tells us that there could be several reasons why this failed
        try:
            import kaggle
        except ImportError:
            print("Our importation attempt failed after our installation attempt was completed. Could be due to several reasons.")
            return False # Stops. Signals failure. Don't move forward
        else:
            print("kaggle was imported successfully after our installation attempt.")

    # 1.3.2 This block runs if kaggle can be found. It tries to import kaggle
    else:
        try:
            import kaggle
        except ImportError:
            print("kaggle is installed but there is an import error." 
            "\nPlease check the folder stipulated in VsCode workspace as the first step in troubleshooting")
            return False # Stops here. Signals failure
        else:
            print("Kaggle was installed earlier. Kaggle is imported successfully")
        
    # At this point, we can say that Kaggle should have been imported so we should start preparing to download the data
        
    # 1.4 We set credentails as environment variables (no file written to disk)
    os.environ["KAGGLE_USERNAME"] = config.KAGGLE_USERNAME
    os.environ["KAGGLE_API_TOKEN"] = config.KAGGLE_API_TOKEN

    # 1.5 We download with retries
    os.makedirs(config.SALES_DATA_DOWNLOAD_PATH, exist_ok = True)
    for attempt in range(1, retries + 1):
        try: 
            print(f"Attempt {attempt} / {retries} - Downloading '{config.CAFE_DATASET_KAGGLE}'")
            import kaggle
            kaggle.api.authenticate()
            kaggle.api.dataset_download_files (
            config.CAFE_DATASET_KAGGLE,
            path = config.SALES_DATA_DOWNLOAD_PATH,
            unzip = True
            ) 
            print(f"Attempt {attempt} failed. Retrying...") # Codes reruns because of the loop
        except Exception as e:
            print(f"Download failed : {type(e).__name__}: {e}")
            raise
        else:
            print(f"Download complete. Files saved to: {config.SALES_DATA_DOWNLOAD_PATH}")



    print("All retries failed.")
    return False # Stops here. Signals failure
    

def extract():
    # 1. We check if the file exists using the file path
    cafe_sales_file_path= os.path.join(config.EXTRACT_PATH, config.CAFE_SALES_DATASET)
    if not os.path.exists(cafe_sales_file_path):
        print(f"Cafe Sales Dataset not found : {cafe_sales_file_path}. ")
        return None # Stops here. Signals failure.
    # File exists. Safe to read
    print("Starting extraction...")
    print(f"Reading dataset from {cafe_sales_file_path}...")

    cafe_sales = pd.read_csv(cafe_sales_file_path)
    print(f"Dataset extracted successfully")

    return cafe_sales # dataframe which would becoming parameter for all our functions in transform_cafe_sales.py
    
    

# Run extraction pipeline
if __name__ == "__main__":
    print("Starting Download step and Extraction step...")

    if download_kaggle_dataset(): # This runs first
        cafe_sales = extract()     # This only returns if the first function, in this case download function, succeeded
        if cafe_sales is not None:
            print(f"\nExtract sequence complete. Dataset is ready for Transform sequence.")
        else:
            print("\nExtraction failed.")
    else: 
        print("\nDownload failed. Skipping extraction.")

