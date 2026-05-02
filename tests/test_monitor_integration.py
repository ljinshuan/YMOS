"""Integration test — fetch-prices CSV output → check-signals end-to-end."""

import json
from pathlib import Path

from cli.monitor.history import merge_kline_to_csv
from cli.monitor.signal_reader import (
    find_new_signals,
    format_alert_entry,
    scan_signals,
    write_alerts,
)


class TestMonitorIntegration:
    """End-to-end: write CSV history → create signal files → check-signals → alerts."""

    def test_full_pipeline(self, tmp_path):
        # --- Phase 1: Simulate fetch-prices writing CSV history ---
        history_dir = tmp_path / "history"
        history_dir.mkdir()

        # Simulate daily kline for SOXL
        daily_rows = [
            ["2026-05-01", "128.00", "130.50", "127.50", "129.80", "5000000"],
            ["2026-05-02", "129.80", "132.00", "129.00", "131.50", "4500000"],
            ["2026-05-03", "131.50", "133.00", "130.80", "132.20", "3800000"],
        ]
        csv_path = history_dir / "SOXL_daily.csv"
        added = merge_kline_to_csv(csv_path, daily_rows)
        assert added == 3

        # Second fetch — some overlap, some new
        daily_rows_2 = [
            ["2026-05-02", "129.80", "132.00", "129.00", "131.50", "4500000"],  # dup
            ["2026-05-03", "131.50", "133.00", "130.80", "132.20", "3800000"],  # dup
            ["2026-05-04", "132.20", "134.00", "131.50", "133.80", "4200000"],
        ]
        added = merge_kline_to_csv(csv_path, daily_rows_2)
        assert added == 1  # only 1 new

        # Verify CSV content
        lines = csv_path.read_text().strip().split("\n")
        assert len(lines) == 5  # header + 4 data rows

        # --- Phase 2: Simulate naught_backtest writing signal files ---
        signal_dir = tmp_path / "signals"
        signal_dir.mkdir()

        signal = {
            "ticker": "SOXL",
            "signal_time": "14:35",
            "signal_type": "buy",
            "strength": "strong",
            "strategy_name": "ma_cross",
            "detail": "5日均线上穿20日均线",
            "price_at_signal": 133.80,
        }
        (signal_dir / "SOXL.json").write_text(json.dumps(signal))

        # --- Phase 3: check-signals scans and generates alerts ---
        alert_path = tmp_path / "alerts" / "2026-05-04.md"
        signals = scan_signals(signal_dir)
        assert len(signals) == 1

        new_signals = find_new_signals(signals, alert_path)
        assert len(new_signals) == 1

        written = write_alerts(alert_path, new_signals)
        assert written == 1

        # Verify alert content
        alert_content = alert_path.read_text()
        assert "SOXL" in alert_content
        assert "买入信号" in alert_content
        assert "强" in alert_content
        assert "ma_cross" in alert_content
        assert "133.8" in alert_content

    def test_second_check_no_duplicates(self, tmp_path):
        """Second run of check-signals should find no new signals."""
        signal_dir = tmp_path / "signals"
        signal_dir.mkdir()
        alert_path = tmp_path / "alerts" / "2026-05-04.md"

        signal = {
            "ticker": "SOXL",
            "signal_time": "14:35",
            "signal_type": "buy",
            "strength": "strong",
            "strategy_name": "ma_cross",
            "detail": "golden cross",
            "price_at_signal": 130,
        }
        (signal_dir / "SOXL.json").write_text(json.dumps(signal))

        # First check
        signals = scan_signals(signal_dir)
        new = find_new_signals(signals, alert_path)
        write_alerts(alert_path, new)
        assert len(new) == 1

        # Second check — same signal
        signals2 = scan_signals(signal_dir)
        new2 = find_new_signals(signals2, alert_path)
        assert len(new2) == 0

    def test_multiple_tickers(self, tmp_path):
        """Multiple tickers with different signals."""
        signal_dir = tmp_path / "signals"
        signal_dir.mkdir()
        alert_path = tmp_path / "alerts" / "2026-05-04.md"

        signals_data = [
            {"ticker": "SOXL", "signal_time": "10:00", "signal_type": "buy", "strength": "strong", "strategy_name": "ma", "detail": "bullish", "price_at_signal": 130},
            {"ticker": "META", "signal_time": "10:05", "signal_type": "sell", "strength": "medium", "strategy_name": "rsi", "detail": "overbought", "price_at_signal": 512},
            {"ticker": "TSLA", "signal_time": "10:10", "signal_type": "warning", "strength": "weak", "strategy_name": "volume", "detail": "low volume", "price_at_signal": 280},
        ]
        for sig in signals_data:
            (signal_dir / f"{sig['ticker']}.json").write_text(json.dumps(sig))

        signals = scan_signals(signal_dir)
        new = find_new_signals(signals, alert_path)
        assert len(new) == 3

        write_alerts(alert_path, new)
        content = alert_path.read_text()
        assert "SOXL" in content
        assert "META" in content
        assert "TSLA" in content
        assert "买入信号" in content
        assert "卖出信号" in content
        assert "预警信号" in content
