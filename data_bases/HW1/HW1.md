# Домашнее задание 1

## Содержание
- [Домашнее задание 1](#домашнее-задание-1)
  - [Содержание](#содержание)
  - [Структура базы данных](#структура-базы-данных)
  - [Нормализация базы данных](#нормализация-базы-данных)
    - [Первая нормальная форма (1НФ)](#первая-нормальная-форма-1нф)
    - [Вторая нормальная форма (2НФ)](#вторая-нормальная-форма-2нф)
  - [Выделение справочных таблиц: Создание отдельных таблиц для адресов (Addresses) и продуктов (Products) устранило частичные зависимости, так как информация об этих атрибутах не зависит напрямую от ключей транзакций или клиентов.](#выделение-справочных-таблиц-создание-отдельных-таблиц-для-адресов-addresses-и-продуктов-products-устранило-частичные-зависимости-так-как-информация-об-этих-атрибутах-не-зависит-напрямую-от-ключей-транзакций-или-клиентов)
    - [Третья нормальная форма (3НФ)](#третья-нормальная-форма-3нф)
    - [Итог](#итог)
  - [Итоговая стуктура баз данных.](#итоговая-стуктура-баз-данных)
  - [Создание базы данных в DataGrip](#создание-базы-данных-в-datagrip)
  - [Загрузка данных в таблицы](#загрузка-данных-в-таблицы)

## Структура базы данных
База данных будем строить на основе [таблицы](https://github.com/Kontrosha/sf_data_science/tree/main/data_bases/HW1/customer_and_transaction.xlsx).
Файл содержит два листа с данными: transaction и customer. Вот краткое описание каждого из них:

*Лист Transaction*
- transaction_id: уникальный идентификатор транзакции
- product_id: идентификатор продукта
- customer_id: идентификатор клиента
- transaction_date: дата транзакции
- online_order: заказ был сделан онлайн или нет
- order_status: статус заказа
- brand: бренд продукта
- product_line: линейка продуктов
- product_class: класс продукта
- product_size: размер продукта
- list_price: цена продукта
- standard_cost: стандартная стоимость

*Лист Customer*
- customer_id: уникальный идентификатор клиента
- first_name: имя клиента
- last_name: фамилия клиента
- gender: пол клиента
- DOB: дата рождения
- job_title: профессиональное название
- job_industry_category: категория отрасли
- wealth_segment: сегмент богатства
- deceased_indicator: индикатор умерших
- owns_car: владеет ли машиной
- address: адрес
- postcode: почтовый индекс
- state: штат
- country: страна
- property_valuation: оценка имущества

Исходя из этого описания, мы можем спроектировать базу данных с двумя основными таблицами: Transactions и Customers. Для обеспечения связи между таблицами, мы используем customer_id как внешний ключ в таблице Transactions, который ссылается на первичный ключ в таблице Customers.

Базовая структура в [dbdiagram.io](https://dbdiagram.io/d/DB-HW-1-before-normalize-65c78d84ac844320aedd080d).

## Нормализация базы данных
### Первая нормальная форма (1НФ)
**Исходная структура**

Исходные данные содержались в двух листах Excel: transaction и customer. Оба листа включали в себя множество атрибутов, некоторые из которых (например, информация о продуктах в transaction и адресная информация в customer) могли привести к дублированию данных при множественных записях.

**Приведение к 1НФ**

Разбиение на таблицы: данные были разбиты на отдельные таблицы (Customers, Transactions, Products, Addresses), каждая из которых хранит данные об отдельной сущности.

Уникальные ключи: Для каждой таблицы был определен уникальный ключ (например, customer_id, transaction_id, product_id, address_id), обеспечивая уникальность каждой записи.

Атомарность атрибутов: Все атрибуты были приведены к атомарной форме, то есть каждый атрибут содержит неделимое значение.

---
### Вторая нормальная форма (2НФ)

**Приведение к 2НФ**

2НФ требует, чтобы база данных была в 1НФ и каждый атрибут, не являющийся частью ключа, полностью зависел от первичного ключа.

Устранение частичных зависимостей: Таблицы были спроектированы таким образом, чтобы каждое неключевое поле зависело от первичного ключа. Например, в таблице Transactions каждое поле зависит от transaction_id, а в Customers — от customer_id.

Выделение справочных таблиц: Создание отдельных таблиц для адресов (Addresses) и продуктов (Products) устранило частичные зависимости, так как информация об этих атрибутах не зависит напрямую от ключей транзакций или клиентов.
---

### Третья нормальная форма (3НФ)
Приведение к 3НФ
3НФ требует, чтобы база данных была во 2НФ и все атрибуты были не транзитивно зависимы от первичных ключей.

Устранение транзитивных зависимостей: Вынос информации о адресах из таблицы Customers в отдельную таблицу Addresses устранило транзитивную зависимость, где адресные данные могли зависеть от других атрибутов клиента. Теперь address_id в таблице Customers напрямую связывает клиента с его адресом без транзитивных зависимостей.
Нормализация данных о продуктах: Аналогично, выделение таблицы Products обеспечило, что вся информация о продукте зависит только от product_id, устраняя транзитивные зависимости в Transactions.

### Итог

Каждая таблица в результате нормализации:
- Содержит только данные, связанные с одной сущностью (1НФ).
Имеет все данные, не являющиеся ключом, полностью зависимыми от первичного ключа (2НФ).
Не содержит транзитивных зависимостей (3НФ).
Эта структура минимизирует дублирование данных, упрощает обслуживание базы данных и уменьшает риск аномалий при модификации данных.

[Итоговая](https://dbdiagram.io/d/DB-HW-1-after-normalization-65c79600ac844320aedd5194) стуктура баз данных.
---
## Создание базы данных в DataGrip
Для создания базы данных использовался PostgresSQL и JetBrains DataGrip.
Код, запущенный в консоли для создания:
```
CREATE DATABASE customer_and_transactions;
```
В результате выполения SQL-команды получили базу данных:
![customer_and_transaction_db.png](Users/kate-chuiko-os-x/Documents/Maga/ GitRepo/sf_data_science/data_bases/HW1/customer_and_transaction_db.png)

Для создания таблиц использовались следующие SQL команды:
```
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
```
Сам скрипт располагается в [table_creation.sql](link)

## Загрузка данных в таблицы
Для загрузки данных был использован встроенный фукционал JetBrains DataGrip - Import -> Import Data from Files из заранее подготовленных csv-файлов [trasactions.csv](link) и [customers.csv](link).

Для преобразования листов исходной xlsx таблицы был написан скрипт на Python [convert_to_csv.py](link)

```
import pandas as pd

excel_file = 'customer_and_transaction.xlsx'
sheets = pd.read_excel(excel_file, sheet_name=None)
transactions_csv_path = 'transactions.csv'
customers_csv_path = 'customers.csv'
sheets['transaction'].to_csv(transactions_csv_path, sep=';', index=False, encoding='utf-8')
sheets['customer'].to_csv(customers_csv_path, sep=';', index=False, encoding='utf-8')

```