"""Tushare A-share data source (migrated from fetch_price_tushare.py).

Zero third-party dependencies. Uses urllib + json stdlib only.
"""

from __future__ import annotations

import json
import urllib.request
from datetime import datetime, timedelta, timezone

TUSHARE_API_URL = "http://api.tushare.pro"


def to_tushare_code(ticker: str) -> str | None:
    """Convert state-machine ticker to Tushare ts_code. Returns None for non-A-shares."""
    t = ticker.strip().upper()
    if t.endswith(".SS"):
        return t[:-3] + ".SH"
    if t.endswith(".SH") or t.endswith(".SZ"):
        return t
    return None


def from_tushare_code(ts_code: str) -> str:
    """Tushare ts_code → state-machine ticker (reverse mapping)."""
    if ts_code.endswith(".SH"):
        return ts_code[:-3] + ".SS"
    return ts_code


def _tushare_post(api_name: str, token: str, params: dict, fields: str) -> dict:
    payload = json.dumps({
        "api_name": api_name, "token": token,
        "params": params, "fields": fields,
    }).encode("utf-8")
    req = urllib.request.Request(
        TUSHARE_API_URL, data=payload,
        headers={"Content-Type": "application/json"}, method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"code": -1, "msg": str(e), "data": None}


def fetch_daily(ts_codes: list[str], token: str,
                trade_date: str | None = None,
                start_date: str | None = None,
                end_date: str | None = None) -> list[dict]:
    """Batch-fetch A-share daily prices. Returns latest record per symbol."""
    params: dict = {"ts_code": ",".join(ts_codes)}
    if trade_date:
        params["trade_date"] = trade_date
    elif start_date and end_date:
        params["start_date"] = start_date
        params["end_date"] = end_date
    else:
        today = datetime.now(timezone.utc)
        params["start_date"] = (today - timedelta(days=7)).strftime("%Y%m%d")
        params["end_date"] = today.strftime("%Y%m%d")

    result = _tushare_post(
        "daily", token, params,
        "ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount",
    )
    if result.get("code") != 0:
        print(f"  ❌ Tushare API error: {result.get('msg')}")
        return []

    raw_items = result["data"].get("items", [])
    raw_fields = result["data"].get("fields", [])

    latest: dict[str, dict] = {}
    for row in raw_items:
        d = dict(zip(raw_fields, row))
        code = d["ts_code"]
        if code not in latest:
            latest[code] = d
    return list(latest.values())


def format_result(ts_code: str, row: dict | None) -> dict:
    """Unified output format aligned with Yahoo source."""
    original_ticker = from_tushare_code(ts_code)
    if row is None:
        return {"symbol": original_ticker, "ts_code": ts_code, "ok": False, "error": "no_data"}
    return {
        "symbol": original_ticker, "ts_code": ts_code, "ok": True,
        "trade_date": row.get("trade_date", ""),
        "last_close": float(row.get("close") or 0),
        "last_open": float(row.get("open") or 0),
        "last_high": float(row.get("high") or 0),
        "last_low": float(row.get("low") or 0),
        "last_volume": float(row.get("vol") or 0),
        "pre_close": float(row.get("pre_close") or 0),
        "change": float(row.get("change") or 0),
        "pct_chg": float(row.get("pct_chg") or 0),
        "amount_wan": float(row.get("amount") or 0),
    }
