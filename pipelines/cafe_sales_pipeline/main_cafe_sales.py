# Orchestration script 

# Import Python standard modules 
import logging 

# Import Third-party Python packages 
import pandas as pd 

# Import customised local packages 
from sales_data_logs.sales_data_logging_config import setup_logging
from cafe_sales_pipeline_sequence import config_cafe_sales as config
from cafe_sales_pipeline_sequence.extract_cafe_sales import run_extract_sequence
from cafe_sales_pipeline_sequence.transform_cafe_sales import run_transformation
from cafe_sales_pipeline_sequence.load_cafe_sales import run_load_cafe_sales

# I set up logger 
logger = logging.getLogger(__name__)


#
def run_cafe_sales_pipeline (config, cafe_sales):
    run_extract_sequence()
    run_transformation(cafe_sales)
    run_load_cafe_sales()

if __name__ == "__main__":
    setup_logging()
    run_cafe_sales_pipeline()

