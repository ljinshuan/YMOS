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

### Requirement: Strategy auto-calls research for missing data
The skill SHALL invoke ymos-research when P1/P4/P2 data is missing for a target ticker.

#### Scenario: Missing P1 data
- **WHEN** strategy analysis starts for a ticker without P1 in its knowledge base
- **THEN** skill executes ymos-research flow (reads references/sops/research.md) to generate P1+P4+P2

### Requirement: Strategy writes back to state and stock folders
The skill SHALL use CLI commands to update state machines and save reports to stock folders.

#### Scenario: Save strategy report
- **WHEN** a strategy analysis completes
- **THEN** report is saved to data/reports/strategy/ and then moved to the stock's directory under data/stocks/

