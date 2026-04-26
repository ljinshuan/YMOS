## MODIFIED Requirements

### Requirement: skill 文档自包含
ymos-research SHALL 将其 SOP 和独占 prompts 纳入 skill 目录内部。SOP 存放于 `skills/ymos-research/sop.md`，独占 prompts 存放于 `skills/ymos-research/prompts/`。

独占 prompts：p1-genesis、p4-radar。

#### Scenario: research skill 引用独占 prompt
- **WHEN** ymos-research 执行 P1 Genesis 基石建档
- **THEN** 引用路径 SHALL 为 `skills/ymos-research/prompts/p1-genesis.md`

#### Scenario: research skill 引用共享 prompt
- **WHEN** ymos-research 需要使用 p2-phase-check
- **THEN** 引用路径 SHALL 为 `skills/ymos-core/prompts/p2-phase-check.md`

#### Scenario: research skill 引用自己的 SOP
- **WHEN** ymos-research 需要查看详细执行步骤
- **THEN** 引用路径 SHALL 为 `skills/ymos-research/sop.md`
