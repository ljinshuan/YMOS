"""Tests for cli.monitor.signal_reader — signal scanning, validation, alerting."""

import json
from pathlib import Path

from cli.monitor.signal_reader import (
    find_new_signals,
    format_alert_entry,
    scan_signals,
    validate_signal,
    write_alerts,
)


class TestValidateSignal:
    def test_valid_signal(self):
        data = {
            "ticker": "SOXL",
            "signal_time": "14:35",
            "signal_type": "buy",
            "strength": "strong",
            "strategy_name": "ma_cross",
            "detail": "test",
            "price_at_signal": 130.42,
        }
        assert validate_signal(data) == []

    def test_missing_fields(self):
        data = {"ticker": "SOXL"}
        errors = validate_signal(data)
        assert len(errors) > 0
        assert "missing" in errors[0]

    def test_invalid_signal_type(self):
        data = {
            "ticker": "SOXL",
            "signal_time": "14:35",
            "signal_type": "invalid",
            "strength": "strong",
            "strategy_name": "ma_cross",
            "detail": "test",
            "price_at_signal": 130.42,
        }
        errors = validate_signal(data)
        assert any("signal_type" in e for e in errors)

    def test_invalid_strength(self):
        data = {
            "ticker": "SOXL",
            "signal_time": "14:35",
            "signal_type": "buy",
            "strength": "extreme",
            "strategy_name": "ma_cross",
            "detail": "test",
            "price_at_signal": 130.42,
        }
        errors = validate_signal(data)
        assert any("strength" in e for e in errors)


class TestScanSignals:
    def test_valid_signals(self, tmp_path):
        signal = {
            "ticker": "SOXL",
            "signal_time": "14:35",
            "signal_type": "buy",
            "strength": "strong",
            "strategy_name": "ma_cross",
            "detail": "golden cross",
            "price_at_signal": 130.42,
        }
        (tmp_path / "SOXL.json").write_text(json.dumps(signal))
        result = scan_signals(tmp_path)
        assert len(result) == 1
        assert result[0]["ticker"] == "SOXL"

    def test_malformed_json(self, tmp_path):
        (tmp_path / "BAD.json").write_text("not json{{{")
        result = scan_signals(tmp_path)
        assert result == []

    def test_invalid_schema(self, tmp_path):
        (tmp_path / "BAD.json").write_text(json.dumps({"ticker": "SOXL"}))
        result = scan_signals(tmp_path)
        assert result == []

    def test_ticker_filter(self, tmp_path):
        for name in ["SOXL", "META"]:
            (tmp_path / f"{name}.json").write_text(json.dumps({
                "ticker": name,
                "signal_time": "14:35",
                "signal_type": "buy",
                "strength": "strong",
                "strategy_name": "test",
                "detail": "test",
                "price_at_signal": 100,
            }))
        result = scan_signals(tmp_path, tickers=["SOXL"])
        assert len(result) == 1
        assert result[0]["ticker"] == "SOXL"

    def test_empty_dir(self, tmp_path):
        result = scan_signals(tmp_path)
        assert result == []

    def test_nonexistent_dir(self, tmp_path):
        result = scan_signals(tmp_path / "nope")
        assert result == []


class TestFindNewSignals:
    def test_all_new(self, tmp_path):
        alert_path = tmp_path / "2026-05-03.md"
        signals = [{"signal_time": "14:35", "strategy_name": "ma_cross", "ticker": "SOXL", "signal_type": "buy", "strength": "strong", "detail": "test", "price_at_signal": 130}]
        result = find_new_signals(signals, alert_path)
        assert len(result) == 1

    def test_duplicate_filtered(self, tmp_path):
        alert_path = tmp_path / "2026-05-03.md"
        alert_path.write_text(
            "# 告警日志\n\n"
            "## 14:35 SOXL - 买入信号 [强]\n"
            "- 策略: ma_cross\n"
            "- 详情: test\n"
            "- 触发价: 130\n"
        )
        signals = [{"signal_time": "14:35", "strategy_name": "ma_cross", "ticker": "SOXL", "signal_type": "buy", "strength": "strong", "detail": "test", "price_at_signal": 130}]
        result = find_new_signals(signals, alert_path)
        assert len(result) == 0


class TestFormatAlertEntry:
    def test_buy_signal(self):
        sig = {
            "ticker": "SOXL",
            "signal_time": "14:35",
            "signal_type": "buy",
            "strength": "strong",
            "strategy_name": "ma_cross",
            "detail": "golden cross",
            "price_at_signal": 130.42,
        }
        entry = format_alert_entry(sig)
        assert "14:35" in entry
        assert "SOXL" in entry
        assert "买入信号" in entry
        assert "强" in entry
        assert "ma_cross" in entry


class TestWriteAlerts:
    def test_new_file(self, tmp_path):
        alert_path = tmp_path / "2026-05-03.md"
        signals = [{"signal_time": "14:35", "strategy_name": "ma_cross", "ticker": "SOXL", "signal_type": "buy", "strength": "strong", "detail": "test", "price_at_signal": 130}]
        written = write_alerts(alert_path, signals)
        assert written == 1
        content = alert_path.read_text()
        assert "# 告警日志 2026-05-03" in content
        assert "SOXL" in content

    def test_no_signals(self, tmp_path):
        alert_path = tmp_path / "2026-05-03.md"
        written = write_alerts(alert_path, [])
        assert written == 0
        assert not alert_path.exists()

    def test_append_to_existing(self, tmp_path):
        alert_path = tmp_path / "2026-05-03.md"
        alert_path.write_text("# 告警日志 2026-05-03\n")
        signals = [{"signal_time": "14:35", "strategy_name": "ma_cross", "ticker": "SOXL", "signal_type": "buy", "strength": "strong", "detail": "test", "price_at_signal": 130}]
        write_alerts(alert_path, signals)
        content = alert_path.read_text()
        assert "SOXL" in content
        assert content.startswith("# 告警日志")
