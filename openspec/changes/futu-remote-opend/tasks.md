## 1. 环境变量与配置

- [x] 1.1 在 `.env` 中新增 `FUTU_OPEND_HOST=192.168.41.237` 和 `FUTU_OPEND_RSA_KEY`（RSA 私钥 PEM 内容，单行转义）
- [x] 1.2 在 `CLAUDE.md` 的 Environment Variables 表格中注册新增的两个环境变量

## 2. 连接工厂核心实现

- [x] 2.1 在 `cli/core/futu_utils.py` 中新增 `_is_remote_host()` 判断函数（非 localhost/127.0.0.1 返回 True）
- [x] 2.2 新增 `_ensure_rsa_key_file()` 函数：从 `FUTU_OPEND_RSA_KEY` 环境变量读取 PEM 内容，写入临时文件，注册 atexit 清理
- [x] 2.3 新增 `create_quote_context(host="", port=0)` 工厂函数：解析环境变量 → 远程时启用加密并配置私钥 → 返回 `OpenQuoteContext`
- [x] 2.4 新增 `create_trade_context(host="", port=0)` 工厂函数：同上逻辑，返回 `OpenSecTradeContext`
- [x] 2.5 修改 `check_opend_connection()` 默认参数，未传参时从环境变量读取 host/port

## 3. 替换现有连接调用点

- [x] 3.1 `cli/core/sources/futu.py` — `fetch_futu_history` 中替换 `ft.OpenQuoteContext` 为 `create_quote_context`
- [x] 3.2 `cli/core/sources/futu_quote.py` — `fetch_extended_quotes` 中替换连接创建 + `check_opend_connection` 调用
- [x] 3.3 `cli/core/sources/technical_anomaly.py` — 替换 `ft.OpenQuoteContext` 为 `create_quote_context`
- [x] 3.4 `cli/core/sources/derivatives_anomaly.py` — 替换 `ft.OpenQuoteContext` 为 `create_quote_context`
- [x] 3.5 `cli/commands/monitor.py` — 替换 `ft.OpenQuoteContext` + `check_opend_connection` 调用
- [x] 3.6 `cli/commands/screener.py` — 替换 `ft.OpenQuoteContext` + `check_opend_connection` 调用
- [x] 3.7 `cli/commands/capital_flow.py` — 替换 `ft.OpenQuoteContext` + `check_opend_connection` 调用
- [x] 3.8 其他 `check_opend_connection` 调用点（`trade_history`, `tech`, `position`, `derivatives_anomaly`, `technical_anomaly` commands）— 确保默认参数从环境变量读取

## 4. 验证

- [x] 4.1 运行 `ruff check cli/core/futu_utils.py` 确认无 lint 错误
- [x] 4.2 运行 `uv run python -c "from cli.core.futu_utils import create_quote_context, create_trade_context"` 验证导入正常
- [x] 4.3 使用 `--from-state` 执行 `uv run ymos price-scan` 测试远程连接实际可用
