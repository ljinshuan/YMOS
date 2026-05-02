## Why

YMOS 已有 Futu 持仓获取能力（`ymos position fetch`），但缺少历史交易记录查询。用户的实际买卖行为是交易纪律分析和行为偏误检测的核心数据源。P12（纪律审查）和 P11（清仓复盘）目前只能依赖用户口述或备忘录记录，缺少客观的交易数据支撑。

## What Changes

- 新增 `ymos trade-history fetch` CLI 命令，通过 Futu OpenD `history_deal_list_query` 获取最近 30 天的成交记录
- 新增 `cli/core/sources/futu_deals.py` 数据源，封装 Futu SDK 调用并标准化输出
- 输出 JSON 格式，包含每笔成交的 ticker、方向（买/卖）、成交价、成交量、成交时间、手续费
- 输出 Markdown 汇总格式：交易统计（总笔数、买入/卖出比例）+ 按标的分组明细
- 支持 `--days` 参数调整回看天数（默认 30）

## Capabilities

### New Capabilities
- `futu-deal-fetch`: 通过 Futu OpenD `history_deal_list_query` 获取历史成交记录并输出标准化 JSON/Markdown

### Modified Capabilities

（无现有 spec 需修改）

## Impact

- 新增 `cli/core/sources/futu_deals.py`
- 新增 `cli/commands/trade_history.py`
- 修改 `cli/main.py` 注册新子命令
- 依赖 `futu-api` SDK + 本地 Futu OpenD 在线
- 复用 `cli/core/futu_utils.py` 的连接检查和 ticker 转换工具
