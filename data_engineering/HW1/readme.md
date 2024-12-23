# Инжиниринг данных. Домашнее задание 1 (HW)

## Написать пайплайн с помощью фреймворка Luigi

### Содержание

1. [Как запустить пайплайн](#как-запустить-пайплайн)
    1. [Как установить зависимости](#как-установить-зависимости)
    2. [Как запустить](#как-запустить)
2. [Выполнение задачи](#выполнение-задачи)
    1. [Разбор задания на таски](#разбор-задания-на-таски)
    2. [Организация нашего проекта](#организация-проекта)
    3. [Краткое описание используемых модулей](#краткое-описание-используемых-модулей)
3. [Результаты](#результаты)
    1. [Результат работы в интерфейсе Luigi](#результат-работы-в-интерфейсе-luigi)
    2. [Краткий вывод](#краткий-вывод)

---

### Как запустить пайплайн
#### Как установить зависимости:
Для установки необходимых зависимостей выполните следующую команду в терминале из корня проекта:

```bash
pip install -r requirements.txt
```
#### Как запустить:
Преварительно скачайте папку [HW1]().  
Запустите центральный планировщик Luigi, используя команду luigid.
```bash
luigid
```
*Запуск пайплайна:* для запуска выполните команду в терминале, находя в корне проекта:
```bash
 python3 src/run_pipeline.py <DATASET_NAME>
```
Пример:
```bash
 python3 src/run_pipeline.py GSE68849
```
После запуска процесс можно наблюдать в планировщике на локальном хосте по ссылке: http://localhost:8082

### Выполнение задачи

#### Разбор задания на таски
Задание разбито на несколько тасок:
- **Таск 0**: Поиск ссылки на скачивание датасета.
- **Таск 1**: Скачивание датасета.
- **Таск 2**: Разархивация и первичная обработка данных.
- **Таск 3**: Обработка и подготовка данных.
- **Таск 4**: Создание урезанных версий таблиц.
- **Таск 5**: Очистка и подготовка к финальной стадии, удаление исходных текстовых файлов из папки extracted.

#### Организация проекта
```css
HW1/
├── src/
│   ├── run_pipeline.py
│   └── tasks/
│       ├── __init__.py
│       ├── Task0FindDownloadLink.py
│       ├── Task1DownloadDataset.py
│       ├── Task2ExtractAndOrganize.py
│       ├── Task3ProcessExtracted.py
│       ├── Task4CreateReducedTables.py
│       └── Task5Cleanup.py
└── execute_results/
    ├── GSE68849/
    │   ├── extracted/
    │   │   ├── archive1/
    │   │   │   └── archive1.txt
    │   │   └── archive2/
    │   │       └── archive2.txt
    │   ├── processed/
    │   │   ├── table1.tsv
    │   │   ├── table2.tsv
    │   │   ├── table3.tsv
    │   │   └── table4.tsv
    │   └── reduced/
    │       ├── table1_reduced.tsv
    │       └── table2_reduced.tsv
    └── GSE68849_download_link.json

```
*Структура папки [src](https://github.com/Kontrosha/sf_data_science/tree/main/data_engineering/HW1/src):* содержит все скрипты пайплайна, разделенные по задачам.  
*Структура папки [execute_results](https://github.com/Kontrosha/sf_data_science/tree/main/data_engineering/HW1/execute_results):* содержит результаты выполнения пайплайна, включая скачанные и обработанные данные.

#### Краткое описание используемых модулей
- **os**: используется для взаимодействия с файловой системой.
- **beautifulsoup4 (bs4)**: применяется для парсинга HTML и XML документов.
- **tarfile и gzip**: используются для работы с архивами.
- **shutil**: предоставляет различные операции с файлами, включая копирование и удаление.
- **pandas**: основной инструмент для обработки и анализа данных.
### Результаты
#### Результат работы в интерфейсе Luigi
На картинках ниже отображен успешно выполненный пайплайн:
![run_pipeline](https://github.com/Kontrosha/sf_data_science/blob/main/data_engineering/HW1/screenshots/run_pipeline.png)
![pipeline_graph](https://github.com/Kontrosha/sf_data_science/blob/main/data_engineering/HW1/screenshots/pipeline_graph.png)  
#### Краткий вывод
В ходе выполнения данного домашнего задания мы познакомились с фреймворком Luigi для организации и управления пайплайнами обработки данных. Мы реализовали пайплайн, который включает в себя скачивание данных, их разархивацию, обработку и подготовку к дальнейшему анализу, а также финальную очистку рабочей директории от временных файлов.

В результате работы пайплайна были успешно извлечены необходимые данные, проведена их предварительная обработка и подготовлены к анализу. Работа с Luigi позволила нам организовать процесс выполнения задач таким образом, чтобы каждая задача выполнялась только после успешного завершения всех предшествующих ей зависимостей. Это гарантировало последовательность и корректность выполнения всех этапов обработки данных.

Использование центрального планировщика и веб-интерфейса Luigi дало нам возможность наглядно отслеживать процесс выполнения пайплайна, что облегчило отладку и ускорило процесс разработки.
