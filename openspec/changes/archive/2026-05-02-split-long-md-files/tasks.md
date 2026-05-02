## 1. 盘点与规划

- [x] 1.1 扫描 skills/ 目录，列出所有超过 5KB/150 行的 MD 文件，确认拆分清单
- [x] 1.2 对每个候选文件分析其内部结构边界（路由、层、主题），确定拆分点和模式

## 2. SOP 文件拆分

- [x] 2.1 拆分 `skills/ymos-strategy/sop.md`（391行→248行）：提取 Route A-E 到 `sop/route-*.md`
- [x] 2.2 拆分 `skills/ymos-radar/sop.md`（361行→224行）：提取分析+触发、报告模板到子文件
- [x] 2.3 拆分 `skills/ymos-onboarding/sop.md`（229行→138行）：提取 Step 1 访谈到 `sop/step1-interview.md`
- [x] 2.4 拆分 `skills/ymos-reconcile/sop.md`（225行→159行）：提取 Dashboard 布局到 `sop/dashboard-layout.md`
- [x] 2.5 拆分 `skills/ymos-research/sop.md`（197行→160行）：提取 P-phase 执行到 `sop/p-phase-execution.md`
- [x] 2.6 拆分 `skills/ymos-target-mgmt/sop.md`（184行→85行）：按操作类型拆为 4 个 action 子文件
- [x] 2.7 拆分 `skills/ymos-market-insight/sop.md`（190行→130行）：提取数据加载到 `sop/data-loading.md`
- [x] 2.8 拆分 `skills/ymos-screener/sop.md`（143行/4KB）：低于阈值，不拆分

## 3. P-series Prompt 拆分

- [x] 3.1 拆分 `skills/ymos-research/prompts/p1-genesis.md`（424行→98行）：分类层保留，七维度提取为 `p1-genesis-deepdive.md`（332行）
- [x] 3.2 拆分 `skills/ymos-research/prompts/p4-radar.md`（263行→157行）：维度1-2保留，维度3-5提取为 `p4-radar-ext.md`（112行）
- [x] 3.3 拆分 `skills/ymos-core/prompts/p18-master-consultation.md`（209行→92行）：Buffett+Graham 保留，Marks+Lynch 提取为 `p18-master-consultation-ext.md`（121行）
- [x] 3.4 拆分 `skills/ymos-strategy/prompts/p12-referee.md`（145行）：评估后不拆分（结构紧凑，无自然边界）
- [x] 3.5 评估其他 P-series prompt：8 个文件均评估，低于阈值或无自然边界，均不拆分

## 4. Knowledge 文件拆分

- [x] 4.1 拆分 `skills/ymos-diagnosis/knowledge/investment_axioms_and_framework.md`（233行→154行）：核心公理保留，扩展内容提取为 `axioms-extended.md`（88行）
- [x] 4.2 拆分 `skills/ymos-diagnosis/knowledge/diagnosis_case_library.md`（203行→109行）：前3案例保留，后3案例提取为 `cases-extended.md`（103行）

## 5. 索引与路由更新

- [x] 5.1 为每个拆分后的原文件添加子文件路径索引表（路由映射）
- [x] 5.2 检查并更新相关 SKILL.md 中的文件引用路径 — 无需更新（路径不变）
- [x] 5.3 检查并更新 `skills/ymos-core/routing.md` 中的路径引用 — 无需更新（路径不变）

## 6. 验证

- [x] 6.1 验证每个拆分后的子文件内容与原文件对应段落完全一致（无语义丢失）
- [x] 6.2 模拟 agent 读取路径：SKILL.md → sop 索引 → 路由子文件，确认路由无缝衔接
- [x] 6.3 统计拆分前后的单次会话 token 消耗估算：索引文件总量 47% 缩减，典型场景 20-77% 缩减
