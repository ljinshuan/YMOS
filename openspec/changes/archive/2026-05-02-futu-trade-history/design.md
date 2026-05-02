## Context

YMOS 已有 `futu_position.py`（持仓获取）作为参考实现，使用 `OpenSecTradeContext` + 标准化 DataFrame → dict 的模式。本 change 沿用相同架构，将 `history_deal_list_query` 封装为独立数据源。

Futu SDK 关键 API：
- `history_deal_list_query(code='', start='YYYY-MM-DD', end='YYYY-MM-DD')` — 返回 `(ret, data)` 二元组
- 默认查询所有标的（code 为空），按日期范围过滤

## Goals / Non-Goals

**Goals:**
- 获取最近 30 天的成交记录，标准化为 JSON 和 Markdown
- 支持按天数和单个标的过滤
- 复用现有 `futu_utils.py` 的工具函数

**Non-Goals:**
- 不做交易行为分析（留给 skill 层的 P12/P11 prompts）
- 不做历史委托单查询（`history_order_list_query`，后续可扩展）
- 不做资金流水查询（`get_acc_cash_flow`）
- 不修改现有 skills 文档（后续单独同步）

## Decisions

1. **使用 `history_deal_list_query` 而非 `order_list_query`** — deal 是实际成交记录，order 包含未成交和撤单，对行为分析来说成交记录更有价值
2. **命令名为 `trade-history`** — 与 `position` 命令并列，清晰表达"历史交易"语义
3. **输出目录默认 `data/trade-history/`** — 与 `data/position/` 并列
4. **JSON 结构** — `{"meta": {...}, "deals": [...]}`，每条 deal 包含 ticker/name/side/price/quantity/timestamp/fee/currency

## Risks / Trade-offs

- [OpenD 需要登录状态] → 不可达时返回 None 并打印启动指南，与 position 命令行为一致
- [history_deal_list_query 时间范围限制] → 实测确认是否支持 30 天回看，如不支持则缩短并提示
