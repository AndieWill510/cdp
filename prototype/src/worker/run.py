import json
import logging
import time
from sqlalchemy import create_engine, text
from src.app.config import settings

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger("cdp-worker")

engine = create_engine(settings.sync_database_url, future=True, pool_pre_ping=True)

def adjudicate_pending():
    with engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT p.id, p.title, p.payload
            FROM cdp_proposal p
            WHERE p.status='proposed'
              AND NOT EXISTS (
                SELECT 1 FROM cdp_adjudication a WHERE a.proposal_id = p.id
              )
            ORDER BY p.id
            LIMIT 10
        """)).mappings().all()

        for row in rows:
            payload = row["payload"] if isinstance(row["payload"], dict) else row["payload"]
            rationale = "Auto-approved because no challenge was present within current prototype workflow."
            conn.execute(
                text("""
                    INSERT INTO cdp_adjudication (proposal_id, adjudicator, decision, rationale, conditions)
                    VALUES (:proposal_id, 'auto-judge', 'approve', :rationale, '{}'::jsonb)
                """),
                {"proposal_id": row["id"], "rationale": rationale},
            )
            conn.execute(text("UPDATE cdp_proposal SET status='adjudicated' WHERE id=:id"), {"id": row["id"]})
            conn.execute(
                text("""
                    INSERT INTO cdp_event (proposal_id, event_type, actor, body)
                    VALUES (:proposal_id, 'adjudication_created', 'auto-judge', CAST(:body AS jsonb))
                """),
                {"proposal_id": row["id"], "body": json.dumps({"decision": "approve", "rationale": rationale})},
            )
            logger.info("Auto-adjudicated proposal_id=%s", row["id"])

if __name__ == "__main__":
    logger.info("Worker started")
    while True:
        try:
            adjudicate_pending()
        except Exception:
            logger.exception("Worker loop failed")
        time.sleep(settings.worker_poll_seconds)
