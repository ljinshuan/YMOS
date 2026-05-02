"""Futu OpenD deal history data source — fetch trade records via history_deal_list_query.

Used by: cli/commands/trade_history.py
"""

from __future__ import annotations

from cli.core.futu_utils import futu_symbol_to_ticker, ticker_to_futu_symbol


def fetch_deals(
    host: str = "127.0.0.1",
    port: int = 11111,
    start_date: str = "",
    end_date: str = "",
    ticker: str | None = None,
) -> list[dict] | None:
    """Fetch historical deal records from Futu OpenD.

    Uses OpenSecTradeContext.history_deal_list_query() to retrieve trade records.

    Args:
        host: OpenD host
        port: OpenD port
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        ticker: Optional YMOS ticker to filter (e.g., AAPL, 0700.HK)

    Returns:
        list[dict]: normalized deal dicts (empty list if no deals)
        None: if OpenD is not reachable or user not logged in
    """
    try:
        import futu as ft
    except ImportError:
        print("futu-api SDK not installed. Run: uv add futu-api")
        return None

    code = ""
    if ticker:
        code = ticker_to_futu_symbol(ticker)

    try:
        trd_ctx = ft.OpenSecTradeContext(host=host, port=port)
        try:
            ret, data = trd_ctx.history_deal_list_query(
                code=code, start=start_date, end=end_date
            )
        finally:
            trd_ctx.close()

        if ret != ft.RET_OK:
            error_msg = str(data)
            if "not logged" in error_msg.lower() or "未登录" in error_msg:
                print("请先在富途牛牛客户端登录账户")
                return None
            print(f"获取成交记录失败: {error_msg}")
            return None

        if data is None or (hasattr(data, "empty") and data.empty):
            return []

        return _normalize_deals(data)

    except Exception as e:
        error_str = str(e)
        if "Connection" in error_str or "connect" in error_str.lower() or "refused" in error_str.lower():
            return None
        print(f"OpenD 连接失败: {e}")
        return None


_MARKET_CURRENCY = {"HK": "HKD", "US": "USD", "SH": "CNY", "SZ": "CNY"}


def _normalize_deals(df) -> list[dict]:
    """Convert Futu history_deal_list_query DataFrame to standardized deal dicts."""
    deals = []
    for _, row in df.iterrows():
        code = str(row.get("code", ""))
        ticker = futu_symbol_to_ticker(code)
        market = str(row.get("deal_market", ""))
        deals.append({
            "ticker": ticker,
            "name": str(row.get("stock_name", "")),
            "side": str(row.get("trd_side", "")),
            "price": float(row.get("price", 0)),
            "quantity": float(row.get("qty", 0)),
            "timestamp": str(row.get("create_time", "")),
            "fee": 0.0,
            "currency": _MARKET_CURRENCY.get(market, ""),
        })

    return deals
