# Сеть по продаже электроники

## Описание

Проект реализует иерархическую сеть по продаже электроники, состоящую из трёх уровней:
- Завод
- Розничная сеть
- Индивидуальный предприниматель

Каждое звено сети может иметь поставщика, продукты, задолженность и контакты. Уровень звена определяется по отношению к другим звеньям.

## Функционал

- Создание, редактирование и удаление звеньев сети
- Управление контактами и продуктами
- Вычисление уровня звена в иерархии
- Админ-панель с возможностью сброса задолженности
- REST API с аутентификацией и фильтрацией
- Тесты и покрытие кода

## Технологии

- Python 3.8+
- Django 4+
- Django REST Framework
- PostgreSQL (или SQLite)
- django-filter
- coverage.py
- Django Admin

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/SarasonAndrey/ellark
   cd ellark
   
2. Создайте виртуальное окружение:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
##### или
    venv\Scripts\activate     # Windows

2. Установите зависимости:
    ```bash
   pip install -r requirements.txt
   
2. Примените миграции:
    ```bash
   python manage.py migrate
   
2. Запустите сервер::
    ```bash
   python manage.py runserver
   
## API
```bash
    http://127.0.0.1:8000//api/docs/
   ```
    
## Лицензия 
MIT