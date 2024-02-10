CREATE TABLE Addresses (
    address_id INT PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    postcode INT NOT NULL,
    state VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    property_valuation INT NOT NULL
);
CREATE TABLE Customers (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255),
    gender VARCHAR(50) NOT NULL,
    DOB DATE,
    job_title VARCHAR(255),
    job_industry_category VARCHAR(255),
    wealth_segment VARCHAR(255) NOT NULL,
    deceased_indicator CHAR(1) NOT NULL,
    owns_car BOOLEAN NOT NULL,
    address_id INT,
    FOREIGN KEY (address_id) REFERENCES Addresses(address_id)
);
CREATE TABLE Products (
    product_id INT PRIMARY KEY,
    brand VARCHAR(255) NOT NULL,
    product_line VARCHAR(255) NOT NULL,
    product_class VARCHAR(255) NOT NULL,
    product_size VARCHAR(255) NOT NULL,
    list_price DECIMAL NOT NULL,
    standard_cost DECIMAL NOT NULL
);
CREATE TABLE Transactions (
    transaction_id INT PRIMARY KEY,
    product_id INT NOT NULL,
    customer_id INT NOT NULL,
    transaction_date DATE NOT NULL,
    online_order BOOLEAN,
    order_status VARCHAR(255) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);