# 📡 投资雷达 SOP（桥接报告）

> 暗号：`跑一下投资雷达`
> 模块：ymos-radar（持仓信号追踪与桥接报告）

---

## 一句话定位

投资雷达是市场洞察 → 策略分析的**桥接报告**：**从7天市场趋势 + 价格变化 + 个股事件中，判断下一步该调研什么、该分析什么**

- **市场洞察看全局，投资雷达看持仓**
- 统一承载：策略分析建议 + 调研建议（取代原 status.md + 调研与确认）
- 价格扫描只扫状态机里的 ticker，不做全市场盲扫

---

## 🔑 触发暗号

| 暗号 | 操作 |
|:---|:---|
| `跑一下投资雷达` | 完整流程（7天趋势 + 价格扫描 + 信号追踪 + 生成桥接报告） |
| `查一下价格` | 只跑价格扫描，不生成完整雷达报告 |
| `看看有什么信号` | 只做信号演变扫描，不触发分流 |

---

## ⚙️ 完整执行步骤

### Step 1：加载用户上下文

按顺序读取以下文件：

```
data/state/preferences.md
data/state/holdings.md
data/state/watchlist.md
```

### Step 2：加载市场洞察（7天趋势分析）⭐ 核心输入

**2.1 当日洞察**

查找路径：`data/reports/market-insight/YYYY-MM/YYYY-MM-DD_市场洞察.md`

- **若当日洞察已存在**：直接读取
- **若当日洞察不存在**：先自动触发「跑一下市场洞察」，再继续

**2.2 过去7天趋势分析**

扫描 `data/reports/market-insight/YYYY-MM/` 下最近 7 个洞察文件，提取：
- **主线演变**：哪些主题连续多日出现？强化还是弱化？
- **信号持续性**：重复信号 = 趋势；单次 = 噪音
- **事件链条**：多个独立事件是否指向同一结论？
- **逻辑验证**：之前洞察中的预判，后续是否被验证？

### Step 3：加载上份投资雷达（连续性基础）

查找最新雷达：`data/reports/radar/YYYY-MM/投资雷达_YYYY-MM-DD.md`

提取用于连续跟踪的信息：
- 上期关注板块和监控点
- 上期建议及执行进展
- 上期持仓监控价位

### Step 3.5：大盘 + 板块 ETF 扫描（三层信号基础）

> 在个股价格扫描之前，先获取大盘和板块 ETF 的量化技术面数据。

**3.5.1 读取配置**

```
data/state/market_anchors.md  → 提取大盘 ETF 列表（如 QQQ, SPY）
data/state/sector_mapping.md  → 提取持仓涉及的板块 ETF 列表（如 SOXX, XLK, KWEB）
```

**3.5.2 大盘 ETF 价格 + 技术面扫描**

```bash
# 价格扫描
ymos price-scan scan --symbols QQQ,SPY \
  --output-dir "data/reports/radar/raw/$(date +%Y-%m)" \
  --date-tag "$(date +%Y%m%d)"

# 技术分析
ymos tech-analysis analyze --symbols QQQ,SPY \
  --source yahoo \
  --output-dir "data/reports/tech/$(date +%Y-%m)"
```

**3.5.3 板块 ETF 价格 + 技术面扫描**

```bash
# 价格扫描（从 sector_mapping 提取不重复的板块 ETF）
ymos price-scan scan --symbols SOXX,XLK,KWEB \
  --output-dir "data/reports/radar/raw/$(date +%Y-%m)" \
  --date-tag "$(date +%Y%m%d)"

# 技术分析
ymos tech-analysis analyze --symbols SOXX,XLK,KWEB \
  --source yahoo \
  --output-dir "data/reports/tech/$(date +%Y-%m)"
```

**3.5.4 三层信号联动判断**

对每个持仓标的，综合大盘→板块→个股三个层级判断顺风/逆风：

| 大盘 verdict | 板块 verdict | 标记 | 含义 |
|:---|:---|:---|:---|
| 偏多 | 偏多 | 🟢 顺风 | 大盘+板块共振看多，个股看多信号权重增加 |
| 偏多 | 偏空 | 🟡 分化 | 大盘与板块矛盾，需关注板块是否有独立利空 |
| 偏空 | 偏多 | 🟡 分化 | 大盘逆风中板块独立走强，需确认逻辑硬度 |
| 偏空 | 偏空 | 🔴 逆风 | 大盘+板块共振看空，个股看多需极强逻辑支撑 |
| 中性 | 任意 | ⚪ 中性 | 大盘方向不明，以板块+个股信号为主 |

**3.5.5 P14 板块猎手自动触发**

当板块 ETF 技术分析 verdict 为「偏多⬆」或「偏空⬇」时，自动触发 P14 板块猎手对该板块做深度分析：

- **板块偏多**：触发 P14，输出该板块的龙头标的、资金反馈、逻辑复盘
- **板块偏空**：触发 P14，输出风险点、逻辑松动证据
- **板块中性**：跳过 P14，仅保留技术面数据在报告中

P14 prompt 路径：`skills/ymos-market-insight/prompts/p14-sector-hunter.md`

### Step 4：价格扫描

**只扫持仓 + Watchlist，不做全市场盲扫**

```bash
mkdir -p "data/reports/radar/raw/$(date +%Y-%m)" \
         "data/reports/radar/$(date +%Y-%m)"

ymos price-scan scan --from-state \
  --output-dir "data/reports/radar/raw/$(date +%Y-%m)" \
  --date-tag "$(date +%Y%m%d)"
```

> **价格路由规则（三源分流）**：
> | 市场 | 数据源 | 条件 |
> |:---|:---|:---|
> | 美股 / Crypto | Finnhub | 有 `FINNHUB_API_KEY` |
> | A股（.SS / .SZ） | Tushare | 有 `TUSHARE_TOKEN` |
> | 港股（.HK） | Yahoo Finance | 免费 |
> | 兜底（无 Key） | Yahoo Finance | 所有市场回退 |

### Step 4.5：资金流扫描

**只扫持仓 + Watchlist，复用价格扫描的 ticker 列表**

```bash
ymos fetch-capital-flow fetch --from-state \
  --output-dir "data/reports/radar/raw/$(date +%Y-%m)"
```

> **数据源**：富途 OpenD `get_financial_unusual` API
> **前置条件**：本地需运行 Futu OpenD 客户端（localhost:11111）
> **覆盖范围**：资金分布（主力/散户）、经纪商买卖活动、资金流趋势（多日）、卖空量与比率
> **可选过滤**：`--dimensions funds_distribution funds_broker short_sell_number short_sell_ratio`

**P20 资金异动分析**：

对每个标的的资金流数据，使用 P20 prompt 进行异动信号检测：
```
skills/ymos-radar/prompts/p20-capital-anomaly.md
```

P20 输出包含：
- 三维度异动信号（资金分布 / 资金流向 / 卖空情况）
- 信号强度评级（strong / moderate / weak）
- Tier 评级调整建议
- P4 重点关注点更新建议

> **资金流不可用时**：跳过此步骤（非阻塞），在报告中标注「资金流数据缺失」。

### Step 4.6：技术面异动扫描

**只扫持仓 + Watchlist，复用 ticker 列表**

```bash
ymos fetch-technical-anomaly fetch --from-state \
  --output-dir "data/reports/radar/raw/$(date +%Y-%m)"
```

> **数据源**：富途 OpenD `get_technical_unusual` API
> **前置条件**：本地需运行 Futu OpenD 客户端（localhost:11111）
> **覆盖范围**：K 线形态识别 + 14 种技术指标异常（MACD / RSI / KDJ / CCI / BOLL / MA 等）
> **可选过滤**：`--indicators MACD RSI6 RSI12 RSI24`

输出每个标的的技术面异常信号，包含：日期、指标名称、信号方向、支撑/压力位。

> **技术面数据不可用时**：跳过此步骤（非阻塞），在报告中标注「技术面数据不可用（OpenD 未连接）」。

### Step 4.7：衍生品异动扫描

**只扫持仓 + Watchlist，复用 ticker 列表**

```bash
ymos fetch-derivatives-anomaly fetch --from-state \
  --output-dir "data/reports/radar/raw/$(date +%Y-%m)"
```

> **数据源**：富途 OpenD `get_derivative_unusual` API
> **前置条件**：本地需运行 Futu OpenD 客户端（localhost:11111）
> **覆盖范围**：
> - 港股：牛熊证街货比例/价格区间异动 + 期权五维信号（大单/波动率/量价/情绪/综合）
> - 非港股：仅期权五维信号（牛熊证维度自动跳过）
> **可选过滤**：`--dimensions option_unusual option_volatility option_sentiment`

输出每个标的的衍生品异常信号，按维度分组。

> **衍生品数据不可用时**：跳过此步骤（非阻塞），在报告中标注「衍生品数据不可用（OpenD 未连接）」。

### Step 4.8：期权市场情绪扫描（可选）

> ⚠️ **前置条件**：用户显式启用或设置了期权分析偏好
> **数据源**：富途 OpenD `get_option_chain` + `get_market_snapshot` API

**4.8.1 读取配置**

检查用户是否启用期权分析：
- `data/state/preferences.md` 中的 `option_analysis_enabled` 字段
- 或 CLI 参数 `--with-options`

**4.8.2 获取期权链数据**

```bash
ymos fetch-option-chain fetch --from-state \
  --output-dir "data/reports/radar/raw/$(date +%Y-%m)"
```

**数据范围**：
- 获取所有到期的期权合约
- 包含：静态数据（行权价、到期日、类型）+ 动态数据（价格、IV、希腊值、未平仓）
- 派生指标：PCR、IV 分位数、OI 变化

**4.8.3 期权情绪分析**

调用 `P-option-sentiment` prompt 对每个标的的期权链数据进行分析，生成情绪摘要。

> **期权数据不可用时**：跳过此步骤（非阻塞），在报告中标注「期权数据不可用（OpenD 未连接）」。

### Step 5：综合分析

> 详细分析流程见 `sop/analysis-and-triggers.md`

综合 Step 1-4.7 所有输入 + **Step 3.5 三层信号联动判断**，执行信号分析和分流。

**三层信号联动在综合分析中的应用**：
- 逆风标记的标的，看多信号需要更强的逻辑支撑
- 顺风标记的标的，利空信号需要更审慎的评估
- 分化标记的标的，需在报告中明确矛盾点

### Step 6：触发分流（AI 自主分析）

> 详细触发规则和分析链见 `sop/analysis-and-triggers.md`

### Step 7：生成投资雷达报告

> 完整报告模板见 `sop/report-template.md`

**输出路径**：`data/reports/radar/YYYY-MM/投资雷达_YYYY-MM-DD.md`
**命名规则**：`投资雷达_YYYY-MM-DD.md`（同一天重跑覆盖，不加后缀）

### Step 8：写回状态机

每次完整流程**至少写回**：
1. `data/state/watchlist.md` 或 `持仓_状态机.md`（P4更新、价格更新）
2. 相关标的的 `个股基础知识库.md`（P4 增量更新）

---

## 📦 产出物清单

| 文件 | 路径 | 说明 |
|:---|:---|:---|
| 投资雷达报告 | `data/reports/radar/YYYY-MM/` | 桥接报告（核心产出） |
| 价格扫描（Raw） | `data/reports/radar/raw/YYYY-MM/` | 价格数据（个股 + 大盘/板块 ETF） |
| 资金流扫描（Raw） | `data/reports/radar/raw/YYYY-MM/` | 资金异动数据 |
| 大盘/板块 ETF 技术面 | `data/reports/tech/YYYY-MM/` | ETF 技术分析报告 |
| 更新：状态机 | `data/state/` | P4 + 价格 |
| 更新：单标的知识库 | `data/stocks/{holdings,watchlist}/名称_TICKER/` | P4 增量 |

---

## 📁 路径速查

| 内容 | 路径 |
|:---|:---|
| 价格扫描脚本 | `cli/`（`ymos price-scan`） |
| 价格路由脚本 | `cli/`（`ymos price-scan`） |
| Finnhub 价格 | `cli/`（`ymos price-scan`，自动路由） |
| Yahoo 价格 | `cli/`（`ymos price-scan`，自动路由） |
| Tushare 价格 | `cli/`（`ymos price-scan`，自动路由） |
| 当前策略 | `data/state/preferences.md` |
| 持仓状态机 | `data/state/holdings.md` |
| Watchlist 状态机 | `data/state/watchlist.md` |
| 大盘锚点 | `data/state/market_anchors.md` |
| 板块-个股映射 | `data/state/sector_mapping.md` |
| 市场洞察归档 | `data/reports/market-insight/YYYY-MM/` |
| 投资雷达归档 | `data/reports/radar/YYYY-MM/` |
| P 提示词目录 | `skills/<skill>/prompts/` 或 `skills/ymos-core/prompts/` |

---

## ⚠️ 边界与反模式

**投资雷达不做**：
- 不做市场全景分析（那是市场洞察的事）
- 不做策略制定（那是策略分析的事）
- 不自动执行买卖（Human in the Loop）
- 不给出买/卖/加仓/持有建议（只建议路由暗号）

**反模式**：
- 只跑了分析，不写回状态机
- 跳过 P2 就直接进入 P5/P6
- 把市场洞察当成投资雷达（洞察不看持仓，雷达才看持仓）

---

*SOP 版本：2026-05-03 · YMOS V4 Skills 架构 · 新增大盘+板块三层信号联动*
