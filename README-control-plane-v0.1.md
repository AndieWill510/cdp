# CDP Control Plane v0.1

Tiny FastAPI prototype for the first executable CDP object: DecisionEnvelope.

## Run

```bash
docker compose up --build
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
  -d '{"record_id":"RECORD_UUID","actor_id":"g","adjudication":"Promote v0.1 as executable spine"}'
```

## Read record

```bash
curl http://localhost:8000/records/RECORD_UUID
```

## v0.1 limits

No auth. No database. No UI. No policy engine.

Records are stored as JSONL under `data/records.jsonl`.
