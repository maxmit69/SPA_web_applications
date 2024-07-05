# SPA Web Applications

SPA Web Applications - это проект, предназначенный для управления привычками пользователей, с интеграцией напоминаний через Telegram и использованием Django и Celery.

## Оглавление

- [Установка](#установка)
- [Использование](#использование)
- [API](#api)
- [Тестирование](#тестирование)
- [Дополнительная информация](#дополнительная-информация)

## Установка

### Предварительные требования

- Python 3.12
- [Poetry](https://python-poetry.org/)

### Шаги для установки

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/maxmit69/SPA_web_applications.git
   cd SPA_web_applications

2. Установите зависимости с помощью Poetry:

   ```bash
   poetry install
   
3. Создайте файл .env в корне проекта и добавьте необходимые переменные окружения. 
   Пример:

   ```bash
   SECRET_KEY=your_secret_key
   DEBUG=True
   DATABASE_URL=postgres://user:password@localhost:5432/yourdatabase
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   
4. Примените миграции базы данных:
   
   ```bash
   poetry run python manage.py migrate
   
5. Создайте суперпользователя для доступа к административной панели:
   
   ```bash
   poetry run python manage.py create_superuser
   
6. Запустите сервер разработки:
   
   ```bash
   poetry run python manage.py runserver

## Использование

### Запуск Celery и Redis

1. Запустите Redis:

   ```bash
   redis-server
   
2. Запустите Celery worker и beat:

   ```bash
   celery -A config worker --beat --scheduler django --loglevel=info
   
### Настройка CORS

   Для настройки CORS, чтобы фронтенд мог подключаться к проекту на развернутом сервере,
   добавьте следующие настройки в settings.py:
   
      ```python
      CORS_ALLOWED_ORIGINS = [
       "http://localhost:3000",
       "http://your-frontend-domain.com",
      ]
      
      INSTALLED_APPS += [
          'corsheaders',
      ]
      
      MIDDLEWARE = [
          'corsheaders.middleware.CorsMiddleware',
          # другие middlewares
      ]

## API

### Список эндпоинтов
   
*    GET /habits/habit/ - Список привычек текущего пользователя с пагинацией.
*    GET /habits/public-habits/ - Список публичных привычек.
*    POST /habits/create-habit/ - Создание привычки.
*    PUT /habits/update-habit/<int:pk>/ - Редактирование привычки.
*    DELETE /habits/delete-habit/<int:pk>/ - Удаление привычки.
*    POST /users/register/ - Регистрация
*    POST /users/login/ - Авторизация
*    POST /users/token/refresh/ - Обновление токена
*    GET /swagger/ - API свагер
*    GET /redoc/ - API редок

### Примеры запросов

Создание привычки

      ```bash
      curl -X POST http://localhost:8000/habits/create-habit/ -H "Content-Type: application/json" -d '{
        "place": "Спортзал",
        "time_start_habits": "07:00:00",
        "action": "Тренировка",
        "pleasant_habit": true,
        "reminder_frequency_days": "mon",
        "time_perform": "00:01:30",
        "is_public": false
      }'

## Тестирование

Для запуска тестов используйте:

      ```bash
      poetry run python manage.py test

Для получения покрытия тестами используйте coverage:

1. Установите coverage:

   ```bash
   poetry add --dev coverage

2. Запустите тесты с покрытием:

   ```bash
   poetry run coverage run --source='.' manage.py test

3. Сгенерируйте отчет:

   ```bash
   poetry run coverage html

4. Откройте отчет:

   ```bash
   open htmlcov/index.html


## Дополнительная информация

   Swagger
   Для включения Swagger добавьте в settings.py:

      ```python
      SWAGGER_SETTINGS = {
          'SECURITY_DEFINITIONS': {
              'api_key': {
                  'type': 'apiKey',
                  'in': 'header',
                  'name': 'Authorization'
              }
          },
          'USE_SESSION_AUTH': False,
      }

### Загрузка фикстур

Для загрузки фикстур в базу данных используйте команды:

      ```bash
      python manage.py loaddata users/fixtures/users.json
      python manage.py loaddata habits/fixtures/habits.json

### Лицензия

Этот проект лицензирован под лицензией MIT - подробности см. в файле LICENSE.