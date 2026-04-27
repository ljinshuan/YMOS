## Why

前 4 个 change（CLI 基础设施、数据层分离、References 重组、Skills 转换）完成后，YMOS 的目录结构和调用方式发生根本变化。CLAUDE.md、总入口暗号、AGENT_GUIDE 中的路径引用、命令示例、目录描述全部过时。

需要更新所有入口文件，确保 agent 在新架构下能正确发现 skill、引用 references、通过 CLI 操作数据。

## What Changes

- **BREAKING** 重写 `CLAUDE.md`：更新目录结构描述、路径速查表、脚本调用方式、环境变量说明
- **BREAKING** 重写 `总入口暗号.md`：SOP 链接指向 `references/sops/`，脚本命令改为 `ymos` CLI
- 更新 `AGENT_GUIDE.md`：同上
- 更新 `.gitignore`：新增 `data/` 忽略规则
- 删除旧的空模块目录骨架（`Eyes/`、`Brain/`、`持仓与关注/` 下的运行时内容已迁移）
- 更新 `pyproject.toml`：注册 `ymos` CLI 入口点

## Capabilities

### New Capabilities

（无新 capability，本 change 是纯文档和配置更新）

### Modified Capabilities

（无现有 spec 需要修改）

## Impact

- **依赖关系**：依赖于前 4 个 change 全部完成
- **Agent 行为**：agent 读取更新后的 CLAUDE.md 获取新架构认知
- **用户体验**：总入口暗号中的命令示例更新，暗号触发方式不变
- **git 管理范围**：`.gitignore` 变更影响 git 跟踪范围
