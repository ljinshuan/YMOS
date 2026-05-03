## Context

YMOS 的分析架构是「个股为中心」——P1 基石建档、P4 雷达、P2 阶段判断、策略路由全部围绕单只股票。大盘和板块只存在于 P13 市场洞察的文字新闻描述中，没有量化的价格/技术面追踪。

CLI 工具层已完全具备对任意 ETF 做价格扫描（`ymos price-scan --symbols`）和技术分析（`ymos tech-analysis analyze --symbols`）的能力，数据源支持 Yahoo Finance（免费，美股/港股/ETF 通用）、Tushare（A 股）、Futu OpenD。缺口在 skill 编排层——没有流程去调用这些工具做大盘/板块分析。

当前持仓：SOXL(半导体ETF)、META、INTC、CRDO、BABA，涉及半导体、社交、通信芯片、中概等多个板块，但雷达扫描时看不到板块层面的资金流向和趋势。

## Goals / Non-Goals

**Goals:**
- 每次雷达扫描时自动获取大盘+板块 ETF 的技术面数据
- 提供三层信号联动判断（大盘→板块→个股），作为雷达和策略的决策输入
- 维护 ticker→板块 ETF 映射，新增持仓时自动关联板块
- 将量化技术面数据注入 P13 市场洞察分析，减少对纯文字新闻的依赖

**Non-Goals:**
- 不新建数据源（复用现有 Yahoo/Finnhub/Tushare）
- 不新建 CLI 命令（复用 `ymos price-scan` 和 `ymos tech-analysis`）
- 不做实时行情推送（保持 batch 模式）
- 不做量化策略回测或自动化交易
- 不修改 P1/P4/P2 的核心 prompt 内容（只增加输入数据）

## Decisions

### D1: 大盘锚点配置位置 → `data/state/market_anchors.md`

**选择**: 独立状态机文件，不放在 preferences.md 中。

**理由**: preferences.md 是用户偏好（风险承受、投资风格），大盘锚点是运行时配置（关注哪些指数 ETF），语义不同。独立文件便于 radar 流程独立读取，也便于未来支持多市场锚点（美股看 QQQ、A 股看 510300、港股看 2800.HK）。

**格式**: 简单 Markdown 表格，同 holdings.md 风格。

**替代方案**: 放在 preferences.md → 混杂了偏好和配置，每次雷达扫描要解析整个偏好文件。

### D2: 板块-个股映射位置 → `data/state/sector_mapping.md`

**选择**: 独立状态机文件，维护 `ticker → sector ETF` 双向映射。

**理由**: 映射表需要双向查询——扫描个股时找板块 ETF，看板块时找持仓个股。独立文件结构清晰，radar 和 strategy 都能引用。

**格式**: Markdown 表格，包含 Ticker、板块名称、板块 ETF、市场列。

**替代方案**: 嵌入 holdings.md → 增加状态机复杂度，且 watchlist 中的个股也需要映射。

### D3: 三层信号注入方式 → 作为 radar SOP 的前置步骤

**选择**: 在 radar 流程的「价格扫描」步骤之前，增加「大盘+板块扫描」步骤。结果作为雷达桥接报告的独立 section 输出。

**理由**: 不修改现有 P-series prompt 的输入格式，避免级联影响。雷达报告已有结构化模板，增加一个 section 即可。strategy 流程在读取雷达报告时自然获得三层信号上下文。

**数据流**:
```
market_anchors.md → 提取大盘 ETF 列表
sector_mapping.md + holdings.md → 提取板块 ETF 列表
    ↓
ymos price-scan --symbols QQQ,SOXX,XLK,KWEB
ymos tech-analysis analyze --symbols QQQ,SOXX,XLK,KWEB
    ↓
大盘/板块技术面 JSON → 注入雷达桥接报告 "三层信号联动" section
    ↓
个股价格扫描 + 资金流（现有流程不变）
    ↓
综合分析时引用三层信号判断顺风/逆风
```

**替代方案**: 修改 P13 prompt 增加技术面输入 → P13 是市场洞察的 prompt，关注点是新闻事件分析，塞入技术指标会改变 prompt 定位。

### D4: P14 板块猎手触发方式 → radar 流程自动触发

**选择**: 当 radar 检测到持仓涉及的板块有显著技术面信号时（偏多或偏空信号占比 > 60%），自动触发 P14 对该板块做深度分析。

**理由**: P14 已有成熟的板块分析 prompt，只需在 radar SOP 中增加条件触发。不需要修改 P14 本身。

**条件**: 板块 ETF 技术分析 verdict 为「偏多⬆」或「偏空⬇」时才触发，「中性➡」跳过。

## Risks / Trade-offs

- **[Yahoo 限流]** → 多个 ETF 批量请求可能触发 Yahoo API 限流。缓解：每次最多扫描 5-8 个 ETF，且 Yahoo 返回 1 年日线只需单次请求。
- **[映射表维护成本]** → 新增持仓时需要手动或半自动更新 sector_mapping。缓解：research 流程（P1）可建议映射关系，用户确认后写入。
- **[雷达执行时间增加]** → 增加大盘+板块扫描步骤会使雷达流程多 10-20 秒。缓解：技术面分析可并行执行，且 ETF 数量有限。
- **[板块分类粒度]** → 同一股票可能属于多个板块（如 NVDA 既是大盘科技也是半导体、AI）。缓解：映射表中每个 ticker 只映射一个「最相关」的板块 ETF，避免过度复杂。
