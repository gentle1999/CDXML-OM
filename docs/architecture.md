# Architecture

English | [简体中文](zh-CN/architecture.md)

CDXML-OM treats the CDXML schema as its source of truth. Specification evidence
is normalized into immutable schema IR, then generators emit static Python
models, enums, registries, and validation metadata. The runtime wraps the
original `lxml` tree so typed access and edits do not discard unknown elements,
attributes, or ordering.

```text
specification evidence → canonical schema → schema IR → static generators
                                                   ↓
                                  models / enums / registry / metadata
                                                   ↓
                       lossless XML wrapper → document → semantic adapters
```

The runtime keeps a full `lxml` element tree and layers secure CDXML input and
output beneath the document facade. Generated descriptors read values lazily
from generated property metadata; exact XML tags select one of the 53 static
DTD-backed wrappers while undeclared tags remain generic, navigable wrappers.
The generated `CDXMLRoot` is distinct from the handwritten `CDXMLDocument`
facade. Wrapper identity is cached by the original lxml element. Object-ID
lookup is restricted to document-scoped modeled objects; local resource IDs,
the root, and undeclared element IDs are not assumed to share that namespace.

Typed setters and live parent-scoped child collections encode and modify
generated known properties. Creation validates all values and same-document
reference wrappers before appending; removal preserves following mixed-content
text and does not cascade references. Document-scoped IDs are allocated
monotonically. Typed allocation reserves existing opaque `id` attributes and
parseable raw reference IDs observed on the live tree for the document
lifetime; arbitrary raw edits bypass allocator history, though each allocation
rescans current IDs to prevent collisions. Font IDs have an independent
table-local allocator; color rows and rich-text runs have no object ID.
Renaming an ID does not rewrite references. `validate()` reports known schema
violations without rejecting load or altering the tree, including child
cardinality, and does not infer illegal parent routes through an unmodeled
envelope. Documents remain editable when temporarily invalid. Validation does
not claim complete DTD content-model enforcement or chemical validity. Core
dependencies are intentionally limited to `lxml`; RDKit is not a core
dependency.

Generated metadata is maintained as ordinary static Python in the repository
under `cdxml_om._generated._metadata/`, organized by named objects, enums,
logical property owners/shared properties, and evidence sources. Schema
changes should be accompanied by their regenerated artifacts. The public
`schema_metadata` module is a compatibility re-export facade. Metadata objects
are frozen/slotted and shared properties retain object identity. This static
layout keeps runtime imports independent of YAML, DTD, SDK catalogs, and
compiler tooling; semantic organization and its rationale are recorded in
[ADR 0002](adr/0002-semantic-static-metadata.md).

The source order for future schema reconciliation is the current Revvity
CDXML DTD, archived CambridgeSoft SDK documentation, W3C XML requirements,
ChemDraw-generated files, and differential implementations. PyCDXML can be
consulted as historical evidence only. Imported evidence is a candidate, not an
automatic replacement for reviewed canonical definitions.
