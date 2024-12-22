import pika
import json
import csv
import os

# Создаем локальные хранилища для значений
y_true_store = {}
y_pred_store = {}

# Убедимся, что директория для логов существует
os.makedirs("/app/logs", exist_ok=True)

# Путь к файлу логов
log_file = "/app/logs/metric_log.csv"

# Инициализация файла логов
with open(log_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    # Записываем заголовок
    writer.writerow(["id", "y_true", "y_pred", "absolute_error"])

# Инициализация файла логов
with open(log_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    # Записываем заголовок
    writer.writerow(["id", "y_true", "y_pred", "absolute_error"])

try:
    # Создаём подключение к серверу на локальном хосте
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # Объявляем очереди
    channel.queue_declare(queue='y_true')
    channel.queue_declare(queue='y_pred')

    # Функция для обработки сообщений из y_true
    def callback_y_true(ch, method, properties, body):
        message = json.loads(body)
        print(f"Получено из y_true: {message}")

        # Сохраняем y_true с уникальным ID
        unique_id = message['id']
        y_true_store[unique_id] = message['value']

        # Проверяем, есть ли предсказание с таким же ID
        if unique_id in y_pred_store:
            calculate_metric(unique_id)

    # Функция для обработки сообщений из y_pred
    def callback_y_pred(ch, method, properties, body):
        message = json.loads(body)
        print(f"Получено из y_pred: {message}")

        # Сохраняем y_pred с уникальным ID
        unique_id = message['id']
        y_pred_store[unique_id] = message['prediction']

        # Проверяем, есть ли истинное значение с таким же ID
        if unique_id in y_true_store:
            calculate_metric(unique_id)

    # Функция для расчёта метрики
    def calculate_metric(unique_id):
        y_true = y_true_store.pop(unique_id)
        y_pred = y_pred_store.pop(unique_id)
        error = abs(y_true - y_pred)

        # Записываем метрики в лог-файл
        with open(log_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([unique_id, y_true, y_pred, error])

        print(f"ID: {unique_id} | y_true: {y_true}, y_pred: {y_pred}, error: {error}")

    # Подписываемся на очереди
    channel.basic_consume(queue='y_true', on_message_callback=callback_y_true, auto_ack=True)
    channel.basic_consume(queue='y_pred', on_message_callback=callback_y_pred, auto_ack=True)

    print('...Ожидание сообщений, для выхода нажмите CTRL+C')
    channel.start_consuming()
except Exception as e:
    print(f"Ошибка из metric.py: {e}")