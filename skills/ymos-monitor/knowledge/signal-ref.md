# 信号类型参考表

## signal_type（信号类型）

| 值 | 中文 | 含义 |
|----|------|------|
| `buy` | 买入信号 | 策略建议买入/加仓 |
| `sell` | 卖出信号 | 策略建议卖出/减仓 |
| `hold` | 持有信号 | 策略建议继续持有 |
| `warning` | 预警信号 | 需要关注的风险提示 |

## strength（信号强度）

| 值 | 中文 | 含义 |
|----|------|------|
| `strong` | 强 | 高置信度信号，多个指标共振 |
| `medium` | 中 | 中等置信度，需结合其他因素 |
| `weak` | 弱 | 低置信度，仅供参考 |

## 信号文件格式

```json
{
  "ticker": "SOXL",
  "signal_time": "2026-05-03 14:35:00",
  "signal_type": "buy",
  "strength": "strong",
  "strategy_name": "ma_cross",
  "detail": "5日均线上穿20日均线",
  "price_at_signal": 130.42
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `ticker` | string | 是 | YMOS ticker 格式 |
| `signal_time` | string | 是 | 信号产生时间，HH:MM 或完整 datetime |
| `signal_type` | string | 是 | buy/sell/hold/warning |
| `strength` | string | 是 | strong/medium/weak |
| `strategy_name` | string | 是 | 策略名称（用于去重） |
| `detail` | string | 是 | 信号详情描述 |
| `price_at_signal` | number | 是 | 信号触发时的价格 |

### 去重规则

信号按 `signal_time` + `strategy_name` 组合去重。同一时间同一策略的信号只告警一次。
