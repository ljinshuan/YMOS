## Why

YMOS 的投资雷达（ymos-radar）目前仅依赖价格扫描 + 基础技术信号，缺乏资金流维度的异动检测。资金流向是市场主力行为的直接反映——大单流入、经纪商集中买卖、做空量突增等信号能提前捕捉到价格异动。富途提供完整的资金异动检测能力（资金分布、经纪商买卖、资金流趋势、做空量），用户本地已安装 OpenD，可直接复用数据源。

## What Changes

- 在 `ymos-radar` skill 中新增资金流异动检测环节（SOP 扩展）
- 新增 CLI 命令 `ymos fetch-capital-flow`，通过富途 OpenD 获取资金流数据
- 新增 P-series prompt（P20-capital-anomaly），用于资金异动信号的结构化分析
- 异动信号纳入投资雷达报告，作为 Tier 1/Tier 2 事件评级的新维度
- 在 `skills/ymos-core/routing.md` 中更新 radar 路由，增加资金异动检测步骤

## Capabilities

### New Capabilities
- `capital-flow-anomaly`: 资金流异动检测能力，覆盖资金分布、经纪商买卖活动、资金流趋势、做空量与比率，输出异动信号评级

### Modified Capabilities
- `ymos-radar`: SOP 扩展——价格扫描后增加资金流扫描环节，异动信号纳入 Tier 1/Tier 2 事件评级体系
- `ymos-strategy`: 在买入/加仓路由中增加资金流确认维度（大单流入作为正向确认信号）

## Impact

- **新增文件**: `cli/commands/capital_flow.py`, `skills/ymos-core/prompts/p20-capital-anomaly.md`（或放在 ymos-radar/prompts/ 下）
- **修改文件**: `cli/main.py` (注册新命令), `skills/ymos-radar/sop.md` (SOP 扩展), `skills/ymos-radar/SKILL.md` (新增触发和步骤), `skills/ymos-core/routing.md` (更新路由)
- **依赖**: 需要本地运行富途 OpenD 客户端（用户已安装）
- **数据源**: 富途资金流 API（通过 OpenD 网关）
