---
name: ymos-catalyst-calendar
metadata:
  depends_on: [ymos-core]
description: |
  催化剂日历管理，收集和展示即将到来的关键投资事件。触发方式：/ymos-catalyst-calendar、「看一下日历」「下周有什么事件」「催化剂日历」
  可被 ymos-radar、ymos-strategy、ymos-thesis-tracker 组合引用。
---

# ymos-catalyst-calendar：催化剂日历

## 触发
- `催化剂日历` — 查看全局催化剂日历
- `下周有什么事件` — 查看下周关键事件
- `看一下日历 [ticker]` — 查看某标的的催化剂
- `添加事件` — 手动添加催化剂事件
- `看一下财报日期 [ticker]` — 查看财报发布日期

## 前置条件
- `data/state/holdings.md` 或 `data/state/watchlist.md` 应有内容（用于关联标的）
- 无状态机依赖（日历独立运行）

## 执行步骤
> 详细步骤见 sop.md

1. **加载日历数据** — 读取全局催化剂日历
2. **按需筛选** — 按标的/类型/影响等级/时间范围
3. **展示事件** — 按日期排序，高亮高影响事件
4. **生成每周预览**（可选）— 汇总本周关键事件 + 下周前瞻

## 产出物
- `data/reports/catalyst-calendar/YYYY-MM/催化剂日历.md`（全局日历）
- `data/reports/catalyst-calendar/YYYY-MM/催化剂周报_YYYY-MM-DD.md`（每周预览）
- Excel 导出（可选）

## 边界
- 不实时推送通知（用户主动查看）
- 不自动执行交易
- 不维护历史事件数据库（关注未来）
- 财报日期通过 API 获取，宏观事件手动维护
