# Проект написание ETL с использованием Apache Airflow
## Описание стуктуры проекта
Проект содержит следующие файлы:
```bash
data_engineering/
└── HW2/
    ├── airflow_venv/ # виртуальное окружение проекта
    ├── output/ # папка с выходными таблицами
    │   └── flags_activity2024-05-01.csv # выходная таблицы
    ├── screenshots/ # папка со скриншотами
    ├── scripts/ # исходный скрипт для встраивания в DAG
    │   └── transform_script.py
    ├── tables/ # таблицы
    │   ├── flags_activity.csv
    │   └── profit_table.csv
    ├── config.yaml # конфигурация DAG
    ├── customer_activity_etl_dag.py # исходный код DAG
    └── req.txt # зависимости проекта
```  
## Вывполнение задачи
### 1. Описание задачи и исходные данные
Описание задачи:  
Целью проекта была реализация DAG в Apache Airflow для автоматизации ETL-процесса (извлечение, трансформация, загрузка данных). Задача заключалась в ежемесячной обработке данных активности клиентов по сумме и количеству транзакций, а также формирование витрины данных с флагами активности клиентов по продуктам.

Исходные данные:  
Исходные данные представлены в виде CSV-файла profit_table_lite.csv, содержащего транзакции клиентов по 10 продуктам. Для каждого продукта указываются сумма (sum_) и количество (count_) транзакций.

### 2. Декомпозиция задачи
Этапы выполнения задачи:
- Извлечение данных из CSV-файла.
- Трансформация данных с расчетом флагов активности для каждого продукта, используя предоставленный скрипт трансформации.
- Загрузка данных в конечный файл, где данные всех продуктов собираются вместе.
### 3. Написание кода
Код был написан в Python с использованием Apache Airflow. Был создан DAG, включающий:

- Задачу извлечения данных (extract_data), которая загружает данные из CSV-файла.
- Задачи трансформации данных для каждого продукта (transform_product_data), выполняемые параллельно.
- Задачу загрузки данных (load_data), которая агрегирует результаты трансформации и сохраняет их в итоговом файле.
### 4. Запуск кода с результатами
DAG был успешно запущен через интерфейс Airflow. В результате выполнения DAG был получен файл с флагами активности клиентов, агрегированный по всем продуктам. В интерфейсе Airflow были наблюдены статусы выполнения каждой задачи, подтверждающие успешное завершение процесса без ошибок.
Граф запуска: ![etl_graph.png]([https://github.com/Kontrosha/sf_data_science/blob/main/data_engineering/HW2/screenshots/etl_graph.png])
DAG на главной странице: ![etl_main_page]([https://github.com/Kontrosha/sf_data_science/blob/main/data_engineering/HW2/screenshots/etl_main_page.png])
### 5. Выводы
Проект показал эффективность использования Apache Airflow для автоматизации сложных ETL-процессов. Разделение процесса на отдельные задачи и их параллельное выполнение позволило эффективно обрабатывать данные, сокращать время обработки и улучшать управление данными. Airflow обеспечил надежное выполнение задач по расписанию, легкость мониторинга и возможность масштабирования процессов.