---
name: ymos-research
metadata:
  depends_on: [ymos-core]
description: |
  个股深度调研（P1+P4+P2）。触发方式：/ymos-research、「调研一下 [ticker]」
  可被 ymos-strategy、ymos-target-mgmt、ymos-onboarding 组合引用。
---

# ymos-research：初始调研

## 触发
- `调研一下 [ticker/名称]` — 深度调研（P1 → P4 → P2 + P9）
- `大师会诊 [ticker/名称]` — 深度调研 + 大师多视角验证（P1 → P4 → P18 → P2）

## 前置条件
- 无强制前置（可独立运行）

## 调用接口

| 调用方 | 触发场景 | 传入参数 |
|:---|:---|:---|
| 用户直接 | `调研一下 XX` | ticker + 名称 |
| ymos-target-mgmt | `关注 XX` / `建仓 XX` | ticker + 名称 + 位置 |
| ymos-strategy | 策略路由发现缺 P1/P4 | ticker + 位置 |
| ymos-radar | 雷达建议调研的标的 | ticker + 名称 + 位置 |
| ymos-screener | 筛选结果中选择调研 | ticker 列表（批量） |

## 执行步骤
> 详细步骤见 sop.md

1. **确认标的信息** — 解析 ticker、名称、所属市场、确认位置（持仓/Watchlist）
2. **检查个股基础知识库** — 读取或创建最小骨架
3. **执行 P1 Genesis 基石建档**（`prompts/p1-genesis.md`）
   - 治理结构 / 商业壁垒 / 财务健康 / 周期维度 / PVE-PVP 初判
   - AI 搜索补足公开信息，标注来源和时效性
4. **执行 P4 Radar 关注点雷达**（`prompts/p4-radar.md`）
   - 五维度：本体核心 / 叙事验证 / 直接竞品 / 产业链 / 宏观与行业
   - 同步更新状态机 P4 摘要
5. **[可选] 执行 P18 大师会诊**（`skills/ymos-core/prompts/p18-master-consultation.md`）
   - 触发条件：用户明确请求"大师会诊"或"多视角分析"
   - 四大师 lens 交叉验证：巴菲特（护城河）、格雷厄姆（安全边际）、马克斯（周期）、林奇（成长）
   - 输出追加到个股基础知识库"大师会诊"章节
   - 标准调研流程中默认不包含此环节
6. **执行 P2 Phase Check 阶段判断**（`skills/ymos-core/prompts/p2-phase-check.md`）
   - PVE/PVP 特征扫描 / 玩家识别 / 叙事验证状态 / 三情景预演
7. **执行 P9 估值分析**（仅用户直接调用时，`skills/ymos-core/prompts/p9-valuation.md`）
   - 被其他 skill 调用时跳过（P9 在策略路由中按需触发）
8. **输出确认** — 汇报完成状态 + 待人工补充项
9. **[可选] 初始化论点追踪** — 调研完成后询问用户是否初始化论点追踪（`ymos-thesis-tracker`）
10. **[可选] 启动 DCF 建模** — P9 估值后可选触发 DCF 深度建模（`ymos-dcf-model`）

## 产出物
- `data/stocks/{holdings,watchlist}/名称_TICKER/个股基础知识库.md`（P1+P4+可选P18+P2+可选P9）
- 状态机 P4 摘要同步更新（强制三步：更新时间 + 标的行 + 变更日志）
- P18 大师会诊报告（仅用户请求时）追加到个股基础知识库

## 边界
- 只做 P1+P4+P2（直接调用时加 P9；用户请求时在 P4 和 P2 之间插入 P18）
- 不做策略制定（ymos-strategy 的事）
- 不修改状态机的身份/状态列（ymos-target-mgmt 的事），只更新 P4 关注点列
