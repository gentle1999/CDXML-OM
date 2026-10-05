# 架构

[English](../architecture.md) | 简体中文

CDXML-OM 以 CDXML schema 为事实来源。规范证据先整理为不可变 schema IR，再由生成器
产生静态 Python 模型、枚举、注册表和验证元数据。运行时包装原始 `lxml` 树，使类型化
读取和修改不会丢弃未知元素、属性或顺序。

```text
规范证据 → 规范 schema → schema IR → 静态代码生成
                                      ↓
                            模型 / 枚举 / 注册表 / 元数据
                                      ↓
                   保留 XML 树的 wrapper → 文档 → 语义适配器
```

运行时保留完整 `lxml` 元素树，并在文档 facade 下实现安全 CDXML 输入/输出。生成字段会
从静态属性元数据中惰性读取值；精确 XML 标签映射到 53 个静态 DTD 模型，未声明标签使用
通用、可导航的 wrapper。生成的 `CDXMLRoot` 与手写的 `CDXMLDocument` facade 分离。相同
`lxml` 元素会复用同一 wrapper。只有文档级 ID 对象参与文档对象查找；局部资源 ID、根节点
和未声明元素的 ID 不会被当成同一命名空间。

类型化 setter 和父对象所有的实时子元素集合会编码并修改已知属性。追加前会验证参数和
同文档引用；移除元素时会保留后续混合文本，不级联更新引用。文档级 ID 单调分配。分配器
在文档生命周期中保留观察到的不透明 `id` 和可解析引用 ID，且每次分配都会重新扫描当前树
以避免冲突；直接修改原始 DOM 会绕过分配历史。Font ID 有独立的表内分配器；Color 行和
富文本片段没有对象 ID。修改 ID 不会重写引用。`validate()` 报告已知 schema 诊断而不拒绝
加载或修改树，并包括子元素数量检查；它不会推断经过未建模封装节点的完整路由，也不是
完整 DTD 文法验证或化学验证。核心依赖仅为 `lxml`，RDKit 不是核心依赖。

生成器产生并保存在源码树中的普通 Python 元数据位于
`cdxml_om._generated._metadata/`，按对象、枚举、逻辑属性所属方/共享属性和证据来源组织。
`schema_metadata` 是向后兼容的导出 facade。元数据是冻结/插槽类型，共享属性保持单一实例
身份。运行时无需导入 YAML、DTD、SDK 目录或编译器工具。该语义化静态布局记录在
[ADR 0002](adr/0002-semantic-static-metadata.md)。

后续来源协调的参考顺序为当前 Revvity CDXML DTD、存档 CambridgeSoft SDK 文档、W3C XML
要求、ChemDraw 生成文件和差分实现。PyCDXML 仅作为历史证据。导入的数据只是候选，不会
自动覆盖经审查的规范定义。
