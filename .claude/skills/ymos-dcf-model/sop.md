# DCF 估值模型 SOP

> 暗号：`DCF 分析` / `估值建模` / `算一下 DCF`
> 模块：ymos-dcf-model（DCF 深度估值模型）

---

## 一句话定位

DCF 模型是**估值层**：通过现金流折现方法，量化估算企业内在价值。

- 研究是「定性理解」，DCF 是「定量估值」
- DCF 输出仅供参考，不构成投资建议

---

## 触发暗号

| 暗号 | 操作 |
|:---|:---|
| `DCF 分析 [ticker]` | 完整 DCF 建模流程 |
| `估值建模 [ticker]` | 同上 |
| `算一下 DCF [ticker]` | 快速 DCF 估算 |

---

## 完整执行步骤

### Step 1：收集假设数据

**从数据源获取：**
- 近 3-5 年收入、EBITDA、EBIT
- 近 3-5 年折旧摊销、资本支出
- 近 3-5 年营运资本变化
- 当前市值、债务、现金

**用户输入/确认：**
- 收入增长率预测（逐年或平均）
- EBITDA/EBIT 利润率预测
- 资本支出占收入比例
- 折旧占资本支出比例

**默认参数：**
- 无风险利率 (Rf): 3%（10 年期国债）
- 市场风险溢价 (Rm - Rf): 6%
- Beta: 行业平均
- 永续增长率 (g): 2.5%
- 企业所得税率: 25%
- 预测期: 5 年

### Step 2：构建现金流预测

使用 prompts/dcf-cash-flow.md prompt。

**5 年预测表格：**

| 年份 | 收入 | 增长率 | EBITDA | EBITDA% | D&A | EBIT | EBIT% | CapEx | NWC变化 | FCF |
|------|------|--------|--------|---------|-----|------|-------|-------|---------|-----|
| Y1 | ... | ...% | ... | ...% | ... | ... | ...% | ... | ... | ... |
| Y2 | ... | ...% | ... | ...% | ... | ... | ...% | ... | ... | ... |
| Y3 | ... | ...% | ... | ...% | ... | ... | ...% | ... | ... | ... |
| Y4 | ... | ...% | ... | ...% | ... | ... | ...% | ... | ... | ... |
| Y5 | ... | ...% | ... | ...% | ... | ... | ...% | ... | ... | ... |

**FCF = EBIT x (1 - Tax) + D&A - CapEx - DeltaNWC**

### Step 3：计算 WACC

使用 prompts/dcf-wacc.md prompt。

```
WACC = (E/V x Re) + (D/V x Rd x (1 - Tc))

Re = Rf + beta x (Rm - Rf)
```

| 参数 | 值 | 来源 |
|------|-----|------|
| 无风险利率 | {Rf}% | 10 年期国债 |
| Beta | {beta} | 行业平均 |
| 市场风险溢价 | {MRP}% | 历史平均 |
| 权益成本 (Re) | {Re}% | CAPM |
| 债务成本 (Rd) | {Rd}% | 公司债券利率 |
| 权益占比 (E/V) | {EV}% | 市值结构 |
| 债务占比 (D/V) | {DV}% | 市值结构 |
| **WACC** | **{WACC}%** | **计算结果** |

### Step 4：计算终值

使用 prompts/dcf-terminal-value.md prompt。

**方法 1：永续增长法**
```
TV = FCF_5 x (1 + g) / (WACC - g)
```

**方法 2：退出倍数法**
```
TV = EBITDA_5 x Exit Multiple
```

两种方法取平均或用户选择。

### Step 5：计算现值

```
企业价值 = Sum(FCF_t / (1 + WACC)^t) + TV / (1 + WACC)^5
股权价值 = 企业价值 - 净债务
每股价值 = 股权价值 / 总股本
```

### Step 6：敏感性分析

使用 prompts/dcf-sensitivity.md prompt。

**WACC vs 永续增长率：**

| WACC \ g | 1.0% | 1.5% | 2.0% | 2.5% | 3.0% |
|----------|------|------|------|------|------|
| 7% | ... | ... | ... | ... | ... |
| 8% | ... | ... | ... | ... | ... |
| 9% | ... | ... | ... | ... | ... |
| 10% | ... | ... | ... | ... | ... |
| 11% | ... | ... | ... | ... | ... |

**收入增长 vs EBITDA 利润率：**

| Growth \ Margin | {m1}% | {m2}% | {m3}% |
|-----------------|-------|-------|-------|
| {g1}% | ... | ... | ... |
| {g2}% | ... | ... | ... |
| {g3}% | ... | ... | ... |

### Step 7：情景分析

使用 prompts/dcf-scenarios.md prompt。

| 情景 | 收入增长 | 利润率 | WACC | 永续增长率 | 每股价值 |
|------|----------|--------|------|------------|----------|
| 乐观 | {high_g}% | {high_m}% | {low_wacc}% | {high_tg}% | {bull_value} |
| 基准 | {base_g}% | {base_m}% | {base_wacc}% | {base_tg}% | {base_value} |
| 悲观 | {low_g}% | {low_m}% | {high_wacc}% | {low_tg}% | {bear_value} |

**概率加权估值：**
- 乐观概率: 25% -> {bull_value}
- 基准概率: 50% -> {base_value}
- 悲观概率: 25% -> {bear_value}
- **加权估值**: {weighted_value}

### Step 8：生成报告

使用模板生成 Markdown 报告。
同时生成 Excel 模型（7 个 Sheet）。

---

## 产出物清单

| 文件 | 路径 | 说明 |
|:---|:---|:---|
| DCF 报告 | `data/reports/valuation/{ticker}/DCF分析_{ticker}_{date}.md` | Markdown 分析报告 |
| Excel 模型 | `data/reports/valuation/{ticker}/excel/DCF模型_{ticker}_{date}.xlsx` | 可交互 Excel 模型 |

---

## 路径速查

| 内容 | 路径 |
|:---|:---|
| Prompts | `skills/ymos-dcf-model/prompts/` |
| 报告模板 | `skills/ymos-dcf-model/templates/dcf-report.md` |
| Excel 模板 | `skills/ymos-dcf-model/templates/dcf-excel.json` |
| 个股知识库 | `data/stocks/{ticker}/个股基础知识库.md` |
| 路由表 | `skills/ymos-core/routing.md` |

---

## 边界与反模式

**DCF 模型不做**：
- 不提供实时估值更新
- 不实现行业特定变体（银行、地产等）
- 不替代专业金融模型
- 不构成投资建议

**反模式**：
- 过度依赖终值（终值占比 > 80% 需警惕）
- 使用过于乐观的假设
- 忽略敏感性分析的结果范围
- 只看基准情景不看极端情景

---

*SOP 版本：2026-05-08 · YMOS V4 Skills 架构*
