## Context

YMOS 的 skills 目录包含 11 个 skill，其中 SKILL.md、sop.md 和 routing.md 大量引用 `ymos` CLI 命令。CLI 基于 Typer 二级命令结构（`ymos <command> <subcommand>`），但部分文档只写了一级。同时，今天完成的 3 个 Futu 增强（position fetch、tech-analysis --source、news Futu fallback）尚未反映到 skills 文档中。

当前 CLI 命令结构（涉及本次修改的）：

```
ymos price-scan scan --from-state --output-dir DIR --date-tag TAG
ymos fetch-capital-flow fetch --from-state --output-dir DIR
ymos fetch-news fetch --hours 24 --output PATH
ymos fetch-sentiment fetch --ticker TICKER --from-state
ymos screen screen --market HK --preset growth
ymos position fetch --output-dir DIR --format both
ymos tech-analysis analyze --symbols X --source auto
```

## Goals / Non-Goals

**Goals:**
- 修复所有 CLI 命令调用的子命令层级缺失，确保 agent 按文档执行不会报错
- 修复参数名错误
- 更新 news 相关描述，反映 Futu 兜底能力
- 将 `ymos position fetch` 接入 reconcile 和 radar
- 更新 routing.md 补充新入口

**Non-Goals:**
- 不修改任何 Python 代码
- 不修改 CLI 命令本身的接口
- 不修改 prompts/ 目录下的 P 系列提示词
- 不修改 SOP 的业务逻辑流程（只修正命令调用）

## Decisions

1. **纯文档修复，不改代码** — 所有变更都在 Markdown 文件中，风险极低
2. **position 接入 reconcile 而非 radar 作为主要场景** — reconcile 的"持仓收口"天然需要真实持仓校验；radar 中的持仓监控可保留现有 price-scan 路径，仅在 Step 5.2 中增加"可选：读取 position fetch 数据"提示
3. **不修改只读文件** — SOP 文件中 `skills/*/sop.md` 在 CLAUDE.md 中标记为只读，但本次修复属于文档纠错，需与用户确认是否允许修改

## Risks / Trade-offs

- [sop.md 标记只读] → 本次修复属于文档纠错，不改业务逻辑，需用户确认
- [position fetch 需要 OpenD 在线] → 在 reconcile 步骤中标记为可选，OpenD 不可用时跳过
