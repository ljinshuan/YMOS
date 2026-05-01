## MODIFIED Requirements

### Requirement: routing.md 增加意图识别层
`skills/ymos-core/routing.md` MUST 增加意图识别层文档，描述自然语言输入的路由流程：意图分类 → skill 映射 → 链条执行。

#### Scenario: routing 文档包含意图分类表
- **WHEN** Agent 查询 routing.md 的意图识别部分
- **THEN** 返回 8 种意图的定义、映射关系和触发词绕过规则

### Requirement: 总入口暗号.md 增加智能路由 section
`总入口暗号.md` MUST 增加"智能路由"section，作为 Agent 处理用户输入的第一层判断。

#### Scenario: Agent 遵循智能路由
- **WHEN** Agent 读取 `总入口暗号.md` 并收到自然语言输入
- **THEN** 先检查触发词匹配，若无匹配则执行意图分类，再路由到对应 skill
