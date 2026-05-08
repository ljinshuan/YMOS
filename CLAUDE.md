# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What Is YMOS

YMOS (勇麦投资操作系统) is a natural-language-driven human-AI collaborative investment research system. The core is NOT code — it's **Markdown SOP documents + P-series prompts** that structure investment thinking. Python CLI tools are lightweight data fetchers only.

## Architecture: Three Layers

```
.claude/skills/ (能力层) → data/ (数据层) → cli/ (工具层)
```

- **.claude/skills/** — 16 个 YMOS 能力（含 ymos-core 共享基础设施），每个 skill 自包含 SOP、prompts、knowledge。通过 `/ymos-*` 或触发词调用
- **data/** — 运行时数据（状态机 + 个股文件夹 + 报告），.gitignore 忽略
- **cli/** — 统一 CLI 工具（`ymos` 命令），数据抓取 + 文件操作

Information flows: skills trigger workflows → data stores state → cli fetches data. Skills depend on ymos-core for shared resources (prompts, templates, routing).

## Running Scripts

**项目使用 uv 管理虚拟环境。** 执行 Python/CLI 命令前必须通过 `uv run` 进入正确的虚拟环境。示例：`uv run ymos ...`、`uv run python ...`。不要直接调用 `python` 或裸 `ymos`，除非已确认在 uv 虚拟环境内（`.venv`）。

**.env 环境变量必须加载。** 富途 OpenD 使用远程连接（`FUTU_OPEND_HOST`/`PORT`/`RSA_KEY` 配置在 `.env` 中），不加载环境变量会回退到 `127.0.0.1` 导致连接失败。通过 `uv run ymos ...` 执行时 typer 命令内部已有 `load_dotenv()`；直接在 Python 中调用 ymos 模块时，需先 `from cli.utils.env_loader import load_dotenv; load_dotenv()`。

```bash
# Price scan
uv run ymos price-scan --symbols AAPL,NIO,688008.SS,0700.HK --output-dir data/reports/radar/raw --date-tag 20260426

# Price scan from state
uv run ymos price-scan --from-state

# RSS fetch
uv run ymos fetch-rss --days 1

# State operations
uv run ymos state read holdings
uv run ymos state update holdings --ticker AAPL --field P4 --value "测试中"
uv run ymos state validate
```

## Key Rules for Editing

### File Permissions
- **Read-only**: P-series prompts (`.claude/skills/*/prompts/*.md`), `AGENT_GUIDE.md`, `总入口暗号.md`, `.env`, `.claude/skills/ymos-diagnosis/**`
- **Skills 可修改**: SKILL.md、sop.md、routing.md 在主动丰富 skill 能力时可以修改（如新增 CLI 命令引用、新增执行步骤），但不应改变核心业务逻辑
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

16 skills registered in `.claude/skills/`, callable via `/ymos-*` slash commands or trigger words:

| Skill | Slash Command | Trigger Words |
|-------|--------------|---------------|
| ymos-core | `/ymos-core` | (shared infrastructure, not user-facing) |
| ymos-onboarding | `/ymos-onboarding` | `开始使用`、`初始化系统`、`补全信息` |
| ymos-market-insight | `/ymos-market-insight` | `跑一下市场洞察`、`今天有什么新闻` |
| ymos-radar | `/ymos-radar` | `跑一下投资雷达`、`查一下价格` |
| ymos-strategy | `/ymos-strategy` | `我想买/卖/加仓/持有怎么看 [ticker]` |
| ymos-research | `/ymos-research` | `调研一下 [ticker]` |
| ymos-target-mgmt | `/ymos-target-mgmt` | `关注/建仓/移除/清仓 [ticker]` |
| ymos-reconcile | `/ymos-reconcile` | `收口一下`、`刷新持仓视图` |
| ymos-diagnosis | `/ymos-diagnosis` | `诊断一下我的策略`、`帮我看看我的投资` |
| ymos-screener | `/ymos-screener` | `帮我选股`、`筛选一下` |
| ymos-sentiment | `/ymos-sentiment` | `看一下情绪`、`多空怎么样` |
| ymos-thesis-tracker | `/ymos-thesis-tracker` | `追踪论点 [ticker]`、`论点怎么样`、`更新论点` |
| ymos-excel-output | `/ymos-excel-output` | (internal, used by other skills via cli/excel_writer.py) |
| ymos-earnings-update | `/ymos-earnings-update` | `看一下财报 [ticker]`、`财报怎么样`、`财报分析` |
| ymos-catalyst-calendar | `/ymos-catalyst-calendar` | `催化剂日历`、`下周有什么事件`、`看一下日历` |
| ymos-dcf-model | `/ymos-dcf-model` | `DCF 分析 [ticker]`、`估值建模`、`算一下 DCF` |

## Data Layer

Runtime data lives in `data/` (ignored by git):
- `data/state/` — Holdings/watchlist/preferences state machines
- `data/stocks/` — Individual stock folders (holdings + watchlist)
- `data/reports/` — Generated reports (market-insight, radar, strategy, earnings, valuation, catalyst-calendar)
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
| `FUTU_OPEND_HOST` | Futu OpenD address (remote: auto-enable encryption) | `127.0.0.1` (local) |
| `FUTU_OPEND_PORT` | Futu OpenD port | `11111` |
| `FUTU_OPEND_RSA_KEY` | RSA private key file path, required for remote | Local only (no encryption) |

## Price Router Logic

`cli/core/router.py` dispatches by ticker suffix:
- `.SS`/`.SZ` → Tushare (or Yahoo fallback)
- `.HK` → Yahoo (fixed)
- No suffix / Crypto → Finnhub (or Yahoo fallback)

Run: `ymos price-scan --symbols TICKER1,TICKER2`

Crypto symbols (BTC, ETH, etc.) stored as bare symbols in state machines; router normalizes to source-specific format (e.g., `BINANCE:BTCUSDT` for Finnhub, `BTC-USD` for Yahoo).

## Onboarding Flow

New users say "开始使用" → Agent invokes `/ymos-onboarding` → guided interview (investment preferences → holdings → watchlist → first run).

## Known Issues

- **Team 模式不可用**: Claude Code 的 `Agent(team_name=...)` 在 tmux pane 中启动 worker 时，prompt 未传递给 `claude --print` 命令，导致 worker 无法启动（报错 `Input must be provided either through stdin or as a prompt argument when using --print`）。**替代方案：用 `Agent` 工具直接并行 spawn 多个 agent（不传 team_name），各自独立完成任务后结果直接返回主会话。**

## Agent Entry Point

`总入口暗号.md` is the master routing table for all natural language commands. Read it first in every new session.
