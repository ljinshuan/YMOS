## MODIFIED Requirements

### Requirement: ymos-core 包含路由速查表
ymos-core SHALL 包含路由速查表（route-cheatsheet.md），提供跨 skill 路由参考。文件 SHALL 存放于 `skills/ymos-core/` 根目录。路由表 SHALL 包含 ymos-screener 的路由入口。

#### Scenario: 新 skill 查找路由规则
- **WHEN** 任意 skill 需要参考路由暗号到 skill 的映射
- **THEN** 可通过 `skills/ymos-core/routing.md` 获取完整路由表

#### Scenario: Screener routing entry
- **WHEN** user input matches screener triggers (`帮我选股`, `筛选一下`, `找一下` + stock type)
- **THEN** routing.md SHALL map these triggers to ymos-screener skill

#### Scenario: Screener to research handoff routing
- **WHEN** user selects tickers from screener results and requests research
- **THEN** routing.md SHALL define the handoff: screener output → user selection → ymos-research trigger
