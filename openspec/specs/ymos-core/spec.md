# ymos-core Specification

## Purpose
ymos-core is the foundational infrastructure skill for YMOS, housing shared documents used by 2 or more skills. All other skills declare dependency on ymos-core via `depends_on`.

## Requirements

### Requirement: ymos-core skill 声明与定位
ymos-core SHALL 作为 YMOS 系统的基础设施 skill，收纳被 2 个及以上 skill 共享的文档。所有其他 skill 通过 `depends_on` 声明对 ymos-core 的依赖。

#### Scenario: 新 skill 需要使用共享 prompt
- **WHEN** 一个 skill 需要引用 p2-phase-check 或 p9-valuation
- **THEN** 该 skill 的 SKILL.md frontmatter 中 SHALL 包含 `depends_on: [ymos-core]`，引用路径为 `skills/ymos-core/prompts/<file>`

#### Scenario: 判断文档是否属于 ymos-core
- **WHEN** 一个文档被且仅被 1 个 skill 使用
- **THEN** 该文档 SHALL NOT 放入 ymos-core，而 SHALL 放入对应 skill 目录

### Requirement: ymos-core 包含共享 prompts
ymos-core SHALL 包含被多 skill 共享的 prompt 文件：p2-phase-check.md、p9-valuation.md。文件 SHALL 存放于 `skills/ymos-core/prompts/` 目录。

#### Scenario: strategy skill 引用共享 prompt
- **WHEN** ymos-strategy 需要使用 p2-phase-check
- **THEN** SKILL.md 中引用路径 SHALL 为 `skills/ymos-core/prompts/p2-phase-check.md`

#### Scenario: research skill 引用共享 prompt
- **WHEN** ymos-research 需要使用 p9-valuation
- **THEN** SKILL.md 中引用路径 SHALL 为 `skills/ymos-core/prompts/p9-valuation.md`

### Requirement: ymos-core 包含共享 templates
ymos-core SHALL 包含共享模板文件：knowledge-base.md、memo.md。文件 SHALL 存放于 `skills/ymos-core/templates/` 目录。

#### Scenario: target-mgmt skill 引用共享模板
- **WHEN** ymos-target-mgmt 需要使用 knowledge-base.md 模板初始化个股知识库
- **THEN** 引用路径 SHALL 为 `skills/ymos-core/templates/knowledge-base.md`

### Requirement: ymos-core 包含路由速查表
ymos-core SHALL 包含路由速查表（route-cheatsheet.md），提供跨 skill 路由参考。文件 SHALL 存放于 `skills/ymos-core/` 根目录。

#### Scenario: 新 skill 查找路由规则
- **WHEN** 任意 skill 需要参考路由暗号到 skill 的映射
- **THEN** 可通过 `skills/ymos-core/routing.md` 获取完整路由表

### Requirement: ymos-core 包含 watchlist 更新工作流
ymos-core SHALL 包含 watchlist-update-workflow.md，提供跨 skill（radar、target-mgmt）共享的关注列表更新流程。

#### Scenario: radar skill 触发 watchlist 更新
- **WHEN** ymos-radar 建议新增关注标的
- **THEN** 可通过 `skills/ymos-core/watchlist-update-workflow.md` 获取标准更新流程
