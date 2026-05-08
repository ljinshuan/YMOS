# 催化剂日历 SOP

> 暗号：`催化剂日历` / `下周有什么事件` / `看一下日历`
> 模块：ymos-catalyst-calendar（催化剂事件管理与日历）

---

## 一句话定位

催化剂日历是**前瞻层**：收集和展示即将到来的关键投资事件，帮助用户提前规划仓位。

- 雷达是「事后反应」，日历是「事前规划」
- 关注未来事件，不维护历史数据

---

## 触发暗号

| 暗号 | 操作 |
|:---|:---|
| `催化剂日历` | 查看全局催化剂日历 |
| `下周有什么事件` | 查看下周关键事件 |
| `看一下日历 [ticker]` | 查看某标的的催化剂 |
| `添加事件` | 手动添加催化剂事件 |
| `看一下财报日期` | 查看/抓取财报发布日期 |

---

## 完整执行步骤

### Step 1：加载日历数据

读取全局日历文件：
`data/reports/catalyst-calendar/YYYY-MM/催化剂日历.md`

若不存在 → 创建空日历

### Step 2：操作分流

**查看日历（默认）：**
1. 按日期排序展示所有未来事件
2. 包含：日期、事件描述、类型、影响等级、关联标的、距今天数
3. 高亮高影响（High）事件

**添加事件：**
1. 收集事件信息：
   - 日期
   - 事件描述
   - 事件类型（Earnings/Corporate/Industry/Macro）
   - 影响等级（High/Medium/Low）
   - 关联标的（从持仓/关注列表选择）
   - 事件详情/备注
2. 写入全局日历
3. 若有关联标的 → 同步更新论点追踪的催化剂

**每周预览：**
1. 收集本周（周一至周日）的所有事件
2. 按影响等级排序
3. 生成报告结构：
   - 本周关键事件（按日期排序）
   - 每个事件的影响分析
   - 下周前瞻
   - 风险提示
4. 保存为 Markdown 文件

**财报日期抓取：**
1. 获取持仓/关注列表中的标的
2. 调用 CLI 命令抓取财报日期：
   ```bash
   uv run ymos catalyst-calendar fetch-earnings --tickers AAPL,MSFT,0700.HK
   ```
3. 自动添加到全局日历

### Step 3：事件类型分类

| 类型 | 代码 | 说明 |
|:---|:---|:---|
| 财报 | Earnings | 季度/年度财报发布 |
| 企业 | Corporate | 产品发布、FDA、M&A、管理层变动 |
| 行业 | Industry | 行业会议、贸易展、监管裁决 |
| 宏观 | Macro | FOMC、CPI、GDP、央行决策 |

### Step 4：影响评估

| 等级 | 标准 |
|:---|:---|
| High | 直接影响持仓标的的核心论点 |
| Medium | 可能影响标的的短期价格 |
| Low | 间接影响或仅影响市场情绪 |

### Step 5：事件格式

```markdown
### [日期] 事件名称

- **类型**: Earnings/Corporate/Industry/Macro
- **影响等级**: High/Medium/Low
- **关联标的**: {tickers}
- **仓位影响**: {impact_description}
- **备注**: {notes}
```

---

## 产出物清单

| 文件 | 路径 | 说明 |
|:---|:---|:---|
| 全局日历 | `data/reports/catalyst-calendar/YYYY-MM/催化剂日历.md` | 按月管理 |
| 每周预览 | `data/reports/catalyst-calendar/YYYY-MM/催化剂周报_YYYY-MM-DD.md` | 按周生成 |
| Excel 导出 | `data/reports/catalyst-calendar/YYYY-MM/催化剂日历_{date}.xlsx` | 可选 |

---

## 路径速查

| 内容 | 路径 |
|:---|:---|
| 模板（日历） | `skills/ymos-catalyst-calendar/templates/catalyst-calendar.md` |
| 模板（周报） | `skills/ymos-catalyst-calendar/templates/weekly-preview.md` |
| CLI 命令 | `cli/commands/catalyst_calendar.py` |
| 路由表 | `skills/ymos-core/routing.md` |

---

## 边界与反模式

**催化剂日历不做**：
- 不实时推送通知
- 不自动执行交易
- 不维护历史事件数据库
- 不做事件结果预测

**反模式**：
- 日历过于拥挤，失去焦点（应筛选高影响事件）
- 只关注财报，忽略宏观/行业事件
- 添加事件但不关联持仓

---

*SOP 版本：2026-05-08 · YMOS V4 Skills 架构*
