## Context

当前运行时数据分布：
- `Eyes/市场洞察/` — 市场洞察报告 + Raw_Data
- `Eyes/投资雷达/` — 投资雷达报告 + Raw_Data
- `Brain/策略分析/` — 策略分析报告 + Raw_Data + 日志
- `持仓与关注/持仓/` — 个股文件夹（知识库 + 备忘录 + 策略报告）
- `持仓与关注/动态Watchlist/` — 关注个股文件夹
- `持仓与关注/持仓_状态机.md` — 持仓状态机
- `持仓与关注/Watchlist_状态机.md` — Watchlist 状态机
- `持仓与关注/当前关注方向与投资偏好.md` — 用户配置
- `持仓与关注/持仓备忘录_视图.md` — 执行看板

这些数据全部在 git 跟踪中，与代码混在一起。

## Goals / Non-Goals

**Goals:**
- 运行时数据全部迁移至 `data/`，与代码分离
- `data/` 加入 `.gitignore`，不再跟踪运行时数据
- 新旧路径映射清晰，便于 CLI 的 paths.py 引用
- 提供一次性迁移命令 `ymos migrate`

**Non-Goals:**
- 不改变文件内容格式（状态机仍是 Markdown，报告仍是 Markdown）
- 不做数据版本管理（不做 git-based data versioning）
- 不合并或去重已有数据

## Decisions

### D1: 目标目录结构

```
data/
├── state/
│   ├── holdings.md              ← 持仓_状态机.md
│   ├── watchlist.md             ← Watchlist_状态机.md
│   ├── preferences.md           ← 当前关注方向与投资偏好.md
│   └── memo-view.md             ← 持仓备忘录_视图.md
├── stocks/
│   ├── holdings/
│   │   ├── 阿里巴巴_BABA/
│   │   │   ├── 个股基础知识库.md
│   │   │   ├── 买入卖出备忘录.md
│   │   │   └── (策略报告等)
│   │   └── ...
│   └── watchlist/
│       ├── Astera Labs_ALAB/
│       │   └── 个股基础知识库.md
│       └── ...
│       └── _archive/            ← 归档的标的
├── reports/
│   ├── market-insight/
│   │   ├── 2026-04/
│   │   │   ├── 2026-04-26_市场洞察.md
│   │   │   └── ...
│   │   └── raw/
│   │       └── 2026-04/
│   │           ├── financial_data_20260426.json
│   │           ├── cio_processed_20260426.md
│   │           └── finnhub_news_20260426.json
│   ├── radar/
│   │   ├── 2026-04/
│   │   │   └── 投资雷达_2026-04-26.md
│   │   └── raw/
│   │       └── 2026-04/
│   │           └── price_scan_20260426.json
│   └── strategy/
│       ├── 2026-04/
│       │   ├── 策略分析日志_2026-04-26.md
│       │   └── ...
│       └── raw/
│           └── 2026-04/
└── dashboard/
    └── 2026-04/
        └── dashboard_2026-04-26.html
```

### D2: 迁移策略

1. 创建 `data/` 目录结构
2. `mv` 文件到新位置
3. 更新 `.gitignore`
4. 提供 `ymos migrate` 命令做自动化迁移
5. 迁移完成后删除旧目录下的空文件夹

### D3: 命名规范化

- 状态机文件名改为英文（`holdings.md`、`watchlist.md`、`preferences.md`）
- 报告文件名保持现有命名（中文日期格式保留，与用户阅读习惯一致）
- Raw_Data 统一放 `raw/` 子目录

## Risks / Trade-offs

- **用户迁移成本**：已有用户需要运行 `ymos migrate`。缓解：提供清晰的迁移指南
- **git 历史断裂**：mv 操作后 git 不再跟踪这些文件。可接受——运行时数据本来就不该在 git 中
- **与 CLI 协同**：此 change 与 cli-infrastructure 的 paths.py 强耦合，需要先定义好路径常量
