from __future__ import annotations

import os
import re
import unittest
from collections import Counter
from pathlib import Path
from typing import Any

try:
    import psycopg  # type: ignore
    from psycopg import sql  # type: ignore
except ImportError:
    try:
        import psycopg2 as psycopg  # type: ignore
        from psycopg import sql  # type: ignore
    except ImportError:
        psycopg = None  # type: ignore
        sql = None  # type: ignore

REPO_ROOT = Path(__file__).resolve().parents[1]
DDL_DIR = REPO_ROOT / "db" / "ddl"

DDL_OBJECT_PATTERNS = {
    "schemas": re.compile(r"create\s+schema\s+(?:if\s+not\s+exists\s+)?([a-zA-Z0-9_]+)", re.I),
    "tables": re.compile(
        r"create\s+table\s+(?:if\s+not\s+exists\s+)?([a-zA-Z0-9_]+\.[a-zA-Z0-9_]+)",
        re.I,
    ),
    "views": re.compile(
        r"create\s+(?:or\s+replace\s+)?view\s+([a-zA-Z0-9_]+\.[a-zA-Z0-9_]+)",
        re.I,
    ),
    "functions": re.compile(
        r"create\s+(?:or\s+replace\s+)?function\s+([a-zA-Z0-9_]+\.[a-zA-Z0-9_]+)\s*\(",
        re.I,
    ),
    "extensions": re.compile(
        r"create\s+extension\s+(?:if\s+not\s+exists\s+)?([a-zA-Z0-9_]+)",
        re.I,
    ),
}
INSERT_PATTERN = re.compile(r"insert\s+into\s+([a-zA-Z0-9_]+\.[a-zA-Z0-9_]+)", re.I)


def _database_url() -> str:
    return os.getenv("CDP_TEST_DATABASE_URL", "postgresql://cdp:cdp@localhost:5432/cdp")


def _read_ddl_files() -> list[Path]:
    return sorted(DDL_DIR.glob("*.sql"))


def _extract_ddl_assets(sql_text: str) -> tuple[set[str], set[str], set[str], set[str], set[str], Counter[str]]:
    schemas: set[str] = set()
    tables: set[str] = set()
    views: set[str] = set()
    functions: set[str] = set()
    extensions: set[str] = set()
    inserts: Counter[str] = Counter()

    content = sql_text.replace("\n", " ")
    for name, pattern in DDL_OBJECT_PATTERNS.items():
        for match in pattern.finditer(content):
            value = match.group(1).lower()
            if name == "schemas":
                schemas.add(value)
            elif name == "tables":
                tables.add(value)
            elif name == "views":
                views.add(value)
            elif name == "functions":
                functions.add(value)
            elif name == "extensions":
                extensions.add(value)

    for match in INSERT_PATTERN.finditer(content):
        inserts[match.group(1).lower()] += 1

    return schemas, tables, views, functions, extensions, inserts


def _fetch_ddl_catalog() -> tuple[set[str], set[str], set[str], set[str], set[str], Counter[str]]:
    schemas: set[str] = set()
    tables: set[str] = set()
    views: set[str] = set()
    functions: set[str] = set()
    extensions: set[str] = set()
    inserts: Counter[str] = Counter()

    for ddl_path in _read_ddl_files():
        sql_text = ddl_path.read_text(encoding="utf-8")
        ddl_schemas, ddl_tables, ddl_views, ddl_functions, ddl_extensions, ddl_inserts = _extract_ddl_assets(sql_text)
        schemas.update(ddl_schemas)
        tables.update(ddl_tables)
        views.update(ddl_views)
        functions.update(ddl_functions)
        extensions.update(ddl_extensions)
        inserts.update(ddl_inserts)

    return schemas, tables, views, functions, extensions, inserts


def _assert_relation_exists(cursor: psycopg.Cursor, relation: str) -> None:
    cursor.execute("SELECT to_regclass(%s)", (relation,))
    assert cursor.fetchone()[0] is not None, f"Missing relation {relation}"


def _assert_function_exists(cursor: psycopg.Cursor, function_name: str) -> None:
    schema_name, proc_name = function_name.split(".")
    cursor.execute(
        "SELECT proname FROM pg_proc JOIN pg_namespace ON pg_proc.pronamespace = pg_namespace.oid WHERE pg_namespace.nspname = %s AND pg_proc.proname = %s",
        (schema_name, proc_name),
    )
    assert cursor.fetchone() is not None, f"Missing function {function_name}"


def _assert_extension_exists(cursor: psycopg.Cursor, extension_name: str) -> None:
    cursor.execute("SELECT extname FROM pg_extension WHERE extname = %s", (extension_name,))
    assert cursor.fetchone() is not None, f"Missing extension {extension_name}"


def _assert_schema_exists(cursor: psycopg.Cursor, schema_name: str) -> None:
    cursor.execute(
        "SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s",
        (schema_name,),
    )
    assert cursor.fetchone() is not None, f"Missing schema {schema_name}"


def _assert_table_has_rows(cursor: psycopg.Cursor, relation: str) -> None:
    schema_name, table_name = relation.split(".")
    cursor.execute(
        sql.SQL("SELECT count(*) FROM {}.{} ").format(
            sql.Identifier(schema_name), sql.Identifier(table_name)
        )
    )
    count = cursor.fetchone()[0]
    assert count > 0, f"Expected rows in {relation}, found none"


@unittest.skipIf(psycopg is None, "psycopg or psycopg2 is required to run this test")
def test_db_ddl_objects_and_seeded_rows_exist() -> None:
    if psycopg is None:
        raise unittest.SkipTest("psycopg or psycopg2 is required to run this test")

    schemas, tables, views, functions, extensions, inserts = _fetch_ddl_catalog()

    try:
        with psycopg.connect(_database_url()) as conn:
            with conn.cursor() as cursor:
                for schema in sorted(schemas):
                    _assert_schema_exists(cursor, schema)

                for relation in sorted(tables | views):
                    _assert_relation_exists(cursor, relation)

                for function_name in sorted(functions):
                    _assert_function_exists(cursor, function_name)

                for extension_name in sorted(extensions):
                    _assert_extension_exists(cursor, extension_name)

                for relation, insert_count in inserts.items():
                    if relation in tables:
                        _assert_table_has_rows(cursor, relation)
    except AttributeError:
        raise unittest.SkipTest("psycopg or psycopg2 failed to import properly")
    except psycopg.OperationalError as exc:
        raise AssertionError(
            "Could not connect to Postgres. Is the running database available at CDP_TEST_DATABASE_URL?"
        ) from exc
