"""Markdown state-machine table parser and writer."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path


def read_state(filepath: Path) -> list[dict]:
    """Read a Markdown state-machine table and return a list of dicts.

    Each dict has keys from the header row and values from data rows.
    Metadata lines (title, 更新时间, etc.) are stored under a __meta__ key.
    """
    if not filepath.exists():
        return []

    text = filepath.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Parse metadata (lines before the table)
    meta: dict[str, str] = {}
    header_cols: list[str] = []
    records: list[dict] = []
    in_table = False
    past_separator = False

    for line in lines:
        stripped = line.strip()

        # Metadata: key-value pairs like "更新时间: 2026-01-01"
        if not stripped.startswith("|") and ":" in stripped and not in_table:
            key, _, val = stripped.partition(":")
            meta[key.strip()] = val.strip()
            continue

        if not stripped.startswith("|"):
            if in_table:
                in_table = False
            continue

        cols = [c.strip() for c in stripped.split("|")]
        cols = [c for c in cols if c]

        if not in_table:
            # Look for header row containing 'ticker' or '代码'
            header_candidates = [c.strip() for c in stripped.split("|") if c.strip()]
            if any(c.lower() in ("ticker", "代码", "标的") for c in header_candidates):
                header_cols = header_candidates
                in_table = True
                past_separator = False
            continue

        # Skip separator row |:---|:---|
        if not past_separator:
            if all(re.match(r"^[-:]+$", c.strip()) for c in cols if c.strip()):
                past_separator = True
                continue
            # If we see a non-separator, treat it as data (no separator found)
            past_separator = True

        # Data row
        if header_cols:
            row = {}
            for i, h in enumerate(header_cols):
                if i < len(cols):
                    row[h] = cols[i].strip()
                else:
                    row[h] = ""
            records.append(row)

    # Attach metadata to each record via special key
    for r in records:
        r["__meta__"] = meta

    return records


def write_state(filepath: Path, records: list[dict], changelog_entry: str = "") -> None:
    """Write records back to a Markdown state-machine file.

    Preserves the table format with header and separator rows.
    Updates 更新时间 and appends to 变更日志 if present.
    """
    if not records:
        return

    # Read original file to preserve structure
    meta_prefix: list[str] = []
    if filepath.exists():
        original = filepath.read_text(encoding="utf-8").splitlines()
        for line in original:
            if line.strip().startswith("|"):
                break
            meta_prefix.append(line)

    # Get headers from first record (excluding __meta__)
    sample = records[0]
    headers = [k for k in sample.keys() if k != "__meta__"]

    # Build output
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines: list[str] = []

    # Update metadata
    updated_prefix = False
    for line in meta_prefix:
        if line.strip().startswith("更新时间"):
            lines.append(f"更新时间: {now_str}")
            updated_prefix = True
        else:
            lines.append(line)
    if not updated_prefix and meta_prefix:
        # If no 更新时间 line found but there is metadata, add one
        lines.append(f"更新时间: {now_str}")

    # Blank line before table
    if lines and lines[-1].strip():
        lines.append("")

    # Header row
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(":---" for _ in headers) + " |")

    # Data rows
    for record in records:
        vals = [str(record.get(h, "")) for h in headers]
        lines.append("| " + " | ".join(vals) + " |")

    # Changelog
    if changelog_entry:
        lines.append("")
        lines.append(f"### 变更日志")
        lines.append(f"- [{now_str}] {changelog_entry}")

    filepath.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_row(filepath: Path, match_field: str, match_value: str,
               updates: dict[str, str], changelog_entry: str = "") -> bool:
    """Update a specific row in a state-machine table matching match_field=match_value.

    Returns True if a row was found and updated.
    """
    records = read_state(filepath)
    if not records:
        return False

    found = False
    for record in records:
        if record.get(match_field, "").upper() == match_value.upper():
            for k, v in updates.items():
                if k in record:
                    record[k] = v
            found = True
            break

    if found:
        if not changelog_entry:
            changes = ", ".join(f"{k}={v}" for k, v in updates.items())
            changelog_entry = f"{match_field}={match_value}: {changes}"
        write_state(filepath, records, changelog_entry)
    return found
