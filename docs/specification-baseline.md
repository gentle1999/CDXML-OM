# CDXML specification evidence baseline

English | [简体中文](zh-CN/specification-baseline.md)

This document describes the pinned source facts used to expand the object model.
The catalogs are evidence, not generated canonical schema: `schema/sources/sdk/evidence.json`
reconciles the checked-in Revvity DTD with the historical CambridgeSoft SDK, and
`schema/sources/sdk/focused-properties.json` records selected value and encoding
details. The schema/compiler/runtime must consume reviewed mappings rather than
automatically importing these catalogs as canonical behavior.

## Denominators and inventory

The pinned DTD is identified by SHA-256
`5311978e514ffe154108540c3634c314dc66031a4f3c877a681fc6dca8e128c2`. It declares
53 elements including the `CDXML` root (52 nonroot tags) and 762
owner/attribute pairs. Attribute declaration facts preserve the DTD's lexical
type, required status, default kind/value, and enumeration values exactly.

The archived `AllCDXObjects.htm` inventory has 38 rows: 32 `object` namespace
rows, three `property` namespace rows (`colortable`, `fonttable`, `represent`),
and three rows without CDX IDs (`color`, `font`, `s`). The SDK inventory includes
the `CDXML` Document object (`0x8000`); that numeric object-tag value is not an
XML `id`. The DTD has no `CDXML id` attribute.

The detailed SDK object tables provide 410 exact owner-name/attribute-name
matches. A missing exact match is not treated as evidence that a DTD attribute
is unsupported. No owner or attribute names are case-folded. The catalogs
classify, separately:

- 20 documented XML attributes that are absent from the pinned DTD;
- three curve property names whose SDK casing differs from the DTD spelling;
- two XML child elements (`fonttable` and `colortable`) backed by CDX properties;
- six `(not used)` binary property row groups that are not XML attributes; and
- 15 DTD-declared tags with no SDK inventory entry.

The 15 unmapped declarations are `annotation`, `bioshape`,
`coloredmoleculararea`, `gepband`, `geplane`, `gepplate`, `marker`,
`plasmidmap`, `plasmidmarker`, `plasmidregion`, `rlogic`, `rlogicitem`,
`sgcomponent`, `sgdatum`, and `stoichiometrygrid`. The SDK-only XML attributes
are factual union-baseline additions, not members of the DTD's 762-pair
denominator. Their owner, CDXML name, CDX property ID/constant/type, and source
locator are recorded in the catalog. These 15 declarations are DTD-backed XML
models with typed attributes and declared child routes; their lack of a binary
object inventory entry does not make them generic unknown elements. DTD
`CDATA` fields for which no richer XML contract is established remain lexical
strings, and no CDX object tag is fabricated for these declarations.

## Source-specific edge cases

The root `CDXML` tag maps to the SDK Document object (object tag `0x8000`), but
it does not carry an XML `id`. The SDK Node object page labels its historical
`n id` property `UINT16`; the generic `CDXObjectID` datatype page says
references use `UINT32`. Both source claims are preserved separately. The
generic datatype page also describes closest-object resolution for ambiguous
IDs; the runtime intentionally keeps its stricter ambiguity rejection rather
than adopting that historical heuristic.

The DTD content model for `altgroup` at line 410 references a `bracket` child,
but the pinned DTD has no `bracket` element declaration. The SDK
`NamedAltGroup` subobject table lists `group`, `fragment`, `t`, and `objecttag`,
not `bracket`. This remains an unresolved source anomaly; neither side is
silently corrected and it does not change the 53/762 denominator.

The archived SDK `Curve` property table also assigns binary ID `0x0A38` to
both `Closed` (`kCDXProp_Closed`, `CDXBoolean`) and `CurveSpacing`
(`kCDXProp_Curve_Spacing`, `UINT16`). The archived global predefined-property
table repeats the same pair of assignments, but is part of the same SDK source
family rather than independent corroboration. The linked detail pages for
these properties were unavailable, and no independent SDK header evidence was
found during this check. This is recorded as an unresolved source anomaly;
neither numeric value is silently changed or treated as independently verified.

The detailed facts also preserve XML-versus-binary differences that would be
lost by typing an attribute only from its CDX storage type:

- `Bond_Order` is binary `INT16` and bit-encoded. Its SDK value table lists 16
  CDXML value tokens; `0xFFFF` is unspecified and omitted from CDXML. If the
  property is absent, the SDK says it is treated as a single bond. The SDK says
  the listed binary values may be combined. The pinned DTD declares `b.Order`
  as `CDATA #IMPLIED`, not as a four-value enumeration. These claims do not
  define an ordinal enum, and `focused-properties.json` retains the binary
  values and XML tokens in separate fields.
- `LabelSize` and `CaptionSize` property pages document binary `INT16` default
  font sizes. Separately, the `CDXString` datatype page says style-run font
  size is an integral `UINT16` count of twentieths of a point and shows an XML
  `<s size="12">` example. The historical source does not explicitly state
  that the separate `LabelSize`/`CaptionSize` properties use the same scale,
  so the catalog does not infer that conversion.
- The `CDXFontTable` datatype page describes each binary font character-set
  code as `UINT16`, while its CDXML example writes `font charset="iso-8859-1"`;
  the DTD declares the XML attribute `CDATA`. The SDK page provides no mapping
  from XML charset tokens to binary codes, so XML `font.charset` remains
  lexical text rather than being interpreted as an integer.
- The archived coordinate datatype page gives a three-value CDXML example
  (`72 144 216`) for `CDXPoint3D`, ordered x/y/z, with coordinates expressed in
  points and decimal values allowed. One sentence in that paragraph mistakenly
  labels the XML value `CDXPoint2D`; the catalog records this caveat alongside
  the example rather than treating the sentence as a separate type contract.
  The global property table assigns `CDXPoint3D` to the center and two axis-end
  records, but lists `Center3D` as the CDXML Name for all three and gives no
  owning XML object. The DTD has matching `Center3D` attributes and distinct
  `MajorAxisEnd3D`/`MinorAxisEnd3D` attributes on several owners. The repeated
  SDK name is therefore retained as an unresolved reconciliation issue; the
  catalog does not invent corrected XML names or associate binary IDs with
  those DTD fields.
- `RotationAngle` is binary `INT32`, degrees multiplied by 65536; absence means
  zero degrees.
- `CDXDate` is documented as a 14-byte structure of seven `INT16` fields in
  UTC. That datatype page does not define a CDXML lexical date format.
- `Attachments` (`CDXObjectIDArrayWithCounts`) has a `UINT16` count prefix in
  CDX, while the CDXML representation is the same as `CDXObjectIDArray` and
  omits that count. The `LineStarts` `INT16ListWithCounts` datatype also has a
  CDX count prefix but a flat list in CDXML. Curve point arrays similarly have
  a CDX count and flat component lists in CDXML.
- `CDXElementList` and `CDXGenericList` document `NOT`-prefixed CDXML lists.
  `CDXFormula` is explicitly undefined/future expansion, and the SDK says
  ChemDraw neither reads nor writes a property of that datatype; no formula
  semantics are asserted from its name.
- `ObjectTag.Value` is binary `varies`; `TagType` selects `FLOAT64`, `INT32`, or
  unformatted string. The pages define omission defaults but do not define the
  meaning of an explicitly present empty XML value. `Unformatted` says
  nonprintable XML bytes are hex-encoded; this does not justify hex-decoding
  arbitrary printable values.
- `Spectrum_DataPoint` is a binary `FLOAT64` array. Its property page labels
  `temp_SpectrumDataPoint`, says the property is used explicitly only for CDX,
  and says CDXML stores the data directly as `spectrum` `#PCDATA`. It is not a
  literal attribute name. `Spectrum_YLow` is documented as future compatibility
  and not read or written by ChemDraw.
- `colortable` and `fonttable` are CDX property tags (`kCDXProp_ColorTable`
  and `kCDXProp_FontTable`) saved instead as child table objects in CDXML.
  `color`, `font`, and `s` are kept in the SDK's XML-only namespace; no binary
  object IDs are fabricated for them.

These are statements from archived SDK documentation, not black-box ChemDraw
verification. Where the SDK itself states that a feature is not read/written
or only defined for future compatibility, that statement remains attributed to
the source and is not upgraded to a runtime test result.

The SDK `Curve` page spells three property names `ArrowHeadType`,
`ArrowHeadHead`, and `ArrowHeadTail`, while the pinned DTD spells the same
Curve attributes `ArrowheadType`, `ArrowheadHead`, and `ArrowheadTail`. Runtime
metadata retains the DTD names as canonical and records these exact case
variants as aliases. A single spelling is read and edited in place; a newly
created Curve uses the DTD spelling. If both spellings are present, even with
identical values, typed access and validation report a conflict rather than
guessing which attribute to keep. Parsing and serialization preserve both raw
attributes so a caller can repair the retained tree explicitly.

## Provenance and refresh

Each archived page's exact returned Memento URL, capture timestamp, retrieval
time, raw-byte size, SHA-256 digest, and locator are recorded in the JSON
catalogs. The catalogs contain factual extraction only; archived HTML is not
checked in because redistribution terms are unclear. Their source URL/hash
records are intended to support review and pin verification.

Acquisition is explicit development tooling and is not a runtime network
dependency:

```sh
uv run python -m tools.spec_evidence.acquire --fetch \
  --pins schema/sources/sdk/evidence.json \
  --output /tmp/sdk-evidence-refresh.json

uv run python -m tools.spec_evidence.acquire --fetch --focused-only \
  --pins schema/sources/sdk/focused-properties.json \
  --output /tmp/focused-evidence-refresh.json
```

`--pins` requests the exact source URLs already recorded and rejects a SHA-256
mismatch. Running without pins is an explicit source refresh: a requested
archive timestamp may resolve to a different returned capture, which the tool
records rather than presenting as a byte-deterministic re-download. The HTML
importer uses offline HTML recovery for malformed historical pages and stores
recovery diagnostics in its candidate record; CDXML/DTD parsing remains strict.
