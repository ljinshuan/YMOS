## Context

YMOS 的 skills/ 目录包含 268KB / 6380 行 MD 文件，其中 Top 10 文件占总量 44%。当前 agent 路由机制是逐层收窄的（SKILL.md → sop.md → p-series prompt），但 SOP 文件内部没有按路由拆分，导致 agent 必须 15KB 全量读取，即使只走其中一条路由。

典型会话 token 消耗：仅 prompt 内容就 50-70KB（~15K-20K input tokens），其中约 30-40% 是不必要的内容。

## Goals / Non-Goals

**Goals:**
- 将 8-10 个大型 MD 文件按路由/层/主题拆分为独立小文件
- 每个 SOP 拆分后保留索引文件（公共步骤 + 路由 → 子文件映射）
- 保持 agent 路由机制无缝衔接（无需修改 agent 行为）
- 单次会话 prompt token 消耗降低 30-50%

**Non-Goals:**
- 不引入摘要脚本或预处理机制（ROI 不如结构化拆分）
- 不修改 SKILL.md 文件（已经足够小，是天然的索引层）
- 不修改任何 Python 代码（纯文档结构优化）
- 不改变 prompt 的语义内容（只拆分，不重写）

## Decisions

### D1: 拆分阈值 = 5KB / 150 行

低于此阈值的文件不拆分（如大多数 SKILL.md、小 prompt）。5KB 以上才考虑拆分。

**替代方案**: 按文件类型统一阈值（如所有 SOP 都拆）→ 拒绝，因为有些 SOP 已经足够紧凑。

### D2: SOP 拆分模式 — 公共步骤 + 路由子文件

```
skills/ymos-strategy/
  sop.md                    ← 保留：Step 1-5 公共步骤 + 路由索引表
  sop/                      ← 新增目录
    route-a-buy.md          ← 路由A：首次建仓
    route-b-add.md          ← 路由B：加仓
    route-c-hold.md         ← 路由C：持有评估
    route-d-sell.md         ← 路由D：减仓/卖出
    route-e-rebalance.md    ← 路由E：仓位再平衡
```

原 sop.md 底部替换为路径索引：
```markdown
## 路由子文件
执行完上述公共步骤后，根据路由结果读取对应子文件：
- Route A（买入）→ `sop/route-a-buy.md`
- Route B（加仓）→ `sop/route-b-add.md`
- ...
```

**替代方案**: 用文件名约定如 `sop--route-a.md` 扁平存放 → 拒绝，子目录更清晰，避免文件名冲突。

### D3: P-series prompt 拆分模式 — 按结构层

p1-genesis.md (20KB) 有明确的两层结构：
```
prompts/
  p1-genesis.md             ← 保留：索引 + 第一层（机会分类）~8KB
  p1-genesis-deepdive.md    ← 新增：第二层（七维度深度分析）~12KB
```

**替代方案**: 拆成更多文件 → 拒绝，两层是 p1 的自然边界，过度拆分增加 agent 的决策负担。

### D4: Knowledge 文件拆分模式 — 按主题

investment_axioms_and_framework.md (11KB) 包含多个独立公理：
```
knowledge/
  investment-axioms.md      ← 保留：公理索引 + 前 5 条核心公理 ~6KB
  investment-axioms-ext.md  ← 新增：扩展公理 + 详细案例 ~5KB
```

**替代方案**: 每条公理一个文件 → 拒绝，粒度太细，增加读取次数。

## Risks / Trade-offs

- **[碎片化风险]** 拆分后文件数量增加 2-3 倍 → 通过索引文件 + 子目录结构保持可发现性
- **[上下文断裂]** agent 读路由子文件时可能丢失公共步骤的上下文 → 索引文件明确标注"需先读完公共步骤"
- **[维护成本]** 修改 prompt 时需要定位到正确的子文件 → 子文件命名清晰，IDE 全局搜索不受影响
- **[过度拆分]** 可能对边界模糊的文件拆错 → 只拆有明确结构边界的文件，其余保持原样
