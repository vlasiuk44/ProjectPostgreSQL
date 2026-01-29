# ProjectPostgreSQL

Консольное приложение для работы с PostgreSQL по заданию: две таблицы (Cars и Drivers),
CRUD для первой таблицы, просмотр/добавление/удаление/изменение записей второй таблицы
по ключу из первой, постраничный просмотр и защита от SQL‑инъекций.

## Требования
- Python 3.10+
- PostgreSQL 16+
- Пакеты Python: `psycopg2-binary`, `pyyaml`

## Установка зависимостей
```
python -m pip install psycopg2-binary pyyaml
```

## Настройка
Заполните `config.yaml`:
```
dbname: postgres
user: qwellert
password: 1234
host: localhost
dbtableprefix: "public."
```

## Запуск
```
python main.py
```

## Проверка функционала (быстрый сценарий)
1) В меню выбрать `2` (создание таблиц и демо‑данных).
2) `1` — просмотр автомобилей, переход к водителям выбранного авто.
3) Проверить добавление/изменение/удаление авто и водителей.
4) Проверить постраничный просмотр (пункты 5/6 в меню).

## Структура проекта
- `main.py` — консольный интерфейс и логика меню
- `dbconnection.py` — подключение к PostgreSQL
- `dbtable.py` — базовые операции с таблицами
- `tables/cars_table.py` — таблица Cars
- `tables/drivers_table.py` — таблица Drivers
