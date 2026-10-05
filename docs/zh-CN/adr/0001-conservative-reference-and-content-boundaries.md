# ADR 0001：保守处理引用、ID 与混合内容边界

[English](../../adr/0001-conservative-reference-and-content-boundaries.md) | 简体中文

- 状态：已接受
- 日期：2026-10-05

## 背景

CDXML 同时包含文档对象 ID、表内资源 ID、ID 列表和混合 XML 内容。固定 DTD 和 SDK 证据
只部分描述了一些结构。对象模型在目标或资源语义不明确时必须保留原内容，而不能只凭 XML
属性名或可能的化学惯例推断含义。

## 决策

1. **ID 作用域是显式 schema 元数据。** 只有标记为 `document` 的生成对象类型参与文档
   查找和引用解析。Font ID 属于各自 FontTable；TextRun 和 Color 没有对象 ID。未知标签
   的 `id` 不会自动视为文档对象 ID。类型化分配器会在整个文档生命周期中保留已观察到的
   不透明 ID；原始 DOM 修改后会重新扫描当前树以避免现存冲突，但无法记住两次扫描间通过
   原始修改加入又删除的 ID。
2. **保守解析 ReactionStep 对象数组。** `reactants`、`products`、`arrows` 暴露通用
   `CDXMLElement` wrapper 元组，而不是化学语义上更窄的模型类型。这允许旧式
   `<graphic>` 箭头等有效变化。悬空或有歧义时仍可读取原始数字 ID；赋值前会验证全部目标。
3. **TextRun 内容修改不会删除不透明混合内容。** 读取不修改 XML，只暴露字符数据。仅当
   文本片段没有子节点时才允许替换 `.content`；否则抛出结构化修改错误，避免静默删除嵌套
   元素、注释或其他保留内容。
4. **不推断 Font/Color 资源链接。** Font ID 在其 FontTable 内分配和验证，但 TextRun 的
   Font 索引不会解析为 Font wrapper。Color 行没有对象 ID，颜色索引不会解析。自动插表、
   去重和索引重映射推迟到证据充分且 API 可安全保留原内容时再实现。

## 结果

解析器和序列化器可保留语义未识别的 ID、引用和混合内容，不会对其含义作过度承诺。类型化
解析不可用时，调用方仍可查看原始引用 ID 和保留的 XML。相应取舍是，Font/Color 链接和
化学语义上的反应验证需要由运行时之外的应用层处理。序列化保留 XML 结构，不保证原始
字节不变。

另见[兼容性说明](../compatibility.md)、[覆盖率方法](../coverage.md)和
[离线 Schema 导入指南](../ingestion.md)。
