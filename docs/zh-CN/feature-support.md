# 特性支持范围

[English](../feature-support.md) | 简体中文

本页说明当前 Python API 的能力。它与[覆盖率计量方法](coverage.md)分开：后者说明
如何统计映射和测试证据。

## 来源限定的范围

截至 **2026-10-05** 的已接受、绑定当前源码指纹的新鲜证据运行报告：

| 特性集合 | 已实现并类型化 | 已测试 | 往返验证 |
| --- | ---: | ---: | ---: |
| 固定 DTD 元素 | 53/53 | 53/53 | 53/53 |
| 固定 DTD 的元素/属性组合 | 762/762 | 762/762 | 762/762 |
| PCDATA 特性（`s`、`spectrum`） | 2/2 | 2/2 | 2/2 |
| SDK 扩展组合（20 个额外 XML 属性 + 3 个别名） | 23/23 | 23/23 | 23/23 |

固定版本 Revvity DTD 的 SHA-256 为
`5311978e514ffe154108540c3634c314dc66031a4f3c877a681fc6dca8e128c2`。这些比率表示：
固定来源范围内列出的特性都有类型化实现，并通过特性级读取、写入/修改及序列化/重载
证据。它们**不**表示符合完整 DTD 文法，也**不**表示与 ChemDraw 互操作。
`ChemDrawVerified` 仍为 **0**：本次验收没有独立采集的 ChemDraw 应用验证产物和观察记录。

与上述绑定来源的覆盖快照分开，用户报告称六个当前视觉样例在 Windows ChemDraw Professional
25.5.0.5789 中正常打开；较早的曲线载荷出现 “vector too long”。曲线候选之后已更新，等待复验；
这些观察不改变 `ChemDrawVerified=0`。见[人工样例观察记录](../../examples/render_samples/README.zh-CN.md)。

DTD 的 53 个声明包含 `CDXML` 根元素。`UnknownElement` 是未声明 XML 标签的通用回退
wrapper，不是第 54 个 DTD 模型。`CDXMLDocument` 是手写文档 facade；根元素本身由生成的
`CDXMLRoot` 模型包装。

## DTD 元素模型

每行列出区分大小写的 XML 标签、公开模型类和往返测试特性 ID；链接指向测试源码。
52 个非根元素使用 `test_element_create_remove_round_trip[feature-element:<tag>]`，
`CDXML` 根单独使用 `test_root_creation_mutation_round_trip[feature-element:CDXML]`。
完整测试目录见[特性测试索引](feature-tests.md)。分组仅便于查找，不意味着额外化学语义。

### 文档、页面布局和富文本

| XML 标签 | 公开模型 | 往返测试特性 ID |
| --- | --- | --- |
| `CDXML` | `CDXMLRoot` | [`feature-element:CDXML`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `page` | `Page` | [`feature-element:page`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `fragment` | `Fragment` | [`feature-element:fragment`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `group` | `Group` | [`feature-element:group`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `templategrid` | `TemplateGrid` | [`feature-element:templategrid`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `t` | `Text` | [`feature-element:t`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `s` | `TextRun` | [`feature-element:s`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### 化学图、绘图元素和 XML 引用

| XML 标签 | 公开模型 | 往返测试特性 ID |
| --- | --- | --- |
| `n` | `Node` | [`feature-element:n`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `b` | `Bond` | [`feature-element:b`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `arrow` | `Arrow` | [`feature-element:arrow`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `graphic` | `Graphic` | [`feature-element:graphic`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `curve` | `Curve` | [`feature-element:curve`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `embeddedobject` | `EmbeddedObject` | [`feature-element:embeddedobject`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `objecttag` | `ObjectTag` | [`feature-element:objecttag`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `border` | `Border` | [`feature-element:border`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `table` | `Table` | [`feature-element:table`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `splitter` | `Splitter` | [`feature-element:splitter`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `crossingbond` | `CrossingBond` | [`feature-element:crossingbond`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `crossreference` | `CrossReference` | [`feature-element:crossreference`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `altgroup` | `AltGroup` | [`feature-element:altgroup`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `bracketedgroup` | `BracketedGroup` | [`feature-element:bracketedgroup`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `bracketattachment` | `BracketAttachment` | [`feature-element:bracketattachment`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `represent` | `Represent` | [`feature-element:represent`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `regnum` | `RegistryNumber` | [`feature-element:regnum`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### 反应

| XML 标签 | 公开模型 | 往返测试特性 ID |
| --- | --- | --- |
| `scheme` | `ReactionScheme` | [`feature-element:scheme`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `step` | `ReactionStep` | [`feature-element:step`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### 资源表

| XML 标签 | 公开模型 | 往返测试特性 ID |
| --- | --- | --- |
| `fonttable` | `FontTable` | [`feature-element:fonttable`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `font` | `Font` | [`feature-element:font`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `colortable` | `ColorTable` | [`feature-element:colortable`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | `Color` | [`feature-element:color`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### 几何、注释和光谱

| XML 标签 | 公开模型 | 往返测试特性 ID |
| --- | --- | --- |
| `annotation` | `Annotation` | [`feature-element:annotation`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `chemicalproperty` | `ChemicalProperty` | [`feature-element:chemicalproperty`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `coloredmoleculararea` | `ColoredMolecularArea` | [`feature-element:coloredmoleculararea`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `constraint` | `Constraint` | [`feature-element:constraint`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `geometry` | `Geometry` | [`feature-element:geometry`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `marker` | `Marker` | [`feature-element:marker`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `spectrum` | `Spectrum` | [`feature-element:spectrum`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### 生物结构与序列记录

| XML 标签 | 公开模型 | 往返测试特性 ID |
| --- | --- | --- |
| `bioshape` | `BioShape` | [`feature-element:bioshape`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `plasmidmap` | `PlasmidMap` | [`feature-element:plasmidmap`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `plasmidmarker` | `PlasmidMarker` | [`feature-element:plasmidmarker`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `plasmidregion` | `PlasmidRegion` | [`feature-element:plasmidregion`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `sequence` | `Sequence` | [`feature-element:sequence`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### GEP、TLC 与化学计量记录

| XML 标签 | 公开模型 | 往返测试特性 ID |
| --- | --- | --- |
| `gepband` | `GEPBand` | [`feature-element:gepband`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `geplane` | `GEPLane` | [`feature-element:geplane`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `gepplate` | `GEPPlate` | [`feature-element:gepplate`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `tlclane` | `TLCLane` | [`feature-element:tlclane`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `tlcplate` | `TLCPlate` | [`feature-element:tlcplate`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `tlcspot` | `TLCSpot` | [`feature-element:tlcspot`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `stoichiometrygrid` | `StoichiometryGrid` | [`feature-element:stoichiometrygrid`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### 逻辑与结构组记录

| XML 标签 | 公开模型 | 往返测试特性 ID |
| --- | --- | --- |
| `rlogic` | `RLogic` | [`feature-element:rlogic`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `rlogicitem` | `RLogicItem` | [`feature-element:rlogicitem`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `sgcomponent` | `SGComponent` | [`feature-element:sgcomponent`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `sgdatum` | `SGDatum` | [`feature-element:sgdatum`](../../tests/coverage/test_full_schema_feature_evidence.py) |

SDK 对象清单中缺失的 15 个声明仍然有 DTD 支持的 XML 模型；清单缺失不意味着它们是
未知标签。固定 DTD 的 `altgroup` 内容模型提到了未声明的 `bracket` 子元素；在新来源
证据定义它之前，`<bracket>` 仍使用 `UnknownElement`。

## DTD 之外的 XML 属性

单独统计的 SDK 扩展集合共有 23 组类型化往返特性：其中 20 组是存档 SDK 文档中精确记录、
但不在固定 DTD 中的 XML 元素/属性组合，另有 3 组是 Curve 属性的大小写别名。每一行的
特性 ID 均链接到对应参数化测试源码。

| 所属标签 | XML 属性 | 往返测试特性 ID |
| --- | --- | --- |
| `n` | `bgcolor` | [`feature-sdk:n@bgcolor`](../../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `b` | `bgcolor` | [`feature-sdk:b@bgcolor`](../../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `graphic` | `bgcolor` | [`feature-sdk:graphic@bgcolor`](../../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `curve` | `bgcolor` | [`feature-sdk:curve@bgcolor`](../../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `curve` | `ArrowHeadType` | [`feature-sdk:curve@ArrowHeadType`](../../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `curve` | `ArrowHeadHead` | [`feature-sdk:curve@ArrowHeadHead`](../../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `curve` | `ArrowHeadTail` | [`feature-sdk:curve@ArrowHeadTail`](../../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `embeddedobject` | `bgcolor` | [`feature-sdk:embeddedobject@bgcolor`](../../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `table` | `bgcolor` | [`feature-sdk:table@bgcolor`](../../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `altgroup` | `bgcolor` | [`feature-sdk:altgroup@bgcolor`](../../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `spectrum` | `bgcolor` | [`feature-sdk:spectrum@bgcolor`](../../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `geometry` | `BondLength` | [`feature-sdk:geometry@BondLength`](../../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `geometry` | `LabelFont` | [`feature-sdk:geometry@LabelFont`](../../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `geometry` | `LabelSize` | [`feature-sdk:geometry@LabelSize`](../../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `geometry` | `LabelFace` | [`feature-sdk:geometry@LabelFace`](../../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `geometry` | `LabelColor` | [`feature-sdk:geometry@LabelColor`](../../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `geometry` | `PointIsDirected` | [`feature-sdk:geometry@PointIsDirected`](../../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `constraint` | `BondLength` | [`feature-sdk:constraint@BondLength`](../../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `constraint` | `LabelFont` | [`feature-sdk:constraint@LabelFont`](../../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `constraint` | `LabelSize` | [`feature-sdk:constraint@LabelSize`](../../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `constraint` | `LabelFace` | [`feature-sdk:constraint@LabelFace`](../../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `constraint` | `LabelColor` | [`feature-sdk:constraint@LabelColor`](../../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `tlcplate` | `bgcolor` | [`feature-sdk:tlcplate@bgcolor`](../../tests/coverage/test_sdk_extension_feature_evidence.py) |

SDK 对三个 Curve 属性的大小写拼法与 DTD 不同：`ArrowHeadType`、`ArrowHeadHead`、
`ArrowHeadTail` 是规范 DTD 属性 `ArrowheadType`、`ArrowheadHead`、`ArrowheadTail` 的别名。
两种拼法均可独立读取和写入；冲突会被报告，而不会静默改写大小写。这 20 + 3 组特性与 762 组
DTD 属性分开计数。测试目录为 [`sdk_extension_cases.json`](../../tests/coverage/sdk_extension_cases.json)。

## 特性与测试对应关系

- **53 个元素模型：** 上表逐项列出生命周期往返特性 ID；52 个非根标签对应
  `test_element_create_remove_round_trip`，根标签 `CDXML` 对应单独的
  `test_root_creation_mutation_round_trip`。
- **762 组 DTD 属性：** 每组都有独立的目录 ID 和类型化解析、读取、修改、序列化及重载用例。
  完整的按所属标签索引见[DTD 属性往返测试索引](feature-tests.md)。参数化函数为
  `tests/coverage/test_full_schema_feature_evidence.py::test_mapped_pair_parse_read_mutate_serialize_reload`；
  例如 ID `feature:n@Element` 对应同名参数节点。
- **2 个 PCDATA 特性：** 两项都使用相同的文本解析/修改/重载测试函数：

  | XML 标签 | 特性 ID | 往返测试源码 |
  | --- | --- | --- |
  | `s` | [`feature-character:s`](../../tests/coverage/test_full_schema_feature_evidence.py) | [`test_character_data_parse_read_mutate_serialize_reload`](../../tests/coverage/test_full_schema_feature_evidence.py) |
  | `spectrum` | [`feature-character:spectrum`](../../tests/coverage/test_full_schema_feature_evidence.py) | [`test_character_data_parse_read_mutate_serialize_reload`](../../tests/coverage/test_full_schema_feature_evidence.py) |

- **23 组 SDK 扩展：** 上表逐项列出 `feature-sdk:<owner>@<attribute>` ID；参数化函数为
  `tests/coverage/test_sdk_extension_feature_evidence.py::test_sdk_extension_typed_mutation_roundtrip`。

接受快照中这些适用特性行均有当前新鲜 JUnit 运行的通过往返测试。这里的“逐项对应”不表示
测试了每一种词法取值、所有组合或所有 ChemDraw 语义；测试运行与覆盖率分母详见
[覆盖率计量方法](coverage.md)。

## 可用 API 能力

- **解析和序列化：** `CDXMLDocument.from_string()` 与 `.from_file()` 解析本地 XML；
  `.to_string()` 与 `.to_file()` 写出保留的树。解析器禁用网络访问、DTD 加载和外部实体
  解析。序列化保留 XML 结构和未知内容，但不保证输出字节与源文件逐字节相同。
- **类型化导航与身份：** 精确 XML 标签选择生成的 wrapper；重复包装同一个 `lxml` 元素
  会返回同一个 wrapper。`document.find(Model)` 按公开模型搜索。未知元素可通过
  `UnknownElement`/`CDXMLElement` 导航。
- **集合与查找：** 可通过 `document.pages`、`page.fragments`、`fragment.nodes` 和
  `fragment.bonds` 导航。集合支持迭代、`len()`、索引和 `.all()`；父集合提供
  `.create()`/`.remove()`。`document.get(Node, object_id)` 在没有匹配对象（或对象并非
  `Node`）时返回 `None`；若同一 ID 有多个匹配对象，则抛出 `ReferenceResolutionError`，
  不会任选目标。wrapper 仍暴露原始 XML 元素和属性以供检查。
- **类型化值和修改：** 生成字段覆盖有来源依据的字符串、布尔、数值、枚举、点坐标、
  边界框、列表和引用。专用 XML codec 支持点数组、列表值、键级标志以及依赖上下文的
  `ObjectTag.Value`。读取是惰性的，不会重写未修改值的原始词法形式。
- **子元素集合：** DTD 声明的父子路径可通过父对象集合类型化创建/移除。修改保留 wrapper
  身份，不级联删除对象，也不改写引用。树可以暂时违反子元素最小数量；`validate()` 会
  报告问题，调用方可随后修复。
- **ID 与引用：** 文档级 ID 会在当前可观察 ID 范围内避免冲突。Font ID 属于各自的
  FontTable；Color 行和 TextRun 没有对象 ID。`Bond.begin` 和 `Bond.end` 是类型化 `Node`
  引用。`ReactionStep.reactants`、`.products`、`.arrows` 是面向任意已建模文档对象的引用
  数组，不固定绑定某种化学角色；悬空或歧义引用会被报告，不会猜测目标。
- **富文本和光谱文本：** 当 `TextRun` 含子节点时，拒绝修改 `.content`，以保护不透明的
  混合内容。`Spectrum.data` 是原始直接 PCDATA（元素自己的 `.text` 加直接子节点的
  tails），不是解析后的数值光谱数组。`Text.plain_text` 便利地拼接后代文本片段内容。
- **Font 与 Color 表：** 文档 helper 可读取/创建可选根表，表内集合提供 `Font` 和
  `Color` 行。Font ID 属于 FontTable；Color 行没有 ID。其他元素中的 font/color 索引不会
  解析为 `Font`/`Color` wrapper，也不会自动重映射。
- **验证：** `document.validate()` 返回结构化诊断，覆盖支持的必需字段、类型化值/引用、
  ID 作用域、已知父子路径和子元素数量；它不会拒绝解析，也不会修改 XML 树。

`CDATA` 映射为 `str` 表示原始 XML 词法值可作为文本读取；它不承诺化学解释、单位、应用
默认值或二进制 CDX 编码。仅在固定 DTD 和审查过的来源证据建立 XML 约定时才使用更丰富的
类型。

## 明确边界

- 覆盖结果限定于固定 DTD、审查过的 SDK XML 扩展和已测试 API 操作，不证明符合每一种
  DTD 序列/选择文法，也不覆盖每个 CDXML 修订版或厂商扩展。
- `validate()` 不检查化学正确性；除有文档记录的类型化 XML 约定外，不推断键、结构、反应
  或光谱含义。
- Spectrum PCDATA 保留为词法文本；不声称已知数值样本的分隔符或编码。
- 未知 XML 会被保留，但不会提升为类型化模型。特别是，未声明的 `bracket` 不会产生模型类。
- 不提供二进制 CDX 读写、自动级联引用更新、font/color 索引自动解析/重映射或 ChemDraw
  应用验证。
- 输出保留 XML 结构，但不保证逐字节或全部词法格式与输入一致。

## 重新生成特性证据

在仓库外创建新的证据目录，避免误用旧 JUnit 报告：

```sh
evidence_dir="$(mktemp -d "${TMPDIR:-/tmp}/cdxml-om-feature-run.XXXXXX")"
uv run python -m tools.schema_compiler test-features \
  --run-evidence "$evidence_dir/feature-run.json" \
  --junitxml "$evidence_dir/feature-run.xml" -- tests/coverage
uv run python -m tools.schema_compiler coverage \
  --test-run "$evidence_dir/feature-run.json" --format text
```

JUnit 报告与证据 sidecar 将测试结果绑定到当前源码、schema、覆盖策略、fixtures 和特性
目录。相关文件后续修改会使旧运行失效；请修改后重新运行以上命令。独立目录为
[`feature_cases.json`](../../tests/coverage/feature_cases.json) 和
[`sdk_extension_cases.json`](../../tests/coverage/sdk_extension_cases.json)。
[覆盖率指南](coverage.md)解释所有计量阶段；[规范证据基线](specification-baseline.md)
记录来源事实及未解决分歧。
