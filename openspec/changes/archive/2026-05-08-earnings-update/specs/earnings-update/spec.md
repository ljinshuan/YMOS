## ADDED Requirements

### Requirement: 财报数据收集
系统 SHALL 收集财报相关的核心数据。

#### Scenario: 财报数据输入
- **WHEN** 用户开始财报分析
- **THEN** 系统收集以下数据：
  - 财报期间（Q1/Q2/Q3/Q4）
  - 收入
  - 毛利润/毛利率
  - 营业利润/营业利润率
  - 净利润
  - EPS（摊薄/基本）
  - 现金余额
  - 债务水平
  - 关键运营指标

#### Scenario: 预期数据获取
- **WHEN** 收集财报数据
- **THEN** 系统同时获取或提示用户输入市场预期：
  - 收入预期
  - EPS 预期
  - 其他关键指标预期

#### Scenario: 历史数据获取
- **WHEN** 生成财报报告
- **THEN** 系统获取近 4 个季度的历史数据用于趋势分析

### Requirement: Beat/Miss 分析
系统 SHALL 标准化分析财报表现与预期的差异。

#### Scenario: Beat/Miss 计算
- **WHEN** 分析财报表现
- **THEN** 系统计算：
  - 绝对差异（实际值 - 预期值）
  - 相对差异（%）
  - 结果分类（Beat/Miss/In-line）

#### Scenario: 差异解释
- **WHEN** 财报与预期存在显著差异
- **THEN** 系统分析可能的原因：
  - 宏观因素
  - 行业因素
  - 公司特定因素
  - 一次性项目

### Requirement: 执行摘要
系统 SHALL 生成简明的执行摘要。

#### Scenario: 执行摘要内容
- **WHEN** 生成财报报告
- **THEN** 执行摘要包含：
  - 核心财务表现（Beat/Miss/In-line）
  - 关键亮点
  - 主要担忧
  - 整体评价（积极/中性/消极）

#### Scenario: 执行摘要长度
- **WHEN** 生成执行摘要
- **THEN** 长度控制在 1-2 段话

### Requirement: 数据源引用
系统 SHALL 提供完整的数据来源引用。

#### Scenario: 数据源列表
- **WHEN** 生成财报报告
- **THEN** 系统列出所有数据源，包括：
  - 财报发布（公司官网）
  - 10-Q/10-K（SEC EDGAR）
  - 财报电话会议（公司官网/Seeking Alpha）
  - 投资者演示（公司官网）
  - 预期数据（Bloomberg/FactSet）

#### Scenario: 超链接
- **WHEN** 引用数据源
- **THEN** 每个引用包含可点击的超链接

### Requirement: 分部/业务线分析
系统 SHALL 支持分部或业务线的详细分析。

#### Scenario: 分部数据展示
- **WHEN** 公司有多个业务分部
- **THEN** 系统展示各分部的：
  - 收入及增长
  - 利润率
  - 对整体贡献

#### Scenario: 分部变化分析
- **WHEN** 分析分部表现
- **THEN** 系统指出各分部与上期的变化

### Requirement: 前瞻指引分析
系统 SHALL 分析管理层的前瞻指引。

#### Scenario: 指引对比
- **WHEN** 公司提供前瞻指引
- **THEN** 系统对比：
  - 当前指引 vs. 上期指引
  - 当前指引 vs. 市场预期
  - 指引变化的原因

#### Scenario: 指引缺失
- **WHEN** 公司未提供前瞻指引
- **THEN** 系统明确标注"未提供指引"

### Requirement: 估值影响分析
系统 SHALL 分析财报对估值的影响。

#### Scenario: 估值变化
- **WHEN** 分析估值影响
- **THEN** 系统提供：
  - 基于财报数据的估值变化
  - 与当前市价的对比
  - 简要的投资含义（不作为投资建议）

#### Scenario: 估值方法
- **WHEN** 分析估值影响
- **THEN** 系统明确说明估值方法（DCF/可比公司等）

### Requirement: 趋势数据展示
系统 SHALL 展示关键指标的历史趋势。

#### Scenario: 近 4 季度数据
- **WHEN** 生成财报报告
- **THEN** 系统展示近 4 个季度的：
  - 收入趋势
  - 利润率趋势
  - EPS 趋势

#### Scenario: 同比/环比
- **WHEN** 展示趋势数据
- **THEN** 系统同时提供同比和环比数据

### Requirement: 报告生成
系统 SHALL 生成结构化的财报报告。

#### Scenario: 报告结构
- **WHEN** 生成财报报告
- **THEN** 报告包含以下章节：
  1. 标题（公司名称 + 财报期间）
  2. 执行摘要
  3. 关键财务数据
  4. Beat/Miss 分析
  5. 分部/业务线分析
  6. 前瞻指引
  7. 估值影响
  8. 数据来源

#### Scenario: 报告格式
- **WHEN** 生成财报报告
- **THEN** 系统使用 Markdown 格式

### Requirement: 与现有 Skill 集成
系统 SHALL 与现有 YMOS skill 集成。

#### Scenario: ymos-radar 集成
- **WHEN** ymos-radar 检测到财报事件
- **THEN** 系统询问用户是否生成财报报告

#### Scenario: ymos-strategy 集成
- **WHEN** ymos-strategy 分析投资决策
- **THEN** 系统可引用最新的财报分析结果

#### Scenario: 历史报告引用
- **WHEN** 同一标的已有历史财报报告
- **THEN** 系统可引用历史数据做对比

### Requirement: 报告管理
系统 SHALL 管理财报报告的存储和归档。

#### Scenario: 报告命名
- **WHEN** 保存财报报告
- **THEN** 文件名格式为 `{ticker}_Q{Q}_{FY}_财报报告.md`

#### Scenario: 报告归档
- **WHEN** 生成新财报报告
- **THEN** 系统归档到 `data/reports/earnings/{ticker}/YYYY/` 目录

#### Scenario: 同日覆盖
- **WHEN** 同一标的、同一期间已存在报告
- **THEN** 系统覆盖旧报告
