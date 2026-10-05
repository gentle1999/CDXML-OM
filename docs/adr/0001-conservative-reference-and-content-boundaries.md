# ADR 0001: Conservative reference, ID, and mixed-content boundaries

English | [简体中文](../zh-CN/adr/0001-conservative-reference-and-content-boundaries.md)

- Status: Accepted
- Date: 2026-10-05

## Context

CDXML combines document object IDs, table-local resource IDs, ID arrays, and
mixed XML content. Some source constructs are only partially described by the
pinned DTD and SDK evidence. The object model must remain loss-preserving when
the target or resource semantics are ambiguous, rather than inferring meaning
from an XML attribute name or a likely chemistry convention.

## Decisions

1. **ID scope is explicit schema metadata.** Only generated object types marked
   `document` participate in document lookup and reference resolution. Font
   IDs are local to their FontTable; TextRun and Color have no object ID. An
   unknown tag's `id` attribute is never assumed to be a document object ID.
   Typed allocation reserves opaque IDs observed during the document lifetime;
   live-tree rescans avoid current collisions after raw edits, but raw IDs
   introduced and removed between scans are outside mutation history.
2. **ReactionStep object arrays resolve conservatively.** `reactants`,
   `products`, and `arrows` expose tuples of generic `CDXMLElement` wrappers,
   not chemically narrowed model types. This preserves valid variation such
   as legacy arrows represented by `<graphic>`. Raw numeric IDs remain
   accessible when a reference is dangling or ambiguous; assignment validates
   all targets before changing XML.
3. **TextRun content edits do not destroy opaque mixed content.** Reads are
   non-mutating and expose character data. Replacing `.content` is supported
   only when the run has no child nodes; otherwise a structured mutation error
   is raised. This avoids silently deleting elements, comments, or other
   retained content nested in a run.
4. **Font and color resource links are not inferred.** Font IDs are allocated
   and validated within their own FontTable, but TextRun font indices are not
   resolved to Font wrappers. Color rows do not have object IDs, and color
   indices are not resolved. Automatic resource insertion, deduplication, and
   index remapping are deferred until evidence and a preservation-safe API are
   available.

## Consequences

The parser and serializer can preserve unrecognized IDs, references, and
mixed content without claiming semantics they do not have. Callers can inspect
raw reference IDs and the retained XML when typed resolution is unavailable.
The corresponding tradeoff is that font/color links and chemically specific
reaction validation require application-level interpretation outside this
runtime. Serialization preserves XML structure, not original source bytes.

See [compatibility notes](../compatibility.md), [coverage](../coverage.md),
and the [offline schema ingestion guide](../ingestion.md).
