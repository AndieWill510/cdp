#!/usr/bin/env bash
set -Eeuo pipefail

if [ -z "${BASH_VERSION:-}" ]; then
  exec bash "$0" "$@"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${SCRIPT_DIR}/.."
COMPOSE_FILE="${REPO_ROOT}/docker/docker-compose.yml"
LOG_DIR="${CDP_TEST_LOG_DIR:-${REPO_ROOT}/tests/out}"
TEST_SUITE_SCRIPT="${CDP_TEST_SUITE_SCRIPT:-${REPO_ROOT}/scripts/test_suite.sh}"
RUN_ID="$(date +%Y%m%d_%H%M%S)"
LOG_FILE="${LOG_DIR}/codex_test_loop_${RUN_ID}.log"

mkdir -p "${LOG_DIR}"
cd "${REPO_ROOT}"

function capture_logs() {
  local exit_code=$?

  echo "== Capturing Docker logs to ${LOG_FILE} =="
  docker compose -f "${COMPOSE_FILE}" logs --no-color --tail=500 >"${LOG_FILE}" 2>&1 || true

  if [ "${exit_code}" -ne 0 ]; then
    echo "Codex test loop failed with exit code ${exit_code}." >&2
    echo "Docker logs: ${LOG_FILE}" >&2
  else
    echo "Docker logs: ${LOG_FILE}"
  fi

  exit "${exit_code}"
}

trap capture_logs EXIT

function wait_for_url() {
  local url=$1
  local attempts=${2:-60}
  local delay_seconds=${3:-2}

  for ((attempt = 1; attempt <= attempts; attempt++)); do
    if curl -fsS "${url}" >/dev/null 2>&1; then
      return 0
    fi

    if [ "${attempt}" -eq "${attempts}" ]; then
      echo "ERROR: ${url} did not become healthy after ${attempts} attempts." >&2
      return 1
    fi

    sleep "${delay_seconds}"
  done
}

function wait_for_postgres() {
  local attempts=${1:-60}
  local delay_seconds=${2:-2}

  for ((attempt = 1; attempt <= attempts; attempt++)); do
    if docker compose -f "${COMPOSE_FILE}" exec -T postgres pg_isready -U cdp -d cdp >/dev/null 2>&1; then
      return 0
    fi

    if [ "${attempt}" -eq "${attempts}" ]; then
      echo "ERROR: PostgreSQL did not become healthy after ${attempts} attempts." >&2
      return 1
    fi

    sleep "${delay_seconds}"
  done
}

function localstack_exec() {
  docker compose -f "${COMPOSE_FILE}" exec -T localstack awslocal "$@"
}

function require_localstack_resource() {
  local description=$1
  shift
  local output

  if ! output="$(localstack_exec "$@" 2>&1)"; then
    echo "ERROR: Required LocalStack resource is unavailable: ${description}." >&2
    if [ -n "${output}" ]; then
      echo "${output}" >&2
    fi
    return 1
  fi
}

function verify_localstack_bootstrap_once() {
  local bucket
  local queue
  local parameter
  local secret

  for bucket in cdp-evidence-local cdp-artifacts-local cdp-exports-local; do
    require_localstack_resource "S3 bucket ${bucket}" \
      s3api head-bucket --bucket "${bucket}" || return 1
  done

  for queue in \
    cdp-intake-queue \
    cdp-review-queue \
    cdp-execution-queue \
    cdp-appeal-queue \
    cdp-repair-queue \
    cdp-dead-letter-queue; do
    require_localstack_resource "SQS queue ${queue}" \
      sqs get-queue-url --queue-name "${queue}" || return 1
  done

  require_localstack_resource "EventBridge bus cdp-events-local" \
    events describe-event-bus --name cdp-events-local || return 1

  require_localstack_resource "DynamoDB table cdp-idempotency-local" \
    dynamodb describe-table --table-name cdp-idempotency-local || return 1

  for parameter in \
    /cdp/local/database-url \
    /cdp/local/qdrant-url \
    /cdp/local/redis-url \
    /cdp/local/default-policy-profile \
    /cdp/local/event-bus-name; do
    require_localstack_resource "SSM parameter ${parameter}" \
      ssm get-parameter --name "${parameter}" || return 1
  done

  for secret in /cdp/local/signing-key /cdp/local/database-password; do
    require_localstack_resource "Secrets Manager secret ${secret}" \
      secretsmanager get-secret-value --secret-id "${secret}" || return 1
  done

  echo "Verified required LocalStack bootstrap resources."
}

function wait_for_localstack_bootstrap() {
  local attempts=${CDP_LOCALSTACK_BOOTSTRAP_ATTEMPTS:-60}
  local delay_seconds=${CDP_LOCALSTACK_BOOTSTRAP_DELAY_SECONDS:-2}
  local verification_output

  for ((attempt = 1; attempt <= attempts; attempt++)); do
    if verification_output="$(verify_localstack_bootstrap_once 2>&1)"; then
      echo "${verification_output}"
      return 0
    fi

    if [ "${attempt}" -eq "${attempts}" ]; then
      echo "ERROR: LocalStack bootstrap did not complete after ${attempts} attempts." >&2
      echo "${verification_output}" >&2
      return 1
    fi

    sleep "${delay_seconds}"
  done
}

CURRENT_BRANCH="$(git branch --show-current)"

if [ -z "${CURRENT_BRANCH}" ]; then
  echo "ERROR: Unable to determine the current Git branch." >&2
  exit 1
fi

if [ "${CURRENT_BRANCH}" = "main" ]; then
  echo "ERROR: Refusing to run the Codex repair loop on main." >&2
  exit 1
fi

echo "== Git context =="
echo "Branch: ${CURRENT_BRANCH}"
git status --short

echo "== Validating Docker Compose configuration =="
docker compose -f "${COMPOSE_FILE}" config --quiet

echo "== Building and starting CDP headlessly =="
docker compose -f "${COMPOSE_FILE}" up --build -d

echo "== Waiting for PostgreSQL =="
wait_for_postgres

echo "== Waiting for CDP API =="
wait_for_url "${BASE_URL:-http://localhost:8000}/health"

echo "== Waiting for LocalStack =="
wait_for_url "${LOCALSTACK_HEALTH_URL:-http://localhost:4566/_localstack/health}"

echo "== Docker service status =="
docker compose -f "${COMPOSE_FILE}" ps

echo "== Running CDP test suite =="
if [ "${1:-}" = "--" ]; then
  shift
fi
bash "${TEST_SUITE_SCRIPT}" "$@"

echo "== Verifying LocalStack bootstrap resources =="
wait_for_localstack_bootstrap

echo "== Verifying CDP database tables =="
TABLE_COUNT="$(
  docker compose -f "${COMPOSE_FILE}" exec -T postgres \
    psql -U cdp -d cdp -Atqc \
    "SELECT count(*) FROM pg_catalog.pg_tables WHERE schemaname NOT IN ('pg_catalog', 'information_schema');"
)"

if ! [[ "${TABLE_COUNT}" =~ ^[0-9]+$ ]]; then
  echo "ERROR: PostgreSQL returned an invalid table count: ${TABLE_COUNT}" >&2
  exit 1
fi

if [ "${TABLE_COUNT}" -eq 0 ]; then
  echo "ERROR: The cdp database contains no user tables." >&2
  echo "Inspect docker/postgres/init and remember that entrypoint initialization runs only for a new data directory." >&2
  exit 1
fi

echo "Verified ${TABLE_COUNT} user table(s) in the cdp database."
echo "Codex test loop passed. Containers and volumes were preserved for inspection."
