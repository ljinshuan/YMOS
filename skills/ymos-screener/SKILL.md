---
name: ymos-screener
metadata:
  depends_on: [ymos-core]
description: |
  多因子选股筛选，支持港股/美股/A股。触发方式：/ymos-screener、「帮我选股」「筛选一下」「找一下XX股」
  筛选结果可衔接 ymos-research 做深度调研。
---

# ymos-screener：选股筛选器

## 触发
- `帮我选股` — 交互式选股（询问市场和偏好）
- `筛选一下 [市场]` — 对指定市场执行默认筛选
- `找一下 [类型]股` — 按类型筛选（成长股/价值股/高息股/动量股）
- `选股` — 同「帮我选股」

## 前置条件
- 本地需运行 Futu OpenD（localhost:11111）
- 无状态机依赖（选股不依赖持仓/关注列表）

## 执行步骤
> 详细步骤见 sop.md

1. **解析筛选意图** — 确定市场（HK/US/CN）和筛选类型（预设/自定义）
2. **构建筛选条件** — 加载预设模板或解析自定义条件
3. **执行筛选** — 调用 `ymos screen --market MARKET --preset PRESET`
4. **展示结果** — 输出候选标的表格
5. **衔接调研**（可选）— 用户选择感兴趣的标的 → 触发 `调研一下 [ticker]`

## 产出物
- `data/reports/screener/YYYY-MM/screener_YYYYMMDD.json`（原始数据）
- `data/reports/screener/YYYY-MM/选股结果_YYYY-MM-DD.md`（可读报告）

## 边界
- 只做筛选发现，不做深度分析（ymos-research 的事）
- 不自动下单（筛选结果只供研究参考）
- 不维护本地股票数据库（完全依赖 Futu 实时数据）
- 不做量化回测或策略回测
