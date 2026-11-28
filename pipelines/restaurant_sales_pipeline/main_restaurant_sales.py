# orchestration script 

# Import python standard modules 
import logging 

# Import customised local packages 
from sales_data_logs.sales_data_logging_config import setup_logging 
from restaurant_sales_pipeline_sequence import config_restaurant_sales as config 
from restaurant_sales_pipeline_sequence.config_restaurant_sales import sales_dw_engine 
from restaurant_sales_pipeline_sequence.extract_restaurant_sales import run_extract_sequence 
from restaurant_sales_pipeline_sequence.transform_restaurant_sales import run_transformation 
from restaurant_sales_pipeline_sequence.load_restaurant_sales import run_load_restaurant_sales 

logger - logging.getLogger (__name__)



# Full pipeline 
def run_restaurant_sales_pipeline():
    restaurant_sales = run_extract_sequence()
    restaurant_sales = run_transformation (restaurant_sales)
    run_load_restaurant_sales (restaurant_sales, sales_dw_engine) 

# Script guard 
if __name__ == "__main__":
    setup_logging()
    run_restaurant_sales_pipeline()



