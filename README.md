# Advertisement Service API

FastAPI сервис для управления объявлениями купли/продажи с использованием SQLAlchemy и SQLite базы данных.

## Описание

Сервис предоставляет REST API для создания, обновления, удаления и поиска объявлений. Данные хранятся в базе данных SQLite через SQLAlchemy ORM.

## Архитектура

- **База данных**: SQLite с SQLAlchemy ORM
- **Валидация**: Pydantic v2
- **ID**: Integer с автоинкрементом
- **Поиск**: Полнотекстовый поиск по полям с фильтрацией

## Поля объявления

- **title** (str): Заголовок объявления
- **description** (str): Описание объявления  
- **price** (float): Цена
- **author** (str): Автор объявления
- **created_at** (datetime): Дата создания (автоматически)
- **id** (int): Уникальный идентификатор (автоинкремент)

## API Эндпоинты

### Создание объявления
```
POST /advertisement
```
Тело запроса:
```json
{
    "title": "Продам автомобиль",
    "description": "Отличный автомобиль в хорошем состоянии",
    "price": 500000.0,
    "author": "Иван Иванов"
}
```

### Получение объявления по ID
```
GET /advertisement/{advertisement_id}
```
Пример: `GET /advertisement/1`

### Обновление объявления
```
PATCH /advertisement/{advertisement_id}
```
Тело запроса (только поля для обновления):
```json
{
    "price": 450000.0,
    "description": "Новый текст описания"
}
```

### Удаление объявления
```
DELETE /advertisement/{advertisement_id}
```

### Поиск объявлений
```
GET /advertisement?title=автомобиль&description=отличный&author=Иван&min_price=100000&max_price=600000&created_after=2024-01-01T00:00:00&created_before=2024-12-31T23:59:59
```

Параметры запроса:
- `title`: Фильтр по заголовку (частичное совпадение, нечувствительно к регистру)
- `description`: Фильтр по описанию (частичное совпадение, нечувствительно к регистру)
- `author`: Фильтр по автору (частичное совпадение, нечувствительно к регистру)
- `min_price`: Минимальная цена
- `max_price`: Максимальная цена
- `created_after`: Фильтр объявлений, созданных после этой даты (ISO формат)
- `created_before`: Фильтр объявлений, созданных до этой даты (ISO формат)

## Особенности реализации

### ✅ Исправленные недочеты
- **Integer ID**: Используется `Column(Integer, primary_key=True, index=True)` вместо UUID
- **Поиск по description**: Добавлен фильтр через `ilike(f"%{description}%")`
- **Поиск по датам**: Поддержка диапазона дат `created_after`/`created_before`
- **Pydantic v2**: Используется `model_dump(exclude_unset=True)` вместо `dict()`

### 🏗️ Структура проекта
```
├── main.py          # Основные эндпоинты FastAPI
├── database.py      # Модель SQLAlchemy и подключение к БД
├── schemas.py       # Pydantic модели для валидации
├── requirements.txt  # Зависимости проекта
└── README.md       # Документация
```

## Запуск проекта

### Локальный запуск
1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Запустите сервис:
```bash
python main.py
```

### Docker запуск
1. Сборка и запуск через docker-compose:
```bash
docker-compose up --build
```

2. Или сборка Docker образа и запуск:
```bash
docker build -t advertisement-service .
docker run -p 9999:9999 advertisement-service
```

## Документация API

После запуска сервиса документация доступна по адресам:
- Swagger UI: http://localhost:9999/docs
- ReDoc: http://localhost:9999/redoc
- Главная страница: http://localhost:9999/

## Технологический стек

- **FastAPI**: Веб-фреймворк
- **SQLAlchemy**: ORM для работы с базой данных
- **SQLite**: База данных
- **Pydantic v2**: Валидация данных
- **Uvicorn**: ASGI сервер

## Примеры использования

### Создание объявления
```bash
curl -X POST "http://localhost:9999/advertisement" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "iPhone 15 Pro",
       "description": "Новый iPhone 15 Pro в отличном состоянии",
       "price": 999.99,
       "author": "John Doe"
     }'
```

### Поиск по описанию
```bash
curl "http://localhost:9999/advertisement?description=iphone&min_price=500&max_price=1500"
```

### Обновление цены
```bash
curl -X PATCH "http://localhost:9999/advertisement/1" \
     -H "Content-Type: application/json" \
     -d '{"price": 899.99}'
```
