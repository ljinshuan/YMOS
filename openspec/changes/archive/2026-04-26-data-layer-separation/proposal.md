## Why

当前运行时数据（报告、状态机、个股文件夹）与流程定义（SOP）和知识资产（P 系列提示词）混在同一目录树下。这导致 git 管理混乱、路径硬编码分散、无法独立版本控制流程代码与用户数据。

需要将运行时数据抽到独立的 `data/` 层，与代码和知识资产彻底分离。

## What Changes

- **BREAKING** 新建 `data/` 顶层目录，承载所有运行时数据
- 将 `Eyes/市场洞察/`、`Eyes/投资雷达/` 的报告产出迁移至 `data/reports/`
- 将 `Brain/策略分析/` 的报告产出迁移至 `data/reports/`
- 将 `持仓与关注/持仓/`、`持仓与关注/动态Watchlist/` 迁移至 `data/stocks/`
- 将状态机文件（`持仓_状态机.md`、`Watchlist_状态机.md`）迁移至 `data/state/`
- 将 `当前关注方向与投资偏好.md` 迁移至 `data/state/`
- 将 `持仓备忘录_视图.md` 迁移至 `data/state/`
- 将 `dashboard/` 迁移至 `data/dashboard/`
- `.gitignore` 新增 `data/` 忽略规则
- 清空旧模块目录下的运行时数据

## Capabilities

### New Capabilities
- `data-directory-layout`: data/ 目录结构规范，定义各子目录用途和命名规则

### Modified Capabilities

（无现有 spec 需要修改）

## Impact

- **路径变更**：所有 SOP、脚本、skill 中的文件路径全部更新
- **git 历史**：迁移后旧路径文件从 git 跟踪中移除
- **用户影响**：已有用户的 data/ 需要一次性迁移（可提供 `ymos migrate` 命令）
- **与 cli-infrastructure 协同**：`cli/core/paths.py` 统一引用新路径
