"""Market Data API source (migrated from fetch_market_api.py).

Zero third-party dependencies.
"""

from __future__ import annotations

import json
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_API_URL = "https://example.com/wp-json/tib/v1/reports"
DEFAULT_CATEGORIES = ["#中国股市", "#美国股市", "#Crypto", "#宏观经济", "#科技动态", "#个人精选"]


def _is_retryable(exc: Exception) -> bool:
    if isinstance(exc, urllib.error.HTTPError):
        return exc.code >= 500
    if isinstance(exc, (urllib.error.URLError, TimeoutError, ConnectionError, OSError)):
        return True
    return False


def _do_fetch(api_url: str, api_key: str, time_value, categories: list[str]):
    params = {"time_value": time_value, "categories": ",".join(categories)}
    full_url = f"{api_url}?{urllib.parse.urlencode(params)}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "YMOS-MarketAPI/1.0",
        "Accept": "application/json",
    }
    req = urllib.request.Request(full_url, headers=headers, method="GET")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_reports(api_url: str, api_key: str, time_value,
                  categories: list[str] | None = None,
                  max_retries: int = 3):
    """Fetch market reports with retry logic (exponential backoff)."""
    categories = categories or DEFAULT_CATEGORIES
    last_exc = None
    for attempt in range(1, max_retries + 1):
        try:
            return _do_fetch(api_url, api_key, time_value, categories)
        except urllib.error.HTTPError as exc:
            last_exc = exc
            if not _is_retryable(exc):
                print(f"❌ HTTP Error: {exc.code} - {exc.reason} (non-retryable)")
                return None
            wait = 2 ** attempt
            print(f"⚠️ HTTP {exc.code} (attempt {attempt}/{max_retries}), retry in {wait}s...")
            time.sleep(wait)
        except json.JSONDecodeError as exc:
            print(f"❌ JSON parse failed: {exc}")
            return None
        except Exception as exc:
            last_exc = exc
            if _is_retryable(exc):
                wait = 2 ** attempt
                print(f"⚠️ {exc} (attempt {attempt}/{max_retries}), retry in {wait}s...")
                time.sleep(wait)
            else:
                print(f"❌ Unexpected: {exc}")
                return None
    print(f"❌ Failed after {max_retries} retries: {last_exc}")
    return None
