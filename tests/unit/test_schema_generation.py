import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from tools.schema_compiler.generate import (
    _module_component,
    _provenance_modules,
    _schema_metadata_refs,
    compare_outputs,
    compile_outputs,
    write_outputs,
)
from tools.schema_compiler.ir import SourceRef
from tools.schema_compiler.loader import load_schema
from tools.schema_compiler.validate import validate_schema

from cdxml_om import BondOrder
from cdxml_om._generated.schema_metadata import (
    DATATYPE_METADATA,
    ENUM_METADATA,
    OBJECT_METADATA,
    PROPERTY_METADATA,
)

ROOT = Path(__file__).resolve().parents[2]


def test_generated_files_are_current_and_have_notices() -> None:
    schema = load_schema(ROOT)
    assert validate_schema(schema) == ()
    outputs = compile_outputs(schema, ROOT)
    assert compare_outputs(outputs, ROOT) == ()
    for path, contents in outputs.items():
        if path.startswith("src/cdxml_om/_generated/"):
            assert contents.startswith("# AUTO-GENERATED. DO NOT EDIT DIRECTLY.")


def test_generation_is_deterministic() -> None:
    schema = load_schema(ROOT)

    assert compile_outputs(schema, ROOT) == compile_outputs(schema, ROOT)


def test_metadata_modules_are_named_by_schema_specs() -> None:
    schema = load_schema(ROOT)
    outputs = compile_outputs(schema, ROOT)
    generated_root = "src/cdxml_om/_generated/_metadata/"

    object_modules = {
        path.removeprefix(f"{generated_root}objects/")
        for path in outputs
        if path.startswith(f"{generated_root}objects/")
        and path != f"{generated_root}objects/__init__.py"
    }
    enum_modules = {
        path.removeprefix(f"{generated_root}enums/")
        for path in outputs
        if path.startswith(f"{generated_root}enums/")
        and path != f"{generated_root}enums/__init__.py"
    }
    property_modules = {
        path.removeprefix(f"{generated_root}properties/")
        for path in outputs
        if path.startswith(f"{generated_root}properties/")
        and path != f"{generated_root}properties/__init__.py"
    }
    expected_property_groups = {
        "shared" if len(prop.owners) > 1 else prop.owners[0] for prop in schema.properties
    }

    assert object_modules == {f"{obj.id}.py" for obj in schema.objects}
    assert enum_modules == {f"{_module_component(enum.python_name)}.py" for enum in schema.enums}
    assert property_modules == {f"{group}.py" for group in expected_property_groups}
    assert not any("part_" in path for path in outputs)
    assert len(outputs["src/cdxml_om/_generated/schema_metadata.py"].splitlines()) < 150


def test_nested_stale_generated_files_are_reported(tmp_path: Path) -> None:
    schema = load_schema(ROOT)
    outputs = compile_outputs(schema, ROOT)
    stale_relative = Path("src/cdxml_om/_generated/_metadata/objects/stale.py")
    stale = tmp_path / stale_relative
    stale.parent.mkdir(parents=True)
    stale.write_text("# AUTO-GENERATED. DO NOT EDIT DIRECTLY.\nstale = True\n", encoding="utf-8")

    differences = compare_outputs(outputs, tmp_path)

    assert f"unexpected generated file: {stale_relative.as_posix()}" in differences


def test_provenance_symbols_do_not_renumber_when_an_unrelated_source_is_added() -> None:
    schema = load_schema(ROOT)
    references = _schema_metadata_refs(schema)
    _, before = _provenance_modules(references)
    selected = references[0]
    unrelated = SourceRef(
        source="newly_reviewed_source",
        locator="unrelated fact",
        uri="https://example.invalid/newly-reviewed-source",
    )
    _, after = _provenance_modules((*references, unrelated))

    assert before[(selected.uri, selected.locator)] == after[(selected.uri, selected.locator)]


def test_write_outputs_removes_only_stale_generated_python(tmp_path: Path) -> None:
    schema = load_schema(ROOT)
    outputs = compile_outputs(schema, ROOT)
    generated = tmp_path / "src" / "cdxml_om" / "_generated"
    stale = generated / "_metadata" / "objects" / "stale.py"
    stale.parent.mkdir(parents=True)
    stale.write_text(
        "# AUTO-GENERATED. DO NOT EDIT DIRECTLY.\nstale = True\n",
        encoding="utf-8",
    )
    write_outputs(outputs, tmp_path)
    assert not stale.exists()

    private_file = generated / "private.py"
    private_file.write_text("# Keep this user file.\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="refusing to remove non-generated Python file"):
        write_outputs(outputs, tmp_path)
    assert private_file.read_text(encoding="utf-8") == "# Keep this user file.\n"
    private_file.unlink()


def test_schema_lock_has_required_hashes() -> None:
    lock = json.loads((ROOT / "schema/schema.lock.json").read_text(encoding="utf-8"))

    assert lock["schema_version"] == 1
    assert len(lock["schema_hash"]) == 64
    assert lock["generator_version"]
    assert lock["input_hashes"]
    assert isinstance(lock["source_hashes"], dict)
    assert (
        lock["source_hashes"]["schema/sources/revvity-CDXML.dtd"]
        == "5311978e514ffe154108540c3634c314dc66031a4f3c877a681fc6dca8e128c2"
    )


def test_generated_metadata_is_valid_and_shared_properties_have_one_definition() -> None:
    common_id = PROPERTY_METADATA["common.id"]

    assert OBJECT_METADATA["page"].properties["common.id"] is common_id
    assert OBJECT_METADATA["fragment"].properties["common.id"] is common_id
    assert OBJECT_METADATA["node"].properties["common.id"] is common_id
    assert OBJECT_METADATA["bond"].properties["common.id"] is common_id
    assert PROPERTY_METADATA["bond.order"].codec == "bond_order"
    assert PROPERTY_METADATA["bond.order"].default == "1"
    assert PROPERTY_METADATA["bond.begin"].reference_target == "node"
    assert PROPERTY_METADATA["bond.end"].reference_target == "node"
    assert PROPERTY_METADATA["dtd.crossingbond.bond_id"].reference_target == "bond"
    assert PROPERTY_METADATA["dtd.crossingbond.inner_atom_id"].reference_target == "node"
    assert DATATYPE_METADATA["object_id"].maximum == 2**32 - 1
    assert all(
        prop.codec == "object_id_list" for prop in PROPERTY_METADATA.values() if prop.reference_many
    )
    assert ENUM_METADATA["bond_order"].representation == "intflag"
    assert BondOrder.SINGLE | BondOrder.DOUBLE == 3
    assert {value.xml_value: value.cdx_value for value in ENUM_METADATA["bond_order"].values} == {
        "1": 1,
        "2": 2,
        "3": 4,
        "4": 8,
        "5": 16,
        "6": 32,
        "0.5": 64,
        "1.5": 128,
        "2.5": 256,
        "3.5": 512,
        "4.5": 1024,
        "5.5": 2048,
        "dative": 4096,
        "ionic": 8192,
        "hydrogen": 16384,
        "threecenter": 32768,
    }


def test_build_bootstraps_when_generated_runtime_files_are_missing(tmp_path: Path) -> None:
    project = tmp_path / "project"
    (project / "tools").mkdir(parents=True)
    shutil.copy2(ROOT / "tools" / "__init__.py", project / "tools" / "__init__.py")
    shutil.copytree(ROOT / "tools" / "schema_compiler", project / "tools" / "schema_compiler")
    shutil.copytree(ROOT / "schema" / "canonical", project / "schema" / "canonical")
    (project / "schema" / "sources").mkdir(parents=True)
    shutil.copy2(
        ROOT / "schema" / "sources" / "revvity-CDXML.dtd",
        project / "schema" / "sources" / "revvity-CDXML.dtd",
    )
    if (ROOT / "schema" / "sources" / "sdk" / "evidence.json").is_file():
        shutil.copytree(
            ROOT / "schema" / "sources" / "sdk",
            project / "schema" / "sources" / "sdk",
        )
    shutil.copy2(ROOT / "schema" / "schema.lock.json", project / "schema" / "schema.lock.json")
    shutil.copy2(ROOT / "pyproject.toml", project / "pyproject.toml")

    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    result = subprocess.run(
        [sys.executable, "-m", "tools.schema_compiler", "build"],
        cwd=project,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert (project / "src" / "cdxml_om" / "_generated" / "models.py").is_file()
