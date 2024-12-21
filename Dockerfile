# Используем официальный образ Python как базовый
FROM python:3.12

# Устанавливаем curl для загрузки poetry
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Создаем каталог для проекта
RUN mkdir /wallet

# Устанавливаем рабочую директорию
WORKDIR /wallet

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Добавляем poetry в PATH
ENV PATH="/root/.local/bin:$PATH"

# Устанавливаем PYTHONPATH, чтобы Python мог найти модули в каталоге src
ENV PYTHONPATH=/wallet/src

# Копируем pyproject.toml и poetry.lock для установки зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости через poetry
RUN poetry install

# Копируем все оставшиеся файлы проекта
COPY . .

# Запускаем приложение через poetry и gunicorn
CMD ["poetry", "run", "gunicorn", "src.main:app", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]


