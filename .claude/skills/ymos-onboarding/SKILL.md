---
name: ymos-onboarding
description: |
  系统冷启动与用户入职引导。触发方式：/ymos-onboarding、「开始使用」「初始化系统」「补全信息」
---

# ymos-onboarding：入职引导

## 触发
- `开始使用` — 完整入职引导
- `初始化系统` — 完整入职引导
- `补全信息` — 仅补全缺失部分

## 前置条件
- 无（这是系统的入口 skill）

自动检测逻辑（每次新会话）：
1. `data/当前关注方向与投资偏好.md` 是否有实质内容
2. `data/state/holdings.md` 是否有持仓行
3. `data/state/watchlist.md` 是否有关注行
4. Futu OpenD 是否在线（`ymos position fetch` 测试连接）

三者全空 → 完整引导；投资偏好为空 → 优先补全；仅缺持仓/Watchlist → 提示补全。

## 执行步骤
> 详细步骤见 sop.md

1. **Futu OpenD 检测**（可选）— 尝试连接 Futu OpenD，若在线则后续持仓录入可自动导入
2. **投资偏好深度访谈**（最核心）— 结构化 9 维度访谈，引导用户填写 `当前关注方向与投资偏好.md`
   - 投资者画像 / 仓位配置框架 / 仓位管理参数 / 策略立场 / 关注方向 / Watchlist 偏好 / 执行纪律 / 禁忌 / 核心心法
   - 写入前必须将完整内容展示给用户确认
3. **当前持仓录入** — 优先从 Futu OpenD 自动导入；否则手动录入，调用 `ymos-target-mgmt` 的建仓流程
4. **关注清单录入** — 调用 `ymos-target-mgmt` 的关注流程
5. **确认与引导下一步** — 提示用户可以跑市场洞察、投资雷达或调研

## Futu OpenD 集成能力

入职引导会检测 Futu OpenD 连接状态。若在线，可使用以下能力：

| 命令 | 能力 | 入职中的用途 |
|:---|:---|:---|
| `ymos position fetch` | 获取真实持仓 | 自动导入持仓，省去手动录入 |
| `ymos trade-history fetch` | 获取历史成交 | 初始化交易行为基线 |
| `ymos fetch-sentiment` | 个股评论情绪 | 非入职必需 |
| `ymos fetch-capital-flow` | 资金异动 | 非入职必需 |
| `ymos screen` | 选股筛选 | 非入职必需 |

> Futu OpenD 离线时，入职引导仍可正常完成（手动录入模式），不阻塞。

## 产出物
- `data/state/preferences.md`（用户确认后写入）
- `data/state/holdings.md`（新增持仓行）
- `data/state/watchlist.md`（新增关注行）
- 各标的文件夹（`data/stocks/{holdings,watchlist}/名称_TICKER/`）

## 边界
- 不做市场分析、不做策略推荐
- 持仓/关注的建档复用 `ymos-target-mgmt`，不重复实现
- 偏好文件写入前必须获得用户明确确认（Human-in-the-Loop）
