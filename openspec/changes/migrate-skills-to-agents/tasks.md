## 1. 预检查

- [x] 1.1 验证 `.agents/skills/` 不在 `.gitignore` 中被忽略
- [x] 1.2 确认 `.agents/skills/` 下没有与 ymos 技能同名的目录（避免覆盖）

## 2. 迁移技能目录

- [x] 2.1 `git mv skills/ymos-core .agents/skills/ymos-core`
- [x] 2.2 `git mv skills/ymos-onboarding .agents/skills/ymos-onboarding`
- [x] 2.3 `git mv skills/ymos-market-insight .agents/skills/ymos-market-insight`
- [x] 2.4 `git mv skills/ymos-radar .agents/skills/ymos-radar`
- [x] 2.5 `git mv skills/ymos-research .agents/skills/ymos-research`
- [x] 2.6 `git mv skills/ymos-strategy .agents/skills/ymos-strategy`
- [x] 2.7 `git mv skills/ymos-target-mgmt .agents/skills/ymos-target-mgmt`
- [x] 2.8 `git mv skills/ymos-reconcile .agents/skills/ymos-reconcile`
- [x] 2.9 `git mv skills/ymos-diagnosis .agents/skills/ymos-diagnosis`
- [x] 2.10 `git mv skills/ymos-screener .agents/skills/ymos-screener`
- [x] 2.11 `git mv skills/ymos-sentiment .agents/skills/ymos-sentiment`
- [x] 2.12 删除空的 `skills/` 目录

## 3. 更新文档路径引用

- [x] 3.1 更新 `CLAUDE.md` 中所有 `skills/` 路径引用为 `.agents/skills/`
- [x] 3.2 更新 `AGENT_GUIDE.md` 中所有 `skills/` 路径引用为 `.agents/skills/`
- [x] 3.3 更新 `总入口暗号.md` 中所有 `skills/` 路径引用为 `.agents/skills/`
- [x] 3.4 更新 `setup.sh` 中 `SKILLS_SRC` 路径引用为 `.agents/skills/`
- [x] 3.5 更新 `进阶指南.md` 中 `skills/` 路径引用为 `.agents/skills/`
- [x] 3.6 更新 `README.md` 中 `skills/` 路径引用为 `.agents/skills/`
- [x] 3.7 更新 `docs/superpowers/specs/2026-05-01-tech-analysis-design.md` 中路径引用

## 4. 验证

- [x] 4.1 全项目 `grep -r "skills/" ` 扫描，确认无遗漏的 ymos 技能路径引用（排除 `.git/`、`data/`、`openspec/` 内部引用）
- [x] 4.2 验证 `.agents/skills/` 下 11 个技能目录均存在且结构完整
- [x] 4.3 验证 `git diff --stat` 仅显示 rename（无内容修改）
- [x] 4.4 验证 `skills/` 目录已不存在
