## Why

YMOS 目前只能对已知标的做分析，缺乏主动选股/筛选能力。用户只能手动添加关注或持仓 ticker，无法根据基本面/技术面条件批量筛选候选标的。富途提供完整的选股筛选能力（按市值、PE、涨幅、板块等多维度过滤），且有成熟的方法论。用户本地已安装 OpenD，可直接复用数据源和方法论。

## What Changes

- 新增 `skills/ymos-screener/` skill，支持基本面/技术面多因子筛选
- 新增 CLI 命令 `ymos screen`，通过富途 OpenD 执行选股筛选
- 筛选结果输出候选标的列表，可直接接入已有的 ymos-research pipeline
- 支持预设筛选模板（成长股、价值股、高息股等）和自定义条件组合
- 在 `skills/ymos-core/routing.md` 中新增 screener 路由入口

## Capabilities

### New Capabilities
- `stock-screening`: 多因子选股筛选能力，支持港股/美股/A股，可按市值/PE/涨幅/换手率/板块等维度组合过滤，输出结构化候选标的列表

### Modified Capabilities
- `ymos-research`: 新增从 screener 结果批量发起调研的入口（screener 输出 → research pipeline）
- `ymos-core/routing`: 新增选股路由表（触发词 → 筛选条件 → 输出 → 可选 research 接入）

## Impact

- **新增文件**: `skills/ymos-screener/` (SKILL.md, sop.md), `cli/commands/screener.py`
- **修改文件**: `cli/main.py` (注册新命令), `skills/ymos-core/routing.md` (新增路由), `skills/ymos-research/SKILL.md` (新增调用接口)
- **依赖**: 需要本地运行富途 OpenD 客户端（用户已安装）
- **数据源**: 富途选股 API（通过 OpenD 网关）
