"""Shared Futu OpenD utilities — connection check, ticker conversion, startup guide.

Used by: capital_flow, screener, tech (futu source), position commands.
"""

from __future__ import annotations

import socket

OPEND_STARTUP_GUIDE = """
Futu OpenD 未运行或不可连接。请按以下步骤操作：

1. 打开富途牛牛客户端（或独立的 FutuOpenD）
2. 确保菜单「更多 → Futu OpenD」已开启，监听端口 11111
3. 如端口被修改，设置环境变量 FUTU_OPEND_PORT=端口号
4. 等待 OpenD 状态变为「已连接」后重试
"""


def check_opend_connection(host: str = "127.0.0.1", port: int = 11111) -> bool:
    """Check if Futu OpenD is reachable on the given host:port."""
    try:
        with socket.create_connection((host, port), timeout=3):
            return True
    except (ConnectionRefusedError, OSError, TimeoutError):
        return False


def ticker_to_futu_symbol(ticker: str) -> str:
    """Convert YMOS ticker to Futu standard symbol format.

    YMOS: 0700.HK, AAPL, 688008.SS, 000001.SZ
    Futu: HK.00700, US.AAPL, SH.688008, SZ.000001
    """
    if "." in ticker:
        base, suffix = ticker.rsplit(".", 1)
        mapping = {"HK": "HK", "SS": "SH", "SZ": "SZ"}
        market = mapping.get(suffix.upper(), "US")
        if market == "HK":
            return f"HK.{base.zfill(5)}"
        return f"{market}.{base}"
    return f"US.{ticker}"


def futu_symbol_to_ticker(symbol: str) -> str:
    """Convert Futu standard symbol back to YMOS ticker format.

    Futu: HK.00700, US.AAPL, SH.688008, SZ.000001
    YMOS: 0700.HK, AAPL, 688008.SS, 000001.SZ
    """
    if "." not in symbol:
        return symbol
    market, code = symbol.split(".", 1)
    reverse = {"SH": "SS", "SZ": "SZ", "HK": "HK"}
    suffix = reverse.get(market, None)
    if suffix == "HK":
        # Futu uses 5-digit codes (00700), YMOS uses 4-digit (0700)
        stripped = code.lstrip("0") or "0"
        return f"{stripped.zfill(4)}.{suffix}"
    if suffix in ("SS", "SZ"):
        return f"{code}.{suffix}"
    # US and others — no suffix
    return code
