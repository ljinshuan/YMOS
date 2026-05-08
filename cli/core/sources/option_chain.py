"""Futu OpenD option chain data source."""

from __future__ import annotations

import datetime as dt
from typing import Any

# Option type constants
OPTION_TYPE_ALL = "ALL"
OPTION_TYPE_CALL = "CALL"
OPTION_TYPE_PUT = "PUT"

# Moneyness constants
MONEYNESS_ALL = "ALL"
MONEYNESS_ATM = "ATM"
MONEYNESS_OUTSIDE = "OUTSIDE"
MONEYNESS_WITHIN = "WITHIN"


def fetch_expiration_dates(ticker: str, host: str = "", port: int = 0) -> list[dict]:
    """Fetch option expiration dates via Futu OpenD.

    Args:
        ticker: YMOS ticker (e.g. "AAPL", "BABA").
        host: OpenD host (uses env var if empty).
        port: OpenD port (uses env var if 0).

    Returns:
        List of expiration dates with days to expiry.
    """
    from cli.core.futu_utils import create_quote_context, ticker_to_futu_symbol

    symbol = ticker_to_futu_symbol(ticker)

    try:
        import futu as ft
    except ImportError:
        return []

    quote_ctx = None
    try:
        quote_ctx = create_quote_context(host=host, port=port)
        ret, data = quote_ctx.get_option_expiration_date(symbol)

        if ret != ft.RET_OK or data is None or data.empty:
            return []

        results = []
        for _, row in data.iterrows():
            results.append({
                "strike_time": row.get("strike_time", ""),
                "option_expiry_date_distance": int(row.get("option_expiry_date_distance", 0)),
                "expiration_cycle": row.get("expiration_cycle", ""),
            })
        return results
    except Exception as e:
        return []
    finally:
        if quote_ctx:
            quote_ctx.close()


def fetch_option_chain_static(
    ticker: str,
    start: str | None = None,
    end: str | None = None,
    option_type: str = OPTION_TYPE_ALL,
    moneyness: str = MONEYNESS_ALL,
    host: str = "",
    port: int = 0,
) -> list[dict]:
    """Fetch option chain static data via Futu OpenD.

    Args:
        ticker: YMOS ticker.
        start: Start date (expiry date), e.g. "2026-05-08".
        end: End date (expiry date), e.g. "2026-05-15".
        option_type: ALL/CALL/PUT.
        moneyness: ALL/ATM/OUTSIDE/WITHIN.
        host: OpenD host.
        port: OpenD port.

    Returns:
        List of option contracts with static data.
    """
    from cli.core.futu_utils import create_quote_context, ticker_to_futu_symbol

    symbol = ticker_to_futu_symbol(ticker)

    try:
        import futu as ft
    except ImportError:
        return []

    quote_ctx = None
    try:
        quote_ctx = create_quote_context(host=host, port=port)

        # Map moneyness and option_type to Futu constants
        futu_option_type = _map_option_type(option_type)
        futu_moneyness = _map_moneyness(moneyness)

        ret, data = quote_ctx.get_option_chain(
            symbol,
            start=start,
            end=end,
            option_type=futu_option_type,
            option_cond_type=futu_moneyness,
        )

        if ret != ft.RET_OK or data is None or data.empty:
            return []

        results = []
        for _, row in data.iterrows():
            results.append({
                "code": row.get("code", ""),
                "name": row.get("name", ""),
                "option_type": row.get("option_type", ""),
                "strike_price": float(row.get("strike_price", 0)),
                "strike_time": row.get("strike_time", ""),
                "lot_size": int(row.get("lot_size", 0)),
                "suspension": bool(row.get("suspension", False)),
            })
        return results
    except Exception as e:
        return []
    finally:
        if quote_ctx:
            quote_ctx.close()


def fetch_option_quotes(
    option_codes: list[str],
    host: str = "",
    port: int = 0,
) -> list[dict]:
    """Fetch option live data via subscribe + get_market_snapshot.

    Args:
        option_codes: List of option codes (e.g. ["US.BABA260508C80000", ...]).
        host: OpenD host.
        port: OpenD port.

    Returns:
        List of option contracts with live data (price, IV, Greeks, OI).
    """
    from cli.core.futu_utils import create_quote_context

    try:
        import futu as ft
    except ImportError:
        return []

    if not option_codes:
        return []

    quote_ctx = None
    try:
        quote_ctx = create_quote_context(host=host, port=port)

        # Subscribe to quotes
        ret, _ = quote_ctx.subscribe(option_codes, [ft.SubType.QUOTE])
        if ret != ft.RET_OK:
            return []

        # Fetch market snapshot
        ret, data = quote_ctx.get_market_snapshot(option_codes)

        if ret != ft.RET_OK or data is None or data.empty:
            return []

        results = []
        for _, row in data.iterrows():
            results.append({
                "code": row.get("code", ""),
                "last_price": _safe_float(row.get("last_price")),
                "ask_price": _safe_float(row.get("ask_price")),
                "bid_price": _safe_float(row.get("bid_price")),
                "ask_vol": _safe_int(row.get("ask_vol")),
                "bid_vol": _safe_int(row.get("bid_vol")),
                "implied_volatility": _safe_float(row.get("option_implied_volatility")),
                "delta": _safe_float(row.get("option_delta")),
                "gamma": _safe_float(row.get("option_gamma")),
                "vega": _safe_float(row.get("option_vega")),
                "theta": _safe_float(row.get("option_theta")),
                "rho": _safe_float(row.get("option_rho")),
                "open_interest": _safe_int(row.get("option_open_interest")),
                "volume": _safe_int(row.get("volume")),
            })
        return results
    except Exception as e:
        return []
    finally:
        if quote_ctx:
            try:
                quote_ctx.unsubscribe(option_codes, [ft.SubType.QUOTE])
            except Exception:
                pass
            quote_ctx.close()


def build_derived_metrics(chain_data: list[dict], quotes_data: list[dict]) -> dict:
    """Calculate derived metrics from option chain and quotes.

    Args:
        chain_data: Static option chain data.
        quotes_data: Live option quote data.

    Returns:
        Dict with derived metrics: put_call_ratio, iv_stats.
    """
    if not chain_data or not quotes_data:
        return {"put_call_ratio": None, "iv_stats": None}

    # Create code -> quote mapping
    quotes_map = {q["code"]: q for q in quotes_data}

    # Separate calls and puts
    call_oi = 0
    put_oi = 0
    call_vol = 0
    put_vol = 0
    iv_values = []

    for contract in chain_data:
        code = contract["code"]
        quote = quotes_map.get(code)
        if not quote:
            continue

        opt_type = contract.get("option_type", "")
        oi = quote.get("open_interest", 0) or 0
        vol = quote.get("volume", 0) or 0
        iv = quote.get("implied_volatility")

        if opt_type == "CALL":
            call_oi += oi
            call_vol += vol
        elif opt_type == "PUT":
            put_oi += oi
            put_vol += vol

        if iv is not None and iv > 0:
            iv_values.append(iv)

    # Calculate PCR (Put/Call Ratio)
    pcr_oi = put_oi / call_oi if call_oi > 0 else None
    pcr_vol = put_vol / call_vol if call_vol > 0 else None

    # Calculate IV stats
    iv_stats = None
    if iv_values:
        iv_stats = {
            "min": min(iv_values),
            "max": max(iv_values),
            "median": sum(iv_values) / len(iv_values),
            "count": len(iv_values),
        }

    return {
        "put_call_ratio_oi": pcr_oi,
        "put_call_ratio_vol": pcr_vol,
        "iv_stats": iv_stats,
    }


def fetch_option_chain(
    ticker: str,
    start: str | None = None,
    end: str | None = None,
    option_type: str = OPTION_TYPE_ALL,
    moneyness: str = MONEYNESS_ALL,
    host: str = "",
    port: int = 0,
) -> dict:
    """Fetch complete option chain with static and live data.

    Args:
        ticker: YMOS ticker.
        start: Start date for expiry filtering.
        end: End date for expiry filtering.
        option_type: ALL/CALL/PUT.
        moneyness: ALL/ATM/OUTSIDE/WITHIN.
        host: OpenD host.
        port: OpenD port.

    Returns:
        Dict with standardized output schema.
    """
    from cli.core.futu_utils import check_opend_connection

    # Check OpenD connection
    if not check_opend_connection(host, port):
        return _error_result(ticker, "OpenD 未连接")

    # Fetch static chain data
    chain_data = fetch_option_chain_static(
        ticker, start, end, option_type, moneyness, host, port
    )

    if not chain_data:
        return _error_result(ticker, "未找到期权合约")

    # Extract option codes for live data fetch
    option_codes = [c["code"] for c in chain_data]

    # Fetch live quotes
    quotes_data = fetch_option_quotes(option_codes, host, port)

    # Build derived metrics
    derived_metrics = build_derived_metrics(chain_data, quotes_data)

    # Merge static and live data
    quotes_map = {q["code"]: q for q in quotes_data}
    contracts = []
    for contract in chain_data:
        code = contract["code"]
        quote = quotes_map.get(code, {})
        merged = {**contract, **quote}
        contracts.append(merged)

    # Fetch expiration dates
    expiry_dates = fetch_expiration_dates(ticker, host, port)

    return {
        "ticker": ticker,
        "market": _detect_market(ticker),
        "source": "futu_opend",
        "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "expiry_dates": expiry_dates,
        "contracts": contracts,
        "derived_metrics": derived_metrics,
    }


def _map_option_type(option_type: str) -> Any:
    """Map option type string to Futu constant."""
    try:
        import futu as ft
        mapping = {
            OPTION_TYPE_ALL: ft.OptionType.ALL,
            OPTION_TYPE_CALL: ft.OptionType.CALL,
            OPTION_TYPE_PUT: ft.OptionType.PUT,
        }
        return mapping.get(option_type, ft.OptionType.ALL)
    except ImportError:
        return None


def _map_moneyness(moneyness: str) -> Any:
    """Map moneyness string to Futu constant."""
    try:
        import futu as ft
        mapping = {
            MONEYNESS_ALL: ft.OptionCondType.ALL,
            MONEYNESS_ATM: ft.OptionCondType.WITHIN,  # Futu doesn't have ATM, use WITHIN
            MONEYNESS_OUTSIDE: ft.OptionCondType.OUTSIDE,
            MONEYNESS_WITHIN: ft.OptionCondType.WITHIN,
        }
        return mapping.get(moneyness, ft.OptionCondType.ALL)
    except ImportError:
        return None


def _detect_market(ticker: str) -> str:
    """Detect market from ticker suffix."""
    if "." in ticker:
        _, suffix = ticker.rsplit(".", 1)
        if suffix.upper() in ("SS", "SZ"):
            return "CN"
        if suffix.upper() == "HK":
            return "HK"
    return "US"


def _safe_float(value: Any) -> float | None:
    """Safely convert to float."""
    try:
        if value is None or value == "":
            return None
        return float(value)
    except (ValueError, TypeError):
        return None


def _safe_int(value: Any) -> int | None:
    """Safely convert to int."""
    try:
        if value is None or value == "":
            return None
        return int(value)
    except (ValueError, TypeError):
        return None


def _error_result(ticker: str, error: str) -> dict:
    """Return error result dict."""
    return {
        "ticker": ticker,
        "market": _detect_market(ticker),
        "source": "none",
        "error": error,
        "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "contracts": [],
        "derived_metrics": None,
    }
