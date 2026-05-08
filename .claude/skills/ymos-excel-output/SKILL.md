---
name: ymos-excel-output
metadata:
  depends_on: [ymos-core]
description: |
  Excel 输出基础能力，提供通用的 Excel 生成、格式化和模板管理功能。
  其他 skill 通过 cli/excel_writer.py 调用。
---

# ymos-excel-output：Excel 输出

## 调用方式
其他 skill 通过 Python 模块调用：
```python
from cli.excel_writer import write_excel, write_excel_from_template
```

## 格式规范
- 字体：Times New Roman 11pt（数据）、12pt 加粗（标题）
- 颜色：深蓝标题(#1F4E79)、浅蓝表头(#D9E1F2)、灰统计行(#F2F2F2)
- 对齐：数据居中，统计标签左对齐
- 公式：计算值用 Excel 公式而非硬编码
- 注释：硬编码数据添加数据源注释

## 模板系统
- 模板文件：`.claude/skills/ymos-excel-output/templates/*.json`
- 支持参数替换：{key} 格式
- 自定义模板：指定 template_dir 路径

## 边界
- 只写不读（不读取 Excel 数据）
- 不支持宏或 VBA
- 不支持在线编辑
