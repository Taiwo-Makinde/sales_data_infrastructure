# Import standard python libaries 
import logging                                                      # For logging


# Import third party python packages 
import pandas as pd                                                  # For dataframe 
from sqlalchemy import text                                          # for the SQL database


# Import customised local packages 
from sales_data_logs.sales_data_logging_config import setup_logging  # My personalised logging module that outputs logs in single-line json format. 
from config_cafe_sales import sales_dw_engine                        # My database (data warehouse) configuration (has the details: user, password, host, port & database name)


# We set up our logger 
logger = logging.getLogger(__name__) # We use __name__ so that it correctly resolves to the module name and file name cafe_sales_pipeline_sequence + load_cafe_sales



class PrepareCafeSales:   
    def prepare_columns(dataframe, column_maps):
        """
        Generic function that 
        1. picks only the columns we need
        2. drops duplicates
        3. renames our column names to match the database name
        """
        return (
            dataframe[list(column_maps.keys())]
            .drop_duplicates()
            .rename(columns = column_mapping)
        )

    def prepare_all_dataframes (cafe_sales):
        # Dimensions
        # We call the generic column for Item
        item_df = prepare_columns (cafe_sales, column_maps = {"Item": "item_name"})

        # Payment Method 
        payment_df = prepare_columns (cafe_sales, column_maps = {"Payment Method": "payment_method_name"})

        # Location 
        location_df  = prepare_columns (cafe_sales, column_maps = {"Location" : "location_name"})

        # date 
        date_df = prepare_columns (cafe_sales, column_maps = {
            "Transaction Date" : "full_date",
            "Day of the Week" : "day_of_week",
            "Is weekend" : "is_weekend",
            "Month Number" : "month_number", 
            "Month of the Year": "month_of_year",
            "Quarter of the Year": "quarter", 
            "Year": "dateyear"
        })

        # Facts 
        # 
