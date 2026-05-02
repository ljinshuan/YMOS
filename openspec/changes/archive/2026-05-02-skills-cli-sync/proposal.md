## Why

Skills 目录中的 SKILL.md、sop.md、routing.md 引用了大量 `ymos` CLI 命令，但其中 6 处缺少 Typer 二级子命令层级（如 `ymos price-scan --from-state` 应为 `ymos price-scan scan --from-state`），会导致 agent 按文档执行时直接报错。此外，今天完成的 3 个 Futu OpenD 增强（持仓获取、技术分析 Futu 数据源、新闻 Futu 兜底）尚未被 skills 引用，市场洞察的新闻描述仍然写着"仅持仓美股/Crypto"。

## What Changes

- 修复 6 处 CLI 命令调用缺少子命令层级的问题（SKILL.md + sop.md）
- 修复 1 处 `--output` 参数名错误（应为 `--output-dir`）
- 更新 `ymos-market-insight` SKILL.md 和 sop.md 中 `fetch-news` 的描述，反映 Futu 兜底能力
- 将 `ymos position fetch` 新能力接入 `ymos-reconcile`（持仓校验）和 `ymos-radar`（真实持仓数据）
- 在 `routing.md` 中补充 position、tech-analysis --source、news Futu 兜底的入口

## Capabilities

### New Capabilities
- `position-integration`: 将 `ymos position fetch` 接入 reconcile 和 radar 的执行步骤，使 skills 能读取真实 broker 持仓数据

### Modified Capabilities
- `cli-references`: 修复所有 skills 文档中 CLI 命令调用的子命令层级和参数名错误
- `news-futu-fallback-docs`: 更新 market-insight 的 SKILL.md 和 sop.md 中关于 fetch-news 的描述

## Impact

- 修改范围：skills/ 目录下的 Markdown 文档（SKILL.md、sop.md、routing.md）
- 不涉及代码变更，纯文档修复
- 影响 agent 执行时的命令调用准确性
