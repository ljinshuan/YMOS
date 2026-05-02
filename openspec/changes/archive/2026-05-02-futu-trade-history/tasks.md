## 1. 数据源

- [x] 1.1 创建 `cli/core/sources/futu_deals.py`，实现 `fetch_deals(host, port, start_date, end_date, ticker=None)` 函数
- [x] 1.2 实现 Futu `history_deal_list_query` 调用，处理 `code` 参数（空=所有标的，或 Futu symbol）
- [x] 1.3 实现数据标准化：每条 deal 转换为 ticker/name/side/price/quantity/timestamp/fee/currency
- [x] 1.4 实现 Futu symbol → YMOS ticker 转换（复用 `futu_symbol_to_ticker`）
- [x] 1.5 实现错误处理：OpenD 不可达返回 None，未登录返回 None 并提示

## 2. CLI 命令

- [x] 2.1 创建 `cli/commands/trade_history.py`，实现 `ymos trade-history fetch` 命令（Typer app）
- [x] 2.2 实现 `--days` 参数（默认 30）
- [x] 2.3 实现 `--ticker` 参数（可选，按标的过滤）
- [x] 2.4 实现 `--output-dir` 参数（默认 `data/trade-history/`）
- [x] 2.5 实现 `--format` 参数（json/markdown/both，默认 both）
- [x] 2.6 实现 JSON 输出：`{"meta": {"source", "start_date", "end_date", "deal_count"}, "deals": [...]}`
- [x] 2.7 实现 Markdown 输出：统计摘要 + 按标的分组明细表
- [x] 2.8 在 `cli/main.py` 中注册 `trade-history` 子命令

## 3. Skills 同步

- [x] 3.1 在 `skills/ymos-strategy/SKILL.md` 中提及 P12 纪律审查可引用 `ymos trade-history fetch` 数据作为行为偏误实证
- [x] 3.2 在 `skills/ymos-strategy/sop.md` 中添加交易记录作为 P12 可选输入说明
- [x] 3.3 在 `skills/ymos-diagnosis/SKILL.md` 中提及交易行为分析可使用 `ymos trade-history fetch`
- [x] 3.4 在 `skills/ymos-reconcile/SKILL.md` 中提及可选使用 `ymos trade-history fetch` 校验状态机操作记录
- [x] 3.5 在 `skills/ymos-core/routing.md` 中添加交易记录入口（trade-history → strategy P12 / diagnosis）

## 4. 验证

- [x] 4.1 验证 `ymos trade-history fetch` 在 OpenD 未运行时报错退出
- [x] 4.2 验证 JSON 和 Markdown 输出格式正确
- [x] 4.3 验证 Futu symbol 转换正确（HK.00700 → 0700.HK 等）
