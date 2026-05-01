## MODIFIED Requirements

### Requirement: Route C 和 Route E 适配 P8 新输出格式
`skills/ymos-strategy/SKILL.md` 中使用 P8 的 Route（Route C 持有评估、Route E 再平衡）MUST 能正确消费 P8 辩论模式的新增输出字段（最强反对论点、辩结论）。

#### Scenario: Route C 消费 P8 辩论输出
- **WHEN** Route C 执行 P8 Macro Filter
- **THEN** 策略分析 MUST 参考 P8 的辩结论（而非仅看原始评级）做最终判断
