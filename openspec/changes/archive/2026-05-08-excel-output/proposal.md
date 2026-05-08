## Why

YMOS 当前所有输出都是 Markdown 格式。虽然 Markdown 易读，但投资机构需要可交互的数据分析工具：
1. 投资者需要对数据进行排序、筛选、计算
2. 需要将数据导入到自己的 Excel 模型中
3. 需要生成标准格式的报告给其他人
4. 缺乏 Excel 输出限制了 YMOS 的专业用途

Financial Services 的 Excel 输出能力提供了完整的模板和格式规范。

## What Changes

**新增能力：**
- 新增 `excel-output` 基础能力，提供通用的 Excel 生成功能
- 新增模板系统，支持可复用的 Excel 模板
- 新增格式化规范，定义专业的 Excel 样式
- 新增数据验证功能，确保 Excel 数据质量

**修改内容：**
- 现有 skill 可选集成 Excel 输出功能
- ymos-radar 的价格扫描报告可导出为 Excel
- ymos-screener 的筛选结果可导出为 Excel
- 未来技能（DCF、Comps）将优先支持 Excel 输出

## Capabilities

### New Capabilities
- `excel-output`: Excel 输出基础能力，包括模板管理、格式化、数据验证

### Modified Capabilities
- (无)

## Impact

**新增文件：**
- `.claude/skills/ymos-excel-output/SKILL.md` — Excel 输出 skill
- `.claude/skills/ymos-excel-output/templates/` — Excel 模板文件
- `.claude/skills/ymos-excel-output/styles/` — 样式定义

**修改文件：**
- `cli/excel_writer.py` — 新增 Python Excel 写入模块
- `ymos-screener` skill — 添加 Excel 导出选项
- `ymos-radar` skill — 添加 Excel 导出选项

**依赖：**
- Python openpyxl 库
- Python xlsxwriter 库（用于高级格式化）

**数据层：**
- Excel 文件输出到 `data/reports/*/excel/` 目录
