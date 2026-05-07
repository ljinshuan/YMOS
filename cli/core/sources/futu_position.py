"""Futu OpenD position data source — fetch real holdings via position_list_query.

Used by: cli/commands/position.py
"""

from __future__ import annotations

from cli.core.futu_utils import create_trade_context, futu_symbol_to_ticker


def fetch_positions(host: str = "", port: int = 0) -> list[dict] | None:
    """Fetch current stock positions from Futu OpenD.

    Uses OpenSecTradeContext.position_list_query() to retrieve real holdings.

    Returns:
        list[dict]: normalized position dicts (empty list if no positions)
        None: if OpenD is not reachable or user not logged in
    """
    try:
        import futu as ft
    except ImportError:
        print("futu-api SDK not installed. Run: uv add futu-api")
        return None

    try:
        trd_ctx = create_trade_context(host=host, port=port)
        try:
            ret, data = trd_ctx.position_list_query()
        finally:
            trd_ctx.close()

        if ret != ft.RET_OK:
            error_msg = str(data)
            if "not logged" in error_msg.lower() or "未登录" in error_msg:
                print("请先在富途牛牛客户端登录账户")
                return None
            print(f"获取持仓失败: {error_msg}")
            return None

        if data is None or (hasattr(data, "empty") and data.empty):
            return []

        return _normalize_positions(data)

    except Exception as e:
        error_str = str(e)
        if "Connection" in error_str or "connect" in error_str.lower() or "refused" in error_str.lower():
            return None
        print(f"OpenD 连接失败: {e}")
        return None


def _normalize_positions(df) -> list[dict]:
    """Convert Futu position_list_query DataFrame to standardized position dicts."""
    positions = []
    for _, row in df.iterrows():
        ticker = futu_symbol_to_ticker(str(row.get("code", "")))
        quantity = float(row.get("qty", 0))
        cost_price = float(row.get("cost_price", 0))
        current_price = float(row.get("nominal_price", 0))
        market_value = float(row.get("market_val", 0))
        profit_loss = float(row.get("pl_val", 0))
        profit_loss_pct = float(row.get("pl_ratio", 0))

        positions.append({
            "ticker": ticker,
            "name": str(row.get("stock_name", "")),
            "quantity": quantity,
            "cost_price": cost_price,
            "current_price": current_price,
            "market_value": market_value,
            "profit_loss": profit_loss,
            "profit_loss_pct": profit_loss_pct,
            "currency": str(row.get("currency", "")),
        })

    return positions
