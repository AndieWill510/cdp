#!/usr/bin/env bash
set -Eeuo pipefail

if [ -z "${BASH_VERSION:-}" ]; then
  exec bash "$0" "$@"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${SCRIPT_DIR}/.."
COMPOSE_FILE="${REPO_ROOT}/docker/docker-compose.yml"
LOG_DIR="${REPO_ROOT}/tests/out"
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

echo "== Docker service status =="
docker compose -f "${COMPOSE_FILE}" ps

echo "== Running CDP test suite =="
if [ "${1:-}" = "--" ]; then
  shift
fi
bash "${REPO_ROOT}/scripts/test_suite.sh" "$@"

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
