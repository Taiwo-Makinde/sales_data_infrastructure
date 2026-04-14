--
-- PostgreSQL database dump
--

\restrict 7d8oVvSd76gWqDiu5cMsy6fPRdNzJh51i2tAEMXrz3FDEl0jC6ZYtpXp1rheq0F

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: dimensions; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA dimensions;


ALTER SCHEMA dimensions OWNER TO postgres;

--
-- Name: facts; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA facts;


ALTER SCHEMA facts OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: category; Type: TABLE; Schema: dimensions; Owner: postgres
--

CREATE TABLE dimensions.category (
    category_key bigint NOT NULL,
    category_name character varying
);


ALTER TABLE dimensions.category OWNER TO postgres;

--
-- Name: category_category_key_seq; Type: SEQUENCE; Schema: dimensions; Owner: postgres
--

CREATE SEQUENCE dimensions.category_category_key_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE dimensions.category_category_key_seq OWNER TO postgres;

--
-- Name: category_category_key_seq; Type: SEQUENCE OWNED BY; Schema: dimensions; Owner: postgres
--

ALTER SEQUENCE dimensions.category_category_key_seq OWNED BY dimensions.category.category_key;


--
-- Name: date; Type: TABLE; Schema: dimensions; Owner: postgres
--

CREATE TABLE dimensions.date (
    date_key bigint NOT NULL,
    full_date date,
    day_of_week text,
    is_weekend boolean,
    month_number smallint,
    month_of_year text,
    quarter character(2),
    dateyear smallint
);


ALTER TABLE dimensions.date OWNER TO postgres;

--
-- Name: date_date_key_seq; Type: SEQUENCE; Schema: dimensions; Owner: postgres
--

CREATE SEQUENCE dimensions.date_date_key_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE dimensions.date_date_key_seq OWNER TO postgres;

--
-- Name: date_date_key_seq; Type: SEQUENCE OWNED BY; Schema: dimensions; Owner: postgres
--

ALTER SEQUENCE dimensions.date_date_key_seq OWNED BY dimensions.date.date_key;


--
-- Name: diet; Type: TABLE; Schema: dimensions; Owner: postgres
--

CREATE TABLE dimensions.diet (
    diet_key bigint NOT NULL,
    diet_name character varying
);


ALTER TABLE dimensions.diet OWNER TO postgres;

--
-- Name: diet_diet_key_seq; Type: SEQUENCE; Schema: dimensions; Owner: postgres
--

CREATE SEQUENCE dimensions.diet_diet_key_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE dimensions.diet_diet_key_seq OWNER TO postgres;

--
-- Name: diet_diet_key_seq; Type: SEQUENCE OWNED BY; Schema: dimensions; Owner: postgres
--

ALTER SEQUENCE dimensions.diet_diet_key_seq OWNED BY dimensions.diet.diet_key;


--
-- Name: item; Type: TABLE; Schema: dimensions; Owner: postgres
--

CREATE TABLE dimensions.item (
    item_key bigint NOT NULL,
    item_name character varying
);


ALTER TABLE dimensions.item OWNER TO postgres;

--
-- Name: item_item_key_seq; Type: SEQUENCE; Schema: dimensions; Owner: postgres
--

CREATE SEQUENCE dimensions.item_item_key_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE dimensions.item_item_key_seq OWNER TO postgres;

--
-- Name: item_item_key_seq; Type: SEQUENCE OWNED BY; Schema: dimensions; Owner: postgres
--

ALTER SEQUENCE dimensions.item_item_key_seq OWNED BY dimensions.item.item_key;


--
-- Name: location; Type: TABLE; Schema: dimensions; Owner: postgres
--

CREATE TABLE dimensions.location (
    location_key bigint NOT NULL,
    location_name character varying
);


ALTER TABLE dimensions.location OWNER TO postgres;

--
-- Name: location_location_key_seq; Type: SEQUENCE; Schema: dimensions; Owner: postgres
--

CREATE SEQUENCE dimensions.location_location_key_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE dimensions.location_location_key_seq OWNER TO postgres;

--
-- Name: location_location_key_seq; Type: SEQUENCE OWNED BY; Schema: dimensions; Owner: postgres
--

ALTER SEQUENCE dimensions.location_location_key_seq OWNED BY dimensions.location.location_key;


--
-- Name: payment_method; Type: TABLE; Schema: dimensions; Owner: postgres
--

CREATE TABLE dimensions.payment_method (
    payment_method_key bigint NOT NULL,
    payment_method_name character varying
);


ALTER TABLE dimensions.payment_method OWNER TO postgres;

--
-- Name: payment_method_payment_method_key_seq; Type: SEQUENCE; Schema: dimensions; Owner: postgres
--

CREATE SEQUENCE dimensions.payment_method_payment_method_key_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE dimensions.payment_method_payment_method_key_seq OWNER TO postgres;

--
-- Name: payment_method_payment_method_key_seq; Type: SEQUENCE OWNED BY; Schema: dimensions; Owner: postgres
--

ALTER SEQUENCE dimensions.payment_method_payment_method_key_seq OWNED BY dimensions.payment_method.payment_method_key;


--
-- Name: cafe_sales; Type: TABLE; Schema: facts; Owner: postgres
--

CREATE TABLE facts.cafe_sales (
    cafe_sales_key bigint NOT NULL,
    transaction_id character varying NOT NULL,
    date_key bigint NOT NULL,
    item_key bigint NOT NULL,
    payment_method_key bigint NOT NULL,
    location_key bigint NOT NULL,
    quantity integer,
    price_per_unit numeric(10,2),
    total_spent numeric(10,2)
);


ALTER TABLE facts.cafe_sales OWNER TO postgres;

--
-- Name: cafe_sales_cafe_sales_key_seq; Type: SEQUENCE; Schema: facts; Owner: postgres
--

CREATE SEQUENCE facts.cafe_sales_cafe_sales_key_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facts.cafe_sales_cafe_sales_key_seq OWNER TO postgres;

--
-- Name: cafe_sales_cafe_sales_key_seq; Type: SEQUENCE OWNED BY; Schema: facts; Owner: postgres
--

ALTER SEQUENCE facts.cafe_sales_cafe_sales_key_seq OWNED BY facts.cafe_sales.cafe_sales_key;


--
-- Name: restaurant_sales; Type: TABLE; Schema: facts; Owner: postgres
--

CREATE TABLE facts.restaurant_sales (
    restaurant_sales_key bigint NOT NULL,
    order_id character varying NOT NULL,
    customer_id character varying NOT NULL,
    date_key bigint NOT NULL,
    item_key bigint NOT NULL,
    payment_method_key bigint NOT NULL,
    location_key bigint NOT NULL,
    category_key bigint NOT NULL,
    diet_key bigint NOT NULL,
    price numeric(10,2),
    quantity integer,
    order_total numeric(10,2)
);


ALTER TABLE facts.restaurant_sales OWNER TO postgres;

--
-- Name: restaurant_sales_restaurant_sales_key_seq; Type: SEQUENCE; Schema: facts; Owner: postgres
--

CREATE SEQUENCE facts.restaurant_sales_restaurant_sales_key_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facts.restaurant_sales_restaurant_sales_key_seq OWNER TO postgres;

--
-- Name: restaurant_sales_restaurant_sales_key_seq; Type: SEQUENCE OWNED BY; Schema: facts; Owner: postgres
--

ALTER SEQUENCE facts.restaurant_sales_restaurant_sales_key_seq OWNED BY facts.restaurant_sales.restaurant_sales_key;


--
-- Name: retail_sales; Type: TABLE; Schema: facts; Owner: postgres
--

CREATE TABLE facts.retail_sales (
    retail_sales_key bigint NOT NULL,
    transaction_id character varying NOT NULL,
    customer_id character varying NOT NULL,
    date_key bigint NOT NULL,
    item_key bigint NOT NULL,
    payment_method_key bigint NOT NULL,
    location_key bigint NOT NULL,
    category_key bigint NOT NULL,
    price_per_unit numeric(4,2),
    quantity integer,
    total_spent numeric(4,2),
    discount_applied boolean
);


ALTER TABLE facts.retail_sales OWNER TO postgres;

--
-- Name: retail_sales_retail_sales_key_seq; Type: SEQUENCE; Schema: facts; Owner: postgres
--

CREATE SEQUENCE facts.retail_sales_retail_sales_key_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE facts.retail_sales_retail_sales_key_seq OWNER TO postgres;

--
-- Name: retail_sales_retail_sales_key_seq; Type: SEQUENCE OWNED BY; Schema: facts; Owner: postgres
--

ALTER SEQUENCE facts.retail_sales_retail_sales_key_seq OWNED BY facts.retail_sales.retail_sales_key;


--
-- Name: category category_key; Type: DEFAULT; Schema: dimensions; Owner: postgres
--

ALTER TABLE ONLY dimensions.category ALTER COLUMN category_key SET DEFAULT nextval('dimensions.category_category_key_seq'::regclass);


--
-- Name: date date_key; Type: DEFAULT; Schema: dimensions; Owner: postgres
--

ALTER TABLE ONLY dimensions.date ALTER COLUMN date_key SET DEFAULT nextval('dimensions.date_date_key_seq'::regclass);


--
-- Name: diet diet_key; Type: DEFAULT; Schema: dimensions; Owner: postgres
--

ALTER TABLE ONLY dimensions.diet ALTER COLUMN diet_key SET DEFAULT nextval('dimensions.diet_diet_key_seq'::regclass);


--
-- Name: item item_key; Type: DEFAULT; Schema: dimensions; Owner: postgres
--

ALTER TABLE ONLY dimensions.item ALTER COLUMN item_key SET DEFAULT nextval('dimensions.item_item_key_seq'::regclass);


--
-- Name: location location_key; Type: DEFAULT; Schema: dimensions; Owner: postgres
--

ALTER TABLE ONLY dimensions.location ALTER COLUMN location_key SET DEFAULT nextval('dimensions.location_location_key_seq'::regclass);


--
-- Name: payment_method payment_method_key; Type: DEFAULT; Schema: dimensions; Owner: postgres
--

ALTER TABLE ONLY dimensions.payment_method ALTER COLUMN payment_method_key SET DEFAULT nextval('dimensions.payment_method_payment_method_key_seq'::regclass);


--
-- Name: cafe_sales cafe_sales_key; Type: DEFAULT; Schema: facts; Owner: postgres
--

ALTER TABLE ONLY facts.cafe_sales ALTER COLUMN cafe_sales_key SET DEFAULT nextval('facts.cafe_sales_cafe_sales_key_seq'::regclass);


--
-- Name: restaurant_sales restaurant_sales_key; Type: DEFAULT; Schema: facts; Owner: postgres
--

ALTER TABLE ONLY facts.restaurant_sales ALTER COLUMN restaurant_sales_key SET DEFAULT nextval('facts.restaurant_sales_restaurant_sales_key_seq'::regclass);


--
-- Name: retail_sales retail_sales_key; Type: DEFAULT; Schema: facts; Owner: postgres
--

ALTER TABLE ONLY facts.retail_sales ALTER COLUMN retail_sales_key SET DEFAULT nextval('facts.retail_sales_retail_sales_key_seq'::regclass);


--
-- Data for Name: category; Type: TABLE DATA; Schema: dimensions; Owner: postgres
--

COPY dimensions.category (category_key, category_name) FROM stdin;
\.


--
-- Data for Name: date; Type: TABLE DATA; Schema: dimensions; Owner: postgres
--

COPY dimensions.date (date_key, full_date, day_of_week, is_weekend, month_number, month_of_year, quarter, dateyear) FROM stdin;
\.


--
-- Data for Name: diet; Type: TABLE DATA; Schema: dimensions; Owner: postgres
--

COPY dimensions.diet (diet_key, diet_name) FROM stdin;
\.


--
-- Data for Name: item; Type: TABLE DATA; Schema: dimensions; Owner: postgres
--

COPY dimensions.item (item_key, item_name) FROM stdin;
\.


--
-- Data for Name: location; Type: TABLE DATA; Schema: dimensions; Owner: postgres
--

COPY dimensions.location (location_key, location_name) FROM stdin;
\.


--
-- Data for Name: payment_method; Type: TABLE DATA; Schema: dimensions; Owner: postgres
--

COPY dimensions.payment_method (payment_method_key, payment_method_name) FROM stdin;
\.


--
-- Data for Name: cafe_sales; Type: TABLE DATA; Schema: facts; Owner: postgres
--

COPY facts.cafe_sales (cafe_sales_key, transaction_id, date_key, item_key, payment_method_key, location_key, quantity, price_per_unit, total_spent) FROM stdin;
\.


--
-- Data for Name: restaurant_sales; Type: TABLE DATA; Schema: facts; Owner: postgres
--

COPY facts.restaurant_sales (restaurant_sales_key, order_id, customer_id, date_key, item_key, payment_method_key, location_key, category_key, diet_key, price, quantity, order_total) FROM stdin;
\.


--
-- Data for Name: retail_sales; Type: TABLE DATA; Schema: facts; Owner: postgres
--

COPY facts.retail_sales (retail_sales_key, transaction_id, customer_id, date_key, item_key, payment_method_key, location_key, category_key, price_per_unit, quantity, total_spent, discount_applied) FROM stdin;
\.


--
-- Name: category_category_key_seq; Type: SEQUENCE SET; Schema: dimensions; Owner: postgres
--

SELECT pg_catalog.setval('dimensions.category_category_key_seq', 1, false);


--
-- Name: date_date_key_seq; Type: SEQUENCE SET; Schema: dimensions; Owner: postgres
--

SELECT pg_catalog.setval('dimensions.date_date_key_seq', 1, false);


--
-- Name: diet_diet_key_seq; Type: SEQUENCE SET; Schema: dimensions; Owner: postgres
--

SELECT pg_catalog.setval('dimensions.diet_diet_key_seq', 1, false);


--
-- Name: item_item_key_seq; Type: SEQUENCE SET; Schema: dimensions; Owner: postgres
--

SELECT pg_catalog.setval('dimensions.item_item_key_seq', 1, false);


--
-- Name: location_location_key_seq; Type: SEQUENCE SET; Schema: dimensions; Owner: postgres
--

SELECT pg_catalog.setval('dimensions.location_location_key_seq', 1, false);


--
-- Name: payment_method_payment_method_key_seq; Type: SEQUENCE SET; Schema: dimensions; Owner: postgres
--

SELECT pg_catalog.setval('dimensions.payment_method_payment_method_key_seq', 1, false);


--
-- Name: cafe_sales_cafe_sales_key_seq; Type: SEQUENCE SET; Schema: facts; Owner: postgres
--

SELECT pg_catalog.setval('facts.cafe_sales_cafe_sales_key_seq', 1, false);


--
-- Name: restaurant_sales_restaurant_sales_key_seq; Type: SEQUENCE SET; Schema: facts; Owner: postgres
--

SELECT pg_catalog.setval('facts.restaurant_sales_restaurant_sales_key_seq', 1, false);


--
-- Name: retail_sales_retail_sales_key_seq; Type: SEQUENCE SET; Schema: facts; Owner: postgres
--

SELECT pg_catalog.setval('facts.retail_sales_retail_sales_key_seq', 1, false);


--
-- Name: category category_pkey; Type: CONSTRAINT; Schema: dimensions; Owner: postgres
--

ALTER TABLE ONLY dimensions.category
    ADD CONSTRAINT category_pkey PRIMARY KEY (category_key);


--
-- Name: date date_pkey; Type: CONSTRAINT; Schema: dimensions; Owner: postgres
--

ALTER TABLE ONLY dimensions.date
    ADD CONSTRAINT date_pkey PRIMARY KEY (date_key);


--
-- Name: diet diet_pkey; Type: CONSTRAINT; Schema: dimensions; Owner: postgres
--

ALTER TABLE ONLY dimensions.diet
    ADD CONSTRAINT diet_pkey PRIMARY KEY (diet_key);


--
-- Name: item item_pkey; Type: CONSTRAINT; Schema: dimensions; Owner: postgres
--

ALTER TABLE ONLY dimensions.item
    ADD CONSTRAINT item_pkey PRIMARY KEY (item_key);


--
-- Name: location location_pkey; Type: CONSTRAINT; Schema: dimensions; Owner: postgres
--

ALTER TABLE ONLY dimensions.location
    ADD CONSTRAINT location_pkey PRIMARY KEY (location_key);


--
-- Name: payment_method payment_method_pkey; Type: CONSTRAINT; Schema: dimensions; Owner: postgres
--

ALTER TABLE ONLY dimensions.payment_method
    ADD CONSTRAINT payment_method_pkey PRIMARY KEY (payment_method_key);


--
-- Name: cafe_sales cafe_sales_pkey; Type: CONSTRAINT; Schema: facts; Owner: postgres
--

ALTER TABLE ONLY facts.cafe_sales
    ADD CONSTRAINT cafe_sales_pkey PRIMARY KEY (cafe_sales_key);


--
-- Name: restaurant_sales restaurant_sales_pkey; Type: CONSTRAINT; Schema: facts; Owner: postgres
--

ALTER TABLE ONLY facts.restaurant_sales
    ADD CONSTRAINT restaurant_sales_pkey PRIMARY KEY (restaurant_sales_key);


--
-- Name: retail_sales retail_sales_pkey; Type: CONSTRAINT; Schema: facts; Owner: postgres
--

ALTER TABLE ONLY facts.retail_sales
    ADD CONSTRAINT retail_sales_pkey PRIMARY KEY (retail_sales_key);


--
-- Name: cafe_sales cafe_sales_date_key_fkey; Type: FK CONSTRAINT; Schema: facts; Owner: postgres
--

ALTER TABLE ONLY facts.cafe_sales
    ADD CONSTRAINT cafe_sales_date_key_fkey FOREIGN KEY (date_key) REFERENCES dimensions.date(date_key) ON DELETE RESTRICT;


--
-- Name: cafe_sales cafe_sales_item_key_fkey; Type: FK CONSTRAINT; Schema: facts; Owner: postgres
--

ALTER TABLE ONLY facts.cafe_sales
    ADD CONSTRAINT cafe_sales_item_key_fkey FOREIGN KEY (item_key) REFERENCES dimensions.item(item_key) ON DELETE RESTRICT;


--
-- Name: cafe_sales cafe_sales_location_key_fkey; Type: FK CONSTRAINT; Schema: facts; Owner: postgres
--

ALTER TABLE ONLY facts.cafe_sales
    ADD CONSTRAINT cafe_sales_location_key_fkey FOREIGN KEY (location_key) REFERENCES dimensions.location(location_key) ON DELETE RESTRICT;


--
-- Name: cafe_sales cafe_sales_payment_method_key_fkey; Type: FK CONSTRAINT; Schema: facts; Owner: postgres
--

ALTER TABLE ONLY facts.cafe_sales
    ADD CONSTRAINT cafe_sales_payment_method_key_fkey FOREIGN KEY (payment_method_key) REFERENCES dimensions.payment_method(payment_method_key) ON DELETE RESTRICT;


--
-- Name: restaurant_sales restaurant_sales_category_key_fkey; Type: FK CONSTRAINT; Schema: facts; Owner: postgres
--

ALTER TABLE ONLY facts.restaurant_sales
    ADD CONSTRAINT restaurant_sales_category_key_fkey FOREIGN KEY (category_key) REFERENCES dimensions.category(category_key) ON DELETE RESTRICT;


--
-- Name: restaurant_sales restaurant_sales_date_key_fkey; Type: FK CONSTRAINT; Schema: facts; Owner: postgres
--

ALTER TABLE ONLY facts.restaurant_sales
    ADD CONSTRAINT restaurant_sales_date_key_fkey FOREIGN KEY (date_key) REFERENCES dimensions.date(date_key) ON DELETE RESTRICT;


--
-- Name: restaurant_sales restaurant_sales_diet_key_fkey; Type: FK CONSTRAINT; Schema: facts; Owner: postgres
--

ALTER TABLE ONLY facts.restaurant_sales
    ADD CONSTRAINT restaurant_sales_diet_key_fkey FOREIGN KEY (diet_key) REFERENCES dimensions.diet(diet_key) ON DELETE RESTRICT;


--
-- Name: restaurant_sales restaurant_sales_item_key_fkey; Type: FK CONSTRAINT; Schema: facts; Owner: postgres
--

ALTER TABLE ONLY facts.restaurant_sales
    ADD CONSTRAINT restaurant_sales_item_key_fkey FOREIGN KEY (item_key) REFERENCES dimensions.item(item_key) ON DELETE RESTRICT;


--
-- Name: restaurant_sales restaurant_sales_location_key_fkey; Type: FK CONSTRAINT; Schema: facts; Owner: postgres
--

ALTER TABLE ONLY facts.restaurant_sales
    ADD CONSTRAINT restaurant_sales_location_key_fkey FOREIGN KEY (location_key) REFERENCES dimensions.location(location_key) ON DELETE RESTRICT;


--
-- Name: restaurant_sales restaurant_sales_payment_method_key_fkey; Type: FK CONSTRAINT; Schema: facts; Owner: postgres
--

ALTER TABLE ONLY facts.restaurant_sales
    ADD CONSTRAINT restaurant_sales_payment_method_key_fkey FOREIGN KEY (payment_method_key) REFERENCES dimensions.payment_method(payment_method_key) ON DELETE RESTRICT;


--
-- Name: retail_sales retail_sales_category_key_fkey; Type: FK CONSTRAINT; Schema: facts; Owner: postgres
--

ALTER TABLE ONLY facts.retail_sales
    ADD CONSTRAINT retail_sales_category_key_fkey FOREIGN KEY (category_key) REFERENCES dimensions.category(category_key) ON DELETE RESTRICT;


--
-- Name: retail_sales retail_sales_date_key_fkey; Type: FK CONSTRAINT; Schema: facts; Owner: postgres
--

ALTER TABLE ONLY facts.retail_sales
    ADD CONSTRAINT retail_sales_date_key_fkey FOREIGN KEY (date_key) REFERENCES dimensions.date(date_key) ON DELETE RESTRICT;


--
-- Name: retail_sales retail_sales_item_key_fkey; Type: FK CONSTRAINT; Schema: facts; Owner: postgres
--

ALTER TABLE ONLY facts.retail_sales
    ADD CONSTRAINT retail_sales_item_key_fkey FOREIGN KEY (item_key) REFERENCES dimensions.item(item_key) ON DELETE RESTRICT;


--
-- Name: retail_sales retail_sales_location_key_fkey; Type: FK CONSTRAINT; Schema: facts; Owner: postgres
--

ALTER TABLE ONLY facts.retail_sales
    ADD CONSTRAINT retail_sales_location_key_fkey FOREIGN KEY (location_key) REFERENCES dimensions.location(location_key) ON DELETE RESTRICT;


--
-- Name: retail_sales retail_sales_payment_method_key_fkey; Type: FK CONSTRAINT; Schema: facts; Owner: postgres
--

ALTER TABLE ONLY facts.retail_sales
    ADD CONSTRAINT retail_sales_payment_method_key_fkey FOREIGN KEY (payment_method_key) REFERENCES dimensions.payment_method(payment_method_key) ON DELETE RESTRICT;


--
-- PostgreSQL database dump complete
--

\unrestrict 7d8oVvSd76gWqDiu5cMsy6fPRdNzJh51i2tAEMXrz3FDEl0jC6ZYtpXp1rheq0F

