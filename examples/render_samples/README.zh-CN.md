# 视觉样例与诊断探针

[English](README.md) | 简体中文

这些文件是针对用户反馈制作的后续样例。生成器通过 CDXML-OM 类型化文档和集合 API
创建文件，并以用户认为可接受的 `mol1` fixture 中的 Arial/Times 字体、标准色表、页面样式和
30pt 键长作为起点。生成器会移除来源 `CreationProgram`、文档名、旧页面、旧视口和打印裁剪字段；
不会声称这些文件由 ChemDraw 创建。

用户报告称这些文件曾在 Windows ChemDraw Professional 25.5.0.5789 中打开：下表六个文件正常打开并渲染；
较早的 `probe_curve_points.cdxml` 载荷出现 “vector too long”。未提供截图或可独立复现的应用产物。
之后曲线文件已用不同载荷重新生成，等待用户复验。CDXML-OM 结构验证只说明内部结构检查通过。复验时请
记录 ChemDraw 版本、文件名、缩放比例及错误/警告弹窗；对照原六个文件时使用相同视图设置。

下列 SHA-256 标识用户正常渲染反馈对应的六个文件字节。它们记录报告所指的文件，不是独立应用验证产物。

| 文件 | SHA-256 |
| --- | --- |
| `01_before_after.cdxml` | `964a3a13e65ed5b2206deac62467860bac992403853f463ea8b2c3cb7d167715` |
| `02_reaction_and_resources.cdxml` | `04438a51a15e4f0e009a1f5765f5b73e76bdd705d5a9ca2b72e1b9b85ac0b1d3` |
| `03_unknown_preservation.cdxml` | `420791e8c34b1cdcf602109ba28cecd634f27766f57584a4494aac1c12a65fd7` |
| `probe_element_generic_lists.cdxml` | `d4f28d9375ae7ba35a3470256af0c31fe4bc3ef7ce2635950e53124eac8f5234` |
| `probe_spectrum_missing_required_fields.cdxml` | `a04e5a5fb96ad2b98c322ea1239b092c1a215575087cb90b738c7722e2edcce9` |
| `probe_spectrum_sdk_required_fields.cdxml` | `8495b38484ca2545555cfd21569eada5f5555ec333a74e2168cb3647bf59e8d8` |

## 可读场景候选

| 文件 | 检查内容 |
| --- | --- |
| [`01_before_after.cdxml`](01_before_after.cdxml) | 清楚分隔修改前 C–C 与修改后 C=C–O。修改后副本改变原有键级、新建节点并将其元素改为 O，再创建一条键。这是绘图/编辑演示，不是反应预测。 |
| [`02_reaction_and_resources.cdxml`](02_reaction_and_resources.cdxml) | Arial/Times 富文本、矩形、标准箭头、两个片段，以及指向这些对象本身的 ReactionStep 反应物/产物/箭头引用。不含 Spectrum、Curve 或 list 载荷。 |
| [`03_unknown_preservation.cdxml`](03_unknown_preservation.cdxml) | 易读的 C–O 结构，带一个未知 vendor 属性和一个保留在 XML 中的命名空间扩展。ChemDraw 可能忽略或拒绝该扩展。 |

原子标签是节点子元素 `<t><s>`，使用字体 ID `3`（Arial）；继承的 mol1 资源表中 ID `3` 是 Arial，
ID `4` 是 Times New Roman。SDK 说明 ForegroundColor 使用从 2 开始的色表索引：`3` 选择第二项
（黑色），`4` 选择第三项（红色）。因此样例不会把早先示例的颜色索引 `0` 误当作新 RGB 色行。
[来源事实](../../schema/sources/sdk/focused-properties.json)和
[ForegroundColor SDK 页面](https://chemapps.stolaf.edu/iupac/cdx/sdk/properties/ForegroundColor.htm)
记录了这些边界。

## 隔离探针

以下小文件是诊断假设，不是完整结构，也不宣称语法已被 ChemDraw 确认。请先尝试三个场景候选，再
逐个单独打开探针，记录哪一个文件改变了应用行为：

| 文件 | 隔离载荷与证据边界 |
| --- | --- |
| [`probe_curve_points.cdxml`](probe_curve_points.cdxml) | 用户报告中的旧两点 2D+3D 载荷（SHA-256 `abb94c07688e56763deb6a73e57bccc69cc6f60d69758f9b54b60525ef39d28c`）出现 “vector too long”。当前候选是带边界框的页面级开放曲线，含九个 2D 点；省略可选 3D 点，尚待用户复验。 |
| [`probe_element_generic_lists.cdxml`](probe_element_generic_lists.cdxml) | 使用 `ElementList="NOT 6 8"` 和 `GenericList="alpha beta"`。用户报告称该文件可正常打开并渲染；这并不能独立确认这些 token 的化学含义。SDK 描述空格分隔的值及可选 `NOT` 前缀（例：`NOT 9 17 35` 和 `NOT R X A`）。 |
| [`probe_spectrum_missing_required_fields.cdxml`](probe_spectrum_missing_required_fields.cdxml) | 使用 Spectrum 字段和词法载荷 `400 0.2 500 0.5`，不声称它是有效数值样本编码；与早先示例一样省略 `BoundingBox` 和 `XSpacing`。 |
| [`probe_spectrum_sdk_required_fields.cdxml`](probe_spectrum_sdk_required_fields.cdxml) | 除添加 `BoundingBox` 和 `XSpacing` 外，与上一个探针的 Spectrum 载荷和字段相同。[存档 SDK Spectrum 对象页](https://chemapps.stolaf.edu/iupac/cdx/sdk/Spectrum.htm)将 `BoundingBox`、`XLow`、`XSpacing` 标为必需；固定 DTD 则将这些属性标为可选。两个探针均包含 `XLow`。此差异用于隔离来源不一致，不验证 PCDATA 语法。 |

当前曲线候选的点顺序取自固定版本 [RDKit 样例（提交 `d1985caa`）](https://github.com/rdkit/rdkit/blob/d1985caaa79f6f5d803966a5f4bed69e0c6ef2bc/Code/GraphMol/test_data/CDXML/chemdraw_template5.cdxml)
中的曲线 `80755`，随后按统一比例缩放并平移到本页面。这只是一个样例，不是通用控制点数量规则；
来源样例的许可文件保留在[语料目录](../../tests/fixtures/corpus/RDKit-LICENSE.txt)。SDK 将 Curve 描述为
Bezier 曲线，并将 `CurvePoints` 标记为必需、`CurvePoints3D` 标记为可选（[Curve](https://chemapps.stolaf.edu/iupac/cdx/sdk/Curve.htm)、
[Curve_Points](https://chemapps.stolaf.edu/iupac/cdx/sdk/properties/Curve_Points.htm)、
[Curve_Points3D](https://chemapps.stolaf.edu/iupac/cdx/sdk/properties/Curve_Points3D.htm)）。
XML 点数组没有二进制计数前缀；SDK 数据类型页中的二进制计数字段不代表 CDXML 也应添加该前缀
（[CDXCurvePoints](https://chemapps.stolaf.edu/iupac/cdx/sdk/DataType/CDXCurvePoints.htm)）。
新曲线候选尚未经 ChemDraw 验证；逐个尝试探针前，请先保存当前正在编辑的文档。相关事实位于
[`focused-properties.json`](../../schema/sources/sdk/focused-properties.json) 中的
`curve_point_arrays`、`element_generic_and_formula_lists` 和 `spectrum_data_is_pcdata`。SDK 说明
Spectrum 数据位于 CDXML PCDATA，但现有来源没有给出数值分隔符/编码。不要将探针词法文本解释为已确认
的光谱样本。没有可复现的应用证据和来源事实定位到具体编码错误前，不应据此修改 codec。

## 重新生成样例

在仓库根目录使用当前安装的运行时生成样例。默认命令拒绝覆盖已有文件。重复生成时可指定新目录，
或者使用 `--update` 只替换 `examples/render_samples/` 中由此生成器管理的七个文件名：

```bash
sample_out="$(mktemp -d "${TMPDIR:-/tmp}/cdxml-om-samples.XXXXXX")"
uv run --no-sync python -m tools.build_visual_samples --output-dir "$sample_out"
uv run --no-sync python -m tools.build_visual_samples --update
```

第一条命令将文件写入新目录；最后一条命令会明确重新生成仓库样例目录中由工具管理的七个文件。

生成器保护 notebook 源文件和原始 corpus，不使用桌面自动化。以上应用观察仍是用户报告，不是
ChemDraw 验证。
