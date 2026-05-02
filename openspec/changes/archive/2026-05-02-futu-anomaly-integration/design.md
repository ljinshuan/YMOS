## Context

YMOS 投资雷达当前覆盖价格扫描（三源分流）和资金流扫描（Futu OpenD `get_financial_unusual`），通过 P20 prompt 做异动分析。技术面和衍生品两个信号维度完全缺失。

Futu OpenD 提供了三个异动检测 API：
- `get_technical_unusual` — 技术指标异常检测，含 K 线形态 + 14 种指标
- `get_derivative_unusual` — 衍生品异常检测，含牛熊证（港股）/ 期权七维信号
- `get_financial_unusual` — 资金异动检测（已在用，但只用了部分维度）

现有 `.futu-skills/futu/` 目录下有 Futu 官方提供的 6 个 skill 定义文件和 3 个 Python 脚本，定义了完整的调用协议、输出格式和路由逻辑。

### 约束
- 所有异动检测依赖 Futu OpenD（localhost:11111），OpenD 未运行时必须优雅降级
- YMOS ticker 格式（`0700.HK`、`AAPL`、`688008.SS`）需转换为 Futu 格式（`HK.00700`、`US.AAPL`、`SH.688008`）
- 技术面和衍生品检测是只读操作，不修改状态机

## Goals / Non-Goals

**Goals:**
- 新增技术面异动检测 CLI 命令和 skill 集成
- 新增衍生品异动检测 CLI 命令和 skill 集成
- 将技术面和衍生品信号接入投资雷达报告
- 增强资金异动检测维度（卖空异动、经纪商追踪）
- 增强情绪分析输出标准化

**Non-Goals:**
- 不做实时异动推送/监控（保持 batch 按需查询模式）
- 不新建独立的 ymos-technical 或 ymos-derivatives skill（作为 ymos-radar 的子能力集成）
- 不引入新的 Python 依赖（复用现有 OpenD 连接机制）
- 不修改 P 系列提示词框架（技术面/衍生品数据作为 P20 的输入增强）

## Decisions

### D1: 异动检测作为 CLI 命令 + radar 集成，而非独立 skill

**选择**：新增 `ymos fetch-technical-anomaly` 和 `ymos fetch-derivatives-anomaly` CLI 命令，在 ymos-radar 的资金流扫描步骤后并行调用，结果汇入雷达报告。

**替代方案**：创建独立的 ymos-technical-anomaly 和 ymos-derivatives-anomaly skill。

**理由**：异动检测是雷达信号层的一部分，与价格扫描、资金流扫描同构。用户不需要单独触发「查一下技术面异动」——它应该是雷达流程的自动环节。保持与现有 `fetch-capital-flow` 一致的架构模式。

### D2: Ticker 格式转换复用现有路由

**选择**：在 `cli/core/router.py` 或新建 `cli/core/ticker_normalize.py` 中添加 YMOS→Futu 格式转换函数，供所有 OpenD 调用共享。

**理由**：现有 `futu_news.py` 里有 `ticker_to_news_keyword()` 做类似转换但不完全一致。统一为 Futu OpenD 标准格式（`US.TSLA`、`HK.00700`、`SH.600519`、`SZ.300750`）。

### D3: 技术面异动输出为标准化 JSON

**选择**：参考 Futu skill 定义的输出格式，每个指标独立一个条目，包含日期、信号方向、异常描述。JSON schema 统一。

**理由**：标准化输出便于 P20 prompt 解析和雷达报告生成，也与现有 capital flow JSON 格式对齐。

### D4: 资金异动增强通过扩展现有 CLI 参数

**选择**：在 `ymos fetch-capital-flow` 增加 `--dimensions` 参数，可选 `funds_distribution`、`funds_broker`、`funds_flow`、`short_sell_number`、`short_sell_ratio`，默认全扫。

**理由**：不破坏现有调用方式，通过可选参数增加新维度。

### D5: 情绪分析增强通过升级 P19 prompt 和 CLI 输出

**选择**：升级 `ymos fetch-sentiment` 的 JSON 输出增加 group 聚合字段，升级 P19 prompt 支持多符号 group 模式和 empty-result fallback。

**理由**：不改变触发方式和 skill 结构，只增强内部逻辑。

## Risks / Trade-offs

- **[OpenD 依赖]** → 所有异动检测需要 OpenD 运行。缓解：与资金流扫描一致，OpenD 不可达时跳过并标注，不阻塞雷达流程
- **[港股特有维度]** → 牛熊证街货仅适用港股。缓解：非港股标的自动跳过牛熊证维度，输出标注「不适用」
- **[数据量膨胀]** → 雷达报告增加两个 section 可能过长。缓解：默认只输出有异常的指标，无异常的折叠为一行
- **[Futu ticker 映射不完整]** → 用户自定义的中文名映射可能不全。缓解：维护可扩展的映射表，未命中时要求用户澄清
