FROM python:3.12-slim

# Настройки Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

# Установка Poetry
RUN python -m pip install --upgrade pip \
    && pip install poetry

# Создание рабочей директории
WORKDIR /app

# Копируем только файлы зависимостей
COPY pyproject.toml poetry.lock* /app/

# Установка зависимостей
RUN poetry install --no-root --only main

# Копируем весь проект
COPY . .

# Открываем порт приложения
EXPOSE 8000

# Указываем команду запуска контейнера
CMD ["gunicorn", "article_hub.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
