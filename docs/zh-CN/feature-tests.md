# DTD 属性往返测试索引

[English](../feature-tests.md) | 简体中文

本索引按确切 XML 所属标签分组，列出固定 DTD 的全部 762 组元素/属性特性及其独立特性 ID。每个 ID 链接到参数化测试源码；目录中的 `pytest_nodeid` 是权威、可直接复制的完整节点 ID。

所有行使用同一参数化测试函数：

`tests/coverage/test_full_schema_feature_evidence.py::test_mapped_pair_parse_read_mutate_serialize_reload[<feature-case-id>]`

例如，`feature:n@Element` 对应节点 `tests/coverage/test_full_schema_feature_evidence.py::test_mapped_pair_parse_read_mutate_serialize_reload[feature:n@Element]`。单独运行：

```sh
uv run pytest 'tests/coverage/test_full_schema_feature_evidence.py::test_mapped_pair_parse_read_mutate_serialize_reload[feature:n@Element]'
```

完整目录在 [`feature_cases.json`](../../tests/coverage/feature_cases.json)；参数化测试实现在 [`test_full_schema_feature_evidence.py`](../../tests/coverage/test_full_schema_feature_evidence.py)。所有特性用例是否当前通过并完成往返，以新鲜 JUnit 绑定覆盖率报告为准；该对应关系不意味着测试了每种词法值/组合或所有 ChemDraw 语义。

### XML 所属标签：`CDXML`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `alpha` | [`feature:CDXML@alpha`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `AminoAcidTermini` | [`feature:CDXML@AminoAcidTermini`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `bgalpha` | [`feature:CDXML@bgalpha`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `bgcolor` | [`feature:CDXML@bgcolor`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoldWidth` | [`feature:CDXML@BoldWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BondLength` | [`feature:CDXML@BondLength`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BondSpacing` | [`feature:CDXML@BondSpacing`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BondSpacingAbs` | [`feature:CDXML@BondSpacingAbs`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoundingBox` | [`feature:CDXML@BoundingBox`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CaptionColor` | [`feature:CDXML@CaptionColor`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CaptionFace` | [`feature:CDXML@CaptionFace`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CaptionFont` | [`feature:CDXML@CaptionFont`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CaptionJustification` | [`feature:CDXML@CaptionJustification`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CaptionLineHeight` | [`feature:CDXML@CaptionLineHeight`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CaptionSize` | [`feature:CDXML@CaptionSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CartridgeData` | [`feature:CDXML@CartridgeData`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ChainAngle` | [`feature:CDXML@ChainAngle`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ChemPropAnalysis` | [`feature:CDXML@ChemPropAnalysis`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ChemPropBoilingPt` | [`feature:CDXML@ChemPropBoilingPt`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ChemPropCLogP` | [`feature:CDXML@ChemPropCLogP`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ChemPropCMR` | [`feature:CDXML@ChemPropCMR`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ChemPropCritPres` | [`feature:CDXML@ChemPropCritPres`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ChemPropCritTemp` | [`feature:CDXML@ChemPropCritTemp`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ChemPropCritVol` | [`feature:CDXML@ChemPropCritVol`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ChemPropEForm` | [`feature:CDXML@ChemPropEForm`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ChemPropExactMass` | [`feature:CDXML@ChemPropExactMass`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ChemPropFormula` | [`feature:CDXML@ChemPropFormula`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ChemPropFragmentLabel` | [`feature:CDXML@ChemPropFragmentLabel`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ChemPropGibbs` | [`feature:CDXML@ChemPropGibbs`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ChemPropHenry` | [`feature:CDXML@ChemPropHenry`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ChemPropID` | [`feature:CDXML@ChemPropID`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ChemPropLogP` | [`feature:CDXML@ChemPropLogP`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ChemPropLogS` | [`feature:CDXML@ChemPropLogS`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ChemPropMeltingPt` | [`feature:CDXML@ChemPropMeltingPt`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ChemPropMolWt` | [`feature:CDXML@ChemPropMolWt`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ChemPropMOverZ` | [`feature:CDXML@ChemPropMOverZ`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ChemPropMR` | [`feature:CDXML@ChemPropMR`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ChemPropName` | [`feature:CDXML@ChemPropName`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ChemPropPKa` | [`feature:CDXML@ChemPropPKa`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ChemProptPSA` | [`feature:CDXML@ChemProptPSA`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | [`feature:CDXML@color`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Comment` | [`feature:CDXML@Comment`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CreationDate` | [`feature:CDXML@CreationDate`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CreationProgram` | [`feature:CDXML@CreationProgram`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CreationUserName` | [`feature:CDXML@CreationUserName`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `FixInPlaceExtent` | [`feature:CDXML@FixInPlaceExtent`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `FixInPlaceGap` | [`feature:CDXML@FixInPlaceGap`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `FractionalWidths` | [`feature:CDXML@FractionalWidths`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `HashSpacing` | [`feature:CDXML@HashSpacing`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `HideImplicitHydrogens` | [`feature:CDXML@HideImplicitHydrogens`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `InterpretChemically` | [`feature:CDXML@InterpretChemically`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelColor` | [`feature:CDXML@LabelColor`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelFace` | [`feature:CDXML@LabelFace`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelFont` | [`feature:CDXML@LabelFont`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelJustification` | [`feature:CDXML@LabelJustification`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelLineHeight` | [`feature:CDXML@LabelLineHeight`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelSize` | [`feature:CDXML@LabelSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LineWidth` | [`feature:CDXML@LineWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `MacPrintInfo` | [`feature:CDXML@MacPrintInfo`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Magnification` | [`feature:CDXML@Magnification`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `MarginWidth` | [`feature:CDXML@MarginWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ModificationDate` | [`feature:CDXML@ModificationDate`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ModificationProgram` | [`feature:CDXML@ModificationProgram`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ModificationUserName` | [`feature:CDXML@ModificationUserName`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Name` | [`feature:CDXML@Name`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `PrintMargins` | [`feature:CDXML@PrintMargins`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ResidueBlockCount` | [`feature:CDXML@ResidueBlockCount`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ResidueWrapCount` | [`feature:CDXML@ResidueWrapCount`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `RxnAutonumberConditions` | [`feature:CDXML@RxnAutonumberConditions`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `RxnAutonumberFormat` | [`feature:CDXML@RxnAutonumberFormat`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `RxnAutonumberStart` | [`feature:CDXML@RxnAutonumberStart`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `RxnAutonumberStyle` | [`feature:CDXML@RxnAutonumberStyle`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowAtomEnhancedStereo` | [`feature:CDXML@ShowAtomEnhancedStereo`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowAtomNumber` | [`feature:CDXML@ShowAtomNumber`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowAtomQuery` | [`feature:CDXML@ShowAtomQuery`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowAtomStereo` | [`feature:CDXML@ShowAtomStereo`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowBondQuery` | [`feature:CDXML@ShowBondQuery`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowBondRxn` | [`feature:CDXML@ShowBondRxn`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowBondStereo` | [`feature:CDXML@ShowBondStereo`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowNonTerminalCarbonLabels` | [`feature:CDXML@ShowNonTerminalCarbonLabels`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowResidueID` | [`feature:CDXML@ShowResidueID`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowSequenceBonds` | [`feature:CDXML@ShowSequenceBonds`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowSequenceTermini` | [`feature:CDXML@ShowSequenceTermini`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowSequenceUnlinkedBranches` | [`feature:CDXML@ShowSequenceUnlinkedBranches`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowTerminalCarbonLabels` | [`feature:CDXML@ShowTerminalCarbonLabels`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `WindowIsZoomed` | [`feature:CDXML@WindowIsZoomed`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `WindowPosition` | [`feature:CDXML@WindowPosition`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `WindowSize` | [`feature:CDXML@WindowSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `WinPrintInfo` | [`feature:CDXML@WinPrintInfo`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`colortable`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `id` | [`feature:colortable@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`color`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `b` | [`feature:color@b`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `g` | [`feature:color@g`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `r` | [`feature:color@r`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`fonttable`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `id` | [`feature:fonttable@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`font`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `charset` | [`feature:font@charset`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:font@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `name` | [`feature:font@name`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`page`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `alpha` | [`feature:page@alpha`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `bgalpha` | [`feature:page@bgalpha`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `bgcolor` | [`feature:page@bgcolor`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoundingBox` | [`feature:page@BoundingBox`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoundsInParent` | [`feature:page@BoundsInParent`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | [`feature:page@color`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `DrawingSpace` | [`feature:page@DrawingSpace`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Footer` | [`feature:page@Footer`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `FooterPosition` | [`feature:page@FooterPosition`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Header` | [`feature:page@Header`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `HeaderPosition` | [`feature:page@HeaderPosition`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Height` | [`feature:page@Height`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `HeightPages` | [`feature:page@HeightPages`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:page@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `PageDefinition` | [`feature:page@PageDefinition`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `PageOverlap` | [`feature:page@PageOverlap`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `PrintTrimMarks` | [`feature:page@PrintTrimMarks`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `SplitterPositions` | [`feature:page@SplitterPositions`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Width` | [`feature:page@Width`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `WidthPages` | [`feature:page@WidthPages`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Z` | [`feature:page@Z`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`group`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `BoundingBox` | [`feature:group@BoundingBox`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:group@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Integral` | [`feature:group@Integral`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Z` | [`feature:group@Z`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`fragment`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `Absolute` | [`feature:fragment@Absolute`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoundingBox` | [`feature:fragment@BoundingBox`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ConnectionOrder` | [`feature:fragment@ConnectionOrder`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Formula` | [`feature:fragment@Formula`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:fragment@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Racemic` | [`feature:fragment@Racemic`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Relative` | [`feature:fragment@Relative`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `SequenceType` | [`feature:fragment@SequenceType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Weight` | [`feature:fragment@Weight`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Z` | [`feature:fragment@Z`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`t`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `alpha` | [`feature:t@alpha`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoundingBox` | [`feature:t@BoundingBox`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CaptionColor` | [`feature:t@CaptionColor`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CaptionFace` | [`feature:t@CaptionFace`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CaptionFont` | [`feature:t@CaptionFont`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CaptionJustification` | [`feature:t@CaptionJustification`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CaptionLineHeight` | [`feature:t@CaptionLineHeight`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CaptionSize` | [`feature:t@CaptionSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | [`feature:t@color`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:t@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `IgnoreWarnings` | [`feature:t@IgnoreWarnings`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `InterpretChemically` | [`feature:t@InterpretChemically`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Justification` | [`feature:t@Justification`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelAlignment` | [`feature:t@LabelAlignment`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelColor` | [`feature:t@LabelColor`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelFace` | [`feature:t@LabelFace`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelFont` | [`feature:t@LabelFont`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelJustification` | [`feature:t@LabelJustification`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelLineHeight` | [`feature:t@LabelLineHeight`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelSize` | [`feature:t@LabelSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LineHeight` | [`feature:t@LineHeight`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LineStarts` | [`feature:t@LineStarts`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `p` | [`feature:t@p`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `RotationAngle` | [`feature:t@RotationAngle`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `SupersededBy` | [`feature:t@SupersededBy`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Visible` | [`feature:t@Visible`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Warning` | [`feature:t@Warning`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `WordWrapWidth` | [`feature:t@WordWrapWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Z` | [`feature:t@Z`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`s`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `alpha` | [`feature:s@alpha`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | [`feature:s@color`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `face` | [`feature:s@face`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `font` | [`feature:s@font`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `size` | [`feature:s@size`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`n`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `AbnormalValence` | [`feature:n@AbnormalValence`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `alpha` | [`feature:n@alpha`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `AltGroupID` | [`feature:n@AltGroupID`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `AS` | [`feature:n@AS`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `AtomID` | [`feature:n@AtomID`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `AtomNumber` | [`feature:n@AtomNumber`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Attachments` | [`feature:n@Attachments`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BondOrdering` | [`feature:n@BondOrdering`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Charge` | [`feature:n@Charge`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | [`feature:n@color`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Element` | [`feature:n@Element`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ElementList` | [`feature:n@ElementList`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `EnhancedStereoGroupNum` | [`feature:n@EnhancedStereoGroupNum`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `EnhancedStereoType` | [`feature:n@EnhancedStereoType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ExternalConnectionNum` | [`feature:n@ExternalConnectionNum`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ExternalConnectionType` | [`feature:n@ExternalConnectionType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Formula` | [`feature:n@Formula`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `FreeSites` | [`feature:n@FreeSites`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `GenericList` | [`feature:n@GenericList`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `GenericNickname` | [`feature:n@GenericNickname`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Geometry` | [`feature:n@Geometry`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `HDash` | [`feature:n@HDash`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `HDot` | [`feature:n@HDot`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `HideImplicitHydrogens` | [`feature:n@HideImplicitHydrogens`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:n@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `IgnoreWarnings` | [`feature:n@IgnoreWarnings`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ImplicitHydrogens` | [`feature:n@ImplicitHydrogens`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Isotope` | [`feature:n@Isotope`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `IsotopicAbundance` | [`feature:n@IsotopicAbundance`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelDisplay` | [`feature:n@LabelDisplay`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelFace` | [`feature:n@LabelFace`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelFont` | [`feature:n@LabelFont`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelSize` | [`feature:n@LabelSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LineWidth` | [`feature:n@LineWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LinkCountHigh` | [`feature:n@LinkCountHigh`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LinkCountLow` | [`feature:n@LinkCountLow`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `MarginWidth` | [`feature:n@MarginWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `NeedsClean` | [`feature:n@NeedsClean`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `NodeType` | [`feature:n@NodeType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `NumHydrogens` | [`feature:n@NumHydrogens`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `p` | [`feature:n@p`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Radical` | [`feature:n@Radical`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `RingBondCount` | [`feature:n@RingBondCount`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `RxnChange` | [`feature:n@RxnChange`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `RxnStereo` | [`feature:n@RxnStereo`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowAtomEnhancedStereo` | [`feature:n@ShowAtomEnhancedStereo`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowAtomID` | [`feature:n@ShowAtomID`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowAtomNumber` | [`feature:n@ShowAtomNumber`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowAtomQuery` | [`feature:n@ShowAtomQuery`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowAtomStereo` | [`feature:n@ShowAtomStereo`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowNonTerminalCarbonLabels` | [`feature:n@ShowNonTerminalCarbonLabels`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowTerminalCarbonLabels` | [`feature:n@ShowTerminalCarbonLabels`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `SubstituentsExactly` | [`feature:n@SubstituentsExactly`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `SubstituentsUpTo` | [`feature:n@SubstituentsUpTo`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `SupersededBy` | [`feature:n@SupersededBy`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Translation` | [`feature:n@Translation`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `UnsaturatedBonds` | [`feature:n@UnsaturatedBonds`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Visible` | [`feature:n@Visible`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Warning` | [`feature:n@Warning`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `xyz` | [`feature:n@xyz`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Z` | [`feature:n@Z`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`b`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `alpha` | [`feature:b@alpha`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `B` | [`feature:b@B`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BeginAttach` | [`feature:b@BeginAttach`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BeginExternalNum` | [`feature:b@BeginExternalNum`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoldWidth` | [`feature:b@BoldWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BondCircularOrdering` | [`feature:b@BondCircularOrdering`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BondLength` | [`feature:b@BondLength`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BondSpacing` | [`feature:b@BondSpacing`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BondSpacingAbs` | [`feature:b@BondSpacingAbs`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BS` | [`feature:b@BS`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | [`feature:b@color`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Connectivity` | [`feature:b@Connectivity`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CrossingBonds` | [`feature:b@CrossingBonds`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CrossingBondss` | [`feature:b@CrossingBondss`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Display` | [`feature:b@Display`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Display2` | [`feature:b@Display2`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `DoublePosition` | [`feature:b@DoublePosition`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `E` | [`feature:b@E`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `EndAttach` | [`feature:b@EndAttach`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `EndExternalNum` | [`feature:b@EndExternalNum`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `HashSpacing` | [`feature:b@HashSpacing`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:b@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `IgnoreWarnings` | [`feature:b@IgnoreWarnings`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelFace` | [`feature:b@LabelFace`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelFont` | [`feature:b@LabelFont`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelSize` | [`feature:b@LabelSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LineWidth` | [`feature:b@LineWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `MarginWidth` | [`feature:b@MarginWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Order` | [`feature:b@Order`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `RxnParticipation` | [`feature:b@RxnParticipation`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowBondQuery` | [`feature:b@ShowBondQuery`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowBondRxn` | [`feature:b@ShowBondRxn`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowBondStereo` | [`feature:b@ShowBondStereo`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `SupersededBy` | [`feature:b@SupersededBy`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Topology` | [`feature:b@Topology`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Visible` | [`feature:b@Visible`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Warning` | [`feature:b@Warning`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Z` | [`feature:b@Z`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`graphic`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `alpha` | [`feature:graphic@alpha`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `AngularSize` | [`feature:graphic@AngularSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ArrowType` | [`feature:graphic@ArrowType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoldWidth` | [`feature:graphic@BoldWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoundingBox` | [`feature:graphic@BoundingBox`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BracketType` | [`feature:graphic@BracketType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BracketUsage` | [`feature:graphic@BracketUsage`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CaptionFace` | [`feature:graphic@CaptionFace`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CaptionFont` | [`feature:graphic@CaptionFont`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CaptionSize` | [`feature:graphic@CaptionSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Center3D` | [`feature:graphic@Center3D`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | [`feature:graphic@color`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CornerRadius` | [`feature:graphic@CornerRadius`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `FadePercent` | [`feature:graphic@FadePercent`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `FrameType` | [`feature:graphic@FrameType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `GraphicType` | [`feature:graphic@GraphicType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `HashSpacing` | [`feature:graphic@HashSpacing`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Head3D` | [`feature:graphic@Head3D`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `HeadSize` | [`feature:graphic@HeadSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:graphic@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `IgnoreWarnings` | [`feature:graphic@IgnoreWarnings`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LineType` | [`feature:graphic@LineType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LineWidth` | [`feature:graphic@LineWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LipSize` | [`feature:graphic@LipSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `MajorAxisEnd3D` | [`feature:graphic@MajorAxisEnd3D`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `MinorAxisEnd3D` | [`feature:graphic@MinorAxisEnd3D`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `OrbitalType` | [`feature:graphic@OrbitalType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `OvalType` | [`feature:graphic@OvalType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `PolymerFlipType` | [`feature:graphic@PolymerFlipType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `PolymerRepeatPattern` | [`feature:graphic@PolymerRepeatPattern`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `RectangleType` | [`feature:graphic@RectangleType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShadowSize` | [`feature:graphic@ShadowSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `SupersededBy` | [`feature:graphic@SupersededBy`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `SymbolType` | [`feature:graphic@SymbolType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Tail3D` | [`feature:graphic@Tail3D`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Visible` | [`feature:graphic@Visible`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Warning` | [`feature:graphic@Warning`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Z` | [`feature:graphic@Z`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`arrow`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `alpha` | [`feature:arrow@alpha`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `AngularSize` | [`feature:arrow@AngularSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ArrowEquilibriumRatio` | [`feature:arrow@ArrowEquilibriumRatio`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ArrowheadCenterSize` | [`feature:arrow@ArrowheadCenterSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ArrowheadHead` | [`feature:arrow@ArrowheadHead`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ArrowheadTail` | [`feature:arrow@ArrowheadTail`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ArrowheadType` | [`feature:arrow@ArrowheadType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ArrowheadWidth` | [`feature:arrow@ArrowheadWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ArrowShaftSpacing` | [`feature:arrow@ArrowShaftSpacing`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ArrowSource` | [`feature:arrow@ArrowSource`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ArrowTarget` | [`feature:arrow@ArrowTarget`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoldWidth` | [`feature:arrow@BoldWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoundingBox` | [`feature:arrow@BoundingBox`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CaptionFace` | [`feature:arrow@CaptionFace`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CaptionFont` | [`feature:arrow@CaptionFont`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CaptionSize` | [`feature:arrow@CaptionSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Center3D` | [`feature:arrow@Center3D`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | [`feature:arrow@color`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Dipole` | [`feature:arrow@Dipole`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `FadePercent` | [`feature:arrow@FadePercent`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `FillType` | [`feature:arrow@FillType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `HashSpacing` | [`feature:arrow@HashSpacing`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Head3D` | [`feature:arrow@Head3D`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `HeadSize` | [`feature:arrow@HeadSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:arrow@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `IgnoreWarnings` | [`feature:arrow@IgnoreWarnings`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LineType` | [`feature:arrow@LineType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LineWidth` | [`feature:arrow@LineWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `MajorAxisEnd3D` | [`feature:arrow@MajorAxisEnd3D`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `MinorAxisEnd3D` | [`feature:arrow@MinorAxisEnd3D`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `NoGo` | [`feature:arrow@NoGo`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `SupersededBy` | [`feature:arrow@SupersededBy`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Tail3D` | [`feature:arrow@Tail3D`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Visible` | [`feature:arrow@Visible`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Warning` | [`feature:arrow@Warning`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Z` | [`feature:arrow@Z`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`curve`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `alpha` | [`feature:curve@alpha`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ArrowheadHead` | [`feature:curve@ArrowheadHead`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ArrowheadTail` | [`feature:curve@ArrowheadTail`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ArrowheadType` | [`feature:curve@ArrowheadType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoldWidth` | [`feature:curve@BoldWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoundingBox` | [`feature:curve@BoundingBox`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Closed` | [`feature:curve@Closed`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | [`feature:curve@color`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CurvePoints` | [`feature:curve@CurvePoints`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CurvePoints3D` | [`feature:curve@CurvePoints3D`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CurveSpacing` | [`feature:curve@CurveSpacing`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CurveType` | [`feature:curve@CurveType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `FadePercent` | [`feature:curve@FadePercent`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `FillType` | [`feature:curve@FillType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `HashSpacing` | [`feature:curve@HashSpacing`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `HeadCenterSize` | [`feature:curve@HeadCenterSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `HeadSize` | [`feature:curve@HeadSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `HeadWidth` | [`feature:curve@HeadWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:curve@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `IgnoreWarnings` | [`feature:curve@IgnoreWarnings`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LineType` | [`feature:curve@LineType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LineWidth` | [`feature:curve@LineWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `SupersededBy` | [`feature:curve@SupersededBy`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Visible` | [`feature:curve@Visible`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Warning` | [`feature:curve@Warning`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Z` | [`feature:curve@Z`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`altgroup`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `alpha` | [`feature:altgroup@alpha`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoundingBox` | [`feature:altgroup@BoundingBox`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | [`feature:altgroup@color`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `GroupFrame` | [`feature:altgroup@GroupFrame`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:altgroup@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `IgnoreWarnings` | [`feature:altgroup@IgnoreWarnings`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `p` | [`feature:altgroup@p`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `SupersededBy` | [`feature:altgroup@SupersededBy`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `TextFrame` | [`feature:altgroup@TextFrame`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Valence` | [`feature:altgroup@Valence`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Visible` | [`feature:altgroup@Visible`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Warning` | [`feature:altgroup@Warning`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Z` | [`feature:altgroup@Z`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`step`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `id` | [`feature:step@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ReactionStepArrows` | [`feature:step@ReactionStepArrows`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ReactionStepAtomMap` | [`feature:step@ReactionStepAtomMap`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ReactionStepAtomMapAuto` | [`feature:step@ReactionStepAtomMapAuto`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ReactionStepAtomMapManual` | [`feature:step@ReactionStepAtomMapManual`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ReactionStepObjectsAboveArrow` | [`feature:step@ReactionStepObjectsAboveArrow`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ReactionStepObjectsBelowArrow` | [`feature:step@ReactionStepObjectsBelowArrow`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ReactionStepPlusses` | [`feature:step@ReactionStepPlusses`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ReactionStepProducts` | [`feature:step@ReactionStepProducts`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ReactionStepReactants` | [`feature:step@ReactionStepReactants`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`scheme`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `id` | [`feature:scheme@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`geometry`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `alpha` | [`feature:geometry@alpha`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BasisObjects` | [`feature:geometry@BasisObjects`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoundingBox` | [`feature:geometry@BoundingBox`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | [`feature:geometry@color`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `GeometricFeature` | [`feature:geometry@GeometricFeature`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:geometry@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LineWidth` | [`feature:geometry@LineWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Name` | [`feature:geometry@Name`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `RelationValue` | [`feature:geometry@RelationValue`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `SupersededBy` | [`feature:geometry@SupersededBy`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Z` | [`feature:geometry@Z`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`constraint`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `alpha` | [`feature:constraint@alpha`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BasisObjects` | [`feature:constraint@BasisObjects`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoundingBox` | [`feature:constraint@BoundingBox`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | [`feature:constraint@color`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ConstraintMax` | [`feature:constraint@ConstraintMax`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ConstraintMin` | [`feature:constraint@ConstraintMin`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ConstraintType` | [`feature:constraint@ConstraintType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `DihedralIsChiral` | [`feature:constraint@DihedralIsChiral`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `HashSpacing` | [`feature:constraint@HashSpacing`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:constraint@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `IgnoreUnconnectedAtoms` | [`feature:constraint@IgnoreUnconnectedAtoms`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LineWidth` | [`feature:constraint@LineWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Name` | [`feature:constraint@Name`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `PointIsDirected` | [`feature:constraint@PointIsDirected`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `SupersededBy` | [`feature:constraint@SupersededBy`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Z` | [`feature:constraint@Z`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`templategrid`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `extent` | [`feature:templategrid@extent`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `NumColumns` | [`feature:templategrid@NumColumns`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `NumRows` | [`feature:templategrid@NumRows`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `PaneHeight` | [`feature:templategrid@PaneHeight`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`spectrum`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `alpha` | [`feature:spectrum@alpha`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoldWidth` | [`feature:spectrum@BoldWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoundingBox` | [`feature:spectrum@BoundingBox`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Class` | [`feature:spectrum@Class`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | [`feature:spectrum@color`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:spectrum@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `IgnoreWarnings` | [`feature:spectrum@IgnoreWarnings`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelFace` | [`feature:spectrum@LabelFace`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelFont` | [`feature:spectrum@LabelFont`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelSize` | [`feature:spectrum@LabelSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LineWidth` | [`feature:spectrum@LineWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `SupersededBy` | [`feature:spectrum@SupersededBy`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Visible` | [`feature:spectrum@Visible`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Warning` | [`feature:spectrum@Warning`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `XAxisLabel` | [`feature:spectrum@XAxisLabel`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `XLow` | [`feature:spectrum@XLow`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `XSpacing` | [`feature:spectrum@XSpacing`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `XType` | [`feature:spectrum@XType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `YAxisLabel` | [`feature:spectrum@YAxisLabel`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `YLow` | [`feature:spectrum@YLow`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `YScale` | [`feature:spectrum@YScale`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `YType` | [`feature:spectrum@YType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Z` | [`feature:spectrum@Z`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`embeddedobject`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `alpha` | [`feature:embeddedobject@alpha`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BMP` | [`feature:embeddedobject@BMP`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoundingBox` | [`feature:embeddedobject@BoundingBox`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | [`feature:embeddedobject@color`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CompressedEnhancedMetafile` | [`feature:embeddedobject@CompressedEnhancedMetafile`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CompressedOLEObject` | [`feature:embeddedobject@CompressedOLEObject`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CompressedWindowsMetafile` | [`feature:embeddedobject@CompressedWindowsMetafile`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Edition` | [`feature:embeddedobject@Edition`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `EditionAlias` | [`feature:embeddedobject@EditionAlias`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `EnhancedMetafile` | [`feature:embeddedobject@EnhancedMetafile`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `GIF` | [`feature:embeddedobject@GIF`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:embeddedobject@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `JPEG` | [`feature:embeddedobject@JPEG`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `MacPICT` | [`feature:embeddedobject@MacPICT`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `OLEObject` | [`feature:embeddedobject@OLEObject`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `PDF` | [`feature:embeddedobject@PDF`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `PNG` | [`feature:embeddedobject@PNG`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `RotationAngle` | [`feature:embeddedobject@RotationAngle`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `SupersededBy` | [`feature:embeddedobject@SupersededBy`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `TIFF` | [`feature:embeddedobject@TIFF`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `UncompressedEnhancedMetafileSize` | [`feature:embeddedobject@UncompressedEnhancedMetafileSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `UncompressedOLEObjectSize` | [`feature:embeddedobject@UncompressedOLEObjectSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `UncompressedWindowsMetafileSize` | [`feature:embeddedobject@UncompressedWindowsMetafileSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `WindowsMetafile` | [`feature:embeddedobject@WindowsMetafile`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Z` | [`feature:embeddedobject@Z`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`represent`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `attribute` | [`feature:represent@attribute`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `object` | [`feature:represent@object`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`objecttag`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `DisplayName` | [`feature:objecttag@DisplayName`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:objecttag@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Name` | [`feature:objecttag@Name`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Persistent` | [`feature:objecttag@Persistent`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `PositioningAngle` | [`feature:objecttag@PositioningAngle`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `PositioningOffset` | [`feature:objecttag@PositioningOffset`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `PositioningType` | [`feature:objecttag@PositioningType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `TagType` | [`feature:objecttag@TagType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Tracking` | [`feature:objecttag@Tracking`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Value` | [`feature:objecttag@Value`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Visible` | [`feature:objecttag@Visible`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`sequence`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `SequenceIdentifier` | [`feature:sequence@SequenceIdentifier`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`crossreference`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `CrossReferenceContainer` | [`feature:crossreference@CrossReferenceContainer`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CrossReferenceDocument` | [`feature:crossreference@CrossReferenceDocument`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CrossReferenceIdentifier` | [`feature:crossreference@CrossReferenceIdentifier`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CrossReferenceSequence` | [`feature:crossreference@CrossReferenceSequence`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`regnum`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `id` | [`feature:regnum@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `RegistryAuthority` | [`feature:regnum@RegistryAuthority`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `RegistryNumber` | [`feature:regnum@RegistryNumber`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`splitter`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `p` | [`feature:splitter@p`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `PageDefinition` | [`feature:splitter@PageDefinition`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`table`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `alpha` | [`feature:table@alpha`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoldWidth` | [`feature:table@BoldWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoundingBox` | [`feature:table@BoundingBox`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | [`feature:table@color`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:table@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelFace` | [`feature:table@LabelFace`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelFont` | [`feature:table@LabelFont`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelSize` | [`feature:table@LabelSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LineWidth` | [`feature:table@LineWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `MarginWidth` | [`feature:table@MarginWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `SupersededBy` | [`feature:table@SupersededBy`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Visible` | [`feature:table@Visible`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Z` | [`feature:table@Z`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`tlcplate`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `alpha` | [`feature:tlcplate@alpha`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoldWidth` | [`feature:tlcplate@BoldWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BottomLeft` | [`feature:tlcplate@BottomLeft`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BottomRight` | [`feature:tlcplate@BottomRight`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoundingBox` | [`feature:tlcplate@BoundingBox`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | [`feature:tlcplate@color`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `HashSpacing` | [`feature:tlcplate@HashSpacing`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:tlcplate@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelFace` | [`feature:tlcplate@LabelFace`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelFont` | [`feature:tlcplate@LabelFont`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelSize` | [`feature:tlcplate@LabelSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LineWidth` | [`feature:tlcplate@LineWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `MarginWidth` | [`feature:tlcplate@MarginWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `OriginFraction` | [`feature:tlcplate@OriginFraction`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowBorders` | [`feature:tlcplate@ShowBorders`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowOrigin` | [`feature:tlcplate@ShowOrigin`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowSideTicks` | [`feature:tlcplate@ShowSideTicks`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowSolventFront` | [`feature:tlcplate@ShowSolventFront`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `SolventFrontFraction` | [`feature:tlcplate@SolventFrontFraction`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `SupersededBy` | [`feature:tlcplate@SupersededBy`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `TopLeft` | [`feature:tlcplate@TopLeft`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `TopRight` | [`feature:tlcplate@TopRight`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Transparent` | [`feature:tlcplate@Transparent`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Visible` | [`feature:tlcplate@Visible`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Z` | [`feature:tlcplate@Z`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`tlclane`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `id` | [`feature:tlclane@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Visible` | [`feature:tlclane@Visible`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`tlcspot`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `alpha` | [`feature:tlcspot@alpha`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | [`feature:tlcspot@color`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CurveType` | [`feature:tlcspot@CurveType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Height` | [`feature:tlcspot@Height`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:tlcspot@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Rf` | [`feature:tlcspot@Rf`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowRf` | [`feature:tlcspot@ShowRf`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Tail` | [`feature:tlcspot@Tail`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Visible` | [`feature:tlcspot@Visible`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Width` | [`feature:tlcspot@Width`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Z` | [`feature:tlcspot@Z`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`gepplate`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `alpha` | [`feature:gepplate@alpha`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `AxisWidth` | [`feature:gepplate@AxisWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoldWidth` | [`feature:gepplate@BoldWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BottomLeft` | [`feature:gepplate@BottomLeft`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BottomRight` | [`feature:gepplate@BottomRight`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoundingBox` | [`feature:gepplate@BoundingBox`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | [`feature:gepplate@color`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `EndRange` | [`feature:gepplate@EndRange`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `HashSpacing` | [`feature:gepplate@HashSpacing`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:gepplate@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelFace` | [`feature:gepplate@LabelFace`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelFont` | [`feature:gepplate@LabelFont`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelsAngle` | [`feature:gepplate@LabelsAngle`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelSize` | [`feature:gepplate@LabelSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelText` | [`feature:gepplate@LabelText`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LineWidth` | [`feature:gepplate@LineWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `MarginWidth` | [`feature:gepplate@MarginWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowBorders` | [`feature:gepplate@ShowBorders`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowScale` | [`feature:gepplate@ShowScale`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `StartRange` | [`feature:gepplate@StartRange`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `SupersededBy` | [`feature:gepplate@SupersededBy`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `TopLeft` | [`feature:gepplate@TopLeft`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `TopRight` | [`feature:gepplate@TopRight`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Transparent` | [`feature:gepplate@Transparent`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `UnitID` | [`feature:gepplate@UnitID`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Visible` | [`feature:gepplate@Visible`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Z` | [`feature:gepplate@Z`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`geplane`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `id` | [`feature:geplane@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelText` | [`feature:geplane@LabelText`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Visible` | [`feature:geplane@Visible`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`gepband`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `alpha` | [`feature:gepband@alpha`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BandValue` | [`feature:gepband@BandValue`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | [`feature:gepband@color`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CurveType` | [`feature:gepband@CurveType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Height` | [`feature:gepband@Height`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:gepband@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ShowValue` | [`feature:gepband@ShowValue`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Visible` | [`feature:gepband@Visible`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Width` | [`feature:gepband@Width`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Z` | [`feature:gepband@Z`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`marker`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `CaptionJustification` | [`feature:marker@CaptionJustification`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | [`feature:marker@color`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `DisplayName` | [`feature:marker@DisplayName`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:marker@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `MarkerAngle` | [`feature:marker@MarkerAngle`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `MarkerOffset` | [`feature:marker@MarkerOffset`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Name` | [`feature:marker@Name`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Persistent` | [`feature:marker@Persistent`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `TagType` | [`feature:marker@TagType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Value` | [`feature:marker@Value`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`stoichiometrygrid`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `alpha` | [`feature:stoichiometrygrid@alpha`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoldWidth` | [`feature:stoichiometrygrid@BoldWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoundingBox` | [`feature:stoichiometrygrid@BoundingBox`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | [`feature:stoichiometrygrid@color`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:stoichiometrygrid@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelFace` | [`feature:stoichiometrygrid@LabelFace`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelFont` | [`feature:stoichiometrygrid@LabelFont`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelSize` | [`feature:stoichiometrygrid@LabelSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LineWidth` | [`feature:stoichiometrygrid@LineWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `MarginWidth` | [`feature:stoichiometrygrid@MarginWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `p` | [`feature:stoichiometrygrid@p`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `SupersededBy` | [`feature:stoichiometrygrid@SupersededBy`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Visible` | [`feature:stoichiometrygrid@Visible`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Z` | [`feature:stoichiometrygrid@Z`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`sgcomponent`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `ComponentIsHeader` | [`feature:sgcomponent@ComponentIsHeader`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ComponentIsReactant` | [`feature:sgcomponent@ComponentIsReactant`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ComponentReferenceID` | [`feature:sgcomponent@ComponentReferenceID`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:sgcomponent@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Visible` | [`feature:sgcomponent@Visible`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Width` | [`feature:sgcomponent@Width`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`sgdatum`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `id` | [`feature:sgdatum@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `IsEdited` | [`feature:sgdatum@IsEdited`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `IsHidden` | [`feature:sgdatum@IsHidden`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `IsReadOnly` | [`feature:sgdatum@IsReadOnly`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `SGDataType` | [`feature:sgdatum@SGDataType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `SGDataValue` | [`feature:sgdatum@SGDataValue`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `SGPropertyType` | [`feature:sgdatum@SGPropertyType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Visible` | [`feature:sgdatum@Visible`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`plasmidmap`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `alpha` | [`feature:plasmidmap@alpha`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoldWidth` | [`feature:plasmidmap@BoldWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoundingBox` | [`feature:plasmidmap@BoundingBox`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | [`feature:plasmidmap@color`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:plasmidmap@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelFace` | [`feature:plasmidmap@LabelFace`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelFont` | [`feature:plasmidmap@LabelFont`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LabelSize` | [`feature:plasmidmap@LabelSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LineWidth` | [`feature:plasmidmap@LineWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `MarginWidth` | [`feature:plasmidmap@MarginWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `NumberBasePairs` | [`feature:plasmidmap@NumberBasePairs`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `p` | [`feature:plasmidmap@p`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `RingRadius` | [`feature:plasmidmap@RingRadius`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `SupersededBy` | [`feature:plasmidmap@SupersededBy`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Visible` | [`feature:plasmidmap@Visible`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Z` | [`feature:plasmidmap@Z`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`plasmidregion`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `alpha` | [`feature:plasmidregion@alpha`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `AngularSize` | [`feature:plasmidregion@AngularSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ArrowheadCenterSize` | [`feature:plasmidregion@ArrowheadCenterSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ArrowheadHead` | [`feature:plasmidregion@ArrowheadHead`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ArrowheadTail` | [`feature:plasmidregion@ArrowheadTail`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ArrowheadType` | [`feature:plasmidregion@ArrowheadType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ArrowheadWidth` | [`feature:plasmidregion@ArrowheadWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ArrowShaftSpacing` | [`feature:plasmidregion@ArrowShaftSpacing`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoundingBox` | [`feature:plasmidregion@BoundingBox`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Center3D` | [`feature:plasmidregion@Center3D`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | [`feature:plasmidregion@color`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `FadePercent` | [`feature:plasmidregion@FadePercent`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `FillType` | [`feature:plasmidregion@FillType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Head3D` | [`feature:plasmidregion@Head3D`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `HeadSize` | [`feature:plasmidregion@HeadSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:plasmidregion@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LineType` | [`feature:plasmidregion@LineType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `MajorAxisEnd3D` | [`feature:plasmidregion@MajorAxisEnd3D`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `MinorAxisEnd3D` | [`feature:plasmidregion@MinorAxisEnd3D`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `RegionEnd` | [`feature:plasmidregion@RegionEnd`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `RegionOffset` | [`feature:plasmidregion@RegionOffset`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `RegionStart` | [`feature:plasmidregion@RegionStart`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Tail3D` | [`feature:plasmidregion@Tail3D`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Z` | [`feature:plasmidregion@Z`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`plasmidmarker`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `CaptionJustification` | [`feature:plasmidmarker@CaptionJustification`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | [`feature:plasmidmarker@color`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `DisplayName` | [`feature:plasmidmarker@DisplayName`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:plasmidmarker@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `MarkerAngle` | [`feature:plasmidmarker@MarkerAngle`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `MarkerOffset` | [`feature:plasmidmarker@MarkerOffset`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Name` | [`feature:plasmidmarker@Name`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Persistent` | [`feature:plasmidmarker@Persistent`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `TagType` | [`feature:plasmidmarker@TagType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Value` | [`feature:plasmidmarker@Value`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`bracketedgroup`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `BracketedObjectIDs` | [`feature:bracketedgroup@BracketedObjectIDs`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BracketUsage` | [`feature:bracketedgroup@BracketUsage`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ComponentOrder` | [`feature:bracketedgroup@ComponentOrder`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:bracketedgroup@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `PolymerFlipType` | [`feature:bracketedgroup@PolymerFlipType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `PolymerRepeatPattern` | [`feature:bracketedgroup@PolymerRepeatPattern`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `RepeatCount` | [`feature:bracketedgroup@RepeatCount`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `SRULabel` | [`feature:bracketedgroup@SRULabel`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`bracketattachment`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `GraphicID` | [`feature:bracketattachment@GraphicID`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:bracketattachment@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`crossingbond`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `BondID` | [`feature:crossingbond@BondID`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:crossingbond@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `InnerAtomID` | [`feature:crossingbond@InnerAtomID`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`border`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `alpha` | [`feature:border@alpha`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | [`feature:border@color`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:border@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LineType` | [`feature:border@LineType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LineWidth` | [`feature:border@LineWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Side` | [`feature:border@Side`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Z` | [`feature:border@Z`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`chemicalproperty`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `BasisObjects` | [`feature:chemicalproperty@BasisObjects`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ChemicallySignificant` | [`feature:chemicalproperty@ChemicallySignificant`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ChemicalPropertyDisplayID` | [`feature:chemicalproperty@ChemicalPropertyDisplayID`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ChemicalPropertyIsActive` | [`feature:chemicalproperty@ChemicalPropertyIsActive`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ChemicalPropertyType` | [`feature:chemicalproperty@ChemicalPropertyType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ExternalBonds` | [`feature:chemicalproperty@ExternalBonds`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:chemicalproperty@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Name` | [`feature:chemicalproperty@Name`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `PositioningAngle` | [`feature:chemicalproperty@PositioningAngle`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `PositioningOffset` | [`feature:chemicalproperty@PositioningOffset`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `PositioningType` | [`feature:chemicalproperty@PositioningType`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`bioshape`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `alpha` | [`feature:bioshape@alpha`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BioShapeType` | [`feature:bioshape@BioShapeType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoldWidth` | [`feature:bioshape@BoldWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoundingBox` | [`feature:bioshape@BoundingBox`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | [`feature:bioshape@color`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CylinderDistance` | [`feature:bioshape@CylinderDistance`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CylinderHeight` | [`feature:bioshape@CylinderHeight`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `CylinderWidth` | [`feature:bioshape@CylinderWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `DNAWaveHeight` | [`feature:bioshape@DNAWaveHeight`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `DNAWaveLength` | [`feature:bioshape@DNAWaveLength`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `DNAWaveOffset` | [`feature:bioshape@DNAWaveOffset`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `DNAWaveWidth` | [`feature:bioshape@DNAWaveWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `EnzymeHeight` | [`feature:bioshape@EnzymeHeight`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `EnzymeReceptorSize` | [`feature:bioshape@EnzymeReceptorSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `EnzymeWidth` | [`feature:bioshape@EnzymeWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `FadePercent` | [`feature:bioshape@FadePercent`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `FillType` | [`feature:bioshape@FillType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `GolgiHeight` | [`feature:bioshape@GolgiHeight`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `GolgiLength` | [`feature:bioshape@GolgiLength`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `GolgiWidth` | [`feature:bioshape@GolgiWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `GproteinLowerHeight` | [`feature:bioshape@GproteinLowerHeight`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `GproteinUpperHeight` | [`feature:bioshape@GproteinUpperHeight`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `HashSpacing` | [`feature:bioshape@HashSpacing`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `HelixProteinExtra` | [`feature:bioshape@HelixProteinExtra`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:bioshape@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ImmunoglobinHeight` | [`feature:bioshape@ImmunoglobinHeight`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `ImmunoglobinWidth` | [`feature:bioshape@ImmunoglobinWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LineType` | [`feature:bioshape@LineType`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LineWidth` | [`feature:bioshape@LineWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `MajorAxisEnd3D` | [`feature:bioshape@MajorAxisEnd3D`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `MembraneElementSize` | [`feature:bioshape@MembraneElementSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `MembraneEndAngle` | [`feature:bioshape@MembraneEndAngle`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `MembraneMajorAxisSize` | [`feature:bioshape@MembraneMajorAxisSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `MembraneMinorAxisSize` | [`feature:bioshape@MembraneMinorAxisSize`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `MembraneStartAngle` | [`feature:bioshape@MembraneStartAngle`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `MinorAxisEnd3D` | [`feature:bioshape@MinorAxisEnd3D`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `NeckHeight` | [`feature:bioshape@NeckHeight`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `NeckWidth` | [`feature:bioshape@NeckWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `PipeWidth` | [`feature:bioshape@PipeWidth`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `SupersededBy` | [`feature:bioshape@SupersededBy`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Visible` | [`feature:bioshape@Visible`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `xyz` | [`feature:bioshape@xyz`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Z` | [`feature:bioshape@Z`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`annotation`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `Content` | [`feature:annotation@Content`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:annotation@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Keyword` | [`feature:annotation@Keyword`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`rlogicitem`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `id` | [`feature:rlogicitem@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `RLogicGroup` | [`feature:rlogicitem@RLogicGroup`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `RLogicIfThenGroup` | [`feature:rlogicitem@RLogicIfThenGroup`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `RLogicOccurrence` | [`feature:rlogicitem@RLogicOccurrence`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `RLogicRestH` | [`feature:rlogicitem@RLogicRestH`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`rlogic`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `alpha` | [`feature:rlogic@alpha`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `BoundingBox` | [`feature:rlogic@BoundingBox`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | [`feature:rlogic@color`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:rlogic@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `LineHeight` | [`feature:rlogic@LineHeight`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `p` | [`feature:rlogic@p`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `Z` | [`feature:rlogic@Z`](../../tests/coverage/test_full_schema_feature_evidence.py) |

### XML 所属标签：`coloredmoleculararea`

| XML 属性 | 特性 ID / 测试源码 |
| --- | --- |
| `BasisObjects` | [`feature:coloredmoleculararea@BasisObjects`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `bgcolor` | [`feature:coloredmoleculararea@bgcolor`](../../tests/coverage/test_full_schema_feature_evidence.py) |
| `id` | [`feature:coloredmoleculararea@id`](../../tests/coverage/test_full_schema_feature_evidence.py) |
