from __future__ import annotations

import re
from pathlib import Path
from typing import cast

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "release.yml"
PINNED_ACTION = re.compile(r"[^@\s]+@[0-9a-f]{40}\Z")


def _workflow() -> dict[str, object]:
    parsed: object = yaml.load(WORKFLOW_PATH.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
    assert isinstance(parsed, dict)
    return cast(dict[str, object], parsed)


def _mapping(value: object) -> dict[str, object]:
    assert isinstance(value, dict)
    return cast(dict[str, object], value)


def _list(value: object) -> list[object]:
    assert isinstance(value, list)
    return cast(list[object], value)


def _job(workflow: dict[str, object], name: str) -> dict[str, object]:
    jobs = _mapping(workflow["jobs"])
    return _mapping(jobs[name])


def _steps(job: dict[str, object]) -> list[dict[str, object]]:
    return [_mapping(step) for step in _list(job["steps"])]


def _run_scripts(job: dict[str, object]) -> list[str]:
    return [step["run"] for step in _steps(job) if isinstance(step.get("run"), str)]


def _action_steps(job: dict[str, object], action_prefix: str) -> list[dict[str, object]]:
    return [
        step
        for step in _steps(job)
        if isinstance(step.get("uses"), str) and cast(str, step["uses"]).startswith(action_prefix)
    ]


def _permissions(job: dict[str, object]) -> dict[str, object]:
    return _mapping(job.get("permissions", {}))


def _needs(job: dict[str, object]) -> set[str]:
    raw_needs = job["needs"]
    if isinstance(raw_needs, str):
        return {raw_needs}
    return {str(value) for value in _list(raw_needs)}


def _find_values(node: object, key_name: str) -> list[object]:
    if isinstance(node, dict):
        mapping = cast(dict[object, object], node)
        return [
            value
            for key, child in mapping.items()
            for value in ([child] if key == key_name else []) + _find_values(child, key_name)
        ]
    if isinstance(node, list):
        return [value for child in node for value in _find_values(child, key_name)]
    return []


def test_release_workflow_is_tag_only_and_preserves_the_on_key() -> None:
    workflow = _workflow()
    triggers = _mapping(workflow["on"])

    assert triggers == {"push": {"tags": ["v*"]}}
    assert "pull_request_target" not in WORKFLOW_PATH.read_text(encoding="utf-8")
    assert "workflow_dispatch" not in triggers


def test_every_github_action_is_pinned_to_a_full_commit_sha() -> None:
    workflow = _workflow()
    jobs = _mapping(workflow["jobs"])
    references: list[str] = []
    for job_value in jobs.values():
        for step in _steps(_mapping(job_value)):
            action = step.get("uses")
            if isinstance(action, str):
                references.append(action)

    assert references
    assert all(PINNED_ACTION.fullmatch(reference) for reference in references)


def test_build_job_runs_all_quality_and_package_gates_against_its_built_artifacts() -> None:
    workflow = _workflow()
    build = _job(workflow, "build")
    scripts = _run_scripts(build)
    command_text = "\n".join(scripts).lower()

    for required in (
        "ruff check",
        "ruff format --check",
        "pyright",
        "mypy",
        "pytest",
        "schema_compiler check",
        "tools/check_package.py",
    ):
        assert required in command_text

    package_check = next(line for line in command_text.splitlines() if "check_package.py" in line)
    assert "--dist-dir" in package_check
    assert "packages" in package_check
    assert "uv build" in command_text
    assert "--no-create-gitignore" in command_text
    assert "python -m tools.release" in command_text
    assert "--packages-dir" in command_text
    assert "--bundle-dir" in command_text
    assert '--tag "$release_tag"' in command_text
    assert '--github-output "$github_output"' in command_text
    assert 'git merge-base --is-ancestor "$release_sha" fetch_head' in command_text
    release_step = next(
        step
        for step in _steps(build)
        if isinstance(step.get("run"), str) and "python -m tools.release" in step["run"]
    )
    assert _mapping(release_step["env"]).get("RELEASE_TAG") == "${{ github.ref_name }}"


def test_privileged_jobs_only_receive_scoped_permissions_after_upstream_success() -> None:
    workflow = _workflow()
    assert _mapping(workflow["permissions"]) == {"contents": "read"}
    jobs = _mapping(workflow["jobs"])
    pypi = _job(workflow, "publish-pypi")
    github_release = _job(workflow, "github-release")

    assert _permissions(pypi) == {"id-token": "write"}
    assert _permissions(github_release) == {"contents": "write"}
    environment = pypi["environment"]
    environment_name = (
        environment if isinstance(environment, str) else _mapping(environment).get("name")
    )
    assert environment_name == "pypi"
    assert _needs(pypi) == {"build"}
    assert _needs(github_release) >= {"build", "publish-pypi"}
    assert {
        name for name, value in jobs.items() if "write" in _permissions(_mapping(value)).values()
    } == {"publish-pypi", "github-release"}
    assert "PYPI_TOKEN" not in WORKFLOW_PATH.read_text(encoding="utf-8")

    release_env = _mapping(github_release["env"])
    assert release_env.get("RELEASE_TAG") == "${{ needs.build.outputs.tag }}"
    assert release_env.get("RELEASE_VERSION") == "${{ needs.build.outputs.version }}"
    assert release_env.get("RELEASE_PRERELEASE") == "${{ needs.build.outputs.prerelease }}"


def test_privileged_jobs_download_and_verify_the_same_bundle_without_checkout_or_build() -> None:
    workflow = _workflow()
    jobs = _mapping(workflow["jobs"])
    for name in ("publish-pypi", "github-release"):
        job = _mapping(jobs[name])
        actions = _action_steps(job, "actions/download-artifact@")
        assert len(actions) == 1
        assert _mapping(actions[0].get("with", {})).get("name") == "release-dist"
        scripts = _run_scripts(job)
        assert any("sha256sum --check --strict" in script for script in scripts)
        assert not any("actions/checkout@" in str(step.get("uses", "")) for step in _steps(job))
        assert not any(
            any(command in script for command in ("uv build", "uv sync", "pip install", "uv pip"))
            for script in scripts
        )
        allowed_actions = (
            "actions/download-artifact@",
            "pypa/gh-action-pypi-publish@",
        )
        assert all(
            any(str(step.get("uses", "")).startswith(prefix) for prefix in allowed_actions)
            for step in _steps(job)
            if step.get("uses") is not None
        )

    pypi_action_steps = _action_steps(
        _mapping(jobs["publish-pypi"]), "pypa/gh-action-pypi-publish@"
    )
    assert len(pypi_action_steps) == 1
    pypi_config = _mapping(pypi_action_steps[0].get("with", {}))
    assert "release-bundle/packages" in str(pypi_config.get("packages-dir", ""))
    assert pypi_config.get("skip-existing") == "false"

    upload_steps = _action_steps(_mapping(jobs["build"]), "actions/upload-artifact@")
    release_uploads = [
        _mapping(step.get("with", {}))
        for step in upload_steps
        if _mapping(step.get("with", {})).get("name") == "release-dist"
    ]
    assert len(release_uploads) == 1
    upload_config = release_uploads[0]
    uploaded_paths = {
        line.strip() for line in str(upload_config.get("path", "")).splitlines() if line.strip()
    }
    assert uploaded_paths == {
        "dist/release-bundle/packages/*.whl",
        "dist/release-bundle/packages/*.tar.gz",
        "dist/release-bundle/SHA256SUMS",
    }
    assert any(
        _mapping(step.get("with", {})).get("name") == "release-feature-evidence"
        for step in upload_steps
    )


def test_shell_commands_use_quoted_tag_environment_not_inline_github_context() -> None:
    workflow = _workflow()
    run_scripts = [
        script
        for job in _mapping(workflow["jobs"]).values()
        for script in _run_scripts(_mapping(job))
    ]
    assert "${{ github.ref_name }}" in _find_values(workflow, "RELEASE_TAG")
    assert all("${{" not in script for script in run_scripts)
    release_job = _job(workflow, "github-release")
    release_text = "\n".join(_run_scripts(release_job)).lower()
    assert "gh release create" in release_text
    assert "--verify-tag" in release_text
    assert '"$release_tag"' in release_text
    assert "release-bundle/packages/*.whl" in release_text
    assert "release-bundle/packages/*.tar.gz" in release_text
    assert "release-bundle/sha256sums" in release_text
    assert 'if [[ "$release_prerelease" == "true" ]]' in release_text
    assert "prerelease_args+=(--prerelease)" in release_text
    assert "--clobber" not in release_text
    assert "--skip-existing" not in "\n".join(_run_scripts(_job(workflow, "publish-pypi"))).lower()
