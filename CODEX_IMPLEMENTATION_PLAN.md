# CDXML-OM implementation plan

This file records the accepted implementation milestones and current handoff
boundaries for the prototype. For user-facing architecture, scope, and
compatibility, see the [README](README.md), [architecture](docs/architecture.md),
[feature-support guide](docs/feature-support.md), and
[compatibility guide](docs/compatibility.md). The canonical schema, generated
runtime, and source-bound evidence define implementation behavior.

1. **Schema compiler — complete:** reviewed canonical data is loaded into
   immutable IR, validated, generated as static typed models/metadata, and
   locked by deterministic schema/source hashes.
2. **Retained-tree runtime — complete:** secure parse/serialize I/O, stable
   wrappers, exact-tag dispatch, typed lazy codecs, object lookup, and typed
   navigation are implemented.
3. **Mutation and validation — complete:** fields and child collections
   mutate the DOM, document IDs allocate monotonically, references are checked
   atomically, and `validate()` reports schema-backed errors/warnings.
4. **Accepted V0.1 slice — complete:** the original Group, Text/TextRun,
   Graphic, Arrow, ReactionScheme/ReactionStep, and resource-table models were
   the first typed slice. The current implementation has since expanded beyond
   that historical scope; see objective 7 and the coverage report.
5. **Specification ingestion — complete:** offline DTD and archived SDK
   import/diff tooling produces reviewable candidates. Promotion remains an
   explicit source-reviewed canonical-schema change.
6. **Pinned-DTD coverage meter — complete:** source-relative inventory and
   assertion-linked, source-bound test evidence distinguish known mappings,
   implementation, typing, successful tests, round trips, and ChemDraw
   verification. See [`docs/coverage.md`](docs/coverage.md) for the measurement
   method and [`docs/feature-support.md`](docs/feature-support.md) for the
   accepted scope snapshot.
7. **Full static CDXML layer — accepted (2026-10-05):** the generated runtime
   contains typed wrappers for all 53 declarations in the pinned DTD, covers
   all 762 DTD owner/attribute pairs and both PCDATA features, and separately
   supports 20 documented SDK-only XML attributes plus three Curve casing
   aliases. A fresh source-bound evidence run reports all applicable elements,
   pairs, PCDATA features, and SDK extensions implemented, typed, tested, and
   round-trip verified. This is 100% of the stated pinned-source feature scope,
   not complete DTD grammar validation or ChemDraw application verification.
   `ChemDrawVerified` remains 0 because no independent application verification
   artifact and observation were captured. The
   undeclared `altgroup -> bracket` symbol and lack of a sourced numeric
   Spectrum PCDATA grammar remain explicit boundaries.

Do not equate schema knowledge with working support or application
interoperability. DTD presence alone does not prove a semantic mapping, and
source-preserving serialization alone does not count as a typed feature test.
Coverage distinguishes source-backed schema knowledge from implemented,
typed, tested, and round-trip-tested behavior. ChemDraw verification requires
application artifacts. CDX binary and chemistry adapters remain outside the
current runtime unless explicitly added to the scope.

## Prototype handoff

This tree is being prepared for prototype review, not a release. This
preparation does not stage or commit files and does not change the version,
create a tag, or publish a package. Keep the canonical schema, source evidence,
generated static models, lock files, fixtures, executed notebooks, and manual
sample files as intentional project content; ignore only local caches and
build/report output. Before a future commit, review the complete candidate diff
and run the repository checks documented in the README. The separate release
process and its prerequisites are in [`docs/releasing.md`](docs/releasing.md).
The MIT license covers project code; it does not automatically relicense
imported specifications or fixtures. Review redistribution rights before a
public release as described in [`schema/sources/README.md`](schema/sources/README.md).

Manual-application status is limited to the user report in the
[sample guide](examples/render_samples/README.md): six current files opened and
rendered normally in Windows ChemDraw Professional 25.5.0.5789; an earlier
curve payload produced “vector too long”, and the revised curve awaits retest.
No screenshots or independent application-verification artifacts were
provided.
