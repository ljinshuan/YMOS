"""CSV history file management — read, merge with dedup, write."""

from __future__ import annotations

import csv
from pathlib import Path

from cli.monitor.dedup import get_existing_csv_timestamps

CSV_HEADER = "timestamp,open,high,low,close,volume"


def merge_kline_to_csv(
    csv_path: Path,
    rows: list[list[str]],
) -> int:
    """Merge new kline rows into CSV, deduplicating by timestamp.

    Args:
        csv_path: Path to the CSV file.
        rows: List of [timestamp, open, high, low, close, volume] rows.

    Returns:
        Number of new rows actually written (excluding duplicates).
    """
    existing_ts = get_existing_csv_timestamps(csv_path)
    new_rows = [r for r in rows if r[0] not in existing_ts]

    if not new_rows:
        return 0

    # Collect all rows (existing + new) for sorted write
    all_rows: list[list[str]] = []
    if csv_path.exists():
        with open(csv_path, newline="") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            for row in reader:
                if row:
                    all_rows.append(row)
    all_rows.extend(new_rows)

    # Sort by timestamp
    all_rows.sort(key=lambda r: r[0])

    # Write back
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with open(csv_path, "w", newline="") as f:
        f.write(CSV_HEADER + "\n")
        writer = csv.writer(f)
        writer.writerows(all_rows)

    return len(new_rows)


def read_csv_timestamps(csv_path: Path) -> list[str]:
    """Read all timestamps from a CSV file, sorted ascending."""
    if not csv_path.exists():
        return []
    timestamps = []
    with open(csv_path, newline="") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if row:
                timestamps.append(row[0])
    return timestamps
