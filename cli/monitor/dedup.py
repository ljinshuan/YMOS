"""Deduplication utilities for CSV timestamps and signal composite keys."""

from __future__ import annotations

import csv
from pathlib import Path


def get_existing_csv_timestamps(path: Path) -> set[str]:
    """Read existing timestamps from a CSV file's first column."""
    if not path.exists():
        return set()
    timestamps: set[str] = set()
    with open(path, newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header is None:
            return set()
        for row in reader:
            if row:
                timestamps.add(row[0])
    return timestamps


def get_existing_signal_keys(alert_path: Path) -> set[str]:
    """Read existing signal dedup keys from alert log.

    Keys are formatted as "signal_time|strategy_name".
    """
    if not alert_path.exists():
        return set()
    keys: set[str] = set()
    with open(alert_path) as f:
        for line in f:
            line = line.strip()
            # Match lines like: "## 14:35 SOXL - 买入信号 [强]"
            if not line.startswith("## "):
                continue
            # Extract metadata from subsequent lines
            # We parse the whole alert block below
    # Re-parse with structured approach: look for signal_time and strategy lines
    keys = _parse_alert_keys(alert_path)
    return keys


def _parse_alert_keys(alert_path: Path) -> set[str]:
    """Parse alert log to extract signal_time|strategy_name keys."""
    keys: set[str] = set()
    content = alert_path.read_text() if alert_path.exists() else ""
    # Alert format:
    # ## HH:MM TICKER - 信号类型 [强度]
    # - 策略: strategy_name
    # We extract time from ## header and strategy from 策略 line
    import re

    pattern = re.compile(r"^## (\d{2}:\d{2}).*?\n.*?策略:\s*(\S+)", re.MULTILINE)
    for match in pattern.finditer(content):
        signal_time = match.group(1)
        strategy_name = match.group(2)
        keys.add(f"{signal_time}|{strategy_name}")
    return keys


def make_signal_key(signal_time: str, strategy_name: str) -> str:
    """Create a dedup key from signal_time and strategy_name."""
    return f"{signal_time}|{strategy_name}"
