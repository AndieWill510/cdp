# CDP Engineering Instructions

## Project

CDP is the Constitutional Decision Plane.

The core decision lifecycle is:

Propose → Challenge → Test → Adjudicate → Legitimize → Execute → Record → Improve

Preserve auditability, contestability, explicit state transitions, and human
oversight. Do not bypass governance controls merely to make tests pass.

## Repository Safety

- Work only within this repository.
- Never commit directly to `main`.
- Never force-push.
- Do not delete Docker volumes unless explicitly instructed.
- Do not run destructive database commands unless explicitly instructed.
- Do not modify secrets or commit `.env` files.
- Before changing architecture, identify the relevant RFCs and explain any
  conflict or schema drift.
- Prefer small, reviewable patches over broad rewrites.

## Docker

Docker Compose file:

```bash
docker compose -f docker/docker-compose.yml
