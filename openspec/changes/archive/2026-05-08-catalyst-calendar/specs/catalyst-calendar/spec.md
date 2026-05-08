## ADDED Requirements

### Requirement: 事件收集
系统 SHALL 支持收集和录入催化剂事件。

#### Scenario: 手动添加事件
- **WHEN** 用户调用 `/ymos-catalyst-calendar add`
- **THEN** 系统提示用户输入：
  - 日期
  - 事件描述
  - 事件类型（Earnings/Corporate/Industry/Macro）
  - 影响等级（High/Medium/Low）
  - 关联标的（可选）
  - 事件详情/备注

#### Scenario: 批量导入财报日期
- **WHEN** 用户调用 `ymos catalyst-calendar fetch-earnings --tickers AAPL,MSFT,0700.HK`
- **THEN** 系统从数据源获取财报日期并添加到日历

#### Scenario: 验证事件日期
- **WHEN** 事件日期在过去
- **THEN** 系统提示用户确认是否为重复录入或日期错误

### Requirement: 日历视图
系统 SHALL 提供催化剂日历视图，展示即将到来的事件。

#### Scenario: 查看日历视图
- **WHEN** 用户调用 `/ymos-catalyst-calendar`
- **THEN** 系统显示按日期排序的事件列表，包含：
  - 日期
  - 事件描述
  - 事件类型
  - 影响等级
  - 关联标的
  - 距离今日的天数

#### Scenario: 筛选事件
- **WHEN** 用户指定筛选条件（标的、类型、影响等级、时间范围）
- **THEN** 系统只显示符合条件的事件

#### Scenario: 高亮高影响事件
- **WHEN** 日历中包含影响等级为 High 的事件
- **THEN** 系统用特殊标记高亮显示

### Requirement: 每周预览
系统 SHALL 生成每周催化剂预览报告。

#### Scenario: 生成每周预览
- **WHEN** 用户调用 `/ymos-catalyst-calendar weekly` 或系统每周自动生成
- **THEN** 系统生成包含以下内容的报告：
  - 本周关键事件（按日期排序）
  - 每个事件的：日期、公司/事件、影响等级、为什么重要、仓位影响
  - 下周前瞻
  - 风险提示

#### Scenario: 关联持仓影响
- **WHEN** 生成每周预览且事件有关联的持仓标的
- **THEN** 系统明确列出该事件对每个持仓的潜在影响

### Requirement: 影响评估
系统 SHALL 支持评估事件对持仓的影响。

#### Scenario: 评估事件影响
- **WHEN** 用户添加或修改事件时指定影响等级
- **THEN** 系统记录：
  - 影响等级（High/Medium/Low）
  - 受影响的持仓列表
  - 影响描述（上涨/下跌/中性）

#### Scenario: 事件影响分析
- **WHEN** 用户请求分析某个事件的影响
- **THEN** 系统提供：
  - 事件背景
  - 可能的市场反应
  - 对相关标的的预期影响
  - 建议的仓位调整

### Requirement: 日历导出
系统 SHALL 支持将日历导出为 Excel 格式。

#### Scenario: 导出为 Excel
- **WHEN** 用户调用 `/ymos-catalyst-calendar export`
- **THEN** 系统生成 Excel 文件，包含：
  - Sheet 1: 日历视图（按日期排序）
  - Sheet 2: 按标的分组
  - Sheet 3: 按影响等级排序

#### Scenario: 指定时间范围导出
- **WHEN** 用户指定导出时间范围
- **THEN** 系统只导出该范围内的事件

### Requirement: 与现有 Skill 集成
系统 SHALL 与现有 YMOS skill 无缝集成。

#### Scenario: ymos-radar 集成
- **WHEN** ymos-radar 检测到新的重大事件
- **THEN** 系统询问用户是否添加到催化剂日历

#### Scenario: ymos-strategy 集成
- **WHEN** ymos-strategy 执行策略分析
- **THEN** 系统读取并显示即将到来的催化剂（未来 7 天）

#### Scenario: ymos-thesis-tracker 集成
- **WHEN** 在 ymos-thesis-tracker 中添加催化剂
- **THEN** 系统同时更新全局催化剂日历

### Requirement: 事件状态管理
系统 SHALL 支持事件状态的生命周期管理。

#### Scenario: 事件状态转换
- **WHEN** 事件日期已过
- **THEN** 系统自动将事件标记为"已发生"

#### Scenario: 归档历史事件
- **WHEN** 生成每周报告时
- **THEN** 系统将已发生的事件从日历移动到历史记录

#### Scenario: 事件更新
- **WHEN** 事件信息发生变化（如财报日期调整）
- **THEN** 系统支持更新事件详情并记录变更历史

### Requirement: 事件通知
系统 SHALL 支持事件临近时的主动提示。

#### Scenario: 临近事件提示
- **WHEN** 用户查看日历且未来 3 天内有高影响事件
- **THEN** 系统在日历顶部显示预警信息

#### Scenario: 事件回顾
- **WHEN** 事件刚刚发生（1-3 天内）
- **THEN** 系统在日历中显示"需回顾"标记
