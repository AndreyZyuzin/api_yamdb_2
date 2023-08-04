# Групповой проект YaMDB

## Описание
YaMDB - Backend сервис для работы с произведениями иссуства, написанием обзоров и комментариев, построенный на принципах REST API
### Зависимости
Для работоспобности необходимые следующие библиотеки:
>requests 2.26.0  
Django 3.2    
djangorestframework 3.12.4  
PyJWT 2.1.0  
django-filter 22.1
djangorestframework 3.12.4  


### Установка
Клонируйте репозиторий коммандой `git clone git@github.com:mxstrv/api_yamdb.git`

Создайте виртуальное окружение   `python3 -m venv venv`

Активируйте виртуальное окружение `source venv/bin/activate`(для Linux и MacOS) `source venv/Scripts/activate` (для Windows)

Установите зависимости `pip install -r requirements.txt`

Выполните миграции `python manage.py makemigration && python manage.py migrate`

Запустите сервер `python manage.py runserver`

### Описание и примеры запросов
### Регистрация пользователя
Для регистрации пользователя необходимо отправить POST запрос на URL `http://127.0.0.1:8000/api/v1/auth/signup/`
в формате 
>`{
"email": "user@example.com",
"username": "username"
}`
> 
Затем на e-mail придет код подтверждения. Его, и e-mail, необходимо отправить POST запросом на URL`http://127.0.0.1:8000/api/v1/auth/token/`
в формате
>`{
"username": "username", "confirmation_code": "code"
}`
> 
В ответе будет JWT токен, необходимый для взаимодействия с web-приложением (Вставляется в формате Bearer "token")
### Работа с пользователями
Пользователю с правами администратора доступно полное взаимодействие с пользователями, а именно:
> Регистрация новых пользователей
> 
> Удаление пользователей
> 
> Изменение их данных, в т.ч. добавление ролей модератора или администратора

Пользователь может найти информацию о себе по URL `http://127.0.0.1:8000/api/v1/users/me/`

### Описание и примеры запросов
### Регистрация пользователя
<details>
<summary><strong>POST</strong> [/api/v1/auth/signup/] - Регистрация нового пользователя</summary>
<pre>
{
  "email": "user@example.com",
  "username": "string"
}
</pre>
</details>

<details>
<summary><strong>POST</strong> [/api/v1/auth/token/] - Получение JWT-токена</summary>
<pre>
{
    "username": "string",
    "confirmation_code": "string"
}
</pre>
</details>

### Работа с пользователями
<details>
<summary><strong>GET</strong> [/api/v1/users/] - Получение списка всех пользователей</summary>
<pre>
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
        {
            "username": "string",
            "email": "user@example.com",
            "first_name": "string",
            "last_name": "string",
            "bio": "string",
            "role": "user"
        }
    ]
}
</pre>
</details>

<details>
<summary><strong>POST</strong> [/api/v1/users/] - Добавление пользователя</summary>
<pre>
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
</pre>
</details>

<details>
<summary><strong>GET</strong> [/api/v1/users/{username}/] - Получение пользователя по username</summary>
<pre>
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
</pre>
</details>

<details>
<summary><strong>PATCH</strong> [/api/v1/users/{username}/] - Изменение данных пользователя по username</summary>
<pre>
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
</pre>
</details>

**DELETE** /api/v1/users/{username}/ - Удаление пользователя по username


<details>
<summary><strong>GET</strong> [/api/v1/users/me/] - Получение данных своей учетной записи</summary>
<pre>
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
</pre>
</details>

<details>
<summary><strong>PATCH</strong> [/api/v1/users/me/] - Изменение данных пользователя по username</summary>
<pre>
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string"
}
</pre>
</details>


### Работа с произведениями

<details>
<summary><strong>GET</strong> [/api/v1/titles/] - Получение списка всех произведений</summary>
<pre>
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
        {
            "id": 0,
            "name": "string",
            "year": 0,
            "rating": 0,
            "description": "string",
            "genre": [
                {
                    "name": "string",
                    "slug": "string"
                }
            ],
            "category": {
                "name": "string",
                "slug": "string"
            }
        }
    ]
}   
</pre>
</details>

<details>
<summary><strong>POST</strong> [/api/v1/titles/] - Добавление произведения</summary>
<pre>
{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
        "string"
    ],
    "category": "string"
}
</pre>
</details>

<details>
<summary><strong>GET</strong> [/api/v1/titles/{titles_id}/] - Получение информации о произведении</summary>
<pre>
{
    "id": 0,
    "name": "string",
    "year": 0,
    "rating": 0,
    "description": "string",
    "genre": [
        {
            "name": "string",
            "slug": "string"
        }
    ],
    "category": {
        "name": "string",
        "slug": "string"
    }
} 
</pre>
</details>


<details>
<summary><strong>PATCH</strong> [/api/v1/titles/{titles_id}/] - Получение информации о произведении</summary>
<pre>
{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
        "string"
    ],
    "category": "string"
}
</pre>
</details>

**DELETE** /api/v1/titles/{titles_id}/ - Удаление произведения


### Работа с категориями произведением

<details>
<summary><strong>GET</strong> [/api/v1/categories/] - Получение списка всех категорий</summary>
<pre>
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
        {
            "name": "string",
            "slug": "string"
        }
    ]
}
</pre>
</details>


<details>
<summary><strong>POST</strong> [/api/v1/categories/] - Добавление новой категории</summary>
<pre>
{
    "name": "string",
    "slug": "string"
}
</pre>
</details>


**DELETE** /api/v1/categories/{slug}/ - Удаление категории



### Работа с жанрами произведением

<details>
<summary><strong>GET</strong> [/api/v1/genres/] - Получение списка всех жанров</summary>
<pre>
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
        {
            "name": "string",
            "slug": "string"
        }
    ]
}
</pre>
</details>


<details>
<summary><strong>POST</strong> [/api/v1/genres/] - Добавление жанра</summary>
<pre>
{
    "name": "string",
    "slug": "string"
}
</pre>
</details>

**DELETE** /api/v1/genres/{slug}/ - Удаление жанра


### Работа с обзорами

<details>
<summary><strong>GET</strong> [/api/v1/titles/{title_id}/reviews/] - Получение списка всех отзывов</summary>
<pre>
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
        {
            "id": 0,
            "text": "string",
            "author": "string",
            "score": 1,
            "pub_date": "2019-08-24T14:15:22Z"
        }
    ]
}
</pre>
</details>


<details>
<summary><strong>POST</strong> [/api/v1/titles/{title_id}/reviews/] - Добавление нового отзыва</summary>
<pre>
{
    "text": "string",
    "score": 1
}
</pre>
</details>


<details>
<summary><strong>GET</strong> [/api/v1/titles/{title_id}/reviews/{review_id}/] - Полуение отзыва по id</summary>
<pre>
{
    "id": 0,
    "text": "string",
    "author": "string",
    "score": 1,
    "pub_date": "2019-08-24T14:15:22Z"
}
</pre>
</details>


<details>
<summary><strong>PATCH</strong> [/api/v1/titles/{title_id}/reviews/{review_id}/] - Частичное обновление отзыва по id</summary>
<pre>
{
    "id": 0,
    "text": "string",
    "author": "string",
    "score": 1,
    "pub_date": "2019-08-24T14:15:22Z"
}
</pre>
</details>

**DELETE** /api/v1/titles/{title_id}/reviews/{review_id}/ - Удаление отзыва по id


### Работа с комментариями

<details>
<summary><strong>GET</strong> [/api/v1/titles/{title_id}/reviews/{review_id}/comments/] - Получение списка всех комментариев к отзыву</summary>
<pre>
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
        {
            "id": 0,
            "text": "string",
            "author": "string",
            "pub_date": "2019-08-24T14:15:22Z"
        }
    ]
}
</pre>
</details>


<details>
<summary><strong>POST</strong> [/api/v1/titles/{title_id}/reviews/{review_id}/comments/] - Добавление комментария к отзыву</summary>
<pre>
{
    "text": "string"
}
</pre>
</details>



<details>
<summary><strong>GET</strong> [/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/] - Получение комментария к отзыву</summary>
<pre>
{
    "id": 0,
    "text": "string",
    "author": "string",
    "pub_date": "2019-08-24T14:15:22Z"
}
</pre>
</details>


<details>
<summary><strong>PATCH</strong> [/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/] - Частичное обновление комментария к отзыву</summary>
<pre>
{
    "text": "string"
}
</pre>
</details>

**DELETE** /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ - Удаление комментария к отзыву

### Документация OpenAPI
Подробная документация по проекту c использованием спецификации OpenAPI доступна по адресу http://127.0.0.1:8000/redoc/

### Авторы
Максим Старовойтов, Андрей Зюзин, Игорь Андреев
