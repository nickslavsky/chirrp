FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock /app/

RUN uv sync --frozen --no-install-project

COPY . /app

RUN uv sync --frozen

ENV PATH="/app/.venv/bin:$PATH"