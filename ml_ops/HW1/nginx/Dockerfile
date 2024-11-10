# базовый образ
FROM alpine:latest

# установка nginx
RUN apk add --no-cache nginx

# создание папки для логов
RUN mkdir -p /run/nginx

COPY nginx.conf /etc/nginx/nginx.conf

# открытие порта
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]