#!/usr/bin/env bash
set -euo pipefail

# CDP local Docker smoke test
#
# Run from the repository root after starting the stack:
#   docker compose -f docker/docker-compose.yml up --build -d
#   bash docker/smoke-test.sh

COMPOSE_FILE="${COMPOSE_FILE:-docker/docker-compose.yml}"
API_URL="${API_URL:-http://localhost:8000}"
LOCALSTACK_URL="${LOCALSTACK_URL:-http://localhost:4566}"

export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID:-test}"
export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY:-test}"
export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"

section() {
  printf '\n==> %s\n' "$1"
}

require_cmd() {
  local cmd="$1"
  if ! command -v "${cmd}" >/dev/null 2>&1; then
    echo "Missing required command: ${cmd}" >&2
    exit 1
  fi
}

compose_exec() {
  docker compose -f "${COMPOSE_FILE}" exec -T "$@"
}

aws_local() {
  if command -v awslocal >/dev/null 2>&1; then
    awslocal "$@"
  else
    aws --endpoint-url "${LOCALSTACK_URL}" "$@"
  fi
}

require_cmd docker
require_cmd curl
require_cmd aws

section "Compose services"
docker compose -f "${COMPOSE_FILE}" ps

section "API health"
curl -fsS "${API_URL}/health"
echo

section "Postgres schema and extensions"
compose_exec postgres psql -U cdp -d cdp -v ON_ERROR_STOP=1 <<'SQL'
SELECT extname FROM pg_extension WHERE extname IN ('vector', 'pgcrypto') ORDER BY extname;
SELECT schema_name FROM information_schema.schemata WHERE schema_name LIKE 'cdp_%' ORDER BY schema_name;
SELECT component, version FROM cdp_core.schema_version ORDER BY component;
SELECT label, embedding FROM cdp_projection.vector_smoke_test ORDER BY created_at LIMIT 1;
SQL

section "Redis ping"
compose_exec redis redis-cli ping

section "Qdrant readiness"
curl -fsS "http://localhost:6333/readyz"
echo

section "LocalStack health"
curl -fsS "${LOCALSTACK_URL}/_localstack/health"
echo

section "LocalStack S3 buckets"
aws_local s3 ls | grep -E 'cdp-(evidence|artifacts|exports)-local'

section "LocalStack SQS queues"
aws_local sqs list-queues --query 'QueueUrls[]' --output text | tr '\t' '\n' | grep -E 'cdp-(intake|review|execution|appeal|repair|dead-letter)-queue'

section "LocalStack EventBridge bus"
aws_local events list-event-buses --query 'EventBuses[].Name' --output text | tr '\t' '\n' | grep '^cdp-events-local$'

section "LocalStack DynamoDB table"
aws_local dynamodb list-tables --query 'TableNames[]' --output text | tr '\t' '\n' | grep '^cdp-idempotency-local$'

section "LocalStack SSM parameters"
aws_local ssm get-parameter --name /cdp/local/database-url --query 'Parameter.Value' --output text
aws_local ssm get-parameter --name /cdp/local/qdrant-url --query 'Parameter.Value' --output text
aws_local ssm get-parameter --name /cdp/local/redis-url --query 'Parameter.Value' --output text

section "Smoke test complete"
echo "CDP local stack smoke test passed."
