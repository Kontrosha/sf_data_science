
import pika
import pickle
import numpy as np
import json

# Читаем файл с сериализованной моделью
with open('myfile.pkl', 'rb') as pkl_file:
    regressor = pickle.load(pkl_file)

try:
    # Создаём подключение по адресу rabbitmq:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # Объявляем очередь features
    channel.queue_declare(queue='features')
    # Объявляем очередь y_pred
    channel.queue_declare(queue='y_pred')

    # Создаём функцию callback для обработки данных из очереди
    def callback(ch, method, properties, body):
        message = json.loads(body)
        print(f"Получено сообщение: {message}")

        # Извлекаем вектор признаков и уникальный ID
        unique_id = message['id']
        features = np.array(message['features']).reshape(1, -1)

        # Генерируем предсказание
        pred = regressor.predict(features)[0]

        # Формируем сообщение с предсказанием и ID
        y_pred_message = {'id': unique_id, 'prediction': pred}

        # Отправляем сообщение в очередь y_pred
        channel.basic_publish(exchange='',
                              routing_key='y_pred',
                              body=json.dumps(y_pred_message))
        print(f"Предсказание {y_pred_message} отправлено в очередь y_pred")

    # Извлекаем сообщение из очереди features
    channel.basic_consume(
        queue='features',
        on_message_callback=callback,
        auto_ack=True
    )
    print('...Ожидание сообщений, для выхода нажмите CTRL+C')

    # Запускаем режим ожидания прихода сообщений
    channel.start_consuming()
except Exception as e:
    print(f"Ошибка: {e}")
