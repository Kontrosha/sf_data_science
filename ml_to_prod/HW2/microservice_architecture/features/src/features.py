
import pika
import numpy as np
import json
import time
from datetime import datetime
from sklearn.datasets import load_diabetes

# Создаём бесконечный цикл для отправки сообщений в очередь
while True:
    try:
        # Загружаем датасет о диабете
        X, y = load_diabetes(return_X_y=True)
        # Формируем случайный индекс строки
        random_row = np.random.randint(0, X.shape[0]-1)

        # Генерируем уникальный идентификатор на основе timestamp
        unique_id = datetime.now().timestamp()

        # Создаём подключение по адресу rabbitmq
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()

        # Создаём очереди y_true и features
        channel.queue_declare(queue='y_true')
        channel.queue_declare(queue='features')

        # Формируем сообщения в формате словаря с уникальным идентификатором
        y_true_message = {'id': unique_id, 'value': y[random_row]}
        features_message = {'id': unique_id, 'features': list(X[random_row])}

        # Публикуем сообщение в очередь y_true
        channel.basic_publish(exchange='',
                              routing_key='y_true',
                              body=json.dumps(y_true_message))
        print(f"Сообщение с правильным ответом отправлено в очередь: {y_true_message}")

        # Публикуем сообщение в очередь features
        channel.basic_publish(exchange='',
                              routing_key='features',
                              body=json.dumps(features_message))
        print(f"Сообщение с вектором признаков отправлено в очередь: {features_message}")

        # Закрываем подключение
        connection.close()

        # Задержка перед следующей итерацией
        time.sleep(2)

    except Exception as e:
        print(f"Ошибка: {e}")
