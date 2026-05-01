## ADDED Requirements

### Requirement: P18 prompt 文件存在
系统 SHALL 在 `skills/ymos-core/prompts/p18-master-consultation.md` 提供完整的大师会诊 prompt 文件。

#### Scenario: prompt 文件可被 Agent 读取
- **WHEN** Agent 执行 P18 环节
- **THEN** 系统从 `skills/ymos-core/prompts/p18-master-consultation.md` 读取 prompt 内容

### Requirement: 四大师 lens 定义
P18 prompt MUST 包含以下 4 个投资大师的分析 lens，每个 lens 有明确的评估维度和评分标准：
- 巴菲特：护城河质量 + 所有者收益 + 资本配置
- 格雷厄姆：安全边际 + 量化筛选指标（P/E、P/B、流动比率）
- 马克斯：周期定位 + 二阶思维 + 市场情绪温度
- 林奇：PEG 比率 + 六分类（慢速/稳定/快速/周期/转机/资产型）

#### Scenario: 四个 lens 全部输出
- **WHEN** Agent 对某只股票执行 P18
- **THEN** 输出 MUST 包含 4 个独立的大师分析 section，每个 section 包含评估维度和结论

### Requirement: 结构化信号输出
每个大师 lens MUST 输出以下结构化信号：
- 判断：bullish / neutral / bearish
- 置信度：0-100%
- 风格专属评分（如 Buffett lens 的 moat_score 1-10）

#### Scenario: 信号格式一致
- **WHEN** 任意一个大师 lens 完成分析
- **THEN** 输出 MUST 包含判断、置信度、风格专属评分三个字段

### Requirement: 大师会诊综合报告
P18 MUST 在 4 个独立 lens 之后输出综合报告，包含：
- 共识点：≥2 个大师一致的判断
- 分歧点：大师之间判断不一致的地方及各自理由
- 综合建议：基于共识和分歧的整体评估

#### Scenario: 共识与分歧标注
- **WHEN** 4 个大师 lens 中 3 个给出 bullish、1 个给出 neutral
- **THEN** 综合报告 MUST 标注"共识：看多（3/4）"并说明唯一 neutral 的理由

### Requirement: P18 为可选环节
P18 MUST NOT 成为 P1 链条的必选环节。Agent 或用户可以选择跳过 P18。

#### Scenario: 用户跳过 P18
- **WHEN** 用户请求执行 P1 → P4 → P2 链条（未提及大师会诊）
- **THEN** 链条正常执行，P18 不被触发
