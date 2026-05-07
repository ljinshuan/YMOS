"""Futu OpenD extended quotes — pre-market, after-hours, overnight data."""

from __future__ import annotations

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from cli.core.futu_utils import check_opend_connection, create_quote_context, ticker_to_futu_symbol

ET = ZoneInfo("America/New_York")

# US market sessions (Eastern Time)
PRE_MARKET_OPEN = 4, 0      # 04:00 ET
REGULAR_OPEN = 9, 30         # 09:30 ET
REGULAR_CLOSE = 16, 0        # 16:00 ET
AFTER_HOURS_CLOSE = 20, 0    # 20:00 ET

SESSION_LABELS = {
    "pre_market": "盘前",
    "regular": "盘中",
    "after_hours": "盘后",
    "overnight": "夜盘",
    "closed": "休市",
}


def detect_us_session() -> str:
    """Detect current US market session based on Eastern Time.

    Returns one of: 'pre_market', 'regular', 'after_hours', 'overnight'.
    """
    now_et = datetime.now(ET)
    t = now_et.hour * 100 + now_et.minute  # HHMM as integer for comparison

    pre_open = PRE_MARKET_OPEN[0] * 100 + PRE_MARKET_OPEN[1]     # 400
    reg_open = REGULAR_OPEN[0] * 100 + REGULAR_OPEN[1]           # 930
    reg_close = REGULAR_CLOSE[0] * 100 + REGULAR_CLOSE[1]        # 1600
    ah_close = AFTER_HOURS_CLOSE[0] * 100 + AFTER_HOURS_CLOSE[1] # 2000

    if t >= reg_open and t < reg_close:
        return "regular"
    if t >= pre_open and t < reg_open:
        return "pre_market"
    if t >= reg_close and t < ah_close:
        return "after_hours"
    return "overnight"


def session_label(session: str | None = None) -> str:
    s = session or detect_us_session()
    return SESSION_LABELS.get(s, s)


def _safe_float(val) -> float | None:
    try:
        if val is None:
            return None
        return float(val)
    except (ValueError, TypeError):
        return None


def _extract_row(df, idx: int = 0) -> dict | None:
    """Extract extended quote data from a snapshot DataFrame row."""
    try:
        import futu as ft
    except ImportError:
        return None

    row = df.iloc[idx]
    ticker = row.get("code", "")

    from cli.core.futu_utils import futu_symbol_to_ticker
    ticker = futu_symbol_to_ticker(ticker)

    def _section(prefix: str) -> dict | None:
        price = _safe_float(row.get(f"{prefix}_price"))
        if price is None or price == 0:
            return None
        return {
            "price": price,
            "high": _safe_float(row.get(f"{prefix}_high_price")),
            "low": _safe_float(row.get(f"{prefix}_low_price")),
            "volume": _safe_float(row.get(f"{prefix}_volume")),
            "change": _safe_float(row.get(f"{prefix}_change_val")),
            "change_pct": _safe_float(row.get(f"{prefix}_change_rate")),
            "amplitude": _safe_float(row.get(f"{prefix}_amplitude")),
        }

    overnight = _section("overnight")
    if overnight and _safe_float(row.get("overnight_turnover")):
        overnight["turnover"] = _safe_float(row.get("overnight_turnover"))

    return {
        "ticker": ticker,
        "source": "Futu OpenD",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "last_price": _safe_float(row.get("last_price")),
        "open_price": _safe_float(row.get("open_price")),
        "high_price": _safe_float(row.get("high_price")),
        "low_price": _safe_float(row.get("low_price")),
        "prev_close": _safe_float(row.get("prev_close_price")),
        "volume": _safe_float(row.get("volume")),
        "avg_price": _safe_float(row.get("avg_price")),
        "pre_market": _section("pre"),
        "after_hours": _section("after"),
        "overnight": overnight,
    }


def fetch_extended_quotes(
    tickers: list[str],
    host: str = "",
    port: int = 0,
) -> list[dict]:
    """Fetch extended quotes (pre-market, after-hours, overnight) via Futu OpenD.

    Returns list of quote dicts. Returns empty list if OpenD is unavailable.
    """
    try:
        import futu as ft
    except ImportError:
        print("⚠️  futu-api not installed, skipping extended quotes")
        return []

    if not check_opend_connection(host, port):
        print("⚠️  Futu OpenD not reachable, skipping extended quotes")
        return []

    us_tickers = [t for t in tickers if not t.endswith((".SS", ".SZ"))]
    if not us_tickers:
        return []

    symbols = [ticker_to_futu_symbol(t) for t in us_tickers]

    try:
        quote_ctx = create_quote_context(host=host, port=port)
        try:
            ret, data = quote_ctx.get_market_snapshot(symbols)
        finally:
            quote_ctx.close()
    except Exception as e:
        print(f"⚠️  Futu get_market_snapshot failed: {e}")
        return []

    if ret != ft.RET_OK:
        print(f"⚠️  Futu get_market_snapshot error: {data}")
        return []

    if data is None or data.empty:
        return []

    results = []
    for i in range(len(data)):
        item = _extract_row(data, i)
        if item:
            results.append(item)

    return results


def _fmt_session(name: str, data: dict) -> str:
    """Format one session line: 价格 (涨跌%) H高 L低."""
    pct = data.get("change_pct") or 0
    price = data.get("price", 0)
    parts = [f"${price:.2f} ({pct:+.2f}%)"]
    if data.get("high"):
        parts.append(f"H ${data['high']:.2f}")
    if data.get("low"):
        parts.append(f"L ${data['low']:.2f}")
    return f"{name} {'  '.join(parts)}"


def _fmt_regular(q: dict) -> str:
    """Format regular session quote from top-level Futu snapshot data."""
    price = q.get("last_price") or 0
    prev = q.get("prev_close") or 0
    pct = ((price - prev) / prev * 100) if prev else 0
    parts = [f"盘中 ${price:.2f} ({pct:+.2f}%)"]
    if q.get("high_price"):
        parts.append(f"H ${q['high_price']:.2f}")
    if q.get("low_price"):
        parts.append(f"L ${q['low_price']:.2f}")
    return "  ".join(parts)


def print_extended_summary(quotes: list[dict], session: str | None = None) -> None:
    """Print a compact summary, auto-highlighting the current session."""
    if not quotes:
        return

    cur = session or detect_us_session()
    label = session_label(cur)

    session_key_map = {
        "pre_market": ("pre_market", ["overnight"]),
        "regular": (None, []),
        "after_hours": ("after_hours", ["overnight"]),
        "overnight": ("overnight", ["pre_market"]),
    }

    primary_key, secondary_keys = session_key_map.get(cur, (None, []))

    print()
    print(f"📊 {label}行情 (Futu OpenD):")

    for q in quotes:
        ticker = q["ticker"]
        parts = []

        if cur == "regular":
            parts.append(_fmt_regular(q))
            for key in ["pre_market", "after_hours", "overnight"]:
                if q.get(key):
                    parts.append(_fmt_session(session_label(key), q[key]))
            prefix = f"   ➡️ {ticker:6s}"
        else:
            if primary_key and q.get(primary_key):
                pm = q[primary_key]
                pct = pm.get("change_pct") or 0
                icon = "🟢" if pct > 0 else "🔴" if pct < 0 else "➡️"
                parts.append(_fmt_session(label, pm))
                prefix = f"   {icon} {ticker:6s}"
            else:
                prefix = f"   ➡️ {ticker:6s}"

            for sk in secondary_keys:
                if q.get(sk):
                    parts.append(_fmt_session(session_label(sk), q[sk]))

        if parts:
            print(f"{prefix} {'  |  '.join(parts)}")
