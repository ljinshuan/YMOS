## MODIFIED Requirements

### Requirement: Strategy uses capital flow as confirmation
The ymos-strategy skill SHALL use capital flow and option data as confirmation signals in buy/add position routes.

#### Scenario: Buy route with capital flow confirmation
- **WHEN** strategy executes Route A (buy) and capital flow shows main force net inflow over 3 consecutive days
- **THEN** P12 (Referee) analysis SHALL include "资金面确认：主力资金连续净流入" as a positive factor

#### Scenario: Buy route with capital flow warning
- **WHEN** strategy executes Route A (buy) and capital flow shows significant main force net outflow
- **THEN** P12 (Referee) analysis SHALL include "资金面警告：主力资金持续流出" as a risk factor

#### Scenario: Buy route with option confirmation
- **WHEN** strategy executes Route A (buy) and option data shows: (1) IV below historical 30th percentile, (2) PCR < 0.7 (call skew), (3) call OI increasing
- **THEN** P12 analysis SHALL include "期权情绪确认：看涨期权溢价收窄、PCR 偏低、持仓量上升" as a positive factor

#### Scenario: Buy route with option warning
- **WHEN** strategy executes Route A (buy) and option data shows: (1) IV above historical 80th percentile, (2) PCR > 1.5 (put skew), (3) large put block trades
- **THEN** P12 analysis SHALL include "期权风险提示：隐含波动率高位、看跌期权持仓集中、大额看跌期权交易" as a risk factor

#### Scenario: Capital flow and option data not available
- **WHEN** strategy executes and no capital flow or option data exists for the ticker
- **THEN** strategy proceeds without these confirmations (non-blocking), noting "资金流/期权数据缺失，跳过资金面和期权情绪确认"

### Requirement: Strategy P12 option sentiment analysis
The ymos-strategy skill SHALL incorporate option market sentiment signals into P12 (Referee) analysis.

#### Scenario: 买入路径的期权正面信号
- **WHEN** analyzing a buy position candidate and option data shows: IV low relative to history, PCR skewed to calls, minimal put block activity
- **THEN** P12 lists "期权市场情绪偏乐观（IV 低、PCR 偏低、无明显看跌保护）" as supporting evidence

#### Scenario: 买入路径的期权负面信号
- **WHEN** analyzing a buy position candidate and option data shows: IV at multi-month high, PCR above 1.5, significant put block trades at OTM strikes
- **THEN** P12 lists "期权市场显示避险需求上升（IV 高位、PCR 偏高、大额看跌期权护盘）" as risk concern

#### Scenario: 持有路径的期权监控信号
- **WHEN** analyzing a hold position and option data shows: IV unchanged, PCR stable, no unusual activity
- **THEN** P12 notes "期权市场情绪平稳，无明显异动"

#### Scenario: 减仓路径的期权预警信号
- **WHEN** analyzing a reduce position route and option data shows: IV spiking, PCR > 2.0, aggressive put buying
- **THEN** P12 flags "期权市场恐慌信号（IV 激增、PCR 暴涨、看跌期权抢筹）" as early warning
