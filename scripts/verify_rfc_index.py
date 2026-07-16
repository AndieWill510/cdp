#!/usr/bin/env python3
"""Verify consistency across canonical RFC files, manifest, and band indexes."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RFC_ROOT = ROOT / "rfc"
INDEX_ROOT = RFC_ROOT / "index"
MANIFEST_PATH = INDEX_ROOT / "rfc-manifest.json"
RFC_FILENAME_RE = re.compile(r"^RFC-CDP-(\d{3})-.*\.md$")
HEADER_NUMBER_RE = re.compile(r"^# RFC-CDP-(\d{3})\s+[—-]\s+(.+)$", re.MULTILINE)
STATUS_RE = re.compile(r"^Status:\s*(.+?)\s*$", re.MULTILINE)
BOLD_STATUS_RE = re.compile(r"^\*\*Status:\*\*\s*(.+?)\s*$", re.MULTILINE)


def expected_band(number: int) -> str:
    if number <= 9:
        return "000-009"
    if number <= 19:
        return "010-019"
    if number <= 29:
        return "020-029"
    if number <= 39:
        return "030-039"
    if number <= 49:
        return "040-049"
    if number <= 59:
        return "050-059"
    if number <= 69:
        return "060-069"
    if number <= 79:
        return "070-079"
    if number <= 89:
        return "080-089"
    if number <= 99:
        return "090-099"
    if number <= 119:
        return "100-119"
    if number <= 149:
        return "120-149"
    return "150+"


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    entries = manifest.get("entries", [])

    numbers = [entry["number"] for entry in entries]
    files = [entry["file"] for entry in entries]

    for number, count in Counter(numbers).items():
        if count > 1:
            errors.append(f"duplicate RFC number in manifest: {number}")

    for filename, count in Counter(files).items():
        if count > 1:
            errors.append(f"duplicate RFC filename in manifest: {filename}")

    indexed_files: set[str] = set()

    for entry in entries:
        number = entry["number"]
        filename = entry["file"]
        status = entry["status"]
        band = entry["band"]
        indexed_files.add(filename)

        if expected_band(int(number)) != band:
            errors.append(
                f"RFC {number} has band {band}; expected {expected_band(int(number))}"
            )

        path = RFC_ROOT / filename
        if status.startswith("Reserved"):
            if path.exists():
                warnings.append(
                    f"reserved RFC has a file and may need promotion review: {filename}"
                )
            continue

        if not path.exists():
            errors.append(f"manifest points to missing canonical file: {filename}")
            continue

        text = path.read_text(encoding="utf-8")
        header = HEADER_NUMBER_RE.search(text)
        if not header:
            warnings.append(f"missing or malformed RFC heading: {filename}")
        elif header.group(1) != number:
            warnings.append(
                "legacy RFC number remains in header: "
                f"{filename} manifest={number}, header={header.group(1)}"
            )

        status_match = STATUS_RE.search(text) or BOLD_STATUS_RE.search(text)
        if not status_match:
            warnings.append(f"could not read Status header from {filename}")
        elif status_match.group(1).strip() != status:
            warnings.append(
                "manifest/header status drift: "
                f"{filename} manifest={status!r}, header={status_match.group(1).strip()!r}"
            )

    canonical_files = {
        path.name
        for path in RFC_ROOT.glob("RFC-CDP-*.md")
        if RFC_FILENAME_RE.match(path.name)
    }
    unindexed = sorted(canonical_files - indexed_files)
    for filename in unindexed:
        warnings.append(f"canonical RFC file is not yet in manifest: {filename}")

    for index_path in INDEX_ROOT.glob("*.md"):
        if index_path.name == "README.md":
            continue
        text = index_path.read_text(encoding="utf-8")
        band_match = re.match(r"^(\d{3}-\d{3})-", index_path.name)
        if not band_match:
            continue
        band = band_match.group(1)
        for entry in entries:
            if entry["band"] == band and entry["number"] not in text:
                errors.append(
                    f"band index {index_path.name} omits RFC {entry['number']}"
                )

    if warnings:
        print("RFC index warnings:")
        for warning in warnings:
            print(f"  WARN: {warning}")

    if errors:
        print("RFC index verification failed:")
        for error in errors:
            print(f"  ERROR: {error}")
        return 1

    print(f"RFC index verification passed: {len(entries)} manifest entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
