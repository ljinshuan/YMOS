## Context

YMOS 目前只能分析已知标的（从持仓/关注列表中选择），缺乏主动选股能力。富途提供完整的选股筛选器（Stock Screener），支持按市值、PE、PB、ROE、涨幅、换手率、板块等多维度组合过滤，覆盖港股、美股、A股。用户本地已安装 OpenD 客户端。

YMOS 的 research pipeline（P1→P4→P2）已经能对新标的做深度分析，缺的是"发现候选标的"这一前置环节。

## Goals / Non-Goals

**Goals:**
- 新增 `skills/ymos-screener/` skill，支持基本面/技术面多因子筛选
- 新增 CLI 命令 `ymos screen`，通过 Futu OpenD 执行选股筛选
- 支持预设筛选模板（成长股、价值股、高息股、动量股等）和自定义条件
- 筛选结果输出候选标的列表，可直接接入 ymos-research pipeline
- 触发词：「帮我选股」「筛选一下港股」「找一下成长股」

**Non-Goals:**
- 不实现量化回测或策略回测
- 不做自动下单（筛选结果只供研究参考）
- 不维护本地股票数据库（完全依赖 Futu 实时数据）

## Decisions

### 1. 新建独立 skill

**选择：新建 `ymos-screener` 独立 skill**

理由：选股是一个独立的工作流，有独特的触发词、输入参数和输出格式。它不依赖 radar/strategy 的执行周期，是用户主动触发的"发现"行为。与 ymos-research 的关系是：screener 输出候选列表 → 用户选择感兴趣的标的 → 触发 research pipeline。

### 2. 预设模板设计

**选择：内置 4 个预设模板 + 支持自定义条件组合**

预设模板：
- **成长股**：营收增速 > 20%、净利润增速 > 15%、市值 > 100 亿
- **价值股**：PE < 15、PB < 1.5、ROE > 10%、股息率 > 2%
- **高息股**：股息率 > 4%、PE < 20、市值 > 50 亿
- **动量股**：20 日涨幅 > 10%、换手率 > 3%、市值 > 30 亿

自定义条件通过 JSON 配置文件传入：`ymos screen --config screener-config.json`

### 3. CLI 命令接口设计

**选择：`ymos screen --market HK --preset growth --limit 20`**

理由：市场参数必填（HK/US/CN），预设模板和自定义条件二选一。limit 控制返回数量。输出 JSON 文件到 `data/reports/screener/`。

替代方案：无参数直接交互式筛选——不利于自动化和 skill 集成。

### 4. 与 research pipeline 的衔接

**选择：screener 输出 JSON 列表，用户选择后触发 research**

理由：screener 可能返回 20+ 只候选股票，不可能全部做深度研究。用户先浏览筛选结果，选出感兴趣的 1-3 只，然后逐个触发 `调研一下 [ticker]`。这种"先广后深"的模式符合 YMOS 的 Human-in-the-Loop 哲学。

在 routing.md 中新增：`选股结果 → 用户选择 → 触发 ymos-research`

### 5. skill 依赖声明

**选择：`depends_on: [ymos-core]`**

理由：screener 需要引用 ymos-core 的路由表（routing.md），且后续可能复用 ymos-core 的 templates。虽然当前不直接使用 P-series prompts，但保持与其他 skill 一致的依赖模式。

## Risks / Trade-offs

- **[OpenD 未运行]** → 同其他方案，检测连接状态并给出指引
- **[筛选条件过宽/过窄]** → 预设模板经过调优，自定义条件需要用户自行验证
- **[市场覆盖差异]** → 不同市场的筛选字段不完全一致（A 股有涨跌停限制等），文档说明差异
- **[候选数量过多]** → 默认 limit=20，超过时提示用户缩小条件范围
