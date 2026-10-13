# Multi-stage build.

# Stages:
#   - deps: Prepares the runtime environment
#   - app: Adds application code

# Stage `deps`
FROM ghcr.io/astral-sh/uv:0.9.26-python3.12-trixie-slim AS deps

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    # GeoDjango dependencies:
    gdal-bin libsqlite3-mod-spatialite \
    # sqlite CLI enables consistent database backups (even with concurrent writers):
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV UV_COMPILE_BYTECODE=1
# Keep the virtualenv outside /app, so the code can be bind-mounted over /app (e.g. for tests)
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev
ENV PATH="/opt/venv/bin:$PATH"

# Stage `app`
FROM deps

COPY . .

ENV DATABASE_URL=spatialite:////data/db.sqlite3

RUN SECRET_KEY=collectstatic python manage.py collectstatic --no-input

VOLUME /data
EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --no-input && exec gunicorn dumpstermap.wsgi --bind 0.0.0.0:8000"]
