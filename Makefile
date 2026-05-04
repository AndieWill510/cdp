COMPOSE_FILE ?= docker/docker-compose.yml
PYTEST ?= pytest

.PHONY: help up up-build down down-volumes ps logs logs-api logs-worker logs-localstack smoke test verify shell-postgres localstack-health localstack-buckets localstack-queues

help:
	@echo "CDP local development commands"
	@echo ""
	@echo "  make up                 Start the local stack"
	@echo "  make up-build           Build and start the local stack"
	@echo "  make down               Stop the local stack"
	@echo "  make down-volumes       Stop the stack and remove local volumes"
	@echo "  make ps                 Show compose service status"
	@echo "  make logs               Tail all logs"
	@echo "  make logs-api           Tail API logs"
	@echo "  make logs-worker        Tail worker logs"
	@echo "  make logs-localstack    Tail LocalStack logs"
	@echo "  make smoke              Run shell-based local smoke tests"
	@echo "  make test               Run pytest build verification tests"
	@echo "  make verify             Run smoke + pytest verification tests"
	@echo "  make shell-postgres     Open psql in the Postgres container"
	@echo "  make localstack-health  Check LocalStack health endpoint"
	@echo "  make localstack-buckets List LocalStack S3 buckets"
	@echo "  make localstack-queues  List LocalStack SQS queues"

up:
	docker compose -f $(COMPOSE_FILE) up -d

up-build:
	docker compose -f $(COMPOSE_FILE) up --build -d

down:
	docker compose -f $(COMPOSE_FILE) down

down-volumes:
	docker compose -f $(COMPOSE_FILE) down -v

ps:
	docker compose -f $(COMPOSE_FILE) ps

logs:
	docker compose -f $(COMPOSE_FILE) logs -f

logs-api:
	docker compose -f $(COMPOSE_FILE) logs -f cdp-api

logs-worker:
	docker compose -f $(COMPOSE_FILE) logs -f cdp-worker

logs-localstack:
	docker compose -f $(COMPOSE_FILE) logs -f localstack

smoke:
	bash docker/smoke-test.sh

test:
	$(PYTEST) tests/test_build_verification.py

verify: smoke test

shell-postgres:
	docker compose -f $(COMPOSE_FILE) exec postgres psql -U cdp -d cdp

localstack-health:
	curl -fsS http://localhost:4566/_localstack/health
	@echo ""

localstack-buckets:
	docker compose -f $(COMPOSE_FILE) exec localstack awslocal s3 ls

localstack-queues:
	docker compose -f $(COMPOSE_FILE) exec localstack awslocal sqs list-queues
