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

### Step 5：综合分析

> 详细分析流程见 `sop/analysis-and-triggers.md`

综合 Step 1-4.7 所有输入，执行信号分析和分流。

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
| 价格扫描（Raw） | `data/reports/radar/raw/YYYY-MM/` | 价格数据 |
| 资金流扫描（Raw） | `data/reports/radar/raw/YYYY-MM/` | 资金异动数据 |
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

*SOP 版本：2026-04-27 · YMOS V4 Skills 架构*
