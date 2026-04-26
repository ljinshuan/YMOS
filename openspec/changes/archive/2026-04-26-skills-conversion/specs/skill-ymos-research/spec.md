## ADDED Requirements

### Requirement: Research skill triggers
The ymos-research skill SHALL trigger on `调研一下 [ticker]` and be callable by other skills.

#### Scenario: Direct trigger
- **WHEN** user says "调研一下 NVDA"
- **THEN** skill executes P1 → P4 → P2 → P9 pipeline for NVDA

#### Scenario: Called by strategy skill
- **WHEN** ymos-strategy discovers missing P1/P4 data for a ticker
- **THEN** strategy skill references this skill's SOP (references/sops/research.md) and executes the research flow

### Requirement: Research is independently usable
The skill SHALL function as a standalone capability that users can trigger directly without any prerequisites.

#### Scenario: Research new ticker
- **WHEN** user says "调研一下 TSLA" for a ticker not in any state machine
- **THEN** skill creates knowledge base, runs P1+P4+P2+P9, outputs results

### Requirement: Research updates state machine P4
The skill SHALL write P4 summary back to the corresponding state machine row.

#### Scenario: Update watchlist P4
- **WHEN** research completes for a watchlist ticker
- **THEN** skill runs `ymos state update watchlist --ticker TICKER --field P4重点关注点 --value "summary"`
