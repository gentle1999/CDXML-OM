# Interactive examples

English | [简体中文](zh-CN/examples.md)

The repository includes three executable notebooks. They are focused API
demonstrations, not a replacement for the pinned-source coverage inventory or
complete DTD/ChemDraw conformance tests.

- [01 — Core workflow](../examples/notebooks/01_core_workflow.ipynb): parse,
  navigate, edit, create/remove objects, and round-trip references.
- [02 — Document features](../examples/notebooks/02_document_features.ipynb):
  local resources, rich text, graphics, reaction references, irregular typed
  fields, and lexical Spectrum data.
- [03 — Validation and preservation](../examples/notebooks/03_validation_and_preservation.ipynb):
  unknown XML preservation, structured validation findings, and safe handling
  of an external entity reference.

## Install and run

From a repository checkout, install the optional notebook tools:

```bash
uv sync --extra notebooks
```

Execute copies into a fresh directory without changing the checked-in
notebooks:

```bash
notebook_output="$(mktemp -d "${TMPDIR:-/tmp}/cdxml-om-notebooks.XXXXXX")"
uv run --no-sync python -m tools.run_notebooks --output-dir "$notebook_output"
```

CI and local development can execute the notebooks and verify that saved
outputs are current:

```bash
uv run --no-sync python -m tools.run_notebooks --check
```

After reviewing an intentional notebook change, refresh committed outputs with
`uv run --no-sync python -m tools.run_notebooks --update`. The runner executes
all notebooks before it begins updating source files, and replaces each file
atomically; a filesystem error during the later multi-file update can still
leave some files updated. Output-copy mode never overwrites existing paths.

The runner uses a temporary kernel specification bound to the current Python
interpreter and a fresh temporary working directory for each notebook. This
keeps relative example files out of the checkout; it is not a security sandbox
for Python code. Treat notebooks as trusted code, and do not execute an
unreviewed notebook merely because it is in a repository. For interactive use,
open the files in a Jupyter-capable editor and select the checkout's Python
environment after installing the `notebooks` extra.

The repository also includes seven persisted CDXML files for manual
application inspection. See the [render-sample guide](../examples/render_samples/README.md)
for the opening order, source notes, and compatibility boundaries. The user
reports that six files opened and rendered normally in Windows ChemDraw
Professional 25.5.0.5789; an earlier curve payload produced “vector too long”.
The curve probe has since changed and awaits retest. This report has no
screenshots or independently reproducible application artifact and is not
independent ChemDraw verification.
