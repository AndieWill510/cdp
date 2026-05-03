# RFC-CDP-016 — Governance API

Author: Kevin “Andie” Williams  
Status: Draft v0.3  
Series: Constitutional Decision Plane (CDP)  
Date: March 17, 2026

## Abstract
Defines external interfaces for submitting acts, reading decisions, retrieving records, appealing, and subscribing to governance events.

## 1. Purpose
The Governance API answers:
- what external interfaces exist;
- what endpoints are exposed;
- how clients submit acts;
- how reads, writes, appeals, and subscriptions work.

## 2. Recommended Endpoints
- `POST /decisions/propose`
- `POST /decisions/{decision_id}/challenge`
- `POST /decisions/{decision_id}/test`
- `POST /decisions/{decision_id}/adjudicate`
- `POST /decisions/{decision_id}/legitimize`
- `POST /decisions/{decision_id}/execute`
- `POST /decisions/{decision_id}/record`
- `POST /decisions/{decision_id}/learn`
- `GET /decisions/{decision_id}`
- `GET /records/{decision_id}`
- `GET /events?decision_id=...`
- `POST /decisions/{decision_id}/appeal`

## 3. Response Semantics
Implementations SHOULD distinguish:
- validation failure (`400`);
- authentication failure (`401`);
- authority failure (`403`);
- state conflict (`409`);
- policy block (`422`);
- success (`200`, `201`, `202`).

## 4. Local-First Guidance
Implementations SHOULD be runnable with SQLite or Postgres and file-based artifacts to minimize infrastructure cost.

## 5. Principle
The API is not the governance model. It is the transport surface for it.
