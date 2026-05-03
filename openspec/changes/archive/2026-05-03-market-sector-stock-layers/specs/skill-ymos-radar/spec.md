## MODIFIED Requirements

### Requirement: Radar skill triggers
The ymos-radar skill SHALL trigger on `跑一下投资雷达`, `查一下价格`, `看看有什么信号`, and additionally `查一下资金流`, `有什么资金异动`.

#### Scenario: Full radar pipeline
- **WHEN** user says "跑一下投资雷达"
- **THEN** skill executes: load state → load market insight (auto-trigger market-insight if missing) → **大盘+板块 ETF 价格扫描和技术分析** → price scan (个股) → **capital flow scan** → 7-day trend analysis → **三层信号联动综合判断** → generate bridge report

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

## ADDED Requirements

### Requirement: Radar 扫描大盘和板块 ETF
ymos-radar SHALL 在个股价格扫描之前，先执行大盘锚点和板块 ETF 的价格扫描与技术分析。

#### Scenario: 大盘锚点扫描
- **WHEN** radar 流程开始价格扫描阶段
- **THEN** 读取 `data/state/market_anchors.md`，执行 `ymos price-scan --symbols <大盘ETF列表>` 和 `ymos tech-analysis analyze --symbols <大盘ETF列表>`

#### Scenario: 板块 ETF 扫描
- **WHEN** radar 流程完成大盘扫描后
- **THEN** 读取 `data/state/sector_mapping.md`，提取持仓涉及的板块 ETF，执行 `ymos price-scan --symbols <板块ETF列表>` 和 `ymos tech-analysis analyze --symbols <板块ETF列表>`

#### Scenario: 桥接报告新增三层信号 section
- **WHEN** 雷达桥接报告生成时
- **THEN** 报告包含「三层信号联动」独立 section，展示大盘 verdict → 板块 verdict → 个股信号的综合判断，标注顺风/逆风/分化

#### Scenario: 板块显著信号触发 P14
- **WHEN** 板块 ETF 技术分析 verdict 为「偏多⬆」或「偏空⬇」
- **THEN** 自动触发 P14 板块猎手对该板块做深度分析，结果纳入雷达报告
