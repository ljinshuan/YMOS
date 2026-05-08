## Why

YMOS 的 ymos-radar 可以监控当前发生的事件，但缺乏前瞻性的事件日历功能。投资决策需要提前布局：
1. 财报日期能帮助用户提前建仓或减仓
2. 行业会议/产品发布会是重要的价格驱动因素
3. 宏观事件（FOMC、CPI 等）影响整体市场情绪
4. 缺乏前瞻性导致用户错过关键机会或风险暴露

当前用户只能被动等待事件发生，无法主动规划仓位。

## What Changes

**新增能力：**
- 新增 `catalyst-calendar` skill，用于构建和维护催化剂日历
- 新增事件收集功能，覆盖财报、企业事件、行业事件、宏观事件
- 新增每周预览功能，汇总即将到来的关键事件
- 新增事件影响评估，帮助用户预判事件对持仓的影响
- 新增日历导出功能（支持 Excel 格式）

**修改内容：**
- `ymos-radar` skill 可选集成催化剂日历，在事件监测后更新日历
- `ymos-strategy` skill 可引用催化剂日历中的即将到来事件作为决策输入

## Capabilities

### New Capabilities
- `catalyst-calendar`: 催化剂日历能力，包括事件收集、日历视图、每周预览、影响评估

### Modified Capabilities
- (无)

## Impact

**新增文件：**
- `.claude/skills/ymos-catalyst-calendar/SKILL.md` — 催化剂日历 skill
- `.claude/skills/ymos-catalyst-calendar/sop.md` — 操作流程
- `.claude/skills/ymos-catalyst-calendar/templates/` — 模板文件

**修改文件：**
- `.claude/skills/ymos-radar/SKILL.md` — 集成日历更新
- `.claude/skills/ymos-strategy/SKILL.md` — 引用即将到来的事件

**数据层：**
- 新增 `data/reports/catalyst-calendar/YYYY-MM/` 目录
- 新增 `催化剂日历.md` 全局文件
- 个股文件夹可选关联催化剂（与 thesis-tracker 集成）

**依赖：**
- 需要数据源支持（Futu/Yahoo 财报日期 API）
