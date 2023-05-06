# API YamDB
## Описание
###### API-сервис для публикации отзывов, рейтингов и комментариев к различным произведениям.

## Технологии:
- Django 
- DRF
- Python
- JWT+Djoser

## Установка
- Склонировать репозиторий:
```sh
git clone https://github.com/dartilius/api_yamdb.git
```

- Перейдите в директорию проекта:
```sh
cd api_yamdb
```

- Создайте и активируйте виртуальное окружение
```sh
python -m venv venv
```

- Activate venv:
```sh
# OS Lunix & MacOS
source venv/bin/activate
```
```sh
# OS Windows GitBash Terminal
source venv/Scripts/activate
```
```sh
# OS Windows cmd.exe terminal
C:\> venv\Scripts\activate
```

- Установите зависимости из requirements.txt:
```sh
python3 -m pip install --upgrade pip
```
```sh
pip install -r requirements.txt
```

- Создайте миграции:
```sh
python manage.py migrate
```

- Запустите сервер:
```sh
python manage.py runserver
```

## Как зарегистрировать пользователя
1. Сделайте POST запрос, укаказав в теле "username" и "email" на эндпоинт "api/v1/auth/signup/"
2. YaMDb отправит проверочный код на указанный email
3. Сделайте POST запрос указав "email" и "confirmation_code" в теле запроса на эндпоинт "api/v1/auth/token/"/,в ответе вы получите JWT-токен

## API YaMDb ресурсы:
- AUTH: Аутентификация.
- USERS: Регистрация пользователей/редактирование информации
- TITLES: Произведения и информация о них
- CATEGORIES: Категории произведений (фильмы, музыка, книги)
- GENRES: Жанры. Одно произведение может иметь несколько жанров
- REVIEWS: Отзывы на произведения. Каждый отзыв относится к определенному произведению.
- COMMENTS: Комментарии к отзывам на произведения.


## Эндпоинты:
Эндпоинт| Тип запроса | Тело запроса | Ответ | Комментарий
--- | --- | --- | --- | ---|
api/v1/auth/signup/	| POST |	{"username": "me","email": "me@mail.ru"}|	Информация о пользователе|
api/v1/auth/token/	|POST|	```{"username": "string","confirmation_code": "string"}|	 {"token": "string"}
api/v1/titles/	|GET|		|Список произведения|	Показать список произведений
api/v1/titles/{title_id}/reviews/ |POST|	{"text": "string","score": 1}	|Информация об отзывах	|Разместить отзыв

## Участники:
- [Илья](https://github.com/dartilius) разрабатывал: систему регистрации и аутентификации, права доступа, работу с токеном,
систему подтверждения через e-mail.
- [Соня](https://github.com/Sonya-yandex) отвечала за: модели, view и эндпойнты для произведений, категорий, жанров;
реализовавывала импорта данных из csv файлов.
- [Николай](https://github.com/nikolala13) разрабатывал отзывы, комментарии, рейтинг произведений.
