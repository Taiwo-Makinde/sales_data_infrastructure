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

    @staticmethod
    def prepare_items(restaurant_sales: pd.DataFrame) -> pd.DataFrame:
        """
        """
        try:
            item_df = PrepareRestaurantSales.prepare_columns(restaurant_sales, column_maps = {"Item": "item_name"})
            logger.info("Successfully built Restaurant Sales data to be loaded into item dimension table.")
        except Exception as e:
            logger.exception (f"Failed to build restaurant_sales data to bew loaded into item dimension table: {e}")
            raise 

        return item_df 

    @staticmethod
    def prepare_date (restaurant_sales : pd.DataFrame) -> pd.DataFrame:
        """
        """
        try:
            date_df = PrepareRestaurantSales.prepare_columns(restaurant_sales, column_maps = {
                "Order Date" : "full_date",
                "Day of the Week" : "day_of_week",
                "Is weekend" : "is_weekend",
                "Month Number" : "month_number",
                "Month of the Year" : "month_of_year",
                "Quarter of the Year" : "quarter",
                "Year": "dateyear"
                }
            )
            logger.info("Successfully created Order Date data to fill date table")

        except Exception as e:
            logger.exception (f"Failed to created Order date data to fill date dimension table: {e}")
            raise 

        return date_df

    @staticmethod
    def prepare_payment (restaurant_sales: pd.DataFrame) -> pd.DataFrame:
        try:
            payment_df = PrepareRestaurantSales.prepare_columns(restaurant_sales, column_maps = {"Payment Method" : "payment_method_name"})
            logger.info("Successfully created a dataframe for payment method data to fill payment_method table.")
        except Exception as e:
            logger.exception(f"Failed to create a dataframe for payment method data: {e} ")
            raise

        return payment_df


    @staticmethod
    def prepare_category(restaurant_sales : pd.DataFrame) -> pd.DataFrame:
        """
        """
        try:
            category_df = PrepareRestaurantSales.prepare_columns(restaurant_sales, column_maps = {"Category": "category_name"})
            logger.info("Successfully created Category dataframe to fill category dimemnsion table.")
        except Exception as e:
            logger.exception(f"failed to create Categpry dataframe. Loading the category dimension table would fail : {e}")
            raise  

        return category_df

    @staticmethod
    def prepare_diet (restaurant_sales : pd.DataFrame) -> pd.DataFrame:
        """
        """
        try:
            diet_df = PrepareRestaurantSales.prepare_columns(restaurant_sales, column_maps ={"Diet": "diet_name"})
            logger.info("Successfully created Diet dataframe for loading in diet dimension table.")
        except Exception as e:
            logger.excpetion(f"Failed to create Diet dataframe for loading in diet dimension table: {e}")
            raise 

        return diet_df


    # Load Dimension Table 
    
def insert_table (dataframe, database_engine, table, schema, conflict_columns):
    """
    """
    try:
        # Step 1 copy dataframe and conver the table to python dictionary 
        dataframe = dataframe.copy

        records = dataframe.to_dict(orient = 'records')

        # Step 2 - Build the SQL schema 
        cols = ", ".join (dataframe.columns)
        vals = ", ".join ([f": {c}" for c in dataframe.columns])
        conflicts = ", ".join(confict_columns) if not isinstance (coflict_columns, str) else conflict_columns

        sql = text (f"""
            INSERT INTO {schema}.{table} ({cols})
            VALUES ({vals})
            ON CONFLICT ({conflicts}) DO NOTHING
            """)

        # Step 3 - Load into the database 
        with database_engine.connect () as conn:
            conn.execute(sql, records)
            conn.commit()
            logger.info(f"Loaded {len(dataframe)} rows into {schema}.{table} successfully.")

    except Exception as f :
        logger.exception(f"Failed to load {schema}.{table}, the reason being {f}")
        raise

def load_dimension_tables (restaurant_sales, sales_dw_engine):
    """
    
    """
    restaurant_sales = restaurant_sales.copy

    try:
        insert_table (PrepareRestaurantSales.prepare_items(restaurant_sales), sales_dw_engine, table = "item", schema = "dimensions", conflict_columns = ["item_name"])
        insert_table (PrepareRestaurantSales.prepare_date(restaurant_sales), sales_dw_engine, table = "date", schema = "dimensions", conflict_columns = ["full_date"])
        insert_table (PrepareRestaurantSales.prepare_payment(restaurant_sales), sales_dw_engine, table = "payment_method", schema = "dimensions", conflict_columns = ["payment_method_name"])
        insert_table (PrepareRestaurantSales.prepare_category(restaurant_sales), sales_dw_engine, table = "category", schema = "dimensions", conflict_columns = ["category_name"] )
        insert_table (PrepareRestaurantSales.prepare_diet(restaurant_sales), sales_dw_engine, table = "diet", schema = "dimensions", conflict_columns = ["diet_name"])

        logger.info("successfully loaded all dimension tables.")
    
    except Exception as e:
        logger.exception (f"Falied to load all dimensions table : {e}")
        raise

    return restaurant_sales 

def read_merge_insert_fact_table (restaurant_sales, sales_dw_engine):
    """
    """

    restaurant_sales = restaurant_sales.copy 

    # Read primary keys from dimension tables 
    # items dimension table 
    try:
        items_db = pd.read_sql ("SELECT item_key, item_name FROM dimensions.item", sales_dw_engine)
        logger.info("Successfully read primary keys and unique values in item dimension table.")
    except Exception as fg:
        logger.exception (f" Failed to read items dimension table : {fg}.")
        raise 

    # date dimension table 
    try:
        date_db = pd.read_sql ("SELECT date_key, full_date FROM dimensions.date", sales_dw_engine)

        logger.info ("Sucessfully read the primary keys and unique vales in data dimensions table.")

    except Exception as e:
        logger.exception (f"Failed to read date dimensions table: {e}")
        raise

     # payment dimension table 
    try:
        payment_db = pd.read_sql ("SELECT paymnt_method_key, payment_method_name FROM dimesnions.payment_method", sales_dw_engine)

        logger.info("Successfully read the primary keys and unique values in payment_method dimenions table.")
    except Exception as e:
        logger.exception (f"Failed to read payment_method dimesnions table : {e}")
        raise

    # Category dimension table
    try:
        category_db = pd.read_sql ("SELECT category_key, category_name FROM dimensions.category", sales_dw_engine)

        logger.info("Successfullly read the primary keys and unique values in category dimesions table")

    except Exception as f:
        logger.exception (f"Failed to read primary keys and uniquye values from category dimensions table : {f}") 
        raise

    # Diet dimension table 
    try:
        diet_db = pd.read_sql ("SELECT diet_key, diet_name FROM dimensions.diet", sales_dw_engine)

        logger.info("Successfully read the primarykey and unique values in diet dimensions table")

    except Exception as e:
        logger.exception (f"Failed to read primary key and unique values from diet dimension table : {e}")
        raise
    
    # 2.0 Merge - merge items_db, date_db, payment_db, category_db and diet_db columns with restaurant_sales dataframes
    try:
        fact_df = (
            restaurant_sales.merge (items_db, left_on = "Item", right_on = "item_name")
            .merge(date_db, left_on = "Order Date", right_on = "full_date")
            .merge(payment_db, left_on = "Payment Method", right_on = "payment_method_name")
            .merge (category_db, left_on = "Category", right_on = "category_name")
            .merge (diet_db, left_on = "Diet", right_on = "diet_name")
            [["Order ID", "Customer ID", "date_key", "item_key", "payment_method_key", "category_key", "diet_key", "Price", "Quantity", "Order Total"]]                                                                             # Select the datasets in the order you want them to appear
            .rename(columns ={                                                                                                                                                                              # We rename the columns in the dataframe to the respective name in the data warehouse 
                        "Order ID" : "order_id",
                        "Customer ID" : "customer_id",
                        "Price" : "price",
                        "Quantity" : "quantity",
                        "Order Total" : "order_total"
                    } 
                )      
        )   

        logger.info("Successsfully merged dimension keys with the dataframe, filtered columns, and renamed columns for loading into the restaurant_sales fact table.")

    except Exception as e:
        logger.exception (f"Failed to merge, filter andrename columsn for loading into the restaurant_sales fact tables : {e}")
        raise


    # 3.0 load data into fact table  
    try: 
        insert_table (fact_df, sales_dw_engine, table = "restaurant_sales", schema = "facts", conflict_columns = ["order_id"])

        logger.info("Successfullyloaded data into restaurant_sales fact table.")
    except Exception as f:
        logger.exception (f"Failed to load data in restaurant_sales fact table : {f}")
        raise

    return restaurant_sales 



# Orchestration function 
def run_load_restaurant_sales (restaurant_sales, sales_dw_engine):
    load_dimension_tables (restaurant_sales, sales_dw_engine)
    read_merge_insert_fact_table (restaurant_sales, sales_dw_engine)

    return restaurant_sales


# Script guard 
if __name__ == "__main__":
    setup_logging()
    restaurant_sales = run_transformation (run_extract_sequence())
    run_load_restaurant_sales (restaurant_sales, sales_dw_engine)






    

    
                                  

