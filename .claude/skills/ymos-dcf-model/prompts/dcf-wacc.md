# WACC 计算 Prompt

计算 {ticker} 的加权平均资本成本（WACC）。

## 计算步骤

### 1. 权益成本（CAPM）
```
Re = Rf + beta x (Rm - Rf)
```

| 参数 | 值 | 来源 |
|------|-----|------|
| Rf（无风险利率） | {Rf}% | {source} |
| beta（Beta） | {beta} | {source} |
| Rm - Rf（市场风险溢价） | {MRP}% | {source} |
| **Re** | **{Re}%** | **CAPM** |

### 2. 债务成本
```
Rd = 公司债券利率或借款利率
```

### 3. WACC
```
WACC = (E/V x Re) + (D/V x Rd x (1 - Tc))
```

| 参数 | 值 |
|------|-----|
| E（权益市值） | {equity} |
| D（债务账面值） | {debt} |
| V = E + D | {total} |
| E/V | {EV}% |
| D/V | {DV}% |
| **WACC** | **{WACC}%** |

## 注意事项
- Beta 使用行业平均（杠杆 Beta 需先卸杠杆再加杠杆）
- 债务成本使用公司实际利率
- 税率使用公司实际税率（非法定税率）
