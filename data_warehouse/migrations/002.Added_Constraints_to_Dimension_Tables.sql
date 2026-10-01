-- ADDING CONSTRAINTS TO DIMENSION TABLES 

ALTER TABLE dimensions.item ADD CONSTRAINT item_name_unique UNIQUE (item_name);

ALTER TABLE dimensions.date ADD CONSTRAINT full_date_unique UNIQUE (full_date);

ALTER TABLE dimensions.payment_method ADD CONSTRAINT payment_method_name_unique UNIQUE (payment_method_name);

ALTER TABLE dimensions.location ADD CONSTRAINT location_name_unique UNIQUE (location_name);

ALTER TABLE dimensions.category ADD CONSTRAINT category_name_unique UNIQUE (category_name);

ALTER TABLE dimensions.diet ADD CONSTRAINT diet_name_unique UNIQUE (diet_name);


-- ADDING CONSTRAINTS TO FACT TABLES

ALTER TABLE facts.cafe_sales ADD CONSTRAINT transaction_id_unique UNIQUE (transaction_id);

