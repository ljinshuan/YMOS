## Context

YMOS 的投资雷达（ymos-radar）目前依赖价格扫描 + 基础技术信号，信号维度单一。富途提供完整的资金异动检测能力：资金分布（主力/散户资金流向）、经纪商买卖活动（哪些经纪商在买/卖）、资金流趋势（多日资金流变化）、做空量与比率。用户本地已安装 OpenD 客户端，可直接通过 OpenAPI 获取这些数据。

## Goals / Non-Goals

**Goals:**
- 新增 CLI 命令 `ymos fetch-capital-flow`，通过 Futu OpenD 获取资金流数据
- 新增 P20-capital-anomaly prompt，用于资金异动信号的结构化分析
- 将资金异动信号纳入 ymos-radar 的 SOP，作为价格扫描后的补充步骤
- 异动信号纳入 Tier 1/Tier 2 事件评级体系
- 在 ymos-strategy 的买入/加仓路由中，资金流作为正向确认维度

**Non-Goals:**
- 不构建实时资金流监控系统（batch 模式，随 radar 一起运行）
- 不做衍生品异动检测（期权/窝轮），这是独立的后续工作
- 不修改现有价格扫描逻辑，只在其后追加资金流步骤

## Decisions

### 1. 扩展 radar vs 新建 skill

**选择：扩展 ymos-radar，不新建独立 skill**

理由：资金异动检测的触发时机和周期与 radar 完全一致（随每日投资雷达一起跑），且输出融入同一个报告。用户不会单独"查资金流"——它是雷达信号的一部分。这与情绪分析不同（情绪是按需查询的独立 skill）。

### 2. CLI 命令粒度

**选择：单一命令 `ymos fetch-capital-flow --ticker TICKER`，支持 `--from-state` 批量模式**

理由：与 `ymos price-scan` 保持一致的模式。单个 ticker 直接查询，`--from-state` 遍历持仓+关注列表批量查询。输出 JSON 文件到 `data/reports/radar/raw/`。

### 3. P20 prompt 位置

**选择：放在 `skills/ymos-radar/prompts/` 下**

理由：P20 仅被 radar 使用，不属于跨 skill 共享资源，按 YMOS 规范应放在使用它的 skill 内部。

### 4. 与 Tier 1/Tier 2 评级体系的集成

**选择：资金异动信号作为 Tier 1 评级的加权因子**

理由：大单净流入/流出、经纪商集中买卖等信号对短期价格影响显著，应提升事件评级权重。具体规则：主力资金连续 3 日净流入 → Tier 1 加分；单日大单净流出超流通市值 1% → Tier 1 警告。

## Risks / Trade-offs

- **[OpenD 未运行]** → 同 sentiment 方案，检测连接状态并给出指引
- **[资金流数据延迟]** → A 股资金流数据通常有 15 分钟延迟，文档说明数据时效性
- **[数据覆盖差异]** → 港股/美股/A 股的资金流数据字段不同，CLI 需要按市场做字段映射
- **[误报风险]** → 资金异动不等同于价格异动，prompt 中需要强调"资金流是辅助信号，不构成独立买卖依据"
