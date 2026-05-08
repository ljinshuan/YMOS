## ADDED Requirements

### Requirement: Excel 文件生成
系统 SHALL 能够根据模板和数据生成 Excel 文件。

#### Scenario: 基础 Excel 生成
- **WHEN** 调用 `write_excel(template, data, output_path)` 函数
- **THEN** 系统生成 Excel 文件并保存到指定路径

#### Scenario: 多 Sheet 生成
- **WHEN** 模板中包含多个 Sheet 配置
- **THEN** 系统生成包含多个 Sheet 的 Excel 文件

#### Scenario: 数据绑定
- **WHEN** 模板中引用数据源（如 `data.rows`）
- **THEN** 系统将数据填充到对应位置

### Requirement: 格式化规范
系统 SHALL 应用专业级格式化到 Excel 文件。

#### Scenario: 标题格式化
- **WHEN** 应用标题样式
- **THEN** 单元格使用：深蓝色背景（#1F4E79）、白色文字、加粗、合并单元格

#### Scenario: 表头格式化
- **WHEN** 应用表头样式
- **THEN** 单元格使用：浅蓝色背景（#D9E1F2）、黑色加粗文字、居中对齐

#### Scenario: 数据行格式化
- **WHEN** 应用数据行样式
- **THEN** 单元格使用：白色背景、黑色文字、居中对齐

#### Scenario: 统计行格式化
- **WHEN** 应用统计行样式
- **THEN** 单元格使用：浅灰色背景（#F2F2F2）、黑色文字、左对齐标签

### Requirement: 公式支持
系统 SHALL 支持 Excel 公式而非硬编码值。

#### Scenario: 基础公式
- **WHEN** 需要计算比例或百分比
- **THEN** 使用公式（如 `=B7/C7`）而非硬编码结果

#### Scenario: 统计函数
- **WHEN** 需要计算统计值（Max/Min/Median/Average）
- **THEN** 使用统计函数（如 `=MAX(B7:B9)`）

#### Scenario: 公式引用
- **WHEN** 使用公式引用其他单元格
- **THEN** 确保引用范围正确且不存在循环引用

### Requirement: 单元格注释
系统 SHALL 为硬编码输入数据添加单元格注释。

#### Scenario: 数据源注释
- **WHEN** 填充外部数据源的数据
- **THEN** 添加注释说明数据来源（如 "Futu OpenD, 2025-05-08"）

#### Scenario: 假设注释
- **WHEN** 填充假设或估算数据
- **THEN** 添加注释说明假设依据

### Requirement: 数据验证
系统 SHALL 在生成 Excel 前验证数据质量。

#### Scenario: 完整性验证
- **WHEN** 验证数据
- **THEN** 检查必填字段是否都有值

#### Scenario: 类型验证
- **WHEN** 验证数据
- **THEN** 检查数值字段是否为有效数字、日期字段是否为有效日期

#### Scenario: 范围验证
- **WHEN** 验证数据
- **THEN** 检查数值是否在合理范围内（如百分比 0-100）

#### Scenario: 验证失败处理
- **WHEN** 数据验证失败
- **THEN** 系统提供清晰的错误信息，不生成 Excel 文件

### Requirement: 与现有 Skill 集成
系统 SHALL 支持现有 skill 集成 Excel 输出功能。

#### Scenario: ymos-screener Excel 输出
- **WHEN** 用户在选股时指定 `--output-format excel`
- **THEN** 系统生成包含筛选结果的 Excel 文件

#### Scenario: ymos-radar Excel 输出
- **WHEN** 用户在雷达扫描时指定 `--output-format excel`
- **THEN** 系统生成包含价格和信号的 Excel 文件

#### Scenario: 自定义模板使用
- **WHEN** skill 需要自定义 Excel 格式
- **THEN** 系统支持指定自定义模板路径

### Requirement: 模板系统
系统 SHALL 提供可复用的 Excel 模板。

#### Scenario: 使用预定义模板
- **WHEN** 调用 Excel 输出时指定模板名称
- **THEN** 系统从模板目录加载对应模板

#### Scenario: 模板参数化
- **WHEN** 模板中包含参数（如 `{title}`, `{date}`）
- **THEN** 系统在生成时替换为实际值

#### Scenario: 自定义模板
- **WHEN** 用户提供自定义模板文件
- **THEN** 系统使用该模板而非默认模板

### Requirement: 文件管理
系统 SHALL 管理 Excel 输出文件的位置和命名。

#### Scenario: 输出路径规范
- **WHEN** 生成 Excel 文件
- **THEN** 文件保存到 `data/reports/{report_type}/excel/` 目录

#### Scenario: 文件命名规范
- **WHEN** 生成 Excel 文件
- **THEN** 文件名格式为 `{report_name}_{date}.xlsx`

#### Scenario: 文件覆盖
- **WHEN** 同日同名文件已存在
- **THEN** 系统覆盖旧文件（不生成版本号）

### Requirement: 错误处理
系统 SHALL 提供清晰的错误信息。

#### Scenario: 模板加载失败
- **WHEN** 指定的模板文件不存在
- **THEN** 系统返回错误 "模板文件不存在: {path}"

#### Scenario: 数据格式错误
- **WHEN** 数据无法正确转换为 Excel 格式
- **THEN** 系统返回详细错误信息，指出问题字段

#### Scenario: 写入失败
- **WHEN** Excel 文件写入失败（如权限问题）
- **THEN** 系统返回错误 "无法写入文件: {path}, 原因: {reason}"
