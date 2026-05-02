## 1. 基础设施：Ticker 标准化

- [x] 1.1 创建 `cli/core/ticker_normalize.py`，实现 YMOS ticker → Futu OpenD 格式转换（`0700.HK` → `HK.00700`、`AAPL` → `US.AAPL`、`688008.SS` → `SH.688008`、`000001.SZ` → `SZ.000001`）— 已存在于 `cli/core/futu_utils.py`
- [x] 1.2 编写 ticker_normalize 单元测试，覆盖 HK/US/SS/SZ 四种市场和边界情况

## 2. 技术面异动检测

- [x] 2.1 创建 `cli/core/sources/technical_anomaly.py`，封装 Futu OpenD `get_technical_unusual` API 调用，支持全扫和指定指标子集
- [x] 2.2 创建 `cli/commands/technical_anomaly.py`，实现 `ymos fetch-technical-anomaly --ticker/--from-state/--indicators/--time-range` 命令
- [x] 2.3 在 `cli/main.py` 注册新命令 `fetch-technical-anomaly`
- [x] 2.4 实现标准化 JSON 输出 schema（ticker, time_range, anomalies 数组含 date/indicator/signal_direction/description）
- [x] 2.5 编写 technical_anomaly 单元测试（mock OpenD 响应）

## 3. 衍生品异动检测

- [x] 3.1 创建 `cli/core/sources/derivatives_anomaly.py`，封装 Futu OpenD `get_derivative_unusual` API 调用，支持全扫和指定维度子集
- [x] 3.2 创建 `cli/commands/derivatives_anomaly.py`，实现 `ymos fetch-derivatives-anomaly --ticker/--from-state/--dimensions/--time-range` 命令
- [x] 3.3 在 `cli/main.py` 注册新命令 `fetch-derivatives-anomaly`
- [x] 3.4 实现 HK 股票包含牛熊证维度、非 HK 股票自动跳过牛熊证的逻辑
- [x] 3.5 实现标准化 JSON 输出 schema（ticker, market, time_range, anomalies 按 dimension 分组）
- [x] 3.6 编写 derivatives_anomaly 单元测试（mock OpenD 响应，含 HK 和非 HK 场景）

## 4. 资金异动增强

- [x] 4.1 扩展 `cli/core/sources/futu.py`（或对应的资金流数据源），增加 `analysis_dimensions` 参数支持（funds_distribution, funds_broker, funds_flow, short_sell_number, short_sell_ratio）
- [x] 4.2 更新 `cli/commands/capital_flow.py`，增加 `--dimensions` 可选参数，默认全扫
- [x] 4.3 实现卖空数量/比例异动检测逻辑（日环比变化率、历史均值比较、同步异动标记）
- [x] 4.4 实现经纪商异动追踪逻辑（排名变化检测、跨境资金流向识别）
- [x] 4.5 更新资金流 JSON 输出 schema，增加 short_sell_anomaly 和 broker_anomaly 字段
- [x] 4.6 编写资金异动增强的单元测试

## 5. 情绪分析增强

- [x] 5.1 更新 `cli/core/sources/sentiment.py`（或对应数据源），增加多符号 group 聚合计算逻辑
- [x] 5.2 实现标准化 JSON 输出契约（request, generated_at, mode, group, symbols, top_opinions, signals）
- [x] 5.3 实现 empty-result fallback 机制（单个 ticker 无数据时标记 empty 不中断批量）
- [x] 5.4 实现 mixed group label 判定逻辑（bull/bear 差值 < 15% 且均 >= 25%）
- [x] 5.5 更新 `skills/ymos-sentiment/prompts/p19-comment-sentiment.md`，支持 group 聚合输出格式
- [x] 5.6 编写情绪分析增强的单元测试

## 6. 投资雷达集成

- [x] 6.1 更新 `skills/ymos-radar/sop.md`，在资金流扫描后增加技术面异动和衍生品异动扫描步骤（含报告模板更新）
- [x] 6.2 创建 P21（技术面异动分析）和 P22（衍生品异动分析）prompt，增加分析指引
- [x] 6.3 实现 OpenD 不可达时的优雅降级（source 层 graceful error + SOP 集成标注）
- [ ] 6.4 端到端验证：运行完整雷达流程，确认报告包含四维信号（价格+资金+技术+衍生品）— 需要 OpenD 运行环境
