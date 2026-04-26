# skill-ymos-strategy Specification

## Purpose
TBD - created by archiving change skills-conversion. Update Purpose after archive.
## Requirements
### Requirement: Strategy skill triggers
The ymos-strategy skill SHALL trigger on `我想买 [ticker]`, `加仓 [ticker]`, `我想卖 [ticker]`, `持有怎么看 [ticker]`, `做个仓位再平衡`, and `跑一下策略分析`.

#### Scenario: Buy routing
- **WHEN** user says "我想买 NVDA"
- **THEN** skill routes to Route A: P2 → P9 → P5 → P12 → P17 → Human decision

#### Scenario: Batch from radar
- **WHEN** user says "跑一下策略分析"
- **THEN** skill reads latest radar report, extracts strategy suggestions, executes analysis for each suggested ticker

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

### Requirement: Strategy auto-calls research for missing data
The skill SHALL invoke ymos-research when P1/P4/P2 data is missing for a target ticker.

#### Scenario: Missing P1 data
- **WHEN** strategy analysis starts for a ticker without P1 in its knowledge base
- **THEN** skill executes ymos-research flow (reads skills/ymos-research/sop.md) to generate P1+P4+P2

### Requirement: Strategy writes back to state and stock folders
The skill SHALL use CLI commands to update state machines and save reports to stock folders.

#### Scenario: Save strategy report
- **WHEN** a strategy analysis completes
- **THEN** report is saved to data/reports/strategy/ and then moved to the stock's directory under data/stocks/

