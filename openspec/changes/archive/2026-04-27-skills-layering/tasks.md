## 1. 新建 ymos-core skill

- [x] 1.1 创建 `skills/ymos-core/` 目录结构（SKILL.md、prompts/、templates/）
- [x] 1.2 编写 `skills/ymos-core/SKILL.md`（frontmatter 含 name/description，body 列出所有共享资源清单）
- [x] 1.3 移动 `references/prompts/p2-phase-check.md` → `skills/ymos-core/prompts/p2-phase-check.md`
- [x] 1.4 移动 `references/prompts/p9-valuation.md` → `skills/ymos-core/prompts/p9-valuation.md`
- [x] 1.5 移动 `references/templates/knowledge-base.md` → `skills/ymos-core/templates/knowledge-base.md`
- [x] 1.6 移动 `references/templates/memo.md` → `skills/ymos-core/templates/memo.md`
- [x] 1.7 移动 `references/prompts/route-cheatsheet.md` → `skills/ymos-core/routing.md`
- [x] 1.8 移动 `references/prompts/watchlist-update-workflow.md` → `skills/ymos-core/watchlist-update-workflow.md`

## 2. ymos-market-insight 吸收文档

- [x] 2.1 创建 `skills/ymos-market-insight/prompts/` 目录
- [x] 2.2 移动 `references/sops/market-insight.md` → `skills/ymos-market-insight/sop.md`
- [x] 2.3 移动 `references/prompts/p13-market-scanner.md` → `skills/ymos-market-insight/prompts/p13-market-scanner.md`
- [x] 2.4 移动 `references/prompts/p14-sector-hunter.md` → `skills/ymos-market-insight/prompts/p14-sector-hunter.md`
- [x] 2.5 移动 `references/prompts/p15-insight.md` → `skills/ymos-market-insight/prompts/p15-insight.md`
- [x] 2.6 移动 `references/prompts/p16-earnings.md` → `skills/ymos-market-insight/prompts/p16-earnings.md`
- [x] 2.7 移动 `references/prompts/cio-rss-processor.md` → `skills/ymos-market-insight/prompts/cio-rss-processor.md`
- [x] 2.8 更新 `skills/ymos-market-insight/SKILL.md` 中所有 references/ 路径为新路径

## 3. ymos-research 吸收文档

- [x] 3.1 创建 `skills/ymos-research/prompts/` 目录
- [x] 3.2 移动 `references/sops/research.md` → `skills/ymos-research/sop.md`
- [x] 3.3 移动 `references/prompts/p1-genesis.md` → `skills/ymos-research/prompts/p1-genesis.md`
- [x] 3.4 移动 `references/prompts/p4-radar.md` → `skills/ymos-research/prompts/p4-radar.md`
- [x] 3.5 更新 `skills/ymos-research/SKILL.md` 中所有 references/ 路径为新路径，添加 `depends_on: [ymos-core]`

## 4. ymos-strategy 吸收文档

- [x] 4.1 创建 `skills/ymos-strategy/prompts/` 目录
- [x] 4.2 移动 `references/sops/strategy.md` → `skills/ymos-strategy/sop.md`
- [x] 4.3 移动 `references/prompts/p3-event-impact.md` → `skills/ymos-strategy/prompts/p3-event-impact.md`
- [x] 4.4 移动 `references/prompts/p5-fomo-killer.md` → `skills/ymos-strategy/prompts/p5-fomo-killer.md`
- [x] 4.5 移动 `references/prompts/p6-profit-keeper.md` → `skills/ymos-strategy/prompts/p6-profit-keeper.md`
- [x] 4.6 移动 `references/prompts/p7-portfolio-check.md` → `skills/ymos-strategy/prompts/p7-portfolio-check.md`
- [x] 4.7 移动 `references/prompts/p8-macro-filter.md` → `skills/ymos-strategy/prompts/p8-macro-filter.md`
- [x] 4.8 移动 `references/prompts/p10-options.md` → `skills/ymos-strategy/prompts/p10-options.md`
- [x] 4.9 移动 `references/prompts/p11-autopsy.md` → `skills/ymos-strategy/prompts/p11-autopsy.md`
- [x] 4.10 移动 `references/prompts/p12-referee.md` → `skills/ymos-strategy/prompts/p12-referee.md`
- [x] 4.11 移动 `references/prompts/p17-position-sizing.md` → `skills/ymos-strategy/prompts/p17-position-sizing.md`
- [x] 4.12 更新 `skills/ymos-strategy/SKILL.md` 中所有 references/ 路径为新路径，添加 `depends_on: [ymos-core]`

## 5. ymos-radar 吸收文档

- [x] 5.1 移动 `references/sops/radar.md` → `skills/ymos-radar/sop.md`
- [x] 5.2 更新 `skills/ymos-radar/SKILL.md` 中所有 references/ 路径为新路径，添加 `depends_on: [ymos-core]`

## 6. ymos-onboarding 吸收文档

- [x] 6.1 移动 `references/sops/onboarding.md` → `skills/ymos-onboarding/sop.md`
- [x] 6.2 更新 `skills/ymos-onboarding/SKILL.md` 中 references/ 路径为新路径

## 7. ymos-reconcile 吸收文档

- [x] 7.1 移动 `references/sops/reconcile.md` → `skills/ymos-reconcile/sop.md`
- [x] 7.2 更新 `skills/ymos-reconcile/SKILL.md` 中 references/ 路径为新路径

## 8. ymos-target-mgmt 吸收文档

- [x] 8.1 移动 `references/sops/target-management.md` → `skills/ymos-target-mgmt/sop.md`
- [x] 8.2 更新 `skills/ymos-target-mgmt/SKILL.md` 中 references/ 路径为新路径，添加 `depends_on: [ymos-core]`

## 9. ymos-diagnosis 吸收文档

- [x] 9.1 创建 `skills/ymos-diagnosis/knowledge/` 目录
- [x] 9.2 移动 `references/knowledge/diagnosis/investment_axioms_and_framework.md` → `skills/ymos-diagnosis/knowledge/investment_axioms_and_framework.md`
- [x] 9.3 移动 `references/knowledge/diagnosis/diagnosis_case_library.md` → `skills/ymos-diagnosis/knowledge/diagnosis_case_library.md`
- [x] 9.4 更新 `skills/ymos-diagnosis/SKILL.md` 中 references/ 路径为新路径

## 10. 清理与更新

- [x] 10.1 确认 `references/` 目录为空，删除整个目录
- [x] 10.2 更新 `CLAUDE.md`：架构描述从四层改为三层，移除 references 层说明，更新路径规则
- [x] 10.3 更新 `AGENT_GUIDE.md`：所有 references/ 引用更新为 skills/ 路径
- [x] 10.4 全局搜索验证：确认项目中无残留的 `references/` 路径引用
