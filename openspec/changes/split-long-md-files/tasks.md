## 1. 盘点与规划

- [ ] 1.1 扫描 skills/ 目录，列出所有超过 5KB/150 行的 MD 文件，确认拆分清单
- [ ] 1.2 对每个候选文件分析其内部结构边界（路由、层、主题），确定拆分点和模式

## 2. SOP 文件拆分

- [ ] 2.1 拆分 `skills/ymos-strategy/sop.md`（15.5KB/386行）：提取 Step 1-5 公共步骤到索引文件，Route A-E 各自独立为 `sop/route-*.md`
- [ ] 2.2 拆分 `skills/ymos-radar/sop.md`（11.5KB/309行）：按执行步骤/扫描模式拆分
- [ ] 2.3 拆分 `skills/ymos-onboarding/sop.md`（7.8KB/229行）：按入职阶段拆分
- [ ] 2.4 拆分 `skills/ymos-reconcile/sop.md`（6.1KB/203行）：如结构允许则按校验步骤拆分
- [ ] 2.5 拆分 `skills/ymos-research/sop.md`（6KB/197行）：如结构允许则按调研阶段拆分
- [ ] 2.6 拆分 `skills/ymos-target-mgmt/sop.md`（6KB/184行）：按操作类型（关注/建仓/移除/清仓）拆分
- [ ] 2.7 拆分 `skills/ymos-market-insight/sop.md`（7.3KB/190行）：如结构允许则按流程阶段拆分
- [ ] 2.8 拆分 `skills/ymos-screener/sop.md`（4KB/143行）：视阈值情况决定是否拆分

## 3. P-series Prompt 拆分

- [ ] 3.1 拆分 `skills/ymos-research/prompts/p1-genesis.md`（20KB/424行）：第一层（机会分类）保留在原文件，第二层（七维度深度分析）提取为 `p1-genesis-deepdive.md`
- [ ] 3.2 拆分 `skills/ymos-research/prompts/p4-radar.md`（16KB/263行）：按分析维度/模块拆分
- [ ] 3.3 拆分 `skills/ymos-core/prompts/p18-master-consultation.md`（9KB/209行）：按大师视角拆分
- [ ] 3.4 拆分 `skills/ymos-strategy/prompts/p12-referee.md`（8.4KB/145行）：如结构允许则按纪律模块拆分
- [ ] 3.5 评估其他 P-series prompt 是否超过阈值，按需拆分

## 4. Knowledge 文件拆分

- [ ] 4.1 拆分 `skills/ymos-diagnosis/knowledge/investment_axioms_and_framework.md`（11KB）：核心公理保留，扩展内容提取为子文件
- [ ] 4.2 拆分 `skills/ymos-diagnosis/knowledge/diagnosis_case_library.md`（11KB）：按诊断类型/主题拆分

## 5. 索引与路由更新

- [ ] 5.1 为每个拆分后的原文件添加子文件路径索引表（路由映射）
- [ ] 5.2 检查并更新相关 SKILL.md 中的文件引用路径
- [ ] 5.3 检查并更新 `skills/ymos-core/routing.md` 中的路径引用

## 6. 验证

- [ ] 6.1 验证每个拆分后的子文件内容与原文件对应段落完全一致（无语义丢失）
- [ ] 6.2 模拟 agent 读取路径：SKILL.md → sop 索引 → 路由子文件，确认路由无缝衔接
- [ ] 6.3 统计拆分前后的单次会话 token 消耗估算，确认 30-50% 降幅目标
