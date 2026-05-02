## 1. CLI 数据获取层

- [x] 1.1 创建 `cli/commands/screener.py`，定义 `ymos screen` 命令组（Typer 子模块）
- [x] 1.2 实现 OpenD 连接检测：启动时检测 localhost:11111 是否可连接
- [x] 1.3 实现 `--market MARKET` 参数（HK/US/CN 必填）
- [x] 1.4 实现 `--preset PRESET` 预设模板查询：加载内置筛选条件，调用 Futu OpenD 选股 API
- [x] 1.5 实现 `--config CONFIG` 自定义配置：读取 JSON 配置文件，解析筛选条件
- [x] 1.6 实现 `--limit N` 结果数量限制（默认 20）
- [x] 1.7 实现 `--list-presets` 列出所有预设模板
- [x] 1.8 实现 JSON + Markdown 双格式输出到 `data/reports/screener/YYYY-MM/`
- [x] 1.9 在 `cli/main.py` 中注册 `screen` 命令

## 2. 预设模板

- [x] 2.1 定义 4 个内置预设模板的筛选条件：
  - growth（成长股）：营收增速 > 20%、净利润增速 > 15%、市值 > 100 亿
  - value（价值股）：PE < 15、PB < 1.5、ROE > 10%、股息率 > 2%
  - high-dividend（高息股）：股息率 > 4%、PE < 20、市值 > 50 亿
  - momentum（动量股）：20 日涨幅 > 10%、换手率 > 3%、市值 > 30 亿
- [x] 2.2 将预设条件按市场（HK/US/CN）适配（不同市场字段名可能不同）

## 3. Skill 文档层

- [x] 3.1 创建 `skills/ymos-screener/` 目录结构：SKILL.md、sop.md、knowledge/
- [x] 3.2 编写 SKILL.md frontmatter（name: ymos-screener, depends_on: [ymos-core], description 含触发词）
- [x] 3.3 编写 SKILL.md body：触发（帮我选股/筛选一下/找一下XX股）、前置条件、执行步骤、产出物、边界
- [x] 3.4 编写 sop.md：详细执行步骤（预设筛选/自定义筛选/结果选择→研究衔接）
- [x] 3.5 编写 `knowledge/screening-templates.md`：预设模板详细定义及各市场适配说明

## 4. 路由与集成

- [x] 4.1 在 `skills/ymos-core/routing.md` 新增 ymos-screener 路由条目（触发词 → screener → 输出 → 可选 research 衔接）
- [x] 4.2 在 intent-classifier 中新增 `stock-screening` 意图分类
- [x] 4.3 更新 `skills/ymos-research/SKILL.md`：新增「从 screener 结果批量触发」调用接口
- [x] 4.4 更新 `skills/ymos-research/sop.md`：新增从 screener 触发的入口（批量调研 + 自动建议加入关注列表）

## 5. 测试与验证

- [x] 5.1 验证 OpenD 连接检测正常工作
- [x] 5.2 验证 `uv run ymos screen --market HK --preset growth --limit 10` 正常返回筛选结果
- [x] 5.3 验证 `uv run ymos screen --list-presets` 列出所有预设
- [x] 5.4 验证自定义配置筛选（JSON config）正常工作
- [x] 5.5 验证 SKILL.md 触发词正确路由到 ymos-screener
- [x] 5.6 验证 screener → research 衔接流程
