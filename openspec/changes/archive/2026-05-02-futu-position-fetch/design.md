## Context

YMOS 的持仓分析依赖手动维护的 `data/state/holdings.md` 状态机，缺乏与券商账户的实时同步。Futu OpenD SDK 提供了 `get_holdings`（持仓查询）接口，可以直接获取用户在富途账户中的真实持仓明细。项目已安装 `futu-api` SDK（v10.4.6408），且已有多个命令使用 OpenD 接口。

### 现状
- `data/state/holdings.md` — 手动维护的持仓状态机
- `cli/core/futu_utils.py` — 即将由 futu-tech-analysis 创建的共享工具模块
- Futu OpenD `get_holdings` 接口返回：股票代码、名称、持有数量、成本价、市值、盈亏等

## Goals / Non-Goals

**Goals:**
- 新增 `ymos position fetch` CLI 命令，获取富途账户实时持仓明细
- 输出标准化 JSON（供下游分析消费）和 Markdown（供人阅读）
- 输出文件保存到 `data/` 目录（已在 .gitignore 中）

**Non-Goals:**
- 不自动同步到 `holdings.md` 状态机（需要 Human-in-the-Loop 确认）
- 不实现交易功能（纯只读查询）
- 不替代 `ymos-reconcile` 的分析逻辑

## Decisions

### 1. 命令设计：`ymos position fetch`

新增 `cli/commands/position.py`，注册为 `position` 子命令。支持参数：
- `--output-dir` — 输出目录（默认 `data/position/`）
- `--format json|markdown|both` — 输出格式（默认 `both`）

### 2. 数据源模块：`cli/core/sources/futu_position.py`

封装 `get_holdings` 接口调用，返回标准化的持仓列表。每条记录包含：
- `ticker` (YMOS 格式，如 `0700.HK`)
- `name` (股票名称)
- `quantity` (持有数量)
- `cost_price` (成本价)
- `current_price` (当前价)
- `market_value` (市值)
- `profit_loss` (浮动盈亏金额)
- `profit_loss_pct` (浮动盈亏百分比)
- `currency` (币种)

### 3. Futu → YMOS ticker 反向转换

`get_holdings` 返回 Futu 格式代码（如 `HK.00700`），需转换为 YMOS 格式（`0700.HK`）以便与现有状态机和分析流程对齐。此转换函数放在 `cli/core/futu_utils.py` 中作为 `futu_symbol_to_ticker()` 补充。

### 4. 安全考虑

持仓数据属于个人财务隐私：
- 输出仅保存到 `data/` 目录（已在 .gitignore）
- 命令输出不包含账户号等敏感信息
- 需要本地 OpenD 已登录状态

## Risks / Trade-offs

- **OpenD 登录状态** → 需要用户已在富途客户端登录，未登录时给出明确提示
- **多账户** → 当前仅支持默认账户，多账户场景后续按需扩展
- **数据时效性** → `get_holdings` 返回的是 OpenD 缓存数据，盘中可能有秒级延迟
