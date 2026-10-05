# 兼容性与内容保留

[English](../compatibility.md) | 简体中文

解析器接受本地文件、Unicode 字符串和 XML 字节串，并由 libxml2 处理声明的编码。解析会
禁用外部实体解析、DTD 加载和网络访问。内部 DTD 声明和未展开实体引用保留在树中。根标签
不是精确的 `CDXML` 或 XML 格式错误时会抛出 `ParseError`；已知字段的错误值和未解析引用
会延后到类型化访问或显式验证时处理。

已知 XML 标签按精确名称（含命名空间）匹配。生成运行时覆盖固定 DTD 的全部 53 个声明，
包括类型化 `CDXMLRoot`；手写的 `CDXMLDocument` 仍是文档级 facade。父级集合支持类型化
创建/移除。文档级 `.groups`、`.texts`、`.graphics`、`.arrows` 和 `.schemes` 集合用于导航；
创建必须通过有效父集合进行。另有 20 个 SDK 文档记录但 DTD 未声明的 XML 属性，以及 3 个
大小写变体 Curve 属性，作为独立扩展集处理。未知标签和属性仍可通过通用 `CDXMLElement`
wrapper 导航。

对象 ID 查找仅包括 `document` 作用域对象。重复文档 ID 会使查找和引用解析失败，不会任选
一个目标。Font ID 限于各自的 FontTable，不会由 `document.get(Font, id)` 查找；Color 行和
TextRun 的 ID 作用域为 `none`。根 FontTable/ColorTable ID、Font ID 及未知标签的 `id` 不
会视作文档级 ID。类型化分配器保留生命周期中观察到的 ID，并扫描当前树和原始引用以避免
当前冲突。原始 DOM 修改绕过历史记录；若某 ID 通过原始 DOM 加入又在两次扫描间移除，分配
器无法记住它。Font 局部 ID 在每个表内单独分配和验证。

ReactionStep 的 `reactants`、`products` 和 `arrows` 使用空白分隔的文档 ID 数组，类型化值
是通用 `CDXMLElement` wrapper 元组。目标可以是任意已建模文档对象，包括旧格式中以
`<graphic>` 表示的箭头。目标悬空或有歧义时仍可检查原始 ID。重新赋值会在修改 XML 前验证
所有引用；改名或移除目标不会自动改写/级联更新引用。

Text `<s>` 文本片段以 `.content` 暴露字符数据，以类型化字段暴露格式属性。只读不会重写
DOM，所以原始内容和 CDATA 表示得以保留。替换 `.content` 会修改该片段的字符数据；若其
含子节点则拒绝修改，以免删除不透明混合内容。其他片段的未知属性和格式不变。
`Text.plain_text` 为便利起见拼接后代文本片段。

`spectrum.data` 暴露 `spectrum` 元素直接拥有的词法字符数据：元素的 `.text` 加直接子节点
的 tails。嵌套于 `objecttag`、`annotation` 或其他子元素中的文本不属于 spectrum 数据；注释、
处理指令文本和未展开实体引用不作为样本解释。设置 `.data` 会修改这些直接字符数据，同时
保留子 wrapper 及顺序（并清空旧的子节点尾随文本）。存档 SDK 说明 CDXML 将光谱数据放入
PCDATA，但固定来源没有确定数字样本的分隔符/编码。该 API 是词法文本接口，不是光谱解析器，
也不会解析或抓取实体。

Curve 的规范 DTD 拼法是 `ArrowheadType`、`ArrowheadHead`、`ArrowheadTail`。SDK 的大小写
变体 `ArrowHeadType`、`ArrowHeadHead`、`ArrowHeadTail` 作为别名接受。读取和修改会保留输入
中已有的拼法；如果同一字段的两种拼法同时出现，类型化读取和验证会报告冲突，不会静默
丢弃其中之一。

序列化使用保留的完整 `lxml` 树，可保留 XML 结构、文档级处理指令/注释、CDATA 边界、内部
DTD/实体引用和未知内容，但不是逐字节还原：libxml2 可能规范化引号、声明细节及词法形式。
通过 `raw_element` 的修改会被后续查找和验证看到，但绕过类型检查和分配器历史。

`document.validate()` 报告已知字段/值错误、必需字段、文档级及表内重复 ID、类型化引用、
已知父子约束和子元素数量。子元素最小数量由验证报告，不由修改操作强制，因此移除必需
子元素后可以得到一个中间无效树，之后再修复。如果生成元素位于未建模的父封装元素下，验证
会给出 warning，而不武断地认定源 XML 路由非法。它不是完整 DTD 文法验证、化学验证或应用
互操作保证。

规范定义基于固定 Revvity DTD 和存档 CambridgeSoft SDK 文档。两个小型语料文件托管在
RDKit 仓库；文件自身声明由 ChemDraw 创建，但这不是独立的 ChemDraw 验证。运行时不支持
二进制 CDX，也不包含化学适配器。核心包不依赖 RDKit。保守 ID、引用、混合内容和资源链接
边界详见 [ADR 0001](adr/0001-conservative-reference-and-content-boundaries.md)。

## 应用观察记录

用户报告称，除曲线探针外的六个当前文件在 Windows ChemDraw Professional 25.5.0.5789 中正常打开并渲染。
较早的两点 2D+3D 曲线载荷（SHA-256
`abb94c07688e56763deb6a73e57bccc69cc6f60d69758f9b54b60525ef39d28c`）出现 “vector too long”；之后曲线探针
已用有来源依据的 2D 候选重新生成，仍待复验。未提供截图或可独立复现的应用产物。文件哈希和来源说明见
[样例说明](../../examples/render_samples/README.zh-CN.md)。修改后的曲线尚未复验；这些报告不会改变绑定来源证据的
`ChemDrawVerified` 状态。
