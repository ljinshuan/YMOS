## MODIFIED Requirements

### Requirement: Radar skill triggers
The ymos-radar skill SHALL trigger on `跑一下投资雷达`, `查一下价格`, `看看有什么信号`, and additionally `查一下资金流`, `有什么资金异动`.

#### Scenario: Full radar pipeline
- **WHEN** user says "跑一下投资雷达"
- **THEN** skill executes: load state → load market insight (auto-trigger market-insight if missing) → price scan → **capital flow scan** → 7-day trend analysis → generate bridge report

#### Scenario: Price only
- **WHEN** user says "查一下价格"
- **THEN** skill runs `ymos price-scan --from-state` and shows results without full report

#### Scenario: Capital flow only
- **WHEN** user says "查一下资金流" or "有什么资金异动"
- **THEN** skill runs `ymos fetch-capital-flow --from-state`, applies P20-capital-anomaly prompt, shows anomaly signals

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

#### Scenario: Update P4 with capital flow signal
- **WHEN** capital flow anomaly is detected for a ticker
- **THEN** skill appends capital flow signal to the P4 focus point update, e.g., "资金面：主力连续3日净流入"
