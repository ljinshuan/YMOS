## MODIFIED Requirements

### Requirement: Strategy skill triggers
The ymos-strategy skill SHALL trigger on `我想买 [ticker]`, `加仓 [ticker]`, `我想卖 [ticker]`, `持有怎么看 [ticker]`, `做个仓位再平衡`, `跑一下策略分析`, and additionally `看一下 [ticker] 的情绪`, `[ticker] 多空怎么样`.

#### Scenario: Buy routing
- **WHEN** user says "我想买 NVDA"
- **THEN** skill routes to Route A: P2 → P9 → P5 → P12 → P17 → Human decision

#### Scenario: Batch from radar
- **WHEN** user says "跑一下策略分析"
- **THEN** skill reads latest radar report, extracts strategy suggestions, executes analysis for each suggested ticker

#### Scenario: Sentiment-aware strategy
- **WHEN** user says "我想买 NVDA，先看一下情绪"
- **THEN** skill fetches sentiment data for NVDA, incorporates sentiment signals as auxiliary input in P5 (FOMO Killer) and P12 (Referee) analysis
