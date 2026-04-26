# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What Is YMOS

YMOS (勇麦投资操作系统) is a natural-language-driven human-AI collaborative investment research system. The core is NOT code — it's **Markdown SOP documents + P-series prompts** that structure investment thinking. Python scripts are lightweight data fetchers only.

## Architecture: Three Modules

```
Eyes/ (看市场) → Brain/ (做分析) → 持仓与关注/ (管状态)
```

- **Eyes/** — Market monitoring: RSS fetching, price scanning, market reports. Scripts in `Eyes/scripts/` are standalone atomic data fetchers
- **Brain/** — Analysis engine: strategy routing, initial research, P1-P16 prompts in `Brain/references/`, diagnosis module in `Brain/ymos-diagnosis/`
- **持仓与关注/** — State layer: state machines (`持仓_状态机.md`, `Watchlist_状态机.md`), individual stock folders, investment preferences

Information flows one direction: Eyes sees → Brain analyzes → 持仓与关注 stores conclusions.

## Running Scripts

Python 3.12, zero third-party dependencies. Scripts use `env_loader.py` to auto-load `.env`.

```bash
# Price scan (most common operation)
python Eyes/scripts/fetch_price_router.py --symbols AAPL,NIO,688008.SS,0700.HK --output-dir Eyes/投资雷达/Raw_Data --date-tag 20260426

# RSS fetch
python Eyes/scripts/fetch_rss.py

# Individual price sources (rarely called directly, router dispatches)
python Eyes/scripts/fetch_price_api.py --symbols AAPL --output out.json --token $FINNHUB_API_KEY
python Eyes/scripts/fetch_price_tushare.py --symbols 688008.SS --token $TUSHARE_TOKEN --output out.json
python Eyes/scripts/fetch_price_yahoo.py --symbols 0700.HK --output out.json
```

## Key Rules for Editing

### File Permissions
- **Read-only**: All SOP files (`SOP_*.md`), P-series prompts (`Brain/references/*.md`), `AGENT_GUIDE.md`, `总入口暗号.md`, `.env`
- **Human-in-the-Loop**: `持仓与关注/当前关注方向与投资偏好.md` — draft changes but require user confirmation before writing
- **Writable via SOP only**: Reports in `Eyes/市场洞察/`, `Eyes/投资雷达/`, `Brain/策略分析/`, state machines, stock knowledge bases

### Report Naming
- Same-day reports overwrite (no `_v2`/`_v3` suffixes)
- Market insight: `YYYY-MM-DD_市场洞察.md`
- Radar: `投资雷达_YYYY-MM-DD.md`
- Monthly archive dirs: `YYYY-MM/`

### State Machine Updates
Every state machine write must: (1) update `更新时间`, (2) update the target row, (3) append to `今日变更日志`.

### Critical Constraints
- Never skip P2 before running P5/P6 — must know the phase first
- Never give buy/sell advice without P12 discipline review
- Don't confuse market insight (no holdings context) with investment radar (reads holdings)
- Read the entire individual stock folder as context when analyzing a ticker
- Market insight → Investment Radar → Strategy Analysis → Position Close — strict ordering, each depends on previous output

## Environment Variables (.env)

All optional. Missing keys trigger automatic fallback to free sources.

| Variable | Source | Fallback |
|---|---|---|
| `FINNHUB_API_KEY` | Finnhub (US stocks, Crypto) | Yahoo Finance |
| `TUSHARE_TOKEN` | Tushare (A-shares .SS/.SZ) | Yahoo Finance |
| `YMOS_MARKET_API_URL` / `YMOS_MARKET_API_KEY` | Market event API | RSS only |

## Price Router Logic

`fetch_price_router.py` dispatches by ticker suffix:
- `.SS`/`.SZ` → Tushare (or Yahoo fallback)
- `.HK` → Yahoo (fixed)
- No suffix / Crypto → Finnhub (or Yahoo fallback)

Crypto symbols (BTC, ETH, etc.) stored as bare symbols in state machines; router normalizes to source-specific format (e.g., `BINANCE:BTCUSDT` for Finnhub, `BTC-USD` for Yahoo).

## Onboarding Flow

New users say "开始使用" → Agent reads `持仓与关注/SOP_入职引导.md` → guided interview (investment preferences → holdings → watchlist → first run).

## Agent Entry Point

`总入口暗号.md` is the master routing table for all natural language commands. Read it first in every new session.
