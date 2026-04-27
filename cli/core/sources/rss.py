"""RSS data source (migrated from fetch_rss.py).

Zero third-party dependencies.
"""

from __future__ import annotations

import json
import ssl
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

FALLBACK_SOURCES = [
    {"name": "Bloomberg Markets", "url": "https://feeds.bloomberg.com/markets/news.rss", "category": "美股", "priority": "high"},
    {"name": "Bloomberg Tech", "url": "https://feeds.bloomberg.com/technology/news.rss", "category": "科技", "priority": "high"},
    {"name": "CNBC Markets", "url": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258", "category": "美股", "priority": "high"},
    {"name": "CNBC Finance", "url": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664", "category": "宏观", "priority": "medium"},
    {"name": "Seeking Alpha Picks", "url": "https://seekingalpha.com/tag/editors-picks.xml", "category": "深度洞察", "priority": "high"},
    {"name": "Stratechery", "url": "https://stratechery.com/feed/", "category": "深度洞察", "priority": "high"},
]


def load_sources(category_filter: str | None = None, config_path: str | None = None) -> list[dict]:
    """Load RSS source config. Priority: specified path → rss_sources.json → built-in."""
    from cli.core.paths import find_ymos_root
    scripts_dir = find_ymos_root() / "Eyes" / "scripts"

    if config_path:
        custom_path = Path(config_path)
        if not custom_path.is_absolute():
            custom_path = scripts_dir / config_path
        if custom_path.exists():
            try:
                config = json.loads(custom_path.read_text(encoding="utf-8"))
                sources = config.get("sources", [])
                print(f"📂 Loaded {len(sources)} sources from {custom_path.name}")
            except Exception as e:
                print(f"⚠️ Failed to read {custom_path.name}: {e}")
                return []
        else:
            print(f"⚠️ Config not found: {custom_path}")
            return []
    else:
        json_path = scripts_dir / "rss_sources.json"
        if json_path.exists():
            try:
                config = json.loads(json_path.read_text(encoding="utf-8"))
                sources = config.get("sources", [])
                print(f"📂 Loaded {len(sources)} sources from rss_sources.json")
            except Exception:
                sources = FALLBACK_SOURCES
        else:
            print("📂 rss_sources.json not found, using built-in sources (6)")
            sources = FALLBACK_SOURCES

    if category_filter:
        sources = [s for s in sources if s.get("category") == category_filter]
        print(f"🔍 Filtered by [{category_filter}]: {len(sources)} sources")
    return sources


def fetch_rss(url: str, days: int = 1):
    """Fetch and parse a single RSS/Atom feed."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "application/rss+xml, application/xml, text/xml",
    }
    req = urllib.request.Request(url, headers=headers, method="GET")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
            xml_content = response.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print(f"   ⚠️ Source blocked (403), skipping")
            return "BLOCKED_403"
        print(f"   ❌ HTTP error: {e.code} - {e.reason}")
        return None
    except urllib.error.URLError as e:
        print(f"   ❌ Network error: {e.reason}")
        return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        print(f"   ❌ XML parse error: {e}")
        return None

    cutoff_time = datetime.now(timezone.utc) - timedelta(days=days)

    # Try Atom format first
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    entries = root.findall("atom:entry", ns)
    if entries:
        items = []
        for entry in entries:
            title = (entry.findtext("atom:title", "", ns) or "").strip()
            link_el = entry.find("atom:link", ns)
            link = link_el.get("href", "") if link_el is not None else ""
            pub_date = (entry.findtext("atom:published", "", ns) or
                        entry.findtext("atom:updated", "", ns) or "").strip()
            summary = (entry.findtext("atom:summary", "", ns) or
                       entry.findtext("atom:content", "", ns) or "").strip()
            if pub_date:
                try:
                    parsed_date = datetime.fromisoformat(pub_date.replace("Z", "+00:00"))
                    if parsed_date < cutoff_time:
                        continue
                except ValueError:
                    pass
            categories = [cat.get("term", "") for cat in entry.findall("atom:category", ns) if cat.get("term")]
            items.append({
                "title": title, "link": link, "pub_date": pub_date,
                "categories": categories, "description": summary, "content": summary,
            })
        return items

    # RSS 2.0 format
    channel = root.find("channel")
    if channel is None:
        print("   ❌ No RSS channel or Atom entries found")
        return None

    items = []
    for item in channel.findall("item"):
        title = item.findtext("title", "").strip()
        link = item.findtext("link", "").strip()
        pub_date = item.findtext("pubDate", "").strip()
        description = item.findtext("description", "").strip()
        content = ""
        for child in item:
            if "encoded" in child.tag:
                content = (child.text or "").strip()
                break
        parsed_date = None
        if pub_date:
            for fmt in ("%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S %Z"):
                try:
                    parsed_date = datetime.strptime(pub_date, fmt)
                    if fmt.endswith("%Z"):
                        parsed_date = parsed_date.replace(tzinfo=timezone.utc)
                    break
                except ValueError:
                    continue
        if parsed_date and parsed_date < cutoff_time:
            continue
        categories = [cat.text for cat in item.findall("category") if cat.text]
        items.append({
            "title": title, "link": link, "pub_date": pub_date,
            "categories": categories, "description": description,
            "content": content if content else description,
        })
    return items


def fetch_all_sources(sources: list[dict], days: int = 1) -> dict:
    """Fetch from all configured RSS sources."""
    all_items: list[dict] = []
    success_count = 0
    fail_count = 0
    blocked_sources: list[str] = []

    for src in sources:
        name = src["name"]
        print(f"\n📡 [{name}] ({src.get('category', '未分类')})")
        items = fetch_rss(src["url"], days)
        if items == "BLOCKED_403":
            blocked_sources.append(name)
            fail_count += 1
        elif items:
            for item in items:
                item["source_name"] = name
                item["source_category"] = src.get("category", "未分类")
                item["source_priority"] = src.get("priority", "medium")
            all_items.extend(items)
            print(f"   ✅ {len(items)} items")
            success_count += 1
        else:
            fail_count += 1

    if blocked_sources:
        print(f"\nℹ️ 403-blocked sources: {len(blocked_sources)}")

    categories_summary: dict[str, int] = {}
    for item in all_items:
        cat = item.get("source_category", "未分类")
        categories_summary[cat] = categories_summary.get(cat, 0) + 1

    return {
        "sources": [s["name"] for s in sources],
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "time_range_days": days,
        "count": len(all_items),
        "sources_ok": success_count,
        "sources_fail": fail_count,
        "sources_blocked_403": len(blocked_sources),
        "categories_summary": categories_summary,
        "data": all_items,
    }
