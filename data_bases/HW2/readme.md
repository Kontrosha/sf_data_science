
# Итоги работы

## Содержание
- [Итоги работы](#итоги-работы)
  - [Содержание](#содержание)
  - [Содержание проекта](#содержание-проекта)
  - [Создание таблиц](#создание-таблиц)
    - [Таблица `customer`](#таблица-customer)
    - [Таблица `transaction`](#таблица-transaction)
  - [Преобразование колонок](#преобразование-колонок)
  - [Выполнение скриптов и комментарии](#выполнение-скриптов-и-комментарии)
    - [Запросы 1-8](#запросы-1-8)
      - [Запрос 1. Вывести все уникальные бренды, у которых стандартная стоимость выше 1500 долларов.](#запрос-1-вывести-все-уникальные-бренды-у-которых-стандартная-стоимость-выше-1500-долларов)
      - [Запрос 2. Вывести все подтвержденные транзакции за период '2017-04-01' по '2017-04-09' включительно.](#запрос-2-вывести-все-подтвержденные-транзакции-за-период-2017-04-01-по-2017-04-09-включительно)
      - [Запрос 3. Вывести все профессии у клиентов из сферы IT или Financial Services, которые начинаются с фразы 'Senior'.](#запрос-3-вывести-все-профессии-у-клиентов-из-сферы-it-или-financial-services-которые-начинаются-с-фразы-senior)
      - [Запрос 4. Вывести все бренды, которые закупают клиенты, работающие в сфере Financial Services](#запрос-4-вывести-все-бренды-которые-закупают-клиенты-работающие-в-сфере-financial-services)
      - [Запрос 5. Вывести 10 клиентов, которые оформили онлайн-заказ продукции из брендов 'Giant Bicycles', 'Norco Bicycles', 'Trek Bicycles'.](#запрос-5-вывести-10-клиентов-которые-оформили-онлайн-заказ-продукции-из-брендов-giant-bicycles-norco-bicycles-trek-bicycles)
      - [Запрос 6. Вывести всех клиентов, у которых нет транзакций.](#запрос-6-вывести-всех-клиентов-у-которых-нет-транзакций)
      - [Запрос 7. Вывести всех клиентов из IT, у которых транзакции с максимальной стандартной стоимостью.](#запрос-7-вывести-всех-клиентов-из-it-у-которых-транзакции-с-максимальной-стандартной-стоимостью)
      - [Запрос 8. Вывести всех клиентов из сферы IT и Health, у которых есть подтвержденные транзакции за период '2017-07-07' по '2017-07-17'.](#запрос-8-вывести-всех-клиентов-из-сферы-it-и-health-у-которых-есть-подтвержденные-транзакции-за-период-2017-07-07-по-2017-07-17)
  - [Краткие выводы](#краткие-выводы)

## Содержание проекта
Ниже представлена структура и содержание папок проекта:
- **screenshots** содержит скриншоты с заполнеными таблицами и их структурой
- **scripts** содержит все скрипты на SQL

## Создание таблиц
Скрипты для создания таблиц `customer` и `transaction`.

### Таблица `customer`
```sql
CREATE TABLE customer (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    gender VARCHAR(50),
    DOB DATE,
    job_title VARCHAR(255),
    job_industry_category VARCHAR(255),
    wealth_segment VARCHAR(255),
    deceased_indicator CHAR(1),
    owns_car BOOLEAN,
    address VARCHAR(255),
    postcode CHAR(5),
    state VARCHAR(255),
    country VARCHAR(255),
    property_valuation INT
);
```


### Таблица `transaction`
```sql
CREATE TABLE transaction (
    transaction_id SERIAL PRIMARY KEY,
    product_id INT,
    customer_id INT,
    transaction_date DATE,
    online_order BOOLEAN,
    order_status VARCHAR(50),
    brand VARCHAR(255),
    product_line VARCHAR(255),
    product_class VARCHAR(50),
    product_size VARCHAR(50),
    list_price NUMERIC(10, 2),
    standard_cost NUMERIC(10, 2),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);
```
После создания таблицы были заполнены из файлов [customers.csv]() и [transaction.csv]() с помощью встроенного функционала JetBrains DataGrip: *Table -> Context Menu -> Import/Export -> Import Data from file(s)...*

Итоговый вид таблиц:
- customers
- transaction

## Преобразование колонок
Преобразование колонок `list_price_char`, `standard_cost_char` и `transaction_date` для корректной работы с данными.

```sql
-- Преобразования для list_price и standard_cost
ALTER TABLE transaction ADD COLUMN list_price float4;
UPDATE transaction
SET list_price = CAST(REPLACE(list_price_char, ',', '.') AS float4);
ALTER TABLE transaction DROP COLUMN list_price_char;

ALTER TABLE transaction ADD COLUMN standard_cost float4;
UPDATE transaction
SET standard_cost = CAST(REPLACE(standard_cost_char, ',', '.') AS float4);
ALTER TABLE transaction DROP COLUMN standard_cost_char;

-- Преобразование transaction_date из VARCHAR(30) в DATE
ALTER TABLE transaction ADD COLUMN transaction_date_new DATE;
UPDATE transaction
SET transaction_date_new = TO_DATE(transaction_date, 'YYYY-MM-DD');
ALTER TABLE transaction DROP COLUMN transaction_date;
ALTER TABLE transaction RENAME COLUMN transaction_date_new TO transaction_date;
```

## Выполнение скриптов и комментарии
Запросы для выполнения различных задач по анализу данных.

### Запросы 1-8
#### Запрос 1. Вывести все уникальные бренды, у которых стандартная стоимость выше 1500 долларов.
``` sql
SELECT DISTINCT brand
FROM transaction
WHERE standard_cost > 1500;
```
---
#### Запрос 2. Вывести все подтвержденные транзакции за период '2017-04-01' по '2017-04-09' включительно.
``` sql
SELECT *
FROM transaction
WHERE order_status = 'Approved'
AND transaction_date BETWEEN '2017-04-01' AND '2017-04-09';
```
---
#### Запрос 3. Вывести все профессии у клиентов из сферы IT или Financial Services, которые начинаются с фразы 'Senior'.
``` sql
SELECT DISTINCT job_title
FROM customer
WHERE (job_industry_category = 'IT' OR job_industry_category = 'Financial Services')
AND job_title LIKE 'Senior%';
```
---

#### Запрос 4. Вывести все бренды, которые закупают клиенты, работающие в сфере Financial Services
``` sql
SELECT DISTINCT t.brand
FROM transaction t
JOIN customer c ON t.customer_id = c.customer_id
WHERE c.job_industry_category = 'Financial Services';
```
---
#### Запрос 5. Вывести 10 клиентов, которые оформили онлайн-заказ продукции из брендов 'Giant Bicycles', 'Norco Bicycles', 'Trek Bicycles'.
``` sql
SELECT DISTINCT c.customer_id, c.first_name, c.last_name
FROM customer c
JOIN transaction t ON c.customer_id = t.customer_id
WHERE t.brand IN ('Giant Bicycles', 'Norco Bicycles', 'Trek Bicycles') AND t.online_order = 'True'
LIMIT 10;
```
---
#### Запрос 6. Вывести всех клиентов, у которых нет транзакций.
``` sql
SELECT c.customer_id, c.first_name, c.last_name
FROM customer c
LEFT JOIN transaction t ON c.customer_id = t.customer_id
WHERE t.transaction_id IS NULL;
```
---
#### Запрос 7. Вывести всех клиентов из IT, у которых транзакции с максимальной стандартной стоимостью.
``` sql
WITH MaxCost AS (
    SELECT MAX(standard_cost) AS max_standard_cost
    FROM transaction
)
SELECT c.customer_id, c.first_name, c.last_name, t.standard_cost
FROM customer c
JOIN transaction t ON c.customer_id = t.customer_id
JOIN MaxCost mc ON t.standard_cost = mc.max_standard_cost
WHERE c.job_industry_category = 'IT';
```
---
#### Запрос 8. Вывести всех клиентов из сферы IT и Health, у которых есть подтвержденные транзакции за период '2017-07-07' по '2017-07-17'.
``` sql
SELECT DISTINCT c.customer_id, c.first_name, c.last_name
FROM customer c
JOIN transaction t ON c.customer_id = t.customer_id
WHERE c.job_industry_category IN ('IT', 'Health')
AND t.order_status = 'Approved'
AND t.transaction_date BETWEEN '2017-07-07' AND '2017-07-17';
```
---


## Краткие выводы
В ходе работы были созданы и оптимизированы структуры данных для удобства работы и анализа. Преобразование данных позволило исправить проблемы с форматами и облегчить дальнейшие запросы и анализ.
