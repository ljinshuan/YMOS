## Why

skills/ 目录下多个 MD 文件过长（最大 20KB/424 行），agent 在执行工作流时必须全量读取，即使只需要其中一小段内容。这导致每次会话浪费 ~10-20KB 的 input tokens，且随着 skill 数量增长会持续恶化。

## What Changes

- 将大型 SOP 文件按路由/步骤拆分为独立小文件，agent 按需读取对应段落
- 将大型 P-series prompt 按结构层拆分（如 p1-genesis 的"分类层"和"深度层"）
- 将大型 knowledge 文件按主题拆分
- 每个拆分后的原文件保留为"索引文件"（公共部分 + 子文件路径索引），让现有路由机制无缝衔接

## Capabilities

### New Capabilities
- `md-structure-split`: 定义 MD 文件拆分的规则、阈值和索引文件格式，确保 agent 路由机制不受影响

### Modified Capabilities

## Impact

- `skills/` 目录下约 8-10 个大型 MD 文件结构变更
- SKILL.md 和路由相关的引用路径需同步更新
- 现有 agent 读取逻辑无需改动（Read 工具天然支持 offset/limit，拆分后反而更自然）
- 无代码变更，纯文档结构优化
