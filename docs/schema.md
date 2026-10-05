# Canonical schema and compiler

English | [简体中文](zh-CN/schema.md)

Canonical files live in `schema/canonical/`; source manifests and notes live in
`schema/sources/`; reviewed compatibility exceptions belong in
`schema/overrides/`. The compiler converts YAML into frozen, slotted Python IR
objects. No runtime package module loads YAML.

The canonical schema generates a thin static model for every one of the 53
declarations in the pinned DTD, including `CDXMLRoot`, XML-only constructs,
and the 15 declared tags absent from the SDK object inventory. The generated
models expose all 762 DTD owner/attribute pairs. Twenty additional SDK XML
attributes and three Curve case aliases are tracked as a separate extension
set. Source references and schema status describe evidence, not ChemDraw
acceptance; runtime behavior and test coverage are summarized separately in
[coverage](coverage.md).

Every object definition declares an explicit ID scope (`document`, `local`, or
`none`). Drawing/document objects use document scope; Font IDs are scoped to
their FontTable; tables, text runs, and color rows have no object-ID scope.
Shared binary properties are represented once with an explicit owner list.
Properties stored as character data (`TextRun.content` and direct lexical
`Spectrum.data`) declare text storage rather than pretending to be XML
attributes. String enums may omit numeric CDX values when the SDK does not
document them. A DTD `CDATA` field is not upgraded to a richer semantic type
without source evidence; known points, references, enums, lists, and
context-dependent ObjectTag values use their explicit codecs.

CDX object/property IDs are included only when directly supported by source
evidence. XML `id` attributes do not automatically imply CDX object IDs or
global ID scope. The schema lock hashes canonical inputs and records external
source digests only when source bytes are actually available locally.

Run `python -m tools.schema_compiler check`, `build`, or `coverage` from the
repository root. Generation is deterministic and generated files are maintained
under `src/cdxml_om/_generated/`; schema changes should commit their generated
artifacts alongside the canonical update. Static metadata is semantically organized in
`_generated/_metadata/`: one module per object and enum, property groups by
logical owner (with common property specs defined once), and provenance grouped
by source. `schema_metadata.py` remains a small compatibility facade. There
are no numbered size-based shards and no runtime schema/JSON/YAML loading.
Generation sorts imports and formats generated Python with Ruff from the
development extra; Ruff remains a development dependency and is not required
to use the runtime package. For offline DTD/SDK evidence import and candidate
diffs, see the [schema ingestion guide](ingestion.md).
