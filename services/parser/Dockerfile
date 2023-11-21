FROM python:3.11.5-slim as builder

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry export --without-hashes --without dev,test -f requirements.txt > requirements.txt

FROM python:3.11.5-slim

WORKDIR /app

COPY --from=builder requirements.txt ./

RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .

