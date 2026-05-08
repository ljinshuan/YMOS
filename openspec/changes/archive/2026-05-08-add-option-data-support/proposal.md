## Why

目前 YMOS 已通过富途 OpenD 获取衍生品异常数据（`get_derivative_unusual`），但该 API 仅返回异常信号，缺少完整的期权链信息（行权价分布、隐含波动率曲面、希腊值、未平仓变化等）。完整的期权数据能提供更精细的市场情绪和风险偏好信号，对高阶交易决策至关重要。

## What Changes

- **新增期权链数据获取 CLI 命令**：`ymos fetch-option-chain --ticker TICKER`，使用富途 OpenD 的 `get_option_chain` + `get_market_snapshot` 获取完整的期权链静态和实时数据
- **新增期权数据源模块**：`cli/core/sources/option_chain.py`，封装期权链获取逻辑
- **投资雷达集成期权分析**：在桥接报告中新增「期权市场情绪」可选 section，展示 IV 曲面、PCR、未平仓变化
- **策略分析集成期权信号**：P12 (Referee) 分析时将期权 Put/Call Ratio、IV 高低、大额期权交易作为可选的确认/风险信号
- **期权数据存储**：原始数据存储至 `data/reports/radar/raw/option_chain_YYYYMMDD.json`

## Capabilities

### New Capabilities
- `option-chain-data`: 期权链数据获取与处理能力，包括期权链列表、实时报价、希腊值、隐含波动率等

### Modified Capabilities
- `skill-ymos-radar`: 雷达报告新增期权市场情绪分析 section（可选）
- `skill-ymos-strategy`: P12 分析新增期权信号作为确认/风险因素（可选）
- `derivatives-anomaly`: 现有能力保持不变，新增完整的期权链数据作为补充

## Impact

- **新增代码**：`cli/core/sources/option_chain.py`、`cli/commands/option_chain.py`、新增 prompts 用于期权分析
- **修改代码**：`ymos-radar` skill 新增可选期权分析流程；`ymos-strategy` skill P12 prompt 新增期权信号处理
- **新增依赖**：无（使用现有 `futu-api`）
- **数据存储**：新增 `data/reports/radar/raw/option_chain_*.json` 文件
- **兼容性**：OpenD 不可用时优雅降级，跳过期权分析，不影响现有雷达和策略流程
