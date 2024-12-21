# Используем официальный образ Python как базовый
FROM python:3.12

# Устанавливаем curl для загрузки poetry и другие необходимые пакеты
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Создаем каталог для проекта
RUN mkdir /wallet

# Устанавливаем рабочую директорию
WORKDIR /wallet

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    echo "PATH=\$PATH:/root/.local/bin" >> ~/.bashrc

# Устанавливаем PYTHONPATH, чтобы Python мог найти модули в каталоге src
ENV PYTHONPATH=/wallet/src
ENV PATH="/root/.local/bin:$PATH"

# Копируем pyproject.toml и poetry.lock для установки зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости через poetry (включая alembic)
RUN poetry install --no-dev

# Копируем все оставшиеся файлы проекта
COPY . .

# Делаем скрипт app.sh исполнимым
RUN chmod +x /wallet/app.sh
