"""Crypto symbol normalisation (extracted from fetch_price_router.py)."""

CRYPTO_SYMBOLS = {"BTC", "ETH", "SOL", "DOGE", "XRP", "ADA", "AVAX", "DOT"}

CRYPTO_MAP_FINNHUB = {
    "BTC": "BINANCE:BTCUSDT",
    "ETH": "BINANCE:ETHUSDT",
    "SOL": "BINANCE:SOLUSDT",
    "DOGE": "BINANCE:DOGEUSDT",
    "XRP": "BINANCE:XRPUSDT",
    "ADA": "BINANCE:ADAUSDT",
    "AVAX": "BINANCE:AVAXUSDT",
    "DOT": "BINANCE:DOTUSDT",
}

CRYPTO_MAP_YAHOO = {
    "BTC": "BTC-USD",
    "ETH": "ETH-USD",
    "SOL": "SOL-USD",
    "DOGE": "DOGE-USD",
    "XRP": "XRP-USD",
    "ADA": "ADA-USD",
    "AVAX": "AVAX-USD",
    "DOT": "DOT-USD",
}


def is_crypto(symbol: str) -> bool:
    return symbol.upper() in CRYPTO_SYMBOLS


def normalize_for_source(symbol: str, source: str) -> str:
    """Convert bare crypto symbols to source-specific format. Non-crypto passes through."""
    upper = symbol.upper()
    if upper not in CRYPTO_SYMBOLS:
        return symbol
    if source == "finnhub":
        return CRYPTO_MAP_FINNHUB.get(upper, f"BINANCE:{upper}USDT")
    if source == "yahoo":
        return CRYPTO_MAP_YAHOO.get(upper, f"{upper}-USD")
    return symbol
