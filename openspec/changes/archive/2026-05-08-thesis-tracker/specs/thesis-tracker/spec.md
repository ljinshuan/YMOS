## ADDED Requirements

### Requirement: 论点初始化
系统 SHALL 在用户首次为某个标的创建论点追踪时，引导用户完成论点定义。

#### Scenario: 首次创建论点追踪
- **WHEN** 用户调用 `/ymos-thesis-tracker` 或 ymos-research 完成后选择初始化
- **THEN** 系统提示用户输入：
  - 标的名称和 ticker
  - 仓位状态（Long/Short）
  - 论点陈述（1-2 句话核心论点）
  - 关键支柱（3-5 个）
  - 关键风险（3-5 个）
  - 目标价格/估值
  - 止损触发条件

#### Scenario: 从个股基础知识库自动填充
- **WHEN** 个股文件夹中已存在 `个股基础知识库.md`
- **THEN** 系统自动读取 P1/P4 内容作为论点支柱的候选

### Requirement: 论点记分卡
系统 SHALL 维护一个论点记分卡，跟踪每个关键支柱的状态和趋势。

#### Scenario: 查看论点记分卡
- **WHEN** 用户请求查看某个标的的论点追踪
- **THEN** 系统显示包含以下列的表格：
  - 支柱名称
  - 原始预期
  - 当前状态（On Track/Behind/Ahead/N/A）
  - 趋势（↑/↓/→）
  - 最近验证日期

#### Scenario: 更新支柱状态
- **WHEN** 用户更新某个支柱的状态
- **THEN** 系统记录状态变化和日期，并更新趋势指示

### Requirement: 更新日志
系统 SHALL 记录每个数据点或事件对论点的影响。

#### Scenario: 记录新数据点
- **WHEN** 用户添加新的数据点或事件
- **THEN** 系统记录：
  - 日期
  - 事件描述
  - 数据点内容
  - 受影响的支柱
  - 论点影响（Strengthen/Weaken/Neutral）
  - 操作建议（No change/Increase/Trim/Exit）
  - 置信度变化

#### Scenario: 查看更新历史
- **WHEN** 用户请求查看更新历史
- **THEN** 系统按时间倒序显示所有更新日志

### Requirement: 置信度管理
系统 SHALL 支持论点置信度的三级量化（High/Medium/Low）和趋势追踪。

#### Scenario: 设置初始置信度
- **WHEN** 用户首次创建论点追踪
- **THEN** 系统记录初始置信度（默认 Medium）和日期

#### Scenario: 更新置信度
- **WHEN** 用户根据新信息更新论点
- **THEN** 系统记录新置信度、趋势方向和更新原因

#### Scenario: 显示置信度趋势
- **WHEN** 用户查看论点追踪摘要
- **THEN** 系统显示当前置信度和最近 N 次变化的趋势

### Requirement: 催化剂关联
系统 SHALL 将催化剂与论点支柱关联，预警即将到来可能验证/证伪论点的事件。

#### Scenario: 添加催化剂
- **WHEN** 用户添加催化剂
- **THEN** 系统记录：
  - 日期
  - 事件描述
  - 事件类型（Earnings/Corporate/Industry/Macro）
  - 预期影响（High/Medium/Low）
  - 关联的支柱

#### Scenario: 催化剂预警
- **WHEN** 用户查看论点追踪且未来 7 天内有催化剂
- **THEN** 系统高亮显示即将到来的催化剂

### Requirement: 论点验证
系统 SHALL 支持用户验证论点是否仍然有效。

#### Scenario: 论点完整性检查
- **WHEN** 用户请求验证论点
- **THEN** 系统检查：
  - 是否有明确的 falsifiable 条件
  - 关键支柱是否有验证记录
  - 是否有记录 disconfirming evidence（反向证据）
  - 置信度是否与最新数据一致

#### Scenario: 论点失效提示
- **WHEN** 系统检测到论点已被关键事件证伪
- **THEN** 系统提示用户考虑退出或调整仓位

### Requirement: 与现有 Skill 集成
系统 SHALL 与现有 YMOS skill 无缝集成。

#### Scenario: ymos-research 初始化论点追踪
- **WHEN** ymos-research 完成 P1/P4/P2 分析
- **THEN** 系统询问用户是否初始化论点追踪

#### Scenario: ymos-strategy 读取论点置信度
- **WHEN** ymos-strategy 执行策略分析
- **THEN** 系统读取论点追踪中的当前置信度作为决策输入

#### Scenario: ymos-radar 提示论点更新
- **WHEN** ymos-radar 检测到标的的重大事件
- **THEN** 系统提示用户是否更新论点追踪
