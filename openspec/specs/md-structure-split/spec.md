## ADDED Requirements

### Requirement: 拆分阈值判定
系统 SHALL 对 skills/ 目录下所有 MD 文件进行大小评估，仅对超过 5KB 或 150 行的文件执行拆分。低于阈值的文件保持原样。

#### Scenario: 文件超过阈值
- **WHEN** 一个 MD 文件超过 5KB 或 150 行
- **THEN** 该文件被纳入拆分计划，按其结构类型（SOP / P-series prompt / Knowledge）选择对应拆分模式

#### Scenario: 文件低于阈值
- **WHEN** 一个 MD 文件低于 5KB 且少于 150 行
- **THEN** 该文件不拆分，保持原样

### Requirement: SOP 路由拆分
SOP 文件 SHALL 按路由拆分为索引文件 + 路由子文件。索引文件保留公共步骤（Step 1-N）和路由索引表，每条路由独立存为子文件。

#### Scenario: Agent 执行策略分析 SOP
- **WHEN** agent 读取 strategy/sop.md 并确定走 Route A（买入）
- **THEN** agent 读完公共步骤后，仅读取 `sop/route-a-buy.md`，不加载 Route B-E 的内容

#### Scenario: SOP 索引文件包含路由映射
- **WHEN** agent 读完 SOP 索引文件的公共步骤
- **THEN** 索引文件底部提供清晰的路由 → 子文件路径映射表

### Requirement: P-series prompt 结构层拆分
具有多层结构的 P-series prompt SHALL 按自然结构边界拆分。原文件保留第一层 + 索引，后续层独立为子文件。

#### Scenario: P1-genesis 两层拆分
- **WHEN** agent 需要对个股执行 P1 初始分类判断
- **THEN** agent 仅读取 p1-genesis.md（第一层：机会分类），无需加载第二层深度分析

#### Scenario: P1-genesis 深度分析
- **WHEN** agent 完成分类判断后需要执行七维度深度分析
- **THEN** agent 读取 p1-genesis-deepdive.md（第二层）

### Requirement: Knowledge 文件主题拆分
Knowledge 文件 SHALL 按主题/独立性拆分。核心内容保留在原文件，扩展内容独立为子文件。

#### Scenario: 投资公理按重要性拆分
- **WHEN** agent 需要参考投资公理做纪律检查
- **THEN** agent 读取核心公理文件（前 5 条），按需加载扩展公理文件

### Requirement: 拆分后语义不变
所有拆分操作 SHALL 保持原始文件的语义内容完全不变。只做结构拆分，不做内容重写或删减。

#### Scenario: 拆分前后内容一致性
- **WHEN** 将拆分后的所有子文件内容按顺序拼接
- **THEN** 得到的文本与原始文件内容完全一致（忽略路径索引表部分）
