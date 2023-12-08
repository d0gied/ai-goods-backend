# Build: docker build -t goodsai-parser:latest ./services/ -f ./services/parser/Dockerfile
FROM python:3.11.5-slim

ARG TARGET_SERVICE

WORKDIR /app

RUN pip install poetry

COPY ${TARGET_SERVICE}/pyproject.toml ${TARGET_SERVICE}/poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-interaction --no-ansi

COPY ${TARGET_SERVICE}/ /app


