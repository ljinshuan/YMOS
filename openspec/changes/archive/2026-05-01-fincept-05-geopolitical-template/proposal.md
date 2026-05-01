## Why

P13 Market Scanner 的 5 维信息聚合中，"宏观/政策"维度对地缘政治事件的分析比较薄弱——通常只做事件摘要，缺乏结构化的地缘政治分析框架。参考 FinceptTerminal 的 20 个地缘政治 Agent 设计（基于《地理囚徒》《世界秩序》《大棋局》三本书），引入轻量化的地缘政治分析模板，补齐宏观分析短板。

## What Changes

- 在 P13 Market Scanner 中新增"地缘政治分析模板"子模块
- 采用三步分析框架：地理约束 → 历史模式类比 → 对持仓/市场的传导路径
- 模板仅在新闻涉及地缘政治事件时激活（非每次 P13 都跑）
- 输出结构：地理锚点、关键约束、历史回声、传导路径（对哪些行业/标的有影响）、盲点提示
- 在 ymos-market-insight 的 SOP 中注册该模板作为 P13 的可选增强

## Capabilities

### New Capabilities
- `geopolitical-analysis-template`: 地缘政治分析模板，包含三步框架、结构化输出格式、传导路径映射

### Modified Capabilities
- `ymos-core`: 在 prompts 目录新增地缘政治分析模板文件
- `skill-ymos-market-insight`: P13 SOP 中注册地缘政治模板为可选增强维度

## Impact

- 新增文件：`skills/ymos-core/templates/geopolitical-analysis.md`
- 修改文件：`skills/ymos-market-insight/SKILL.md`（P13 引用地缘政治模板）
- 无 CLI 代码变更，纯 prompt/模板层改动
- 不破坏现有流程，地缘政治分析为条件触发的可选模块
