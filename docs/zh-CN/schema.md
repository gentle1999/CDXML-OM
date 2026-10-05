# 规范 Schema 与编译器

[English](../schema.md) | 简体中文

规范文件位于 `schema/canonical/`；来源清单和注释位于 `schema/sources/`；经审查的兼容性
例外位于 `schema/overrides/`。编译器将 YAML 转换为冻结、带插槽的 Python IR 对象。运行时
包不加载 YAML。

规范 schema 为固定 DTD 中的全部 53 个声明生成静态模型，包括 `CDXMLRoot`、XML-only
结构以及 SDK 对象清单中缺失的 15 个声明。生成模型覆盖全部 762 组 DTD 元素/属性组合。
另外 20 组 SDK 文档中的 XML 属性和 3 个 Curve 大小写别名单独统计。来源引用和 schema
状态表示证据，不表示 ChemDraw 接受；运行时能力和测试覆盖见[覆盖率](coverage.md)。

每个对象都显式声明 ID 作用域：`document`、`local` 或 `none`。绘图/文档对象使用
`document`；Font ID 限于所属 FontTable；表、文本片段和颜色行不拥有对象 ID。共享二进制
属性只定义一次，并明确列出所属方。字符数据字段（`TextRun.content` 和直接词法形式的
`Spectrum.data`）声明为文本存储，不伪装成 XML 属性。若 SDK 未记录数值 CDX 值，字符串枚举
可以不提供数值映射。没有来源依据时，不会仅因 DTD 类型是 `CDATA` 就升级为更强的语义
类型；有明确来源的坐标、引用、枚举、列表和上下文相关 ObjectTag 值使用相应 codec。

只有来源明确支持的 CDX 对象/属性 ID 才会写入 schema。XML `id` 属性并不自动意味着 CDX
对象 ID 或全局 ID 作用域。Schema lock 对规范输入取哈希；只有本地实际保存原始字节的
来源才记录外部来源内容摘要。

在仓库根目录运行 `python -m tools.schema_compiler check`、`build` 或 `coverage`。生成结果
是确定性的静态文件，保存在 `src/cdxml_om/_generated/`；更新 schema 时应同步更新生成物。
元数据在 `_generated/_metadata/` 下按语义组织：每个对象和枚举各有模块；属性按逻辑所属方分组，共享
属性只定义一次；来源依据按来源 ID 分组。`schema_metadata.py` 保留为小型兼容 facade。
不使用编号式大小切片，也不在运行时加载 schema/JSON/YAML。生成器会排序 import 并使用
开发依赖 Ruff 格式化。Ruff 不是运行时依赖。离线 DTD/SDK 证据导入和候选差分见
[Schema 来源导入指南](ingestion.md)。
