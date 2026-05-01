## MODIFIED Requirements

### Requirement: routing.md 包含 P18 注册
`skills/ymos-core/routing.md` 的 prompt 注册表 MUST 包含 P18 大师会诊条目，标明其在 P1 链条中的位置（P1 → P4 → P18 → P2）和可选性质。

#### Scenario: routing 表查询 P18
- **WHEN** Agent 查询 routing.md 中 P18 的注册信息
- **THEN** 返回 P18 的描述、在链条中的位置、依赖关系（依赖 P1 和 P4 完成）和可选标记

### Requirement: P18 prompt 放置在共享 prompts 目录
`skills/ymos-core/prompts/` 目录 MUST 包含 `p18-master-consultation.md` 文件。

#### Scenario: 共享 prompt 可被多个 skill 引用
- **WHEN** ymos-research 或其他 skill 需要引用 P18
- **THEN** 从 `skills/ymos-core/prompts/p18-master-consultation.md` 路径读取
