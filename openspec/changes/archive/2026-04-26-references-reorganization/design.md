## Context

当前知识资产分散在多处：
- `Brain/references/` — 17 个 P 系列提示词 + 辅助文档（cio-rss-processor、route-cheatsheet、watchlist-update-workflow）
- `Eyes/SOP_市场洞察.md`、`Eyes/SOP_投资雷达.md` — Eyes 模块的 SOP
- `Brain/SOP_策略分析.md`、`Brain/SOP_初始调研.md` — Brain 模块的 SOP
- `持仓与关注/SOP_入职引导.md`、`持仓与关注/SOP_标的管理.md`、`持仓与关注/SOP_持仓收口.md` — 持仓模块的 SOP
- `持仓与关注/_模板_单标的/` — 标的模板
- `Brain/ymos-diagnosis/knowledge/` — 诊断知识库

## Goals / Non-Goals

**Goals:**
- 所有知识资产统一收归 `references/` 目录
- 按类型分子目录：sops/、prompts/、templates/、knowledge/
- SOP 文件名改为英文（kebab-case），便于 skill 引用
- 删除旧目录下已迁移的文件

**Non-Goals:**
- 不改变 SOP 内容逻辑（只迁移不改写）
- 不合并或拆分 SOP
- 不改变 P 系列提示词的内容

## Decisions

### D1: 目标目录结构

```
references/
├── sops/
│   ├── onboarding.md              ← 持仓与关注/SOP_入职引导.md
│   ├── market-insight.md          ← Eyes/SOP_市场洞察.md
│   ├── radar.md                   ← Eyes/SOP_投资雷达.md
│   ├── strategy.md                ← Brain/SOP_策略分析.md
│   ├── research.md                ← Brain/SOP_初始调研.md
│   ├── target-management.md       ← 持仓与关注/SOP_标的管理.md
│   └── reconcile.md               ← 持仓与关注/SOP_持仓收口.md
├── prompts/
│   ├── p1-genesis.md              ← Brain/references/p1-genesis.md
│   ├── p2-phase-check.md          ← Brain/references/p2-phase-check.md
│   ├── p3-event-impact.md         ← Brain/references/p3-event-impact.md
│   ├── p4-radar.md                ← Brain/references/p4-radar.md
│   ├── p5-fomo-killer.md          ← Brain/references/p5-fomo-killer.md
│   ├── p6-profit-keeper.md        ← Brain/references/p6-profit-keeper.md
│   ├── p7-portfolio-check.md      ← Brain/references/p7-portfolio-check.md
│   ├── p8-macro-filter.md         ← Brain/references/p8-macro-filter.md
│   ├── p9-valuation.md            ← Brain/references/p9-valuation.md
│   ├── p10-options.md             ← Brain/references/p10-options.md
│   ├── p11-autopsy.md             ← Brain/references/p11-autopsy.md
│   ├── p12-referee.md             ← Brain/references/p12-referee.md
│   ├── p13-market-scanner.md      ← Brain/references/p13-market-scanner.md
│   ├── p14-sector-hunter.md       ← Brain/references/p14-sector-hunter.md
│   ├── p15-insight.md             ← Brain/references/p15-insight.md
│   ├── p16-earnings.md            ← Brain/references/p16-earnings.md
│   ├── p17-position-sizing.md     ← Brain/references/p17-position-sizing.md
│   ├── cio-rss-processor.md       ← Brain/references/cio-rss-processor.md
│   ├── route-cheatsheet.md        ← Brain/references/route-cheatsheet.md
│   └── watchlist-update-workflow.md ← Brain/references/watchlist-update-workflow.md
├── templates/
│   ├── knowledge-base.md          ← _模板_单标的/个股基础知识库.md
│   └── memo.md                    ← _模板_单标的/买入卖出备忘录.md
└── knowledge/
    ├── diagnosis/
    │   ├── diagnosis_case_library.md     ← ymos-diagnosis/knowledge/diagnosis_case_library.md
    │   └── investment_axioms_and_framework.md ← ymos-diagnosis/knowledge/investment_axioms_and_framework.md
    └── (未来可扩展的知识库)
```

### D2: SOP 重命名映射

| 原路径 | 新路径 |
|--------|--------|
| `Eyes/SOP_市场洞察.md` | `references/sops/market-insight.md` |
| `Eyes/SOP_投资雷达.md` | `references/sops/radar.md` |
| `Brain/SOP_策略分析.md` | `references/sops/strategy.md` |
| `Brain/SOP_初始调研.md` | `references/sops/research.md` |
| `持仓与关注/SOP_入职引导.md` | `references/sops/onboarding.md` |
| `持仓与关注/SOP_标的管理.md` | `references/sops/target-management.md` |
| `持仓与关注/SOP_持仓收口.md` | `references/sops/reconcile.md` |

### D3: 旧目录清理

迁移完成后删除：
- `Brain/references/`（整个目录）
- `持仓与关注/_模板_单标的/`
- `Brain/ymos-diagnosis/knowledge/`
- 各模块目录下的 `SOP_*.md` 文件

## Risks / Trade-offs

- **路径引用断裂**：迁移期间所有引用旧路径的文件（CLAUDE.md、总入口暗号、AGENT_GUIDE）暂时失效。缓解：在 entry-files-update 中统一修复
- **内容不变**：SOP 内容中的路径引用（如 `Brain/references/p13-market-scanner.md`）在本次 change 中暂不修改，由 entry-files-update 统一更新
