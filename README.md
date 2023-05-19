# Collect_weather_service
## Описание проекта:
Микросервис, собирающий информацию по самым большим городам мира, опрашивая
[ninjas.com](https://api-ninjas.com/api/city) , и 
на основе собранных данных проводит опрос API  [openweathermap](https://openweathermap.org).
Все данные записываются в БД [PostgreSQL](https://www.postgresql.org/).Управляет сервисом 
[FastAPI](https://fastapi.tiangolo.com/).

## Запуск проекта

1. Клонируем репозиторий
```commandline
$ git clone https://github.com/femakc/collect_weather.git
```

2. Перед запуском сервиса необходимо добавить в корень проекта файл *.env* переменные окружения :

- X_API_KEY - доступ к API *ninjas.com* 
[инструкция по получению](https://api-ninjas.com/faq#as-1)

- API_KEY - доступ к API *openweathermap.org* 
[инструкция по получению](https://openweathermap.org/appid)

### .env
```dotenv
X_API_KEY=api_key_api-ninjas
BASE_URL=https://api.openweathermap.org/
API_KEY=api_key_openweathermap.org
DB_NAME=cw
POSTGRES_USER=cw
POSTGRES_PASSWORD=cw
POSTGRES_URL=postgresql+asyncpg://cw:cw@0.0.0.0:5432/cw
```

3. Запукаем Docker-compose файл
```commandline
$ docker-compose up -d
```

**После успешного запуска сервис начнет сбор данных, 
которые будут автоматически обновляться каждый час.**

Получить данные можно по адресу http://localhost/api/get_weather

После запуска будет доступна документация по адресам: 

http://localhost/redoc

http://localhost/docs

## Пример полученных данных
```json
[
    {
        "id": 1,
        "name": "Tokyo",
        "latitude": 35.6897,
        "longitude": 139.692,
        "country": "JP",
        "population": 37977000,
        "is_capital": true,
        "weather_id": 401,
        "weather": {
            "id": 401,
            "temp": 19,
            "timestamp": "2023-05-16T16:59:25+00:00"
        }
    },
    {
        "id": 2,
        "name": "Jakarta",
        "latitude": -6.2146,
        "longitude": 106.845,
        "country": "ID",
        "population": 34540000,
        "is_capital": true,
        "weather_id": 402,
        "weather": {
            "id": 402,
            "temp": 30,
            "timestamp": "2023-05-16T16:59:25+00:00"
        }
    }
]
```

