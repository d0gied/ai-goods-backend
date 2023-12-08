# Build: docker build -t {service}:latest ./services/ --build-arg TARGET_SERVICE={service}
FROM python:3.11.5-slim

# make it required
ARG TARGET_SERVICE 

WORKDIR /app

RUN pip install poetry

COPY ${TARGET_SERVICE}/pyproject.toml ${TARGET_SERVICE}/poetry.lock ./${TARGET_SERVICE}/

COPY ./global_modules ./global_modules

WORKDIR /app/${TARGET_SERVICE}

RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-interaction --no-ansi

COPY ${TARGET_SERVICE} /app/${TARGET_SERVICE}




