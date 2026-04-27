# YMOS Agent 导航（V4）

> 本文件是 Agent 的操作手册。每次新会话开始时先读这里。

---

## 系统架构

YMOS 是自然语言驱动的人机协作投资系统。三层架构：

| 层 | 目录 | 职责 | 关键产出 |
|:---|:---|:---|:---|
| **能力层** | `skills/` | 9 个 YMOS 能力（含 ymos-core 共享基础设施），每个 skill 自包含 SOP、prompts、knowledge | Agent 发现和执行入口 |
| **数据层** | `data/` | 状态机 + 个股文件夹 + 报告 | 运行时状态（git 忽略） |
| **工具层** | `cli/` | `ymos` CLI 命令 | 数据抓取 + 文件操作 |

```
skills（ymos-core 提供共享资源）→ data（存储状态）→ cli（获取数据）
```

---

## Agent 读取优先级

**每次新会话，按此顺序读取**：

1. `总入口暗号.md` — 了解所有可用暗号
2. `data/state/preferences.md` — 了解用户投资策略
3. `data/state/holdings.md` — 了解当前持仓
4. `data/state/watchlist.md` — 了解当前关注

**执行具体 Skill/SOP 时再读取**：
- 对应 SKILL.md（`skills/` 目录下）
- 对应 SOP 文件（`skills/<skill>/sop.md`）
- 对应 P 提示词（`skills/<skill>/prompts/` 或 `skills/ymos-core/prompts/`）

---

## 核心文件：`preferences.md`

> **这是整个系统的灵魂文件。** 投资雷达、策略分析、P 系列提示词的执行质量，都直接取决于这个文件的完整度。

**文件位置**：`data/state/preferences.md`

**为什么它如此关键**：
- **投资雷达**读取它来判断「市场发生的事跟用户有什么关系」
- **策略分析**读取它来校准买卖建议是否符合用户当前的风险偏好和策略立场
- **P5 FOMO 审计**和 **P12 纪律审查**读取它来做"灵魂校准"——确保用户不违反自己定下的纪律
- **P1 建档**和 **P2 阶段判断**读取它来理解用户的关注方向和板块逻辑

**文件包含 10 个维度**：
1. 投资者画像（风险承受度、周期、心理弱点）
2. 仓位配置框架（PVE/PVP/现金目标占比）
3. 双轨并行策略（PVE 进入标准 + PVP 纪律约束）
4. 关注方向与板块偏好（板块关联逻辑 + 宏观信号偏好）
5. Watchlist 选择偏好（入池/出池条件）
6. 仓位管理参数（P17 仓位计算器参数，含默认值）
7. 策略执行偏好（前置校验 + 触发阈值）
8. 当前禁忌（红线规则）
9. 核心心法（投资信念 + 历史教训）
10. 使用说明（AI 读取后应能回答的问题）

**Agent 职责**：
- 每次新会话**必须读取**此文件（优先级 #2）
- 如发现文件内容过于简略（如缺少仓位配置或核心心法），应提醒用户补充
- **Agent 不得静默修改此文件。** 所有修改必须经用户明确确认：
  - ✅ 入职引导中，Agent 整理用户访谈内容 → 展示给用户确认 → 写入
  - ✅ 用户主动要求更新某个维度 → Agent 起草修改建议 → 用户确认 → 写入
  - ❌ Agent 在分析过程中发现"用户偏好似乎变了"→ 自行修改（禁止）
  - ❌ Agent 在任何 SOP 执行中静默追加/删除内容（禁止）

---

## SOP 总览（8 个 Skill）

| Skill | SOP | 触发暗号 | 频率 | Pattern |
|:---|:---|:---|:---|:---|
| ymos-market-insight | market-insight | `跑一下市场洞察` | 每日 | Sequential + Fallback |
| ymos-radar | radar | `跑一下投资雷达` | 每日 | Coordinator |
| ymos-strategy | strategy | `跑一下策略分析` / `我想买 XX` 等 | 事件驱动 | Router → Sequential |
| ymos-research | research | `调研一下 XX` / 被调用 | 按需 | Sequential (Reusable) |
| ymos-diagnosis | SKILL.md | `诊断一下我的策略` / `帮我看看我的投资` | 按需 | Guided Loop |
| ymos-onboarding | onboarding | `开始使用` / `初始化系统` | 首次/补全 | Guided Loop |
| ymos-target-mgmt | target-management | `关注 XX` / `建仓 XX` 等 | 手动 | State Machine CRUD |
| ymos-reconcile | reconcile | `收口一下` / `刷新持仓视图` | 每日收尾 | Sequential |

> **Pattern 图例**：
> - **Sequential**：线性管道，步骤依次执行
> - **Coordinator**：聚合多源输入，条件触发下游任务
> - **Router → Sequential**：先路由分发，再顺序执行对应链路
> - **Guided Loop**：与用户交互式循环，直到条件满足
> - **State Machine CRUD**：原子状态转换操作
> - **Fallback**：主路径失败时自动降级到备选路径

---

## 文件权限表

### 只读（不可修改）

| 路径 | 说明 |
|:---|:---|
| `skills/*/sop.md` | SOP 定义 |
| `skills/*/prompts/*.md` | P 系列提示词资产 |
| `skills/ymos-diagnosis/knowledge/**` | 诊断知识库 |
| `skills/ymos-diagnosis/**` | 投资策略诊断模块 |
| `总入口暗号.md` | 路由表 |
| `AGENT_GUIDE.md` | 本文件 |
| `.env` | API key |

### Human-in-the-Loop（需用户确认后写入）

| 路径 | 说明 |
|:---|:---|
| `data/state/preferences.md` | 投资灵魂文件 — Agent 可起草，用户确认后写入 |

### 可写（遵循 SOP 规则）

| 路径 | 写入规则 |
|:---|:---|
| `data/reports/market-insight/` | 通过市场洞察 SOP，命名：`YYYY-MM-DD_市场洞察.md` |
| `data/reports/radar/` | 通过投资雷达 SOP，命名：`投资雷达_YYYY-MM-DD.md`（同日覆盖，不加 `_v2`） |
| `data/reports/strategy/` | 通过策略分析 SOP（报告 + 日志） |
| `data/state/holdings.md` | 通过 `ymos state update` 更新（见下方） |
| `data/state/watchlist.md` | 通过 `ymos state update` 更新（见下方） |
| `data/stocks/holdings/*/个股基础知识库.md` | P1/P4/P2 写入 |
| `data/stocks/holdings/*/买入卖出备忘录.md` | 策略结论追加 |
| `data/state/memo-view.md` | 持仓收口 SOP 覆盖写入 |
| `data/stocks/watchlist/*/个股基础知识库.md` | P1/P4/P2 写入 |

### 用户可自定义

| 路径 | 说明 |
|:---|:---|
| `cli/core/sources/rss_sources.json` | 增减 RSS 源 |
| `.env` | API Keys（FINNHUB_API_KEY, TUSHARE_TOKEN 等） |

---

## 模块依赖关系

```
skills/ymos-core（共享基础设施）
  → provides: skills/ymos-core/prompts/ (p2, p9)
  → provides: skills/ymos-core/templates/ (knowledge-base, memo)
  → provides: skills/ymos-core/routing.md, watchlist-update-workflow.md

skills/ymos-market-insight
  → reads: prompts/p13-*, cio-rss-*
  → reads: data/state/holdings.md (Finnhub 只拉持仓美股)
  → CLI: ymos fetch-rss, ymos fetch-market, ymos fetch-news
  → writes: data/reports/market-insight/

skills/ymos-radar
  → reads: data/reports/market-insight/ (7天)
  → reads: data/state/holdings.md, data/state/watchlist.md
  → reads: skills/ymos-core/ (共享工作流)
  → CLI: ymos price-scan --from-state
       → cli/core/sources/finnhub.py (Finnhub → 美股/Crypto)
       → cli/core/sources/tushare.py (Tushare → A股 .SS/.SZ)
       → cli/core/sources/yahoo.py (Yahoo → 港股 .HK + 兜底)
  → writes: data/reports/radar/
  → writes: data/stocks/*/个股基础知识库.md (P4更新)
  → writes: data/state/*_state.md (P4列)

skills/ymos-strategy
  → reads: data/reports/radar/ (触发来源)
  → reads: data/state/ (状态机 + 个股文件夹全部文件)
  → reads: prompts/ (P3,P5-P8,P10-P12,P17) + skills/ymos-core/prompts/ (P2,P9)
  → reads: data/state/preferences.md (仓位管理参数，P17使用)
  → writes: data/reports/strategy/ (报告 + 日志)
  → writes: data/state/ (状态机 + 备忘录)

skills/ymos-research
  → reads: prompts/ (p1, p4) + skills/ymos-core/prompts/ (p2, p9)
  → writes: data/stocks/*/个股基础知识库.md
  → writes: data/state/*_state.md (P4列)

skills/ymos-diagnosis（投资策略诊断）
  → reads: skills/ymos-diagnosis/SKILL.md（核心入口，自包含）
  → reads: knowledge/（可选，深度参考）
  → 不写入任何文件（纯对话式诊断）

skills/ymos-target-mgmt
  → reads: skills/ymos-core/templates/ (knowledge-base, memo)
  → calls: skills/ymos-research (关注时联动)
  → writes: data/stocks/ (目录) + data/state/ (状态机)
```

---

## 环境变量（.env）

**重要**：`ymos` CLI 自动加载 `.env` 文件。

如果自动加载失败，Agent 应该：
1. 直接读取 `.env` 文件内容
2. 通过 CLI 参数传入（如 `--finnhub-token`、`--api-key`）

| 变量 | 使用方 | 必须？ |
|:---|:---|:---|
| `FINNHUB_API_KEY` | 价格路由器、Finnhub 新闻 | 可选（免费注册） |
| `TUSHARE_TOKEN` | 价格路由器（A股 .SS/.SZ） | 可选（无则回退 Yahoo） |
| `YMOS_MARKET_API_URL` | Market API 脚本 | 可选（Level 2） |
| `YMOS_MARKET_API_KEY` | Market API 脚本 | 可选（Level 2） |

> 数据配置层级详见 `进阶指南.md`（Level 0 → Level 3 逐级解锁）。

---

## 状态机写回规则（强制）

使用 `ymos state update` 命令或手动编辑时必须同时完成：
1. 更新顶部 `更新时间`
2. 更新对应标的所在行
3. 在 `今日变更日志` 中追加一条摘要

---

## Agent 能力整合（Capability Integration）

> YMOS 设计为可被不同 Agent 编排产品（Claude Code、ChatGPT Codex、Google Antigravity、OpenClaw 等）驱动。
> Agent 的内置能力（搜索、工具调用、Skills）可以增强 SOP 的执行质量，但必须遵守下方原则。

### 进入时自检

Agent 进入 YMOS 时，应在首次交互中检查并声明自己的可用能力：

| 能力类别 | 检查项 | 影响的 SOP 环节 |
|:---|:---|:---|
| **Web 搜索** | 能否实时搜索互联网？ | P1 建档、P2 阶段判断、P3 事件分析 |
| **工具/Skills** | 是否挂载了 MX_Skills 或其他数据工具？ | 选股筛选、财务数据、宏观数据 |
| **文件系统范围** | 能否读取 YMOS 同级目录（如 BrainStorm 等知识模块）？ | 上下文补充、跨模块联动 |
| **代码执行** | 能否运行 Python 脚本？ | 数据拉取（`ymos` CLI 命令） |

### 可增强的环节（鼓励用能力提升质量）

| SOP 环节 | 增强方式 | 约束 |
|:---|:---|:---|
| **P1 Genesis（建档）** | 用搜索补充公司财务、竞争格局、行业数据 | 不改变 P1 模板结构 |
| **P2 Phase Check** | 搜索最新价格/资金流数据辅助判断 | 不改变 PVE/PVP 判断标准 |
| **P3/P15 事件分析** | 搜索最新新闻、公告替代等待用户手动输入 | 不改变分析框架 |
| **P13 市场扫描** | 若有 MX_FinSearch → 补充中文财经资讯 | 不替代 RSS 主链，作为补充 |
| **选股筛选** | 若有 MX_StockPick → P13/P14 发现主题后自动筛选候选池 | 输出结果须转入 P1 建档流程 |
| **财务快照** | 若有 MX_FinData → P1 建档时批量拉取财务指标 | 写入 `个股基础知识库.md` 对应区块 |
| **宏观数据** | 若有 MX_MacroData → P8 压力测试前获取最新宏观数据 | 使用标准化查询格式 |

### 进化边界与协作规则

| 项目 | 规则 | 说明 |
|:---|:---|:---|
| P 系列提示词的结构和判断标准 | **可进化，但需人+AI 协作确认** | 用户结合自身策略改造；改动需人工审阅后生效 |
| 策略动作的 Human in the Loop（P5/P6/P12） | **不可绕过** | 买卖决策必须人工确认 |
| 状态机写入规则 | **必须通过 SOP 路径或 `ymos state` 命令** | 不可直接编辑状态机 |
| 报告命名和覆盖规则（同日覆盖，不加 `_v2`） | **固定** | 系统一致性依赖 |
| SOP 文件和 CLI 代码 | **运行时只读，演进时人机协作修改** | 日常执行不改；策略进化时可与用户一起重构 |

> P 系列提示词是框架样板——它代表一种经过验证的投资思路和决策路由。
> 用户的核心进阶路径是：结合自身投资策略，改造 P 系列提示词和 SOP 路由，让系统的"大脑"持续进化。
> 详见 `进阶指南.md` 的「策略进化」章节。

### 系统架构比喻

- **大脑**：skills/（P 系列提示词 + 策略路由 + SOP）— 做决策、出结论
- **眼睛**：cli/ + skills/ymos-market-insight, ymos-radar（数据抓取 + 市场扫描）— 看市场、报信号
- **记忆**：data/（状态机 + 个股文件夹）— 存状态、积累上下文
- **手脚**：cli/（`ymos` CLI 命令）— 获取数据、执行查询
- **感官增强**：同级知识模块（BrainStorm 等）— 打破数据墙，丰富上下文

---

## 跨模块联动

| 模块类型 | 联动方式 | 典型场景 | 限制 |
|:---|:---|:---|:---|
| **Skills 工具（手脚）** | SOP 步骤按需调用 | FinSearch/FinData/StockPick/MacroData 补充数据 | 调用失败不阻断主流程 |
| **知识模块（感官增强）** | Agent 读取作为上下文 | BrainStorm 投资洞察 → P13 背景 | 只读引用，不修改源模块 |

### Skills 接入协议

当 Agent 检测到新的工具或 Skill 可用时：

1. **主动识别**：检查新工具的能力是否匹配上方"可增强的环节"
2. **格式转换**：新工具的输出必须转化为 YMOS 已有格式（Markdown / JSON）再写入，不引入新的文件格式
3. **优雅降级**：新工具调用失败不得阻断主 SOP 流程（增强是可选的，不是必须的）
4. **声明透明**：在报告中注明"本次使用了 [工具名] 补充数据"，让用户知道数据来源

---

## 扩展新模块

标准流程：

1. **数据抓取** → `cli/commands/` 中添加新命令（`ymos fetch-xxx`）
2. **处理提示词** → 放入对应 skill 的 `prompts/` 目录，或 `skills/ymos-core/prompts/`（如为共享）
3. **SOP 步骤** → 在对应 skill 的 `sop.md` 中添加可选步骤
4. **环境变量** → 更新 `.env.example`
5. **文档** → 更新 `进阶指南.md` + `README.md`

---

## 常见陷阱

1. **不要给报告加 `_v2`/`_v3` 后缀** — 同日覆盖
2. **不要跳过 P2 就进 P5/P6** — 必须先知道现在在哪个阶段
3. **不要没有 P12 就给买卖建议** — 纪律审查是最终关卡
4. **不要因前置缺失就完全不跑** — 能跑的先跑，缺啥补啥
5. **不要把市场洞察当投资雷达** — 洞察不看持仓，雷达才看持仓
6. **不要直接给买/卖建议** — 只建议路由暗号，策略分析 SOP 负责结论
7. **个股分析要读整个文件夹** — 个股文件夹下所有文件都是上下文
8. **不要跳过 `preferences.md`** — 策略分析的必要输入
9. **不要跳过横向对比直接买入** — 买入/加仓路由必须执行 Step 3.5 候选标的对比
10. **不要清仓后跳过 P11 复盘** — 完全清仓时 P11 是强制步骤，经验必须回流

### 投资诊断模块

当用户说「诊断一下我的策略」「帮我看看我的投资」「我的投资有什么问题」时，读取 `skills/ymos-diagnosis/SKILL.md` 启动诊断。诊断模块独立于 YMOS 主流程，不依赖状态机或 P 系列提示词——它有自己的公理体系和诊断框架。

**适用场景**：
- 新用户不确定自己的投资策略 → 先诊断，梳理清楚再初始化 YMOS
- 老用户想定期审视投资逻辑 → 体检模式，7 项检验
- 用户带着具体投资困惑 → 问诊模式，5 层消解漏斗

**诊断完的衔接**：如果诊断发现用户需要系统化策略，建议进入 YMOS 主流程（入职引导 → 填写投资偏好 → 初始化持仓）。

### 执行态度

- **不偷懒**：按 SOP 定义的完整 Pipeline 走完每一步，不因为"数据看起来够了"就跳过后续分析环节
- **不静默失败**：某个步骤出错时，把错误信息和上下文清晰地展示给用户，一起协调解决，而不是吞掉错误继续跑
- **不自作主张**：遇到 SOP 没覆盖的边界情况，暂停并询问用户，而不是猜测用户意图
- **养系统的心态**：SOP 不是一成不变的。执行过程中发现可优化的环节，在报告末尾的"优化建议"中如实记录，帮助用户持续迭代

---

## 日常运行建议

```
每日收盘后（四步闭环）：
1. 跑一下市场洞察          → skills/ymos-market-insight 扫描市场
2. 跑一下投资雷达          → skills/ymos-radar 桥接报告（趋势+价格+建议）
3. 跑一下策略分析          → skills/ymos-strategy 处理雷达建议（如有触发）
4. 收口一下                → skills/ymos-reconcile 一致性校验 + 刷新持仓备忘录视图

用户主动触发：
- 关注/建仓/清仓 XX        → 状态管理
- 调研一下 XX              → 深度调研
- 我想买/卖 XX             → 策略直达
```

### 引导用户深度调研

Agent 做的是重复劳动（拉数据、扫价格、跑 P 链、生成报告、维护状态），目的是把用户从信息苦力中解放出来。但**投资的认知差来自用户自己的深度研究**——读券商研报、跟踪行业动态、理解公司基本面。

**Agent 应主动建议用户的深度调研方向**：
- 策略分析或投资雷达发现信号后 → 建议用户去深挖哪个方向（如"建议关注 XX 下季度指引"）
- 个股知识库信息较薄时 → 提示用户补充深度资料
- 用户把研报、笔记等材料手动拖入个股文件夹后，这些文件自动成为后续分析上下文

**核心原则**：AI 负责系统化执行，用户负责策略优化、关键判断、和深度调研。三者缺一不可。

---

## 文档协同

| 文档 | 面向 | 定位 |
|:---|:---|:---|
| `README.md` | 新用户 | 架构总览、暗号速查 |
| `AGENT_GUIDE.md`（本文件） | Agent | 权限、依赖、能力整合、写回规则 |
| `进阶指南.md` | 进阶用户 | 数据源升级、策略定制、系统扩展 |
| `总入口暗号.md` | Agent + 用户 | 暗号路由表 |

---

*Agent Guide 版本：2026-04-26 · YMOS V4 三层架构（skills 自包含）*
