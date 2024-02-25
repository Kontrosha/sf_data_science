## Оглавление
- [Оглавление](#оглавление)
- [Структура проекта](#структура-проекта)
- [Выполнение работы](#выполнение-работы)
  - [Создание БД и таблиц](#создание-бд-и-таблиц)
  - [Выполнение запросов](#выполнение-запросов)
    - [Запрос 1. Распределение клиентов по сферам деятельности](#запрос-1-распределение-клиентов-по-сферам-деятельности)
    - [Запрос 2. Сумма транзакций по месяцам и сферам деятельности](#запрос-2-сумма-транзакций-по-месяцам-и-сферам-деятельности)
    - [Запрос 3. Количество онлайн-заказов для брендов от клиентов из сферы IT](#запрос-3-количество-онлайн-заказов-для-брендов-от-клиентов-из-сферы-it)
    - [Запрос 4. Сумма, максимум, минимум и количество транзакций для всех клиентов](#запрос-4-сумма-максимум-минимум-и-количество-транзакций-для-всех-клиентов)
- [В запросе 4 мы использовали два подхода для анализа транзакций клиентов: агрегацию с помощью GROUP BY и оконные функции. Оба метода дали одинаковые результаты (3493 строки), что демонстрирует их эффективность и взаимозаменяемость для задач агрегации и анализа данных. Это подчеркивает гибкость SQL в обработке данных, позволяя выбирать наиболее подходящий инструмент в зависимости от задачи и предпочтений разработчика.](#в-запросе-4-мы-использовали-два-подхода-для-анализа-транзакций-клиентов-агрегацию-с-помощью-group-by-и-оконные-функции-оба-метода-дали-одинаковые-результаты-3493-строки-что-демонстрирует-их-эффективность-и-взаимозаменяемость-для-задач-агрегации-и-анализа-данных-это-подчеркивает-гибкость-sql-в-обработке-данных-позволяя-выбирать-наиболее-подходящий-инструмент-в-зависимости-от-задачи-и-предпочтений-разработчика)
    - [Запрос 5. Клиенты с минимальной/максимальной суммой транзакций](#запрос-5-клиенты-с-минимальноймаксимальной-суммой-транзакций)
    - [Запрос 6. Первые транзакции клиентов](#запрос-6-первые-транзакции-клиентов)
    - [Запрос 7 . Клиенты с максимальным интервалом между транзакциями](#запрос-7--клиенты-с-максимальным-интервалом-между-транзакциями)
  - [Итог](#итог)


## Структура проекта
- requests.sql - запросы в таблицы
- csv - папка с таблицами в формате csv
- screenshots - папка со скриншотами

## Выполнение работы

### Создание БД и таблиц
- Скрипт для создание БД:
```sql
CREATE DATABASE hw3;
```

- Скрипт для создания таблиц:
```sql
create table customer
(
    customer_id           integer not null
        primary key,
    first_name            varchar(50),
    last_name             varchar(50),
    gender                varchar(30),
    dob                   varchar(50),
    job_title             varchar(50),
    job_industry_category varchar(50),
    wealth_segment        varchar(50),
    deceased_indicator    varchar(50),
    owns_car              varchar(30),
    address               varchar(50),
    postcode              varchar(30),
    state                 varchar(30),
    country               varchar(30),
    property_valuation    integer
);

alter table customer
    owner to postgres;

create table transaction
(
    transaction_id   integer not null
        primary key,
    product_id       integer,
    customer_id      integer
        references customer,
    online_order     varchar(30),
    order_status     varchar(30),
    brand            varchar(30),
    product_line     varchar(30),
    product_class    varchar(30),
    product_size     varchar(30),
    standard_cost    real,
    list_price       real,
    transaction_date date
);

alter table transaction
    owner to postgres;
```

Таблицы были заполнены с помощью встроенного функционала DataGrip: *Import/Export -> Import from File(s)...*

### Выполнение запросов

#### Запрос 1. Распределение клиентов по сферам деятельности
**Задача**:
Вывести распределение (количество) клиентов по сферам деятельности, отсортировав результат по убыванию количества.

**Запрос**:
```sql
SELECT job_industry_category, COUNT(*) AS customer_count
FROM customer
GROUP BY job_industry_category
ORDER BY customer_count DESC;
```
---
#### Запрос 2. Сумма транзакций по месяцам и сферам деятельности
**Задача:**
Найти сумму транзакций за каждый месяц по сферам деятельности, отсортировав по месяцам и по сфере деятельности.

**Запрос:**
```sql
SELECT DATE_TRUNC('month', transaction_date)::date AS month,
       c.job_industry_category,
       SUM(t.list_price) AS total_transaction_amount
FROM transaction t
JOIN customer c ON t.customer_id = c.customer_id
GROUP BY month, c.job_industry_category
ORDER BY month, c.job_industry_category;
```
---
#### Запрос 3. Количество онлайн-заказов для брендов от клиентов из сферы IT
**Задача**:
Вывести количество онлайн-заказов для всех брендов в рамках подтвержденных заказов клиентов из сферы IT.

**Запрос**:
```sql
SELECT brand, COUNT(*) AS online_order_count
FROM transaction
JOIN customer ON transaction.customer_id = customer.customer_id
WHERE customer.job_industry_category = 'IT' AND transaction.online_order = 'True' AND transaction.order_status = 'Approved'
GROUP BY brand;
```
---
#### Запрос 4. Сумма, максимум, минимум и количество транзакций для всех клиентов
**Задача:**
Найти по всем клиентам сумму всех транзакций (list_price), максимум, минимум и количество транзакций, отсортировав результат по убыванию суммы транзакций и количества клиентов. Выполните двумя способами: используя только group by и используя только оконные функции. Сравните результат.

**Запрос**:
- С использованием GROUP BY:
```sql
SELECT customer_id, SUM(list_price) AS total, MAX(list_price) AS max_price,
       MIN(list_price) AS min_price, COUNT(*) AS transaction_count
FROM transaction
GROUP BY customer_id
ORDER BY total DESC, transaction_count DESC;
```

- С использованием оконных функций:
```sql
SELECT DISTINCT customer_id,
       SUM(list_price) OVER (PARTITION BY customer_id) AS total,
       MAX(list_price) OVER (PARTITION BY customer_id) AS max_price,
       MIN(list_price) OVER (PARTITION BY customer_id) AS min_price,
       COUNT(*) OVER (PARTITION BY customer_id) AS transaction_count
FROM transaction
ORDER BY total DESC, transaction_count DESC;
```
- **Сравнение результата:**
В запросе 4 мы использовали два подхода для анализа транзакций клиентов: агрегацию с помощью GROUP BY и оконные функции. Оба метода дали одинаковые результаты (3493 строки), что демонстрирует их эффективность и взаимозаменяемость для задач агрегации и анализа данных. Это подчеркивает гибкость SQL в обработке данных, позволяя выбирать наиболее подходящий инструмент в зависимости от задачи и предпочтений разработчика.
---
#### Запрос 5. Клиенты с минимальной/максимальной суммой транзакций
**Задача**:
Найти имена и фамилии клиентов с минимальной/максимальной суммой транзакций за весь период (сумма транзакций не может быть null). Напишите отдельные запросы для минимальной и максимальной суммы.

**Запрос**:

- Минимальная сумма:
```sql
SELECT first_name, last_name
FROM customer
WHERE customer_id = (
  SELECT customer_id
  FROM transaction
  GROUP BY customer_id
  ORDER BY SUM(list_price) ASC
  LIMIT 1
);
```

- Максимальная сумма:
```sql
SELECT first_name, last_name
FROM customer
WHERE customer_id = (
  SELECT customer_id
  FROM transaction
  GROUP BY customer_id
  ORDER BY SUM(list_price) DESC
  LIMIT 1
);
```
---
#### Запрос 6. Первые транзакции клиентов
**Задача**:
Вывести только самые первые транзакции клиентов. Решить с помощью оконных функций.


**Запрос**:
```sql
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
```
---
#### Запрос 7 . Клиенты с максимальным интервалом между транзакциями
**Задача**:
Вывести имена, фамилии и профессии клиентов, между транзакциями которых был максимальный интервал (интервал вычисляется в днях).

**Запрос**:
```sql
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
```
---


### Итог
В ходе работы мы успешно реализовали серию SQL-запросов для анализа данных клиентов и их транзакций, используя различные техники, включая агрегацию данных с помощью GROUP BY и оконные функции. Это позволило нам глубоко погрузиться в анализ распределения клиентов по сферам деятельности, динамики транзакций, а также выявить ключевые паттерны в поведении клиентов. Применение обоих методов демонстрирует гибкость и мощность SQL для выполнения комплексного анализа данных, подчеркивая их важность и эффективность в решении разнообразных задач аналитики.