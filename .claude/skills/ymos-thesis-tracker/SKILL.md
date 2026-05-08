---
name: ymos-thesis-tracker
metadata:
  depends_on: [ymos-core]
description: |
  投资论点追踪与验证。触发方式：/ymos-thesis-tracker、「追踪论点」「论点怎么样」「更新论点」
  可被 ymos-research、ymos-strategy、ymos-radar 组合引用。
---

# ymos-thesis-tracker：投资论点追踪器

## 触发
- `追踪论点 [ticker]` — 查看或初始化论点追踪
- `论点怎么样 [ticker]` — 快速查看论点摘要（mini 模板）
- `更新论点 [ticker]` — 添加新的数据点/事件到论点追踪
- `验证论点 [ticker]` — 执行论点完整性检查

## 前置条件
- 个股文件夹应有 `个股基础知识库.md`（P1/P4 数据来源）
- `data/state/holdings.md` 或 `data/state/watchlist.md` 中应有该标的

## 执行步骤
> 详细步骤见 sop.md

1. **加载标的上下文** — 读取个股基础知识库、买入卖出备忘录、持仓状态
2. **检查论点追踪文件** — 若存在则加载，否则引导初始化
3. **执行操作** — 按用户意图执行：查看/更新/验证
4. **更新记分卡** — 根据最新数据更新支柱状态和趋势
5. **记录更新日志** — 追加事件、数据点、影响评估
6. **更新置信度** — 根据综合评估更新论点置信度和趋势

## 产出物
- `data/stocks/{ticker}/投资论点追踪.md`（主追踪文件）
- 个股知识库中的 P4 字段更新（置信度）

## 边界
- 不自动生成买入/卖出建议（ymos-strategy 的事）
- 不实时抓取新闻（ymos-radar 的事）
- 不改变 P1/P4/P2 核心逻辑
- 论点追踪文件是可选的，不影响现有流程
