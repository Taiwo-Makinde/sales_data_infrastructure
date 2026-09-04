# Transformation

# Import the packages in the standard python module
import logging                               # for logging
import random 
random.seed(5)                               # 5 is a lucky number; I am specifying 5 so that the random shuffle is reproducible 

# Importing third-party python packages
import numpy as np
import pandas as pd

# Importing local customised packages 

from sales_data_logs.sales_data_logging_config import setup_logging  # My personalise logging module that outputs logs in single-line json format. 

# We set up our logger 

logger = logging.getLogger(__name__) # We use __name__ so that it correctly resolves to the module name and file name cafe_sales_pipeline_sequence + transform_cafe_sales

class CleanCafeSales:
    # The class is for orgnisation purposes. So we use decorator @staticmethod
    # We noticed that some cells are represented as unknown and error
    # We want to replace UNKNOWN and ERROR with nan.


    @staticmethod # I want to inform python that the method following the decorator does not need access to the instance self or the class cls. 
    def convert_error_unknown_to_null(cafe_sales):
        """This function takes in the cafe_sales dataframe, converts all column data type to string while mantinaing null values, 
        converts all 'ERROR' and 'UNKNOWN' to null values (nan) for further data cleaning.
        """
        # We convert all columns datatype to string
        try: 
            # I use .astype("string") instead of .astype(str) because that method converts the columns to string while preserving native pandas null values.  
            cafe_sales = cafe_sales.astype("string") 
        except Exception as e:
            logger.exception(f"Attempt to convert all columns to string data type failed : {e}")
            raise 
        else:
            logger.info("Successfully converted all columns to string data type")

        # Now that UNKNOWN and ERROR have become 'UNKNOWN' AND 'ERROR', let's replace them
        try:
            mask_unknown = (cafe_sales == 'UNKNOWN') 
            mask_error = (cafe_sales == 'ERROR')

            cafe_sales.mask(mask_unknown, np.nan, inplace = True)
            cafe_sales.mask(mask_error, np.nan, inplace = True)

        except Exception as e :
            logger.exception(f"Attempt to replace 'UNKNOWN' and 'ERROR' with null values failed : {e}")
            raise
        else:
            logger.info(f"Successfully replaced 'UNKNOWN' text in {mask_unknown.to_numpy().sum()} cells and 'ERROR' texts in {mask_error.to_numpy.sum()} cells with null values.")
            
        return cafe_sales


    @staticmethod
    def convert_quantity_price_total_date(cafe_sales):
        """This function takes in the cafe_sales dataframe as a parameter,
        converts the data type for Quantity to number,
        the data type for Price Per Unit and Total Spent columns to float, 
        and returns the dataframe.
        """

        # Convert Quantity column to Integer 
        try:
            cafe_sales['Quantity'] = pd.to_numeric(cafe_sales['Quantity'], errors = 'coerce').astype('Int64')
             
        except Exception as e:
            logger.exception(f"Some error occurred during the conversion of Quantity column to Integer: {e}")
            raise
        else:
            logger.info("Quantity column's datatype successfully converted to Integer")

         # The above function has two soft error handling safety: pd.to_numeric + errors = 'coerce' and 'Int64'. We use both of these methods because our data has null values. 
       

        # Convert Price column to Float 
        try:
            cafe_sales['Price Per Unit'] = pd.to_numeric(cafe_sales['Price per Unit'], errors = 'coerce')
            # We use pd.to_numeric + errors = 'coerce' because our data has null values
        except Exception as e: 
            logger.exception(f"Some error occured during conversion of Price Per Unit to Integer: {e}")
            raise
        else:
            logger.info("Price Per Unit column's datatype successfully converted to Integer")


        # Convert Total Spent column to Float 
        try:
            cafe_sales['Total Spent'] = pd.to_numeric(cafe_sales['Total Spent'], errors= 'coerce')
        except Exception as e:
            logger.exception(f"Some error occured during the conversion of Total Spent column to Integer: {e}")
            raise
        else:
            logger.info("Total Spent column's datatype successfully converted to Integer")


        # Convert Transcation date column to datetime 
        try:
            cafe_sales['Transaction Date'] = pd.datetime(cafe_sales["Transaction Date"], errors = 'coerce')
        except Exception as e:
            logger.exception(f"Coversion of datatype fo Transaction date column failed: {e}")
            raise
        else:
            logger.info("Successfully coverted the datatype for 'Transaction Date' to datetime")

        return cafe_sales
   

    @staticmethod
    def fill_price_with_quantity_total (cafe_sales):
        """
        This function takes in the dataframe cafe_sales as a parameter,
        fills the empty cells in Price Per Unit column by dividing the adjacent values of Total Spent and Quantity columns,
        returns the dataframe
        """

        # Deterministic Method to finding Price using Total Spent and Quantity (1st Approach: Deterministic; 1st Method: Using Total/Quantity). 
        mask_empty_price = cafe_sales['Price Per Unit'].isna() & cafe_sales['Total Spent'].notna() & cafe_sales['Quantity'].notna()
        cells_affected = mask_empty_price.to_numpy().sum()

        try:
            cafe_sales.loc[mask_empty_price, 'Price Per Unit'] = cafe_sales.loc[ mask_empty_price, 'Total Spent'] / cafe_sales.loc [
                mask_empty_price, 'Quantity']
        except Exception as e:
            logger.exception(f"Error occured while filling Price Per Unit column with the division of values in Total Spent and Quantity:{e}")
            raise
        else:
            logger.info(f"Successfully filled {cells_affected} cells in the Price Per Unit column with division of Total Spent and Quantity columns.")

        return cafe_sales


    @staticmethod
    def fill_price_based_on_item (cafe_sales):
        """
        This function takes in the dataframe cafe_sales as a parameter, 
        creates a dictionary out of the unique values of Item and Price Per Unit
        fills Price Per Unit column by mapping its content (as values) to content (as keys) in Items columns;
        It returns the new dataframe and the dictionary for subsequent use.
        """
        # Deterministic Method to finding Price using Item (1st Approach: Deterministic; 2nd Method: Using Item ) 
        item_price_dict = (
            cafe_sales [['Item', 'Price Per Unit']]                 # Selecting the two columns (Item and Price Per Unit)
            .dropna()                                               # I remove null values
            .drop_duplicates(subset = ['Item'], keep = 'first')     # I remove duplicates 
            .set_index('Item')['Price Per Unit']                    # Set the index to Item which makes the dataframe a series where index is item and column is Price Per Unit
                               .to_dict()                           # I convert the series to a dictionary, so that I can map it. 
        )

        mask_empty_price = (cafe_sales ['Price Per Unit'].isna() & cafe_sales ['Item'].notna() # The appropriate operator is the bitwise & not boolean operator 'and' 
        cells_affected = mask_empty_price.to_numpy().sum()
        rows_affected = (mask_empty_price.sum(axis=1) > 0).sum()
        # ".sum(axis=1) takes sum of rows, > 0 checks if the sum of rows is greater than 0 returns the output as True if it is and otherwise returns False
        # .sum() takes the sum of all rows containing True

        try: 
            cafe_sales.loc [mask_empty_price, 'Price Per Unit'] = cafe_sales.loc [mask_empty_price, 'Item'].map(item_price_dict)
        except Exception as e:
            logger.exception(f"Attempt to fill Price Per Unit Column with Item failed: {e}.")
            raise
        else:
            logger.info(f"Successfully filled Price Per Unit column with Item in {rows_affected} rows with {cells_affected} cells affected.") 

        return item_price_dict, cafe_sales 


    @staticmethod
    def fill_empty_quantity_total (cafe_sales):
        """
        This function takes in the dataframe cafe_sales as a parameter, 
        fills the empty cells in quantity by dividing the adjacent values of Total Spent and Price Per Unit columns,
        fills the empty cells in Total Spent by  multiplying the adjacent values of Quanity and Price Per Unit,
        returns the dataframe.
        """
        # Deterministic Approach to finding Quantity and Total Spent using adjacent values 
       
        # let's create a mask for each of these steps 
        mask_empty_quantity = cafe_sales['Quantity'].isna() & cafe_sales['Total Spent'].isnotna() & cafe_sales[
            'Price Per Unit'].isnotna()
        mask_empty_total = cafe_sales['Total Spent'].isna() & cafe_sales['Quantity'].isnotna() & cafe_sales[
            'Price Per Unit'].isnotna()

        quantity_affected = mask_empty_quantity.any(axis=1).sum()
        total_filled = mask_empty_total.any(axis=1).sum()

        # To find the values for empty cells in Quantity column 
        try :
            cafe_sales.loc[mask_empty_quantity, 'Quantity'] = cafe_sales.loc[ mask_empty_quantity, 'Total Spent'] / cafe_sales.loc [
                mask_empty_quantity, 'Price Per Unit']
        except Exception as e:
            logger.exception(f"Error occured while filling Quantity column with the division of values in Total Spent and Price : {e}.")
            raise
        else:
            logger.info(f"Successfully filled Quantity column with division of Total Spent and Price columns, {quantity_affected} rows affected.")

        # To find the values for the empty cells in Total Spent
        try: 
            cafe_sales.loc[mask_empty_total, 'Total Spent'] = cafe_sales.loc[ mask_empty_total, 'Quantity'] * cafe_sales.loc [
                mask_empty_total, 'Price Per Unit']
        except Exception as e:
            logger.exception(f"Error occured while filling Price Per Unit column with the division of values in Total Spent and Quantity:{e}")
            raise
        else:
            logger.info(f"Successfully filled Total Spent column with the multiplication of Quantity and Price columns, {total_filled} rows affected.")
    
        return cafe_sales


    @staticmethod
    def fill_empty_item (cafe_sales):
        """
        This function takes in the dataframe cafe_sales as a parameter, 
        flips the item_price_dict dictionary (keys for values, values for keys)
        fills Item column by mapping its content (as values) to content (as keys) in Price Per Unit columns;
        It returns the new dataframe and the dictionary for subsequent use.
        fills the empty cells in quantity by dividing the adjacent values of Total Spent and Price Per Unit columns,
        fills the empty cells in Total Spent by  multiplying the adjacent values of Quanity and Price Per Unit,
        returns the dataframe.
        """
        # 1st Approach (deterministic) : Use the values in Price Per Unit to find Item 
        # We flip the dictionary 
        price_item_dict = {v : k for k, v in item_price_dict.items()}

        # I create a mask filter
        mask_empty_item = cafe_sales ['Item'].isna() & cafe_sales ['Price Per Unit'].notna()

        # We want to know the number of rows affected
        rows_affected = mask_empty_item.any(axis=1).sum()
        

        try:
            cafe_sales.loc [mask_empty_item, 'Item'] = (cafe_sales.loc [mask_empty_item, 'Price Per Unit'].map(price_item_dict))
        except Exception as e:
            logger.exception(f"Attempt to fill Item column with Price Per Unit failed: {e}.")
            raise
        else:
            logger.info(f"Successfully filled {rows_affected} rows in the Item column by apping it with the equivalent value in the Price Per Unit column.") 

        return price_item_dict, cafe_sales


    @staticmethod
    # Probabilistic Approach
    def fill_item_price_probabilistic_approach (cafe_sales):
        """
        This function takes in cafe_sales as a parameter,
        checks if Item and Price Per Unit columns are filled,
        if they are, fills Quantity column with random numbers based on probability and derives Total Spent values from the multiplication of Price Per Unit and Quantity,
        if they aren't, fills Item column with random items by probability, derives price and from price derives Quantity and Total Spent,
        and returns the dataframe.
        """

        # We have tried filling Price Per Unit column cells in two ways:
        # 1. filling price based on the values of Items (there is a standard price for each item; a key-value pair: values of Price Per Unit mapped to the keys of Items)
        # 2. filling price based on the division of Total Spent and Quantity (Total spent is Price * Quantity)

        # At this point, we should be left with four possibilities in regard to Item, Price Per Unit, Quantity and Total Spent columns.
        # i. rows where Item, Price Per Unit, Quantity and Total Spent columns are all empty                       # Second level of probability approach (2.0) solves this
        # ii. rows where Item, Price Per Unit and Quantity columns are empty but Total Spent column is not empty   # 1.2.2 solves this
        # iii. rows where Item, Price Per Unit and Total Spent columns are empty but Quantity column is not empty  # 1.2.1 solves this
        # iv. rows where Quantity and Total Spent columns are empty but Item and Price columns are not empty.      # 1.1 (1.1.1 & 1.1.2) solves this

        # Hence, in summary under the first level of probability approach (1.0) this function has two options 
        # 1.1 Where Item and Price Per Unit columns are completely filled, but Quantity and Total Spent are empty.
        # 1.2 Where Item, Price Per Unit are empty and either Quantity and Total Spent columns are empty.

   
        # 1.1
        if cafe_sales['Item'].notna().all() & cafe_sales ['Price Per Unit'].notna().all():
            logger.info("There are no empty cells in Item or Price Per Unit column...")

            logger.info("Filling Quantity column with probability approach")
            # 1.1.1
            try:
                # I create a mask that filters for empty cells in Quantity column and Total Spent column 
                empty_quantity_total = cafe_sales['Quantity'].isna() & cafe_sales['Total Spent'].isna()

                # I count a sum of all the affected rows
                sum_empty_quantity_total = empty_quantity_total.any(axis=1).sum()


                quantity_proportions = cafe_sales['Quantity'].value_counts(normalize = True)
                empty_quantity_total_count = empty_quantity_total.sum() # We take a count of all rows where Quantity and Total Spent cells are empty 
        

                quantity_method_to_add = [] # create an empty list

                # I create loop through the dictionary (quantity value & proportion pair)
                # 
                for quant, prop in quantity_proportions.items():
                    quantity_method_to_add.extend([quant] * round(prop * empty_quantity_total_count)) 
                                                  # to get a proportion distribution, we round up the multiplication of proportion and the number of empty cells.
                    # we take the proportion distribution (how many times should a value appear) and then multiply the unique_values based on the proportion distribution.
                    #So that the unique values are distributed in the list based on the proportion distribution.
            
                # We shuffle the list randomly
                random.shuffle(quantity_method_to_add)

                # We input the shuffled list into every Quantity column rows where Quantity and Total Spent columns
                cafe_sales.loc [empty_quantity_total, 'Quantity'] = quantity_method_to_add [:empty_quantity_total_count]

            except Exception as e:
                logger.exception(f"Attempt to fill Quantity column based on probability where Item and Price Per Unit columns were not empty failed: {e}.")
                raise
            else:
                logger.info(f"Successfully filled {sum_empty_quantity_total} cells in Quantity column using probability where Item and Price Per Unit columns were not empty.") 

            logger.info("Filling Total Spent column after using probability approach to fill Quantity column where Item and Price Per Unit columns were not empty.")


            #1.1.2
            # 
            try:
                # Total Spent is empty
                # I create a mask that filters for empty cells in Total Spent column and no empty values in Quantity column
                empty_total = cafe_sales ['Total Spent'].isna() & cafe_sales ['Quantity'].notna() 

                # A sum of all affected rows. 
                sum_empty_total = empty_total.any(axis=1).sum()

                # We solve for Total Spent 
                cafe_sales.loc [empty_total, 'Total Spent'] = cafe_sales.loc [empty_total, 'Quantity'] * cafe_sales.loc [
                empty_total, 'Price Per Unit']

            except Exception as e:
                logger.exception(f"Attempt to fill Total Spent column after using probability approach to fill Quantity column failed: {e}")
                raise
            else:
                logger.info(f"Successfully filled {sum_empty_total} cells in Total Spent column after using probability approach to fill Quantity column.")

            return cafe_sales


        # 1.2 Second option of the First Level of Probability Approach:
        # Where both Item and Price Per Unit are empty, but either Quantity or Total Spent columns is empty.
        # I derive Item through the probability approach, then derive Price from Item; and with Price, I derive Quantity and Total Spent.
       
        # We are using mask filter as a freeze in time. This will ensure our codes still works even though no cell in Item column would be empty when the second code runs
        # We are using brackets to instruct Python the order of execution:check where both Item and Price are empty and then where either Quantity or Total Spent is empty
        mask_item_price_qt_empty = (cafe_sales['Item'].isna() & cafe_sales ['Price Per Unit'].isna()) & (
            (cafe_sales['Quantity'].isna() & cafe_sales['Total Spent'].notna()) | (cafe_sales['Quantity'].notna() & cafe_sales['Total Spent'].isna()) 
            )
      
        # We want to know the number of rows where both Item and Price Per Unit are empty.
        affected_rows =  mask_item_price_qt_empty.any(axis=1).sum()
                
        # Create a list of the keys and specify the number of items to be randomly returned based on the number of empty values 
        random_items = random.choices(list(item_price_dict.keys()), k = mask_item_price_qt_empty.sum()) 

        # 1.2.1
        # Fill Item column with random values from the dictionary keys when both Item and Price Per Unit are empty 
        try: 
            # Fill all the records in Item column where both Item and Price Per Unit are empty with random_items
            cafe_sales.loc [mask_item_price_qt_empty, 'Item'] = random_items
        except Exception as e : 
            logger.exception(f"Attempt to randomly fill Item column with the probability approach failed: {e}")
            raise
        else:
            logger.info(f"Successfully filled Item column with the probability approach in {affected_rows} rows")

        # Let's check that all Items have been filled
        if cafe_sales['Item'].notna().all():
            still_missing_item = cafe_sales['Item'].isna().sum()
            logger.warning(f"{still_missing_item} rows in Item column still have empty cells.")

        # 1.2.2
        # Map Price Per Unit to the new randomly generated keys Items columns
        try:
            #Find all the cells in Price Per Unit column where the adjacent cells of Item and Price Per Unit were empty and fill the cells with the dictionary's values from Item
            cafe_sales.loc [mask_item_price_qt_empty, 'Price Per Unit'] = list(map(item_price_dict.get, random_items))
        except Exception as e:
            logger.exception(f"Attempt to randomly fill Item column with the probability approach failed: {e}")
            raise
        else:
            logger.info(f"Successfully filled Price Per Unit column with the probability approach in {affected_rows} rows")

        # Let's check that all Price Per Unit column have been filled 
        if cafe_sales['Price Per Unit'].notna().all():
            still_missing_price = cafe_sales ['Price Per Unit'].isna().sum()
            logger.warning(f"There are still {still_missing_price} empty cells in Price Per Unit columns.")


        # 1.2.3 
        # Having filled Item with probability and derived Price Per Unit; let's solve for Quantity and Total Spent  
        try:     
            # To find the values for empty cells in Quantity column 
            cafe_sales.loc[ mask_item_price_qt_empty, 'Quantity'] = cafe_sales.loc[mask_item_price_qt_empty, 'Total Spent'] / cafe_sales.loc [
                 mask_item_price_qt_empty, 'Price Per Unit']
        except Exception as e:
            logger.exception(f"Error occured while filling Quantity column with the division of values in Total Spent and Price : {e}.")
            raise
        else:
            logger.info(f"Successfully filled Quantity column with division of Total Spent and Price columns, {affected_rows} rows affected.")

        # To find the values for the empty cells in Total Spent
        try: 
            cafe_sales.loc[mask_item_price_qt_empty, 'Total Spent'] = cafe_sales.loc[mask_item_price_qt_empty, 'Quantity'] * cafe_sales.loc [
                 mask_item_price_qt_empty, 'Price Per Unit']
        except Exception as e:
            logger.exception(f"Error occured while filling Price Per Unit column with the division of values in Total Spent and Quantity:{e}")
            raise
        else:
            logger.info(f"Successfully filled {affected_rows} rows Total Spent column with Quantity and Price columns, a   affected.")
            

        return cafe_sales

    
    @staticmethod
    def fill_empty_quantity_total_probabilistic_approach (cafe_sales):

        # Second level of Probabilistic Approach
        # 2.0 rows where Item, Price Per Unit, Quantity and Total Spent columns are all empty    

        if cafe_sales ['Item'].notna().all() & cafe_sales ['Price Per Unit'].notna().all() & cafe_sales['Quantity'].notna().all() & cafe_sales['Total Spent'].notna().all():
            logger.info("Item, Price Per Unit, Quantity and Total Spent are completely filled. Skipping this step...")
            return True
        
        # masks : rows where Item, Price Per Unit, Quantity and Total Spent columns are all empty 
        empty_item_price_quantity_total = cafe_sales['Item']isna() & cafe_sales['Price Per Unit'].isna() & cafe_sales['Quantity'].isna() & cafe_sales['Total Spent'].isna() 

        # Afffected rows
        affected_empty_rows = empty_item_price_quantity_total.any(axis=1).sum()

        # Create a list of the keys and specify the number of items to be randomly returned based on the number of empty values 
        random_items = random.choices(list(item_price_dict.keys()), k = empty_item_price_quantity_total.sum()) 


        # 2.0.1
        # Fill Item column with random values from the dictionary keys when both Item, Price Per Unit,Quantity and Total Spent are empty 
        try: 
            # Fill all the records in Item column where both Item and Price Per Unit are empty with random_items
            cafe_sales.loc [empty_item_price_quantity_total, 'Item'] = random_items
        except Exception as e : 
            logger.exception(f"Attempt to randomly fill Item column with the probability approach (second-level) failed: {e}")
            raise
        else:
            logger.info(f"Successfully filled Item column with the probability approach (second level) in {affected_empty_rows} rows")

        # Let's check that all Items have been filled
        if cafe_sales['Item'].notna().all():
            still_missing_item = cafe_sales['Item'].isna().sum()
            logger.warning(f"There are still {still_missing_item} empty cells in Item column after second-level probability approach.")


        # 2.0.2
        # Map Price Per Unit to the new randomly generated keys Items columns
        try:
            #Find all the empty cells in Price Per Unit column where the adjacent cells of Item, Quantity and Total Spent are also empty
            cafe_sales.loc [empty_item_price_quantity_total, 'Price Per Unit'] = list(map(item_price_dict.get, random_items))
        except Exception as e:
            logger.exception(f"Attempt to randomly fill Price Per Unit column with the probability approach (second level) failed: {e}")
            raise
        else:
            logger.info(f"Successfully filled Price Per Unit column with the probability approach (second level) in {affected_rows} rows")

        # Let's check that all Price Per Unit column have been filled 
        if cafe_sales['Price Per Unit'].notna().all():
            still_missing_price = cafe_sales ['Price Per Unit'].isna().sum()
            logger.warning(f"There are still {still_missing_price} empty cells in Price Per Unit column after second-level probability approach .")


        # 2.0.3 Fill Quantity randomly
        # value counts returns how many times a unique value appears and (normalize = True) returns the proportions (fractions of the whole)
        quantity_proportions = cafe_sales['Quantity'].value_counts(normalize = True)

        # We take a count of all rows where Item, Price Per Unit,  Quantity and Total Spent cells are empty 
        empty_item_price_quantity_total_count = empty_item_price_quantity_total.sum() 

        # create an empty list
         empty_item_price_quantity_total_method_to_add = [] 

        # I create loop through the dictionary (quantity value & proportion pair)
        for quant, prop in quantity_proportions.items():
            empty_item_price_quantity_total_method_to_add.extend([quant] * round(prop * empty_item_price_quantity_total_count)) 
                                                  # to get a proportion distribution, we round up the multiplication of proportion and the number of empty cells.
                    # we take the proportion distribution (how many times should a value appear) and then multiply the unique_values based on the proportion distribution.
                    #So that the unique values are distributed in the list based on the proportion distribution.
            
        # We shuffle the list randomly
        random.shuffle(empty_item_price_quantity_total_method_to_add)

        try:
            # We input the shuffled list into every cell in Quantity rows where Item, Price, Quantity and Total Spent columns
            cafe_sales.loc [empty_item_price_quantity_total, 'Quantity'] = empty_item_price_quantity_total_method_to_add [:empty_item_price_quantity_total_count]
        except Exception as e:
            logger.exception(f"Attempt to fill Quantity column based on probability where Item and Price Per Unit columns were not empty failed: {e}.")
            raise
        else:
            logger.info(f"Successfully filled {affected_empty_rows} cells in Quantity column using probability (second-level)") 


        # 2.0.4. Fill Total Spent after applying second level probability approach 
        try:
            cafe_sales.loc [empty_item_price_quantity_total, 'Total Spent'] = cafe_sales.loc [empty_item_price_quantity_total, 'Quantity'] * cafe_sales.loc [
                empty_item_price_quantity_total, 'Price Per Unit']
        except Exception as e:
            logger.exception(f"Attempt to fill Total Spent after probability approach has been used on Price Per Unit failed: {e}")
            raise
        else:
            logger.info(f"Successfully filled Total Spent column in {affected_empty_rows} cells after Price Per Unit probability approach")
        

        # Let's check that all the fields in Item, Price Per Unit, Quantity & Total Spent
        if cafe_sales['Item'].notna().all() & cafe_sales['Price Per Unit'].notna().all() & cafe_sales['Quantity'].notna().all() & cafe_sales['Total Spent'].notna().all():
            sum_missing_item = cafe_sales['Item'].isna().sum()
            sum_missing_price = cafe_sales['Price Per Unit'].isna().sum()
            sum_missing_quantity = cafe_sales['Quantity'].isna().sum()
            sum_missing_total = cafe_sales['Total Spent'].isna().sum()

            logger.info(f"There are still{sum_missing_item} missing cells in Item column, {sum_missing_price} cells in Price Per Unit column,'\n'
                        {sum_missing_quantity} cells in Quantity column and {sum_missing_total} cells in Total Spent column.")
            raise

        return cafe_sales

    @staticmethod
    # We are not using None because we want the dataframe and column to be required 
    # This is just a helper function 
    def probability_approach(dataframe, column):
        """"
        General function to fill columns of dataframes randomly.
        This function would be called in 
        
        """
        # Fill the column
        column_proportions = dataframe[column].value_counts (normalize = True)
        empty_column_count = dataframe [column].isna().sum()

        column_method_to_add = []
        for method, prop in column_proportions.items():
            column_method_to_add.extend([method] * round(prop * empty_column_count))
        
        random.shuffle(column_method_to_add)

        empty_column = dataframe [column].isna()
        impacted_rows = empty_column.sum() 

        dataframe.loc [empty_column, column] = column_method_to_add [:empty_column_count]

        if dataframe[column].notna().all():
            logger.info(f"Successfully filled {column} column in {impacted_rows} cells with probability approach")

        return dataframe 


    @staticmethod
    def fill_payment_prob_imputation(cafe_sales):
        """
        Function that calls the probability_approach function to fill Payment Method column. 
        """
        # Fill Payment Method
        try:
            cafe_sales = CleanCafeSales.probability_approach(dataframe = cafe_sales, column = 'Payment Method')
        except Exception as e:
            logger.exception(f"Attempt to fill Payment Method column with probability approach failed: {e}")
            raise

        return cafe_sales


    @staticmethod
    def fill_location_prob_imputation (cafe_sales):
        """
        Function that calls the probability_approach function to fill location column. 
        """
        try:
            cafe_sales = CleanCafeSales.probability_approach(dataframe = cafe_sales, column = 'Location')
        except Exception as e:
            logger.exception(f"Attempt to fill Location column with probability approach failed: {e}")
            raise

        return cafe_sales


    @staticmethod
    def fill_date_probabilistic_imputation (cafe_sales):
        """
        Function that calls the probability_approach function to fill Transaction Date column.
        """
        try:
            cafe_sales = CleanCafeSales.probability_approach(dataframe = cafe_sales, column = 'Transaction Date')
        except Exception as e :
            logger.exception(f"Attempt to fill Transaction Date column with probability approach failed: {e}")
            raise

        return cafe_sales


# Feature engineering 

def feature_engineer_date (cafe_sales):
    """
    Function to create new (column) features from Transaction Date: 
    create a day of the week, Is weekend, Month Number, Month of the Year, Quarter of the Year and Year columns based on Transaction Date 
    """

    # 1.0 Date of the week

    cafe_sales['Day of Week'] = cafe_sales['Transaction Date'].dt.day_name()

    # 2.0 Boolean column is_weekend
    # We create a column that contains the boolean solution to whether the day of the week is Saturday (5) or Sunday (6)
        
    cafe_sales['Is weekend'] = cafe_sales ['Transaction Date'].dt.weekday >= 5 # Thus, equal to or greater than 5

    # 3.0 Month number 
        
    cafe_sales ['Month Number'] = cafe_sales ['Transaction Date'].dt.month

    # 4.0 Month of the year 
    cafe_sales ['Month of the Year'] = cafe_sales ['Transaction Date'].dt.month_name()

    # 5.0 quarter 
    # Using datetime string formatter to extract the quater of the year and append 'Q' as a prefix 
    cafe_sales ['Quarter of the Year'] = cafe_sales ['Transaction Date'].dt.strftime('Q%q') # My intent is to format it as Q1, Q2, etc 

    # 6.0 Year 
    cafe_sales ['Year'] = cafe_sales ['Transaction Date'].dt.year

    return cafe_sales




def run_transformation (cafe_sales):
    """
    Function that orchestrates the transformation stage  
    """

    functions = [CleanCafeSales.convert_error_unknown_to_null,
    CleanCafeSales.convert_quantity_price_total_date,
    CleanCafeSales.fill_price_with_quantity_total,
    CleanCafeSales.fill_price_based_on_item,
    CleanCafeSales.fill_empty_quantity_total,
    CleanCafeSales.fill_empty_item,
    CleanCafeSales.fill_item_price_probabilistic_approach,
    CleanCafeSales.fill_empty_quantity_total_probabilistic_approach,
    CleanCafeSales.fill_payment_prob_imputation,                                            # helper function probability_approach() would be called when this function runs
    CleanCafeSales.fill_location_prob_imputation,
    CleanCafeSales.fill_date_probabilistic_imputation,
    feature_engineer_date,
    ]

    for function in functions:
        cafe_sales = function(cafe_sales)
        return cafe_sales


# This is the script guard that controls when the code runs. It ensures that the codes run if we call it directly.
if __name__ == "__main__":
    setup_logging()
    run_transformation(cafe_sales)

     


