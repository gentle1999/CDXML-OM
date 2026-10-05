# Release workflow

The release workflow is [`.github/workflows/release.yml`](../.github/workflows/release.yml).
Only a pushed tag matching `v*` starts it. The workflow validates that the tag is
exactly `v` followed by the canonical PEP 440 version in
[`src/cdxml_om/_version.py`](../src/cdxml_om/_version.py); local-version suffixes
such as `+local` are rejected. PEP 440 development, alpha, beta, and release
candidate versions are accepted and marked as prereleases on GitHub.

## One-time publishing configuration

PyPI Trusted Publishing needs an external configuration before the first
publish. Register a pending or existing publisher for project `cdxml-om` with:

| PyPI publisher field | Value |
| --- | --- |
| Owner | `gentle1999` |
| Repository | `CDXML-OM` |
| Workflow filename | `release.yml` |
| GitHub environment | `pypi` |

If the project does not yet exist on PyPI, use PyPI's pending-publisher flow;
the project name is not reserved until the first successful publish. See the
[PyPI instructions for adding a publisher](https://docs.pypi.org/trusted-publishers/adding-a-publisher/)
and [creating a project through OIDC](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/).

In GitHub repository settings, create the `pypi` environment, allow deployment
only from release tags matching `v*`, and consider requiring a trusted reviewer.
Add a tag ruleset for `v*` that limits tag creation, updates, and deletion to
release maintainers. The workflow independently checks that the tagged commit
is already reachable from the default branch.

## What the workflow does

1. The unprivileged build job installs the locked development environment and
   runs Ruff, Pyright, mypy, pytest, schema check/build, and the package checks.
2. It runs the pinned-source feature cases with current JUnit-bound evidence and
   uploads that report as a separate quality artifact.
3. It builds one wheel and one source distribution, smoke-tests those exact
   files in an isolated runtime environment, checks the tag and metadata
   versions, and writes `SHA256SUMS` outside the package directory.
4. The single `release-dist` artifact carries those same package bytes and the
   checksum manifest. The PyPI job downloads and verifies the artifact, then
   publishes only the contents of `packages/` using OIDC Trusted Publishing.
   It has `id-token: write` and no checkout or project-code execution.
5. Only after PyPI publication succeeds, a separate least-privilege job
   downloads and verifies the same artifact and creates a GitHub Release with
   the verified wheel, sdist, and manifest. It never rebuilds the distributions.

All third-party GitHub Actions are pinned to full commit SHAs. No long-lived
PyPI token is stored in repository secrets. Existing PyPI files and GitHub
releases are not overwritten: `skip-existing` is disabled and the GitHub CLI is
not given `--clobber`.

The checksum manifest is relative to the release bundle layout. For the
workflow artifact, verify it from the bundle root with:

```sh
sha256sum --check --strict SHA256SUMS
```

GitHub Release downloads are flat. To verify those assets with the attached
manifest, place the wheel and sdist under a `packages/` directory next to
`SHA256SUMS`, then run the same command from that directory's parent.

## Local preflight and tagging

First edit only `_version.py` to the intended canonical version, then update the
lock and run the repository checks. The following builds to a fresh temporary
directory and validates the same files the workflow will publish; replace the
example tag with `v` plus the exact version in `_version.py`:

```sh
uv lock
uv sync --locked --extra dev
uv run --no-sync ruff check .
uv run --no-sync ruff format --check .
uv run --no-sync pyright
uv run --no-sync mypy
uv run --no-sync pytest
uv run --no-sync python -m tools.schema_compiler check
uv run --no-sync python -m tools.schema_compiler build
# Only generated outputs must be unchanged; _version.py and uv.lock may contain
# the intentional release-version update described above.
git diff --exit-code -- src/cdxml_om/_generated schema/schema.lock.json

release_dir="$(mktemp -d "${TMPDIR:-/tmp}/cdxml-om-release.XXXXXX")"
mkdir -p "$release_dir/release-bundle/packages"
uv build --no-create-gitignore --out-dir "$release_dir/release-bundle/packages"
uv run --no-sync python tools/check_package.py \
  --dist-dir "$release_dir/release-bundle/packages"
release_tag="v1.2.3"  # Replace with the exact source version.
uv run --no-sync python -m tools.release \
  --tag "$release_tag" \
  --packages-dir "$release_dir/release-bundle/packages" \
  --bundle-dir "$release_dir/release-bundle"
(cd "$release_dir/release-bundle" && sha256sum --check --strict SHA256SUMS)
```

After the version change is reviewed and merged to the default branch, create
and push its exact tag to trigger the workflow:

```sh
git tag -a v1.2.3 -m "Release v1.2.3"  # Use the exact version in _version.py.
git push origin v1.2.3
```

Do not push a tag before its version change is on the default branch. The
workflow uses the helper's validated tag/version outputs for privileged jobs,
not an interpolated shell expression from the event payload.

## Failures and reruns

Build failures before publication can be corrected and rerun. After a PyPI
failure, inspect the published file inventory first: if nothing was uploaded,
correct the cause and retry; if only part of the pair was uploaded, do not
blindly rerun the workflow or enable `skip-existing`. Ask a release maintainer
to reconcile the partial publication; normally the safe recovery is a corrected
new version. If PyPI completed but the GitHub Release job failed, rerun only the
failed `github-release` job in that same workflow run; its successful PyPI
dependency is reused. Rerunning the whole workflow after a successful upload
will fail on already-published filenames because duplicate uploads are not
skipped. Do not enable overwrite or clobber behavior.

The pipeline is configuration, not evidence that a remote release has already
run. PyPI publisher setup and any first-publish project registration remain
maintainer responsibilities.
