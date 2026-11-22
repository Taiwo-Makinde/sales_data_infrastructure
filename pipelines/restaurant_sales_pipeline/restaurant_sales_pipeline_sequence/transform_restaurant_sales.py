# Transformation 

# Import the  modules in the python library 
import logging 
import random 
from decimal import Decimal 
from itertools import cycle

# Import third party python packages
import numpy as np
import pandas as pd

# Import local and customised python packages
from sales_data_logs.sales_data_logging_config import setup_logging 
from restaurant_sales_pipeline_sequence.extract_restaurant_sales import run_extract_sequence 

# Decide the random format and set up logger 
logger = logging.getLogger(__name__) 
random.seed (5)


class ReturnValues:
    @staticmethod 
    def item_price_category_full_dict() -> dict[str, dict[str, int | str ]]:
        # Applying cent - consider everything multiplied by 100  
        return {
            'Chicken Melt' : {'Price' : 800, 'Category' : 'Starters'},
            'French Fries' : {'Price' : 400, 'Category' : 'Starters'},
            'Cheese Fries' : {'Price' : 500, 'Category' : 'Starters'},
            'Sweet Potato Fries': {'Price': 500, 'Category': 'Starters'},
            'Beef Chili': {'Price': 700, 'Category': 'Starters'},
            'Nachos Grande': {'Price': 1000, 'Category': 'Starters'}, 
            'Grilled Chicken' : {'Price': 1500, 'Category': 'Main Dishes'},
            'Steak': {'Price': 2000, 'Category': 'Main Dishes'},
            'Pasta Alfredo': {'Price': 1200, 'Category': 'Main Dishes'},
            'Salmon': {'Price': 1800, 'Category':'Main Dishes'}, 
            'Vegetarian Platter': {'Price': 1400, 'Category': 'Main Dishes'},
            'Chocolate Cake': {'Price': 600, 'Category': 'Desserts'}, 
            'Ice Cream' : { 'Price': 500, 'Category': 'Desserts'}, 
            'Fruit Salad' : { 'Price' : 400, 'Category' : 'Desserts'}, 
            'Cheesecake' : { 'Price' : 700, 'Category' : 'Desserts'}, 
            'Brownie' : {'Price' : 600, 'Category' : 'Desserts'}, 
            'Coca Cola' : {'Price' : 250, 'Category' : 'Drinks'}, 
            'Orange Juice' : {'Price' : 300 , 'Category' : 'Drinks'}, 
            'Lemonade' : {'Price' : 300 , 'Category' : 'Drinks'}, 
            'Iced Tea' : { 'Price' : 250 , 'Category' : 'Drinks'}, 
            'Water' : {'Price' : 100, 'Category': 'Drinks'}, 
            'Mashed Potatoes' : {'Price' : 400, 'Category' : 'Side Dishes'}, 
            'Grilled Vegetables': {'Price' : 500 , 'Category' : 'Side Dishes'},
            'Side Salad' : { 'Price' : 300 , 'Category' : 'Side Dishes'}, 
            'Garlic Bread' : { 'Price' : 400, 'Category' :'Side Dishes'},
            'Onion Rings' : { 'Price' : 500, 'Category' : 'Side Dishes'}
             }

    @staticmethod
    def item_price_category_reoccuring_dict() -> dict [str, dict[str, int | str]]:
        # Dictionary with similar keys 
        return {
            'Cheese Fries' : {'Price' : 500, 'Category' : 'Starters'},
            'Sweet Potato Fries': {'Price': 500, 'Category': 'Starters'},
            'Chocolate Cake': {'Price': 600, 'Category': 'Desserts'}, 
            'Brownie' : {'Price' : 600, 'Category' : 'Desserts'}, 
            'Coca Cola' : {'Price' : 250, 'Category' : 'Drinks'}, 
            'Orange Juice' : {'Price' : 300 , 'Category' : 'Drinks'}, 
            'Lemonade' : {'Price' : 300 , 'Category' : 'Drinks'}, 
            'Iced Tea' : { 'Price' : 250 , 'Category' : 'Drinks'}, 
            'Mashed Potatoes' : {'Price' : 400, 'Category' : 'Side Dishes'}, 
            'Grilled Vegetables': {'Price' : 500 , 'Category' : 'Side Dishes'},
            'Garlic Bread' : { 'Price' : 400, 'Category' :'Side Dishes'},
            'Onion Rings' : { 'Price' : 500, 'Category' : 'Side Dishes'}
             }

    @staticmethod
    def item_price_category_unique_dict() -> dict [str, dict[str, int | str]]:
        # Dictionary with unique values 
        return {
            'Chicken Melt' : {'Price' : 800, 'Category' : 'Starters'},
            'French Fries' : {'Price' : 400, 'Category' : 'Starters'},
            'Beef Chili': {'Price': 700, 'Category': 'Starters'},
            'Nachos Grande': {'Price': 1000, 'Category': 'Starters'}, 
            'Grilled Chicken' : {'Price': 1500, 'Category': 'Main Dishes'},
            'Steak': {'Price': 2000, 'Category': 'Main Dishes'},
            'Pasta Alfredo': {'Price': 1200, 'Category': 'Main Dishes'},
            'Salmon': {'Price': 1800, 'Category':'Main Dishes'}, 
            'Vegetarian Platter': {'Price': 1400, 'Category': 'Main Dishes'}, 
            'Ice Cream' : { 'Price': 500, 'Category': 'Desserts'}, 
            'Fruit Salad' : { 'Price' : 400, 'Category' : 'Desserts'}, 
            'Cheesecake' : { 'Price' : 700, 'Category' : 'Desserts'}, 
            'Water' : {'Price' : 100, 'Category': 'Drinks'}, 
            'Side Salad' : { 'Price' : 300 , 'Category' : 'Side Dishes'}
             }


class CleanRestaurantSales:
    @staticmethod
    def convert_quantity_price_total(restaurant_sales):
        restaurant_sales = restaurant_sales.copy

        def convert_to_decimal_n_cent (y):
            if pd.isna(y):
                return pd.NA
            return int(Decimal(str(y)) * 100)

        try:
            restaurant_sales ['Quantity']  = pd.to_numeric(restaurant_sales['Quantity'], errors = 'coerce').astype("Int64")
            logger.info("Successfully converted Quantity column datatype to Integer")
        except Exception as e:
            logger.exception (f"Failed to convert Quantity column datatype to Integer: {e}")
            raise

        try:
            restaurant_sales ['Price'] = restaurant_sales ['Price'].apply(convert_to_decimal_n_cent)
            logger.info("Successfully centupled Price column.")

        except Exception as e:
            logger.exception(f"Failed to centuple Price column : {e}")
            raise 

        try:
            restaurant_sales ['Order Total'] = restaurant_sales ['Order Total'].apply(convert_to_decimal_n_cent)
            logger.info("Successfully centupled Order Total column.")

        except Exception as e:
            logger.exception (f"Failed to centuple Order Total column: {e}. ")
            raise

        return restaurant_sales

    @staticmethod
    def fill_price_quantity_order_total (restaurant_sales):
        restaurant_sales = restaurant_sales.copy

        # mask
        mask_price = restaurant_sales ['Price'].isna() & restaurant_sales ['Quantity'].notna() & restaurant_sales ['Order Total'].notna() 
        mask_quantity = restaurant_sales ['Quantity'].isna() & restaurant_sales ['Price'].notna() & restaurant_sales ['Order Total'].notna()
        mask_order_total = restaurant_sales ['Order Total'].isna() & restaurant_sales ['Price'].notna() & restaurant_sales ['Quantity'].notna()
        
        try:
            restaurant_sales.loc [mask_price, 'Price'] = restaurant_sales.loc [mask_price, 'Order Total'] / restaurant_sales.loc [mask_price, 'Quantity']
            logger.info(f"Successfully determined the value of price column in {mask_price.sum()} rows by dividing the values of Total Spent and Quantity")

        except Exception as e:
            logger.exception (f"Failed to input the values of Price column by the division of the values in Total Spent and Quantity: {e}")
            raise

        try:
            restaurant_sales.loc [mask_quantity, 'Quantity'] = restaurant_sales [mask_quantity, 'Order Total'] / restaurant_sales [mask_quantity, 'Price']
            logger.info(f"Successsfullly dertemined the value of Quantity column in {mask_quantity.sum} rows by the dividing Total Spent by Price")

        except Exception as e:
            logger.exception (f"Failed to in put the values of Quantity column by the division of the values in Total Spemt and Price columns.")
            raise 

        try:
            restaurant_sales [mask_order_total, 'Order Total'] = restaurant_sales [mask_order_total, 'Quantity']  * restaurant_sales [mask_order_total, 'Price']
            logger.info("Successfully dtermined the value of Order Total by the multiplication of Quantity and Price.")
        except Exception as e:
            logger.exception (f"Failed to input the value of Order Total column based on the multiplication of Quantity and Price")
            raise

        return restaurant_sales

    @staticmethod
    def fill_item_with_price_category(restaurant_sales):

        restaurant_sales = restaurant_sales.copy

        try: 
            # 1.0 We fill Item column with the unique values in category and Price 
            unique_lookup = { (v ['Price'], v ["Category"]) : k   for k, v in ReturnValues.item_price_category_unique_dict().items() }

            mask_item_field = restaurant_sales ['Item'].isna() & restaurant_sales ['Price'].notna() & restaurant_sales ['Category'].notna()

            price_category_series = pd.Series (
                list(zip(restaurant_sales.loc [ mask_item_field, 'Price'], restaurant_sales.loc [mask_item_field, 'Category'])),
                index = restaurant_sales.index[mask_item_field],
            )

            restaurant_sales [mask_item_field, 'Item'] = price_category_series.map(unique_lookup)

            logger.info(f"Filled Item column with the details in Price and Category in {mask_item_field.sum()} rows")
        
        except Exception as e:
            logger.exception(f"Failed to fill Item column with details in price and Category : {e}")
            raise

        return restaurant_sales 


    # Probabilistic approach - 1st level 
    @staticmethod
    def fill_item_with_prob_price_category(restaurant_sales):
        """"Fill the Item column with the Price and Category values of dictionary of reoccurring items. 
        We iterate between similar options. """

        # 
        restaurant_sales = restaurant_sales.copy
        try: 
            items_by_key = {}

            for k, v in ReturnValues.item_price_category_reoccuring_dict().items():
                key = (v['Price'], v['Category'])
                items_by_key.setdefault(key, []).append(k)

            rotations = {key: cycle (items) for key, items in items_by_key.items()}

            mask_item_price_category = restaurant_sales ['Item'].isna() & restaurant_sales ['Price'].notna() & restaurant_sales ['Category'].notna()

            for row_label in restaurant_sales.index[mask_item_price_category]:
                key = (restaurant_sales.at[row_label, 'Price'], restaurant_sales.at[row_label, 'Category'])

                if key in rotations:
                    restaurant_sales.at[row_label, 'Item'] = next (rotations[key])

            logger.info(f"Successfully filled item in {mask_item_price_category.sum()} by iterating between similar values in category and price")

        except Exception as e:
            logger.exception(f"Failed to fill Item by iterating between similar values in item_price_category_reoccuring_dict")
            raise

        return restaurant_sales 


    # Second Approach 
    @staticmethod
    def fill_item_price_qty_total(restaurant_sales):
        """"
        
        """
        restaurant_sales = restaurant_sales.copy

        # 1.1 For unique values - e only use category 
        try:
            lookup_dict = {v ['Category'] : k for k, v in ReturnValues.item_price_category_unique_dict().items()}

            item_unique_category = restaurant_sales ['Item'].isna() & restaurant_sales ['Price'].isna() & restaurant_sales ['Quantity'].isna() & restaurant_sales ['Order Total'].isna() & restaurant_sales ['Category'].notna()

            restaurant_sales.loc[item_unique_category, 'Item'] = restaurant_sales.loc [item_unique_category, 'Category'].map(lookup_dict)

            logger.info(f"Successfully filled {item_unique_category.sum()} rows by mapping unique values of Category to Item column.")
        
        except Exception as e:
            logger.exception(f"Failed to fill rows by mapping the unique values in catgory column to Item column : {e}")
            raise

        # 1.2 For reoccuring values 
        try:
            item_by_reoccuring_category = {}
            for k, v in ReturnValues.item_price_category_reoccuring_dict().items():
                item_by_reoccuring_category.setdefault(v['Category'], []).append(k)

            rotations = {category: cycle(itemised) for category, itemised in item_by_reoccuring_category.items() }

            mask_item_reocurring_category = restaurant_sales ['Item'].isna() & restaurant_sales ['Price'].isna() & restaurant_sales ['Quantity'].isna() & restaurant_sales ['Order Total'].isna() & restaurant_sales ['Category'].notna()

            for row_label in restaurant_sales.index[mask_item_reocurring_category]:
                y = restaurant_sales.at[row_label, 'Category']

                if y in rotations :
                    restaurant_sales.at[row_label, "Item"] = next (rotations[y])

            logger.info (f"Filled in {mask_item_reocurring_category.sum()}")

        except Exception as e:
            logger.exception(f"Failed to fill Item column by iterating betwen the reoccuring values in Category: {e}")
            raise


        # 2. 0 Fill Price based on Category and Item 
        try:
            lookup_price_unique_dict = {(k, v ['Category'] ): v ['Price'] for k, v in ReturnValues.item_price_category_full_dict().items()}

            mask_price = restaurant_sales ['Category'].notna() & restaurant_sales ['Item'].notna() & restaurant_sales ['Price'].isna() & restaurant_sales [
                'Quantity'].isna() & restaurant_sales ['Order Total'].isna()

            item_category_keys = pd.Series(
                list(zip(restaurant_sales.loc[mask_price, 'Item'], restaurant_sales.loc [mask_price, 'Category'])),
                index = restaurant_sales.index [mask_price],
            )

            restaurant_sales.loc [ mask_price, 'Price'] = item_category_keys.map(lookup_price_unique_dict)

            logger.info(f"Successfully filled Price column in {mask_price.sum()}rows  by mapping unique values in Category and Item column")
        
        except Exception as d:
            logger.exception(f"Failed to fill Price column by mapping unique values in Ctagory and Item columns: {d}. ")
            raise


        # 3.0 Fill Quantity
        try:
            value_with_distribution = restaurant_sales ['Quantity'].value_counts (normalize = True) 

            mask_empty_quantity = restaurant_sales ['Price'].notna() & restaurant_sales ['Quantity'].isna() & restaurant_sales ['Order Total'].isna()

            restaurant_sales.loc [mask_empty_quantity, 'Quantity'] = random.choices (
                value_with_distribution.index.tolist(),                                                             # This is the population (that is the all list of things to be picked from)
                weights = value_with_distribution.values,                                                           # Weights refer to the matching probability of being picked (how likely is a thing to be picked)
                k = int(mask_empty_quantity.sum())                                                                  # How many picks can we have 
            )

            logger.info(f"Successfully filled {mask_empty_quantity.sum()} cells in Quantity column with random values based on probability.")

        except Exception as e:
            logger.exception(f"Failed to fill Quantity columns with random values based on probability. {e} ")
            raise 

        # 4.0 Fill Order Total 
        try:
            mask_order_total = restaurant_sales ['Price'].notna() & restaurant_sales ['Quantity'].notna() & restaurant_sales ['Order Total'].isna()

            restaurant_sales.loc [mask_order_total, 'Order Total'] = restaurant_sales.loc [mask_order_total, 'Price'] * restaurant_sales [mask_order_total, 'Quantity']

            logger.info(f"Successfully filled {mask_order_total.sum()} rows in Order Total column by the multiplication of Price and Quantity after applying probability to them.")

        except Exception as e:
            logger.exception(f"Failed to fill Order Total column by the multipication of Price and Quantity after applying porbabilitistic approach to them.: {e}")
            raise


        return restaurant_sales


        




        


                


        
                        
