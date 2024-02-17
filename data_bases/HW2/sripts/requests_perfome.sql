-- 1. Вывести все уникальные бренды, у которых стандартная стоимость выше 1500 долларов.
SELECT DISTINCT brand
FROM transaction
WHERE standard_cost > 1500;

-- 2. Вывести все подтвержденные транзакции за период '2017-04-01' по '2017-04-09' включительно.
SELECT *
FROM transaction
WHERE order_status = 'Approved'
AND transaction_date BETWEEN '2017-04-01' AND '2017-04-09';

-- 3. Вывести все профессии у клиентов из сферы IT или Financial Services, которые начинаются с фразы 'Senior'.
SELECT DISTINCT job_title
FROM customer
WHERE (job_industry_category = 'IT' OR job_industry_category = 'Financial Services')
AND job_title LIKE 'Senior%';

-- 4. Вывести все бренды, которые закупают клиенты, работающие в сфере Financial Services
SELECT DISTINCT t.brand
FROM transaction t
JOIN customer c ON t.customer_id = c.customer_id
WHERE c.job_industry_category = 'Financial Services';

-- 5. Вывести 10 клиентов, которые оформили онлайн-заказ продукции из брендов 'Giant Bicycles', 'Norco Bicycles', 'Trek Bicycles'.
SELECT DISTINCT c.customer_id, c.first_name, c.last_name
FROM customer c
JOIN transaction t ON c.customer_id = t.customer_id
WHERE t.brand IN ('Giant Bicycles', 'Norco Bicycles', 'Trek Bicycles') AND t.online_order = 'True'
LIMIT 10;

-- 6. Вывести всех клиентов, у которых нет транзакций.
SELECT c.customer_id, c.first_name, c.last_name
FROM customer c
LEFT JOIN transaction t ON c.customer_id = t.customer_id
WHERE t.transaction_id IS NULL;

-- 7. Вывести всех клиентов из IT, у которых транзакции с максимальной стандартной стоимостью.
WITH MaxCost AS (
    SELECT MAX(standard_cost) AS max_standard_cost
    FROM transaction
)
SELECT c.customer_id, c.first_name, c.last_name, t.standard_cost
FROM customer c
JOIN transaction t ON c.customer_id = t.customer_id
JOIN MaxCost mc ON t.standard_cost = mc.max_standard_cost
WHERE c.job_industry_category = 'IT';

-- 8. Вывести всех клиентов из сферы IT и Health, у которых есть подтвержденные транзакции за период '2017-07-07' по '2017-07-17'.
SELECT DISTINCT c.customer_id, c.first_name, c.last_name
FROM customer c
JOIN transaction t ON c.customer_id = t.customer_id
WHERE c.job_industry_category IN ('IT', 'Health')
AND t.order_status = 'Approved'
AND t.transaction_date BETWEEN '2017-07-07' AND '2017-07-17';

