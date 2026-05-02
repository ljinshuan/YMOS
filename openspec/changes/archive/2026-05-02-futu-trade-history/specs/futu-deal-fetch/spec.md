## ADDED Requirements

### Requirement: 通过 Futu OpenD 获取历史成交记录
系统 SHALL 提供 `fetch_deals(host, port, start_date, end_date)` 函数，调用 `OpenSecTradeContext.history_deal_list_query()` 获取指定日期范围内的成交记录。

#### Scenario: 正常获取成交记录
- **WHEN** OpenD 在线且用户已登录，调用 `fetch_deals(start_date="2026-04-02", end_date="2026-05-02")`
- **THEN** 返回 `list[dict]`，每条记录包含 ticker/name/side/price/quantity/timestamp/fee/currency

#### Scenario: OpenD 不可达
- **WHEN** OpenD 未运行或端口不通
- **THEN** 返回 None 并打印连接错误提示

#### Scenario: 无成交记录
- **WHEN** 指定日期范围内无成交
- **THEN** 返回空列表 `[]`

#### Scenario: 未登录
- **WHEN** OpenD 在线但用户未在客户端登录
- **THEN** 返回 None 并打印"请先在富途牛牛客户端登录账户"

### Requirement: 成交记录数据标准化
每条成交记录 MUST 包含以下标准化字段：

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| ticker | str | YMOS 格式（如 AAPL, 0700.HK） |
| name | str | 股票名称 |
| side | str | "BUY" 或 "SELL" |
| price | float | 成交价格 |
| quantity | float | 成交数量 |
| timestamp | str | 成交时间 ISO 格式 |
| fee | float | 手续费 |
| currency | str | 币种 |

#### Scenario: Futu symbol 自动转换
- **WHEN** Futu 返回 `HK.00700` 的成交记录
- **THEN** 标准化后 ticker 为 `0700.HK`

### Requirement: CLI 命令 ymos trade-history fetch
系统 SHALL 提供 `ymos trade-history fetch` 命令，支持以下参数：
- `--days`：回看天数，默认 30
- `--ticker`：可选，按单个标的过滤
- `--output-dir`：输出目录，默认 `data/trade-history/`
- `--format`：输出格式 json/markdown/both，默认 both

#### Scenario: 默认执行
- **WHEN** 运行 `ymos trade-history fetch`
- **THEN** 获取最近 30 天所有标的的成交记录，输出 JSON + Markdown 到 `data/trade-history/`

#### Scenario: 指定天数和标的
- **WHEN** 运行 `ymos trade-history fetch --days 7 --ticker AAPL`
- **THEN** 仅获取 AAPL 最近 7 天的成交记录

### Requirement: Markdown 汇总输出
Markdown 输出 MUST 包含：
1. 交易统计摘要（总笔数、买入笔数/金额、卖出笔数/金额、总手续费）
2. 按标的分组的交易明细表

#### Scenario: Markdown 格式正确性
- **WHEN** 成交记录包含 3 笔买入 AAPL、2 笔卖出 0700.HK
- **THEN** Markdown 包含统计摘要 + AAPL 明细表 + 0700.HK 明细表
