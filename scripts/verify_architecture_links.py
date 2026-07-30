#!/usr/bin/env python3
"""Verify discoverability pointers for the architecture/ layer stay valid.

Architecture documents carry no independent constitutional authority (see
architecture/README.md), but an excellent document nobody finds is still a
governance failure. This script checks that the minimum discovery path
required by architecture/README.md's own reader path stays intact:

- every architecture document referenced from architecture/README.md exists;
- every architecture document that exists is listed in architecture/README.md;
- the root README.md links to the canonical starting-point document;
- rfc/RFC-CDP-000-Series-Index.md links to the architecture layer.

This does not duplicate scripts/verify_rfc_index.py, which governs the rfc/
lane only. This script governs the architecture/ lane's discoverability
contract, nothing else.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCH_DIR = ROOT / "architecture"
ARCH_INDEX = ARCH_DIR / "README.md"
ROOT_README = ROOT / "README.md"
SERIES_INDEX = ROOT / "rfc" / "RFC-CDP-000-Series-Index.md"

CANONICAL_START = "architecture/001-canonical-governance-workflow.md"

MD_LINK_RE = re.compile(r"\]\(([^)]+)\)")


def find_markdown_links(text: str) -> set[str]:
    return {match.strip() for match in MD_LINK_RE.findall(text)}


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if not ARCH_DIR.exists():
        print("ERROR: architecture/ directory does not exist")
        return 1

    if not ARCH_INDEX.exists():
        errors.append("architecture/README.md is missing")
        arch_index_text = ""
    else:
        arch_index_text = ARCH_INDEX.read_text(encoding="utf-8")

    arch_docs = sorted(
        p.name
        for p in ARCH_DIR.glob("*.md")
        if p.name != "README.md"
    )

    if not arch_docs:
        errors.append("architecture/ contains no documents besides README.md")

    linked_in_index = find_markdown_links(arch_index_text)
    linked_basenames = {Path(link).name for link in linked_in_index}

    for doc in arch_docs:
        if doc not in linked_basenames:
            errors.append(
                f"architecture/{doc} exists but is not linked from architecture/README.md"
            )

    for link in linked_in_index:
        if link.startswith(("http://", "https://", "#")):
            continue
        target = (ARCH_DIR / link).resolve()
        if not target.exists():
            errors.append(
                f"architecture/README.md links to {link!r}, which does not exist"
            )

    if not ROOT_README.exists():
        errors.append("README.md is missing")
    else:
        readme_text = ROOT_README.read_text(encoding="utf-8")
        if CANONICAL_START not in readme_text:
            errors.append(
                f"README.md does not link to {CANONICAL_START} "
                "(the canonical implementation starting point)"
            )
        if "architecture/README.md" not in readme_text:
            warnings.append(
                "README.md does not link to architecture/README.md (the architecture index)"
            )

    if not SERIES_INDEX.exists():
        errors.append("rfc/RFC-CDP-000-Series-Index.md is missing")
    else:
        series_text = SERIES_INDEX.read_text(encoding="utf-8")
        if "architecture/" not in series_text:
            errors.append(
                "rfc/RFC-CDP-000-Series-Index.md does not reference the architecture/ layer"
            )
        if "non-normative" not in series_text.lower():
            warnings.append(
                "rfc/RFC-CDP-000-Series-Index.md references architecture/ but does not "
                "appear to mark the reference as non-normative"
            )

    if warnings:
        print("Architecture link warnings:")
        for warning in warnings:
            print(f"  WARN: {warning}")

    if errors:
        print("Architecture link verification failed:")
        for error in errors:
            print(f"  ERROR: {error}")
        return 1

    print(
        f"Architecture link verification passed: {len(arch_docs)} document(s), "
        "discovery path intact"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
