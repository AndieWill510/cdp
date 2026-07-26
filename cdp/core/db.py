"""Database access for the live CDP core.

Provides a single connection/transaction boundary per service call. Repository
functions never open their own connections; they accept the cursor yielded
here so multiple repository calls in one service function share one
transaction and commit or roll back together.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from contextlib import contextmanager

import psycopg
from psycopg.rows import DictRow, dict_row

# The canonical docker-compose stack sets DATABASE_URL using the SQLAlchemy
# dialect scheme (postgresql+psycopg://). psycopg3's connect() only
# understands the plain postgresql:// / postgres:// schemes, so that prefix
# is normalized away here rather than in every caller.
_SQLALCHEMY_DRIVER_PREFIXES = (
    "postgresql+psycopg2://",
    "postgresql+psycopg://",
)


def _normalize_database_url(raw_url: str) -> str:
    for prefix in _SQLALCHEMY_DRIVER_PREFIXES:
        if raw_url.startswith(prefix):
            return "postgresql://" + raw_url[len(prefix) :]
    return raw_url


def get_database_url() -> str:
    """Read and normalize DATABASE_URL. Raises if it is not set."""
    raw_url = os.environ.get("DATABASE_URL")
    if not raw_url:
        raise RuntimeError("DATABASE_URL is not set")
    return _normalize_database_url(raw_url)


@contextmanager
def transaction(*, database_url: str | None = None) -> Iterator[psycopg.Cursor[DictRow]]:
    """Yield a cursor for one service-level transaction.

    Opens exactly one connection, commits once on clean exit, rolls back and
    re-raises on any exception, and always closes the connection.
    """
    conn = psycopg.connect(database_url or get_database_url(), row_factory=dict_row)
    try:
        with conn.cursor() as cursor:
            yield cursor
        conn.commit()
    except BaseException:
        conn.rollback()
        raise
    finally:
        conn.close()
