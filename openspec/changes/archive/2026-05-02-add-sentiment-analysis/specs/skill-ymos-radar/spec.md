## ADDED Requirements

### Requirement: Radar detects sentiment extremes
The ymos-radar skill SHALL detect extreme sentiment signals as part of the radar pipeline.

#### Scenario: Extreme bullish sentiment warning
- **WHEN** radar runs and sentiment data shows bullish percentage > 80% for a ticker
- **THEN** radar report includes a Tier 1 warning: "市场情绪极度乐观，注意反向风险"

#### Scenario: Extreme bearish sentiment opportunity
- **WHEN** radar runs and sentiment data shows bearish percentage > 70% for a ticker
- **THEN** radar report includes a Tier 2 note: "市场情绪极度悲观，可能存在逆向机会"
