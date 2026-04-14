-- Creating Schema for dimension tables and fact tables

CREATE SCHEMA dimensions;

CREATE SCHEMA facts;

-- Create dimension tables within the dimension schema. 
-- Compound dimension tables 
CREATE TABLE dimensions.item (
			item_key BIGSERIAL PRIMARY KEY,
			item_name VARCHAR
			);

CREATE TABLE dimensions.date(
			date_key BIGSERIAL PRIMARY KEY,
			full_date DATE,
			day_of_week TEXT,
			is_weekend BOOLEAN,
			month_number SMALLINT,
			month_of_year TEXT,
			quarter CHAR(2),
			dateyear SMALLINT
			);

CREATE TABLE dimensions.payment_method (
			payment_method_key BIGSERIAL PRIMARY KEY,
			payment_method_name VARCHAR
			);
			
CREATE TABLE dimensions.location (
			location_key BIGSERIAL PRIMARY KEY,
			location_name VARCHAR
			);

-- Dimension tables unique to restaurant sales and retail store sales fact tables

CREATE TABLE dimensions.category (
			category_key BIGSERIAL PRIMARY KEY,
			category_name VARCHAR
			);

-- Dimension table unique to restaurant sales fact table only
CREATE TABLE dimensions.diet (
			diet_key BIGSERIAL PRIMARY KEY,
			diet_name VARCHAR
			);

-- Let's do the fact tables for cafe_sales, restaurant_sales and retail sales 
CREATE TABLE facts.cafe_sales (
			-- Primary key (surrogates) for fact table 
			cafe_sales_key BIGSERIAL PRIMARY KEY,
			-- Natural key (unique identifier derived from source data)
			transaction_id VARCHAR NOT NULL, 
			-- Foreign keys (surrogate keys from dimension tables)
			date_key BIGINT NOT NULL REFERENCES dimensions.date(date_key) ON DELETE RESTRICT, 
			item_key BIGINT NOT NULL REFERENCES dimensions.item(item_key) ON DELETE RESTRICT, 
			payment_method_key BIGINT NOT NULL REFERENCES dimensions.payment_method (payment_method_key) ON DELETE RESTRICT,
			location_key BIGINT NOT NULL REFERENCES dimensions.location (location_key) ON DELETE RESTRICT,
			-- Qualitative, numerical data (native to this fact table)
			quantity INT,
			price_per_unit NUMERIC (10,2),
			total_spent NUMERIC (10,2)
			);

CREATE TABLE facts.restaurant_sales (
			-- Primary keys (surrogates) for this fact table
			restaurant_sales_key BIGSERIAL PRIMARY KEY,
			-- Natural key (unique identifier derived from source data)
			order_id VARCHAR NOT NULL, 
			customer_id VARCHAR NOT NULL,
			-- Foreign keys (surrogate keys from dimension tables)
			date_key BIGINT NOT NULL REFERENCES dimensions.date(date_key) ON DELETE RESTRICT, 
			item_key BIGINT NOT NULL REFERENCES dimensions.item(item_key) ON DELETE RESTRICT, 
			payment_method_key BIGINT NOT NULL REFERENCES dimensions.payment_method (payment_method_key) ON DELETE RESTRICT,
			location_key BIGINT NOT NULL REFERENCES dimensions.location (location_key) ON DELETE RESTRICT,
			-- Foreign keys (surrogate keys from dimension tables)
			category_key BIGINT NOT NULL REFERENCES dimensions.category (category_key) ON DELETE RESTRICT, 
			diet_key BIGINT NOT NULL REFERENCES dimensions.diet (diet_key) ON DELETE RESTRICT,
			-- Qualitative, numerical data (native to this fact table)
			price NUMERIC (10,2),
			quantity INT,
			order_total NUMERIC (10,2)
			);


CREATE TABLE facts.retail_sales (
			-- Primary key (surrogates) for this fact table 
			retail_sales_key BIGSERIAL PRIMARY KEY,
			-- Natural key (unique identifier derived from source data)
			transaction_id VARCHAR NOT NULL, 
			customer_id VARCHAR NOT NULL,
			-- Foreign keys (surrogate keys from dimension tables)
			date_key BIGINT NOT NULL REFERENCES dimensions.date(date_key) ON DELETE RESTRICT, 
			item_key BIGINT NOT NULL REFERENCES dimensions.item(item_key) ON DELETE RESTRICT, 
			payment_method_key BIGINT NOT NULL REFERENCES dimensions.payment_method (payment_method_key) ON DELETE RESTRICT,
			location_key BIGINT NOT NULL REFERENCES dimensions.location (location_key) ON DELETE RESTRICT,
			-- Foreign keys (surrogate keys from dimension tables)
			category_key BIGINT NOT NULL REFERENCES dimensions.category (category_key) ON DELETE RESTRICT, 
			-- Qualitative, numerical data (native to this fact table)
			price_per_unit NUMERIC (4,2),
			quantity INT,
			total_spent NUMERIC (4,2),
			discount_applied BOOLEAN
			);