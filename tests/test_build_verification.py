"""Build verification tests for the local CDP Docker stack.

These tests assume the local stack is already running:

    make up-build
    pytest tests/test_build_verification.py

They validate the concrete services defined in docker/docker-compose.yml:

- FastAPI health endpoint
- Postgres + pgvector initialization
- Redis readiness
- Qdrant readiness
- LocalStack S3/SQS/EventBridge/DynamoDB/SSM/Secrets Manager bootstrap

The tests intentionally verify infrastructure shape, not business behavior.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

import boto3
import psycopg
import pytest
import redis
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError


@dataclass(frozen=True)
class LocalStackConfig:
    """Connection settings for local build verification."""

    api_url: str = os.getenv("CDP_TEST_API_URL", "http://localhost:8000")
    qdrant_url: str = os.getenv("CDP_TEST_QDRANT_URL", "http://localhost:6333")
    localstack_url: str = os.getenv("CDP_TEST_LOCALSTACK_URL", "http://localhost:4566")
    database_url: str = os.getenv(
        "CDP_TEST_DATABASE_URL",
        "postgresql://cdp:cdp@localhost:5432/cdp",
    )
    redis_url: str = os.getenv("CDP_TEST_REDIS_URL", "redis://localhost:6379/0")
    aws_region: str = os.getenv("AWS_DEFAULT_REGION", "us-east-1")


CONFIG = LocalStackConfig()


EXPECTED_BUCKETS = {
    "cdp-evidence-local",
    "cdp-artifacts-local",
    "cdp-exports-local",
}

EXPECTED_QUEUES = {
    "cdp-intake-queue",
    "cdp-review-queue",
    "cdp-execution-queue",
    "cdp-appeal-queue",
    "cdp-repair-queue",
    "cdp-dead-letter-queue",
}

EXPECTED_SSM_PARAMETERS = {
    "/cdp/local/database-url",
    "/cdp/local/qdrant-url",
    "/cdp/local/redis-url",
    "/cdp/local/default-policy-profile",
    "/cdp/local/event-bus-name",
}

EXPECTED_SECRETS = {
    "/cdp/local/signing-key",
    "/cdp/local/database-password",
}


def fetch_json(url: str) -> dict[str, Any]:
    """Fetch a JSON URL with helpful failure output."""
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            payload = response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        pytest.fail(f"Could not reach {url}. Is the local Docker stack running? {exc}")

    try:
        return json.loads(payload)
    except json.JSONDecodeError as exc:
        pytest.fail(f"Expected JSON response from {url}, got: {payload!r}. Error: {exc}")


def boto_client(service_name: str):
    """Create a boto3 client pointed at LocalStack."""
    return boto3.client(
        service_name,
        endpoint_url=CONFIG.localstack_url,
        region_name=CONFIG.aws_region,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
        config=Config(retries={"max_attempts": 3, "mode": "standard"}),
    )


def test_api_health_endpoint() -> None:
    """The FastAPI container should expose /health."""
    payload = fetch_json(f"{CONFIG.api_url}/health")

    assert payload["status"] == "ok"
    assert payload["service"] == "cdp-api"
    assert payload["version"]


def test_postgres_extensions_and_schemas() -> None:
    """Postgres should have CDP schemas and required extensions."""
    try:
        with psycopg.connect(CONFIG.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT extname
                    FROM pg_extension
                    WHERE extname IN ('vector', 'pgcrypto')
                    ORDER BY extname
                    """
                )
                extensions = {row[0] for row in cur.fetchall()}

                cur.execute(
                    """
                    SELECT schema_name
                    FROM information_schema.schemata
                    WHERE schema_name LIKE 'cdp_%'
                    ORDER BY schema_name
                    """
                )
                schemas = {row[0] for row in cur.fetchall()}

                cur.execute(
                    """
                    SELECT version
                    FROM cdp_core.schema_version
                    WHERE component = 'local-postgres-bootstrap'
                    """
                )
                version = cur.fetchone()

                cur.execute(
                    """
                    SELECT label
                    FROM cdp_projection.vector_smoke_test
                    WHERE label = 'bootstrap'
                    LIMIT 1
                    """
                )
                vector_smoke = cur.fetchone()
    except psycopg.OperationalError as exc:
        pytest.fail(f"Could not connect to Postgres. Is the stack running? {exc}")

    assert extensions == {"pgcrypto", "vector"}
    assert {"cdp_core", "cdp_audit", "cdp_repair", "cdp_projection"}.issubset(schemas)
    assert version is not None
    assert vector_smoke == ("bootstrap",)


def test_redis_ping() -> None:
    """Redis should accept PING."""
    client = redis.Redis.from_url(CONFIG.redis_url)

    try:
        assert client.ping() is True
    except redis.RedisError as exc:
        pytest.fail(f"Could not ping Redis. Is the stack running? {exc}")


def test_qdrant_ready() -> None:
    """Qdrant should expose its readiness endpoint."""
    try:
        with urllib.request.urlopen(f"{CONFIG.qdrant_url}/readyz", timeout=10) as response:
            body = response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        pytest.fail(f"Could not reach Qdrant. Is the stack running? {exc}")

    assert response.status == 200
    assert body.strip().lower() in {"all shards are ready", "ok", "true"}


def test_localstack_s3_buckets() -> None:
    """LocalStack should contain expected CDP S3 buckets."""
    s3 = boto_client("s3")

    try:
        response = s3.list_buckets()
    except (BotoCoreError, ClientError) as exc:
        pytest.fail(f"Could not list LocalStack S3 buckets. Is LocalStack running? {exc}")

    bucket_names = {bucket["Name"] for bucket in response.get("Buckets", [])}
    assert EXPECTED_BUCKETS.issubset(bucket_names)


def test_localstack_sqs_queues() -> None:
    """LocalStack should contain expected CDP SQS queues."""
    sqs = boto_client("sqs")

    try:
        response = sqs.list_queues()
    except (BotoCoreError, ClientError) as exc:
        pytest.fail(f"Could not list LocalStack SQS queues. Is LocalStack running? {exc}")

    queue_urls = response.get("QueueUrls", [])
    queue_names = {queue_url.rsplit("/", maxsplit=1)[-1] for queue_url in queue_urls}
    assert EXPECTED_QUEUES.issubset(queue_names)


def test_localstack_eventbridge_bus() -> None:
    """LocalStack should contain the CDP EventBridge bus."""
    events = boto_client("events")

    try:
        response = events.list_event_buses()
    except (BotoCoreError, ClientError) as exc:
        pytest.fail(f"Could not list LocalStack EventBridge buses. Is LocalStack running? {exc}")

    bus_names = {bus["Name"] for bus in response.get("EventBuses", [])}
    assert "cdp-events-local" in bus_names


def test_localstack_dynamodb_table() -> None:
    """LocalStack should contain the CDP idempotency table."""
    dynamodb = boto_client("dynamodb")

    try:
        response = dynamodb.list_tables()
    except (BotoCoreError, ClientError) as exc:
        pytest.fail(f"Could not list LocalStack DynamoDB tables. Is LocalStack running? {exc}")

    assert "cdp-idempotency-local" in set(response.get("TableNames", []))


def test_localstack_ssm_parameters() -> None:
    """LocalStack should contain expected SSM parameters."""
    ssm = boto_client("ssm")

    for parameter_name in EXPECTED_SSM_PARAMETERS:
        try:
            response = ssm.get_parameter(Name=parameter_name)
        except (BotoCoreError, ClientError) as exc:
            pytest.fail(f"Missing or unreadable SSM parameter {parameter_name}: {exc}")

        assert response["Parameter"]["Value"]


def test_localstack_secrets() -> None:
    """LocalStack should contain expected Secrets Manager secrets."""
    secretsmanager = boto_client("secretsmanager")

    for secret_name in EXPECTED_SECRETS:
        try:
            response = secretsmanager.get_secret_value(SecretId=secret_name)
        except (BotoCoreError, ClientError) as exc:
            pytest.fail(f"Missing or unreadable secret {secret_name}: {exc}")

        assert response["SecretString"]
