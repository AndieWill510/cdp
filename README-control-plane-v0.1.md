# CDP Control Plane v0.2

Tiny FastAPI prototype for the first executable CDP object: DecisionEnvelope.

Persistence is Postgres.

## Run

```bash
docker compose up --build
```

This starts:

- postgres
- cdp-control-plane

In a second terminal:

```bash
./scripts/smoke_test_control_plane.sh
```

Expected final line:

```text
Smoke test passed
```

## Health check

```bash
curl http://localhost:8000/health
```

## Create proposal

```bash
curl -X POST http://localhost:8000/proposals \
  -H 'Content-Type: application/json' \
  -d '{"actor_id":"andie","proposal":"Create first DecisionEnvelope"}'
```

## Add challenge

```bash
curl -X POST http://localhost:8000/challenges \
  -H 'Content-Type: application/json' \
  -d '{"record_id":"RECORD_UUID","actor_id":"c","challenge":"Test the envelope before expanding scope"}'
```

## Add adjudication

```bash
curl -X POST http://localhost:8000/adjudications \
  -H 'Content-Type: application/json' \
  -d '{"record_id":"RECORD_UUID","actor_id":"g","adjudication":"Promote v0.2 as Postgres-backed spine"}'
```

## Read record

```bash
curl http://localhost:8000/records/RECORD_UUID
```

## v0.2 limits

No auth. No UI. No policy engine. No migration framework.

Records are stored in Postgres table `decision_envelopes`.
