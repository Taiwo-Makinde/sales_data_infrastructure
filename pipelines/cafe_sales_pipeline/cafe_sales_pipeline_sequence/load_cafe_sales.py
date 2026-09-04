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

    #Helper function that helps us convert the names of the dataframe column names to the accurate table names so that there is no error when we load the data
    # We would be dropping duplicates for only dimension tables not fact tables. For dimension tables, which want to create primary key for each dimension value. 
    @staticmethod  
    def prepare_columns(dataframe, column_maps):
        """
        Generic helper function that 
        1. picks only the columns we need
        2. drops duplicates
        3. renames our column names to match the table column name
        """
        return (
            dataframe[list(column_maps.keys())]
            .drop_duplicates()
            .rename(columns = column_maps)
        )
    

    @staticmethod
    def prepare_items(cafe_sales):
        try:
            item_df = PrepareCafeSales.prepare_columns(cafe_sales, column_maps = {"Item": "item_name"})
        except Exception as e:
            logger.exception(f"Attempt to change the dataframe column 'Item' to the table column 'item_name' failed: {e}...")
            raise 

        return item_df


    @staticmethod
    def prepare_payment (cafe_sales):
        try:
            payment_df = PrepareCafeSales.prepare_columns(cafe_sales, column_maps = {"Payment Method" : "payment_method_name"})
        except Exception as e:
            logger.exception(f"Attempt to change the dataframe column 'Payment Method' to the table column 'payment_method_name' failed: {e}...")
            raise

        return payment_df


    @staticmethod
    def prepare_location (cafe_sales):
        try:
            location_df = PrepareCafeSales.prepare_columns(cafe_sales, column_maps = {"Location" : "location_name"})
        except Exception as e:
            logger.exception(f"Attempt to change the dataframe column 'Location' to the table column 'location_name' failed: {e}...")
            raise

        return location_df


    @staticmethod
    def prepare_date(cafe_sales):
        try: 
            date_df = PrepareCafeSales.prepare_columns (cafe_sales, column_maps = {
                        "Transaction Date" : "full_date",
                        "Day of the Week" : "day_of_week",
                        "Is weekend" : "is_weekend",
                        "Month Number" : "month_number", 
                        "Month of the Year": "month_of_year",
                        "Quarter of the Year": "quarter", 
                        "Year": "dateyear"
                    }
                    )

        except Exception as e :
            logger.exception(f"Attempt to change the dataframe date columns to the table date columns failed: {e}...")
            raise

        return date_df


# Load
# LoadCafeSales
# Generic insert function
def insert_table (dataframe, table, schema, conflict_columns ):                 
    # conflict_column is the column whose values should not conflict so we can properly generate primary (surrogate) keys so I check for duplicates 
    """
    A generic function that inserts dataframes into PostgreSQL table. 
    Written with idempotency in mind in that it skips rows that already exist.
    1. converts the whole dataframe to a list of python dictionaries
    2. builds the SQL once using dataframe columns 
    3. inserts all rows in one trip to the DB while skipping rows that already exist.
    """
    try: 
        # Step 1 - Convert the whole table to a lists of python dictionaries
        records = dataframe.to_dict(orient = "records")

        # Step 2 - Build the SQL schema once and for all. 
        # One alternative would have been to map the objects of the dataframe but we would have had to keep (cache) a metadata of the shema to reduce the memory being spent,
        # and then have to refresh the metadata to notice schema drift. That is too tasking when we can just build our schema everytime  
        
        cols = ", ".join(dataframe.columns)
        vals = ", ".join([f":{c}" for c in dataframe.columns])
        conflicts = ", ".join(conflict_columns)

        sql = text(f"""
            INSERT INTO {schema}.{table} ({cols})
            VALUES ({vals})
            ON CONFLICT ({conflicts}) DO NOTHING
        """)

        # Step 3 - 
        with sales_dw_engine.connect() as conn:
            conn.execute(sql, records)
            conn.commit()
            logger.info(f"Loaded {len(dataframe)} rows into{schema}.{table} succesfully")

    except Exception as e:
            logger.exception(f"Failed to load {schema}.{table}, the reason being {e} ")
            raise


# Fill dimension tables first since they contain the primary keys
# We would just call load_dimension_tables function
def load_dimension_tables(cafe_sales):
    """
    One general function to load all dimension tables making use of a helper function insert_table() 
    """
    insert_table(PrepareCafeSales.prepare_items(cafe_sales), table = "item", schema = "dimensions", conflict_columns = ["item_name"])
    insert_table(PrepareCafeSales.prepare_payment(cafe_sales), table = "payment_method", schema = "dimensions", conflict_columns = ["payment_method_name"])
    insert_table(PrepareCafeSales.prepare_location(cafe_sales), table = "location", schema = "dimensions", conflict_column = ["location_name"])
    insert_table(PrepareCafeSales.prepare_date(cafe_sales), table = "date", schema = "dimensions", conflict_columns = ["full_date"])


# Merge 
def read_foreign_keys (sales_dw_engine):
    """
    
    """
    try:
        global global_items_db                                             # We want to be able to reference item_db outside of this function
        global items_db = pd.read_sql("SELECT item_key, item_name", sales_dw_engine)
    except Exception as e:
        logger.exception("")
        raise

    try:
        global global_payment_db
        payment_db = pd.read_sql("SELECT payment_method_key, payment_method_name", sales_dw_engine)
    except Exception as e:
        logger.exception ("")
        raise

    try:
        global global_location_db 
        location_db = pd.read_sql("SELECT location_key, location_name", sales_dw_engine)
    except Exception as e:
        logger.exception ("")
        raise

    try:
        global global_date_db 
        date_db = pd.read_sql("SELECT date_key, full_date", sales_dw_engine)
    except Exception as e:
        logger.exception ("")
        raise


def merge_foreign_keys_dataframe (cafe_sales):
    """
    
    """
    # Merge with items_db
    try:
        (
            cafe_sales.merge (global_items_db, left_on= "Item", right_on = "item_name")
            .merge (global_payment_db, left_on = "Payment Method", right_on = "payment_method_name")
            .merge (global_location_db, left_on = "Location", right_on = "location_name")
            .merge (global_date_db, left_on = "Transaction Date", right_on= "full_date")
        )
    except Exception as e:
        logger.exception(f"")
        raise

    # Choose waht should form the fact table
    try:
        global global_fact_table
        global_fact_table = (
            [["Transaction ID", "date_key", "item_key", "payment_method_key", "location_key", "Quantity", "Price Per Unit", "Total Spent"]] # Some information here is missing 
        .rename(
            columns ={
            "Transaction ID": "transaction_id",
            "Quantity" : "quantity",
            "Price Per Unit": "price_per_unit",
            "Total Spent" : "total_spent"}
        )
        )

    except Exception as e:
        logger.exception(f"")
        raise

    return cafe_sales

def load_fact_table ():
    try:
        insert_table (global_fact_table, table = "cafe_sales", schema ="dimensions", conflict_columns = "transaction_id")
    except Exception as e:
        logger.exception (f"")
        raise


# Orchestration function 
def run_load_cafe_sales ():
    load_dimension_tables(cafe_sales)
    read_foreign_keys(sales_dw_engine)
    merge_foreign_keys_dataframe (cafe_sales)
    load_fact_table()

# 
if __name__ == "__main__" :
    setup_logging()
    run_load_cafe_sales()

