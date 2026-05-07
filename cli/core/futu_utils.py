"""Shared Futu OpenD utilities — connection factory, encryption, ticker conversion.

Used by: capital_flow, screener, tech (futu source), position commands.
"""

from __future__ import annotations

import os
import socket

OPEND_STARTUP_GUIDE = """
Futu OpenD 未运行或不可连接。请按以下步骤操作：

1. 打开富途牛牛客户端（或独立的 FutuOpenD）
2. 确保菜单「更多 → Futu OpenD」已开启，监听端口 11111
3. 如端口被修改，设置环境变量 FUTU_OPEND_PORT=端口号
4. 远程部署时，设置 FUTU_OPEND_HOST=远端IP 并配置 FUTU_OPEND_RSA_KEY
5. 等待 OpenD 状态变为「已连接」后重试
"""


def _is_remote_host(host: str) -> bool:
    return host not in ("", "127.0.0.1", "localhost")


def _resolve_opend_addr(host: str = "", port: int = 0) -> tuple[str, int]:
    host = host or os.getenv("FUTU_OPEND_HOST", "127.0.0.1")
    port = port or int(os.getenv("FUTU_OPEND_PORT", "11111"))
    return host, port


def _setup_encryption(host: str) -> None:
    if not _is_remote_host(host):
        return

    import futu as ft

    key_path = os.getenv("FUTU_OPEND_RSA_KEY", "").strip()
    if not key_path:
        print("⚠️  远程 Futu OpenD 连接未配置 FUTU_OPEND_RSA_KEY，可能连接失败")

    ft.SysConfig.enable_proto_encrypt(is_encrypt=True)
    if key_path:
        ft.SysConfig.set_init_rsa_file(key_path)


def check_opend_connection(host: str = "", port: int = 0) -> bool:
    """Check if Futu OpenD is reachable on the given host:port."""
    host, port = _resolve_opend_addr(host, port)
    try:
        with socket.create_connection((host, port), timeout=3):
            return True
    except (ConnectionRefusedError, OSError, TimeoutError):
        return False


def create_quote_context(host: str = "", port: int = 0):
    """Create an OpenQuoteContext with auto encryption for remote hosts."""
    import futu as ft

    host, port = _resolve_opend_addr(host, port)
    _setup_encryption(host)
    return ft.OpenQuoteContext(host=host, port=port)


def create_trade_context(host: str = "", port: int = 0):
    """Create an OpenSecTradeContext with auto encryption for remote hosts."""
    import futu as ft

    host, port = _resolve_opend_addr(host, port)
    _setup_encryption(host)
    return ft.OpenSecTradeContext(host=host, port=port)


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
