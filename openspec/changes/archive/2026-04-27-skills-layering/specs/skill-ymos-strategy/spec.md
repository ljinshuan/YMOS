## MODIFIED Requirements

### Requirement: skill 文档自包含
ymos-strategy SHALL 将其 SOP 和独占 prompts 纳入 skill 目录内部。SOP 存放于 `skills/ymos-strategy/sop.md`，独占 prompts 存放于 `skills/ymos-strategy/prompts/`。

独占 prompts：p3-event-impact、p5-fomo-killer、p6-profit-keeper、p7-portfolio-check、p8-macro-filter、p10-options、p11-autopsy、p12-referee、p17-position-sizing。

#### Scenario: strategy skill 引用独占 prompt
- **WHEN** ymos-strategy 执行买入路由需要 p5-fomo-killer
- **THEN** 引用路径 SHALL 为 `skills/ymos-strategy/prompts/p5-fomo-killer.md`（skill 内相对路径）

#### Scenario: strategy skill 引用共享 prompt
- **WHEN** ymos-strategy 需要使用 p2-phase-check
- **THEN** 引用路径 SHALL 为 `skills/ymos-core/prompts/p2-phase-check.md`（跨 skill 绝对路径）

#### Scenario: strategy skill 引用自己的 SOP
- **WHEN** ymos-strategy 需要查看详细执行步骤
- **THEN** 引用路径 SHALL 为 `skills/ymos-strategy/sop.md`
