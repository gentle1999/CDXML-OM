# CDXML-OM 文档

[English](../index.md) | 简体中文

本文档介绍类型化 XML 对象模型、所覆盖的源规范范围，以及保守处理的兼容性边界。
这不代表完整 CDXML 文法验证，也不代表已验证 ChemDraw 互操作性。

## 指南

- [特性支持范围](feature-support.md)：支持的模型与 API、固定源范围及明确限制。
- [特性测试索引](feature-tests.md)：按 XML 所属标签分组的全部 762 组 DTD 属性测试。
- [架构](architecture.md)：生成式 schema 与保留原树的运行时。
- [Schema 与编译器](schema.md)：规范 schema、静态生成和来源标注。
- [兼容性与保留行为](compatibility.md)：解析、对象身份、混合内容、修改和验证。
- [覆盖率计量方法](coverage.md)：分母、测试证据和生成新报告的命令。
- [规范证据基线](specification-baseline.md)：DTD/SDK 源事实及未解决的来源异常。
- [离线来源导入](ingestion.md)：安全地从本地来源生成待审候选。
- [发布流程](releasing.md)：版本标签、构建产物校验、PyPI Trusted Publishing 和 GitHub Release。
- [交互式示例](examples.md)：三个双语 notebook 以及执行/更新命令。

## 架构决策

- [ADR 0001：保守处理引用、ID 与混合内容](adr/0001-conservative-reference-and-content-boundaries.md)
- [ADR 0002：语义化静态元数据组织](adr/0002-semantic-static-metadata.md)

[仓库 README](../../README.zh-CN.md) 提供安装方法和可运行的快速示例。也可查看
[English 文档目录](../index.md)。
