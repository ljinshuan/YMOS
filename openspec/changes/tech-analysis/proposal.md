## Why

YMOS 当前策略分析完全依赖基本面+消息面，缺少技术面维度。用户在进行 P5 买点判断和 P6 持仓评估时，无法参考趋势、动量、波动率等技术指标，决策依据不完整。需要增加技术面分析能力，覆盖美股/A股/港股全市场，支持多周期叠加。

## What Changes

- 新增历史 OHLCV 数据获取模块，从 Yahoo/Tushare 统一获取约 1 年日线数据，输出 pandas DataFrame
- 新增技术指标计算引擎，基于 pandas-ta 实现 10 组常用指标（MA/MACD/DMI/RSI/KDJ/Williams %R/布林带/ATR/OBV/成交量均线）
- 支持日/周/月三周期叠加分析，自动生成多空信号和综合评分
- 新增 `ymos tech-analysis` CLI 命令，输出 Markdown 格式技术面报告
- 策略 skill（P5/P6）增加技术面报告引用

## Capabilities

### New Capabilities
- `history-fetch`: 统一历史 OHLCV 数据获取，复用现有 router 路由逻辑，输出标准 DataFrame
- `tech-indicators`: 技术指标计算、多周期处理、信号生成和综合评分
- `tech-analysis-cli`: CLI 命令入口，报告生成和输出

### Modified Capabilities

（无现有 capability 需修改——策略 prompt 的技术面引用属于 prompt 内容调整，不涉及 spec 层面变更）

## Impact

- **依赖**: 新增 pandas>=2.0、pandas-ta>=0.3.14b（pyproject.toml）
- **代码**: 新增 3 个文件（`cli/core/sources/history.py`、`cli/core/tech.py`、`cli/commands/tech.py`），修改 2 个文件（`cli/main.py`、`pyproject.toml`）
- **数据**: 新增 `data/reports/tech/{YYYY-MM}/` 报告目录
- **策略**: P5/P6 prompt 增加技术面报告引用指引
