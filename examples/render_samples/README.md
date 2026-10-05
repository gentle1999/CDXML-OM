# Visual samples and diagnostic probes

English | [简体中文](README.zh-CN.md)

These samples and probes follow the user's reported ChemDraw observations. They
were generated through CDXML-OM's typed document and collection APIs using the
accepted `mol1` fixture's Arial/Times fonts, standard color table, page style,
and 30-point bond length as a starting reference. The generator removes the
source `CreationProgram`, document name, old page, old viewport, and print
cropping fields; it does not claim that these files were created by ChemDraw.

The user reports opening these files in Windows ChemDraw Professional
25.5.0.5789: the six files in the table below opened and rendered normally; an
earlier `probe_curve_points.cdxml` payload produced “vector too long”. No
screenshots or independently reproducible application artifact were provided.
The curve file has since been regenerated with a different payload and is
pending user retest. Passing CDXML-OM validation is only a structural check.
When retesting, record the ChemDraw version, filename, zoom, and any error or
warning dialogs; compare the original six files at the same view settings.

The following SHA-256 values identify the six files covered by the user's
normal-rendering report. They record which bytes were reported, not an
independent application-verification artifact.

| File | SHA-256 |
| --- | --- |
| `01_before_after.cdxml` | `964a3a13e65ed5b2206deac62467860bac992403853f463ea8b2c3cb7d167715` |
| `02_reaction_and_resources.cdxml` | `04438a51a15e4f0e009a1f5765f5b73e76bdd705d5a9ca2b72e1b9b85ac0b1d3` |
| `03_unknown_preservation.cdxml` | `420791e8c34b1cdcf602109ba28cecd634f27766f57584a4494aac1c12a65fd7` |
| `probe_element_generic_lists.cdxml` | `d4f28d9375ae7ba35a3470256af0c31fe4bc3ef7ce2635950e53124eac8f5234` |
| `probe_spectrum_missing_required_fields.cdxml` | `a04e5a5fb96ad2b98c322ea1239b092c1a215575087cb90b738c7722e2edcce9` |
| `probe_spectrum_sdk_required_fields.cdxml` | `8495b38484ca2545555cfd21569eada5f5555ec333a74e2168cb3647bf59e8d8` |

## Readable scene candidates

| File | Intended inspection |
| --- | --- |
| [`01_before_after.cdxml`](01_before_after.cdxml) | Clearly separated before C–C and after C=C–O drawings. The after copy changes the original bond order, creates a node, changes its element to O, and creates a bond. This is a drawing/edit demonstration, not a reaction prediction. |
| [`02_reaction_and_resources.cdxml`](02_reaction_and_resources.cdxml) | Arial/Times rich text, a rectangle, a standard arrow, two fragments, and a ReactionStep whose reactant/product/arrow references target those exact objects. It contains no Spectrum, Curve, or list payload. |
| [`03_unknown_preservation.cdxml`](03_unknown_preservation.cdxml) | A readable C–O drawing with one unknown vendor attribute and one namespaced extension retained in the XML. ChemDraw may ignore or reject the extension. |

Atom labels are child `<t><s>` runs using font ID `3` (Arial); the inherited
mol1 resource table contains Arial at ID `3` and Times New Roman at ID `4`.
The source SDK documents ForegroundColor as a two-based color-table index: `3`
selects the second palette entry (black), and `4` the third (red). The samples
do not treat the earlier examples' color index `0` as a new RGB row. [Pinned source facts](../../schema/sources/sdk/focused-properties.json)
and the [ForegroundColor SDK page](https://chemapps.stolaf.edu/iupac/cdx/sdk/properties/ForegroundColor.htm)
describe these boundaries.

## Isolated probes

These small files are diagnostic hypotheses, not polished structures or
claims of ChemDraw-valid syntax. Try the three scene candidates first, then
open each probe separately and record which file changes the application
behavior:

| File | Isolated payload and evidence boundary |
| --- | --- |
| [`probe_curve_points.cdxml`](probe_curve_points.cdxml) | The previous two-point 2D+3D payload (SHA-256 `abb94c07688e56763deb6a73e57bccc69cc6f60d69758f9b54b60525ef39d28c`) produced “vector too long” in the user's report. The current candidate is a page-level, open curve with a bounding box and nine 2D points; it omits optional 3D points and has not yet been retested. |
| [`probe_element_generic_lists.cdxml`](probe_element_generic_lists.cdxml) | Uses `ElementList="NOT 6 8"` and `GenericList="alpha beta"`. The user reports this file opens and renders normally; that observation does not independently establish the chemical meaning of these tokens. The SDK describes whitespace-separated values and an optional `NOT` prefix (examples: `NOT 9 17 35` and `NOT R X A`). |
| [`probe_spectrum_missing_required_fields.cdxml`](probe_spectrum_missing_required_fields.cdxml) | Uses Spectrum fields and lexical `400 0.2 500 0.5` payload, which is not asserted to be a valid numeric sample encoding. It omits `BoundingBox` and `XSpacing`, as the earlier example did. |
| [`probe_spectrum_sdk_required_fields.cdxml`](probe_spectrum_sdk_required_fields.cdxml) | Same Spectrum payload and other fields as the preceding probe; adds only `BoundingBox` and `XSpacing`. The [archived SDK Spectrum object page](https://chemapps.stolaf.edu/iupac/cdx/sdk/Spectrum.htm) marks `BoundingBox`, `XLow`, and `XSpacing` required, whereas the pinned DTD marks these attributes optional. `XLow` is present in both probes. The field difference isolates that source discrepancy; it does not validate the PCDATA syntax. |

The current curve candidate's point order is derived from curve `80755` in the
pinned [RDKit specimen at commit `d1985caa`](https://github.com/rdkit/rdkit/blob/d1985caaa79f6f5d803966a5f4bed69e0c6ef2bc/Code/GraphMol/test_data/CDXML/chemdraw_template5.cdxml),
then uniformly scaled and translated onto this page. This is one specimen, not
a universal control-point-count rule; the source fixture license is retained in
the [corpus](../../tests/fixtures/corpus/RDKit-LICENSE.txt). The SDK describes
Curve as a Bezier curve and marks `CurvePoints` required while `CurvePoints3D`
is optional ([Curve](https://chemapps.stolaf.edu/iupac/cdx/sdk/Curve.htm),
[Curve_Points](https://chemapps.stolaf.edu/iupac/cdx/sdk/properties/Curve_Points.htm),
[Curve_Points3D](https://chemapps.stolaf.edu/iupac/cdx/sdk/properties/Curve_Points3D.htm)).
The XML point array has no binary count prefix; the SDK datatype page's binary
count field is not an instruction to add one to CDXML
([CDXCurvePoints](https://chemapps.stolaf.edu/iupac/cdx/sdk/DataType/CDXCurvePoints.htm)).
The new candidate remains unverified by ChemDraw; save any document currently
being edited before trying probes one at a time. The relevant checked-in facts are `curve_point_arrays`,
`element_generic_and_formula_lists`, and `spectrum_data_is_pcdata` in
[`focused-properties.json`](../../schema/sources/sdk/focused-properties.json).
The SDK says Spectrum data is stored as CDXML PCDATA, but the available source
does not define a numeric separator/encoding. Do not interpret the probe's
lexical text as confirmed spectrum samples. These probes are not grounds to
change a codec unless reproducible application evidence and source facts
identify a concrete encoding defect.

## Regenerate samples

From the repository root, build the samples with the current installed
runtime. The default command refuses to overwrite existing files. Use a new
directory for another run, or pass `--update` to replace only the seven
filenames owned by this generator in `examples/render_samples/`:

```bash
sample_out="$(mktemp -d "${TMPDIR:-/tmp}/cdxml-om-samples.XXXXXX")"
uv run --no-sync python -m tools.build_visual_samples --output-dir "$sample_out"
uv run --no-sync python -m tools.build_visual_samples --update
```

The first command writes to a new directory. The final command explicitly
regenerates the seven managed files in the repository sample directory.

The generator protects notebook sources and the source corpus. It does not use
desktop automation. The application observations above remain user-reported
and are not ChemDraw verification.
