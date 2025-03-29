# Проект «API для Yatube»

## Описание

Этот проект представляет собой API для социальной сети Yatube. Он предоставляет пользователям возможность создавать и комментировать посты, подписываться на других пользователей и управлять своими подписками.

## Используемые технологии

*   **Python:** Основной язык программирования.
*   **Django:** Python Web Framework для создания API.
*   **Django REST Framework (DRF):**  Библиотека для создания RESTful API.
*   **JWT (JSON Web Tokens):** Для аутентификации и авторизации пользователей.
*   **Postman:** Инструмент для тестирования API.

## Об авторе

*   **Имя:**  Nikita Neupokoev
*   **GitHub:** [https://github.com/NikitaNeupokoev]
*   **Дополнительная информация:**  ЯП. Студент факультета Бэкенд. Когорта №102

## Установка

1.  **Клонирование репозитория:**

    ```bash
    git clone https://github.com/NikitaNeupokoev/api_final_yatube.git
    cd api_final_yatube
    ```

2.  **Создание и активация виртуального окружения:**

    ```bash
    # Создание для Linux/macOS
    python3 -m venv venv

    # Создание для Windows
    python -m venv venv

    # Активация для Linux/macOS
    source venv/bin/activate

    # Активация для Windows
    venv\Scripts\activate
    ```

3.  **Обновление pip (рекомендуется):**

    ```bash
    python -m pip install --upgrade pip
    ```

4.  **Установка зависимостей:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Применение миграций:**

    ```bash
    # Переходим в папку с manage.py
    cd yatube_api

    python manage.py migrate
    ```

6.  **Запуск сервера:**

    ```bash
    python manage.py runserver
    ```

    Сервер будет запущен по адресу `http://127.0.0.1:8000/`.

## Используемые технологии

*   **Python:** Основной язык программирования.
*   **Django:** Python Web Framework для создания API.
*   **Django REST Framework (DRF):**  Библиотека для создания RESTful API.
*   **JWT (JSON Web Tokens):** Для аутентификации и авторизации пользователей.
*   **Postman:** Инструмент для тестирования API.

## Об авторе

*   **Имя:**  Nikita Neupokoev
*   **GitHub:** [https://github.com/NikitaNeupokoev]
*   **Дополнительная информация:**  ЯП. Студент факультета Бэкенд. Когорта №102

### Примеры запросов API

Все запросы к API должны начинаться с префикса `/api/v1/`.

#### Аутентификация (Примеры)

*   **Регистрация нового пользователя:**

    ```
    POST /api/v1/users/
    ```

    **Пример запроса (Body - raw JSON):**

    ```json
    {
        "username": "username",
        "password": "password123"
    }
    ```

*   **Получение JWT access токена:**

    ```
    POST /api/v1/jwt/create/
    ```

    **Пример запроса (Body - raw JSON):**

    ```json
    {
        "username": "username",
        "password": "password123"
    }
    ```

#### Posts

*   **Получение списка постов:**

    ```
    GET /api/v1/posts/
    ```

    **Требуется аутентификация:** Нет (чтение доступно всем).

*   **Создание поста:**

    ```
    POST /api/v1/posts/
    ```

    **Требуется аутентификация:** Да.

    **Заголовки:**

    ```
    Content-Type: application/json
    Authorization: Bearer <your_access_token>
    ```

    **Пример запроса (Body - raw JSON):**

    ```json
    {
        "text": "Текст вашего поста",
        "group": 1,
        "image": "url_изображения" 
    }
    ```

*   **Получение конкретного поста:**

    ```
    GET /api/v1/posts/{post_id}/
    ```

    **Требуется аутентификация:** Нет (чтение доступно всем).

*   **Редактирование поста:**

    ```
    PUT /api/v1/posts/{post_id}/
    PATCH /api/v1/posts/{post_id}/
    ```

    **Требуется аутентификация:** Да, только автор поста.

*   **Удаление поста:**

    ```
    DELETE /api/v1/posts/{post_id}/
    ```

    **Требуется аутентификация:** Да, только автор поста.

#### Comments

*   **Получение комментариев к посту:**

    ```
    GET /api/v1/posts/{post_id}/comments/
    ```

    **Требуется аутентификация:** Нет (чтение доступно всем).

*   **Создание комментария к посту:**

    ```
    POST /api/v1/posts/{post_id}/comments/
    ```

    **Требуется аутентификация:** Да.

    **Заголовки:**

     ```
    Content-Type: application/json
    Authorization: Bearer <your_access_token>
    ```

    **Пример запроса (Body - raw JSON):**

    ```json
    {
        "text": "Текст комментария"
    }
    ```

#### Follow

*   **Получение списка подписок:**

    ```
    GET /api/v1/follow/
    ```

    **Требуется аутентификация:** Да.

    **Параметр search:**  Позволяет искать подписки по username пользователя, на которого подписаны.

    **Пример:**

    ```
    GET /api/v1/follow/?search=username
    ```

*   **Подписка на пользователя:**

    ```
    POST /api/v1/follow/
    ```

    **Требуется аутентификация:** Да.

    **Заголовки:**

    ```
    Content-Type: application/json
    Authorization: Bearer <your_access_token>
    ```

    **Пример запроса (Body - raw JSON):**

    ```json
    {
        "following": <id_пользователя>
    }
    ```

#### Groups

*   **Получение списка групп:**

    ```
    GET /api/v1/groups/
    ```

    **Требуется аутентификация:** Нет (чтение доступно всем).

*   **Получение конкретной группы:**

    ```
    GET /api/v1/groups/{group_id}/
    ```

    **Требуется аутентификация:** Нет (чтение доступно всем).
