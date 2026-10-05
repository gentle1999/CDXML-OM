# CDXML-OM documentation

English | [简体中文](zh-CN/index.md)

This documentation describes the typed XML object model, the source evidence
it covers, and its conservative compatibility boundaries. It does not claim
complete CDXML grammar validation or ChemDraw interoperability.

## Guides

- [Feature support](feature-support.md) — supported models and APIs, exact
  pinned-source scope, and explicit limits.
- [Feature-to-test index](feature-tests.md) — all 762 DTD attribute cases,
  grouped by exact XML owner.
- [Architecture](architecture.md) — generated schema and retained-tree runtime.
- [Schema and compiler](schema.md) — canonical schema, static generation, and
  provenance.
- [Compatibility and preservation](compatibility.md) — parsing, identity,
  mixed content, mutation, and validation behavior.
- [Coverage methodology](coverage.md) — denominators, test evidence, and fresh
  report commands.
- [Specification evidence baseline](specification-baseline.md) — DTD/SDK source
  facts and unresolved source anomalies.
- [Offline ingestion](ingestion.md) — safe local-source candidate imports.
- [Release process](releasing.md) — version tags, artifact checks, PyPI Trusted
  Publishing, and GitHub releases.
- [Interactive examples](examples.md) — three bilingual notebooks and safe
  execution/update commands.

## Architecture decisions

- [ADR 0001: conservative references, IDs, and mixed content](adr/0001-conservative-reference-and-content-boundaries.md)
- [ADR 0002: semantic static metadata organization](adr/0002-semantic-static-metadata.md)

The repository [README](../README.md) contains installation and a runnable
quick-start example. See the [Chinese documentation index](zh-CN/index.md) for
Simplified Chinese pages.
