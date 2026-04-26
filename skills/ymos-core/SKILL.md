---
name: ymos-core
description: |
  YMOS 基础设施 skill，收纳跨 skill 共享的 prompts、templates、路由表和工作流。
  其他 skill 通过 depends_on: [ymos-core] 声明依赖。
---

# ymos-core：共享基础设施

本 skill 是 YMOS 的基础依赖层，提供被 2 个及以上 skill 共享的文档资源。

## 共享资源清单

### Prompts（共享提示词）
- `prompts/p2-phase-check.md` — 阶段判断，被 ymos-research、ymos-strategy 使用
- `prompts/p9-valuation.md` — 反向 DCF 估值，被 ymos-research、ymos-strategy 使用

### Templates（共享模板）
- `templates/knowledge-base.md` — 个股基础知识库模板，被 ymos-target-mgmt、ymos-research 使用
- `templates/memo.md` — 买入卖出备忘录模板，被 ymos-target-mgmt 使用

### 路由与工作流
- `routing.md` — 路由速查表（暗号 → skill 映射）
- `watchlist-update-workflow.md` — 关注列表更新标准流程，被 ymos-radar、ymos-target-mgmt 使用

## 使用方式

其他 skill 的 SKILL.md frontmatter 中添加：
```yaml
depends_on: [ymos-core]
```

引用路径格式：
- `skills/ymos-core/prompts/<file>`
- `skills/ymos-core/templates/<file>`
- `skills/ymos-core/routing.md`
- `skills/ymos-core/watchlist-update-workflow.md`
