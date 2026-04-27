"""Price router — three-source dispatch (migrated from fetch_price_router.py).

No subprocess calls — directly imports source functions.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from cli.core.crypto import is_crypto, normalize_for_source
from cli.core.sources import finnhub, tushare, yahoo


def classify(symbol: str) -> str:
    """Return preferred data source for a ticker (不考虑 Key 是否存在)."""
    if symbol.endswith((".SS", ".SZ")):
        return "tushare"
    if symbol.endswith(".HK"):
        return "yahoo"
    return "finnhub"


def route_prices(symbols: list[str], output_dir: Path, date_tag: str,
                 finnhub_key: str = "", tushare_token: str = "") -> dict:
    """Route symbols to appropriate data sources and fetch prices.

    Returns dict with per-source results and output file paths.
    """
    finnhub_syms: list[str] = []
    tushare_syms: list[str] = []
    yahoo_syms: list[str] = []

    for s in symbols:
        bucket = classify(s)
        if bucket == "finnhub":
            finnhub_syms.append(s) if finnhub_key else yahoo_syms.append(s)
        elif bucket == "tushare":
            tushare_syms.append(s) if tushare_token else yahoo_syms.append(s)
        else:
            yahoo_syms.append(s)

    output_dir.mkdir(parents=True, exist_ok=True)
    date_tag = date_tag or "latest"

    print(f"📡 Price routing:")
    print(f"   Finnhub  ({len(finnhub_syms)}): {finnhub_syms or '—'}")
    print(f"   Tushare  ({len(tushare_syms)}): {tushare_syms or '—'}")
    print(f"   Yahoo    ({len(yahoo_syms)}): {yahoo_syms or '—'}")

    # Crypto normalization
    finnhub_syms_norm = [normalize_for_source(s, "finnhub") for s in finnhub_syms]
    yahoo_syms_norm = [normalize_for_source(s, "yahoo") for s in yahoo_syms]

    if finnhub_syms_norm != finnhub_syms or yahoo_syms_norm != yahoo_syms:
        print(f"🔄 Crypto normalization:")
        if finnhub_syms_norm != finnhub_syms:
            print(f"   Finnhub: {finnhub_syms} → {finnhub_syms_norm}")
        if yahoo_syms_norm != yahoo_syms:
            print(f"   Yahoo:   {yahoo_syms} → {yahoo_syms_norm}")

    results = {"finnhub": [], "tushare": [], "yahoo": [], "outputs": []}

    # Finnhub
    if finnhub_syms_norm:
        quotes = finnhub.fetch_quotes(finnhub_syms_norm, finnhub_key)
        results["finnhub"] = quotes
        out = output_dir / f"price_scan_finnhub_{date_tag}.json"
        payload = {
            "source": "Finnhub.io", "fetched_at": datetime.now(timezone.utc).isoformat(),
            "count": len(quotes), "data": quotes,
        }
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        results["outputs"].append(str(out))

    # Tushare
    if tushare_syms:
        code_map: dict[str, str] = {}
        for sym in tushare_syms:
            tc = tushare.to_tushare_code(sym)
            if tc:
                code_map[tc] = sym
        if code_map:
            rows = tushare.fetch_daily(list(code_map.keys()), tushare_token)
            rows_by_code = {r["ts_code"]: r for r in rows}
            data = []
            for ts_code in code_map:
                item = tushare.format_result(ts_code, rows_by_code.get(ts_code))
                data.append(item)
                status = "✅" if item["ok"] else "❌"
                if item["ok"]:
                    print(f"  {status} {item['symbol']:16s} ¥{item['last_close']:.2f}  ({item['pct_chg']:+.2f}%)")
                else:
                    print(f"  {status} {item['symbol']:16s} ERROR: {item.get('error')}")
            results["tushare"] = data
            out = output_dir / f"price_scan_tushare_{date_tag}.json"
            payload = {
                "source": "Tushare Pro daily API",
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "count": len(data), "data": data,
            }
            out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            results["outputs"].append(str(out))

    # Yahoo
    if yahoo_syms_norm:
        data = [yahoo.fetch_one(s) for s in yahoo_syms_norm]
        for item in data:
            status = "✅" if item.get("ok") else "❌"
            if item.get("ok"):
                print(f"  {status} {item['symbol']:16s} ¥{item['last_close']:.2f}")
            else:
                print(f"  {status} {item['symbol']:16s} ERROR: {item.get('error')}")
        results["yahoo"] = data
        out = output_dir / f"price_scan_yahoo_{date_tag}.json"
        payload = {
            "source": "Yahoo Finance V8 Chart API",
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "count": len(data), "data": data,
        }
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        results["outputs"].append(str(out))

    print("✅ Routing complete")
    return results
