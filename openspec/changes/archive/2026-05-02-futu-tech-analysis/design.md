## Context

当前技术面分析命令 `ymos tech analyze` 通过 `cli/core/sources/history.py` 获取历史 OHLCV 数据，路由逻辑为：A 股 → Tushare，其他 → Yahoo Finance。项目中已有 3 个命令（sentiment、capital_flow、screener）使用 Futu OpenD SDK，但技术分析尚未接入。Futu OpenD 的 `get_history_kline` 接口可获取 HK/US/CN 全市场日线/周线数据，数据质量和时效性优于 Yahoo。

### 现状
- `cli/core/sources/history.py` — `fetch_history()` 根据 `classify()` 路由到 Tushare/Yahoo
- `cli/commands/capital_flow.py` 中有 `_ticker_to_futu_symbol()`、`_check_opend_connection()` 等重复工具函数
- `cli/commands/sentiment.py` 使用 HTTP 接口（非 OpenD），不涉及 K 线数据
- `.futu-skills/futu/anomaly-skills/futu-technical-anomaly/scripts/handle_technical_anomaly.py` 展示了 `get_technical_unusual` 用法

## Goals / Non-Goals

**Goals:**
- 抽取 Futu OpenD 共享工具函数（连接检查、ticker 转换），消除现有 3 个命令中的重复代码
- 新增 Futu 作为 OHLCV 历史数据源，Futu 可用时优先使用，不可用时自动降级到 Tushare/Yahoo
- 保持完全向后兼容，不影响现有命令行为

**Non-Goals:**
- 不实现 `get_technical_unusual` 异动检测（已有 `.futu-skills` 覆盖）
- 不修改技术指标计算逻辑（`cli/core/tech.py`）
- 不替换 price-scan 的价格路由（price-scan 用实时报价，tech analysis 用历史K线）

## Decisions

### 1. 共享工具模块 `cli/core/futu_utils.py`

从 `capital_flow.py` 抽取 `check_opend_connection()`、`ticker_to_futu_symbol()`、`OPEND_STARTUP_GUIDE` 为共享函数。sentiment.py 的 `_ticker_to_keyword()` 因是 HTTP 接口专用，暂不抽取。

**理由**: 当前 3 个命令中有 2 个重复实现了 `_check_opend_connection()` 和 `_ticker_to_futu_symbol()`，新增 tech 数据源会产生第 3 处重复。

### 2. Futu 历史K线数据源 `cli/core/sources/futu.py`

封装 `get_history_kline` 接口，返回与现有 `fetch_history` 一致的 `{symbol: DataFrame}` 格式（columns: open, high, low, close, volume）。自动重试 1 次，失败后返回 None 触发降级。

**理由**: 保持 DataFrame 格式一致，使 `cli/core/tech.py` 的分析逻辑无需修改。

### 3. 路由策略：Futu 优先 + 自动降级

修改 `fetch_history()` 路由逻辑：
1. 检测 Futu OpenD 是否可达（`check_opend_connection`）
2. 可达 → 尝试 `get_history_kline`，失败则降级到原逻辑
3. 不可达 → 直接走原 Tushare/Yahoo 逻辑

**替代方案**: 按市场分源（HK 优先 Futu，US 优先 Finnhub），但增加维护复杂度，且用户场景中 Futu 通常覆盖所有持仓市场。统一优先 Futu 更简洁。

### 4. 新增 `--source` 参数

`ymos tech analyze` 增加 `--source` 选项（`auto`/`futu`/`yahoo`/`tushare`），默认 `auto`。允许用户在 Futu 数据异常时强制使用指定数据源。

## Risks / Trade-offs

- **Futu OpenD 依赖** → OpenD 需要本地运行，不可用时自动降级，不影响功能
- **K 线数据与 Yahoo 格式差异** → Futu 返回字段名不同（如 `vol` vs `volume`），在 `futu.py` 源模块中统一转换
- **graceful degradation 性能** → 每次调用多一次 socket 连接检查（3s timeout），影响极小
