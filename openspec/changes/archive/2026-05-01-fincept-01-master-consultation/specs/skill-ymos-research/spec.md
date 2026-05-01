## MODIFIED Requirements

### Requirement: research 链条支持 P18 可选环节
`skills/ymos-research/SKILL.md` 的 prompt 链条定义 MUST 支持以下两种执行路径：
- 标准路径：P1 → P4 → P2（现有行为）
- 增强路径：P1 → P4 → P18 → P2（新增）

#### Scenario: 用户请求大师会诊
- **WHEN** 用户在研究个股时明确要求"大师会诊"或"多视角分析"
- **THEN** Agent 执行增强路径，在 P4 之后、P2 之前插入 P18 环节

#### Scenario: 默认执行不触发 P18
- **WHEN** 用户请求标准的个股研究（"调研一下 AAPL"）
- **THEN** Agent 执行标准路径，不触发 P18

### Requirement: P18 输出写入个股知识库
P18 大师会诊的输出 MUST 被追加到个股知识库文件中。

#### Scenario: 大师会诊结果持久化
- **WHEN** P18 执行完成
- **THEN** 综合报告（共识点、分歧点、综合建议）被追加到该个股的 `个股基础知识库.md`
