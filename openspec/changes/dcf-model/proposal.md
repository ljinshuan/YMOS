## Why

YMOS 当前的 P9 估值分析过于简化，只提供了基本的估值思路，缺乏：
1. 详细的现金流折现模型
2. WACC（加权平均资本成本）计算
3. 终值计算方法选择
4. 敏感性分析
5. 情景分析（乐观/基准/悲观）
6. 完整的 Excel 模型输出

Financial Services 的 DCF Model 提供了机构级的估值分析能力。

## What Changes

**新增能力：**
- 新增 `dcf-model` skill，提供完整的 DCF 建模能力
- 新增 WACC 计算功能
- 新增终值计算（永续增长法 + 退出倍数法）
- 新增敏感性分析（关键假设变化的影响）
- 新增情景分析（三情景对比）
- 新增 Excel 模型生成

**修改内容：**
- `ymos-research` skill 可选触发 DCF 模型分析
- `ymos-strategy` skill 可引用 DCF 估值结果作为决策输入
- P9 估值提示词可升级为调用 DCF skill

## Capabilities

### New Capabilities
- `dcf-model`: DCF 深度估值能力，包括现金流预测、WACC 计算、终值计算、敏感性分析、情景分析

### Modified Capabilities
- `valuation`: (可能存在的现有 spec) 升级为支持详细 DCF 分析

## Impact

**新增文件：**
- `.claude/skills/ymos-dcf-model/SKILL.md` — DCF 模型 skill
- `.claude/skills/ymos-dcf-model/sop.md` — 操作流程
- `.claude/skills/ymos-dcf-model/prompts/` — DCF 相关 prompts
- `.claude/skills/ymos-dcf-model/templates/` — DCF 模型模板

**修改文件：**
- `.claude/skills/ymos-core/prompts/p9-valuation.md` — 升级为可调用 DCF skill
- `ymos-strategy` skill — 集成 DCF 估值结果

**数据层：**
- DCF 分析报告输出到 `data/reports/valuation/{ticker}/`
- Excel 模型输出到 `data/reports/valuation/{ticker}/excel/`

**依赖：**
- 依赖 `excel-output` skill 生成 Excel 模型
- 依赖财务数据源（Finnhub/Tushare/Yahoo）获取历史数据
