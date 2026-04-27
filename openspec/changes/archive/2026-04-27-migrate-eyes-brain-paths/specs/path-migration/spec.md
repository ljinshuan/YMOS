## MODIFIED Requirements

### Requirement: SOP and SKILL.md 文件路径引用 MUST 使用 V4 目录结构

所有 skills/ 下的 SOP 和 SKILL.md 文件中的路径引用 SHALL 与当前 V4 目录结构一致，不得包含已废弃的 `Eyes/`、`Brain/`、`持仓与关注/` 路径前缀。

#### Scenario: 市场洞察报告路径引用
- **WHEN** agent 读取 ymos-market-insight 的 sop.md 或 SKILL.md
- **THEN** 报告输出路径 SHALL 为 `data/reports/market-insight/YYYY-MM/YYYY-MM-DD_市场洞察.md`，原始数据路径 SHALL 为 `data/reports/market-insight/raw/YYYY-MM/`

#### Scenario: 投资雷达报告路径引用
- **WHEN** agent 读取 ymos-radar 的 sop.md 或 SKILL.md
- **THEN** 报告输出路径 SHALL 为 `data/reports/radar/YYYY-MM/投资雷达_YYYY-MM-DD.md`，原始数据路径 SHALL 为 `data/reports/radar/raw/YYYY-MM/`

#### Scenario: 策略分析报告路径引用
- **WHEN** agent 读取 ymos-strategy 的 sop.md 或 SKILL.md
- **THEN** 报告输出路径 SHALL 为 `data/reports/strategy/YYYY-MM/`，原始数据路径 SHALL 为 `data/reports/strategy/raw/YYYY-MM/`

#### Scenario: 脚本路径引用
- **WHEN** SOP 引用价格扫描或数据抓取脚本
- **THEN** 路径 SHALL 引用 `cli/`（统一 ymos CLI），不得引用 `Eyes/scripts/`

#### Scenario: 跨 skill SOP 引用
- **WHEN** 一个 skill 的 SOP 引用另一个 skill 的 SOP
- **THEN** SHALL 使用 `skills/ymos-<name>/sop.md` 格式，不得使用 `Brain/SOP_*.md` 或 `Eyes/SOP_*.md` 格式

#### Scenario: 个股文件夹路径引用
- **WHEN** SOP 引用个股知识库或备忘录路径
- **THEN** 持仓标的 SHALL 引用 `data/stocks/holdings/名称_TICKER/`，关注标的 SHALL 引用 `data/stocks/watchlist/名称_TICKER/`，不得使用 `持仓与关注/`

### Requirement: 模块描述 MUST 反映 V4 架构

SOP 文件头部的模块描述 SHALL 使用 V4 skill 名称，版本标注 SHALL 为 YMOS V4。

#### Scenario: 模块描述更新
- **WHEN** agent 读取任意 skill 的 sop.md 头部
- **THEN** 模块描述 SHALL 为对应 ymos-* skill 名称，不得包含 `Eyes/（眼睛 — 盯市场）` 或 `Brain/（大脑 — 策略路由 + 分析）`

#### Scenario: 版本标注更新
- **WHEN** agent 读取任意 skill 的 sop.md 底部版本信息
- **THEN** 版本标注 SHALL 为 `YMOS V4 Skills 架构`，不得包含 `YMOS V3 三模块制`
