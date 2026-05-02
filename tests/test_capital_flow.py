"""Tests for cli.commands.capital_flow — enhanced anomaly detection."""

from cli.commands.capital_flow import _detect_enhanced_anomalies


class TestDetectEnhancedAnomalies:
    def test_empty_data(self):
        result = _detect_enhanced_anomalies([], "HK")
        assert result["short_sell_anomaly"] is None
        assert result["broker_anomaly"] is None

    def test_short_sell_anomaly(self):
        data = [
            {"dimension": "short_sell_number", "date": "2026-04-05", "description": "卖空数量异动"},
            {"dimension": "short_sell_ratio", "date": "2026-04-05", "description": "卖空比例异动"},
        ]
        result = _detect_enhanced_anomalies(data, "HK")
        assert result["short_sell_anomaly"] is not None
        assert len(result["short_sell_anomaly"]) == 2

    def test_broker_anomaly(self):
        data = [
            {"dimension": "funds_broker", "date": "2026-04-05", "description": "买入排名前二：中国投资（沪港通）"},
        ]
        result = _detect_enhanced_anomalies(data, "HK")
        assert result["broker_anomaly"] is not None
        assert len(result["broker_anomaly"]) == 1
        assert result["broker_anomaly"][0]["cross_border"] is True

    def test_no_cross_border_broker(self):
        data = [
            {"dimension": "funds_broker", "date": "2026-04-05", "description": "买入排名：富途证券"},
        ]
        result = _detect_enhanced_anomalies(data, "US")
        assert result["broker_anomaly"] is not None
        assert result["broker_anomaly"][0]["cross_border"] is False

    def test_non_dict_items_skipped(self):
        data = ["not a dict"]
        result = _detect_enhanced_anomalies(data, "HK")
        assert result["short_sell_anomaly"] is None
        assert result["broker_anomaly"] is None

    def test_combined_short_sell_flag(self):
        data = [
            {"dimension": "short_sell_number_and_ratio", "date": "2026-04-05", "description": "卖空数量和比例同时异动"},
        ]
        result = _detect_enhanced_anomalies(data, "HK")
        assert result["short_sell_anomaly"] is not None
        assert result["short_sell_anomaly"][0]["combined"] is True
