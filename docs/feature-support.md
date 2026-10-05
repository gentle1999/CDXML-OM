# Feature support

English | [简体中文](zh-CN/feature-support.md)

This page describes what the current Python API can do. It is separate from
the [coverage methodology](coverage.md), which explains how mapping and test
evidence are counted.

## Source-qualified scope

The accepted fresh source-bound evidence run dated **2026-10-05** reports:

| Feature set | Implemented and typed | Tested | Round-trip verified |
| --- | ---: | ---: | ---: |
| Pinned DTD elements | 53/53 | 53/53 | 53/53 |
| Pinned DTD owner/attribute pairs | 762/762 | 762/762 | 762/762 |
| PCDATA features (`s`, `spectrum`) | 2/2 | 2/2 | 2/2 |
| SDK extension pairs (20 additional XML pairs + 3 aliases) | 23/23 | 23/23 | 23/23 |

The pinned Revvity DTD SHA-256 is
`5311978e514ffe154108540c3634c314dc66031a4f3c877a681fc6dca8e128c2`. These
percentages mean 100% of the explicitly enumerated pinned-source feature scope
has a typed implementation and passing feature-level read/write/mutation and
serialize/reload evidence. They do **not** mean 100% DTD grammar conformance or
ChemDraw interoperability. `ChemDrawVerified` remains **0**: no independently
captured ChemDraw application verification artifact and observation were
available for the accepted run.

Separate from that source-bound coverage snapshot, the user reports that six
current visual samples opened normally in Windows ChemDraw Professional
25.5.0.5789, while an earlier curve payload produced “vector too long”. The
curve candidate has since changed and awaits retest; these observations do not
change `ChemDrawVerified=0`. See the [manual sample log](../examples/render_samples/README.md).

The DTD has 53 declarations including the `CDXML` root. `UnknownElement` is a
generic fallback for undeclared XML tags and is not a 54th DTD model.
`CDXMLDocument` is the handwritten document facade; the root itself wraps as
the generated `CDXMLRoot` model.

## DTD element models

Each row gives the exact case-sensitive XML tag and its public model class.
The third column links to the lifecycle round-trip case for that tag. The
groups are for navigation only; they do not imply extra chemical semantics.

### Document, page layout, and rich text

| XML tag | Public model | Round-trip test (`test_full_schema_feature_evidence.py`) |
| --- | --- | --- |
| `CDXML` | `CDXMLRoot` | [`feature-element:CDXML`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `page` | `Page` | [`feature-element:page`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `fragment` | `Fragment` | [`feature-element:fragment`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `group` | `Group` | [`feature-element:group`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `templategrid` | `TemplateGrid` | [`feature-element:templategrid`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `t` | `Text` | [`feature-element:t`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `s` | `TextRun` | [`feature-element:s`](../tests/coverage/test_full_schema_feature_evidence.py) |

### Chemical graph, drawing, and XML references

| XML tag | Public model | Round-trip test (`test_full_schema_feature_evidence.py`) |
| --- | --- | --- |
| `n` | `Node` | [`feature-element:n`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `b` | `Bond` | [`feature-element:b`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `arrow` | `Arrow` | [`feature-element:arrow`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `graphic` | `Graphic` | [`feature-element:graphic`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `curve` | `Curve` | [`feature-element:curve`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `embeddedobject` | `EmbeddedObject` | [`feature-element:embeddedobject`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `objecttag` | `ObjectTag` | [`feature-element:objecttag`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `border` | `Border` | [`feature-element:border`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `table` | `Table` | [`feature-element:table`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `splitter` | `Splitter` | [`feature-element:splitter`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `crossingbond` | `CrossingBond` | [`feature-element:crossingbond`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `crossreference` | `CrossReference` | [`feature-element:crossreference`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `altgroup` | `AltGroup` | [`feature-element:altgroup`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `bracketedgroup` | `BracketedGroup` | [`feature-element:bracketedgroup`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `bracketattachment` | `BracketAttachment` | [`feature-element:bracketattachment`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `represent` | `Represent` | [`feature-element:represent`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `regnum` | `RegistryNumber` | [`feature-element:regnum`](../tests/coverage/test_full_schema_feature_evidence.py) |

### Reactions

| XML tag | Public model | Round-trip test (`test_full_schema_feature_evidence.py`) |
| --- | --- | --- |
| `scheme` | `ReactionScheme` | [`feature-element:scheme`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `step` | `ReactionStep` | [`feature-element:step`](../tests/coverage/test_full_schema_feature_evidence.py) |

### Resource tables

| XML tag | Public model | Round-trip test (`test_full_schema_feature_evidence.py`) |
| --- | --- | --- |
| `fonttable` | `FontTable` | [`feature-element:fonttable`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `font` | `Font` | [`feature-element:font`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `colortable` | `ColorTable` | [`feature-element:colortable`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `color` | `Color` | [`feature-element:color`](../tests/coverage/test_full_schema_feature_evidence.py) |

### Geometry, annotations, and spectra

| XML tag | Public model | Round-trip test (`test_full_schema_feature_evidence.py`) |
| --- | --- | --- |
| `annotation` | `Annotation` | [`feature-element:annotation`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `chemicalproperty` | `ChemicalProperty` | [`feature-element:chemicalproperty`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `coloredmoleculararea` | `ColoredMolecularArea` | [`feature-element:coloredmoleculararea`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `constraint` | `Constraint` | [`feature-element:constraint`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `geometry` | `Geometry` | [`feature-element:geometry`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `marker` | `Marker` | [`feature-element:marker`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `spectrum` | `Spectrum` | [`feature-element:spectrum`](../tests/coverage/test_full_schema_feature_evidence.py) |

### Biological and sequence records

| XML tag | Public model | Round-trip test (`test_full_schema_feature_evidence.py`) |
| --- | --- | --- |
| `bioshape` | `BioShape` | [`feature-element:bioshape`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `plasmidmap` | `PlasmidMap` | [`feature-element:plasmidmap`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `plasmidmarker` | `PlasmidMarker` | [`feature-element:plasmidmarker`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `plasmidregion` | `PlasmidRegion` | [`feature-element:plasmidregion`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `sequence` | `Sequence` | [`feature-element:sequence`](../tests/coverage/test_full_schema_feature_evidence.py) |

### GEP, TLC, and stoichiometry records

| XML tag | Public model | Round-trip test (`test_full_schema_feature_evidence.py`) |
| --- | --- | --- |
| `gepband` | `GEPBand` | [`feature-element:gepband`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `geplane` | `GEPLane` | [`feature-element:geplane`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `gepplate` | `GEPPlate` | [`feature-element:gepplate`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `tlclane` | `TLCLane` | [`feature-element:tlclane`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `tlcplate` | `TLCPlate` | [`feature-element:tlcplate`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `tlcspot` | `TLCSpot` | [`feature-element:tlcspot`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `stoichiometrygrid` | `StoichiometryGrid` | [`feature-element:stoichiometrygrid`](../tests/coverage/test_full_schema_feature_evidence.py) |

### Logic and structure-group records

| XML tag | Public model | Round-trip test (`test_full_schema_feature_evidence.py`) |
| --- | --- | --- |
| `rlogic` | `RLogic` | [`feature-element:rlogic`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `rlogicitem` | `RLogicItem` | [`feature-element:rlogicitem`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `sgcomponent` | `SGComponent` | [`feature-element:sgcomponent`](../tests/coverage/test_full_schema_feature_evidence.py) |
| `sgdatum` | `SGDatum` | [`feature-element:sgdatum`](../tests/coverage/test_full_schema_feature_evidence.py) |

The 15 declarations absent from the SDK's object inventory still have
DTD-backed XML models. This inventory absence does not make them unknown. The
pinned DTD's `altgroup` content model mentions an undeclared `bracket` child;
`<bracket>` remains an `UnknownElement` unless new source evidence defines it.

## XML attributes outside the DTD

The separately measured SDK extension set contains 23 typed, round-trip-tested pairs: 20 exact owner/attribute pairs documented in the archived SDK but absent from the pinned DTD, plus three Curve casing aliases. Each row links to its exact parameterized test source:

| Owner tag | XML attribute | Typed round-trip case (`test_sdk_extension_feature_evidence.py`) |
| --- | --- | --- |
| `n` | `bgcolor` | [`test_sdk_extension_typed_mutation_roundtrip[feature-sdk:n@bgcolor]`](../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `b` | `bgcolor` | [`test_sdk_extension_typed_mutation_roundtrip[feature-sdk:b@bgcolor]`](../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `graphic` | `bgcolor` | [`test_sdk_extension_typed_mutation_roundtrip[feature-sdk:graphic@bgcolor]`](../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `curve` | `bgcolor` | [`test_sdk_extension_typed_mutation_roundtrip[feature-sdk:curve@bgcolor]`](../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `embeddedobject` | `bgcolor` | [`test_sdk_extension_typed_mutation_roundtrip[feature-sdk:embeddedobject@bgcolor]`](../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `table` | `bgcolor` | [`test_sdk_extension_typed_mutation_roundtrip[feature-sdk:table@bgcolor]`](../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `altgroup` | `bgcolor` | [`test_sdk_extension_typed_mutation_roundtrip[feature-sdk:altgroup@bgcolor]`](../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `spectrum` | `bgcolor` | [`test_sdk_extension_typed_mutation_roundtrip[feature-sdk:spectrum@bgcolor]`](../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `tlcplate` | `bgcolor` | [`test_sdk_extension_typed_mutation_roundtrip[feature-sdk:tlcplate@bgcolor]`](../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `geometry` | `BondLength` | [`test_sdk_extension_typed_mutation_roundtrip[feature-sdk:geometry@BondLength]`](../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `constraint` | `BondLength` | [`test_sdk_extension_typed_mutation_roundtrip[feature-sdk:constraint@BondLength]`](../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `geometry` | `LabelFont` | [`test_sdk_extension_typed_mutation_roundtrip[feature-sdk:geometry@LabelFont]`](../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `constraint` | `LabelFont` | [`test_sdk_extension_typed_mutation_roundtrip[feature-sdk:constraint@LabelFont]`](../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `geometry` | `LabelSize` | [`test_sdk_extension_typed_mutation_roundtrip[feature-sdk:geometry@LabelSize]`](../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `constraint` | `LabelSize` | [`test_sdk_extension_typed_mutation_roundtrip[feature-sdk:constraint@LabelSize]`](../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `geometry` | `LabelFace` | [`test_sdk_extension_typed_mutation_roundtrip[feature-sdk:geometry@LabelFace]`](../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `constraint` | `LabelFace` | [`test_sdk_extension_typed_mutation_roundtrip[feature-sdk:constraint@LabelFace]`](../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `geometry` | `LabelColor` | [`test_sdk_extension_typed_mutation_roundtrip[feature-sdk:geometry@LabelColor]`](../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `constraint` | `LabelColor` | [`test_sdk_extension_typed_mutation_roundtrip[feature-sdk:constraint@LabelColor]`](../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `geometry` | `PointIsDirected` | [`test_sdk_extension_typed_mutation_roundtrip[feature-sdk:geometry@PointIsDirected]`](../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `curve` | `ArrowHeadType` | [`test_sdk_extension_typed_mutation_roundtrip[feature-sdk:curve@ArrowHeadType]`](../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `curve` | `ArrowHeadHead` | [`test_sdk_extension_typed_mutation_roundtrip[feature-sdk:curve@ArrowHeadHead]`](../tests/coverage/test_sdk_extension_feature_evidence.py) |
| `curve` | `ArrowHeadTail` | [`test_sdk_extension_typed_mutation_roundtrip[feature-sdk:curve@ArrowHeadTail]`](../tests/coverage/test_sdk_extension_feature_evidence.py) |

The SDK spells three Curve properties with a different case than the DTD:
`ArrowHeadType`, `ArrowHeadHead`, and `ArrowHeadTail`; these are aliases for
the canonical DTD attributes `ArrowheadType`, `ArrowheadHead`, and
`ArrowheadTail`. Alias conflicts are reported rather than silently normalized.
These 20 additional pairs plus three aliases are measured separately from the 762 DTD pairs. The catalog is [`sdk_extension_cases.json`](../tests/coverage/sdk_extension_cases.json).


## Feature-to-test traceability

- **53 element models:** the inventory above links each tag's `feature-element:<tag>` case ID to the test source. The 52 non-root tags use
  `test_element_create_remove_round_trip[feature-element:<tag>]`; `CDXML` uses the separate
  `test_root_creation_mutation_round_trip[feature-element:CDXML]` case. The catalog is
  [`feature_cases.json`](../tests/coverage/feature_cases.json).
- **762 DTD owner/attribute pairs:** every pair has a distinct catalog ID and a typed parse/read,
  mutation, serialization, and reload case. See the complete owner-grouped
  [DTD attribute round-trip test index](feature-tests.md). All cases use
  `tests/coverage/test_full_schema_feature_evidence.py::test_mapped_pair_parse_read_mutate_serialize_reload`;
  for example, `feature:n@Element` is the node
  `test_mapped_pair_parse_read_mutate_serialize_reload[feature:n@Element]`.
- **2 PCDATA features:** `s` and `spectrum` have separate cases in the same parameterized test.

  | XML tag | Feature ID | Round-trip test source |
  | --- | --- | --- |
  | `s` | [`feature-character:s`](../tests/coverage/test_full_schema_feature_evidence.py) | [`test_character_data_parse_read_mutate_serialize_reload`](../tests/coverage/test_full_schema_feature_evidence.py) |
  | `spectrum` | [`feature-character:spectrum`](../tests/coverage/test_full_schema_feature_evidence.py) | [`test_character_data_parse_read_mutate_serialize_reload`](../tests/coverage/test_full_schema_feature_evidence.py) |

- **23 SDK extension pairs:** the table above lists every `feature-sdk:<owner>@<attribute>` case ID.
  They use `tests/coverage/test_sdk_extension_feature_evidence.py::test_sdk_extension_typed_mutation_roundtrip`.

In the accepted fresh run, every applicable listed row has a current passed JUnit round-trip case.
This does not mean every lexical value, possible combination, or all ChemDraw semantics were tested.
See the [coverage methodology](coverage.md) for how current test evidence is counted.

## Working API capabilities

- **Parse and serialize:** `CDXMLDocument.from_string()` and `.from_file()`
  parse local XML; `.to_string()` and `.to_file()` write the retained tree.
  Parser configuration disables network access, DTD loading, and external
  entity resolution. Serialization preserves XML structure and unknown
  content, but is not byte-for-byte source preservation.
- **Typed navigation and identity:** exact XML tags select generated wrappers;
  repeated wrapping of the same `lxml` element returns the same wrapper.
  `document.find(Model)` searches for a public model. Generic unknown elements
  remain navigable through `UnknownElement`/`CDXMLElement`.
- **Collections and lookup:** navigate through `document.pages`,
  `page.fragments`, `fragment.nodes`, and `fragment.bonds`. Collections support
  iteration, `len()`, indexing, and `.all()`; parent collections provide
  `.create()`/`.remove()`. `document.get(Node, object_id)` returns `None` when
  there is no matching object (or it is not a `Node`); duplicate matching IDs
  raise `ReferenceResolutionError` rather than choosing a target. Raw XML
  attributes and elements remain inspectable through the wrappers.
- **Typed values and mutation:** generated fields cover source-supported
  strings, booleans, numbers, enums, points, bounding boxes, lists, and
  references. Irregular XML codecs cover point arrays, list values, bond-order
  flags, and context-dependent `ObjectTag.Value`. Reads are lazy and do not
  rewrite untouched lexical values.
- **Child collections:** parent-owned collections support typed create/remove
  where the DTD declares a route. Mutation preserves wrapper identity and
  does not cascade-delete or rewrite references. A temporary tree may violate
  minimum child cardinality; `validate()` reports it so the caller can repair
  the tree.
- **IDs and references:** document-scoped IDs are allocated without collision
  with currently observed IDs. Font IDs are table-local; color rows and text
  runs have no object ID. `Bond.begin` and `Bond.end` are typed `Node`
  references. `ReactionStep.reactants`, `.products`, and `.arrows` are
  reference arrays over modeled document objects rather than fixed chemical
  roles; dangling or ambiguous links are reported and not guessed.
- **Rich text and spectrum text:** `TextRun.content` edits are rejected when
  child nodes are present, protecting opaque mixed content. `Spectrum.data` is
  raw direct PCDATA (`element.text` plus direct child tails), not a parsed
  numeric spectrum array. `Text.plain_text` is a convenience concatenation of
  descendant text-run content.
- **Font and color tables:** document helpers expose/create the optional root
  tables, and table-owned collections expose `Font` and `Color` rows. Font IDs
  are local to a FontTable; color rows do not have IDs. Font/color indices in
  other elements are not resolved to `Font`/`Color` wrappers and are not
  remapped automatically.
- **Validation:** `document.validate()` returns structured findings for
  supported required fields, typed values/references, ID scopes, known parent
  routes, and child cardinality. It does not reject parsing or mutate the tree.

`CDATA` mapped to `str` means the raw XML lexical value is available as text; it
does not promise chemistry interpretation, units, an application default, or a
binary CDX encoding. Richer types are used where the pinned DTD and reviewed
source evidence establish an XML contract.

## Explicit limits

- The coverage result is scoped to the pinned DTD, reviewed SDK XML extensions,
  and tested API operations. It does not prove conformance to every DTD
  sequence/choice grammar or to every CDXML revision/vendor extension.
- `validate()` is not a chemical correctness validator. No bond, structure,
  reaction, or spectrum meaning is inferred beyond the documented typed XML
  contract.
- Spectrum PCDATA is lexical text; no numeric sample token grammar is claimed.
- Unknown XML is retained, not upgraded into a typed model. In particular the
  undeclared `bracket` token does not create a model class.
- There is no binary CDX reader/writer, automatic reference cascade, automatic
  font/color index resolution/remapping, or ChemDraw application verification.
- XML structure is retained, but output bytes and all lexical formatting are
  not guaranteed to match the input byte-for-byte.

## Reproduce the feature evidence

Create a new evidence directory outside the repository so an old JUnit file
cannot be mistaken for a current run:

```sh
evidence_dir="$(mktemp -d "${TMPDIR:-/tmp}/cdxml-om-feature-run.XXXXXX")"
uv run python -m tools.schema_compiler test-features \
  --run-evidence "$evidence_dir/feature-run.json" \
  --junitxml "$evidence_dir/feature-run.xml" -- tests/coverage
uv run python -m tools.schema_compiler coverage \
  --test-run "$evidence_dir/feature-run.json" --format text
```

The JUnit report and evidence sidecar bind test outcomes to current source,
schema, overrides, fixtures, and feature catalogs. A later relevant edit makes
that saved run stale; repeat the command after changes. The independent catalogs
are [`feature_cases.json`](../tests/coverage/feature_cases.json) and
[`sdk_extension_cases.json`](../tests/coverage/sdk_extension_cases.json). The
[coverage guide](coverage.md) explains all report stages; the
[specification baseline](specification-baseline.md) records source facts and
unresolved disagreements.
