## ADDED Requirements

### Requirement: Reconcile skill triggers
The ymos-reconcile skill SHALL trigger on `收口一下`, `刷新持仓视图`, and `跑一下持仓收口`.

#### Scenario: Full reconciliation
- **WHEN** user says "收口一下"
- **THEN** skill reads all state + reports, validates consistency, generates memo view and dashboard HTML

### Requirement: Consistency validation
The skill SHALL validate that strategy analysis writes are correctly reflected in state machines.

#### Scenario: Missing state machine update
- **WHEN** a strategy report exists for a ticker but the state machine has no corresponding update
- **THEN** skill patches the state machine using `ymos state update` and logs the gap

### Requirement: Dashboard generation
The skill SHALL generate a self-contained HTML dashboard file.

#### Scenario: Generate dashboard
- **WHEN** reconcile completes
- **THEN** HTML file is written to data/dashboard/YYYY-MM/dashboard_YYYY-MM-DD.html with all required layout sections
