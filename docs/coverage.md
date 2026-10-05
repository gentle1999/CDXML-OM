# Coverage model

English | [简体中文](zh-CN/coverage.md)

For user-facing capabilities and limitations, see the separate
[feature-support guide](feature-support.md).

The schema compiler's `coverage` command compares canonical generated artifacts
with the pinned Revvity DTD (`5311978e514ffe154108540c3634c314dc66031a4f3c877a681fc6dca8e128c2`).
Its exact denominators are 53 declared elements, 762 owner/attribute pairs, and
the two DTD elements containing character data (`s` and `spectrum`). The
coverage report is static tooling output; document parsing does not load the
DTD, SDK source catalog, YAML, or coverage tooling.

Coverage stages are intentionally separate:

- `known` means the item is present in the pinned DTD inventory, not that its
  semantics or ChemDraw behavior are known.
- `canonical_*_known` means a reviewed canonical object/property mapping exists.
- `implemented` means a generated wrapper descriptor is connected to a runtime
  codec; opaque XML retention alone does not qualify.
- `typed` means the exact generated model/descriptor is available through the
  static registry.
- `test_case_declared` means the checked-in independent feature catalog links
  that item to the explicitly named assertions.
- `tested` and `round_trip_verified` require all linked pytest cases to pass in
  a current, source-bound test run. Failed, skipped, uncollected, or stale cases
  do not count.
- `chemdraw_verified` requires an explicit artifact and observation; fixture
  round-trips do not imply ChemDraw interoperability.

The DTD denominators and SDK extension denominator are separate. The extension
set contains 20 exact SDK-documented XML owner/attribute pairs beyond the DTD
and three Curve casing aliases; aliases do not add DTD pairs. The two
character-data features (`s` and `spectrum`) have their own denominator. A
current inventory-only report demonstrates mapping/implementation and declared
test recipes, not successful execution; supply a fresh source-bound test run
to count tested and round-trip-verified features. The SDK catalog similarly
distinguishes typed feature recipes from the separate raw-preservation cases.

The accepted source-bound snapshot dated 2026-10-05 reports 53/53 elements,
762/762 DTD pairs, 2/2 PCDATA features, and 23/23 SDK extension pairs
implemented, typed, tested, and round-trip verified. This snapshot is specific
to the pinned DTD and checked-in catalogs. ChemDraw verification remains 0; it
requires a separate real-application artifact and observation.

Generate the deterministic inventory report with:

```sh
uv run python -m tools.schema_compiler coverage --format text
uv run python -m tools.schema_compiler coverage --format json
```

To run the catalog and capture verifiable JUnit outcomes, create a fresh
evidence directory outside the repository (the runner does not reuse existing
JUnit output paths):

```sh
evidence_dir="$(mktemp -d "${TMPDIR:-/tmp}/cdxml-om-feature-run.XXXXXX")"
uv run python -m tools.schema_compiler test-features \
  --run-evidence "$evidence_dir/feature-run.json" \
  --junitxml "$evidence_dir/feature-run.xml" -- tests/coverage
uv run python -m tools.schema_compiler coverage \
  --test-run "$evidence_dir/feature-run.json" --format json
```

The runner captures fingerprints before and after pytest, writes JUnit to a new
path, and binds the run evidence to the resulting JUnit digest. Editing runtime,
schema, feature recipes, fixtures, helpers, or tests invalidates a saved run.
The feature catalog format is described by
[`schema/coverage/feature-cases.schema.json`](../schema/coverage/feature-cases.schema.json);
the deterministic output and test-run formats are described by the adjacent
`report.schema.json` and `test-run.schema.json` schemas.

The report also lists DTD content-model trees but does not claim complete
strict grammar validation. The pinned source contains the undeclared child
symbol `altgroup -> bracket`; `<bracket>` is retained as an unknown element
unless a separate source defines it. `spectrum` character data has a typed
lexical API, but no numeric sample grammar is asserted. ChemDraw verification
remains 0 until there is a separately captured application artifact and
observation.
