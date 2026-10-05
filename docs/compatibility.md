# Compatibility and preservation

English | [简体中文](zh-CN/compatibility.md)

The parser accepts local files, Unicode strings, and XML byte strings whose
declared encoding is handled by libxml2. It disables external entity
resolution, DTD loading, and network access. Internal DTD declarations and
unexpanded entity references remain in the retained tree. Malformed XML and a
root other than exactly `CDXML` raise `ParseError`; malformed known field
values and unresolved references are deferred until typed access or explicit
validation.

Known XML tags are matched exactly, including namespaces. The generated
runtime covers all 53 declarations in the pinned DTD, including a typed
`CDXMLRoot`; the handwritten `CDXMLDocument` remains the document-level facade.
Parent-scoped collections are live and support typed creation/removal.
Document-level `.groups`, `.texts`, `.graphics`, `.arrows`, and `.schemes`
collections are navigational; creation requires a valid parent collection.
Twenty documented SDK XML attributes not declared in the DTD and three
case-variant Curve spellings are handled as a separate extension set. Unknown
tags and attributes remain navigable through generic `CDXMLElement` wrappers.

Object-ID lookup includes only generated `document`-scoped objects. Duplicate
document IDs fail lookup and reference resolution rather than choosing a
target. Font IDs are `local` to each FontTable and are not returned by
`document.get(Font, id)`; color rows and text runs have `none` ID scope. Root
FontTable/ColorTable IDs, font IDs, and unknown-tag `id` attributes are not
treated as document IDs. Typed allocation reserves document IDs observed by
the allocator for the document lifetime and rescans the live tree and raw
references to avoid current collisions. Raw DOM edits bypass mutation history;
an ID introduced and removed entirely through raw edits cannot be remembered.
Local Font IDs are independently allocated and validated per table.

ReactionStep `reactants`, `products`, and `arrows` use whitespace-separated
document-ID arrays. Their typed values are tuples of modeled `CDXMLElement`
wrappers; references may target any modeled document object, including legacy
arrows represented as `<graphic>`. Raw IDs remain available when a target is
dangling or ambiguous. Reassigning a list validates all references before
changing XML, and changing/removing a target does not implicitly rewrite or
cascade its references.

Text `<s>` runs expose character data as `.content` and formatting values as
typed fields. Reads preserve the original run content and CDATA representation
because they do not rewrite the DOM. Replacing content changes that run's
character data; replacement is rejected if the run contains child nodes,
avoiding deletion of opaque mixed content. Unknown attributes and formatting
on other runs remain intact. `Text.plain_text` concatenates descendant run
content for convenience.

`spectrum.data` exposes the raw lexical character data directly owned by the
`spectrum` element: its `.text` plus direct child tails. Text nested inside
`objecttag`, `annotation`, or another child is not treated as spectrum data;
comments, processing-instruction text, and unexpanded entity references are
not interpreted as samples. Setting `.data` changes only those direct
character-data segments while retaining child wrappers and order (and setting
the direct segments clears their previous child tails). The archived SDK says
Spectrum data is stored in CDXML PCDATA, but the pinned sources do not establish
a numeric sample separator/encoding. This API is lexical, not a spectrum
parser; it does not resolve or fetch entities.

Curve's DTD spellings `ArrowheadType`, `ArrowheadHead`, and `ArrowheadTail`
remain canonical. The SDK's case variants `ArrowHeadType`, `ArrowHeadHead`,
and `ArrowHeadTail` are accepted aliases. Reads and edits preserve the spelling
already present; if both spellings for a field occur, typed access and
validation report a conflict instead of silently discarding one.

Serialization uses the complete retained lxml tree, preserving XML structure,
document-level processing instructions/comments, CDATA boundaries, internal
DTD/entity references, and unknown content. It is not byte-identical: lxml may
normalize quoting, declaration details, or other lexical forms. Raw edits
through `raw_element` are visible to later lookups and validation, but bypass
typed checks and allocator history. Allocators rescan the live tree to avoid
current collisions and retain IDs seen through typed allocation for the
document lifetime; they cannot track raw IDs that are introduced and removed
between scans.

`document.validate()` reports known field/value errors, required values,
document- and table-scoped duplicate IDs, typed references, known parent/child
constraints, and child cardinality. Minimum cardinality is reported by
validation rather than enforced by mutation, so callers can create an
intermediate invalid tree by removing a required child and repair it later. If
a generated element is beneath an unmodeled parent envelope, validation emits a
warning instead of claiming that the source-valid route is illegal. Validation
is not complete DTD validation, chemical validation, or an application
interoperability guarantee.

The canonical definitions are based on the pinned Revvity DTD and archived
CambridgeSoft SDK documentation. The two small corpus files are RDKit-hosted;
their own XML declares a ChemDraw creation program, which is not independent
ChemDraw verification. Binary CDX support and chemistry adapters are not part
of this runtime. The core package has no RDKit dependency.

The reasoning behind the conservative ID, reference, mixed-content, and
resource-linking boundaries is recorded in
[ADR 0001](adr/0001-conservative-reference-and-content-boundaries.md).

## Application observations

The user reports that the six current files other than the curve probe opened
and rendered normally in Windows ChemDraw Professional 25.5.0.5789. The earlier
two-point 2D+3D curve payload (SHA-256
`abb94c07688e56763deb6a73e57bccc69cc6f60d69758f9b54b60525ef39d28c`) produced
“vector too long”; the curve probe has since been regenerated with a
source-grounded 2D candidate and is pending retest. No screenshots or
independently reproducible application artifact were supplied. See the
[sample guide](../examples/render_samples/README.md) for the observed-file
hashes and source notes. The changed curve has not been rechecked, and none of
these reports changes the source-bound `ChemDrawVerified` status.
