# CDP worker container
#
# Build context is the repository root when invoked by docker/docker-compose.yml:
#   docker compose -f docker/docker-compose.yml up --build cdp-worker
#
# This Dockerfile mirrors docker/api.Dockerfile so API and worker containers
# share the same dependency and package-install behavior.

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

# Default module path. Adjust once the worker package skeleton is finalized.
# Common target would be something like: cdp.worker.main
ENV CDP_WORKER_MODULE=cdp.worker.main

# No HTTP healthcheck by default: workers may not expose an HTTP port.
# Compose-level checks can be added later once the worker has a heartbeat,
# Redis key, metrics endpoint, or queue polling status.

CMD ["sh", "-c", "python -m ${CDP_WORKER_MODULE}"]
