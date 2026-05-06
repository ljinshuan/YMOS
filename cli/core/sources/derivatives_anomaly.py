"""Futu OpenD derivatives anomaly data source."""

from __future__ import annotations

import datetime as dt


# Valid analysis dimensions for get_derivative_unusual
VALID_DIMENSIONS = {
    "warrant_ratio",
    "warrant_price_distribution",
    "option_unusual",
    "option_volatility",
    "option_volume_price",
    "option_sentiment",
    "option_comprehensive",
}

# Warrant dimensions only apply to HK stocks
WARRANT_DIMENSIONS = {"warrant_ratio", "warrant_price_distribution"}

# All option-related dimensions
OPTION_DIMENSIONS = VALID_DIMENSIONS - WARRANT_DIMENSIONS


def fetch_derivatives_anomaly(
    ticker: str,
    time_range: int = 7,
    analysis_dimensions: list[str] | None = None,
    language_id: int = 0,
) -> dict:
    """Fetch derivatives anomaly data via Futu OpenD get_derivative_unusual.

    Args:
        ticker: YMOS ticker (e.g. "0700.HK", "AAPL").
        time_range: Natural day window (default 7).
        analysis_dimensions: Optional list of dimensions to filter.
        language_id: 0=zh-CN, 1=zh-TW, 2=en.

    Returns:
        Dict with standardized output schema.
    """
    from cli.core.futu_utils import create_quote_context, ticker_to_futu_symbol

    symbol = ticker_to_futu_symbol(ticker)
    market = _detect_market(ticker)

    # Filter warrant dimensions for non-HK stocks
    effective_dimensions = analysis_dimensions
    if analysis_dimensions and market != "HK":
        effective_dimensions = [d for d in analysis_dimensions if d not in WARRANT_DIMENSIONS]
        if not effective_dimensions:
            effective_dimensions = list(OPTION_DIMENSIONS)

    try:
        import futu as ft
    except ImportError:
        return _error_result(ticker, symbol, market, "futu-api SDK not installed. Run: uv add futu-api")

    try:
        quote_ctx = create_quote_context()
        try:
            ret, data = quote_ctx.get_derivative_unusual(
                symbol,
                time_range=time_range,
                analysis_dimensions=effective_dimensions or None,
                language_id=language_id,
            )
        finally:
            quote_ctx.close()
    except Exception as e:
        return _error_result(ticker, symbol, market, f"OpenD connection failed: {e}")

    if ret != ft.RET_OK:
        return _error_result(ticker, symbol, market, str(data))

    normalized = _normalize_data(data)

    start_date = (dt.datetime.now() - dt.timedelta(days=time_range)).strftime("%Y-%m-%d")
    end_date = dt.datetime.now().strftime("%Y-%m-%d")

    anomalies_by_dim = _extract_anomalies_by_dimension(normalized)

    return {
        "ticker": ticker,
        "symbol": symbol,
        "market": market,
        "source": "futu_opend",
        "method": "get_derivative_unusual",
        "time_range": {"start_date": start_date, "end_date": end_date, "days": time_range},
        "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "dimensions_requested": effective_dimensions or list(VALID_DIMENSIONS),
        "anomalies_by_dimension": anomalies_by_dim,
        "summary": _build_summary(anomalies_by_dim),
        "raw_data": normalized,
    }


def _detect_market(ticker: str) -> str:
    if "." in ticker:
        _, suffix = ticker.rsplit(".", 1)
        if suffix.upper() in ("SS", "SZ"):
            return "CN"
        if suffix.upper() == "HK":
            return "HK"
    return "US"


def _normalize_data(data) -> list | dict:
    if hasattr(data, "to_dict"):
        try:
            return data.to_dict(orient="records")
        except TypeError:
            return data.to_dict()
    if isinstance(data, dict):
        return data
    return data if isinstance(data, list) else []


def _extract_anomalies_by_dimension(normalized: list | dict) -> dict[str, list[dict]]:
    """Group anomaly items by dimension."""
    items = normalized if isinstance(normalized, list) else [normalized] if normalized else []
    by_dim: dict[str, list[dict]] = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        dim = item.get("dimension", item.get("analysis_dimension", "unknown"))
        entry = {
            "anomaly_date": item.get("date", item.get("time_key", "")),
            "description": item.get("description", item.get("desc", "")),
            "direction": item.get("direction", item.get("signal_direction", "")),
            "metrics": {k: v for k, v in item.items() if k not in ("dimension", "analysis_dimension")},
        }
        by_dim.setdefault(dim, []).append(entry)
    return by_dim


def _build_summary(anomalies_by_dim: dict) -> str:
    has_anomaly = any(v for v in anomalies_by_dim.values())
    if not has_anomaly:
        return "无异常"
    dim_count = sum(1 for v in anomalies_by_dim.values() if v)
    return f"检测到 {dim_count} 个维度有异常信号"


def _error_result(ticker: str, symbol: str, market: str, error: str) -> dict:
    return {
        "ticker": ticker,
        "symbol": symbol,
        "market": market,
        "source": "none",
        "error": error,
        "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "anomalies_by_dimension": {},
        "summary": f"获取失败: {error}",
    }
