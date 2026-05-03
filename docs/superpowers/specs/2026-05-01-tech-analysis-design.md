# YMOS 技术面分析功能设计

**日期**: 2026-05-01
**状态**: 已批准

## 概述

为 YMOS 投资系统增加技术面分析能力。实现方式为独立 CLI 命令 + 策略流程集成，覆盖趋势/动量/波动率/成交量四个维度共 10 组指标，支持日/周/月三周期叠加分析，适用于美股/A股/港股全市场。

## 技术选型

**pandas + pandas-ta**

- pandas: OHLCV 数据处理、多周期 resample（日线→周线→月线）
- pandas-ta: 130+ 技术指标，覆盖全部需求
- 两个库均为纯 Python，无 C 编译依赖，跨平台兼容

## 架构设计

### 新增文件

| 文件 | 职责 |
|------|------|
| `cli/core/sources/history.py` | 统一历史 OHLCV 获取，输出 DataFrame |
| `cli/core/tech.py` | 技术指标计算 + 信号生成 + 综合评分 |
| `cli/commands/tech.py` | CLI 命令入口，报告生成 |

### 修改文件

| 文件 | 改动 |
|------|------|
| `cli/main.py` | 注册 `tech-analysis` 命令 |
| `pyproject.toml` | 添加 pandas、pandas-ta 依赖 |
| `.claude/skills/ymos-strategy/prompts/` | P5/P6 prompt 中增加技术面引用指引 |

## 详细设计

### 1. 数据层：历史 OHLCV 获取 (`cli/core/sources/history.py`)

复用现有 `router.classify()` 判断数据源，所有 ticker 统一输出 pandas DataFrame（列为 open/high/low/close/volume，索引为 DatetimeIndex）。

**路由规则：**

| Ticker 类型 | 数据源 | 获取方式 |
|-------------|--------|----------|
| A 股 (.SS/.SZ) | Tushare | `fetch_daily(start_date=1年前, end_date=今天)` |
| 港股 (.HK) | Yahoo | `fetch_one(period="1y", interval="1d")` |
| 美股 / 加密货币 | Yahoo | `fetch_one(period="1y", interval="1d")` |

美股/加密货币的历史数据统一走 Yahoo（免费且覆盖完整），Finnhub 仅保留实时报价用途。

**关键函数：**

```python
def fetch_history(symbols: list[str], tushare_token: str = "") -> dict[str, pd.DataFrame]
```

返回 `{symbol: DataFrame}` 字典。每个 DataFrame 包含约 250 个交易日数据，足够计算 MA250。

### 2. 计算层：技术指标引擎 (`cli/core/tech.py`)

#### 指标体系

| 维度 | 指标 | 参数 |
|------|------|------|
| 趋势 | MA | 5/10/20/60/120/250 日 |
| 趋势 | MACD | fast=12, slow=26, signal=9 |
| 趋势 | DMI (ADX/+DI/-DI) | period=14 |
| 动量 | RSI | 6 / 14 |
| 动量 | KDJ | 9/3/3 |
| 动量 | Williams %R | period=14 |
| 波动率 | 布林带 | period=20, std=2 |
| 波动率 | ATR | period=14 |
| 成交量 | OBV | — |
| 成交量 | 成交量均线 | 5 / 20 日 |

#### 多周期处理

```python
daily = compute_indicators(df)
weekly = compute_indicators(df.resample('W').agg({'open':'first','high':'max','low':'min','close':'last','volume':'sum'}))
monthly = compute_indicators(df.resample('ME').agg({'open':'first','high':'max','low':'min','close':'last','volume':'sum'}))
```

#### 信号生成

每个指标输出三类信号：`多头` / `空头` / `中性`，附带说明文字。

| 指标 | 多头信号 | 空头信号 |
|------|----------|----------|
| MA | 价格站上均线 / 均线多头排列 | 价格跌破均线 / 均线空头排列 |
| MACD | DIF > DEA（金叉） | DIF < DEA（死叉） |
| RSI | < 30（超卖） | > 70（超买） |
| KDJ | K > D（金叉） | K < D（死叉） |
| 布林带 | 触及下轨反弹 | 触及上轨回落 |
| ADX | > 25 且 +DI > -DI | > 25 且 -DI > +DI |
| Williams %R | < -80（超卖） | > -20（超买） |
| OBV | OBV 上升趋势 | OBV 下降趋势 |
| ATR | 波动率收窄（可能突破） | 波动率放大（风险增加） |

#### 综合评分

`summarize()` 汇总三个周期的信号，按多空数量占比给出综合判断：`偏多 ⬆` / `偏空 ⬇` / `中性 ➡`，并附共振描述。

#### 核心函数签名

```python
def analyze(df: pd.DataFrame) -> dict
    # 返回 {"daily": {...}, "weekly": {...}, "monthly": {...}, "summary": {...}}

def compute_indicators(df: pd.DataFrame) -> pd.DataFrame
    # 在 DataFrame 上追加所有指标列

def generate_signals(indicators_df: pd.DataFrame) -> list[dict]
    # 返回 [{"dimension": "趋势", "name": "MA", "value": "...", "signal": "多头", "note": "..."}]

def summarize(daily_signals, weekly_signals, monthly_signals) -> dict
    # 返回 {"verdict": "偏多 ⬆", "note": "日线/周线共振看多"}
```

### 3. CLI 命令 (`cli/commands/tech.py`)

```bash
# 指定股票
ymos tech-analysis --symbols AAPL,0700.HK,688008.SS

# 从持仓+关注列表读取
ymos tech-analysis --from-state

# 指定输出目录
ymos tech-analysis --symbols AAPL --output-dir data/reports/tech/2026-05
```

默认输出路径：`data/reports/tech/{YYYY-MM}/{TICKER}_技术面分析.md`

同名同日报告覆盖（无 _v2 后缀），遵循 CLAUDE.md 报告命名规则。

### 4. 报告格式

```markdown
# {TICKER} 技术面分析 ({YYYY-MM-DD})

## 综合判断: {偏多 ⬆ / 偏空 ⬇ / 中性 ➡}
{共振描述}

## 日线
| 维度 | 指标 | 当前值 | 信号 |
|------|------|--------|------|
| 趋势 | MA5 / MA20 / MA60 | ... | ... |
| 趋势 | MACD | DIF ... / DEA ... | ... |
| 动量 | RSI(14) | ... | ... |
| ... | ... | ... | ... |

## 周线
(同上结构)

## 月线
(同上结构)

## 关键信号摘要
- (最重要的 3-5 条信号，供策略分析快速引用)
```

### 5. 策略集成

在 `.claude/skills/ymos-strategy/` 的 P5（买点判断）和 P6（持仓评估）prompt 中增加引用指引：

> 执行前检查 `data/reports/tech/{YYYY-MM}/{TICKER}_技术面分析.md` 是否存在。若存在，将综合判断和关键信号摘要作为技术面参考输入。

策略 skill 的 SOP 不需要新增步骤，仅在现有步骤中增加数据源引用。

## 依赖变更

```toml
# pyproject.toml 新增
dependencies = [
    # ... 现有依赖 ...
    "pandas>=2.0",
    "pandas-ta>=0.3.14b",
]
```

## 不做的事

- 不做可视化图表（纯文本报告）
- 不做回测功能
- 不做自动交易信号
- 不新增独立 skill（技术分析作为 CLI 工具 + 策略引用，不独立成 skill）
