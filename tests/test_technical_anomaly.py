"""Tests for cli.core.sources.technical_anomaly — anomaly extraction logic."""

from cli.core.sources.technical_anomaly import _extract_anomalies, _normalize_data


class TestNormalizeData:
    def test_list_passthrough(self):
        data = [{"a": 1}]
        assert _normalize_data(data) == data

    def test_dict_passthrough(self):
        data = {"a": 1}
        assert _normalize_data(data) == data

    def test_empty_returns_empty(self):
        assert _normalize_data(None) == []

    def test_string_returns_empty(self):
        assert _normalize_data("hello") == []


class TestExtractAnomalies:
    def test_empty_input(self):
        assert _extract_anomalies([]) == []

    def test_single_anomaly(self):
        data = [{
            "date": "2026-04-05",
            "indicator": "MACD",
            "signal_direction": "bullish",
            "description": "金叉",
            "support": "150.0",
            "resistance": "165.0",
            "probability": None,
        }]
        result = _extract_anomalies(data)
        assert len(result) == 1
        assert result[0]["indicator"] == "MACD"
        assert result[0]["signal_direction"] == "bullish"

    def test_multiple_anomalies(self):
        data = [
            {"date": "2026-04-05", "indicator": "MACD", "description": "金叉"},
            {"date": "2026-04-06", "indicator": "RSI", "description": "超买"},
        ]
        result = _extract_anomalies(data)
        assert len(result) == 2

    def test_non_dict_items_skipped(self):
        data = ["not a dict", {"date": "2026-04-05", "indicator": "MACD"}]
        result = _extract_anomalies(data)
        assert len(result) == 1

    def test_fallback_field_names(self):
        data = [{"indicator_name": "KDJ", "direction": "bearish"}]
        result = _extract_anomalies(data)
        assert result[0]["indicator"] == "KDJ"
        assert result[0]["signal_direction"] == "bearish"
