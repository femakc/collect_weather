# colllect_weather

X_API_KEY 
```python
https://api-ninjas.com/api/city
```

API_KEY 
```python
https://openweathermap.org
```
### .env
```python
X_API_KEY="hgwMzL0zKdvwe2cljulQ9g==ToLekCxPkDwwFoON"
BASE_URL="https://api.openweathermap.org/"
API_KEY="0101452058a9a7945c8b353b7f8d618f"
DB_NAME="cw"
POSTGRES_USER="cw"
POSTGRES_PASSWORD="cw"
POSTGRES_URL="postgresql+asyncpg://cw:cw@0.0.0.0:5432/cw"
```

Настройка миграций
Для накатывания миграций, если файла alembic.ini ещё нет, нужно запустить в терминале команду:
```python
alembic init migrations
```
После этого будет создана папка с миграциями и конфигурационный файл для алембика.

В alembic.ini нужно задать адрес базы данных, в которую будем катать миграции.

Дальше идём в папку с миграциями и открываем env.py, там вносим изменения в блок, где написано

from myapp import mymodel
Дальше вводим: 
```python
alembic revision --autogenerate -m "comment"
```
Будет создана миграция
Дальше вводим: 
```python
alembic upgrade heads
```