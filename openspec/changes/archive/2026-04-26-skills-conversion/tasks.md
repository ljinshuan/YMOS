## 1. 创建 Skills 目录结构

- [x] 1.1 创建 `skills/` 顶层目录
- [x] 1.2 创建 8 个 skill 子目录（ymos-onboarding、ymos-market-insight、ymos-radar、ymos-strategy、ymos-research、ymos-target-mgmt、ymos-reconcile、ymos-diagnosis）

## 2. 编写 Skill SKILL.md 文件

- [x] 2.1 编写 `skills/ymos-onboarding/SKILL.md`：触发词、引用 references/sops/onboarding.md、使用 ymos init/state
- [x] 2.2 编写 `skills/ymos-market-insight/SKILL.md`：触发词、引用 references/sops/market-insight.md、使用 ymos fetch-* 命令、引用 references/prompts/p13-market-scanner.md
- [x] 2.3 编写 `skills/ymos-radar/SKILL.md`：触发词、引用 references/sops/radar.md、使用 ymos price-scan/state、声明自动触发 ymos-market-insight
- [x] 2.4 编写 `skills/ymos-strategy/SKILL.md`：触发词、引用 references/sops/strategy.md、5 条路由、声明调用 ymos-research 补足缺失数据
- [x] 2.5 编写 `skills/ymos-research/SKILL.md`：触发词、引用 references/sops/research.md、P1+P4+P2+P9 链、声明可被其他 skill 组合引用
- [x] 2.6 编写 `skills/ymos-target-mgmt/SKILL.md`：触发词、引用 references/sops/target-management.md、4 个动作（关注/建仓/移除/清仓）
- [x] 2.7 编写 `skills/ymos-reconcile/SKILL.md`：触发词、引用 references/sops/reconcile.md、一致性校验 + Dashboard 生成
- [x] 2.8 迁移 `Brain/ymos-diagnosis/SKILL.md` → `skills/ymos-diagnosis/SKILL.md`，更新 knowledge 路径引用为 references/knowledge/diagnosis/

## 3. 清理旧 skill 位置

- [x] 3.1 删除 `Brain/ymos-diagnosis/` 目录（由 entry-files-update 负责处理，不在本任务范围）

## 4. 验证

- [x] 4.1 验证每个 SKILL.md 的 frontmatter 格式正确（name、description）
- [x] 4.2 验证每个 SKILL.md 中引用的 references/sops/ 和 references/prompts/ 路径存在
- [x] 4.3 验证共享 skill（ymos-research）被其他 skill 正确引用
- [x] 4.4 验证 ymos-diagnosis 的 knowledge 路径更新正确
