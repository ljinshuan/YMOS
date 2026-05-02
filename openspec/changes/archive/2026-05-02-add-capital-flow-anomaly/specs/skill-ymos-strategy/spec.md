## ADDED Requirements

### Requirement: Strategy uses capital flow as confirmation
The ymos-strategy skill SHALL use capital flow data as a confirmation signal in buy/add position routes.

#### Scenario: Buy route with capital flow confirmation
- **WHEN** strategy executes Route A (buy) and capital flow shows main force net inflow over 3 consecutive days
- **THEN** P12 (Referee) analysis SHALL include "资金面确认：主力资金连续净流入" as a positive factor

#### Scenario: Buy route with capital flow warning
- **WHEN** strategy executes Route A (buy) and capital flow shows significant main force net outflow
- **THEN** P12 (Referee) analysis SHALL include "资金面警告：主力资金持续流出" as a risk factor

#### Scenario: Capital flow data not available
- **WHEN** strategy executes and no capital flow data exists for the ticker
- **THEN** strategy proceeds without capital flow confirmation (non-blocking), noting "资金流数据缺失，跳过资金面确认"
