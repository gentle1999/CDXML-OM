# Changelog

## Unreleased

- Established a pinned-source static model for all 53 declarations, 762 DTD
  owner/attribute pairs, two PCDATA features, and a separately measured set of
  23 SDK extension pairs. Source-bound feature evidence covers typed reads,
  writes, mutations, and serialize/reload behavior; see the feature-support
  guide for exact denominators and limits.
- Added the immutable canonical schema IR, deterministic semantic code
  generation, generated metadata modules, and source/schema hash lock.
- Added a secure retained-`lxml` runtime with lazy typed fields, stable wrapper
  identity, scoped IDs, references, live child collections, atomic typed
  mutation, structured schema validation, and unknown-content preservation.
- Added source-reviewed value codecs for coordinates, geometry, enums, lists,
  references, mixed text, and context-dependent object tags. These mappings do
  not imply complete DTD content-model validation or chemical interpretation.
- Added offline DTD/SDK candidate ingestion, source provenance, compatibility
  guidance, bilingual documentation, and executable notebooks.
- Added strict Ruff, Pyright, and mypy checks; package verification; CI checks;
  and a tag-based release workflow. These are repository configurations, not
  evidence that a remote release has run.
- User-reported manual observations: six current sample files opened and
  rendered normally in Windows ChemDraw Professional 25.5.0.5789; an earlier
  curve payload produced “vector too long”. The replacement curve is pending
  retest. No screenshots or independent application-verification artifact
  were supplied; see the [manual sample log](examples/render_samples/README.md).
