## Why

YMOS 目前所有价格获取都依赖手动触发（CLI 命令或 AI 对话），缺少自动化盯盘能力。用户需要一个在交易时段内持续监控持仓/关注列表价格、驱动外部策略引擎计算信号、并在信号触发时告警的自动化流程。

## What Changes

- 新增 CLI 命令 `ymos monitor fetch-prices`：通过 Futu OpenD 获取持仓/关注列表的日K + 分钟K线数据，累积写入 CSV 文件
- 新增 CLI 命令 `ymos monitor check-signals`：扫描策略信号文件，对新增信号生成终端/文件告警
- 新增 `cli/monitor/` 模块：交易时段判断、CSV 历史管理（去重合并）、信号读取、告警生成
- 新增 `skills/ymos-monitor/` skill：提供 Agent 盯盘上下文的 SOP 和路由
- 定义与 naught_backtest 的文件接口（价格 CSV 输入、信号 JSON 输出）

## Capabilities

### New Capabilities
- `monitor-price-fetch`: 通过 Futu OpenD 定时获取K线数据，写入标准化 CSV 历史文件
- `monitor-signal-alert`: 扫描策略信号文件，去重后生成终端/文件告警
- `skill-ymos-monitor`: Agent 盯盘能力的 SOP、触发暗号和路由定义

### Modified Capabilities
<!-- 无现有 spec 需要修改，盯盘与雷达流程完全独立 -->

## Impact

- **新增代码**: `cli/commands/monitor.py`, `cli/monitor/` 目录（4 个模块）, `skills/ymos-monitor/`
- **复用**: `cli/core/futu_utils.py`（连接检查、ticker 转换）, `cli/core/sources/futu.py`（K线获取模式）
- **路由更新**: `skills/ymos-core/routing.md` 新增盯盘路由条目
- **依赖**: 零新依赖，使用现有 futu-api + Python 标准库
- **不影响**: 现有 price-scan 三源分流、雷达流程、状态机更新逻辑
