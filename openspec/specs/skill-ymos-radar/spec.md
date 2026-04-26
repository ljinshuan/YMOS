# skill-ymos-radar Specification

## Purpose
TBD - created by archiving change skills-conversion. Update Purpose after archive.
## Requirements
### Requirement: Radar skill triggers
The ymos-radar skill SHALL trigger on `跑一下投资雷达`, `查一下价格`, and `看看有什么信号`.

#### Scenario: Full radar pipeline
- **WHEN** user says "跑一下投资雷达"
- **THEN** skill executes: load state → load market insight (auto-trigger market-insight if missing) → price scan → 7-day trend analysis → generate bridge report

#### Scenario: Price only
- **WHEN** user says "查一下价格"
- **THEN** skill runs `ymos price-scan --from-state` and shows results without full report

### Requirement: Radar auto-triggers market insight
The skill SHALL automatically trigger ymos-market-insight if today's insight report does not exist.

#### Scenario: Missing today's insight
- **WHEN** radar skill starts and data/reports/market-insight/ has no report for today
- **THEN** skill executes ymos-market-insight pipeline first, then continues with radar

### Requirement: Radar writes back state
The skill SHALL use `ymos state update` to write P4 focus points and price updates back to state machines.

#### Scenario: Update P4 in state machine
- **WHEN** radar analysis produces updated P4 focus points for a ticker
- **THEN** skill runs `ymos state update holdings --ticker TICKER --field P4重点关注点 --value "new summary"`

