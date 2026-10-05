# CDXML-OM

English | [简体中文](README.zh-CN.md)

[![Python ≥3.11](https://img.shields.io/badge/Python-%E2%89%A53.11-blue)](pyproject.toml) [![MIT License](https://img.shields.io/badge/License-MIT-blue)](LICENSE) [![Single-source version](https://img.shields.io/badge/Version-single--source%20configuration-1f6feb)](src/cdxml_om/_version.py) [![Typed package](https://img.shields.io/badge/Typing-py.typed-blue)](src/cdxml_om/py.typed) [![Strict type checks](https://img.shields.io/badge/Types-Pyright%20%2B%20mypy%20strict-8a2be2)](pyproject.toml)

[![Ruff lint and format](https://img.shields.io/badge/Ruff-lint%20%2B%20format%20configured-46a2f1)](pyproject.toml) [![Pytest suite](https://img.shields.io/badge/Tests-pytest%20configured-0a9edc)](tests/) [![CI and releases configured](https://img.shields.io/badge/CI%20%2B%20release-GitHub%20Actions%20configured-lightgrey)](.github/workflows/release.yml) [![Generated static models](https://img.shields.io/badge/Models-53%20static%20wrappers-2ea44f)](docs/architecture.md) [![CDXML XML model](https://img.shields.io/badge/XML-lxml%20tree%20preservation-00599c)](docs/compatibility.md)

[![Pinned DTD scope](https://img.shields.io/badge/Pinned%20DTD-53%20elements%20%2F%20762%20pairs-2ea44f)](docs/feature-support.md) [![PCDATA and SDK extension scope](https://img.shields.io/badge/PCDATA%20%2B%20SDK-2%2F2%20%2B%2023%2F23%20round--trip-2ea44f)](docs/feature-support.md) [![Bilingual documentation](https://img.shields.io/badge/Docs-English%20%2B%20Simplified%20Chinese-blue)](docs/index.md) [![Runtime dependencies](https://img.shields.io/badge/Runtime-lxml%20only%20%2F%20no%20RDKit-blue)](pyproject.toml) [![ChemDraw application verification](https://img.shields.io/badge/ChemDraw%20app%20verification-none-lightgrey)](docs/feature-support.md)

These 15 badges describe static configuration and source scope, not live CI,
package-index, or download statistics. The pinned-source test counts do not
imply complete DTD grammar conformance or ChemDraw application verification.

CDXML-OM is a typed, schema-driven Python object model for reading, editing,
validating, and writing ChemDraw CDXML documents. Its generated runtime maps
all 53 elements and 762 owner/attribute pairs in the pinned Revvity DTD, plus a
separately measured set of SDK-documented XML extensions.

## Features

- Typed models, fields, enums, and live child collections generated from a
  reviewed canonical schema.
- Retains the complete `lxml` tree, including unknown tags, attributes, and
  ordering; wrapper identity is stable for each underlying element.
- Secure local XML parsing without network access or external-entity loading.
- Source-bound feature tests exercise typed reads, writes, mutations, and
  serialize/reload behavior. No independent ChemDraw verification artifact
  has been captured; user-reported application observations below are not
  counted as verification.

The user reports that six files in the [manual sample set](examples/render_samples/README.md)
opened and rendered normally in Windows ChemDraw Professional 25.5.0.5789; an
earlier curve payload produced “vector too long”. The curve candidate has since
changed and is pending retest. There are no screenshots or independent
application-verification artifacts, so this report does not change the
`ChemDrawVerified=0` boundary.

## Install from a checkout

The repository version is a development release; these instructions install
from the checkout rather than assuming a package-index release.

```bash
# From the repository root; installs the package and its runtime dependency.
uv sync

# Or, using pip from the repository root:
python -m pip install -e .
```

Python 3.11 or newer is required. The only required runtime dependency is
`lxml`; RDKit is not required.

## Versioning and releases

The single version source is `src/cdxml_om/_version.py`. Hatchling reads its
`__version__` assignment without importing the runtime package; `cdxml_om.__version__`
and built distribution metadata come from that same value. For a release, edit
only that assignment, then run `uv lock`, `uv sync`, and
`uv run python tools/check_package.py` before building or publishing. The uv
cache key includes the version file so editable metadata is refreshed after a
version change. Do not add a second version literal to `pyproject.toml` or
`__init__.py`. The tag-triggered build and publishing procedure is documented in
the [release guide](docs/releasing.md).

## Example

This example starts with an empty document, creates and edits a small graph,
validates it, writes it, reloads it, and checks that bond references resolve to
the reloaded node wrappers:

```python
from cdxml_om import CDXMLDocument

document = CDXMLDocument.from_string("<CDXML/>")
page = document.pages.create()
fragment = page.fragments.create()
carbon = fragment.nodes.create(element=6, position=(0.0, 0.0))
oxygen = fragment.nodes.create(element=8, position=(10.0, 0.0))
bond = fragment.bonds.create(begin=carbon, end=oxygen, order=1)

bond.order = 2
oxygen.charge = -1
report = document.validate()
assert report.is_valid, report.errors

document.to_file("example.cdxml")
reloaded = CDXMLDocument.from_file("example.cdxml")
reloaded_fragment = reloaded.pages[0].fragments[0]
reloaded_bond = reloaded_fragment.bonds[0]
assert reloaded_bond.begin is reloaded_fragment.nodes[0]
assert reloaded_bond.end is reloaded_fragment.nodes[1]
assert reloaded.validate().is_valid
```

Validation reports known schema constraints; it is not chemical validation or
complete DTD grammar validation. Removing an object does not cascade or rewrite
its references. See the [feature-support guide](docs/feature-support.md) for
the exact mapped elements and boundaries. This code illustrates the object API,
not page layout or ChemDraw rendering; see the [manual samples](examples/render_samples/README.md)
for separate visual inspection candidates.

## Interactive notebooks

Install the optional notebook tools with `uv sync --extra notebooks`. The
[notebook guide](docs/examples.md) links three bilingual examples covering
core edits, richer document features, validation, and preservation. Execute and
check their saved outputs with:

```bash
uv run --no-sync python -m tools.run_notebooks --check
```

The runner uses temporary kernels and working directories, not a security
sandbox; execute only reviewed, trusted notebooks.

## Development

Install development tools and run the schema, style, typing, and test checks:

```bash
uv sync --extra dev
uv run python -m tools.schema_compiler check
uv run python -m tools.schema_compiler build
uv run python -m tools.schema_compiler coverage
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run mypy
uv run pytest
uv run --no-sync python -m tools.run_notebooks --check
```

Project documentation is indexed at [docs](docs/index.md). The package is
licensed under the [MIT License](LICENSE).
