# Specification sources

The canonical subset uses the archived CambridgeSoft CDX/CDXML SDK
documentation mirrored by IUPAC FAIRSpec, plus a local snapshot of the DTD
served by Revvity Signals at
`https://static.chemistry.revvitycloud.com/cdxml/CDXML.dtd`. The DTD was
retrieved on 2026-10-04. Its internal header says
`/ChemDraw/CDXML.dtd 48 4/23/03`; the endpoint is current, while the DTD content
identifies itself as a 2003 revision. The snapshot is
[`revvity-CDXML.dtd`](revvity-CDXML.dtd), SHA-256
`5311978e514ffe154108540c3634c314dc66031a4f3c877a681fc6dca8e128c2`.

The checked-in fact catalogs under [`sdk/`](sdk/) reconcile the DTD against the
archived SDK inventory and object-property tables, and retain focused datatype
and property encodings. They record exact returned Internet Archive Memento
URLs, retrieval timestamps, SHA-256 hashes, and table/section locators. The
catalogs contain factual extractions rather than copies of SDK HTML.

The pinned DTD declares 53 XML elements, including the `CDXML` root, and 762
owner/attribute pairs. Its root is the SDK Document object (`0x8000`), but the
DTD has no root `id` attribute. The SDK index has 38 rows: object IDs, property
IDs for `colortable`, `fonttable`, and `represent`, and XML-only rows for
`color`, `font`, and `s`. The detailed tables have 410 exact owner/name matches;
case variants are kept separate. The totals and the DTD-only tags, SDK-only
attributes, XML-child properties, non-XML properties, and unresolved DTD
anomaly are in `sdk/evidence.json`.

`sdk/focused-properties.json` separately records selected XML-versus-binary
contracts, including Bond_Order's bit values and absence default, counted
arrays, list encodings, rotation, dates, curves, object tags, and Spectrum
data. It also pins the SDK coordinate and property-table pages used for 3D
point lexical evidence. The property table repeats `Center3D` as the XML name
for three distinct CDXPoint3D records; because the DTD has separate
`MajorAxisEnd3D` and `MinorAxisEnd3D` names, the catalog preserves this as an
unresolved mismatch instead of assigning speculative property IDs. Binary
IDs/types and XML lexical behavior are kept distinct. Facts that the archived
source does not settle remain explicitly unresolved; neither catalog is a
ChemDraw runtime verification.

The schema lock records the SHA-256 of the vendored DTD. SDK HTML is not
redistributed; evidence JSON records source hashes and provenance only.
Explicit acquisition is provided by `tools/spec_evidence/acquire.py`; it does
not run at package runtime. Use the exact pinned URLs in an existing evidence
catalog with `--pins` to verify byte-for-byte source identity. Acquisition
without pins is a source refresh, not a deterministic re-download.

## Licensing and redistribution notes

The repository's MIT license applies to project-authored software and
documentation; it does not by itself relicense external specifications or
fixtures. The vendored DTD and source evidence retain their origin and
provenance; the DTD header does not state a license grant. The upstream corpus
fixture license is preserved at
[`tests/fixtures/corpus/RDKit-LICENSE.txt`](../../tests/fixtures/corpus/RDKit-LICENSE.txt).
Review the applicable rights before public redistribution of bundled source
artifacts. These notes preserve provenance and do not make a legal conclusion.
