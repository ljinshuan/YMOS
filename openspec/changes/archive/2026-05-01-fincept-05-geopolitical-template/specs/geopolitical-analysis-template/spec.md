## ADDED Requirements

### Requirement: 地缘政治分析模板文件存在
系统 SHALL 在 `skills/ymos-core/templates/geopolitical-analysis.md` 提供完整的地缘政治分析模板。

#### Scenario: 模板文件可被 P13 引用
- **WHEN** P13 Market Scanner 检测到地缘政治事件
- **THEN** 从 `skills/ymos-core/templates/geopolitical-analysis.md` 读取分析模板

### Requirement: 三步分析框架
地缘政治分析模板 MUST 包含以下三步框架：
1. 地理约束：事件的地理基础、资源分布、通道/邻国关系等硬约束
2. 历史模式：1-2 个关键历史类比（限最近 50 年内）
3. 传导路径：事件 → 商品/供应链影响 → 行业影响 → 持仓标的影响

#### Scenario: 三步框架完整输出
- **WHEN** 地缘政治模板被激活
- **THEN** 输出 MUST 包含地理约束、历史回声、传导路径三个 section

### Requirement: 条件触发机制
地缘政治模板 MUST NOT 在每次 P13 执行时都激活。仅在新闻涉及以下领域时触发：
- 军事冲突、制裁、贸易战、关税、领土争端
- 关键地区：中东、台海、南海、乌克兰、朝鲜半岛
- 关键资源：石油、稀土、芯片、粮食

#### Scenario: 非地缘政治新闻不触发
- **WHEN** P13 处理的新闻不涉及地缘政治关键词域
- **THEN** 地缘政治分析模板不被激活，P13 正常输出其他 section

#### Scenario: 地缘政治新闻触发模板
- **WHEN** P13 处理的新闻涉及台海军事演习
- **THEN** 地缘政治分析模板被激活，输出包含传导路径分析

### Requirement: 传导路径必须具体到标的
传导路径 MUST NOT 停留在"影响科技板块"这种泛泛层面，必须说明具体影响哪些行业/标的。

#### Scenario: 传导路径具体化
- **WHEN** 地缘政治事件涉及中东石油供应
- **THEN** 传导路径 MUST 指出具体影响（如"油价上涨 → 航空/运输成本上升 → 关注 AAPL 供应链成本"）
