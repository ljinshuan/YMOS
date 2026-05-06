"""Integration tests — real Futu OpenD connection + mock signals.

These tests require Futu OpenD running locally. Skipped automatically if unavailable.

Run: uv run pytest tests/test_monitor_integration_opend.py -v
"""

import json
import os
from datetime import datetime
from pathlib import Path

import pytest
from typer.testing import CliRunner

from cli.core.futu_utils import check_opend_connection
from cli.commands.monitor import app, _fetch_kline, _get_snapshot_price

runner = CliRunner()

OPEND_HOST = os.getenv("FUTU_OPEND_HOST", "127.0.0.1")
OPEND_PORT = int(os.getenv("FUTU_OPEND_PORT", "11111"))

requires_opend = pytest.mark.skipif(
    not check_opend_connection(OPEND_HOST, OPEND_PORT),
    reason="Futu OpenD not running at {OPEND_HOST}:{OPEND_PORT}",
)


# ── fetch-prices: real OpenD ──────────────────────────────────────────


@requires_opend
class TestFetchKlineRealOpenD:
    """Test _fetch_kline with real Futu OpenD."""

    def test_us_daily_kline(self):
        import futu as ft

        rows = _fetch_kline("AAPL", ft.KLType.K_DAY, 10, OPEND_HOST, OPEND_PORT)
        assert rows is not None
        assert len(rows) > 0
        # Verify row structure: [timestamp, open, high, low, close, volume]
        row = rows[0]
        assert len(row) == 6
        # Timestamp should be a date string
        assert "-" in row[0]
        # OHLCV should be numeric
        for field in row[1:]:
            float(field)

    def test_hk_daily_kline(self):
        import futu as ft

        rows = _fetch_kline("0700.HK", ft.KLType.K_DAY, 10, OPEND_HOST, OPEND_PORT)
        assert rows is not None
        assert len(rows) > 0

    def test_a_share_daily_kline(self):
        import futu as ft

        rows = _fetch_kline("000001.SZ", ft.KLType.K_DAY, 10, OPEND_HOST, OPEND_PORT)
        assert rows is not None
        assert len(rows) > 0

    def test_us_minute_kline(self):
        import futu as ft

        rows = _fetch_kline("AAPL", ft.KLType.K_5M, 10, OPEND_HOST, OPEND_PORT)
        assert rows is not None
        # Minute kline might be empty outside trading hours
        if rows:
            assert len(rows[0]) == 6
            # Minute timestamps should have HH:MM
            assert ":" in rows[0][0]

    def test_invalid_ticker(self):
        import futu as ft

        rows = _fetch_kline("NOTREAL999", ft.KLType.K_DAY, 10, OPEND_HOST, OPEND_PORT)
        # Should return None or empty, not crash
        assert rows is None or rows == []

    def test_snapshot_from_rows(self):
        import futu as ft

        rows = _fetch_kline("AAPL", ft.KLType.K_DAY, 10, OPEND_HOST, OPEND_PORT)
        if not rows:
            pytest.skip("No data returned for AAPL")
        snap = _get_snapshot_price(rows)
        assert snap["source"] == "futu_opend"
        assert snap["close"] > 0
        assert snap["volume"] > 0
        assert "change_pct" in snap


# ── fetch-prices CLI: real OpenD ──────────────────────────────────────


@requires_opend
class TestFetchPricesCLI:
    """Test `ymos monitor fetch-prices` CLI with real OpenD."""

    def test_single_ticker(self, tmp_path):
        result = runner.invoke(app, [
            "fetch-prices",
            "--symbols", "AAPL",
            "--output-dir", str(tmp_path),
            "--count", "10",
            "--no-skip-non-trading-hours",  # bypass trading hours check for testing
        ])
        assert result.exit_code == 0, result.output

        # Verify CSV files created
        daily_csv = tmp_path / "history" / "AAPL_daily.csv"
        minute_csv = tmp_path / "history" / "AAPL_5m.csv"
        assert daily_csv.exists(), f"Daily CSV not found. Output: {result.output}"

        # Verify CSV has header + data rows
        lines = daily_csv.read_text().strip().split("\n")
        assert lines[0] == "timestamp,open,high,low,close,volume"
        assert len(lines) > 1

        # Verify snapshot JSON
        today = datetime.now().strftime("%Y-%m-%d")
        snap_dir = tmp_path / "prices" / today
        assert snap_dir.exists(), f"Snapshot dir not found. Output: {result.output}"
        snap_files = list(snap_dir.glob("*.json"))
        assert len(snap_files) == 1
        snap = json.loads(snap_files[0].read_text())
        assert "AAPL" in snap["tickers"]
        assert snap["tickers"]["AAPL"]["source"] == "futu_opend"

    def test_multiple_tickers(self, tmp_path):
        result = runner.invoke(app, [
            "fetch-prices",
            "--symbols", "AAPL,0700.HK",
            "--output-dir", str(tmp_path),
            "--count", "10",
            "--no-skip-non-trading-hours",
        ])
        assert result.exit_code == 0, result.output

        # Verify both tickers have CSV files
        assert (tmp_path / "history" / "AAPL_daily.csv").exists()
        assert (tmp_path / "history" / "0700.HK_daily.csv").exists()

    def test_dedup_on_second_fetch(self, tmp_path):
        """Fetch twice, verify CSV rows don't duplicate."""
        args = [
            "fetch-prices",
            "--symbols", "AAPL",
            "--output-dir", str(tmp_path),
            "--count", "10",
            "--no-skip-non-trading-hours",
        ]
        # First fetch
        result1 = runner.invoke(app, args)
        assert result1.exit_code == 0, result1.output
        csv_path = tmp_path / "history" / "AAPL_daily.csv"
        lines1 = csv_path.read_text().strip().split("\n")
        data_rows_1 = len(lines1) - 1  # minus header

        # Second fetch
        result2 = runner.invoke(app, args)
        assert result2.exit_code == 0, result2.output
        lines2 = csv_path.read_text().strip().split("\n")
        data_rows_2 = len(lines2) - 1

        # Should not duplicate
        assert data_rows_2 == data_rows_1, (
            f"Rows grew from {data_rows_1} to {data_rows_2} — dedup failed"
        )

    def test_custom_kline_period(self, tmp_path):
        result = runner.invoke(app, [
            "fetch-prices",
            "--symbols", "AAPL",
            "--output-dir", str(tmp_path),
            "--kline", "60m",
            "--count", "10",
            "--no-skip-non-trading-hours",
        ])
        assert result.exit_code == 0, result.output
        assert (tmp_path / "history" / "AAPL_60m.csv").exists()

    def test_invalid_kline_period(self, tmp_path):
        result = runner.invoke(app, [
            "fetch-prices",
            "--symbols", "AAPL",
            "--output-dir", str(tmp_path),
            "--kline", "99m",
        ])
        assert result.exit_code == 1
        assert "Invalid kline" in result.output

    def test_no_symbols(self, tmp_path):
        result = runner.invoke(app, [
            "fetch-prices",
            "--output-dir", str(tmp_path),
        ])
        assert result.exit_code == 1
        assert "No symbols" in result.output


# ── check-signals with mock signals ───────────────────────────────────


class TestCheckSignalsWithMockedSignals:
    """Test check-signals CLI with mock signal files (no naught_backtest needed)."""

    def test_no_signals_dir(self, tmp_path):
        result = runner.invoke(app, [
            "check-signals",
            "--signal-dir", str(tmp_path / "nonexistent"),
            "--output-dir", str(tmp_path),
        ])
        assert result.exit_code == 0
        assert result.output == ""  # silent exit

    def test_new_signal_generates_alert(self, tmp_path):
        # Create mock signal file (as naught_backtest would)
        signal_dir = tmp_path / "signals"
        signal_dir.mkdir()
        signal = {
            "ticker": "AAPL",
            "signal_time": "14:35",
            "signal_type": "buy",
            "strength": "strong",
            "strategy_name": "ma_cross",
            "detail": "5日均线上穿20日均线",
            "price_at_signal": 198.50,
        }
        (signal_dir / "AAPL.json").write_text(json.dumps(signal))

        result = runner.invoke(app, [
            "check-signals",
            "--signal-dir", str(signal_dir),
            "--output-dir", str(tmp_path),
        ])
        assert result.exit_code == 0
        assert "AAPL" in result.output
        assert "买入信号" in result.output
        assert "ma_cross" in result.output

        # Verify alert file
        today = datetime.now().strftime("%Y-%m-%d")
        alert_path = tmp_path / "alerts" / f"{today}.md"
        assert alert_path.exists()
        content = alert_path.read_text()
        assert "AAPL" in content
        assert "198.5" in content

    def test_duplicate_signal_silent(self, tmp_path):
        signal_dir = tmp_path / "signals"
        signal_dir.mkdir()
        signal = {
            "ticker": "AAPL",
            "signal_time": "14:35",
            "signal_type": "buy",
            "strength": "strong",
            "strategy_name": "ma_cross",
            "detail": "test",
            "price_at_signal": 100,
        }
        (signal_dir / "AAPL.json").write_text(json.dumps(signal))

        args = [
            "check-signals",
            "--signal-dir", str(signal_dir),
            "--output-dir", str(tmp_path),
        ]
        # First check
        result1 = runner.invoke(app, args)
        assert "AAPL" in result1.output

        # Second check — same signal, should be silent
        result2 = runner.invoke(app, args)
        assert result2.output == ""

    def test_ticker_filter(self, tmp_path):
        signal_dir = tmp_path / "signals"
        signal_dir.mkdir()
        for ticker in ["AAPL", "META", "TSLA"]:
            (signal_dir / f"{ticker}.json").write_text(json.dumps({
                "ticker": ticker,
                "signal_time": "10:00",
                "signal_type": "buy",
                "strength": "strong",
                "strategy_name": "test",
                "detail": "test",
                "price_at_signal": 100,
            }))

        result = runner.invoke(app, [
            "check-signals",
            "--tickers", "AAPL",
            "--signal-dir", str(signal_dir),
            "--output-dir", str(tmp_path),
        ])
        assert "AAPL" in result.output
        assert "META" not in result.output
        assert "TSLA" not in result.output

    def test_multiple_signal_types(self, tmp_path):
        signal_dir = tmp_path / "signals"
        signal_dir.mkdir()
        signals = [
            ("SOXL", "buy", "strong", "ma_cross"),
            ("META", "sell", "medium", "rsi"),
            ("TSLA", "warning", "weak", "volume"),
            ("NVDA", "hold", "strong", "trend"),
        ]
        for ticker, sig_type, strength, strategy in signals:
            (signal_dir / f"{ticker}.json").write_text(json.dumps({
                "ticker": ticker,
                "signal_time": "10:00",
                "signal_type": sig_type,
                "strength": strength,
                "strategy_name": strategy,
                "detail": f"test {sig_type}",
                "price_at_signal": 100,
            }))

        result = runner.invoke(app, [
            "check-signals",
            "--signal-dir", str(signal_dir),
            "--output-dir", str(tmp_path),
        ])
        assert result.exit_code == 0
        assert "买入信号" in result.output
        assert "卖出信号" in result.output
        assert "预警信号" in result.output
        assert "持有信号" in result.output


# ── Full pipeline: real fetch + mock signals ──────────────────────────


@requires_opend
class TestFullPipeline:
    """End-to-end: real fetch-prices → mock signals → check-signals."""

    def test_fetch_then_check_signals(self, tmp_path):
        # Step 1: Fetch real prices
        result = runner.invoke(app, [
            "fetch-prices",
            "--symbols", "AAPL",
            "--output-dir", str(tmp_path),
            "--count", "10",
            "--no-skip-non-trading-hours",
        ])
        assert result.exit_code == 0, result.output

        # Verify CSV exists and has data
        csv_path = tmp_path / "history" / "AAPL_daily.csv"
        assert csv_path.exists()
        lines = csv_path.read_text().strip().split("\n")
        assert len(lines) > 1  # header + data

        # Step 2: Mock naught_backtest writing signal files
        # Read the latest price from CSV to use as signal price
        last_line = lines[-1].split(",")
        last_price = float(last_line[4])

        signal_dir = tmp_path / "signals"
        signal_dir.mkdir()
        signal = {
            "ticker": "AAPL",
            "signal_time": datetime.now().strftime("%H:%M"),
            "signal_type": "buy",
            "strength": "strong",
            "strategy_name": "ma_cross",
            "detail": f"5日均线上穿20日均线，收盘价 {last_price}",
            "price_at_signal": last_price,
        }
        (signal_dir / "AAPL.json").write_text(json.dumps(signal))

        # Step 3: Check signals
        result = runner.invoke(app, [
            "check-signals",
            "--signal-dir", str(signal_dir),
            "--output-dir", str(tmp_path),
        ])
        assert result.exit_code == 0
        assert "AAPL" in result.output
        assert "买入信号" in result.output
        assert "ma_cross" in result.output

        # Verify alert file references real price
        today = datetime.now().strftime("%Y-%m-%d")
        alert_path = tmp_path / "alerts" / f"{today}.md"
        assert alert_path.exists()
        content = alert_path.read_text()
        assert str(last_price) in content
