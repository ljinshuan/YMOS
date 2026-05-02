"""Tests for cli.core.sources.derivatives_anomaly — warrant dimension filtering and market detection."""

from cli.core.sources.derivatives_anomaly import (
    OPTION_DIMENSIONS,
    VALID_DIMENSIONS,
    WARRANT_DIMENSIONS,
    _detect_market,
    _extract_anomalies_by_dimension,
    _build_summary,
)


class TestDetectMarket:
    def test_hk(self):
        assert _detect_market("0700.HK") == "HK"

    def test_us(self):
        assert _detect_market("AAPL") == "US"

    def test_shanghai(self):
        assert _detect_market("688008.SS") == "CN"

    def test_shenzhen(self):
        assert _detect_market("000001.SZ") == "CN"


class TestDimensionConstants:
    def test_warrant_dimensions_are_subset(self):
        assert WARRANT_DIMENSIONS.issubset(VALID_DIMENSIONS)

    def test_option_dimensions_are_subset(self):
        assert OPTION_DIMENSIONS.issubset(VALID_DIMENSIONS)

    def test_warrant_and_option_are_disjoint(self):
        assert WARRANT_DIMENSIONS.isdisjoint(OPTION_DIMENSIONS)

    def test_all_dimensions_covered(self):
        assert WARRANT_DIMENSIONS | OPTION_DIMENSIONS == VALID_DIMENSIONS


class TestExtractAnomaliesByDimension:
    def test_empty_input(self):
        result = _extract_anomalies_by_dimension([])
        assert result == {}

    def test_single_anomaly(self):
        data = [{"dimension": "option_unusual", "date": "2026-04-05", "description": "Large call trade"}]
        result = _extract_anomalies_by_dimension(data)
        assert "option_unusual" in result
        assert len(result["option_unusual"]) == 1
        assert result["option_unusual"][0]["anomaly_date"] == "2026-04-05"

    def test_multiple_dimensions(self):
        data = [
            {"dimension": "option_unusual", "date": "2026-04-05"},
            {"dimension": "option_volatility", "date": "2026-04-06"},
        ]
        result = _extract_anomalies_by_dimension(data)
        assert len(result) == 2

    def test_unknown_dimension(self):
        data = [{"dimension": "unknown", "date": "2026-04-05"}]
        result = _extract_anomalies_by_dimension(data)
        assert "unknown" in result


class TestBuildSummary:
    def test_no_anomalies(self):
        assert _build_summary({}) == "无异常"
        assert _build_summary({"option_unusual": []}) == "无异常"

    def test_with_anomalies(self):
        result = _build_summary({"option_unusual": [{"date": "2026-04-05"}]})
        assert "1" in result
        assert "异常" in result
