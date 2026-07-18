"""Regression tests for PostgreSQL initialization ownership and bootstrap state."""

from __future__ import annotations

import os
from pathlib import Path

import psycopg
import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
POSTGRES_INIT_DIR = REPO_ROOT / "docker" / "postgres" / "init"
BOOTSTRAP_SQL = POSTGRES_INIT_DIR / "01-init-cdp.sql"
REPOSITORY_HOOK = POSTGRES_INIT_DIR / "02_initialize_repository.sh"
LEGACY_HOOK = POSTGRES_INIT_DIR / "001_initialize.sh"
DUPLICATE_BOOTSTRAP_SQL = POSTGRES_INIT_DIR / "ddl" / "01-init-cdp.sql"


def _database_url() -> str:
    return os.getenv("CDP_TEST_DATABASE_URL", "postgresql://cdp:cdp@localhost:5432/cdp")


def test_postgres_init_files_have_single_ordered_owner() -> None:
    """Native bootstrap must run once before the repository DDL hook."""
    assert BOOTSTRAP_SQL.is_file()
    assert REPOSITORY_HOOK.is_file()
    assert not LEGACY_HOOK.exists()
    assert not DUPLICATE_BOOTSTRAP_SQL.exists()

    ordered_hooks = sorted(
        path.name
        for path in POSTGRES_INIT_DIR.iterdir()
        if path.is_file() and path.suffix in {".sql", ".sh"}
    )

    assert ordered_hooks.index(BOOTSTRAP_SQL.name) < ordered_hooks.index(REPOSITORY_HOOK.name)

    repository_hook = REPOSITORY_HOOK.read_text(encoding="utf-8")
    assert 'run_sql_directory "/docker-entrypoint-initdb.d"' not in repository_hook
    assert 'run_sql_directory "/cdp-init/db/ddl"' in repository_hook
    assert 'run_sql_directory "/cdp-init/db/seed"' in repository_hook


def test_bootstrap_sql_enforces_idempotent_smoke_marker() -> None:
    """The bootstrap marker must remain repairable and unique by label."""
    bootstrap_sql = BOOTSTRAP_SQL.read_text(encoding="utf-8")

    assert "ranked_smoke_rows" in bootstrap_sql
    assert "CREATE UNIQUE INDEX IF NOT EXISTS uq_vector_smoke_test_label" in bootstrap_sql
    assert "ON CONFLICT (label)" in bootstrap_sql


def test_postgres_bootstrap_runtime_marker_is_unique() -> None:
    """The running local database must contain one uniquely indexed bootstrap row."""
    try:
        with psycopg.connect(_database_url()) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT count(*)
                    FROM cdp_projection.vector_smoke_test
                    WHERE label = 'bootstrap'
                    """
                )
                bootstrap_count = cur.fetchone()[0]

                cur.execute(
                    """
                    SELECT indexdef
                    FROM pg_catalog.pg_indexes
                    WHERE schemaname = 'cdp_projection'
                      AND tablename = 'vector_smoke_test'
                      AND indexname = 'uq_vector_smoke_test_label'
                    """
                )
                unique_index = cur.fetchone()
    except psycopg.OperationalError as exc:
        pytest.fail(f"Could not connect to Postgres. Is the local stack running? {exc}")

    assert bootstrap_count == 1, (
        "Expected exactly one bootstrap smoke row; run "
        "`make repair-local-postgres-bootstrap` to repair an existing local volume."
    )
    assert unique_index is not None
    assert "UNIQUE INDEX" in unique_index[0]
