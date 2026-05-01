## MODIFIED Requirements

### Requirement: 所有 Route 适配 P12 新增偏误字段
`skills/ymos-strategy/SKILL.md` 中所有使用 P12 的 Route（A/B/C/D/E）MUST 能消费 P12 新增的行为偏误风险评级字段。

#### Scenario: Route A 参考偏误评级
- **WHEN** Route A（买入决策）执行 P12 审核
- **THEN** 策略报告 MUST 包含 P12 的行为偏误风险评级，若评级为"高"则在最终建议中突出标注
