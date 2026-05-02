"""Tests for cli.commands.sentiment — group aggregation and label logic."""

from cli.commands.sentiment import _compute_group_aggregation, _determine_label


class TestDetermineLabel:
    def test_bullish(self):
        assert _determine_label(65, 20, 15) == "bullish"

    def test_bearish(self):
        assert _determine_label(20, 60, 20) == "bearish"

    def test_neutral(self):
        assert _determine_label(20, 15, 65) == "neutral"

    def test_mixed_within_15pct(self):
        assert _determine_label(40, 35, 25) == "mixed"

    def test_mixed_exact_threshold(self):
        assert _determine_label(40, 26, 34) == "mixed"

    def test_not_mixed_bull_dominates(self):
        assert _determine_label(55, 35, 10) == "bullish"

    def test_not_mixed_bear_dominates(self):
        assert _determine_label(35, 55, 10) == "bearish"


class TestComputeGroupAggregation:
    def test_single_symbol_returns_none(self):
        symbols = [{"ticker": "AAPL", "post_count": 10, "bull_pct": "60%", "bear_pct": "25%", "neutral_pct": "15%"}]
        assert _compute_group_aggregation(symbols) is None

    def test_multi_symbol_returns_group(self):
        symbols = [
            {"ticker": "AAPL", "post_count": 100, "bull_pct": "60%", "bear_pct": "25%", "neutral_pct": "15%"},
            {"ticker": "NVDA", "post_count": 200, "bull_pct": "70%", "bear_pct": "20%", "neutral_pct": "10%"},
        ]
        result = _compute_group_aggregation(symbols)
        assert result is not None
        assert "label" in result
        assert result["post_count"] == 300
        assert "bull_pct" in result
        assert "bear_pct" in result

    def test_all_empty_returns_neutral(self):
        symbols = [
            {"ticker": "AAPL", "post_count": 0, "bull_pct": "0%", "bear_pct": "0%", "neutral_pct": "0%"},
            {"ticker": "NVDA", "post_count": 0, "bull_pct": "0%", "bear_pct": "0%", "neutral_pct": "0%"},
        ]
        result = _compute_group_aggregation(symbols)
        assert result["label"] == "neutral"
        assert result["post_count"] == 0

    def test_driving_symbols_detected(self):
        symbols = [
            {"ticker": "AAPL", "post_count": 100, "bull_pct": "60%", "bear_pct": "25%", "neutral_pct": "15%"},
            {"ticker": "TSLA", "post_count": 100, "bull_pct": "20%", "bear_pct": "60%", "neutral_pct": "20%"},
        ]
        result = _compute_group_aggregation(symbols)
        # TSLA should be a driving symbol since its bull/bear diverges significantly from group avg
        assert result["driving_symbols"] is not None
