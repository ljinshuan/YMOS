## 1. 重写 CLAUDE.md

- [x] 1.1 更新 Architecture 部分：三模块 → 四层架构（skills/references/data/cli）
- [x] 1.2 更新 Running Scripts 部分：所有 python3 命令改为 `ymos` CLI 命令
- [x] 1.3 更新 Key Rules 部分：路径速查表全部指向新路径
- [x] 1.4 更新 Price Router Logic：引用 cli/core/router.py
- [x] 1.5 新增 Skill Discovery 部分：列出 8 个 skill 路径和触发词
- [x] 1.6 新增 Data Layer 部分：说明 data/ 目录结构和 .gitignore 策略
- [x] 1.7 更新 Environment Variables 部分（逻辑不变，路径更新）

## 2. 更新总入口暗号.md

- [x] 2.1 SOP 文件链接：全部指向 references/sops/xxx.md
- [x] 2.2 脚本清单：改为 `ymos` CLI 命令列表
- [x] 2.3 目录结构速查：更新为新四层架构
- [x] 2.4 路径速查：更新所有路径引用
- [x] 2.5 暗号表：触发暗号不变，SOP 链接更新

## 3. 更新 AGENT_GUIDE.md

- [x] 3.1 全局替换路径引用（Eyes/、Brain/、持仓与关注/ → 新路径）
- [x] 3.2 更新文件权限表
- [x] 3.3 更新报告命名规则中的路径
- [x] 3.4 更新状态机操作流程（改用 `ymos state` 命令）

## 4. 更新 .gitignore

- [x] 4.1 确认 `data/` 忽略规则已添加（data-layer-separation 中应已完成，此处验证）

## 5. 更新 pyproject.toml

- [x] 5.1 确认 version 更新（3.0 → 3.1）
- [x] 5.2 确认 `[project.scripts] ymos = "cli.main:app"` 已注册

## 6. 清理旧目录

- [x] 6.1 删除 `Eyes/` 目录（脚本已迁 cli/，报告已迁 data/，SOP 已迁 references/）
- [x] 6.2 删除 `Brain/` 目录（同上）
- [x] 6.3 删除 `持仓与关注/` 目录（同上）
- [x] 6.4 删除 `docs/` 目录（空目录）

## 7. 验证

- [x] 7.1 验证 CLAUDE.md 中所有路径引用指向存在的文件/目录
- [x] 7.2 验证总入口暗号中所有链接可访问
- [x] 7.3 验证 `ymos` CLI 可正常安装和运行
- [x] 7.4 验证 .gitignore 正确忽略 data/
- [x] 7.5 端到端测试：agent 读取 CLAUDE.md 后能发现所有 skill 并正确调用
