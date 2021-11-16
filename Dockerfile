# syntax=docker/dockerfile:1
# # escape=`
# Указывает Docker использовать официальный образ python 3 с dockerhub в качестве базового образа
FROM python:3
# Устанавливает рабочий каталог контейнера — "app"
WORKDIR /app
# Указывем, что код внутри контейнера слушает порт 8000 (при запуске обязательно использовать -p 8000:8000)

# Копирует requirements.txt
COPY requirements.txt requirements.txt
# Запускает команду pip install для всех библиотек, перечисленных в requirements.txt
RUN pip install -r requirements.txt
# Копируем все файлы в рабочий каталог
COPY . .
# Стартуем приложение в режиме отладки
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8080" ]