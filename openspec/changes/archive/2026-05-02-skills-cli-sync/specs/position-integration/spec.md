## ADDED Requirements

### Requirement: reconcile 可读取 Futu 真实持仓进行校验
`ymos-reconcile` 的 SKILL.md 和 sop.md SHALL 包含可选步骤：调用 `ymos position fetch` 获取 Futu 真实持仓数据，用于与状态机中的持仓信息做一致性校验。

#### Scenario: OpenD 在线时的持仓校验
- **WHEN** 用户触发"收口一下"且 Futu OpenD 在线
- **THEN** reconcile 流程在一致性校验步骤中增加：调用 `ymos position fetch` → 对比状态机持仓 ticker 列表和数量 → 标注差异

#### Scenario: OpenD 离线时跳过
- **WHEN** 用户触发"收口一下"且 Futu OpenD 不可达
- **THEN** 跳过持仓校验，在报告中标注"Futu 持仓数据不可用"

### Requirement: radar 持仓监控可引用 Futu 真实持仓数据
`ymos-radar` 的 sop.md 在 Step 5.2 持仓监控中 SHALL 添加可选数据源说明：若 `ymos position fetch` 数据可用，可在持仓监控表中引用真实市值和盈亏数据。

#### Scenario: 持仓监控增强
- **WHEN** radar 流程执行 Step 5.2 且 Futu 持仓数据存在
- **THEN** 持仓监控表可包含真实市值、浮动盈亏（来自 position fetch），与 price-scan 价格互为验证

### Requirement: routing.md 补充新入口
`skills/ymos-core/routing.md` SHALL 包含以下新入口：
1. 持仓同步入口（position fetch → reconcile）
2. tech-analysis 数据源选项（--source auto/futu）
3. fetch-news Futu 兜底说明

#### Scenario: routing.md 完整性
- **WHEN** agent 读取 routing.md 寻找命令入口
- **THEN** 能找到 position、tech-analysis --source、news Futu 兜底的相关说明
