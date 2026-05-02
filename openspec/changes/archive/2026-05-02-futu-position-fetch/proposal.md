## Why

YMOS 的持仓分析（`ymos-reconcile`、`ymos-strategy`）依赖 `data/state/holdings.md` 状态机中的手动录入持仓数据，缺乏与券商账户的实时同步能力。Futu OpenD 提供了 `get_holdings`（持仓查询）和 `accinfo_query`（账户信息）接口，可以直接获取用户的真实持仓明细（代码、数量、成本价、市值、盈亏），为后续持仓分析和策略制定提供准确数据基础。

## What Changes

- 新增 `cli/commands/position.py`，实现 `ymos position fetch` 命令，通过 Futu OpenD 获取当前账户持仓明细
- 新增 `cli/core/sources/futu_position.py`，封装 Futu OpenD 持仓查询接口（`get_holdings`），返回标准化的持仓数据
- 修改 `cli/main.py`，注册新命令
- 输出格式包含：股票代码、名称、持有数量、成本价、当前价、市值、浮动盈亏（金额和百分比）
- 支持 JSON 输出（供下游分析消费）和 Markdown 输出（供人阅读）

## Capabilities

### New Capabilities
- `futu-position-query`: 通过 Futu OpenD 查询真实账户持仓明细，返回标准化的持仓数据（代码、数量、成本、市值、盈亏）

### Modified Capabilities

（无现有 spec 需修改）

## Impact

- **代码**: 新增 `cli/commands/position.py`、`cli/core/sources/futu_position.py`，修改 `cli/main.py`（注册命令）
- **依赖**: 需要 `futu-api` SDK（已安装）+ 本地 Futu OpenD 运行
- **安全**: 持仓数据涉及个人财务隐私，输出文件仅保存在 `data/` 目录（已 .gitignore）
- **运行时**: 需要 Futu OpenD 已登录且处于连接状态，需配置 `FUTU_OPEND_HOST` / `FUTU_OPEND_PORT` 环境变量
- **下游消费**: 输出 JSON 可被 `ymos-reconcile`、`ymos-strategy` 等 skill 引用，实现持仓数据自动同步
