# 终值计算 Prompt

计算 {ticker} 的终值（Terminal Value）。

## 方法 1：永续增长法（Gordon Growth Model）
```
TV = FCF_n x (1 + g) / (WACC - g)
```

| 参数 | 值 |
|------|-----|
| FCF_n（最后一年 FCF） | {fcf} |
| g（永续增长率） | {g}% |
| WACC | {wacc}% |
| **TV** | **{tv}** |

## 方法 2：退出倍数法
```
TV = EBITDA_n x Exit Multiple
```

| 参数 | 值 |
|------|-----|
| EBITDA_n（最后一年 EBITDA） | {ebitda} |
| Exit Multiple | {multiple}x |
| **TV** | **{tv}** |

## 对比分析
- 永续增长法 TV: {tv1}
- 退出倍数法 TV: {tv2}
- 平均 TV: {avg_tv}
- 终值占总估值比例: {tv_pct}%

**注意**: 终值占比 > 80% 时需特别关注假设合理性。
