## 1. 共享工具模块

- [x] 1.1 创建 `cli/core/futu_utils.py`，实现 `check_opend_connection(host, port)` 函数
- [x] 1.2 实现 `ticker_to_futu_symbol(ticker)` 函数（YMOS → Futu 格式转换）
- [x] 1.3 添加 `OPEND_STARTUP_GUIDE` 常量
- [x] 1.4 重构 `cli/commands/capital_flow.py`，删除内联的 `_check_opend_connection` 和 `_ticker_to_futu_symbol`，改为从 `cli.core.futu_utils` 导入
- [x] 1.5 重构 `cli/commands/screener.py`，删除内联的 `_check_opend_connection` 和相关转换逻辑，改为从 `cli.core.futu_utils` 导入

## 2. Futu 历史数据源

- [x] 2.1 创建 `cli/core/sources/futu.py`，实现 `fetch_futu_history(symbol, host, port)` 函数，调用 `get_history_kline` 获取 ~1 年日K数据
- [x] 2.2 实现返回值标准化：Futu DataFrame → 统一格式（columns: open, high, low, close, volume, DatetimeIndex sorted ascending, float64）
- [x] 2.3 实现错误处理：OpenD 不可达返回 None，API 错误返回 None 并打印 warning

## 3. 路由逻辑改造

- [x] 3.1 修改 `cli/core/sources/history.py` 的 `fetch_history()`，在现有路由前增加 Futu 优先尝试逻辑
- [x] 3.2 实现 graceful degradation：Futu 失败时自动降级到原 Tushare/Yahoo 逻辑
- [x] 3.3 修改 `cli/commands/tech.py`，新增 `--source` 参数（auto/futu/yahoo/tushare），默认 auto
- [x] 3.4 实现 `--source futu` 模式：Futu 不可用时直接报错退出（不降级）

## 4. 验证

- [x] 4.1 验证 Futu OpenD 不可用时，`ymos tech analyze` 自动降级到 Yahoo/Tushare 且输出正常
- [x] 4.2 验证 `_check_opend_connection` 和 `ticker_to_futu_symbol` 无重复定义（仅在 `futu_utils.py` 中）
- [x] 4.3 验证 `capital_flow` 和 `screener` 命令重构后功能不变（import 替换正确）
