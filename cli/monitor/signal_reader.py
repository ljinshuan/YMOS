"""Signal file scanner — read signals, validate schema, compare with alert log."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from cli.monitor.dedup import get_existing_signal_keys, make_signal_key

REQUIRED_SIGNAL_FIELDS = {"ticker", "signal_time", "signal_type", "strength", "strategy_name", "detail", "price_at_signal"}
VALID_SIGNAL_TYPES = {"buy", "sell", "hold", "warning"}
VALID_STRENGTHS = {"strong", "medium", "weak"}

SIGNAL_TYPE_CN = {"buy": "买入信号", "sell": "卖出信号", "hold": "持有信号", "warning": "预警信号"}
STRENGTH_CN = {"strong": "强", "medium": "中", "weak": "弱"}


def validate_signal(data: dict) -> list[str]:
    """Validate signal JSON structure. Returns list of error messages."""
    errors = []
    missing = REQUIRED_SIGNAL_FIELDS - set(data.keys())
    if missing:
        errors.append(f"missing fields: {', '.join(sorted(missing))}")
    if data.get("signal_type") not in VALID_SIGNAL_TYPES:
        errors.append(f"invalid signal_type: {data.get('signal_type')}")
    if data.get("strength") not in VALID_STRENGTHS:
        errors.append(f"invalid strength: {data.get('strength')}")
    return errors


def scan_signals(
    signal_dir: Path,
    tickers: list[str] | None = None,
) -> list[dict]:
    """Scan signal directory for valid signals.

    Args:
        signal_dir: Path to signals/ directory.
        tickers: Optional filter — only read these tickers.

    Returns:
        List of valid signal dicts.
    """
    if not signal_dir.exists():
        return []

    signals: list[dict] = []
    for json_file in sorted(signal_dir.glob("*.json")):
        if tickers:
            ticker_name = json_file.stem
            if ticker_name not in tickers:
                continue
        try:
            data = json.loads(json_file.read_text())
        except json.JSONDecodeError:
            print(f"⚠️  Skipping malformed JSON: {json_file.name}", flush=True)
            continue

        errors = validate_signal(data)
        if errors:
            print(f"⚠️  Skipping {json_file.name}: {', '.join(errors)}", flush=True)
            continue

        signals.append(data)

    return signals


def find_new_signals(
    signals: list[dict],
    alert_path: Path,
) -> list[dict]:
    """Filter signals to only those not yet in the alert log."""
    existing_keys = get_existing_signal_keys(alert_path)
    new = []
    for sig in signals:
        key = make_signal_key(sig["signal_time"], sig["strategy_name"])
        if key not in existing_keys:
            new.append(sig)
    return new


def format_alert_entry(signal: dict) -> str:
    """Format a signal as a markdown alert entry."""
    sig_type_cn = SIGNAL_TYPE_CN.get(signal["signal_type"], signal["signal_type"])
    strength_cn = STRENGTH_CN.get(signal["strength"], signal["strength"])
    # Extract HH:MM from signal_time
    time_short = signal["signal_time"][:5] if len(signal["signal_time"]) >= 5 else signal["signal_time"]
    lines = [
        f"## {time_short} {signal['ticker']} - {sig_type_cn} [{strength_cn}]",
        f"- 策略: {signal['strategy_name']}",
        f"- 详情: {signal['detail']}",
        f"- 触发价: {signal['price_at_signal']}",
    ]
    return "\n".join(lines)


def write_alerts(alert_path: Path, signals: list[dict]) -> int:
    """Append new signal alerts to daily alert log.

    Args:
        alert_path: Path to alerts/YYYY-MM-DD.md.
        signals: List of new signal dicts.

    Returns:
        Number of alerts written.
    """
    if not signals:
        return 0

    alert_path.parent.mkdir(parents=True, exist_ok=True)

    today = alert_path.stem
    header = f"# 告警日志 {today}\n"

    if alert_path.exists():
        content = alert_path.read_text()
        if not content.startswith("# "):
            content = header + "\n" + content
    else:
        content = header + "\n"

    entries = []
    for sig in signals:
        entries.append("\n" + format_alert_entry(sig) + "\n")

    content += "\n".join(entries) + "\n"
    alert_path.write_text(content)

    return len(signals)
