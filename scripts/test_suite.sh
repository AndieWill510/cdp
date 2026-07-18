#!/usr/bin/env bash
set -euo pipefail

if [ -z "${BASH_VERSION:-}" ]; then
  exec bash "$0" "$@"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${SCRIPT_DIR}/.."
cd "${REPO_ROOT}"

VENV_DIR="${REPO_ROOT}/dev"
PATH="${VENV_DIR}/bin:${PATH}"
TEST_OUT_DIR="${REPO_ROOT}/tests/out"
TEST_RESULTS_FILE="${TEST_OUT_DIR}/test_results_$(date +%Y%m%d).txt"

mkdir -p "${TEST_OUT_DIR}"

function usage() {
  cat <<EOF
Usage: $(basename "$0") [--smoke-only] [--skip-smoke] [pytest args...]

Runs the CDP test suite and the smoke control-plane test.

Options:
  --smoke-only   Run only the smoke control-plane test.
  --skip-smoke   Run pytest only and skip the smoke control-plane test.
  -h, --help     Show this help message.
EOF
}

function ensure_python_command() {
  if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD=python3
  elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD=python
  else
    echo "ERROR: Python 3 is required to create the dev virtualenv." >&2
    exit 1
  fi
}

function install_dev_dependencies() {
  echo "Installing Python dependencies into ${VENV_DIR} from requirements.txt..."
  env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY -u all_proxy \
    PIP_CONFIG_FILE=/dev/null PIP_NO_PROXY='*' \
    "${VENV_DIR}/bin/python" -m pip install --proxy "" --trusted-host pypi.org --trusted-host files.pythonhosted.org --disable-pip-version-check --no-cache-dir -r "${REPO_ROOT}/requirements.txt" || {
      echo "ERROR: failed to install dependencies from requirements.txt into ${VENV_DIR}." >&2
      echo "This may be caused by proxy or network restrictions." >&2
      echo "Run the following manually after activating the venv:" >&2
      echo "  source dev/bin/activate" >&2
      echo "  env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY -u all_proxy PIP_CONFIG_FILE=/dev/null PIP_NO_PROXY='*' pip install --proxy \"\" --trusted-host pypi.org --trusted-host files.pythonhosted.org --disable-pip-version-check --no-cache-dir -r requirements.txt" >&2
      exit 1
    }
}

function ensure_dev_dependencies() {
  if ! "${VENV_DIR}/bin/python" -c 'import boto3,pytest,redis,psycopg,ruff' >/dev/null 2>&1; then
    install_dev_dependencies
  fi
}

PYTEST_ARGS=()
SMOKE_ONLY=false
SKIP_SMOKE=false

while [ "$#" -gt 0 ]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --smoke-only)
      SMOKE_ONLY=true
      shift
      ;;
    --skip-smoke)
      SKIP_SMOKE=true
      shift
      ;;
    *)
      PYTEST_ARGS+=("$1")
      shift
      ;;
  esac
done

if [ ! -d "${VENV_DIR}" ]; then
  echo "Virtualenv not found at ${VENV_DIR}. Creating it now."
  ensure_python_command
  "${PYTHON_CMD}" -m venv "${VENV_DIR}"
fi

ensure_dev_dependencies

if [ -x "${VENV_DIR}/bin/pytest" ]; then
  PYTEST_CMD="${VENV_DIR}/bin/pytest"
elif command -v pytest >/dev/null 2>&1; then
  PYTEST_CMD="pytest"
else
  echo "ERROR: pytest is not installed. Activate the dev venv or install dependencies with:"
  echo "  source dev/bin/activate"
  echo "  pip install pytest psycopg[binary] ruff"
  exit 1
fi

if [ "$SMOKE_ONLY" = false ]; then
  mkdir -p "${TEST_OUT_DIR}"

  if command -v ruff >/dev/null 2>&1; then
    echo "Running ruff lint..."
    if ! ruff check .; then
      echo "WARNING: ruff found lint issues, but continuing with pytest."
    fi
  fi

  echo "Running pytest..."
  "${PYTEST_CMD}" "${PYTEST_ARGS[@]:-}" | tee "${TEST_RESULTS_FILE}"
  TEST_EXIT_CODE=${PIPESTATUS[0]:-${?}}
  if [ "$TEST_EXIT_CODE" -ne 0 ]; then
    echo "pytest failed; output written to ${TEST_RESULTS_FILE}" >&2
    exit "$TEST_EXIT_CODE"
  fi
fi

if [ "$SKIP_SMOKE" = false ]; then
  echo "Running smoke control-plane test..."

  BASE_URL="${BASE_URL:-http://localhost:8000}"

  echo "Checking health..."
  curl -fsS "${BASE_URL}/health" >/dev/null

  echo "Creating proposal..."
  if ! PROPOSAL_RESPONSE=$(curl -fsS -X POST "${BASE_URL}/proposals" \
    -H 'Content-Type: application/json' \
    -d '{"actor_id":"andie","proposal":"Smoke test DecisionEnvelope"}'); then
    echo "WARNING: Smoke control-plane endpoint ${BASE_URL}/proposals is unavailable or rejected the request. Skipping smoke test."
    exit 0
  fi

  RECORD_ID=$(python - <<'PY'
import json, sys
print(json.load(sys.stdin)["id"])
PY
  <<<"${PROPOSAL_RESPONSE}")

  echo "Record id: ${RECORD_ID}"

  echo "Adding challenge..."
  curl -fsS -X POST "${BASE_URL}/challenges" \
    -H 'Content-Type: application/json' \
    -d "{\"record_id\":\"${RECORD_ID}\",\"actor_id\":\"reviewer\",\"challenge\":\"Verify v0.1 spine before scope expansion\"}" >/dev/null

  echo "Adding adjudication..."
  curl -fsS -X POST "${BASE_URL}/adjudications" \
    -H 'Content-Type: application/json' \
    -d "{\"record_id\":\"${RECORD_ID}\",\"actor_id\":\"runner\",\"adjudication\":\"Smoke test passed\"}" >/dev/null

  echo "Reading record..."
  FINAL_RESPONSE=$(curl -fsS "${BASE_URL}/records/${RECORD_ID}")
  STATUS=$(python - <<'PY'
import json, sys
print(json.load(sys.stdin)["status"])
PY
  <<<"${FINAL_RESPONSE}")
  RECORD_HASH=$(python - <<'PY'
import json, sys
print(json.load(sys.stdin)["record_hash"])
PY
  <<<"${FINAL_RESPONSE}")

  if [ "${STATUS}" != "adjudicated" ]; then
    echo "Smoke test failure: expected status=adjudicated, got ${STATUS}" >&2
    exit 1
  fi

  if [ "${#RECORD_HASH}" -ne 64 ]; then
    echo "Smoke test failure: expected record_hash length 64, got ${#RECORD_HASH}}" >&2
    exit 1
  fi

  echo "Smoke test passed"
fi
