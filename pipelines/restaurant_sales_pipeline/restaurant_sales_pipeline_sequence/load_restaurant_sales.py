# Load Restaurant sales 

# Import standard python libaries
import logging 

# Third party python packages 
import pandas as pd 
import numpy as np
from sqlalchemy import text 
from sqlalchemy import IntegrityError, SQLAlchemyError 

# Import customised local modules 
from sales_data_logs.sales_data_logging_config import setup_logging 
from restaurant_sales_pipeline_sequence.config_restaurant_sales import sales_dw_engine
from restaurant_sales_pipeline_sequence.extract_restaurant_sales import run_extract_sequence 
from restaurant_sales_pipeline_sequence.transform_restaurant_sales import run_transformation

# Set up Logger 
logger = logging.getLogger(__name__)


class PrepareRestaurantSales:
    
    @staticmethod 
    def prepare_columns (dataframe, column_maps):
        """
        """
        dataframe = dataframe.copy 

        return (
            dataframe[list(column_maps.keys())]
            .drop_duplicates()
            .rename(columns = column_maps)
        )
