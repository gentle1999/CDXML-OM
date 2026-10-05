from __future__ import annotations

import os
import shutil
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest
from tools.schema_compiler.loader import load_schema
from tools.schema_importer.errors import ImporterError
from tools.schema_importer.promote_full_schema import (
    _add_property_owner,
    _object_sdk_identifiers,
)

ROOT = Path(__file__).resolve().parents[2]


def _assert_promoted_reference_metadata(project: Path) -> None:
    schema = load_schema(project)
    properties = {prop.id: prop for prop in schema.properties}

    many_references = [
        prop for prop in schema.properties if prop.reference is not None and prop.reference.many
    ]
    assert many_references
    assert all(prop.codec == "object_id_list" for prop in many_references)
    assert properties["bond.begin"].reference is not None
    assert properties["bond.begin"].reference.target_type == "node"
    assert properties["bond.end"].reference is not None
    assert properties["bond.end"].reference.target_type == "node"
    assert properties["dtd.crossingbond.bond_id"].reference is not None
    assert properties["dtd.crossingbond.bond_id"].reference.target_type == "bond"
    assert properties["dtd.crossingbond.inner_atom_id"].reference is not None
    assert properties["dtd.crossingbond.inner_atom_id"].reference.target_type == "node"


def test_repeated_full_schema_promotion_is_deterministic(tmp_path: Path) -> None:
    project = tmp_path / "project"
    shutil.copytree(
        ROOT / "tools",
        project / "tools",
        ignore=shutil.ignore_patterns("__pycache__"),
    )
    shutil.copytree(ROOT / "schema", project / "schema")

    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    command = [sys.executable, "-m", "tools.schema_importer.promote_full_schema"]

    first = subprocess.run(
        command,
        cwd=project,
        env=environment,
        capture_output=True,
        check=False,
        text=True,
    )
    assert first.returncode == 0, first.stderr
    _assert_promoted_reference_metadata(project)
    canonical_files = (
        project / "schema" / "canonical" / "objects.yaml",
        project / "schema" / "canonical" / "properties.yaml",
        project / "schema" / "canonical" / "enums.yaml",
    )
    first_outputs = tuple(path.read_bytes() for path in canonical_files)

    second = subprocess.run(
        command,
        cwd=project,
        env=environment,
        capture_output=True,
        check=False,
        text=True,
    )
    assert second.returncode == 0, second.stderr
    _assert_promoted_reference_metadata(project)
    assert tuple(path.read_bytes() for path in canonical_files) == first_outputs


@pytest.mark.parametrize(
    "prop",
    [
        {"owners": "node"},
        {"owners": ["node", 17]},
        {"owner": 17},
        {"owners": ["node"], "owner": 17},
    ],
)
def test_invalid_property_owner_shape_is_rejected_without_mutation(
    prop: dict[str, object],
) -> None:
    original = deepcopy(prop)

    with pytest.raises(ImporterError) as error:
        _add_property_owner(prop, "fragment")

    assert error.value.code == "FULL_SCHEMA_PROPERTY_OWNER"
    assert prop == original


def test_legacy_single_property_owner_is_promoted_to_sorted_owner_list() -> None:
    prop: dict[str, object] = {"owner": "node"}

    _add_property_owner(prop, "fragment")

    assert prop == {"owners": ["fragment", "node"]}


def test_existing_owner_list_is_deduplicated_without_mutating_input_list() -> None:
    owners = ["node", "fragment", "node"]
    prop: dict[str, object] = {"owners": owners}

    _add_property_owner(prop, "fragment")

    assert prop == {"owners": ["fragment", "node"]}
    assert prop["owners"] is not owners
    assert owners == ["node", "fragment", "node"]


@pytest.mark.parametrize(
    "sdk",
    [
        {"namespace": "object", "cdx_id": True, "cdx_constant": "kFoo"},
        {"namespace": "object", "cdx_id": "32769", "cdx_constant": "kFoo"},
        {"namespace": "object", "cdx_id": 32769, "cdx_constant": 17},
    ],
)
def test_invalid_object_sdk_identifiers_are_rejected(sdk: dict[str, object]) -> None:
    with pytest.raises(ImporterError) as error:
        _object_sdk_identifiers("fragment", sdk)

    assert error.value.code == "FULL_SCHEMA_OBJECT_MAPPING"


def test_object_sdk_identifiers_keep_verified_integer_and_constant() -> None:
    assert _object_sdk_identifiers(
        "fragment",
        {"namespace": "object", "cdx_id": 0x8001, "cdx_constant": "kCDXObj_Fragment"},
    ) == (0x8001, "kCDXObj_Fragment")
