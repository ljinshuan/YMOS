## Why

P8 Macro Filter 当前是单向压力测试——对宏观因素做高风险/中性/有利三档评级，但缺乏对立视角的碰撞。投资者最常见的宏观误判来自确认偏误：只看到支持自己持仓方向的宏观信号。参考 FinceptTerminal 的 6 经济学派辩论 Agent 设计，将 P8 升级为"辩论模式"，强制 LLM 先 steelman 对立面再给结论。

## What Changes

- 重构 P8 Macro Filter prompt，增加"辩论模式"环节
- 引入 2-3 个核心对立经济学派视角（凯恩斯主义 vs 奥地利学派 vs 重商主义）
- 每个学派视角独立分析同一宏观问题，输出各自的传导路径判断
- 最终综合环节必须标注"最强反对论点"和"该论点为何被否决/被采纳"
- P8 输出增加"辩结论"字段，区别于原有的单向评级

## Capabilities

### New Capabilities
- `prompt-p8-debate-mode`: P8 辩论模式增强，包含多学派视角模板、steelman 反驳格式、辩结论输出结构

### Modified Capabilities
- `ymos-core`: 更新 `prompts/p8-macro-filter.md`，增加辩论模式章节
- `skill-ymos-strategy`: P8 输出格式变更影响 Route C 和 Route E 的消费方

## Impact

- 修改文件：`skills/ymos-core/prompts/p8-macro-filter.md`
- 可能影响：`skills/ymos-strategy/SKILL.md`（如果 Route C/E 需要适配新输出格式）
- 无 CLI 代码变更，纯 prompt 层改动
- 不破坏现有流程，辩论模式为 P8 的增强而非替换
