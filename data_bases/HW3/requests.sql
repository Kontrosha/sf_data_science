-- Запрос 1. Распределение клиентов по сферам деятельности:
SELECT job_industry_category, COUNT(*) AS customer_count
FROM customer
GROUP BY job_industry_category
ORDER BY customer_count DESC;

-- Запрос 2. Сумма транзакций по месяцам и сферам деятельности:
SELECT DATE_TRUNC('month', transaction_date)::date AS month,
       c.job_industry_category,
       SUM(t.list_price) AS total_transaction_amount
FROM transaction t
JOIN customer c ON t.customer_id = c.customer_id
GROUP BY month, c.job_industry_category
ORDER BY month, c.job_industry_category;

-- Запрос 3. Количество онлайн-заказов для брендов от клиентов из сферы IT:
SELECT brand, COUNT(*) AS online_order_count
FROM transaction
JOIN customer ON transaction.customer_id = customer.customer_id
WHERE customer.job_industry_category = 'IT' AND transaction.online_order = 'True' AND transaction.order_status = 'Approved'
GROUP BY brand;

-- Запрос 4. Сумма, максимум, минимум и количество транзакций для всех клиентов:
SELECT customer_id, SUM(list_price) AS total, MAX(list_price) AS max_price,
       MIN(list_price) AS min_price, COUNT(*) AS transaction_count
FROM transaction
GROUP BY customer_id
ORDER BY total DESC, transaction_count DESC;

SELECT DISTINCT customer_id,
       SUM(list_price) OVER (PARTITION BY customer_id) AS total,
       MAX(list_price) OVER (PARTITION BY customer_id) AS max_price,
       MIN(list_price) OVER (PARTITION BY customer_id) AS min_price,
       COUNT(*) OVER (PARTITION BY customer_id) AS transaction_count
FROM transaction
ORDER BY total DESC, transaction_count DESC;

-- Запрос 5. Клиенты с минимальной/максимальной суммой транзакций:
SELECT first_name, last_name
FROM customer
WHERE customer_id = (
  SELECT customer_id
  FROM transaction
  GROUP BY customer_id
  ORDER BY SUM(list_price) ASC
  LIMIT 1
);

SELECT first_name, last_name
FROM customer
WHERE customer_id = (
  SELECT customer_id
  FROM transaction
  GROUP BY customer_id
  ORDER BY SUM(list_price) DESC
  LIMIT 1
);

-- Запрос 6. Первые транзакции клиентов:
WITH RankedTransactions AS (
    SELECT
        t.customer_id,
        t.transaction_id,
        t.transaction_date,
        ROW_NUMBER() OVER (
            PARTITION BY t.customer_id
            ORDER BY t.transaction_date ASC
        ) AS rn
    FROM transaction t
)
SELECT
    rt.customer_id,
    rt.transaction_id,
    rt.transaction_date
FROM RankedTransactions rt
WHERE rt.rn = 1;


-- Запрос 7. Клиенты с максимальным интервалом между транзакциями:
WITH CustomerTransactions AS (
    SELECT
        c.customer_id,
        c.first_name,
        c.last_name,
        c.job_title,
        t.transaction_date,
        LEAD(t.transaction_date) OVER (
            PARTITION BY c.customer_id
            ORDER BY t.transaction_date
        ) AS next_transaction_date
    FROM customer c
    JOIN transaction t ON c.customer_id = t.customer_id
),
TransactionIntervals AS (
    SELECT
        customer_id,
        first_name,
        last_name,
        job_title,
        transaction_date,
        next_transaction_date,
        next_transaction_date - transaction_date AS interval_days
    FROM CustomerTransactions
    WHERE next_transaction_date IS NOT NULL
)
SELECT
    first_name,
    last_name,
    job_title,
    MAX(interval_days) OVER () AS max_interval_days
FROM TransactionIntervals
WHERE interval_days = (SELECT MAX(interval_days) FROM TransactionIntervals);
