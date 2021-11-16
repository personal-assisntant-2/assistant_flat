# personal-assistant

## WEB-приложение Personal Assistant является курсовым проектом второго семестра (Python WEB) обучения по программе [Python WEB и Data Science](https://goit.ua/course/) компании [GoIT](https://goit.ua/)

Ознакомиться развернутой демонстрационной версией приложения можно [тут.](https://blooming-springs-73568.herokuapp.com/)

Так же Вы можете скачать готовый демострационный docker-image, используя команду
`docker pull romanskyy78/first_team:latest`
Он предназначен дя локального развертывания приложения (localhost:8000/) и ознакомлпения с его работой. ВАЖНО! При равертывании приложения локально необходимо подключение базы данных с передачей в контейнер переменных окружения, описывающих подключение к базе данных.

## Приложение является многопользовательским и предназначено:

#### Для ведения адресной книги контактов.

Каждый контакт имеет следующе поля:

- Имя (обязательное поле)
- День рождения
- Адрес
- Телефон (может быть любое количество)
- E-mail (может быть любое количество)
- Заметки:
  - Каждая заметка может иметь тэги. Любые и любое количество.

#### Для сбора новостей на интересующую тематику.

В случае развернутого приложения – курсы нескольких криптовалют, которые собираются при каждом обращении с ряда сайтов.

#### Для хранения файлов с воможностью сортировки по типам файлов.

---

## особенности

#### Используемый стек технологий:

- базовый фрймворк - Django
- сбор новостей построен асинхронно с использованием asyncio и AIOHTTP
- в качестве базы данных используется PostgreSQL
- для визуализации использован клиентский фреймворк bootstrap
- вспомогательные технологии:
  - dotenv, pylint, black, docker

## Подключение к базе данных

База данных для приложения реализована как отдельное приложение развернутое отдельно на отдельном сервере.
Для запуска приложения в корневой директории проекта должен находится файл .env, в котором в формате пакета [python-dotenv](https://pypi.org/project/python-dotenv/) определены значения следующих переменных среды:
имя переменной | значение переменной
---------------|--------------------
HOST_DB | адрес хоста БД
PORT_DB | порт, на котором подключена БД
NAME_DB | имя базы данных
USER_DB | имя пользователя базы данных
ASSISTANT_RASS | пароль для подключения к базе данных
ASSISTANT_SECRET_KEY | ключ шифрования Django для защиты от csrf-атак

## запуск тестового приложения на локальном web-сервере из docker-image

Для запуска приложения из образа локально, необходимо подключение к реальной базе данных (предполагается что она создана заранее). Это подключение должно быть описано в файле, передаваемом при старте контейнера, например:

```
docker run -it -p 8000:8000 --env-file ./env_docker romanskyy78/first_team
```

в данном случае файл имеет название env_docker и находится в директории из которой запускается образ (может находиться в любом месте и иметь любое название. Подробнее об этом можете прочитать в [документации](https://docs.docker.com/engine/reference/commandline/run/#set-environment-variables--e---env---env-file)). Содержание файла - перечень переменных окружения (каждая - с новой строки) с присвоенными значениями (без пробелов и кавычек). Пример:

```
ASSISTANT_PASS=your_db_password
ASSISTANT_SECRET_KEY=your_secret_key
NAME_DB=your_db_abonent_name
USER_DB=your_db_namr
HOST_DB=your_db_host_addr
PORT_DB=your_db_port
```
