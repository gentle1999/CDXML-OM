# Offline schema-source ingestion

English | [简体中文](zh-CN/ingestion.md)

The schema importer turns one explicitly selected local source into a review
candidate. It never fetches URLs, executes page scripts, updates canonical YAML,
or generates runtime code. Candidate JSON retains the source path and SHA-256;
diff output is evidence for review, not an apply plan.

```sh
python -m tools.schema_importer import-dtd schema/sources/revvity-CDXML.dtd \
  --output build/revvity-dtd.candidate.json
python -m tools.schema_importer import-sdk path/to/archived-sdk-page.html \
  --output build/node-sdk.candidate.json
python -m tools.schema_importer diff build/node-sdk.candidate.json \
  --output build/node-sdk.diff.json
```

Outputs default to standard output; `--output -` makes that explicit. Existing
output paths require `--force`, but no output path under `schema/canonical/` is
allowed, even with `--force`. A successful import or diff exits 0, including
when the diff contains findings. Invalid, unreadable, unsafe, or malformed input
returns 2 and writes a one-line structured JSON diagnostic to standard error.
Diff findings are categorized as `added`, `changed`, or `missing`; the tool
does not decide which source is authoritative or rewrite either one.

The current diff is intentionally bounded: it reviews selected attribute
presence, requiredness, lexical defaults, declared-type evidence, and enum
alternatives; object/property identifiers and constants; and child-name
inventory. It does not assert equivalence of complete DTD grammar, ordering, or
cardinality, nor does it claim a complete interpretation of the SDK. Recognized
subobject rows are retained as source evidence even where no canonical
comparison is attempted.

## Safety and source quirks

Inputs are local paths only. DTD input must be UTF-8. Parameter-entity
declarations and references are conservatively refused before libxml parsing,
and external `SYSTEM`/`PUBLIC` entity or doctype declarations are rejected.
This deliberately excludes DTD features that can synthesize declarations or
read external resources; the checked-in [Revvity DTD snapshot](../schema/sources/revvity-CDXML.dtd)
does not require parameter entities. The source digest always covers the
original bytes, before any parser-only normalization.

The pinned DTD contains legacy enumeration tokens `+`, `-`, and `?` (for
example the `AS` attribute). These are escaped only in the temporary bytes sent
to the DTD parser, then restored in candidate values. Each such parser-only
normalization is recorded in the candidate; it is not presented as a correction
to the source or as a CDX semantic mapping.

Archived SDK HTML is parsed with networking disabled and without loading an
external doctype or entity. The tool only reads tables in the supplied file; it
does not crawl links or execute scripts. The SDK’s object and property
namespaces remain separate: an inventory entry such as `Color Table` with
`kCDXProp_ColorTable` is retained as a property, while the XML `colortable`
resource container is not assigned a CDX object identifier. Likewise, SDK type
text such as `UINT16` is kept verbatim and diffed against (not silently
converted to) canonical datatype evidence such as `object_id`.

The importer recognizes the documented [SDK object inventory](https://chemapps.stolaf.edu/iupac/cdx/sdk/AllCDXObjects.htm)
and per-object tables such as [Node](https://chemapps.stolaf.edu/iupac/cdx/sdk/Node.htm).
These pages are evidence sources, not runtime dependencies. The local DTD
snapshot is the input used for reproducible imports; the upstream copy is
available at [RevVity’s CDXML DTD](https://static.chemistry.revvitycloud.com/cdxml/CDXML.dtd).
