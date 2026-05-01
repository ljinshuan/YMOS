## MODIFIED Requirements

### Requirement: 案例库增加行为偏误类别
`skills/ymos-diagnosis/knowledge/diagnosis_case_library.md` MUST 增加"行为偏误"案例类别，包含至少 3 个典型案例。

#### Scenario: 行为偏误案例可被引用
- **WHEN** ymos-diagnosis 的问诊模式检测到用户存在行为偏误
- **THEN** 可以引用案例库中的行为偏误案例作为参考
