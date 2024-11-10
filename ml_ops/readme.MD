# Docker-окружение для Nginx и PostgreSQL с автоматическим тестированием

Этот проект предоставляет настройку для запуска Nginx и PostgreSQL в Docker-контейнерах с предустановленной конфигурацией и автоматизированным тестированием на Python.

## Возможности

1. **Nginx**:
   - Настроен на разрешение только `POST` запросов к `/api`.
   - Возвращает `403 Forbidden` для всех других методов.

2. **PostgreSQL**:
   - Автоматически создаёт пользователя `test` и пустую базу данных с таким же именем.

3. **Автоматическое тестирование**:
   - Python-скрипт для сборки, запуска и тестирования контейнеров.
   - Проверяет корректность конфигурации.

---

## Структура проекта
```
project/
├── nginx/
│   ├── Dockerfile        # Dockerfile для сборки образа Nginx
│   └── nginx.conf        # Конфигурация Nginx
├── postgres/
│   ├── Dockerfile        # Dockerfile для сборки образа PostgreSQL
│   └── init.sql          # SQL-скрипт для инициализации PostgreSQL
├── test_docker.py        # Python-скрипт для автоматизации сборки и тестирования контейнеров
├── requirements.txt      # Список Python-зависимостей
└── venv/                 # (опционально) Виртуальное окружение
```

---

## Требования

- Установленный Docker и Docker Compose
- Python 3.8+ (с поддержкой `venv`)
- PosrgreSQL

---

## Настройка и использование

### 1. Создайте и активируйте виртуальное окружение
```bash
python3 -m venv venv
source venv/bin/activate  
```

### 2. Установите зависимости Python
```bash
pip install -r requirements.txt
```

### 3. Запуск сборки и тестирования контейнеров
```bash
python3 init_and_test_docker.py
```

Этот скрипт:

	•	Соберёт образы Docker для Nginx и PostgreSQL.
	•	Запустит контейнеры.
	•	Проверит конфигурации.
	•	Удалит контейнеры и образы после тестирования.

### 4. Ручное тестирование (опционально)
1. Соберите контейры:
```bash
docker build -t custom-nginx ./nginx
docker build -t custom-postgres ./postgres
```

2. Запустите контейнеры вручную
```bash
docker run -d -p 8080:80 --name test-nginx custom-nginx
docker run -d -p 5432:5432 --name test-postgres custom-postgres
```
3. Проверка ответов:
```bash
curl -X GET http://localhost:8080/api
# Должно вернуть "403 Forbidden"

curl -X POST http://localhost:8080/api
# Должно вернуть "200 OK" или пустой ответ
```

4. Остановка и удаление контейнеров:
```bash
docker stop test-nginx test-postgres
docker rm test-nginx test-postgres
docker rmi custom-nginx custom-postgres
```