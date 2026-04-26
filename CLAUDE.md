# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What Is YMOS

YMOS (勇麦投资操作系统) is a natural-language-driven human-AI collaborative investment research system. The core is NOT code — it's **Markdown SOP documents + P-series prompts** that structure investment thinking. Python CLI tools are lightweight data fetchers only.

## Architecture: Three Layers

```
skills/ (能力层) → data/ (数据层) → cli/ (工具层)
```

- **skills/** — 9 个 YMOS 能力（含 ymos-core 共享基础设施），每个 skill 自包含 SOP、prompts、knowledge。Agent 发现和执行的入口
- **data/** — 运行时数据（状态机 + 个股文件夹 + 报告），.gitignore 忽略
- **cli/** — 统一 CLI 工具（`ymos` 命令），数据抓取 + 文件操作

Information flows: skills trigger workflows → data stores state → cli fetches data. Skills depend on ymos-core for shared resources (prompts, templates, routing).

## Running Scripts

Python 3.12+ with typer+rich. `ymos` CLI auto-loads `.env`.

```bash
# Price scan
ymos price-scan --symbols AAPL,NIO,688008.SS,0700.HK --output-dir data/reports/radar/raw --date-tag 20260426

# Price scan from state
ymos price-scan --from-state

# RSS fetch
ymos fetch-rss --days 1

# State operations
ymos state read holdings
ymos state update holdings --ticker AAPL --field P4 --value "测试中"
ymos state validate
```

## Key Rules for Editing

### File Permissions
- **Read-only**: All SOP files (`skills/*/sop.md`), P-series prompts (`skills/*/prompts/*.md`), `AGENT_GUIDE.md`, `总入口暗号.md`, `.env`, `skills/ymos-diagnosis/**`
- **Human-in-the-Loop**: `data/state/preferences.md` — draft changes but require user confirmation before writing
- **Writable via SOP only**: Reports in `data/reports/market-insight/`, `data/reports/radar/`, `data/reports/strategy/`, state machines, stock knowledge bases

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

## Skill Discovery

9 skills in `skills/` directory:

| Skill | Trigger Words | Depends On |
|-------|--------------|------------|
| ymos-core | (shared infrastructure, not user-facing) | — |
| ymos-onboarding | `开始使用`、`初始化系统`、`补全信息` | — |
| ymos-market-insight | `跑一下市场洞察`、`今天有什么新闻` | — |
| ymos-radar | `跑一下投资雷达`、`查一下价格` | ymos-core |
| ymos-strategy | `我想买/卖/加仓/持有怎么看 [ticker]` | ymos-core |
| ymos-research | `调研一下 [ticker]` | ymos-core |
| ymos-target-mgmt | `关注/建仓/移除/清仓 [ticker]` | ymos-core |
| ymos-reconcile | `收口一下`、`刷新持仓视图` | — |
| ymos-diagnosis | `诊断一下我的策略`、`帮我看看我的投资` | — |

## Data Layer

Runtime data lives in `data/` (ignored by git):
- `data/state/` — Holdings/watchlist/preferences state machines
- `data/stocks/` — Individual stock folders (holdings + watchlist)
- `data/reports/` — Generated reports (market-insight, radar, strategy)
- `data/dashboard/` — Visual dashboards

Use `ymos migrate` to migrate from old directory structure.
Use `ymos init dirs` to create the directory structure.

## Environment Variables (.env)

All optional. Missing keys trigger automatic fallback to free sources.

| Variable | Source | Fallback |
|---|---|---|
| `FINNHUB_API_KEY` | Finnhub (US stocks, Crypto) | Yahoo Finance |
| `TUSHARE_TOKEN` | Tushare (A-shares .SS/.SZ) | Yahoo Finance |
| `YMOS_MARKET_API_URL` / `YMOS_MARKET_API_KEY` | Market event API | RSS only |

## Price Router Logic

`cli/core/router.py` dispatches by ticker suffix:
- `.SS`/`.SZ` → Tushare (or Yahoo fallback)
- `.HK` → Yahoo (fixed)
- No suffix / Crypto → Finnhub (or Yahoo fallback)

Run: `ymos price-scan --symbols TICKER1,TICKER2`

Crypto symbols (BTC, ETH, etc.) stored as bare symbols in state machines; router normalizes to source-specific format (e.g., `BINANCE:BTCUSDT` for Finnhub, `BTC-USD` for Yahoo).

## Onboarding Flow

New users say "开始使用" → Agent reads `skills/ymos-onboarding/SKILL.md` → guided interview (investment preferences → holdings → watchlist → first run).

## Agent Entry Point

`总入口暗号.md` is the master routing table for all natural language commands. Read it first in every new session.
