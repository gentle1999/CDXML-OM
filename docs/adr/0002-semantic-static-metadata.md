# ADR 0002: Semantically organized static metadata

English | [简体中文](../zh-CN/adr/0002-semantic-static-metadata.md)

Status: accepted

## Context

The full source-backed schema produces metadata for hundreds of properties,
53 element models, enums, codecs, child routes, and source references. A single
generated module was unwieldy, but splitting it into numbered size-based
chunks would make ownership and review arbitrary. Runtime package consumers
must also remain independent of build-time YAML, DTD, SDK catalogs, and compiler
tools.

## Decision

The compiler emits ordinary static Python maintained in the repository under
`cdxml_om._generated._metadata/`, organized by schema meaning:

- frozen metadata types and shared source/datatype constants have dedicated
  modules;
- each object and each enum has a module named from its canonical schema ID;
- properties are grouped by logical owner, with common property definitions
  emitted once and imported by owners that share them;
- provenance constants are grouped by their source ID, with symbol names
  derived from stable content hashes of source URI and locator.

`schema_metadata.py` remains a thin backward-compatible re-export facade.
Generated wrapper classes, registries, enums, and metadata are static imports;
the runtime does not parse JSON/YAML schema files, interpret the schema, or use
`exec`/`eval`/JIT model construction. Python imports the static modules
normally. Schema changes should be accompanied by the generated artifacts. The
compiler deterministically sorts imports and formats emitted source. It checks
the generated tree recursively, rejects unexpected files, and only removes
stale Python files bearing the generated-file notice.

## Consequences

Reviewers can find metadata by object, enum, property owner/shared family, or
source instead of counting into a numbered shard. Common property metadata
retains single-instance identity. Adding an unrelated provenance reference
does not renumber existing provenance symbols. The module graph is larger, but
the organization follows the canonical schema and the installed runtime still
imports only Python modules.

This layout is an implementation organization, not a claim of complete DTD
grammar or ChemDraw behavior. Coverage remains reported independently by the
source-bound feature evidence system.
