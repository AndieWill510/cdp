#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8000}"

echo "Checking health..."
curl -fsS "$BASE_URL/health" >/dev/null

echo "Creating proposal..."
PROPOSAL_RESPONSE=$(curl -fsS -X POST "$BASE_URL/proposals" \
  -H 'Content-Type: application/json' \
  -d '{"actor_id":"andie","proposal":"Smoke test DecisionEnvelope"}')

RECORD_ID=$(python -c 'import json,sys; print(json.load(sys.stdin)["id"])' <<< "$PROPOSAL_RESPONSE")
echo "Record id: $RECORD_ID"

echo "Adding challenge..."
curl -fsS -X POST "$BASE_URL/challenges" \
  -H 'Content-Type: application/json' \
  -d "{\"record_id\":\"$RECORD_ID\",\"actor_id\":\"reviewer\",\"challenge\":\"Verify v0.1 spine before scope expansion\"}" >/dev/null

echo "Adding adjudication..."
curl -fsS -X POST "$BASE_URL/adjudications" \
  -H 'Content-Type: application/json' \
  -d "{\"record_id\":\"$RECORD_ID\",\"actor_id\":\"runner\",\"adjudication\":\"Smoke test passed\"}" >/dev/null

echo "Reading record..."
FINAL_RESPONSE=$(curl -fsS "$BASE_URL/records/$RECORD_ID")
STATUS=$(python -c 'import json,sys; print(json.load(sys.stdin)["status"])' <<< "$FINAL_RESPONSE")
RECORD_HASH=$(python -c 'import json,sys; print(json.load(sys.stdin)["record_hash"])' <<< "$FINAL_RESPONSE")

test "$STATUS" = "adjudicated"
test "${#RECORD_HASH}" -eq 64

echo "Smoke test passed"
