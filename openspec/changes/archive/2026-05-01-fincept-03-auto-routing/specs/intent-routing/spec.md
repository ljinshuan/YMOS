## ADDED Requirements

### Requirement: 意图分类 prompt 文件存在
系统 SHALL 在 `skills/ymos-core/prompts/intent-classifier.md` 提供意图分类 prompt 文件。

#### Scenario: prompt 文件可被 Agent 读取
- **WHEN** 用户输入自然语言指令
- **THEN** Agent 读取 `skills/ymos-core/prompts/intent-classifier.md` 进行意图识别

### Requirement: 8 种意图分类定义
意图分类 prompt MUST 定义以下 8 种投资意图：
- market-overview：市场概览 → market-insight
- investment-radar：投资雷达 → radar
- stock-research：个股研究 → research
- buy-entry：买入/建仓 → strategy Route A/B
- hold-evaluate：持有评估 → strategy Route C
- sell-reduce：卖出/减仓 → strategy Route D
- portfolio-mgmt：组合管理 → strategy Route E + reconcile
- system-ops：系统操作 → target-mgmt / onboarding / diagnosis

#### Scenario: 自然语言被正确分类
- **WHEN** 用户输入"最近美联储加息对 NIO 影响大吗"
- **THEN** 系统将意图分类为"hold-evaluate"或"stock-research"，并映射到对应的 skill 链条

### Requirement: 复合意图识别
意图分类 MUST 支持识别复合意图（一句话中包含多个意图）。

#### Scenario: 复合意图输出有序任务列表
- **WHEN** 用户输入"帮我研究一下 NIO 然后看看要不要加仓"
- **THEN** 系统识别为"stock-research" + "buy-entry"，输出有序任务列表：先 research 后 strategy Route B

### Requirement: 触发词绕过机制
用户直接使用触发词时 MUST 绕过意图识别，直接路由到对应 skill。

#### Scenario: 直接触发词不经过意图识别
- **WHEN** 用户输入"跑一下投资雷达"
- **THEN** 系统直接路由到 ymos-radar，不执行意图分类
