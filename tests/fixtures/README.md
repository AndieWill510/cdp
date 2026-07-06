# CDP Ingestion Fixtures

These fixtures intentionally use human-friendly, non-canonical headers.

The tests prove that ingestion derives canonical headers from the ingestion profile, sheet role, and column position rather than trusting the first row.

Fixtures:

- `identifier_registry_bad_headers.csv` — rows for `cdp_core.identifier_registry`
- `decision_classes_bad_headers.csv` — rows for `cdp_core.decision_class_registry`
- `decisions_bad_headers.csv` — rows for `cdp_core.decision_registry`

The Excel ingestion test builds a temporary `.xlsx` workbook from these same rows at test time. This avoids committing a binary workbook while still testing Excel-style ingestion.
