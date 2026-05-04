"""Minimal CDP worker process.

The worker currently provides a safe no-op loop so the local Docker stack can
start cleanly before queue consumers are implemented.

Future workers should consume LocalStack/AWS SQS queues for intake, review,
execution, appeal, and repair work.
"""

from __future__ import annotations

import logging
import os
import signal
import time
from dataclasses import dataclass

LOGGER = logging.getLogger("cdp.worker")


@dataclass(frozen=True)
class WorkerConfig:
    """Runtime configuration for the local worker."""

    environment: str
    aws_region: str
    aws_endpoint_url: str | None
    intake_queue_name: str
    review_queue_name: str
    execution_queue_name: str
    appeal_queue_name: str
    repair_queue_name: str
    dead_letter_queue_name: str
    poll_interval_seconds: float

    @classmethod
    def from_environment(cls) -> "WorkerConfig":
        """Build worker configuration from environment variables."""
        return cls(
            environment=os.getenv("CDP_ENV", "local"),
            aws_region=os.getenv("AWS_REGION", "us-east-1"),
            aws_endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
            intake_queue_name=os.getenv("CDP_INTAKE_QUEUE_NAME", "cdp-intake-queue"),
            review_queue_name=os.getenv("CDP_REVIEW_QUEUE_NAME", "cdp-review-queue"),
            execution_queue_name=os.getenv("CDP_EXECUTION_QUEUE_NAME", "cdp-execution-queue"),
            appeal_queue_name=os.getenv("CDP_APPEAL_QUEUE_NAME", "cdp-appeal-queue"),
            repair_queue_name=os.getenv("CDP_REPAIR_QUEUE_NAME", "cdp-repair-queue"),
            dead_letter_queue_name=os.getenv("CDP_DEAD_LETTER_QUEUE_NAME", "cdp-dead-letter-queue"),
            poll_interval_seconds=float(os.getenv("CDP_WORKER_POLL_INTERVAL_SECONDS", "5")),
        )


class ShutdownFlag:
    """Signal-safe shutdown flag."""

    def __init__(self) -> None:
        self.should_stop = False

    def request_stop(self, signum: int, _frame: object | None) -> None:
        """Request worker shutdown."""
        LOGGER.info("Received signal %s; shutting down worker", signum)
        self.should_stop = True


def configure_logging() -> None:
    """Configure process logging."""
    logging.basicConfig(
        level=os.getenv("CDP_LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


def run_noop_worker(config: WorkerConfig, shutdown: ShutdownFlag) -> None:
    """Run a safe no-op loop until real queue polling is implemented."""
    LOGGER.info("Starting CDP worker in %s environment", config.environment)
    LOGGER.info(
        "Configured queues: intake=%s review=%s execution=%s appeal=%s repair=%s dlq=%s",
        config.intake_queue_name,
        config.review_queue_name,
        config.execution_queue_name,
        config.appeal_queue_name,
        config.repair_queue_name,
        config.dead_letter_queue_name,
    )
    LOGGER.info("AWS region=%s endpoint=%s", config.aws_region, config.aws_endpoint_url)
    LOGGER.info("Worker is currently running in no-op mode")

    while not shutdown.should_stop:
        time.sleep(config.poll_interval_seconds)

    LOGGER.info("CDP worker stopped")


def main() -> None:
    """Worker entrypoint."""
    configure_logging()
    config = WorkerConfig.from_environment()
    shutdown = ShutdownFlag()

    signal.signal(signal.SIGTERM, shutdown.request_stop)
    signal.signal(signal.SIGINT, shutdown.request_stop)

    run_noop_worker(config, shutdown)


if __name__ == "__main__":
    main()
