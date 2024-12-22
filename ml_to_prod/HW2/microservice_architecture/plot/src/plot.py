import pandas as pd
import matplotlib.pyplot as plt
import time

# Путь к файлу с логами
log_file = "/app/logs/metric_log.csv"
# Путь к файлу с графиком
output_plot = "/app/logs/error_distribution.png"

while True:
    try:
        # Читаем таблицу метрик
        data = pd.read_csv(log_file)

        # Проверяем, есть ли данные
        if not data.empty:
            # Строим гистограмму распределения абсолютных ошибок
            plt.figure(figsize=(8, 6))
            plt.hist(data['absolute_error'], bins=10, alpha=0.7, color="purple", edgecolor="black", density=True)
            plt.title("Distribution of Absolute Errors")
            plt.xlabel("Absolute Error")
            plt.ylabel("Density")
            
            # Сохраняем график
            plt.savefig(output_plot)
            plt.close()
            print(f"Гистограмма успешно сохранена в {output_plot}")
        else:
            print("Нет данных для построения графика.")

        # Задержка перед следующей итерацией
        time.sleep(5)
    except Exception as e:
        print(f"Ошибка из plot.py: {e}")