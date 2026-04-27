## Why

当前 SOP 散落在 `Eyes/`、`Brain/`、`持仓与关注/` 三个模块目录下，P 系列提示词在 `Brain/references/`，模板在 `持仓与关注/_模板_单标的/`，诊断知识库在 `Brain/ymos-diagnosis/knowledge/`。知识资产分散在多处，skill 需要跨目录引用。

需要统一收归到 `references/` 目录，按类型组织（sops/ prompts/ templates/ knowledge/），让 skill 引用路径清晰一致。

## What Changes

- 新建 `references/` 顶层目录
- `references/sops/`：迁移 7 个 SOP 文件（重命名为英文名）
- `references/prompts/`：迁移 `Brain/references/` 下全部 P 系列提示词和辅助文档
- `references/templates/`：迁移 `持仓与关注/_模板_单标的/` 的模板文件
- `references/knowledge/`：迁移 `Brain/ymos-diagnosis/knowledge/` 的知识库文件
- 删除旧目录下已迁移的文件
- `Brain/references/` 目录整体迁移后删除

## Capabilities

### New Capabilities
- `references-directory-layout`: references/ 目录结构规范，定义各子目录用途

### Modified Capabilities

（无现有 spec 需要修改）

## Impact

- **路径变更**：所有 skill 的 SKILL.md 中引用路径更新
- **依赖关系**：依赖于 data-layer-separation 完成（确保 references 只含知识资产不含运行时数据）
- **删除旧目录**：`Brain/references/`、`持仓与关注/_模板_单标的/`、`Brain/ymos-diagnosis/knowledge/` 删除
- **诊断 skill**：`ymos-diagnosis` 的 knowledge 路径更新
