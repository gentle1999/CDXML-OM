# CDXML 规范证据基线

[English](../specification-baseline.md) | 简体中文

本页说明用于扩展对象模型的固定来源事实。目录仅记录证据，不是生成后的规范 schema：
`schema/sources/sdk/evidence.json` 对照仓库中的 Revvity DTD 与历史 CambridgeSoft SDK；
`schema/sources/sdk/focused-properties.json` 保存选定属性的值与编码细节。Schema、编译器和
运行时使用经审查的映射，不会自动把这些事实目录当成规范行为。

## 分母与清单

固定 DTD 的 SHA-256 为
`5311978e514ffe154108540c3634c314dc66031a4f3c877a681fc6dca8e128c2`。该 DTD 声明 53 个元素，
包含 `CDXML` 根节点（非根标签 52 个），以及 762 组元素/属性组合。每个属性的 DTD 词法
类型、必需状态、默认类型/值和枚举值均按原声明记录。

存档 `AllCDXObjects.htm` 清单有 38 行：32 行属于 `object` 命名空间，3 行属于 `property`
命名空间（`colortable`、`fonttable`、`represent`），另有 3 行没有 CDX ID（`color`、`font`、
`s`）。SDK 清单将 `CDXML` 根节点列为 Document 对象（对象标签 `0x8000`）；这不是 XML
`id`，且 DTD 中没有 `CDXML id` 属性。

SDK 对象属性表提供了 410 组精确的 owner/属性名匹配。找不到完全相同的名称不代表 DTD
属性不受支持；名称不会忽略大小写。目录另行分类：

- 20 组有 SDK 记录、但固定 DTD 未声明的 XML 属性；
- 3 个 SDK 拼写与 DTD 仅大小写不同的 Curve 属性；
- 两个由 CDX property 支持的 XML 子元素（`fonttable`、`colortable`）；
- 6 组标为 `(not used)` 的二进制属性记录，它们不是 XML 属性；
- 15 个 DTD 声明但 SDK object 清单没有条目的标签。

15 个缺少 SDK object 清单项的标签为 `annotation`、`bioshape`、
`coloredmoleculararea`、`gepband`、`geplane`、`gepplate`、`marker`、`plasmidmap`、
`plasmidmarker`、`plasmidregion`、`rlogic`、`rlogicitem`、`sgcomponent`、`sgdatum` 和
`stoichiometrygrid`。它们都有 DTD 支持的 XML 模型；没有出现在二进制 object 清单中，不
代表它们是未知标签。若 DTD `CDATA` 属性没有更丰富的 XML 契约证据，则保留为词法字符串；
不会为这些 XML 标签虚构 CDX object tag。

SDK-only XML 属性是来源事实的并集，不计入 DTD 的 762 组分母。所属标签、CDXML 名称、
CDX 属性 ID/常量/类型及来源 locator 均记录在目录中。

## 特定来源的边界案例

根标签 `CDXML` 对应 SDK Document 对象（object tag `0x8000`），但 XML 根元素没有 `id`。
SDK Node 对象页历史性地将 `n id` 标作 `UINT16`；通用 `CDXObjectID` 类型页则说引用使用
`UINT32`。这两条来源事实分别保留。通用类型页还描述了歧义 ID 的“最近对象”解析规则；
运行时采取更严格的歧义拒绝，不沿用该历史启发式。

DTD 第 410 行附近的 `altgroup` 内容模型引用 `bracket` 子元素，但固定 DTD 没有
`bracket` 元素声明。SDK `NamedAltGroup` 子对象表列出的是 `group`、`fragment`、`t` 和
`objecttag`，没有 `bracket`。这仍是未解决的来源异常；不会静默修正任一侧，也不改变
53/762 分母。

存档 SDK `Curve` 属性表将二进制 ID `0x0A38` 同时分配给 `Closed`
（`kCDXProp_Closed`、`CDXBoolean`）和 `CurveSpacing`
（`kCDXProp_Curve_Spacing`、`UINT16`）。存档全局预定义属性表重复相同配对，但它们属于同一
SDK 来源家族，不构成独立佐证。对应属性详情页无法访问；也未找到独立 SDK 头文件证据。
该冲突作为未解决来源异常记录；不擅自修改任一编号，也不把它们宣称为独立验证过的二进制
映射。

详细来源还记录了 XML 与二进制编码不同的情况，避免仅凭 CDX 存储类型推断 XML 类型：

- `Bond_Order` 在二进制中是 `INT16` 位编码。SDK 值表列出 16 个 CDXML 词元；`0xFFFF`
  表示未指定，不会写入 CDXML。SDK 说明属性缺省时按单键处理，列出的二进制值可组合。
  固定 DTD 中 `b.Order` 是 `CDATA #IMPLIED`，不是只有四种值的枚举。`focused-properties.json`
  分别记录二进制值和 XML 词元，不把它们混为普通序号枚举。
- `LabelSize` 与 `CaptionSize` 属性页记录二进制 `INT16` 默认字体大小。另一个
  `CDXString` 类型页称文本格式片段的字体大小为整数 `UINT16`，单位为二十分之一 point，
  并展示 `<s size="12">`。历史来源没有明确说独立的 `LabelSize`/`CaptionSize` 使用相同
  比例，因此不推断这种换算。
- `CDXFontTable` 类型页说明二进制字体 charset 代码是 `UINT16`，但 CDXML 示例写作
  `font charset="iso-8859-1"`；DTD 将 XML 属性声明为 `CDATA`。SDK 没有给出 charset 词元
  到二进制代码的映射，所以 XML `font.charset` 保持词法文本，不转成整数。
- 存档坐标类型页用 `72 144 216` 示例说明 `CDXPoint3D` 的 CDXML 形式是按 x/y/z 排列的
  三个值，单位为 point，允许小数。该段的一句话错误地把 XML 值标为 `CDXPoint2D`；目录
  保留此说明，不将其当作另一条类型约定。全局属性表将中心和两条轴端记录标为
  `CDXPoint3D`，却把三者的 CDXML 名称都写为 `Center3D`，也没有给出所属 XML 对象。DTD
  在一些元素上既有 `Center3D`，也有不同的 `MajorAxisEnd3D`/`MinorAxisEnd3D`。因此保留
  这个名称差异，不自行更正来源表格，也不把二进制 ID 关联到这些 DTD 字段。
- `RotationAngle` 的二进制类型为 `INT32`，单位是度乘以 65536；缺省表示 0 度。
- `CDXDate` 被定义为由七个 `INT16` 组成的 14 字节 UTC 结构，但类型页没有定义 CDXML
  词法日期格式。
- `Attachments`（`CDXObjectIDArrayWithCounts`）在 CDX 中有 `UINT16` 计数前缀，但 CDXML
  表示与 `CDXObjectIDArray` 相同，不带该计数。`LineStarts` 的 `INT16ListWithCounts` 在
  CDX 中也有计数前缀，CDXML 则是扁平列表。Curve 点数组同样是 CDX 带计数、CDXML 扁平
  组件列表。
- `CDXElementList` 和 `CDXGenericList` 说明 CDXML 列表可带 `NOT` 前缀。
  `CDXFormula` 被明确标为未定义/未来扩展；SDK 说明 ChemDraw 不读取也不写入这类数据，
  所以不根据名称推断公式语义。
- `ObjectTag.Value` 的二进制类型为 `varies`；`TagType` 选择 `FLOAT64`、`INT32` 或
  unformatted 字符串。相关页面说明缺省值，但未定义显式空 XML 值的含义。`Unformatted`
  说非打印 XML 字节应十六进制编码；这不足以支持对任意可打印值解码十六进制。
- `Spectrum_DataPoint` 是二进制 `FLOAT64` 数组。属性页将其称为 `temp_SpectrumDataPoint`，
  并说明该显式属性只用于 CDX；CDXML 将数据直接存入 `spectrum` 的 `#PCDATA`。该名称不是
  XML 属性。`Spectrum_YLow` 被标为未来兼容属性，ChemDraw 不读写它。
- `colortable` 和 `fonttable` 是 CDX property 标签（`kCDXProp_ColorTable`、
  `kCDXProp_FontTable`），在 CDXML 中保存为子表对象。`color`、`font` 和 `s` 留在 SDK
  XML-only 命名空间，不伪造二进制对象 ID。

以上是存档 SDK 文档事实，不是对 ChemDraw 的黑盒验证。若 SDK 明确声明某特性不读写或只供
未来兼容，这仍只归因于来源文件，不提升为运行时测试结果。

SDK `Curve` 页将三个属性拼作 `ArrowHeadType`、`ArrowHeadHead`、`ArrowHeadTail`；固定 DTD
拼作 `ArrowheadType`、`ArrowheadHead`、`ArrowheadTail`。运行时以 DTD 名称为规范拼法并将
SDK 拼法记录为别名。读取和修改单一拼法时会保留原大小写；新建 Curve 使用 DTD 拼法。
若两种拼法同时存在，即使值相同，类型化读取和验证也会报告冲突，不会猜测应保留哪一个。
解析和序列化会保留这两个原始属性，调用方可显式修复。

## 来源记录与刷新

每个存档页面的实际 Memento URL、抓取时间戳、获取时间、原始字节大小、SHA-256 和 locator
都记录在 JSON 目录中。由于再分发许可不明确，不在仓库保存存档 HTML。来源 URL/摘要记录
用于审查和固定来源校验。

获取操作是明确调用的开发工具，不是运行时网络依赖：

```sh
uv run python -m tools.spec_evidence.acquire --fetch \
  --pins schema/sources/sdk/evidence.json \
  --output /tmp/sdk-evidence-refresh.json

uv run python -m tools.spec_evidence.acquire --fetch --focused-only \
  --pins schema/sources/sdk/focused-properties.json \
  --output /tmp/focused-evidence-refresh.json
```

`--pins` 请求目录中记录的确切 URL 并在 SHA-256 不符时拒绝结果。不提供固定目录表示明确
刷新来源：请求的存档时间戳可能返回另一份实际快照，工具会记录该变化，而不是声称重新
下载字节确定一致。HTML 导入器会离线修复不规则历史页面，并将修复诊断写入候选记录；
CDXML/DTD 解析仍严格执行。
