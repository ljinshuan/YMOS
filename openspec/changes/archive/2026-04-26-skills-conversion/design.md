## Context

YMOS 有 8 个核心能力，目前只有投资诊断（`Brain/ymos-diagnosis/SKILL.md`）是 skill 格式。其余 7 个以 SOP 文件存在。skill 是 Claude Code agent 发现和执行能力的标准单元，SKILL.md 定义触发条件、执行步骤、引用资源。

## Goals / Non-Goals

**Goals:**
- 8 个能力全部转为 skill，放在 `skills/` 顶层目录
- 每个 skill 通过 SKILL.md 定义触发词、引用 references/sops/ 中的 SOP、调用 ymos CLI
- 共享 skill（ymos-research）采用混合模式：独立可调用 + 可被其他 skill 组合引用
- skill 发现机制通过 CLAUDE.md 中的路径声明实现

**Non-Goals:**
- 不将 skill 放入 `.claude/skills/`（那是 Claude Code 原生 skill 的位置）
- 不改变 SOP 的内容逻辑
- 不实现 skill 间的自动调用链（skill 只声明依赖，由 agent 决定调用顺序）

## Decisions

### D1: Skill 目录结构

```
skills/
├── ymos-onboarding/
│   └── SKILL.md
├── ymos-market-insight/
│   └── SKILL.md
├── ymos-radar/
│   └── SKILL.md
├── ymos-strategy/
│   └── SKILL.md
├── ymos-research/
│   └── SKILL.md
├── ymos-target-mgmt/
│   └── SKILL.md
├── ymos-reconcile/
│   └── SKILL.md
└── ymos-diagnosis/
    └── SKILL.md          ← 从 Brain/ymos-diagnosis/ 迁移
```

### D2: SKILL.md 通用模板

```yaml
---
name: ymos-xxx
description: |
  一句话描述。触发方式：/ymos-xxx、「暗号1」「暗号2」
---
# ymos-xxx：中文名称

## 触发
- `暗号1`
- `暗号2`

## 前置条件
<!-- 需要哪些数据/状态已存在 -->

## 执行步骤
> 详细步骤见 references/sops/xxx.md

1. 步骤1（调用 ymos CLI 命令）
2. 步骤2（引用 references/prompts/ 中的提示词）
3. ...

## 产出物
<!-- 列出写入的文件 -->

## 边界
<!-- 不做什么 -->
```

### D3: 共享 Skill 协议（ymos-research）

`ymos-research` 被 3 个 skill 引用（ymos-strategy、ymos-target-mgmt、ymos-onboarding）。协议：

1. **独立调用**：用户说 `调研一下 TICKER` 直接触发
2. **组合引用**：其他 skill 的 SKILL.md 中写 `→ 需要调研时，引导用户调用 ymos-research` 或 `→ 缺少 P1/P4 时，执行 ymos-research 流程（读取 references/sops/research.md）`
3. **不自动嵌套调用**：skill 不会自动调用另一个 skill 的 SKILL.md，而是由 agent 判断是否需要执行对应流程

### D4: 8 个 Skill 的触发词映射

| Skill | 触发暗号 |
|-------|---------|
| ymos-onboarding | `开始使用`、`初始化系统`、`补全信息` |
| ymos-market-insight | `跑一下市场洞察`、`今天有什么新闻`、`抓 N 天数据` |
| ymos-radar | `跑一下投资雷达`、`查一下价格`、`看看有什么信号` |
| ymos-strategy | `我想买/卖/加仓/持有怎么看 [ticker]`、`做个仓位再平衡`、`跑一下策略分析` |
| ymos-research | `调研一下 [ticker]` |
| ymos-target-mgmt | `关注/建仓/移除关注/清仓 [ticker]` |
| ymos-reconcile | `收口一下`、`刷新持仓视图` |
| ymos-diagnosis | `诊断一下我的策略`、`帮我看看我的投资`、`我的投资有什么问题` |

### D5: ymos-diagnosis 迁移

`Brain/ymos-diagnosis/SKILL.md` 迁移到 `skills/ymos-diagnosis/SKILL.md`。其 knowledge 引用更新为 `references/knowledge/diagnosis/`。原 `Brain/ymos-diagnosis/` 目录删除。

## Risks / Trade-offs

- **Skill 间调用无自动机制**：依赖 agent 理解 SKILL.md 中的引用文字并主动执行。风险：agent 可能遗漏。缓解：在引用文字中写明确
- **CLAUDE.md 膨胀**：8 个 skill 路径声明会增加 CLAUDE.md 长度。可接受
- **与 .claude/skills/ 的关系**：用户可能在 `.claude/skills/` 也有 skill（如当前的 openspec skills）。两套 skill 体系共存，不冲突
