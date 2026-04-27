## Context

当前 YMOS 的文档架构为四层：`skills/ → references/ → data/ → cli/`。references/ 目录包含 31 个文件，分为 prompts (18)、sops (7)、knowledge (2)、templates (2)。每个 skill 的 SKILL.md 通过 `references/...` 路径引用这些文档，但文档与 skill 的归属关系仅在 SKILL.md 文本中隐式表达，无结构化依赖声明。

## Goals / Non-Goals

**Goals:**
- 每个 skill 目录自包含：SOP、prompts、knowledge 都在 skill 内，无外部 references 依赖
- 共享文档归入 `ymos-core` skill，其他 skill 通过显式依赖声明引用
- skills 有清晰的分层：core（基础层）→ 域 skill（业务层）
- 移除 `references/` 目录，简化架构为三层

**Non-Goals:**
- 不修改 Python CLI 代码或路由逻辑
- 不改变 P-series prompt 的内容（仅移动位置）
- 不引入新的 skill 格式或元数据系统（保持 SKILL.md 格式）
- 不修改 data/ 层或 cli/ 层

## Decisions

### 1. 新建 `ymos-core` 作为共享基础 skill

**选择**：创建 `skills/ymos-core/` 收纳所有跨 skill 共享文档。

**备选方案**：
- (A) 保留 references/ 但加索引文件 → 维持四层，未解决归属不清问题
- (B) 共享文档复制到每个需要的 skill → 产生冗余副本，同步困难

**理由**：ymos-core 既是 skill（有 SKILL.md 声明内容），又是依赖层（其他 skill 声明依赖它）。比保留 references/ 更清晰，比复制更 DRY。

### 2. Skill 内部目录结构

**选择**：每个 skill 采用统一子目录结构：

```
skills/<skill-name>/
  SKILL.md              # 能力描述（已存在）
  sop.md                # 该 skill 的 SOP（从 references/sops/ 移入）
  prompts/              # 该 skill 独占的 prompts（从 references/prompts/ 移入）
  knowledge/            # 该 skill 独占的知识文档（从 references/knowledge/ 移入）
```

ymos-core 额外包含：
```
skills/ymos-core/
  SKILL.md
  prompts/              # 共享 prompts (p2, p9)
  templates/            # 共享模板 (knowledge-base.md, memo.md)
  routing.md            # 路由速查表
  axioms.md             # 投资公理框架
```

**备选方案**：扁平结构（所有文件放 skill 根目录）→ 文件多时混乱，prompts 数量多的 skill（如 strategy 有 11 个 prompt）尤其严重。

**理由**：子目录分类清晰，与原 references/ 结构对齐，迁移成本低。

### 3. 依赖声明方式

**选择**：在 SKILL.md 的 frontmatter 中添加 `depends_on` 字段：

```yaml
---
name: ymos-strategy
depends_on: [ymos-core]
---
```

**备选方案**：
- (A) 单独的 dependencies.md 文件 → 额外文件，容易被忽略
- (B) 不声明依赖，仅在文本中引用路径 → 当前状态，隐式脆弱

**理由**：frontmatter 是 YAML 结构化数据，易于解析和验证。对现有格式侵入最小。

### 4. 路径引用格式

**选择**：skill 内部使用相对路径引用自己的文件，跨 skill 引用使用 `skills/<skill-name>/` 绝对路径。

- 自引用：`./prompts/p5-fomo-killer.md` 或 `prompts/p5-fomo-killer.md`
- 跨 skill：`skills/ymos-core/prompts/p2-phase-check.md`

**理由**：自引用相对路径让 skill 真正自包含（移动目录不影响内部引用）；跨 skill 绝对路径让依赖关系显式。

## Risks / Trade-offs

- **[Risk] 路径变更导致历史文档失效** → 所有 SKILL.md 中 `references/` 路径一次性替换，全局搜索确认无遗漏
- **[Risk] ymos-core 成为"垃圾桶"** → 严格限制：只有被 2+ skill 使用的文档才能放入 core，单使用者文档必须归属对应 skill
- **[Trade-off] 增加一层间接引用** → strategy 引用 p2 需要写 `skills/ymos-core/prompts/` 而非 `references/prompts/`，但依赖关系更清晰
- **[Trade-off] skill 目录膨胀** → strategy 将有 12 个文件（1 SKILL + 1 SOP + 10 prompts），比之前 1 个文件多，但换来自包含性
