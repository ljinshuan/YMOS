## MODIFIED Requirements

### Requirement: Radar 桥接报告 section 结构
ymos-radar 桥接报告 SHALL 包含以下 section：价格扫描、技术分析、资金流异动、衍生品信号（可选）、期权市场情绪（可选）、三层信号联动、综合判断。

#### Scenario: 完整桥接报告包含期权 section
- **WHEN** radar 流程完成且 OpenD 可用且用户启用期权分析
- **THEN** 桥接报告包含「期权市场情绪」独立 section，展示 IV 曲面、PCR、未平仓变化

#### Scenario: OpenD 不可用时跳过期权 section
- **WHEN** radar 流程完成但 OpenD 不可用
- **THEN** 桥接报告跳过期权 section，或显示"期权数据不可用（OpenD 未连接）"

## ADDED Requirements

### Requirement: Radar 集成期权数据分析
The ymos-radar skill SHALL optionally integrate option chain data analysis into the bridge report.

#### Scenario: 自动获取期权数据
- **WHEN** radar 流程完成价格扫描和资金流分析，且 OpenD 可用
- **THEN** skill runs `ymos fetch-option-chain --from-state` to get option data for all held/watched tickers

#### Scenario: 期权数据写入状态机
- **WHEN** option chain data is fetched successfully
- **THEN** skill stores the data to `data/reports/radar/raw/option_chain_YYYYMMDD.json`

#### Scenario: 期权分析 prompt 调用
- **WHEN** option chain data is available
- **THEN** skill applies a dedicated option analysis prompt (P-option-sentiment) to generate insights: IV level/ranking, Put/Call Ratio skew, OI concentration, unusual option activity

#### Scenario: 桥接报告期权 section
- **WHEN** radar generates the bridge report and option analysis is available
- **THEN** report includes "期权市场情绪" section with: IV 分位数、PCR、大额期权交易、未平仓变化趋势

### Requirement: Radar 期权数据可选开关
The ymos-radar skill SHALL support optional option data fetching via a flag or user preference.

#### Scenario: 显式启用期权分析
- **WHEN** user runs ymos-radar with `--with-options` flag or preference enabled
- **THEN** skill includes option data fetching and analysis

#### Scenario: 默认不包含期权分析
- **WHEN** user runs ymos-radar without options flag and no preference set
- **THEN** skill skips option data fetching (for performance), report does not include option section
