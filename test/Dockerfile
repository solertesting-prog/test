# Dockerfile

FROM python:3.13.3

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY .env .env
COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock
COPY .python-version .python-version
# Sync
RUN pip3 install --no-cache-dir --upgrade .[dev]

COPY . .
