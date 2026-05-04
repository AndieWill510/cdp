# CDP Docker Local Stack

This directory contains the local development stack for the Constitutional Decision Plane (CDP).

The stack is designed to run on a laptop using Docker Compose while preserving a clean path to cloud deployment.

---

## Quick Start

Run from the repository root:

```bash
docker compose -f docker/docker-compose.yml up --build
```

To stop the stack:

```bash
docker compose -f docker/docker-compose.yml down
```

To stop the stack and remove local volumes:

```bash
docker compose -f docker/docker-compose.yml down -v
```

---

## Services

| Service | Purpose | Local Port |
|---|---|---:|
| `cdp-api` | FastAPI governance API container | `8000` |
| `cdp-worker` | Queue consumer / async worker container | n/a |
| `postgres` | Postgres + pgvector transactional store | `5432` |
| `qdrant` | Vector database for semantic retrieval | `6333`, `6334` |
| `redis` | Cache, leases, short-lived grants, coordination | `6379` |
| `localstack` | Local AWS service emulation | `4566` |

---

## LocalStack Resources

LocalStack is initialized by:

```text
docker/localstack/init/01-bootstrap-cdp.sh
```

It creates:

### S3 Buckets

```text
cdp-evidence-local
cdp-artifacts-local
cdp-exports-local
```

### SQS Queues

```text
cdp-intake-queue
cdp-review-queue
cdp-execution-queue
cdp-appeal-queue
cdp-repair-queue
cdp-dead-letter-queue
```

### EventBridge

```text
cdp-events-local
```

### DynamoDB

```text
cdp-idempotency-local
```

### SSM Parameters

```text
/cdp/local/database-url
/cdp/local/qdrant-url
/cdp/local/redis-url
/cdp/local/default-policy-profile
/cdp/local/event-bus-name
```

### Secrets Manager

```text
/cdp/local/signing-key
/cdp/local/database-password
```

---

## Postgres Initialization

Postgres is initialized by:

```text
docker/postgres/init/01-init-cdp.sql
```

It creates:

```text
Extensions:
  vector
  pgcrypto

Schemas:
  cdp_core
  cdp_audit
  cdp_repair
  cdp_projection

Smoke-test tables:
  cdp_core.schema_version
  cdp_audit.event_log
  cdp_projection.vector_smoke_test
```

Canonical schema design should move into migrations once the package skeleton is established.

---

## Current Placeholders

The API and worker containers assume conventional Python module paths:

```text
CDP_API_APP=cdp.api.main:app
CDP_WORKER_MODULE=cdp.worker.main
```

These are placeholders until the application skeleton exists.

Expected future files might include:

```text
cdp/api/main.py
cdp/worker/main.py
pyproject.toml
requirements.txt
```

---

## Health Checks

Current health checks:

| Service | Health Check |
|---|---|
| `postgres` | `pg_isready -U cdp -d cdp` |
| `redis` | `redis-cli ping` |
| `localstack` | `/_localstack/health` |
| `cdp-api` | `GET /health` from inside the container |

The API health check will fail until the FastAPI app provides `/health`.

The worker has no health check yet. Add one once the worker exposes a heartbeat, metrics endpoint, Redis key, or queue status signal.

---

## Useful Local Commands

Check running containers:

```bash
docker compose -f docker/docker-compose.yml ps
```

Tail logs:

```bash
docker compose -f docker/docker-compose.yml logs -f
```

Tail one service:

```bash
docker compose -f docker/docker-compose.yml logs -f localstack
```

Open Postgres shell:

```bash
docker compose -f docker/docker-compose.yml exec postgres psql -U cdp -d cdp
```

List LocalStack S3 buckets:

```bash
docker compose -f docker/docker-compose.yml exec localstack awslocal s3 ls
```

List LocalStack SQS queues:

```bash
docker compose -f docker/docker-compose.yml exec localstack awslocal sqs list-queues
```

Check LocalStack health:

```bash
curl http://localhost:4566/_localstack/health
```

---

## Design Posture

This local stack follows a pragmatic separation of responsibilities:

| Responsibility | Local Technology |
|---|---|
| Transactional governance state | Postgres |
| Small/medium vector retrieval | Postgres + pgvector |
| Larger semantic retrieval | Qdrant |
| Short-lived runtime state | Redis |
| Evidence and artifacts | LocalStack S3 |
| Work queues | LocalStack SQS |
| Domain events | LocalStack EventBridge |
| Local secrets/config | LocalStack Secrets Manager + SSM |
| Idempotency / locks | LocalStack DynamoDB |

LocalStack is for AWS-like service emulation. It is not the local database layer.

---

## Next Steps

Likely next implementation steps:

1. Add a minimal Python package skeleton.
2. Add `pyproject.toml` or `requirements.txt`.
3. Add `cdp/api/main.py` with `/health`.
4. Add `cdp/worker/main.py` with a safe no-op polling loop.
5. Add real migrations.
6. Add bootstrap tests for Postgres, Qdrant, Redis, and LocalStack.
