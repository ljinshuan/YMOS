# P-option: 期权市场情绪分析


## 路径上下文（YMOS）
- 根目录：`YMOS/`
- 主数据目录：`data/stocks/`
- 读取：`data/reports/radar/raw/option_chain_YYYYMMDD.json`
- 输出：期权情绪分析摘要

## 适用场景

分析标的期权链数据，提取市场情绪信号、隐含波动率水平、Put/Call Ratio (PCR) 偏斜、未平仓变化趋势。用于投资雷达和策略分析中的期权情绪确认/风险提示。

> **期权情绪铁律**
> - **PCR < 0.7**：看涨期权溢价收窄，市场情绪偏乐观
> - **PCR > 1.5**：看跌期权持仓集中，市场避险需求上升
> - **IV 高位（80%分位以上）**：期权价格反映高波动预期，可能存在过度定价
> - **IV 低位（30%分位以下）**：期权价格反映低波动预期，可能存在价值机会

---

## 提示词模板

```
# Role
我是一名独立科技投资者。我已经获取了标的 **[{{ticker}}** 的期权链数据。
你的任务是协助我分析期权市场的情绪状态，提取关键信号。

---

# Input Data Format

期权链数据 JSON 包含：
```json
{
  "ticker": "AAPL",
  "market": "US",
  "fetched_at": "2026-05-08T10:00:00Z",
  "expiry_dates": [
    {"strike_time": "2026-05-08", "option_expiry_date_distance": 1, "expiration_cycle": "WEEK"},
    ...
  ],
  "contracts": [
    {
      "code": "US.AAPL260508C150000",
      "option_type": "CALL",
      "strike_price": 150.0,
      "strike_time": "2026-05-08",
      "last_price": 10.5,
      "ask_price": 10.8,
      "bid_price": 10.2,
      "implied_volatility": 25.5,
      "delta": 0.52,
      "gamma": 0.08,
      "vega": 0.15,
      "theta": -0.05,
      "rho": 0.02,
      "open_interest": 15000,
      "volume": 5000
    },
    ...
  ],
  "derived_metrics": {
    "put_call_ratio_oi": 0.85,
    "put_call_ratio_vol": 0.72,
    "iv_stats": {
      "min": 15.0,
      "max": 45.0,
      "median": 28.0,
      "count": 365
    }
  }
}
```

---

# Analysis Framework

## 维度 A: Put/Call Ratio (PCR) 分析

* **OI-based PCR**:
  * {{derived_metrics.put_call_ratio_oi}}
  * < 0.7：Call 持仓占优 → 情绪偏乐观
  * 0.7 ~ 1.3：相对平衡 → 情绪中性
  * > 1.5：Put 持仓集中 → 避险需求上升
* **Volume-based PCR**:
  * {{derived_metrics.put_call_ratio_vol}}
  * 与 OI PCR 对比，判断短期 vs 中长期情绪
* **斜率分析**:
  * 观察不同到期日 PCR 的变化趋势（近月 vs 远月）

## 维度 B: 隐含波动率 (IV) 分析

* **IV 水平判断**:
  * 当前 IV 中位数：{{derived_metrics.iv_stats.median}}%
  * IV 区间：{{derived_metrics.iv_stats.min}}% ~ {{derived_metrics.iv_stats.max}}%
* **IV 分位评估**:
  * 需要历史数据对比，如无历史数据则定性分析
  * 高位信号：期权价格反映高波动预期，需警惕过度定价
  * 低位信号：期权价格反映低波动预期，可能存在价值机会
* **IV 曲面分析**:
  * ATM vs OTM IV 是否有显著差异
  * 远月 vs 近月 IV 结构（期限结构）

## 维度 C: 未平仓 (OI) 和成交量分析

* **OI 集中度**:
  * 哪些行权价 OI 最多？（最大 OI 对应的行权价 = "Max Pain"）
  * OI 集中在 OTM Put → 看跌保护需求高
  * OI 集中在 OTM Call → 看涨追涨情绪高
* **OI 变化趋势**:
  * 近月 OI 是增加还是减少？
  * OI 增加 + 价格上涨 → 新多仓入场
  * OI 增加 + 价格下跌 → 新空仓入场
* **大额交易扫描**:
  * 是否有异常高的成交量期权？（量能突增）
  * 大额 Block 交易方向（Call vs Put）

## 维度 D: 希腊值分布分析（可选）

* **Delta 分布**:
  * ATM Delta 是否接近 0.5？
  * 不同行权价的 Delta 曲线是否平滑？
* **Theta 风险**:
  * 近月期权的 Theta 是否明显偏高（时间价值衰减快）？

---

# Output Format

## 期权市场情绪摘要

```
【期权市场情绪】{{ticker}}

### 核心指标
- Put/Call Ratio (OI): {{put_call_ratio_oi}}
- Put/Call Ratio (Vol): {{put_call_ratio_vol}}
- 隐含波动率中位数: {{iv_median}}%
- IV 区间: {{iv_min}}% ~ {{iv_max}}%

### 情绪定性
{{SENTIMENT_SUMMARY}}

* PCR 偏斜：{{PCR_SKEW_ANALYSIS}}
* IV 水平：{{IV_LEVEL_ANALYSIS}}
* OI 趋势：{{OI_TREND_ANALYSIS}}
* 异动信号：{{UNUSUAL_ACTIVITY_ANALYSIS}}

### 风险提示
{{RISK_WARNINGS}}

### 市场观察点
{{MARKET_OBSERVATIONS}}
```

---

# Decision Rules

## 看涨情绪确认（正面信号）
```
满足以下条件时，定性为"看涨情绪确认"：
1. PCR (OI) < 0.7 或 PCR (Vol) < 0.7
2. IV 处于历史低位（如有历史数据）或 IV < 25%
3. ATM Call OI 显著增加（近周 +20%以上）
4. 无大额 Put Block 交易
```

## 看跌情绪确认（风险信号）
```
满足以下条件时，定性为"看跌情绪确认"或"避险需求上升"：
1. PCR (OI) > 1.5 或 PCR (Vol) > 1.5
2. IV 处于历史高位（如有历史数据）或 IV > 40%
3. ATM Put OI 显著增加
4. 有大额 Put Block 交易
```

## 情绪平稳
```
满足以下条件时，定性为"情绪平稳"：
1. PCR 在 0.7 ~ 1.3 区间
2. IV 处于中等水平（25% ~ 40%）
3. OI 变化幅度 < 10%
4. 无明显大额异动交易
```
```
