## 1. 共享工具扩展

- [x] 1.1 在 `cli/core/futu_utils.py` 中添加 `futu_symbol_to_ticker(symbol)` 函数（Futu → YMOS 格式反向转换）

## 2. 持仓数据源

- [x] 2.1 创建 `cli/core/sources/futu_position.py`，实现 `fetch_positions(host, port)` 函数，调用 Futu OpenD `position_list_query`
- [x] 2.2 实现持仓数据标准化：每条记录包含 ticker（YMOS 格式）、name、quantity、cost_price、current_price、market_value、profit_loss、profit_loss_pct、currency
- [x] 2.3 实现 Futu symbol → YMOS ticker 转换（调用 `futu_symbol_to_ticker`）
- [x] 2.4 实现错误处理：OpenD 不可达返回 None，未登录返回 None 并打印提示

## 3. CLI 命令

- [x] 3.1 创建 `cli/commands/position.py`，实现 `ymos position fetch` 命令（Typer app）
- [x] 3.2 实现 `--output-dir` 参数（默认 `data/position/`）
- [x] 3.3 实现 `--format` 参数（json/markdown/both，默认 both）
- [x] 3.4 实现 JSON 输出格式：`{"meta": {"source", "fetched_at", "position_count"}, "positions": [...]}`
- [x] 3.5 实现 Markdown 输出格式：表头 + 持仓行 + 汇总行（总市值、总盈亏）
- [x] 3.6 实现 OpenD 连接检查，不可达时打印启动指南并 exit(1)
- [x] 3.7 在 `cli/main.py` 中注册 `position` 子命令

## 4. 验证

- [x] 4.1 验证 `ymos position fetch` 在 OpenD 未运行时报错退出
- [x] 4.2 验证 `futu_symbol_to_ticker` 转换正确（HK.00700 → 0700.HK 等）
- [x] 4.3 验证 JSON 和 Markdown 输出格式符合 spec
- [x] 4.4 验证输出文件保存在 `data/` 目录下（.gitignore 覆盖）
