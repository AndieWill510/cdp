# CDP API container
#
# Build context is the repository root when invoked by docker/docker-compose.yml:
#   docker compose -f docker/docker-compose.yml up --build cdp-api
#
# This Dockerfile is intentionally conservative. It supports common Python
# dependency layouts and defaults to a conventional FastAPI module path.

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    APP_HOME=/app

WORKDIR ${APP_HOME}

# System packages kept minimal. Add build-essential/libpq-dev later only if
# dependency compilation requires it.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency manifests first for better layer caching.
COPY pyproject.toml poetry.lock* requirements*.txt ./

# Install dependencies for the common repo layouts.
# - requirements.txt: standard pip flow
# - pyproject.toml: install the local package after source copy below
RUN if [ -f requirements.txt ]; then \
        pip install -r requirements.txt; \
    fi

# Copy the rest of the repository.
COPY . .

# If the repo is package-installable, install it in editable mode.
# This is allowed to fail because early architecture repos may not yet define
# a Python package.
RUN if [ -f pyproject.toml ]; then \
        pip install -e . || true; \
    fi

EXPOSE 8000

# Default module path. Adjust once the API package skeleton is finalized.
# Common target would be something like: cdp.api.main:app
ENV CDP_API_APP=cdp.api.main:app

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD curl -fsS http://localhost:8000/health || exit 1

CMD ["sh", "-c", "uvicorn ${CDP_API_APP} --host 0.0.0.0 --port 8000"]
