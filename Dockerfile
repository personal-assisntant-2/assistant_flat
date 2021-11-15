# syntax=docker/dockerfile:1
# Указывает Docker использовать официальный образ python 3 с dockerhub в качестве базового образа
FROM python:3
# Устанавливает рабочий каталог контейнера — "app"
WORKDIR /app
# Копирует requirements.txt
COPY requirements.txt requirements.txt
# Запускает команду pip install для всех библиотек, перечисленных в requirements.txt
RUN pip install -r requirements.txt
# Копируем все файлы в рабочий каталог
COPY . .
