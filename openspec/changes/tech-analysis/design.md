## Context

YMOS 是一个自然语言驱动的投资研究系统，当前策略分析完全基于基本面和消息面。CLI 层已有 Finnhub/Tushare/Yahoo 三个数据源，能获取实时报价和有限历史数据（Yahoo 支持 1mo-5y，Tushare 默认 7 天），但没有技术分析能力。

现有数据获取使用 `requests`/`urllib` 返回 dict/JSON，无 pandas 依赖。技术分析需要结构化时序数据处理（OHLCV DataFrame）和多周期重采样（日→周→月），这是引入 pandas 的核心驱动因素。

## Goals / Non-Goals

**Goals:**
- 统一获取约 1 年历史 OHLCV 数据，覆盖美股/A股/港股/加密货币
- 计算 10 组常用技术指标，支持日/周/月三周期
- 自动生成多空信号和综合评分
- 输出 Markdown 报告，可供策略分析引用

**Non-Goals:**
- 不做可视化图表
- 不做回测功能
- 不做自动交易信号
- 不新增独立 skill

## Decisions

### D1: 使用 pandas + pandas-ta 计算指标

**选择**: pandas（数据处理）+ pandas-ta（指标计算）

**替代方案**:
- `ta` 库：更轻量但指标覆盖面较窄（~40 个）
- 纯 Python 手写：零依赖但计算量大、维护成本高、准确性难保证

**理由**: pandas-ta 覆盖 130+ 指标，纯 Python 无 C 编译依赖，与 pandas DataFrame 原生集成。pandas 的 `resample()` 可一行完成多周期转换。两个库都是成熟的社区项目。

### D2: 历史数据统一路由策略

**选择**: 所有 ticker 的历史数据走 Yahoo 或 Tushare，Finnhub 不参与历史数据获取。

**理由**: Finnhub 只提供实时报价，无历史 K 线 API。Yahoo 免费覆盖美股/港股/加密货币，Tushare 覆盖 A 股。复用现有 `router.classify()` 逻辑，A股→Tushare，其他→Yahoo。

### D3: 多周期通过 resample 实现

**选择**: 获取日线数据后，用 pandas resample 转换为周线和月线。

**替代方案**: 分别调用 API 获取不同周期数据。

**理由**: 减少 API 调用次数，数据一致性更好。1 年日线数据（~250 根 K 线）resample 后周线 ~52 根、月线 ~12 根，足够计算指标。

### D4: 报告格式为 Markdown

**选择**: 纯 Markdown 表格 + 文字，无图表。

**理由**: 与 YMOS 现有报告格式一致（市场洞察、投资雷达都是 Markdown），无需引入可视化库，且 Markdown 报告可直接被 AI agent 读取和引用。

### D5: 策略集成方式

**选择**: 在 P5/P6 prompt 中增加引用指引，策略执行前自动检查技术面报告是否存在。

**替代方案**: 新增独立 skill 或在 SOP 中增加步骤。

**理由**: 技术分析是策略分析的辅助输入，不值得独立成 skill。在 prompt 中加引用指引最小化改动，不破坏现有 SOP 流程。

## Risks / Trade-offs

- **[pandas 依赖体积]** pandas 安装包约 30MB，会增加项目依赖体积 → 可接受，pandas 是 Python 数据处理标准库，用户机器大概率已安装
- **[Yahoo API 限流]** Yahoo Finance 非官方 API，高频请求可能被限流 → 单次 tech-analysis 最多请求几十个 ticker，风险可控；已有 retry 机制
- **[Tushare 历史数据权限]** Tushare 部分历史数据需要积分 → 已有 fallback 到 Yahoo 的机制；A 股 1 年日线属于基础数据，通常无积分要求
- **[pandas-ta 维护状态]** pandas-ta 最后一次 major release 是 2023 年 → 库功能成熟稳定，当前需求范围内的指标计算不受影响；如后续有问题可切换到 ta 库
