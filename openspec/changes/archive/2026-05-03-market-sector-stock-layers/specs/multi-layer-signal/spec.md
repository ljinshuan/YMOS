## ADDED Requirements

### Requirement: 三层信号数据获取
系统 SHALL 在 radar 流程中自动获取大盘和板块 ETF 的价格与技术面数据。

#### Scenario: 大盘 ETF 价格和技术面扫描
- **WHEN** radar 流程执行价格扫描步骤
- **THEN** 系统先执行 `ymos price-scan --symbols <大盘ETF列表>` 和 `ymos tech-analysis analyze --symbols <大盘ETF列表>`，获取大盘 ETF 的价格和完整技术指标

#### Scenario: 板块 ETF 价格和技术面扫描
- **WHEN** radar 流程执行价格扫描步骤
- **THEN** 系统读取 `sector_mapping.md`，提取持仓涉及的所有板块 ETF，执行 `ymos price-scan --symbols <板块ETF列表>` 和 `ymos tech-analysis analyze --symbols <板块ETF列表>`

#### Scenario: 扫描结果持久化
- **WHEN** 大盘和板块 ETF 扫描完成
- **THEN** 价格 JSON 保存到 `data/reports/radar/raw/YYYY-MM/`，技术面报告保存到 `data/reports/tech/YYYY-MM/`

### Requirement: 三层信号联动判断
系统 SHALL 在雷达桥接报告中输出「三层信号联动」section，综合大盘、板块、个股三个层级的趋势判断。

#### Scenario: 顺风判断
- **WHEN** 大盘 verdict 为「偏多」且持仓所属板块 verdict 为「偏多」
- **THEN** 三层联动标记为「顺风」，个股看多信号权重增加

#### Scenario: 逆风判断
- **WHEN** 大盘 verdict 为「偏空」或板块 verdict 为「偏空」
- **THEN** 三层联动标记为「逆风」，个股看多信号需要更强的逻辑支撑

#### Scenario: 混合判断
- **WHEN** 大盘偏多但板块偏空（或反之）
- **THEN** 三层联动标记为「分化」，报告需说明大盘与板块的矛盾点

### Requirement: 三层信号注入策略分析
系统 SHALL 在 ymos-strategy 流程中读取雷达报告的三层信号，作为策略路由的上下文输入。

#### Scenario: 策略分析引用三层信号
- **WHEN** ymos-strategy 读取最新的雷达桥接报告
- **THEN** 策略分析 SHALL 引用该 ticker 对应的板块和大盘信号，在 P5/P6 分析中纳入顺风/逆风判断

### Requirement: 板块显著信号触发 P14
系统 SHALL 在 radar 流程中，当板块 ETF 技术分析出现显著信号时自动触发 P14 板块猎手。

#### Scenario: 板块偏多触发 P14
- **WHEN** 某板块 ETF 技术分析 verdict 为「偏多⬆」
- **THEN** 自动对持仓中该板块的个股触发 P14 板块猎手分析

#### Scenario: 板块偏空触发 P14
- **WHEN** 某板块 ETF 技术分析 verdict 为「偏空⬇」
- **THEN** 自动对持仓中该板块的个股触发 P14 板块猎手，标注风险

#### Scenario: 板块中性不触发
- **WHEN** 某板块 ETF 技术分析 verdict 为「中性➡」
- **THEN** 跳过 P14，仅保留技术面数据在报告中
