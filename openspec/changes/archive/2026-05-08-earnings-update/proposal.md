## Why

YMOS 当前的财报分析分散在 ymos-radar 和 ymos-research 中，缺乏：
1. 机构级的财报更新报告格式
2. 标准化的 Beat/Miss 分析
3. 完整的数据来源引用
4. 与前次预期的对比
5. 图表化展示（收入、利润率、估值等）

Financial Services 的 Earnings Analysis 提供了完整的财报报告模板（8-12 页、3000-5000 字、8-12 张图）。

## What Changes

**新增能力：**
- 新增 `earnings-update` skill，生成机构级财报更新报告
- 新增 Beat/Miss 分析功能
- 新增数据源引用规范（带超链接）
- 新增图表生成功能（收入趋势、利润率趋势等）
- 新增报告模板（Word/Markdown）

**修改内容：**
- `ymos-radar` skill 可选触发财报报告生成
- `ymos-strategy` skill 可引用财报分析结果

## Capabilities

### New Capabilities
- `earnings-update`: 财报更新报告能力，包括 Beat/Miss 分析、数据源引用、图表生成、报告模板

### Modified Capabilities
- (无)

## Impact

**新增文件：**
- `.claude/skills/ymos-earnings-update/SKILL.md` — 财报更新 skill
- `.claude/skills/ymos-earnings-update/sop.md` — 操作流程
- `.claude/skills/ymos-earnings-update/prompts/` — 财报相关 prompts
- `.claude/skills/ymos-earnings-update/templates/` — 报告模板

**修改文件：**
- `ymos-radar` skill — 集成财报报告触发
- `ymos-strategy` skill — 引用财报分析结果

**数据层：**
- 财报报告输出到 `data/reports/earnings/{ticker}/`
- 历史财报报告归档到 `data/reports/earnings/{ticker}/archive/`

**依赖：**
- 依赖 `excel-output` skill 生成图表数据
- 依赖财务数据源获取财报数据

## 时间框架

- **快速版本（V1）**：Markdown 格式报告，无图表
- **完整版本（V2）**：Word/Markdown 格式报告，带图表生成
