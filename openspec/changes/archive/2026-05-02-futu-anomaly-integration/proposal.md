## Why

YMOS 投资雷达目前覆盖「价格 + 资金流」两个信号维度，但缺少技术面和衍生品维度的异动检测。Futu OpenD 提供了 6 个成熟的异动检测 skill（技术面 14 种指标、衍生品期权/牛熊证、资金异动多维检测），当前未被 YMOS 吸收。同时，现有情绪分析和资金流扫描可以参考 Futu skill 的标准化输出、多符号聚合、empty fallback 等模式进行增强。

## What Changes

- **新增技术面异动检测能力**：通过 Futu OpenD `get_technical_unusual` 接口，对个股进行 K 线形态识别 + 14 种技术指标（MACD/RSI/KDJ/CCI/BOLL/MA 等）异常检测，按时间窗口输出异常信号
- **新增衍生品异动检测能力**：通过 Futu OpenD `get_derivative_unusual` 接口，检测牛熊证街货比例/价格区间异动（港股）、期权大单/IV/PCR/量价/情绪/综合信号异动
- **增强资金异动检测**：现有 capital-flow-anomaly 仅做资金流扫描 + P20 分析，增加卖空数量/比例异动、买卖经纪商追踪维度
- **增强情绪分析**：参考 Futu comment-sentiment skill 的多符号 group 聚合模式、标准化 JSON 输出契约、empty-result fallback 机制，升级现有 comment-sentiment 能力

## Capabilities

### New Capabilities
- `technical-anomaly`: 技术面异动检测 — K 线形态 + 14 种技术指标异常扫描，支持全扫和指定指标子集
- `derivatives-anomaly`: 衍生品异动检测 — 牛熊证街货/期权大单/IV/PCR/量价/情绪/综合信号七维异动检测

### Modified Capabilities
- `capital-flow-anomaly`: 增加卖空数量/比例异动、买卖经纪商追踪两个检测维度
- `comment-sentiment`: 增加多符号 group 聚合模式、标准化 JSON 输出契约、empty-result fallback

## Impact

- **CLI 层**：新增 `ymos fetch-technical-anomaly` 和 `ymos fetch-derivatives-anomaly` 命令；`ymos fetch-capital-flow` 增加卖空/经纪商参数
- **数据源**：三个异动检测均依赖 Futu OpenD（localhost:11111），需要 OpenD 运行才能使用
- **Skill 层**：ymos-radar 的资金流扫描步骤将集成技术面和衍生品信号；ymos-sentiment 输出格式升级
- **报告层**：投资雷达报告新增「技术面信号」和「衍生品信号」section
- **依赖**：无新外部 Python 依赖（使用现有的 futu-api 或 OpenD HTTP 接口）
