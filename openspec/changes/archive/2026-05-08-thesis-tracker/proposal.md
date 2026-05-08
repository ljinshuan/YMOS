## Why

YMOS 当前有投资论点分析（P1/P4/P2），但缺乏持续追踪机制。投资论点需要随着新信息不断验证和更新，现有系统无法：
1. 记录论点随时间的演变
2. 跟踪关键支柱的进展/偏离
3. 维护催化剂日历并关联到论点
4. 量化论点置信度的变化

导致用户无法系统性地评估投资决策的质量和及时调整仓位。

## What Changes

**新增能力：**
- 新增 `thesis-tracker` skill，用于投资论点的持续追踪和更新
- 新增论点记分卡系统，跟踪关键支柱的状态
- 新增更新日志功能，记录每个数据点对论点的影响
- 新增催化剂关联功能，将事件与论点支柱绑定

**修改内容：**
- `ymos-research` skill 可选集成 thesis-tracker，在 P1/P4 完成后初始化论点追踪
- `ymos-strategy` skill 可引用 thesis-tracker 的当前置信度作为决策输入

## Capabilities

### New Capabilities
- `thesis-tracker`: 投资论点追踪能力，包括论点定义、记分卡、更新日志、催化剂关联

### Modified Capabilities
- (无)

## Impact

**新增文件：**
- `.claude/skills/ymos-thesis-tracker/SKILL.md` — 论点追踪 skill
- `.claude/skills/ymos-thesis-tracker/sop.md` — 操作流程
- `.claude/skills/ymos-thesis-tracker/templates/thesis-tracker.md` — 论点追踪模板

**修改文件：**
- `.claude/skills/ymos-research/SKILL.md` — 集成论点初始化
- `.claude/skills/ymos-strategy/SKILL.md` — 引用论点置信度

**数据层：**
- 个股文件夹新增 `投资论点追踪.md` 文件
- 状态机 P4 列新增论点置信度字段
