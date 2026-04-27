## Context

前 4 个 change 完成后，YMOS 的目录结构从 `Eyes/Brain/持仓与关注` 三模块变为 `skills/references/data/cli` 四层。所有入口文件中的路径引用、命令示例、目录描述均已过时。

## Goals / Non-Goals

**Goals:**
- CLAUDE.md 完全重写，反映新架构
- 总入口暗号.md 更新路径引用
- AGENT_GUIDE.md 更新路径引用
- .gitignore 新增 data/ 忽略
- pyproject.toml 注册 ymos CLI 入口
- 删除旧的空模块目录

**Non-Goals:**
- 不重写总入口暗号的交互设计（暗号表结构保留）
- 不改变 AGENT_GUIDE 的整体结构
- 不删除 `总入口暗号.md` 本身（仍是用户入口）

## Decisions

### D1: CLAUDE.md 重写要点

1. **Architecture 部分**：更新为四层架构图
   ```
   skills/ (能力层) → references/ (知识层) → data/ (数据层) → cli/ (工具层)
   ```
2. **Running Scripts 部分**：所有 `python3 Eyes/scripts/xxx.py` 替换为 `ymos xxx`
3. **Key Rules 部分**：路径速查表全部更新
4. **Price Router Logic**：逻辑不变，只更新脚本路径为 CLI 命令
5. **新增 Skill Discovery 部分**：列出 8 个 skill 的路径和触发词
6. **新增 Data Layer 部分**：说明 data/ 目录结构和 .gitignore 策略

### D2: 总入口暗号.md 更新要点

1. SOP 文件链接：从 `Eyes/SOP_xxx.md` 改为 `references/sops/xxx.md`
2. 脚本清单：改为 `ymos` CLI 命令列表
3. 目录结构速查：更新为新四层架构
4. 暗号表：触发暗号不变，SOP 引用路径更新

### D3: AGENT_GUIDE.md 更新要点

1. 全局替换路径引用
2. 更新文件权限表
3. 更新报告命名规则中的路径
4. 更新状态机操作流程（改用 `ymos state` 命令）

### D4: .gitignore 新增

```gitignore
# Runtime data
data/

# Legacy (will be removed)
Eyes/市场洞察/
Eyes/投资雷达/
Brain/策略分析/
```

### D5: pyproject.toml 更新

```toml
[project]
name = "ymos"
version = "3.1.0"
dependencies = ["typer>=0.9", "rich>=13"]

[project.scripts]
ymos = "cli.main:app"
```

### D6: 旧目录清理

删除以下空目录（内容已迁移到 data/ 和 references/）：
- `Eyes/` 整个目录（脚本已迁至 cli/，报告已迁至 data/，SOP 已迁至 references/）
- `Brain/` 整个目录（同上）
- `持仓与关注/` 整个目录（同上）
- `docs/`（当前为空）

## Risks / Trade-offs

- **大批量文件变更**：CLAUDE.md 和 AGENT_GUIDE 内容较多，重写工作量大。缓解：逐段更新，不遗漏
- **过渡期**：在所有 change 应用完成之前，入口文件与新架构不一致。缓解：按顺序执行（P1→P2→P3→P4→P5）
