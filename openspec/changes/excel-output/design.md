## Context

YMOS 的输出完全基于 Markdown，虽然适合阅读但不利于数据分析。投资者需要：
1. 对数据进行排序、筛选、计算
2. 创建自己的图表和透视表
3. 与其他 Excel 模型集成

Financial Services 的 Excel 输出能力提供了：
- 标准的格式化规范（字体、颜色、边框）
- 公式而非硬编码值
- 多 Sheet 支持
- 条件格式化

YMOS 需要建立类似的 Excel 输出能力，但保持轻量级和可扩展性。

## Goals / Non-Goals

**Goals:**
- 建立通用的 Excel 生成能力
- 提供专业级格式化规范
- 支持公式而非硬编码
- 支持多 Sheet 结构
- 与现有 skill 无缝集成

**Non-Goals:**
- 不提供 Excel 在线编辑功能
- 不实现复杂的 Excel 自动化（如宏）
- 不支持从 Excel 读取数据（当前只写不读）

## Decisions

### 1. Python 库选择

**决策：** 使用 openpyxl 作为主要库，xlsxwriter 用于高级格式化

**理由：**
- openpyxl 是最流行的 Python Excel 库，生态成熟
- xlsxwriter 在图表和条件格式方面更强
- 两者可互补使用

**备选方案：** 只用 openpyxl
- 不利：某些高级格式支持有限

### 2. 格式化规范

**决策：** 采用 Financial Services 的格式规范，简化为最小必要样式

**规范：**
- **字体**：Times New Roman 11pt（数据）、12pt（标题）
- **颜色**：深蓝色标题（#1F4E79）、浅蓝色表头（#D9E1F2）、浅灰色统计行（#F2F2F2）
- **对齐**：所有数据居中对齐
- **边框**：无边框（极简风格）
- **小数位**：百分比 1 位小数、倍数 1 位小数、金额无小数

**理由：**
- 专业且简洁
- 与 Financial Services 一致
- 易于维护

### 3. 模板系统

**决策：** 使用 JSON 模板 + Python 渲染

**模板格式：**
```json
{
  "sheets": [
    {
      "name": "Sheet1",
      "rows": [
        {"type": "header", "cells": [{"value": "Title", "span": 5}]},
        {"type": "data", "source": "data.rows"}
      }
    ]
  ]
}
```

**理由：**
- JSON 易于解析和修改
- 与 YMOS 现有 JSON 配置一致
- 支持动态数据绑定

**备选方案：** Excel 模板文件（.xlsx）
- 不利：版本控制困难，难以合并冲突

### 4. 公式 vs 硬编码

**决策：** 所有计算使用 Excel 公式

**规则：**
- 比例/百分比使用公式（如 `=B7/C7`）
- 统计函数使用公式（如 `=MAX(B7:B9)`）
- 只有原始输入数据可以硬编码
- 所有硬编码输入必须添加单元格注释

**理由：**
- 数据变更时自动更新
- 用户可以修改输入，公式自动重新计算
- 提供透明度（公式可见）

### 5. 多 Sheet 支持

**决策：** 支持多 Sheet，每个 Sheet 有独立配置

**理由：**
- 便于组织不同类型的数据
- 支持多视图（如日历视图 + 按标的分组）
- 与专业 Excel 报告一致

### 6. 与现有 Skill 集成

**决策：** 创建独立的 `ymos-excel-output` skill，通过函数调用使用

**调用方式：**
```python
from cli.excel_writer import write_excel
write_excel(template, data, output_path)
```

**理由：**
- 可复用的核心功能
- 各 skill 通过简单函数调用使用
- 便于测试和维护

### 7. 数据验证

**决策：** 在生成 Excel 前进行数据验证

**验证项目：**
- 必填字段完整性
- 数据类型正确性
- 数值范围合理性
- 公式引用有效性

**理由：**
- 提前发现问题，避免生成错误 Excel
- 提供清晰的错误信息

## Risks / Trade-offs

### Risk 1: Excel 兼容性问题

**风险：** 生成的 Excel 在某些版本或工具（如 WPS、Google Sheets）中显示异常

**缓解：**
- 使用标准格式，避免过于复杂的样式
- 测试多种 Excel 兼容工具
- 提供导出为 CSV 的备选方案

### Risk 2: 性能问题

**风险：** 大量数据时 Excel 生成缓慢

**缓解：**
- 使用批量写入操作
- 对超大数据集提供分页导出
- 考虑使用 xlsxwriter 的优化模式

### Risk 3: 格式维护成本

**风险：** 样式规范需要持续维护，增加复杂度

**缓解：**
- 将样式定义为常量，集中管理
- 使用样式继承，减少重复
- 保持样式简单，减少维护需求

## Migration Plan

**部署步骤：**
1. 安装 openpyxl 和 xlsxwriter 依赖
2. 创建 `cli/excel_writer.py` 模块
3. 创建 `ymos-excel-output` skill
4. 创建 Excel 模板文件
5. 更新 ymos-screener 和 ymos-radar skill
6. 更新 CLAUDE.md

**回滚策略：**
- 所有新增功能都是可选的，不影响现有 Markdown 输出
- 可通过 pip uninstall 卸载新增依赖

## Open Questions

1. **图表支持：** 是否需要支持 Excel 图表生成？
   - 建议：V2 功能，当前只支持数据和公式

2. **条件格式：** 是否需要支持条件格式（如高亮异常值）？
   - 建议：V2 功能，当前使用固定格式

3. **模板管理：** 模板文件存储在哪里？
   - 建议：`.claude/skills/ymos-excel-output/templates/` 目录

4. **多语言支持：** Excel 中的表头和提示是否需要支持多语言？
   - 建议：当前只支持中文，未来扩展

5. **密码保护：** 是否需要支持 Excel 密码保护？
   - 建议：不支持，保持简单

6. **打印设置：** 是否需要设置打印区域和页面布局？
   - 建议：V2 功能，当前不处理
