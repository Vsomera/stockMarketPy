-- Create the storage database if it doesn't exist
CREATE DATABASE IF NOT EXISTS storage;

-- Switch to the 'analytics' database
USE storage;

-- Create the orders table
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    trace_id VARCHAR(255) NOT NULL,
    stock_id VARCHAR(255) NOT NULL,
    order_type VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    date_created VARCHAR(100) NOT NULL
);

-- Create the stocks table
CREATE TABLE IF NOT EXISTS stocks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    trace_id VARCHAR(255) NOT NULL,
    symbol VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    purchase_price DECIMAL(10, 2) NOT NULL,
    date_created VARCHAR(100) NOT NULL
);