## Context

YMOS 当前有 8 个独立 Python 脚本在 `Eyes/scripts/` 中，零第三方依赖，通过 argparse 解析参数。脚本间通过 `subprocess.call` 互调（如 `fetch_price_router.py` 调用 `fetch_price_api.py`）。状态机读写、目录创建、模板初始化等操作由 agent 在 SOP 中临时拼接 bash 命令完成。

## Goals / Non-Goals

**Goals:**
- 统一 CLI 入口 `ymos`，覆盖所有数据抓取 + 文件操作
- 路径集中管理，skill 不硬编码路径
- 保持现有脚本的全部功能，不丢失数据源回退逻辑
- typer + rich 提供友好的 CLI 体验

**Non-Goals:**
- 不做 API server / web 服务
- 不做交互式 REPL
- 不改变数据抓取的业务逻辑（路由规则、回退策略保持不变）

## Decisions

### D1: 目录结构

```
cli/
├── __init__.py
├── main.py                  ← typer app 入口
├── commands/
│   ├── __init__.py
│   ├── price.py             ← price-scan 子命令
│   ├── rss.py               ← fetch-rss 子命令
│   ├── market.py            ← fetch-market 子命令
│   ├── news.py              ← fetch-news 子命令
│   ├── state.py             ← state 子命令（read/write/validate）
│   ├── init.py              ← init 子命令（stock/dirs/template）
│   └── report.py            ← report 子命令（list）
├── core/
│   ├── __init__.py
│   ├── paths.py             ← 所有路径常量
│   ├── router.py            ← 价格路由逻辑（从 fetch_price_router.py 迁移）
│   ├── sources/
│   │   ├── __init__.py
│   │   ├── finnhub.py       ← 从 fetch_price_api.py 迁移
│   │   ├── tushare.py       ← 从 fetch_price_tushare.py 迁移
│   │   ├── yahoo.py         ← 从 fetch_price_yahoo.py 迁移
│   │   └── rss.py           ← 从 fetch_rss.py 迁移
│   ├── state.py             ← 状态机解析/写入工具
│   └── crypto.py            ← Crypto 符号归一化
└── utils/
    ├── __init__.py
    └── env_loader.py         ← 从 scripts/env_loader.py 迁移
```

### D2: CLI 命令设计

```bash
# 数据抓取
ymos price-scan --symbols AAPL,NIO,0700.HK [--output-dir DIR] [--date-tag TAG]
ymos price-scan --from-state                               # 从状态机读取 ticker
ymos fetch-rss --days N [--config FILE] [--output FILE]
ymos fetch-market --days N [--output FILE]
ymos fetch-news --hours N [--output FILE]

# 状态机操作
ymos state read {holdings|watchlist|preferences}
ymos state update holdings --ticker TICKER --field FIELD --value VALUE
ymos state validate

# 初始化
ymos init stock --ticker TICKER --name NAME --location {holdings|watchlist}
ymos init dirs
ymos init template --type {knowledge-base|memo} --ticker TICKER --name NAME

# 报告
ymos report list --type {insight|radar|strategy} [--latest] [--date DATE]
```

### D3: paths.py 设计

集中定义所有路径，接受 YMOS 根目录作为参数（默认自动检测）：

```python
class Paths:
    root: Path                    # YMOS 项目根
    data: Path                    # data/
    state: Path                   # data/state/
    stocks: Path                  # data/stocks/
    reports: Path                 # data/reports/
    holdings_state: Path          # data/state/holdings.md
    watchlist_state: Path         # data/state/watchlist.md
    preferences: Path             # data/state/preferences.md
    # ... 报告路径、Raw_Data 路径等
```

### D4: pyproject.toml 注册

```toml
[project.scripts]
ymos = "cli.main:app"
```

### D5: state 子命令的 Markdown 解析

状态机是 Markdown 表格格式。`state read` 输出 JSON，`state update` 解析表格、修改指定行、写回。使用简单的正则解析，不引入 Markdown 解析库。

## Risks / Trade-offs

- **typer 依赖**：引入第三方依赖，但 typer 是 Python CLI 生态的标准选择，维护活跃
- **状态机 Markdown 解析**：正则解析脆弱，表格格式变化会导致解析失败。缓解：状态机写回也通过 CLI，确保读写一致
- **迁移风险**：脚本迁移过程中可能丢失边界情况。缓解：保留原脚本作为参考，新 CLI 通过后再删除
