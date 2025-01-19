FROM python:3.12

# Устанавливаем curl для загрузки poetry и другие необходимые пакеты
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN mkdir /wallet

WORKDIR /wallet

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    echo "PATH=\$PATH:/root/.local/bin" >> ~/.bashrc

# Устанавливаем PYTHONPATH, чтобы Python мог найти модули в каталоге src
ENV PYTHONPATH=/wallet/src
ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main

COPY . .

# Делаем скрипт app.sh исполняемым
RUN chmod +x /wallet/app.sh
