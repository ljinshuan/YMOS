# 情景分析 Prompt

基于 DCF 模型，执行三情景分析。

## 情景定义

### 乐观（Bull）
- 收入增长率: {base_g} + 3pp
- EBITDA 利润率: {base_m} + 2pp
- WACC: {base_wacc} - 1pp
- 永续增长率: {base_tg} + 0.5pp
- Exit Multiple: {base_mult} + 2x

### 基准（Base）
- 所有参数使用默认值

### 悲观（Bear）
- 收入增长率: {base_g} - 3pp
- EBITDA 利润率: {base_m} - 2pp
- WACC: {base_wacc} + 1pp
- 永续增长率: {base_tg} - 0.5pp
- Exit Multiple: {base_mult} - 2x

## 结果对比

| 情景 | 收入增长 | 利润率 | WACC | 每股价值 | vs 市价 |
|------|----------|--------|------|----------|---------|
| 乐观 | {hg}% | {hm}% | {lw}% | {bv} | {bv_pct}% |
| 基准 | {bg}% | {bm}% | {bw}% | {base_v} | {base_pct}% |
| 悲观 | {lg}% | {lm}% | {hw}% | {sv} | {sv_pct}% |

## 概率加权

| 情景 | 概率 | 每股价值 | 加权价值 |
|------|------|----------|----------|
| 乐观 | 25% | {bv} | {bv_25} |
| 基准 | 50% | {base_v} | {base_50} |
| 悲观 | 25% | {sv} | {sv_25} |
| **加权估值** | | | **{weighted}** |

## 投资含义（非投资建议）
- 当前市价位于估值范围的 {percentile} 分位
- 安全边际: {margin_of_safety}%
