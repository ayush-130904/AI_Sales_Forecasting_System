CREATE DATABASE ecommerce_intelligence;
USE ecommerce_intelligence;

CREATE TABLE customers (
customer_id VARCHAR(50) PRIMARY KEY,
city VARCHAR(100),
state VARCHAR(50),
zip_code VARCHAR(20),
region VARCHAR(50)  
);

CREATE TABLE products (
product_id VARCHAR(50) PRIMARY KEY,
category VARCHAR(100),
name_length INT,
description_length INT,
photos_qty INT,
weight_g FLOAT,
price FLOAT
);

CREATE TABLE orders (
order_id VARCHAR(50) PRIMARY KEY,
customer_id VARCHAR(50),
status VARCHAR(30),
purchase_date DATETIME,
approved_date DATETIME,
delivered_date DATETIME,
estimated_delivery DATETIME,
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE sales (
sale_id INT AUTO_INCREMENT PRIMARY KEY,
order_id VARCHAR(50),
product_id VARCHAR(50),
quantity INT,
unit_price FLOAT,
freight_value FLOAT,
FOREIGN KEY (order_id) REFERENCES orders(order_id),
FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE predictions (
prediction_id INT AUTO_INCREMENT PRIMARY KEY,
month DATE,
orders_count INT,
unique_customers INT,
total_freight FLOAT,
predicted_revenue FLOAT,
acutal_revenue FLOAT,
created_at DATETIME DEFAULT CURRENT_TIMESTAMP 
);

CREATE TABLE ai_insights (
insight_id INT AUTO_INCREMENT PRIMARY KEY,
month DATE,
question TEXT,
insight_text TEXT,
revenue_change FLOAT,
created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE products ADD COLUMN avg_price FLOAT;
SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE sales;
TRUNCATE orders;
TRUNCATE customers;
TRUNCATE products;

SET FOREIGN_KEY_CHECKS = 1;