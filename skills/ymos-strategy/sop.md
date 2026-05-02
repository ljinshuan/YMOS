# 🎯 策略分析 SOP

> 暗号：`我想买 [ticker]` / `我想卖 [ticker]` / `做个仓位再平衡` / `跑一下策略分析`
> 模块：ymos-strategy（投资策略分析与路由分发）

---

## 一句话定位

策略分析专注回答一件事：**基于分析结论和当前仓位，现在应该做什么动作，怎么做**

- 策略分析是下游模块，依赖投资雷达（ymos-radar）的输出作为触发
- 它本身不做信息收集，也不做市场洞察
- 核心原则：**能跑的先跑完，不阻塞**

---

## 🔑 触发暗号

| 暗号 | 动作意图 | 跳转路由 |
|:---|:---|:---|
| `我想买 [ticker]` | 首次建仓 | → 路由 A：买入 |
| `加仓 [ticker]` | 已有仓位再加 | → 路由 B：加仓 |
| `我想卖 [ticker]` | 减仓/清仓 | → 路由 D：卖出 |
| `持有怎么看 [ticker]` | 持有评估 | → 路由 C：持有 |
| `做个仓位再平衡` | 组合级调整 | → 路由 E：再平衡 |
| `跑一下策略分析` | 定时/手动批量 | → 自动模式（读雷达 → 分流） |

---

## ⚙️ 完整执行步骤

### Step 1：确定触发来源与目标

**1.1 手动暗号触发**（`我想买/卖/加仓/持有怎么看`）：
- 目标标的 = 用户指定的 ticker
- 动作意图 = 暗号直接指定
- 跳到 Step 3

**1.2 定时任务/自动触发**（`跑一下策略分析`）：
- 读取最新投资雷达报告：`data/reports/radar/YYYY-MM/投资雷达_YYYY-MM-DD.md`
  - 若今日无雷达 → 查找最近一份
- 提取雷达报告中 `## 🔭 下一步建议 > 策略分析建议` 区块
- 从中筛选需要策略分析的标的和动作意图

**1.3 消费调研建议（1.2 同时执行）**：
- 同样从投资雷达报告中提取 `## 🔭 下一步建议 > 调研建议` 区块
- 对每个「建议跑 调研一下 TICKER」的标的：
  - 调用 `skills/ymos-research/sop.md` 执行 P1+P4+P2 补全
  - 完成后记录到策略分析日志的「本次自动调研」section
- 若无调研建议 → 跳过
- **先完成 1.3 调研，再进入 Step 2**（确保后续策略路由有完整的个股上下文）

> 为什么在策略分析里消费调研建议？调研完成后 P1/P4 补全，后续策略路由可直接使用完整上下文，不需要用户手动 `调研一下`。

**1.2 + 1.3 均无建议时** → 输出「雷达无策略分析建议，本次跳过」→ 退出

### Step 2：加载用户上下文

按顺序读取：

```
data/state/preferences.md          ← 必须存在，否则阻塞
data/state/holdings.md
data/state/watchlist.md
```

> ⛔ 如果 `当前关注方向与投资偏好.md` 不存在或为空 → 停止，输出：
> 「前置条件不足：缺少当前关注方向与投资偏好。请先填写（路径：data/state/preferences.md）」

### Step 3：逐标的前置检查与补足

对每个目标标的执行以下检查：

| # | 检查项 | 文件路径 | 若缺失 |
|:---|:---|:---|:---|
| ① | 个股基础知识库 | `data/stocks/{holdings,watchlist}/名称_TICKER/个股基础知识库.md` | **调用 skills/ymos-research/sop.md 补足** → 继续 |
| ② | P1 基石档案 | 知识库内 `## P1 基石档案` 区块 | **调用初始调研补足** → 继续 |
| ③ | P4 重点关注点 | 知识库内 `## P4 重点关注点` 区块 | **调用初始调研补足** → 继续 |
| ④ | P2 阶段判断 | 知识库内 `## P2 阶段判断` 区块 | **AI 自动执行 P2** → 继续 |
| ⑤ | 买入卖出备忘录 | `data/stocks/{holdings,watchlist}/名称_TICKER/买入卖出备忘录.md` | **不阻塞**，分析完后提示补充 |
| ⑥ | 当前关注方向与投资偏好 | `data/state/preferences.md` | ⛔ 阻塞（Step 2 已检查） |

**不阻塞原则**：
- ①②③ 缺失 → 调用初始调研子模块补足后继续
- ④ 缺失 → AI 自动执行 P2
- ⑤ 缺失 → 继续执行，报告末尾标注「优化建议」
- 只有 ⑥ 缺失才阻塞

**个股上下文范围**：读取该标的文件夹下的**所有文件**作为分析上下文（知识库 + 备忘录 + 用户手动拖入的文件 + 历史策略报告）

### Step 4：执行目录初始化

```bash
mkdir -p "data/reports/strategy/raw/$(date +%Y-%m)" \
         "data/reports/strategy/$(date +%Y-%m)"
```

### Step 5：执行策略路由

根据动作意图分流到对应路由：

---

#### 路由 A：买入（首次建仓）

**提示词链**：
```
P2（复用 Step 3 结论）
  ↓
Step 3.5 候选标的横向对比（见下方）
  ↓
P9 反向DCF 估值 → skills/ymos-core/prompts/p9-valuation.md
  ↓
P5 FOMO Killer → prompts/p5-fomo-killer.md
  ↓
[可选] P10 期权策略 → prompts/p10-options.md
  ↓
P12 纪律审查 → prompts/p12-referee.md
  ↓
P17 仓位计算器 → prompts/p17-position-sizing.md
  ↓
Human 最终决策 ✋

**情绪数据（可选辅助）**：
- 若存在 `data/reports/sentiment/` 中对应标的的最新情绪报告，可在 P5 和 P12 分析中引用
- 情绪数据不阻塞流程，仅作为辅助参考维度（如：极端看多时 P5 需额外警惕 FOMO）

**交易行为实证（可选辅助）**：
- 运行 `ymos trade-history fetch --days 30` 获取近期实际成交记录，P12 可引用作为行为偏误的客观实证
- 例如：频繁换手率、追涨杀跌模式、亏损后加大投入等行为模式
- 需 Futu OpenD 在线，不可用时跳过，标注「交易记录数据缺失，跳过行为实证」

**资金流确认（可选辅助）**：
- 若存在 `data/reports/radar/raw/` 中对应标的的最新资金流数据，可在 P12 分析中引用
- 运行 `ymos fetch-capital-flow fetch --ticker TICKER` 获取，或在雷达报告中读取
- 资金流数据不阻塞流程，仅作为辅助确认维度：
  - 主力资金连续 3 日净流入 → P12 正向确认「资金面确认：主力资金连续净流入」
  - 主力资金持续流出 → P12 风险提示「资金面警告：主力资金持续流出」
  - 无资金流数据时跳过，标注「资金流数据缺失，跳过资金面确认」
```

**Step 3.5 候选标的横向对比**（P2 之后、P9 之前执行）：

1. 从 `Watchlist_状态机.md` 和 `持仓_状态机.md` 中筛选与目标标的**同类型**（PVE/PVP 分类相同）的候选标的
2. 对每个候选标的，从其 `个股基础知识库.md` 提取 P2 和 P9 数据
3. 按以下四个维度进行标准化评分（1-5 分 + 一句话理由）：
   - **阶段成熟度**（P2）：当前阶段，距催化剂远近
   - **估值安全边际**（P9）：价格相对合理估值的折让/溢价
   - **催化剂临近度**（P4）：近期是否有明确催化剂事件
   - **风险收益比**（综合）：下行风险 vs 上行空间
4. 输出对比表格，排名第一的标的标注为「当前最优选择」
5. 写入策略报告的「## 候选标的横向对比」区块

**无同类候选时**：输出"当前无同类候选标的可供对比，继续执行单标的分析"，跳过对比步骤。

**写回**：
1. `Watchlist_状态机.md` → 更新为「已建仓」
2. 对应标的 `买入卖出备忘录.md` → 追加买入记录
3. `持仓_状态机.md` → 新增标的
4. 将标的从 `动态Watchlist/` 迁移至 `持仓/`
5. 归档到 `data/reports/strategy/YYYY-MM/YYYY-MM-DD_TICKER_买入.md`
6. → **最终挪入个股文件夹**
7. 策略报告中**必须包含**「## 候选标的横向对比」和「## 仓位建议」区块

---

#### 路由 B：加仓

**提示词链**：
```
P2 → Step 3.5 候选标的横向对比 → P3/P9（事件/价格触发） → P5 FOMO Killer → P12 纪律审查 → P17 仓位计算器 → Human ✋
```

**资金流确认（可选辅助）**：
- 同 Route A 资金流确认逻辑
- 加仓场景中，主力资金持续流入作为加仓的正向确认信号

**Step 3.5 横向对比（加仓模式）**：对比「加仓当前标的」vs「用同等资金买入 Watchlist 中其他候选」的预期收益风险比，输出建议。

**写回**：
1. `买入卖出备忘录.md` → 追加加仓记录
2. `持仓_状态机.md` → 更新成本价
3. 归档 → 挪入个股文件夹
4. 策略报告中**必须包含**「## 候选标的横向对比」和「## 仓位建议」区块

---

#### 路由 C：持有评估

**提示词链**：
```
P2 → P6 利润守门员 → [事件]P3 → [宏观]P8 → P12 纪律审查 → Human ✋
```

**写回**：
1. `买入卖出备忘录.md` → 追加评估记录
2. `持仓_状态机.md` → 更新监控价位
3. 归档 → 挪入个股文件夹

---

#### 路由 D：减仓 / 卖出

**提示词链**：
```
读取备忘录（原始买入理由） → P2 → P6 → [可选]P10 → P12 → Human ✋
```

> ⚠️ **卖出前三问**：
> 1. 买入核心逻辑是否已被证伪？
> 2. 卖出是基于策略还是恐慌？
> 3. 再出现利好会后悔吗？

**强制复盘（完全清仓时）**：

当标的完全清仓（从持仓移入 Watchlist）后，**必须执行 P11 交易复盘**：
1. 读取 `prompts/p11-autopsy.md` 结构化复盘模板
2. 执行四维度复盘：买入逻辑回溯 / P1P4偏差 / P5P6阈值校准 / 经验教训提炼
3. **写回个股知识库**：在 `个股基础知识库.md` 末尾追加 `## P11 交易复盘` 区块
4. **写回投资偏好**（需用户确认）：如阈值需调整，追加到「核心心法」→「历史教训」
5. 归档复盘报告到 `data/reports/strategy/YYYY-MM/YYYY-MM-DD_TICKER_P11复盘.md` → 最终挪入个股文件夹

**部分减仓时**：不执行完整 P11，仅输出简版提示（买入逻辑是否仍然成立）。

**写回**：
1. `买入卖出备忘录.md` → 追加卖出记录
2. `持仓_状态机.md` → 移除或降级
3. 完全清仓：标的从 `持仓/` 移入 `动态Watchlist/`
4. 归档 → 挪入个股文件夹
5. 完全清仓：执行 P11 复盘（见上方）并归档复盘报告
6. 在 `data/stocks/{holdings}/名称_TICKER/` 生成复盘提醒（仅完全清仓时）

---

#### 路由 E：仓位再平衡

**提示词链**：
```
持仓_状态机 → 当前关注方向与投资偏好 → P17 仓位计算器（逐标的） → P7 组合再平衡 → [逐个]P6 → P12 → Human ✋
```

**P17 在再平衡中的角色**：
- 在 P7 之前，先对每个持仓标的调用 P17 计算当前仓位偏差
- 输出调整建议表格（标的、当前仓位、目标仓位、建议操作、调整量）
- P7 基于该表格进行组合级再平衡决策

**写回**：
1. `持仓_状态机.md` → 更新权重
2. 各标的 `买入卖出备忘录.md` → 追加记录
3. 归档到 `data/reports/strategy/YYYY-MM/YYYY-MM-DD_仓位再平衡.md`
4. 策略报告中**必须包含**「## 仓位调整建议」区块（来自 P17 输出）

---

### Step 6：写回产出物

每次策略分析**必须完成以下写回**：

**A. 策略报告**
- `data/reports/strategy/YYYY-MM/YYYY-MM-DD_TICKER_动作类型.md`（成品报告）
- `data/reports/strategy/raw/YYYY-MM/strategy_context_YYYYMMDD_TICKER_动作.json`（中间件）
- **个股报告最终挪入对应标的文件夹**（`data/stocks/{holdings,watchlist}/名称_TICKER/`）

**B. 状态更新**
- `持仓_状态机.md` / `Watchlist_状态机.md`
- 对应标的 `买入卖出备忘录.md`

**B+. 个股知识库增量更新**
- 若本次分析执行了 P2 → 将结论增量写回 `data/stocks/{holdings,watchlist}/名称_TICKER/个股基础知识库.md` 的 `## P2 阶段判断` 区块
  - 已有旧 P2 结论 → **替换**为最新结论（保留日期戳，如 `> 更新于 YYYY-MM-DD`）
  - 无此区块 → **新建追加**到知识库末尾
- 目的：下次策略分析 Step 3 前置检查时，P2 不再缺失，避免重复执行

**C. 策略分析日志（当日汇总）** ⭐
- 路径：`data/reports/strategy/YYYY-MM/策略分析日志_YYYY-MM-DD.md`
- 每次策略分析完成后，追加条目到当日日志
- 日志格式：

```markdown
# 策略分析日志 - YYYY-MM-DD

## 今日分析记录

| 时间 | 标的 | 动作 | 路由 | 结论摘要 | 报告路径 | 状态 |
|:---|:---|:---|:---|:---|:---|:---|
| HH:MM | TICKER | 持有评估 | C | P2:PVE P6:持有 P12:通过 | data/stocks/holdings/XX/... | 待确认 |

## 📋 本次自动调研（Step 1.3）

| 标的 | 触发原因 | 完成状态 |
|:---|:---|:---|
| TICKER | P1 缺失 / 信息过期 / 新关注未建档 | ✅ 完成 / ❌ 失败（原因） |

（无调研建议时此 section 可省略）

## 待用户确认

- [ ] TICKER：P12 通过，建议执行 `建议跑 我想买 TICKER`
- [ ] TICKER：止盈触发，建议确认是否执行

## 宏观分析（如有）

（当日宏观事件分析结论，不针对单标的）

## 下一步建议

- 建议优先处理：XXX
- 信息缺口：XXX 缺少最新财报数据，建议补充
```

**D. 缺失项提示**

仅当存在缺失项时，在策略报告末尾追加：
```markdown
## 📌 优化建议
- 建议补充买入卖出备忘录：`data/stocks/{holdings,watchlist}/名称_TICKER/买入卖出备忘录.md`
```

> 注意：P2 写回已在 B+ 步骤自动完成，不再列入优化建议。

### Step 7：在对话中输出策略报告

直接输出完整策略分析报告内容。

---

## 📦 产出物清单

| 文件 | 路径 | 说明 |
|:---|:---|:---|
| 策略分析报告 | `data/reports/strategy/YYYY-MM/` → 最终挪入个股文件夹 | 按日-标的归档 |
| 策略上下文（Raw） | `data/reports/strategy/raw/YYYY-MM/` | 中间件 |
| 策略分析日志 | `data/reports/strategy/YYYY-MM/` | 当日汇总 |
| 更新：状态机 | `data/state/` | 状态 + P4 |
| 更新：单标的 | `data/stocks/{holdings,watchlist}/名称_TICKER/` | 备忘录 + 策略报告 |

---

## 📁 路径速查

| 内容 | 路径 |
|:---|:---|
| 当前关注方向与投资偏好 | `data/state/preferences.md` |
| 持仓状态机 | `data/state/holdings.md` |
| Watchlist 状态机 | `data/state/watchlist.md` |
| 个股知识库 | `data/stocks/{holdings,watchlist}/名称_TICKER/个股基础知识库.md` |
| 买入卖出备忘录 | `data/stocks/{holdings,watchlist}/名称_TICKER/买入卖出备忘录.md` |
| 最新投资雷达 | `data/reports/radar/YYYY-MM/投资雷达_YYYY-MM-DD.md` |
| 策略归档 | `data/reports/strategy/YYYY-MM/` |
| 策略分析日志 | `data/reports/strategy/YYYY-MM/策略分析日志_YYYY-MM-DD.md` |
| 初始调研 SOP | `skills/ymos-research/sop.md` |
| P 提示词目录 | `skills/<skill>/prompts/` 或 `skills/ymos-core/prompts/` |

---

## 🔮 P 提示词模块（策略层）

| 提示词 | 场景 | 路径 |
|:---|:---|:---|
| P2 Phase Check | 阶段判断 — **每次必跑** | `skills/ymos-core/prompts/p2-phase-check.md` |
| P3 Event Impact | 事件冲击 | `prompts/p3-event-impact.md` |
| P5 FOMO Killer | 买入/加仓审计 | `prompts/p5-fomo-killer.md` |
| P6 Profit Keeper | 持有/卖出审计 | `prompts/p6-profit-keeper.md` |
| P7 Portfolio Check | 组合再平衡 | `prompts/p7-portfolio-check.md` |
| P8 Macro Filter | 宏观过滤 | `prompts/p8-macro-filter.md` |
| P9 Valuation | 反向DCF估值 | `skills/ymos-core/prompts/p9-valuation.md` |
| P10 Options | 期权策略 | `prompts/p10-options.md` |
| P11 Autopsy | 交易复盘 — **清仓时强制执行** | `prompts/p11-autopsy.md` |
| P12 Referee | 纪律审查 — **每次最终必过** | `prompts/p12-referee.md` |
| P17 Position Sizing | 仓位计算器 — **买入/加仓/再平衡时调用** | `prompts/p17-position-sizing.md` |

---

## ⚠️ 边界与反模式

**策略分析不做**：
- 不做市场洞察（ymos-market-insight 的事）
- 不做信号发现（投资雷达的事）
- 不自动执行买卖（Human in the Loop）

**反模式**：
- 跳过 P2 直接进 P5/P6
- 没有 P12 就给出买卖建议
- 没有读取备忘录就做卖出
- 策略分析没有归档
- 因前置缺失就完全不跑（能跑的先跑）

---

*SOP 版本：2026-04-27 · YMOS V4 Skills 架构*
