## MODIFIED Requirements

### Requirement: P12 prompt 包含行为偏误扫描模块
`skills/ymos-core/prompts/p12-referee.md` MUST 包含行为偏误扫描模块，位于"死亡边界扫描"之后、verdict 之前。

#### Scenario: P12 执行顺序
- **WHEN** Agent 执行 P12 Referee
- **THEN** 执行顺序为：死亡边界扫描 → 行为偏误扫描 → 综合 verdict
