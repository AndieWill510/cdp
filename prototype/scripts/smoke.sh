#!/usr/bin/env bash
set -euo pipefail

curl -s http://localhost:8000/health
echo

curl -s -X POST http://localhost:8000/proposals \
  -H "Content-Type: application/json" \
  -d '{"title":"Review claim","domain":"cms","proposer":"smoke","policy_basis":"risk > 0.9","payload":{"claim_id":"CLM-9","risk_score":0.97}}'
echo
