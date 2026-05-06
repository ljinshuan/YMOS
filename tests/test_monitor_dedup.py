"""Tests for cli.monitor.dedup — CSV and signal dedup."""

import tempfile
from pathlib import Path

from cli.monitor.dedup import (
    get_existing_csv_timestamps,
    get_existing_signal_keys,
    make_signal_key,
)


class TestGetExistingCsvTimestamps:
    def test_empty_file(self, tmp_path):
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("timestamp,open,high,low,close,volume\n")
        result = get_existing_csv_timestamps(csv_file)
        assert result == set()

    def test_existing_timestamps(self, tmp_path):
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "timestamp,open,high,low,close,volume\n"
            "2026-05-03 09:30:00,100,101,99,100.5,1000\n"
            "2026-05-03 09:35:00,100.5,102,100,101,1200\n"
        )
        result = get_existing_csv_timestamps(csv_file)
        assert result == {"2026-05-03 09:30:00", "2026-05-03 09:35:00"}

    def test_nonexistent_file(self, tmp_path):
        csv_file = tmp_path / "nonexistent.csv"
        result = get_existing_csv_timestamps(csv_file)
        assert result == set()


class TestMakeSignalKey:
    def test_basic(self):
        assert make_signal_key("14:35", "ma_cross") == "14:35|ma_cross"

    def test_different_strategy(self):
        k1 = make_signal_key("14:35", "ma_cross")
        k2 = make_signal_key("14:35", "rsi")
        assert k1 != k2


class TestGetExistingSignalKeys:
    def test_empty_file(self, tmp_path):
        alert_file = tmp_path / "2026-05-03.md"
        alert_file.write_text("# 告警日志 2026-05-03\n")
        result = get_existing_signal_keys(alert_file)
        assert result == set()

    def test_existing_alerts(self, tmp_path):
        alert_file = tmp_path / "2026-05-03.md"
        alert_file.write_text(
            "# 告警日志 2026-05-03\n"
            "\n## 14:35 SOXL - 买入信号 [强]\n"
            "- 策略: ma_cross\n"
            "- 详情: 5日均线上穿20日均线\n"
            "- 触发价: 130.42\n"
            "\n## 15:10 META - 卖出信号 [中]\n"
            "- 策略: rsi_divergence\n"
            "- 详情: RSI顶背离\n"
            "- 触发价: 512.80\n"
        )
        result = get_existing_signal_keys(alert_file)
        assert "14:35|ma_cross" in result
        assert "15:10|rsi_divergence" in result

    def test_nonexistent_file(self, tmp_path):
        alert_file = tmp_path / "nonexistent.md"
        result = get_existing_signal_keys(alert_file)
        assert result == set()
