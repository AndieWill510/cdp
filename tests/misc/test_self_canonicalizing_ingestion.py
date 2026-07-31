"""Unit tests for CDP self-canonicalizing spreadsheet ingestion.

These tests intentionally keep the ingestion code small and dependency-free.
They prove the contract, not a production loader:

- human headers are not authoritative;
- canonical headers are derived by profile and ordinal position;
- CSV and Excel-style workbooks ingest the same rows;
- identifiers must be registered and correctly typed;
- packed strings are rejected before insert;
- parent-child edges and class rollups are derived from atomic IDs.
"""

from __future__ import annotations

import csv
import re
import tempfile
import unittest
import zipfile
from copy import deepcopy
from html import escape
from pathlib import Path
from typing import Callable
from xml.etree import ElementTree as ET

FIXTURE_DIR = Path(__file__).parent / "fixtures"

IDENTIFIER_COLUMNS = [
    "registry_name",
    "identifier_id",
    "identifier_type_registry_name",
    "identifier_type_id",
    "parent_registry_name",
    "parent_identifier_id",
    "display_label",
    "description",
    "status",
    "created",
]

CLASS_COLUMNS = [
    "registry_name",
    "class_id",
    "parent_class_id",
    "class_label",
    "class_level",
    "created",
]

DECISION_COLUMNS = [
    "registry_name",
    "decision_id",
    "decision_class_id",
    "parent_decision_id",
    "parent_relation_type",
    "antecedent_text",
    "subject_actor_type",
    "subject_actor_id",
    "predicate_verb",
    "object_type",
    "object_id",
    "permission_source_type",
    "permission_source_id",
    "human_required",
    "human_approver_id",
    "created",
]

STATUSES = {"active", "deprecated", "inactive", "retired"}
RELATION_TYPES = {
    "none",
    "child_of",
    "depends_on",
    "derived_from",
    "escalates_from",
    "approves",
    "denies",
    "appeal_of",
    "repair_of",
    "supersedes",
}
BOOLS = {"yes", "no", "true", "false"}
SIMPLE_ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")
DATEISH_RE = re.compile(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z)?$")

# Fields that must never contain packed colon-delimited values.
ATOMIC_DECISION_FIELDS = {
    "registry_name",
    "decision_id",
    "decision_class_id",
    "parent_decision_id",
    "parent_relation_type",
    "subject_actor_type",
    "subject_actor_id",
    "predicate_verb",
    "object_type",
    "object_id",
    "permission_source_type",
    "permission_source_id",
    "human_approver_id",
}


def simple_id(value: str | None) -> bool:
    return bool(value and SIMPLE_ID_RE.match(value))


def dateish(value: str | None) -> bool:
    return bool(value and DATEISH_RE.match(value))


def read_csv_rows(path: Path) -> list[list[str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [[cell.strip() for cell in row] for row in csv.reader(handle)]


def normalize_blank(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped if stripped else None


def looks_like_identifier_data_row(row: list[str]) -> bool:
    return (
        len(row) == len(IDENTIFIER_COLUMNS)
        and simple_id(row[0])
        and simple_id(row[1])
        and row[8].strip().lower() in STATUSES
        and dateish(row[9])
    )


def looks_like_class_data_row(row: list[str]) -> bool:
    return (
        len(row) == len(CLASS_COLUMNS)
        and simple_id(row[0])
        and simple_id(row[1])
        and row[4].strip().isdigit()
        and dateish(row[5])
    )


def looks_like_decision_data_row(row: list[str]) -> bool:
    return (
        len(row) == len(DECISION_COLUMNS)
        and simple_id(row[0])
        and simple_id(row[1])
        and simple_id(row[2])
        and row[4].strip().lower() in RELATION_TYPES
        and row[13].strip().lower() in BOOLS
        and dateish(row[15])
    )


def canonicalize_rows(
    raw_rows: list[list[str]],
    columns: list[str],
    looks_like_data_row: Callable[[list[str]], bool],
) -> list[dict[str, object]]:
    """Assign canonical columns by ordinal position.

    The first non-empty row is treated as data only when it matches the role's
    expected data shape. Otherwise it is treated as a human header row and
    discarded for canonical ingestion.
    """

    rows = [row for row in raw_rows if any(cell.strip() for cell in row)]
    if not rows:
        return []

    data_rows = rows if looks_like_data_row(rows[0]) else rows[1:]
    canonical: list[dict[str, object]] = []
    for source_index, row in enumerate(data_rows, start=1):
        if len(row) != len(columns):
            raise ValueError(
                f"row {source_index} has {len(row)} columns; expected {len(columns)}"
            )
        mapped = dict(zip(columns, [cell.strip() for cell in row]))
        for optional in (
            "identifier_type_registry_name",
            "identifier_type_id",
            "parent_registry_name",
            "parent_identifier_id",
            "parent_class_id",
            "parent_decision_id",
            "description",
        ):
            if optional in mapped:
                mapped[optional] = normalize_blank(mapped[optional])
        canonical.append(mapped)
    return canonical


def canonicalize_identifier_rows(raw_rows: list[list[str]]) -> list[dict[str, object]]:
    return canonicalize_rows(raw_rows, IDENTIFIER_COLUMNS, looks_like_identifier_data_row)


def canonicalize_class_rows(raw_rows: list[list[str]]) -> list[dict[str, object]]:
    rows = canonicalize_rows(raw_rows, CLASS_COLUMNS, looks_like_class_data_row)
    for row in rows:
        row["class_level"] = int(str(row["class_level"]))
    return rows


def normalize_bool(value: object) -> bool:
    normalized = str(value).strip().lower()
    if normalized in {"yes", "true"}:
        return True
    if normalized in {"no", "false"}:
        return False
    raise ValueError(f"invalid Boolean: {value}")


def canonicalize_decision_rows(raw_rows: list[list[str]]) -> list[dict[str, object]]:
    rows = canonicalize_rows(raw_rows, DECISION_COLUMNS, looks_like_decision_data_row)
    for row in rows:
        row["human_required"] = normalize_bool(row["human_required"])
        row["source_system"] = "spreadsheet"
    return rows


def assert_no_packed_decision_fields(decisions: list[dict[str, object]]) -> None:
    for row in decisions:
        for field in ATOMIC_DECISION_FIELDS:
            value = row.get(field)
            if value and ":" in str(value):
                raise ValueError(f"packed value is not allowed in {field}: {value}")


def build_identifier_index(
    identifiers: list[dict[str, object]],
) -> dict[tuple[str, str], dict[str, object]]:
    return {
        (str(row["registry_name"]), str(row["identifier_id"])): row
        for row in identifiers
        if str(row["status"]) in {"active", "deprecated"}
    }


def assert_registered(
    index: dict[tuple[str, str], dict[str, object]],
    registry_name: str,
    identifier_id: str,
    context: str,
) -> None:
    if (registry_name, identifier_id) not in index:
        raise ValueError(f"unregistered identifier for {context}: {registry_name}.{identifier_id}")


def assert_registered_of_type(
    index: dict[tuple[str, str], dict[str, object]],
    registry_name: str,
    identifier_id: str,
    type_registry_name: str,
    type_id: str,
    context: str,
) -> None:
    row = index.get((registry_name, identifier_id))
    if not row:
        raise ValueError(f"unregistered identifier for {context}: {registry_name}.{identifier_id}")
    if (
        row.get("identifier_type_registry_name") != type_registry_name
        or row.get("identifier_type_id") != type_id
    ):
        raise ValueError(
            f"mistyped identifier for {context}: {registry_name}.{identifier_id} "
            f"is not typed as {type_registry_name}.{type_id}"
        )


def validate_decisions(
    identifiers: list[dict[str, object]],
    classes: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> None:
    assert_no_packed_decision_fields(decisions)

    identifier_index = build_identifier_index(identifiers)
    class_index = {
        (str(row["registry_name"]), str(row["class_id"])) for row in classes
    }
    decision_index = {
        (str(row["registry_name"]), str(row["decision_id"])) for row in decisions
    }

    for row in decisions:
        registry_name = str(row["registry_name"])
        decision_class_id = str(row["decision_class_id"])
        parent_relation_type = str(row["parent_relation_type"])
        parent_decision_id = row.get("parent_decision_id")

        if (registry_name, decision_class_id) not in class_index:
            raise ValueError(f"unknown decision class: {registry_name}.{decision_class_id}")

        if parent_relation_type == "none" and parent_decision_id is not None:
            raise ValueError("parent_decision_id must be blank when relation is none")
        if parent_relation_type != "none" and parent_decision_id is None:
            raise ValueError("parent_decision_id is required when relation is not none")
        if parent_decision_id and (registry_name, str(parent_decision_id)) not in decision_index:
            raise ValueError(f"unknown parent decision: {registry_name}.{parent_decision_id}")

        assert_registered(identifier_index, "parent_relation_type", parent_relation_type, "parent_relation_type")
        assert_registered(identifier_index, "actor_type", str(row["subject_actor_type"]), "subject_actor_type")
        assert_registered_of_type(
            identifier_index,
            "actor",
            str(row["subject_actor_id"]),
            "actor_type",
            str(row["subject_actor_type"]),
            "subject_actor_id",
        )
        assert_registered(identifier_index, "predicate_verb", str(row["predicate_verb"]), "predicate_verb")
        assert_registered(identifier_index, "object_type", str(row["object_type"]), "object_type")
        assert_registered_of_type(
            identifier_index,
            "object",
            str(row["object_id"]),
            "object_type",
            str(row["object_type"]),
            "object_id",
        )
        assert_registered(
            identifier_index,
            "permission_source_type",
            str(row["permission_source_type"]),
            "permission_source_type",
        )
        assert_registered_of_type(
            identifier_index,
            "permission_source",
            str(row["permission_source_id"]),
            "permission_source_type",
            str(row["permission_source_type"]),
            "permission_source_id",
        )

        human_approver_id = str(row["human_approver_id"])
        if human_approver_id == "none":
            pass
        elif human_approver_id == "unknown":
            assert_registered_of_type(
                identifier_index,
                "actor",
                human_approver_id,
                "actor_type",
                "unknown",
                "human_approver_id",
            )
        else:
            assert_registered_of_type(
                identifier_index,
                "actor",
                human_approver_id,
                "actor_type",
                "human",
                "human_approver_id",
            )

        assert_registered(identifier_index, "source_system", str(row["source_system"]), "source_system")


def decision_class_rollup(decisions: list[dict[str, object]]) -> dict[str, dict[str, int]]:
    rollup: dict[str, dict[str, int]] = {}
    for row in decisions:
        class_id = str(row["decision_class_id"])
        bucket = rollup.setdefault(
            class_id,
            {"decision_count": 0, "human_required_count": 0, "unknown_permission_count": 0},
        )
        bucket["decision_count"] += 1
        if row["human_required"] is True:
            bucket["human_required_count"] += 1
        if row["permission_source_type"] == "unknown":
            bucket["unknown_permission_count"] += 1
    return rollup


def decision_parent_child_edges(decisions: list[dict[str, object]]) -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []
    for row in decisions:
        if row.get("parent_decision_id"):
            edges.append(
                {
                    "parent_decision_id": str(row["parent_decision_id"]),
                    "child_decision_id": str(row["decision_id"]),
                    "parent_relation_type": str(row["parent_relation_type"]),
                }
            )
    return edges


def flat_decision_projection(row: dict[str, object]) -> dict[str, object]:
    registry_name = str(row["registry_name"])
    decision_id = str(row["decision_id"])
    class_id = str(row["decision_class_id"])
    return {
        **row,
        "decision_domain": f"decision_register:{registry_name}:{decision_id}",
        "decision_class_domain": f"decision_class:{registry_name}:{class_id}",
        "plain_english_decision": (
            f"Because {row['antecedent_text']}, {row['subject_actor_type']} "
            f"{row['subject_actor_id']} performed {row['predicate_verb']} "
            f"on {row['object_type']} {row['object_id']}."
        ),
    }


def load_fixture_set() -> tuple[
    list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]
]:
    identifiers = canonicalize_identifier_rows(
        read_csv_rows(FIXTURE_DIR / "identifier_registry_bad_headers.csv")
    )
    classes = canonicalize_class_rows(
        read_csv_rows(FIXTURE_DIR / "decision_classes_bad_headers.csv")
    )
    decisions = canonicalize_decision_rows(
        read_csv_rows(FIXTURE_DIR / "decisions_bad_headers.csv")
    )
    validate_decisions(identifiers, classes, decisions)
    return identifiers, classes, decisions


def column_letter(index: int) -> str:
    letters = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters


def make_sheet_xml(rows: list[list[str]]) -> str:
    sheet_rows: list[str] = []
    for row_index, row in enumerate(rows, start=1):
        cells: list[str] = []
        for col_index, value in enumerate(row, start=1):
            ref = f"{column_letter(col_index)}{row_index}"
            cells.append(
                f'<c r="{ref}" t="inlineStr"><is><t>{escape(value)}</t></is></c>'
            )
        sheet_rows.append(f'<row r="{row_index}">{"".join(cells)}</row>')
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<sheetData>{"".join(sheet_rows)}</sheetData></worksheet>'
    )


def write_minimal_xlsx(path: Path, sheets: list[tuple[str, list[list[str]]]]) -> None:
    workbook_sheets = []
    workbook_rels = []
    content_overrides = [
        '<Override PartName="/xl/workbook.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
    ]
    for idx, (name, _rows) in enumerate(sheets, start=1):
        workbook_sheets.append(
            f'<sheet name="{escape(name)}" sheetId="{idx}" r:id="rId{idx}"/>'
        )
        workbook_rels.append(
            f'<Relationship Id="rId{idx}" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
            f'Target="worksheets/sheet{idx}.xml"/>'
        )
        content_overrides.append(
            f'<Override PartName="/xl/worksheets/sheet{idx}.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        )

    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            "[Content_Types].xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            f'{"".join(content_overrides)}</Types>',
        )
        archive.writestr(
            "_rels/.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
            'Target="xl/workbook.xml"/></Relationships>',
        )
        archive.writestr(
            "xl/workbook.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            f'<sheets>{"".join(workbook_sheets)}</sheets></workbook>',
        )
        archive.writestr(
            "xl/_rels/workbook.xml.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            f'{"".join(workbook_rels)}</Relationships>',
        )
        for idx, (_name, rows) in enumerate(sheets, start=1):
            archive.writestr(f"xl/worksheets/sheet{idx}.xml", make_sheet_xml(rows))


def cell_column_index(cell_ref: str) -> int:
    letters = "".join(ch for ch in cell_ref if ch.isalpha())
    index = 0
    for char in letters:
        index = index * 26 + (ord(char.upper()) - 64)
    return index - 1


def read_minimal_xlsx(path: Path) -> list[list[list[str]]]:
    worksheets: list[list[list[str]]] = []
    with zipfile.ZipFile(path) as archive:
        sheet_paths = sorted(
            name
            for name in archive.namelist()
            if name.startswith("xl/worksheets/sheet") and name.endswith(".xml")
        )
        for sheet_path in sheet_paths:
            root = ET.fromstring(archive.read(sheet_path))
            rows: list[list[str]] = []
            for row_el in root.findall(".//{*}row"):
                row_values: list[str] = []
                for cell_el in row_el.findall("{*}c"):
                    cell_ref = cell_el.attrib.get("r", "A1")
                    col_idx = cell_column_index(cell_ref)
                    while len(row_values) <= col_idx:
                        row_values.append("")
                    text_el = cell_el.find(".//{*}t")
                    row_values[col_idx] = text_el.text if text_el is not None and text_el.text else ""
                rows.append(row_values)
            worksheets.append(rows)
    return worksheets


class TestSelfCanonicalizingIngestion(unittest.TestCase):
    def test_csv_bad_headers_are_ignored_and_canonical_headers_are_derived(self) -> None:
        identifiers, classes, decisions = load_fixture_set()

        self.assertEqual(list(identifiers[0].keys()), IDENTIFIER_COLUMNS)
        self.assertEqual(list(classes[0].keys()), CLASS_COLUMNS)
        self.assertTrue(set(DECISION_COLUMNS).issubset(decisions[0].keys()))
        self.assertEqual(len(decisions), 4)

        projected = flat_decision_projection(decisions[0])
        self.assertEqual(
            projected["decision_domain"],
            "decision_register:sample_attorney_demo:dec_001",
        )
        self.assertEqual(
            projected["decision_class_domain"],
            "decision_class:sample_attorney_demo:claim_intake",
        )

        rollup = decision_class_rollup(decisions)
        self.assertEqual(rollup["claim_approval"]["decision_count"], 1)
        self.assertEqual(rollup["claim_approval"]["human_required_count"], 1)

        edges = decision_parent_child_edges(decisions)
        self.assertEqual(
            edges,
            [
                {
                    "parent_decision_id": "dec_001",
                    "child_decision_id": "dec_003",
                    "parent_relation_type": "escalates_from",
                },
                {
                    "parent_decision_id": "dec_003",
                    "child_decision_id": "dec_004",
                    "parent_relation_type": "approves",
                },
            ],
        )

    def test_excel_workbook_bad_headers_ingests_by_sheet_role_and_position(self) -> None:
        identifier_rows = read_csv_rows(FIXTURE_DIR / "identifier_registry_bad_headers.csv")
        class_rows = read_csv_rows(FIXTURE_DIR / "decision_classes_bad_headers.csv")
        decision_rows = read_csv_rows(FIXTURE_DIR / "decisions_bad_headers.csv")

        with tempfile.TemporaryDirectory() as tmpdir:
            workbook_path = Path(tmpdir) / "messy_attorney_workbook.xlsx"
            write_minimal_xlsx(
                workbook_path,
                [
                    ("Stuff from counsel", identifier_rows),
                    ("Classes maybe", class_rows),
                    ("Final final v7", decision_rows),
                ],
            )
            sheets = read_minimal_xlsx(workbook_path)

        identifiers = canonicalize_identifier_rows(sheets[0])
        classes = canonicalize_class_rows(sheets[1])
        decisions = canonicalize_decision_rows(sheets[2])
        validate_decisions(identifiers, classes, decisions)

        self.assertEqual(len(identifiers), 36)
        self.assertEqual(len(classes), 6)
        self.assertEqual(len(decisions), 4)
        self.assertEqual(decisions[3]["subject_actor_type"], "human")
        self.assertEqual(decisions[3]["subject_actor_id"], "user_442")

    def test_headerless_body_first_decision_sheet_is_accepted(self) -> None:
        rows = read_csv_rows(FIXTURE_DIR / "decisions_bad_headers.csv")[1:]
        decisions = canonicalize_decision_rows(rows)

        self.assertEqual(len(decisions), 4)
        self.assertEqual(decisions[0]["decision_id"], "dec_001")
        self.assertIsNone(decisions[0]["parent_decision_id"])

    def test_missing_identifier_is_rejected(self) -> None:
        identifiers, classes, decisions = load_fixture_set()
        broken = deepcopy(decisions)
        broken[0]["subject_actor_id"] = "unregistered_agent"

        with self.assertRaisesRegex(ValueError, "unregistered identifier.*subject_actor_id"):
            validate_decisions(identifiers, classes, broken)

    def test_mistyped_identifier_is_rejected(self) -> None:
        identifiers, classes, decisions = load_fixture_set()
        broken = deepcopy(decisions)
        broken[3]["subject_actor_type"] = "agent"
        broken[3]["subject_actor_id"] = "user_442"

        with self.assertRaisesRegex(ValueError, "mistyped identifier.*subject_actor_id"):
            validate_decisions(identifiers, classes, broken)

    def test_packed_fields_are_rejected_before_insert(self) -> None:
        identifiers, classes, decisions = load_fixture_set()
        broken = deepcopy(decisions)
        broken[0]["predicate_verb"] = "recommend_approval:claim:claim_9981"

        with self.assertRaisesRegex(ValueError, "packed value.*predicate_verb"):
            validate_decisions(identifiers, classes, broken)


if __name__ == "__main__":
    unittest.main()
