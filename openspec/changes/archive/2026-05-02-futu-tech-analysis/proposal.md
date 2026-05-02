## Why

当前技术面分析 (`ymos tech analyze`) 的历史 OHLCV 数据仅依赖 Tushare（A 股）和 Yahoo Finance（其他市场），数据源单一且 Yahoo 在港股/A 股覆盖上不稳定。项目已集成 Futu OpenD SDK（`futu-api`），且已有 sentiment、capital_flow、screener 等命令使用 Futu 接口，应将这一能力扩展到技术面分析，提升数据获取的可靠性和时效性。

## What Changes

- 新增 `cli/core/sources/futu.py` 数据源模块，封装 Futu OpenD 历史K线获取（`get_history_kline`）
- 修改 `cli/core/sources/history.py`，在路由逻辑中优先使用 Futu 获取 OHLCV 数据，Futu 不可用时降级到原有 Tushare/Yahoo
- 修改 `cli/commands/tech.py`，增加 `--source` 参数允许用户显式指定数据源
- 新增 `cli/core/futu_utils.py`，抽取 Futu OpenD 连接检查和 ticker 格式转换为共享工具函数（避免 sentiment、capital_flow、screener、tech 中重复代码）

## Capabilities

### New Capabilities
- `futu-history-source`: Futu OpenD 作为 OHLCV 历史数据源，支持 HK/US/CN 市场的日线/周线K线数据获取，含自动降级逻辑
- `futu-shared-utils`: Futu OpenD 连接检查、ticker 格式转换（YMOS → Futu 标准格式）、OpenD 启动提示等共享工具

### Modified Capabilities
- `history-routing`: `cli/core/sources/history.py` 的路由逻辑增加 Futu 优先级，Futu 可用时优先走 Futu，不可用时降级到原逻辑

## Impact

- **代码**: `cli/core/sources/history.py`（路由改动）、`cli/commands/tech.py`（参数扩展）、新增 `cli/core/sources/futu.py` 和 `cli/core/futu_utils.py`
- **依赖**: 已有 `futu-api` 依赖，无需新增
- **兼容性**: 完全向后兼容，Futu 不可用时自动降级到原有 Tushare/Yahoo 链路
- **运行时**: 需要本地 Futu OpenD 运行（localhost:11111），通过 `FUTU_OPEND_HOST` / `FUTU_OPEND_PORT` 环境变量配置
