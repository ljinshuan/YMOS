"""Futu OpenD technical anomaly data source."""

from __future__ import annotations

import datetime as dt


def fetch_technical_anomaly(
    ticker: str,
    time_range: int = 7,
    indicator_filters: list[str] | None = None,
    language_id: int = 0,
) -> dict:
    """Fetch technical anomaly data via Futu OpenD get_technical_unusual.

    Args:
        ticker: YMOS ticker (e.g. "0700.HK", "AAPL").
        time_range: Natural day window (default 7).
        indicator_filters: Optional list of indicator names to filter.
        language_id: 0=zh-CN, 1=zh-TW, 2=en.

    Returns:
        Dict with standardized output schema.
    """
    from cli.core.futu_utils import create_quote_context, ticker_to_futu_symbol

    symbol = ticker_to_futu_symbol(ticker)

    try:
        import futu as ft
    except ImportError:
        return _error_result(ticker, symbol, "futu-api SDK not installed. Run: uv add futu-api")

    try:
        quote_ctx = create_quote_context()
        try:
            ret, data = quote_ctx.get_technical_unusual(
                symbol,
                time_range=time_range,
                indicator_filters=indicator_filters or None,
                language_id=language_id,
            )
        finally:
            quote_ctx.close()
    except Exception as e:
        return _error_result(ticker, symbol, f"OpenD connection failed: {e}")

    if ret != ft.RET_OK:
        return _error_result(ticker, symbol, str(data))

    normalized = _normalize_data(data)

    start_date = (dt.datetime.now() - dt.timedelta(days=time_range)).strftime("%Y-%m-%d")
    end_date = dt.datetime.now().strftime("%Y-%m-%d")

    anomalies = _extract_anomalies(normalized)

    return {
        "ticker": ticker,
        "symbol": symbol,
        "source": "futu_opend",
        "method": "get_technical_unusual",
        "time_range": {"start_date": start_date, "end_date": end_date, "days": time_range},
        "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "anomalies": anomalies,
        "summary": "无异常" if not anomalies else f"检测到 {len(anomalies)} 个异常信号",
        "raw_data": normalized,
    }


def _normalize_data(data) -> list | dict:
    if hasattr(data, "to_dict"):
        try:
            return data.to_dict(orient="records")
        except TypeError:
            return data.to_dict()
    if isinstance(data, dict):
        return data
    return data if isinstance(data, list) else []


def _extract_anomalies(normalized: list | dict) -> list[dict]:
    """Extract structured anomaly items from raw OpenD data."""
    items = normalized if isinstance(normalized, list) else [normalized] if normalized else []
    anomalies = []
    for item in items:
        if not isinstance(item, dict):
            continue
        anomalies.append({
            "date": item.get("date", item.get("time_key", "")),
            "indicator": item.get("indicator", item.get("indicator_name", "")),
            "signal_direction": item.get("signal_direction", item.get("direction", "")),
            "description": item.get("description", item.get("desc", "")),
            "support": item.get("support"),
            "resistance": item.get("resistance"),
            "probability": item.get("probability"),
        })
    return anomalies


def _error_result(ticker: str, symbol: str, error: str) -> dict:
    return {
        "ticker": ticker,
        "symbol": symbol,
        "source": "none",
        "error": error,
        "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "anomalies": [],
        "summary": f"获取失败: {error}",
    }
