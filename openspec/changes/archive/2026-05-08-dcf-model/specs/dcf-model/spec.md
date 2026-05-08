## ADDED Requirements

### Requirement: 现金流预测
系统 SHALL 支持预测未来 5-10 年的自由现金流。

#### Scenario: 现金流预测输入
- **WHEN** 用户开始 DCF 分析
- **THEN** 系统收集以下输入：
  - 预测期（5-10 年）
  - 收入增长率（每年或分段）
  - EBITDA 利润率或营业利润率
  - 折旧与摊销占收入比例
  - 资本支出占收入比例
  - 营运资本占收入比例
  - 税率

#### Scenario: 自由现金流计算
- **WHEN** 计算自由现金流
- **THEN** 系统使用公式：FCF = EBIT × (1 - T) + D&A - CapEx - ΔWC

#### Scenario: 历史数据参考
- **WHEN** 用户输入预测参数
- **THEN** 系统显示历史 3-5 年的同类数据作为参考

### Requirement: WACC 计算
系统 SHALL 计算加权平均资本成本。

#### Scenario: CAPM 模型
- **WHEN** 计算权益成本
- **THEN** 系统使用 CAPM 公式：Re = Rf + β × (Rm - Rf)
- **AND** 用户可输入或使用默认值：
  - Rf（无风险利率）
  - β（Beta 系数）
  - Rm - Rf（市场风险溢价）

#### Scenario: 债务成本
- **WHEN** 计算债务成本
- **THEN** 系统使用当前利率或用户输入的债务成本

#### Scenario: WACC 汇总
- **WHEN** 计算最终 WACC
- **THEN** 系统使用公式：WACC = (E/V × Re) + (D/V × Rd × (1 - Tc))
- **AND** 显示权益占比、债务占比、有效税率

### Requirement: 终值计算
系统 SHALL 支持两种终值计算方法。

#### Scenario: 永续增长法
- **WHEN** 使用永续增长法
- **THEN** 系统计算：TV = FCF_n × (1 + g) / (WACC - g)
- **AND** 用户可输入永续增长率 g

#### Scenario: 退出倍数法
- **WHEN** 使用退出倍数法
- **THEN** 系统计算：TV = EBITDA_n × Exit Multiple
- **AND** 用户可输入退出倍数

#### Scenario: 终值对比
- **WHEN** 两种方法都计算
- **THEN** 系统显示两种方法的结果和差异
- **AND** 建议使用更合理的值或取平均值

### Requirement: 估值计算
系统 SHALL 计算企业价值和股权价值。

#### Scenario: 现值计算
- **WHEN** 计算现金流现值
- **THEN** 系统将每期现金流按 WACC 折现到当前

#### Scenario: 终值现值计算
- **WHEN** 计算终值现值
- **THEN** 系统将终值按 WACC 折现到预测期末，再折现到当前

#### Scenario: 企业价值计算
- **WHEN** 计算企业价值
- **THEN** 系统汇总：企业价值 = Σ(FCF 现值) + 终值现值

#### Scenario: 股权价值计算
- **WHEN** 计算股权价值
- **THEN** 系统计算：股权价值 = 企业价值 - 净债务

#### Scenario: 每股价值计算
- **WHEN** 计算每股价值
- **THEN** 系统计算：每股价值 = 股权价值 / 总股本

### Requirement: 敏感性分析
系统 SHALL 提供双变量敏感性分析。

#### Scenario: WACC vs. 永续增长率
- **WHEN** 生成敏感性分析
- **THEN** 系统创建 WACC（7%-13%）vs. 永续增长率（1%-4%）的二维表
- **AND** 每个单元格显示估值

#### Scenario: 收入增长 vs. 利润率
- **WHEN** 生成敏感性分析
- **THEN** 系统创建收入增长率（-5% 至 20%）vs. 利润率（X% ± 5%）的二维表

#### Scenario: 条件格式化
- **WHEN** 生成敏感性表
- **THEN** 系统使用条件格式高亮显示高/低估值

### Requirement: 情景分析
系统 SHALL 提供三情景对比分析。

#### Scenario: 乐观情景
- **WHEN** 定义乐观情景
- **THEN** 系统使用高于基准的假设：
  - 更高的收入增长率
  - 更高的利润率
  - 更低的 WACC
  - 更高的退出倍数

#### Scenario: 悲观情景
- **WHEN** 定义悲观情景
- **THEN** 系统使用低于基准的假设：
  - 更低的收入增长率
  - 更低的利润率
  - 更高的 WACC
  - 更低的退出倍数

#### Scenario: 概率加权
- **WHEN** 用户为每个情景分配概率
- **THEN** 系统计算概率加权估值

### Requirement: Excel 模型生成
系统 SHALL 生成完整的 Excel DCF 模型。

#### Scenario: 多 Sheet 结构
- **WHEN** 生成 Excel 模型
- **THEN** 系统创建以下 Sheet：
  - Assumptions（假设）
  - Free Cash Flow（现金流）
  - WACC（资本成本）
  - Terminal Value（终值）
  - Valuation（估值）
  - Sensitivity（敏感性）
  - Scenarios（情景）

#### Scenario: 公式使用
- **WHEN** 生成 Excel 模型
- **THEN** 所有计算使用 Excel 公式，非硬编码值

#### Scenario: 格式化
- **WHEN** 生成 Excel 模型
- **THEN** 应用专业格式化（标题、表头、数据行、统计行）

### Requirement: 与现有 Skill 集成
系统 SHALL 与现有 YMOS skill 集成。

#### Scenario: ymos-research 集成
- **WHEN** ymos-research 执行 P9 估值
- **THEN** 系统询问是否生成完整 DCF 模型

#### Scenario: ymos-strategy 集成
- **WHEN** ymos-strategy 分析买入/卖出决策
- **THEN** 系统读取并显示 DCF 估值结果

#### Scenario: 历史对比
- **WHEN** 同一标的存在历史 DCF 模型
- **THEN** 系统显示历史预测 vs 当前预测的对比

### Requirement: 报告生成
系统 SHALL 生成 DCF 分析报告。

#### Scenario: 执行摘要
- **WHEN** 生成 DCF 报告
- **THEN** 系统包含：
  - 基准情景估值
  - 每股价值
  - 与当前市价对比
  - 关键假设
  - 估值范围（敏感性分析）

#### Scenario: 详细假设
- **WHEN** 生成 DCF 报告
- **THEN** 系统列出所有输入假设及其来源

#### Scenario: 风险提示
- **WHEN** 生成 DCF 报告
- **THEN** 系统包含：
  - 关键风险因素
  - 假设敏感性分析
  - 建议的后续验证
