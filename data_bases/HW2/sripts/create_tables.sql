CREATE TABLE customer
(
    customer_id           INT4 PRIMARY KEY,
    first_name            VARCHAR(50),
    last_name             VARCHAR(50),
    gender                VARCHAR(30),
    DOB                   VARCHAR(50),
    job_title             VARCHAR(50),
    job_industry_category VARCHAR(50),
    wealth_segment        VARCHAR(50),
    deceased_indicator    VARCHAR(50),
    owns_car              VARCHAR(30),
    address               VARCHAR(50),
    postcode              VARCHAR(30),
    state                 VARCHAR(30),
    country               VARCHAR(30),
    property_valuation    INT4
);

CREATE TABLE transaction
(
    transaction_id     INT4 PRIMARY KEY,
    product_id         INT4,
    customer_id        INT4,
    transaction_date   VARCHAR(30),
    online_order       VARCHAR(30),
    order_status       VARCHAR(30),
    brand              VARCHAR(30),
    product_line       VARCHAR(30),
    product_class      VARCHAR(30),
    product_size       VARCHAR(30),
    list_price_char    VARCHAR(30),
    standard_cost_char VARCHAR(30),
    FOREIGN KEY (customer_id) REFERENCES customer (customer_id)
);
