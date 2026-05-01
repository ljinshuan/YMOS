## MODIFIED Requirements

### Requirement: P8 prompt 包含辩论模式
`skills/ymos-core/prompts/p8-macro-filter.md` MUST 包含辩论模式章节，作为原有三维度评级的后续分析环节。

#### Scenario: P8 prompt 被完整执行
- **WHEN** Agent 读取并执行 P8 prompt
- **THEN** 执行顺序为：三维度评级 → 辩论模式 → 辩结论
