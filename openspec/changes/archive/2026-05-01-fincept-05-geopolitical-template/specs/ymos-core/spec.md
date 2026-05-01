## MODIFIED Requirements

### Requirement: 地缘政治模板放置在共享 templates 目录
`skills/ymos-core/templates/` 目录 MUST 包含 `geopolitical-analysis.md` 文件。

#### Scenario: 模板可被多个 skill 引用
- **WHEN** P13 或 P3 需要地缘政治分析模板
- **THEN** 从 `skills/ymos-core/templates/geopolitical-analysis.md` 路径读取
