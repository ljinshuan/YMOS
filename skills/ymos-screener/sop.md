# 🔍 选股筛选器 SOP

> 暗号：`帮我选股` / `筛选一下 [市场]` / `找一下 [类型]股`
> 模块：ymos-screener（多因子选股筛选）

---

## 一句话定位

选股筛选器是**发现层**：从全市场中按基本面/技术面条件筛选候选标的，输出结构化列表供用户选择和深度调研。

- 筛选是「广撒网」，调研是「深挖掘」
- 筛选不依赖持仓/关注列表，独立运行

---

## 🔑 触发暗号

| 暗号 | 操作 |
|:---|:---|
| `帮我选股` | 交互式选股（询问市场和偏好后执行） |
| `筛选一下 [市场]` | 对指定市场执行筛选 |
| `找一下 [类型]股` | 按类型筛选（成长/价值/高息/动量） |
| `选股` | 同「帮我选股」 |

---

## ⚙️ 完整执行步骤

### Step 1：解析筛选意图

从用户输入中提取：

| 参数 | 来源 | 必填 |
|:---|:---|:---|
| 市场 (HK/US/CN) | 用户明确指定或交互询问 | 是 |
| 筛选类型 | 预设模板名或自定义条件 | 是 |
| 数量限制 | 用户指定，默认 20 | 否 |

**市场推断规则**：
- 「港股」→ HK
- 「美股」→ US
- 「A股」→ CN
- 未指定 → 询问用户

**类型推断规则**：
- 「成长股」→ growth
- 「价值股」→ value
- 「高息股」→ high-dividend
- 「动量股」→ momentum
- 其他条件 → 自定义筛选

### Step 2：构建筛选条件

**预设模板**（详见 `knowledge/screening-templates.md`）：

| 模板 | 关键字段 | 排序 |
|:---|:---|:---|
| growth（成长股） | 营收增速、净利润增速、市值 | 营收增速降序 |
| value（价值股） | PE、PB、ROE、股息率 | PE 升序 |
| high-dividend（高息股） | 股息率、PE、市值 | 股息率降序 |
| momentum（动量股） | 涨幅、换手率、市值 | 涨幅降序 |

**自定义条件**：
- 用户以自然语言描述条件 → AI 解析为筛选参数
- 生成 JSON 配置 → `ymos screen --market MARKET --config <path>`

### Step 3：执行筛选

```bash
# 预设模板
ymos screen screen --market HK --preset growth --limit 20

# 自定义条件
ymos screen screen --market US --config /tmp/screener-config.json --limit 20
```

**前置检查**：OpenD 连接检测（localhost:11111）

### Step 4：展示结果

以表格形式展示筛选结果：

| 代码 | 名称 | 关键指标 1 | 关键指标 2 | ... |
|:---|:---|:---|:---|:---|

**结果处理**：
- 结果为空 → 建议放宽条件或更换模板
- 结果过多（> 50） → 建议缩小条件范围
- 结果适中 → 展示表格 + 提示用户选择

### Step 5：衔接调研（可选）

用户从结果中选择 1-3 只感兴趣的标的 → 逐个触发调研：

```
用户："帮我调研一下这几只"
→ 触发 ymos-research → `调研一下 [ticker1]`
→ 触发 ymos-research → `调研一下 [ticker2]`
```

**调研完成后的建议**：
- 如标的不在持仓/关注列表 → 建议通过 `关注 [ticker]` 加入 Watchlist
- 如调研结果良好 → 建议通过 `我想买 [ticker]` 进入策略分析

---

## 📦 产出物清单

| 文件 | 路径 | 说明 |
|:---|:---|:---|
| 筛选结果（JSON） | `data/reports/screener/YYYY-MM/screener_YYYYMMDD.json` | 原始数据 |
| 筛选报告（Markdown） | `data/reports/screener/YYYY-MM/选股结果_YYYY-MM-DD.md` | 可读报告 |

---

## 📁 路径速查

| 内容 | 路径 |
|:---|:---|
| CLI 命令 | `cli/commands/screener.py`（`ymos screen`） |
| 预设模板 | `skills/ymos-screener/knowledge/screening-templates.md` |
| 调研 SOP | `skills/ymos-research/sop.md` |
| 路由表 | `skills/ymos-core/routing.md` |

---

## ⚠️ 边界与反模式

**选股筛选器不做**：
- 不做深度分析（ymos-research 的事）
- 不自动下单或自动关注
- 不做回测验证
- 不维护本地数据库

**反模式**：
- 筛选结果直接当买入依据（必须经过调研）
- 不看筛选条件就接受结果（条件可能过宽/过窄）
- 跳过调研直接进入策略分析

---

*SOP 版本：2026-05-02 · YMOS V4 Skills 架构*
