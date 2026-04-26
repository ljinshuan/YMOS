## Why

当前 8 个 Python 脚本散落在 `Eyes/scripts/` 中，通过 `python3 Eyes/scripts/xxx.py` 直接调用。SOP 中的文件操作（创建目录、读写状态机、初始化模板）全靠 agent 临时拼接 bash 命令。这导致：路径硬编码在各 SOP 中、脚本与状态机之间无类型安全的接口、新增功能需要 agent 手动组装多步操作。

需要统一 CLI 层，让 skill 通过 `ymos <command>` 调用所有能力，路径由 CLI 内部管理。

## What Changes

- 新建 `cli/` 目录，用 typer 构建统一的 `ymos` CLI 入口
- 将现有 8 个脚本迁移为 CLI 子命令（`price-scan`、`fetch-rss`、`fetch-market`、`fetch-news`）
- 新增文件操作子命令：`state read/write/validate`、`init stock/dirs/template`、`report list`
- 引入 `cli/core/paths.py` 集中管理所有路径常量
- `pyproject.toml` 中注册 `ymos` 为 console script 入口
- 引入 typer、rich 作为依赖（不再追求零依赖）
- 删除 `Eyes/scripts/` 下已迁移的脚本

## Capabilities

### New Capabilities
- `cli-data-fetch`: 价格路由、RSS 抓取、市场 API、个股新闻等数据抓取命令
- `cli-state-ops`: 状态机读写、一致性校验、投资偏好管理
- `cli-init-ops`: 目录初始化、标的建档、模板生成
- `cli-path-management`: 统一路径常量管理，所有路径由 paths.py 定义

### Modified Capabilities

（无现有 spec 需要修改）

## Impact

- **依赖变更**：pyproject.toml 新增 typer、rich 依赖
- **代码迁移**：8 个脚本从 `Eyes/scripts/` 迁至 `cli/`，原脚本删除
- **调用方变更**：所有 SOP/skill 中的 `python3 Eyes/scripts/xxx.py` 改为 `ymos xxx`
- **Python 版本**：维持 3.12+
