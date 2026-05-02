"""Tests for cli.monitor.history — CSV merge with dedup."""

from pathlib import Path

from cli.monitor.history import merge_kline_to_csv, read_csv_timestamps


class TestMergeKlineToCsv:
    def test_new_file(self, tmp_path):
        csv_path = tmp_path / "SOXL_daily.csv"
        rows = [
            ["2026-05-03 09:30:00", "129.00", "131.50", "128.80", "130.42", "1234567"],
            ["2026-05-03 09:35:00", "130.50", "132.00", "130.20", "131.80", "987654"],
        ]
        added = merge_kline_to_csv(csv_path, rows)
        assert added == 2
        assert csv_path.exists()
        lines = csv_path.read_text().strip().split("\n")
        assert len(lines) == 3  # header + 2 rows
        assert lines[0] == "timestamp,open,high,low,close,volume"

    def test_merge_with_dedup(self, tmp_path):
        csv_path = tmp_path / "SOXL_daily.csv"
        rows1 = [
            ["2026-05-03 09:30:00", "129.00", "131.50", "128.80", "130.42", "1234567"],
        ]
        merge_kline_to_csv(csv_path, rows1)

        rows2 = [
            ["2026-05-03 09:30:00", "129.00", "131.50", "128.80", "130.42", "1234567"],  # dup
            ["2026-05-03 09:35:00", "130.50", "132.00", "130.20", "131.80", "987654"],
        ]
        added = merge_kline_to_csv(csv_path, rows2)
        assert added == 1  # only 1 new row

        lines = csv_path.read_text().strip().split("\n")
        assert len(lines) == 3  # header + 2 unique rows

    def test_all_duplicates(self, tmp_path):
        csv_path = tmp_path / "SOXL_daily.csv"
        rows = [
            ["2026-05-03 09:30:00", "129.00", "131.50", "128.80", "130.42", "1234567"],
        ]
        merge_kline_to_csv(csv_path, rows)

        added = merge_kline_to_csv(csv_path, rows)
        assert added == 0

    def test_sorted_output(self, tmp_path):
        csv_path = tmp_path / "SOXL_daily.csv"
        rows = [
            ["2026-05-03 09:35:00", "130.50", "132.00", "130.20", "131.80", "987654"],
            ["2026-05-03 09:30:00", "129.00", "131.50", "128.80", "130.42", "1234567"],
        ]
        merge_kline_to_csv(csv_path, rows)

        lines = csv_path.read_text().strip().split("\n")
        assert "09:30" in lines[1]
        assert "09:35" in lines[2]

    def test_empty_rows(self, tmp_path):
        csv_path = tmp_path / "SOXL_daily.csv"
        added = merge_kline_to_csv(csv_path, [])
        assert added == 0
        assert not csv_path.exists()


class TestReadCsvTimestamps:
    def test_existing_file(self, tmp_path):
        csv_path = tmp_path / "test.csv"
        csv_path.write_text(
            "timestamp,open,high,low,close,volume\n"
            "2026-05-03 09:30:00,129,131,128,130,1234\n"
            "2026-05-03 09:35:00,130,132,130,131,987\n"
        )
        result = read_csv_timestamps(csv_path)
        assert result == ["2026-05-03 09:30:00", "2026-05-03 09:35:00"]

    def test_nonexistent_file(self, tmp_path):
        csv_path = tmp_path / "nonexistent.csv"
        result = read_csv_timestamps(csv_path)
        assert result == []
