"""Source-relative schema and feature-test coverage reporting.

This module is build-time tooling. Runtime document loading never imports it.
"""

from __future__ import annotations

import ast
import hashlib
import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ElementTree
from dataclasses import asdict
from pathlib import Path
from typing import cast

from cdxml_om._generated.schema_metadata import OBJECT_METADATA, PropertyMetadata
from cdxml_om._generated.schema_registry import OBJECT_BY_XML_TAG
from cdxml_om.core.codecs import supports_property_codec
from cdxml_om.core.fields import Field, RefField, RefListField
from cdxml_om.core.models import CDXMLElement
from tools.schema_compiler.generate import compare_outputs, compile_outputs, schema_hash
from tools.schema_compiler.ir import Schema
from tools.schema_importer.candidate import DTDElementCandidate
from tools.schema_importer.dtd_importer import import_dtd

PINNED_DTD_SHA256 = "5311978e514ffe154108540c3634c314dc66031a4f3c877a681fc6dca8e128c2"
DTD_RELATIVE_PATH = "schema/sources/revvity-CDXML.dtd"
LOCK_RELATIVE_PATH = "schema/schema.lock.json"
CASE_CATALOG_RELATIVE_PATH = "tests/coverage/feature_cases.json"
SDK_EXTENSION_CASE_CATALOG_RELATIVE_PATH = "tests/coverage/sdk_extension_cases.json"
CASE_FORMAT = "cdxml-om-full-schema-feature-cases"
CASE_FORMAT_VERSION = 1
SDK_EXTENSION_CASE_FORMAT = "cdxml-om-sdk-extension-feature-cases"
SDK_EXTENSION_CASE_FORMAT_VERSION = 1
SDK_EXTENSION_PAIR_COUNT = 23
REPORT_FORMAT = "cdxml-om-coverage-report"
REPORT_FORMAT_VERSION = 2
RUN_FORMAT = "cdxml-om-feature-test-run"
RUN_FORMAT_VERSION = 2

TEST_OPERATIONS = frozenset({"read", "write", "mutation", "round_trip"})
ELEMENT_OPERATIONS = frozenset({"dispatch", "mutation", "round_trip"})
_FIELD_DESCRIPTORS = (Field, RefField, RefListField)
_ATTRIBUTE_ASSERTIONS = frozenset(
    {
        "exact_wrapper_type",
        "source_lexical_value",
        "typed_read_value_and_python_type",
        "typed_mutation",
        "mutation_lexical_value",
        "serialization_reload_readback",
        "unknown_content_and_order_preserved",
    }
)
_ELEMENT_ASSERTIONS = frozenset(
    {
        "exact_wrapper_type",
        "element_creation",
        "element_removal",
        "element_round_trip",
        "root_creation",
        "root_mutation",
    }
)
_CHARACTER_ASSERTIONS = frozenset(
    {
        "storage_lexical_value",
        "typed_read_value_and_python_type",
        "typed_mutation",
        "mutation_lexical_value",
        "serialization_reload_readback",
    }
)
_SDK_TYPED_ASSERTIONS = frozenset(
    {
        "typed_read_value_and_python_type",
        "typed_mutation",
        "mutation_lexical_value",
        "serialization_reload_typed_readback",
    }
)
_SDK_RAW_ASSERTIONS = frozenset(
    {"raw_lexical_read", "unrelated_edit_preserves_raw", "serialization_reload_preserves_raw"}
)


class CoverageError(ValueError):
    """The pinned DTD, feature-case catalog, or test-run evidence is invalid."""


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def _read_json(path: Path, label: str) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CoverageError(f"cannot read {label} at {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CoverageError(f"{label} must be a JSON object")
    return cast(dict[str, object], value)


def _mapping(value: object, location: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise CoverageError(f"{location} must be a JSON object with text keys")
    raw = cast(dict[object, object], value)
    if any(not isinstance(key, str) for key in raw):
        raise CoverageError(f"{location} must be a JSON object with text keys")
    return {cast(str, key): item for key, item in raw.items()}


def _string(value: object, location: str) -> str:
    if not isinstance(value, str) or not value:
        raise CoverageError(f"{location} must be non-empty text")
    return value


def _string_list(value: object, location: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise CoverageError(f"{location} must be an array of non-empty text values")
    raw = cast(list[object], value)
    if any(not isinstance(item, str) or not item for item in raw):
        raise CoverageError(f"{location} must be an array of non-empty text values")
    entries = cast(list[str], raw)
    if len(entries) != len(set(entries)):
        raise CoverageError(f"{location} contains duplicate entries")
    return tuple(entries)


def _pinned_inventory(root: Path) -> tuple[str, tuple[DTDElementCandidate, ...]]:
    dtd_path = root / DTD_RELATIVE_PATH
    try:
        raw = dtd_path.read_bytes()
    except OSError as exc:
        raise CoverageError(f"cannot read pinned DTD {DTD_RELATIVE_PATH}: {exc}") from exc
    digest = _sha256(raw)
    if digest != PINNED_DTD_SHA256:
        raise CoverageError(
            f"pinned DTD digest changed: expected {PINNED_DTD_SHA256}, found {digest}"
        )
    lock = _read_json(root / LOCK_RELATIVE_PATH, "schema lock")
    hashes = _mapping(lock.get("source_hashes"), "schema lock source_hashes")
    if hashes.get(DTD_RELATIVE_PATH) != PINNED_DTD_SHA256:
        raise CoverageError("schema lock does not name the fixed pinned DTD digest")
    try:
        candidate = import_dtd(str(dtd_path))
    except Exception as exc:
        raise CoverageError(f"cannot parse the pinned DTD: {exc}") from exc
    if candidate.source.sha256 != PINNED_DTD_SHA256:
        raise CoverageError("DTD importer digest disagrees with the pinned DTD bytes")
    elements = candidate.dtd_elements
    tags = [item.xml_name for item in elements]
    if len(tags) != len(set(tags)):
        raise CoverageError("pinned DTD contains duplicate element declarations")
    pairs = [(item.xml_name, attribute.name) for item in elements for attribute in item.attributes]
    if len(pairs) != len(set(pairs)):
        raise CoverageError("pinned DTD contains duplicate owner-attribute declarations")
    if len(elements) != 53 or len(pairs) != 762:
        raise CoverageError(
            "pinned DTD inventory differs from the accepted denominator "
            f"(expected 53 elements/762 owner-attribute pairs, found {len(elements)}/{len(pairs)})"
        )
    return digest, elements


def _test_node_function(node_id: str, root: Path) -> tuple[str, str]:
    path_text, separator, function_text = node_id.partition("::")
    if not separator or "::" in function_text or not path_text.startswith("tests/"):
        raise CoverageError(
            f"invalid pytest node ID {node_id!r}; expected tests/path.py::test_name"
        )
    if not path_text.endswith(".py") or "/../" in f"/{path_text}/":
        raise CoverageError(f"pytest node ID must use a repository-relative test path: {node_id!r}")
    if not function_text.startswith("test_") or "[" in function_text or "]" in function_text:
        # Parameterized IDs are represented as suffixes after the function name.
        if not function_text.startswith("test_") or function_text.count("[") != 1:
            raise CoverageError(f"invalid pytest test function in node ID {node_id!r}")
        function_text = function_text.split("[", 1)[0]
    test_path = root / path_text
    try:
        source = test_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise CoverageError(f"test source referenced by {node_id!r} is unavailable: {exc}") from exc
    try:
        module = ast.parse(source, filename=path_text)
    except SyntaxError as exc:
        raise CoverageError(f"cannot parse test source {path_text}: {exc}") from exc
    if not any(
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function_text
        for node in ast.walk(module)
    ):
        raise CoverageError(f"pytest node ID {node_id!r} names no test function in its source")
    return path_text, function_text


def _catalog(root: Path, tags: set[str], pairs: set[tuple[str, str]]) -> dict[str, object]:
    path = root / CASE_CATALOG_RELATIVE_PATH
    catalog = _read_json(path, "feature-case catalog")
    if catalog.get("format") != CASE_FORMAT or catalog.get("version") != CASE_FORMAT_VERSION:
        raise CoverageError("feature-case catalog format or version is unsupported")
    if catalog.get("dtd_sha256") != PINNED_DTD_SHA256:
        raise CoverageError("feature-case catalog is not bound to the pinned DTD digest")
    raw_elements = catalog.get("element_cases", [])
    raw_pairs = catalog.get("cases")
    raw_character_data = catalog.get("character_data_cases", [])
    if (
        not isinstance(raw_elements, list)
        or not isinstance(raw_pairs, list)
        or not isinstance(raw_character_data, list)
    ):
        raise CoverageError(
            "feature-case catalog requires element_cases, cases, and character_data_cases arrays"
        )

    elements: dict[str, dict[str, object]] = {}
    all_node_ids: set[str] = set()
    node_owners: dict[str, tuple[str, ...]] = {}
    for index, raw in enumerate(cast(list[object], raw_elements)):
        item = _mapping(raw, f"element_cases[{index}]")
        tag = _string(item.get("xml_name"), f"element_cases[{index}].xml_name")
        if tag not in tags:
            raise CoverageError(f"feature-case catalog names non-DTD element {tag!r}")
        if tag in elements:
            raise CoverageError(f"feature-case catalog repeats element {tag!r}")
        case_id = _string(item.get("case_id"), f"element_cases[{index}].case_id")
        expected_case_id = f"feature-element:{tag}"
        if case_id != expected_case_id:
            raise CoverageError(f"element case ID must be {expected_case_id!r}")
        assertions = _string_list(item.get("assertions"), f"element_cases[{index}].assertions")
        if set(assertions) - _ELEMENT_ASSERTIONS:
            raise CoverageError(f"element case {tag!r} contains unsupported assertions")
        if tag == "CDXML":
            valid_root = {
                "exact_wrapper_type",
                "root_creation",
                "root_mutation",
                "element_round_trip",
            }
            if set(assertions) - valid_root:
                raise CoverageError("CDXML root evidence cannot claim child creation or removal")
        elif {"root_creation", "root_mutation"} & set(assertions):
            raise CoverageError("nonroot element evidence cannot claim CDXML root operations")
        raw_node_id = item.get("pytest_nodeid")
        element_node_id: str | None = None
        if assertions:
            element_node_id = _string(raw_node_id, f"element_cases[{index}].pytest_nodeid")
            if not element_node_id.endswith(f"[{case_id}]"):
                raise CoverageError(f"element pytest node ID must end in [{case_id}]")
            _test_node_function(element_node_id, root)
        elif raw_node_id not in {None, ""}:
            raise CoverageError(f"untested element case {tag!r} cannot name a pytest node")
        evidence = _chemdraw_evidence(
            item.get("chemdraw_evidence", []), root, f"element case {tag}"
        )
        if element_node_id is not None:
            all_node_ids.add(element_node_id)
            node_owner = ("element", tag)
            if element_node_id in node_owners and node_owners[element_node_id] != node_owner:
                raise CoverageError(
                    f"pytest node ID {element_node_id!r} is assigned to multiple features"
                )
            node_owners[element_node_id] = node_owner
        elements[tag] = {
            "case_id": case_id,
            "pytest_nodeid": element_node_id,
            "assertions": assertions,
            "chemdraw_evidence": evidence,
        }

    attribute_cases: dict[tuple[str, str], dict[str, object]] = {}
    for index, raw in enumerate(cast(list[object], raw_pairs)):
        item = _mapping(raw, f"cases[{index}]")
        owner = _string(item.get("owner_tag"), f"cases[{index}].owner_tag")
        xml_name = _string(item.get("xml_attribute"), f"cases[{index}].xml_attribute")
        key = (owner, xml_name)
        if key not in pairs:
            raise CoverageError(f"feature-case catalog names non-DTD owner-attribute pair {key!r}")
        if key in attribute_cases:
            raise CoverageError(f"feature-case catalog repeats owner-attribute pair {key!r}")
        case_id = _string(item.get("case_id"), f"cases[{index}].case_id")
        expected_case_id = f"feature:{owner}@{xml_name}"
        if case_id != expected_case_id:
            raise CoverageError(f"attribute case ID must be {expected_case_id!r}")
        assertions = _string_list(item.get("assertions"), f"cases[{index}].assertions")
        if set(assertions) - _ATTRIBUTE_ASSERTIONS:
            raise CoverageError(
                f"attribute case {owner}@{xml_name} contains unsupported assertions"
            )
        raw_node_id = item.get("pytest_nodeid")
        attribute_node_id: str | None = None
        if assertions:
            attribute_node_id = _string(raw_node_id, f"cases[{index}].pytest_nodeid")
            if not attribute_node_id.endswith(f"[{case_id}]"):
                raise CoverageError(f"attribute pytest node ID must end in [{case_id}]")
            _test_node_function(attribute_node_id, root)
        elif raw_node_id not in {None, ""}:
            raise CoverageError(
                f"untested attribute case {owner}@{xml_name} cannot name a pytest node"
            )
        evidence = _chemdraw_evidence(
            item.get("chemdraw_evidence", []), root, f"attribute case {owner}@{xml_name}"
        )
        if assertions:
            if attribute_node_id is None:
                raise CoverageError(f"attribute case {owner}@{xml_name} has no test node ID")
            all_node_ids.add(attribute_node_id)
            attribute_node_owner = ("attribute", owner, xml_name)
            if (
                attribute_node_id in node_owners
                and node_owners[attribute_node_id] != attribute_node_owner
            ):
                raise CoverageError(
                    f"pytest node ID {attribute_node_id!r} is assigned to multiple features"
                )
            node_owners[attribute_node_id] = attribute_node_owner
        attribute_cases[key] = {
            "case_id": case_id,
            "pytest_nodeid": attribute_node_id,
            "assertions": assertions,
            "chemdraw_evidence": evidence,
        }
    character_cases: dict[str, dict[str, object]] = {}
    for index, raw in enumerate(cast(list[object], raw_character_data)):
        item = _mapping(raw, f"character_data_cases[{index}]")
        tag = _string(item.get("xml_name"), f"character_data_cases[{index}].xml_name")
        if tag not in {"s", "spectrum"} or tag not in tags:
            raise CoverageError(f"character-data case names non-PCDATA feature {tag!r}")
        if tag in character_cases:
            raise CoverageError(f"feature-case catalog repeats character-data element {tag!r}")
        case_id = _string(item.get("case_id"), f"character_data_cases[{index}].case_id")
        expected_case_id = f"feature-character:{tag}"
        if case_id != expected_case_id:
            raise CoverageError(f"character-data case ID must be {expected_case_id!r}")
        assertions = _string_list(
            item.get("assertions"), f"character_data_cases[{index}].assertions"
        )
        if set(assertions) - _CHARACTER_ASSERTIONS:
            raise CoverageError(f"character-data case {tag!r} has unsupported assertions")
        raw_node_id = item.get("pytest_nodeid")
        character_node_id: str | None = None
        if assertions:
            character_node_id = _string(raw_node_id, f"character_data_cases[{index}].pytest_nodeid")
            if not character_node_id.endswith(f"[{case_id}]"):
                raise CoverageError(f"character-data pytest node ID must end in [{case_id}]")
            _test_node_function(character_node_id, root)
            character_node_owner = ("character_data", tag)
            if (
                character_node_id in node_owners
                and node_owners[character_node_id] != character_node_owner
            ):
                raise CoverageError(
                    f"pytest node ID {character_node_id!r} is assigned to multiple features"
                )
            node_owners[character_node_id] = character_node_owner
            all_node_ids.add(character_node_id)
        elif raw_node_id not in {None, ""}:
            raise CoverageError(f"untested character-data case {tag!r} cannot name a pytest node")
        character_cases[tag] = {
            "case_id": case_id,
            "pytest_nodeid": character_node_id,
            "assertions": assertions,
            "chemdraw_evidence": _chemdraw_evidence(
                item.get("chemdraw_evidence", []), root, f"character-data case {tag}"
            ),
        }
    catalog["_elements_by_tag"] = elements
    catalog["_pairs_by_key"] = attribute_cases
    catalog["_character_cases_by_tag"] = character_cases
    sdk_cases, sdk_digest = _sdk_extension_cases(root, all_node_ids, node_owners)
    catalog["_sdk_extensions_by_key"] = sdk_cases
    catalog["_sdk_extension_sha256"] = sdk_digest
    catalog["_node_ids"] = tuple(sorted(all_node_ids))
    catalog["_node_owners"] = node_owners
    catalog["_sha256"] = _sha256(path.read_bytes())
    return catalog


def _sdk_extension_cases(
    root: Path,
    all_node_ids: set[str],
    node_owners: dict[str, tuple[str, ...]],
) -> tuple[dict[tuple[str, str], dict[str, object]], str]:
    path = root / SDK_EXTENSION_CASE_CATALOG_RELATIVE_PATH
    catalog = _read_json(path, "SDK-extension feature-case catalog")
    if (
        catalog.get("format") != SDK_EXTENSION_CASE_FORMAT
        or catalog.get("version") != SDK_EXTENSION_CASE_FORMAT_VERSION
    ):
        raise CoverageError("SDK-extension feature-case catalog format or version is unsupported")
    raw_cases = catalog.get("cases")
    if not isinstance(raw_cases, list):
        raise CoverageError("SDK-extension feature-case catalog requires a cases array")
    if catalog.get("source_evidence") != "schema/sources/sdk/evidence.json":
        raise CoverageError("SDK-extension feature catalog names an unexpected source catalog")
    evidence = _read_json(root / "schema" / "sources" / "sdk" / "evidence.json", "SDK evidence")
    evidence_rows = evidence.get("sdk_only_properties")
    if not isinstance(evidence_rows, list):
        raise CoverageError("SDK evidence must contain sdk_only_properties")
    expected_pairs: set[tuple[str, str]] = set()
    for index, raw in enumerate(cast(list[object], evidence_rows)):
        fact = _mapping(raw, f"SDK evidence sdk_only_properties[{index}]")
        if fact.get("classification") not in {
            "sdk_documented_xml_attribute_not_in_pinned_dtd",
            "case_variant_of_dtd_xml_attribute",
        }:
            continue
        expected_pairs.add(
            (
                _string(fact.get("owner_xml_name"), "SDK evidence owner_xml_name"),
                _string(fact.get("xml_name"), "SDK evidence xml_name"),
            )
        )

    def register_node(node_id: str, owner: tuple[str, ...], location: str) -> None:
        _test_node_function(node_id, root)
        if node_id in node_owners and node_owners[node_id] != owner:
            raise CoverageError(f"pytest node ID {node_id!r} is assigned to multiple features")
        node_owners[node_id] = owner
        all_node_ids.add(node_id)

    cases: dict[tuple[str, str], dict[str, object]] = {}
    for index, raw in enumerate(cast(list[object], raw_cases)):
        location = f"sdk_extension_cases[{index}]"
        item = _mapping(raw, location)
        owner = _string(item.get("owner_tag"), f"{location}.owner_tag")
        xml_name = _string(item.get("xml_attribute"), f"{location}.xml_attribute")
        key = (owner, xml_name)
        if key in cases:
            raise CoverageError(f"SDK-extension catalog repeats owner-attribute pair {key!r}")
        case_id = _string(item.get("case_id"), f"{location}.case_id")
        expected_case_id = f"feature-sdk:{owner}@{xml_name}"
        if case_id != expected_case_id:
            raise CoverageError(f"SDK-extension case ID must be {expected_case_id!r}")
        _string(item.get("source_xml"), f"{location}.source_xml")
        _string(item.get("sdk_type"), f"{location}.sdk_type")

        raw_assertions = _string_list(item.get("assertions"), f"{location}.assertions")
        if frozenset(raw_assertions) != _SDK_RAW_ASSERTIONS:
            raise CoverageError(f"SDK-extension case {case_id!r} has unsupported raw assertions")
        raw_node_id = _string(item.get("pytest_nodeid"), f"{location}.pytest_nodeid")
        if not raw_node_id.endswith(f"[{case_id}]"):
            raise CoverageError(f"SDK-extension raw pytest node ID must end in [{case_id}]")
        register_node(raw_node_id, ("sdk_raw", owner, xml_name), location)

        recipe = _mapping(item.get("typed_recipe"), f"{location}.typed_recipe")
        _string(recipe.get("expected_python_type"), f"{location}.typed_recipe.expected_python_type")
        if "expected_python_value" not in recipe or "mutation_python_value" not in recipe:
            raise CoverageError(f"SDK-extension typed recipe {case_id!r} lacks typed values")
        _string(recipe.get("mutation_xml"), f"{location}.typed_recipe.mutation_xml")
        required = _string_list(
            recipe.get("required_assertions"), f"{location}.typed_recipe.required_assertions"
        )
        if set(required) - _SDK_TYPED_ASSERTIONS:
            raise CoverageError(f"SDK-extension typed recipe {case_id!r} has unknown assertions")
        typed_node_raw = recipe.get("pytest_nodeid")
        typed_node: str | None = None
        if typed_node_raw not in {None, ""}:
            typed_node = _string(typed_node_raw, f"{location}.typed_recipe.pytest_nodeid")
            if not typed_node.endswith(f"[{case_id}]"):
                raise CoverageError(f"SDK-extension typed pytest node ID must end in [{case_id}]")
            register_node(typed_node, ("sdk_typed", owner, xml_name), location)
        cases[key] = {
            "case_id": case_id,
            "pytest_nodeid": typed_node,
            "raw_pytest_nodeid": raw_node_id,
            "assertions": required,
            "raw_assertions": raw_assertions,
            "typed_recipe": recipe,
        }
    if len(cases) != SDK_EXTENSION_PAIR_COUNT:
        raise CoverageError(
            "SDK-extension catalog must contain "
            f"{SDK_EXTENSION_PAIR_COUNT} rows, found {len(cases)}"
        )
    if set(cases) != expected_pairs:
        missing = sorted(expected_pairs - set(cases))
        extra = sorted(set(cases) - expected_pairs)
        raise CoverageError(
            "SDK-extension feature catalog does not match source-evidence inventory "
            f"(missing={missing!r}, extra={extra!r})"
        )
    return cases, _sha256(path.read_bytes())


def _chemdraw_evidence(value: object, root: Path, location: str) -> tuple[dict[str, str], ...]:
    if not isinstance(value, list):
        raise CoverageError(f"{location}.chemdraw_evidence must be an array")
    records: list[dict[str, str]] = []
    for index, raw in enumerate(cast(list[object], value)):
        item = _mapping(raw, f"{location}.chemdraw_evidence[{index}]")
        required = ("application", "version", "verified_on", "artifact", "observation")
        record = {
            key: _string(item.get(key), f"{location}.chemdraw_evidence[{index}].{key}")
            for key in required
        }
        if Path(record["artifact"]).is_absolute() or ".." in Path(record["artifact"]).parts:
            raise CoverageError("ChemDraw evidence artifacts must be repository-relative paths")
        artifact = root / record["artifact"]
        if not artifact.is_file():
            raise CoverageError(f"ChemDraw evidence artifact is missing: {record['artifact']}")
        records.append(record)
    return tuple(records)


def _model_for_tag(tag: str) -> tuple[str | None, type[CDXMLElement] | None]:
    model = OBJECT_BY_XML_TAG.get(tag)
    if model is None:
        return None, None
    spec_id = next(
        (key for key, metadata in OBJECT_METADATA.items() if metadata.xml_tag == tag), None
    )
    return spec_id, model


def _property_for_attribute(
    tag: str,
    xml_name: str,
) -> tuple[
    str | None,
    PropertyMetadata | None,
    Field[object] | RefField[object] | RefListField[object] | None,
]:
    spec_id, model = _model_for_tag(tag)
    if spec_id is None or model is None:
        return None, None, None
    metadata = OBJECT_METADATA[spec_id]
    matches = [
        (property_id, prop)
        for property_id, prop in metadata.properties.items()
        if (prop.xml_name == xml_name or xml_name in prop.xml_aliases) and spec_id in prop.owners
    ]
    if len(matches) != 1:
        return None, None, None
    property_id, prop = matches[0]
    raw_descriptor = getattr(model, prop.name, None)
    descriptor: Field[object] | RefField[object] | RefListField[object] | None = None
    if isinstance(raw_descriptor, _FIELD_DESCRIPTORS) and raw_descriptor.property_id == property_id:
        descriptor = cast(Field[object] | RefField[object] | RefListField[object], raw_descriptor)
    return property_id, prop, descriptor


def _test_state(
    tests: dict[str, tuple[str, ...]],
    passed: set[str],
    failed: set[str],
    skipped: set[str],
    *,
    required: tuple[str, ...],
) -> tuple[bool, dict[str, object]]:
    states: dict[str, object] = {}
    for operation, node_ids in tests.items():
        states[operation] = {
            "declared": bool(node_ids),
            "passed": bool(node_ids) and all(node in passed for node in node_ids),
            "failed": [node for node in node_ids if node in failed],
            "skipped": [node for node in node_ids if node in skipped],
            "not_run": [node for node in node_ids if node not in passed | failed | skipped],
            "test_ids": list(node_ids),
        }
    complete = all(tests.get(operation) for operation in required) and all(
        node in passed for operation in required for node in tests[operation]
    )
    return complete, states


def _attribute_operations(case: dict[str, object]) -> dict[str, tuple[str, ...]]:
    assertions = set(cast(tuple[str, ...], case["assertions"]))
    node_id = case["pytest_nodeid"]
    if not isinstance(node_id, str):
        return {operation: () for operation in TEST_OPERATIONS}
    return {
        "read": (node_id,)
        if {"source_lexical_value", "typed_read_value_and_python_type"} <= assertions
        else (),
        "write": (node_id,) if "mutation_lexical_value" in assertions else (),
        "mutation": (node_id,) if "typed_mutation" in assertions else (),
        "round_trip": (node_id,) if "serialization_reload_readback" in assertions else (),
    }


def _element_operations(tag: str, case: dict[str, object]) -> dict[str, tuple[str, ...]]:
    assertions = set(cast(tuple[str, ...], case["assertions"]))
    node_id = case["pytest_nodeid"]
    if not isinstance(node_id, str):
        return {operation: () for operation in ELEMENT_OPERATIONS}
    if tag == "CDXML":
        return {
            "dispatch": (node_id,) if {"root_creation", "exact_wrapper_type"} <= assertions else (),
            "mutation": (node_id,) if {"root_creation", "root_mutation"} <= assertions else (),
            "round_trip": (node_id,) if "element_round_trip" in assertions else (),
        }
    return {
        "dispatch": (node_id,) if "exact_wrapper_type" in assertions else (),
        "mutation": (node_id,) if {"element_creation", "element_removal"} <= assertions else (),
        "round_trip": (node_id,) if "element_round_trip" in assertions else (),
    }


def _character_operations(case: dict[str, object]) -> dict[str, tuple[str, ...]]:
    assertions = set(cast(tuple[str, ...], case["assertions"]))
    node_id = case["pytest_nodeid"]
    if not isinstance(node_id, str):
        return {operation: () for operation in TEST_OPERATIONS}
    return {
        "read": (node_id,)
        if {"storage_lexical_value", "typed_read_value_and_python_type"} <= assertions
        else (),
        "write": (node_id,) if "mutation_lexical_value" in assertions else (),
        "mutation": (node_id,) if "typed_mutation" in assertions else (),
        "round_trip": (node_id,) if "serialization_reload_readback" in assertions else (),
    }


def _sdk_extension_operations(case: dict[str, object]) -> dict[str, tuple[str, ...]]:
    assertions = set(cast(tuple[str, ...], case["assertions"]))
    node_id = case["pytest_nodeid"]
    if not isinstance(node_id, str):
        return {operation: () for operation in TEST_OPERATIONS}
    return {
        "read": (node_id,) if "typed_read_value_and_python_type" in assertions else (),
        "write": (node_id,) if "mutation_lexical_value" in assertions else (),
        "mutation": (node_id,) if "typed_mutation" in assertions else (),
        "round_trip": (node_id,) if "serialization_reload_typed_readback" in assertions else (),
    }


def _parse_junit(path: Path) -> tuple[dict[str, str], str]:
    try:
        raw = path.read_bytes()
        root = ElementTree.fromstring(raw)
    except (OSError, ElementTree.ParseError) as exc:
        raise CoverageError(f"cannot read JUnit XML report {path}: {exc}") from exc
    outcomes: dict[str, str] = {}
    for case in root.iter():
        if case.tag.rsplit("}", 1)[-1] != "testcase":
            continue
        classname = case.get("classname")
        name = case.get("name")
        if not classname or not name:
            raise CoverageError("JUnit testcase is missing classname or name")
        module_path = classname.replace(".", "/") + ".py"
        node_id = f"{module_path}::{name}"
        result = "passed"
        for child in case:
            local_name = child.tag.rsplit("}", 1)[-1]
            if local_name in {"failure", "error"}:
                result = "failed"
                break
            if local_name == "skipped":
                result = "skipped"
                break
        if node_id in outcomes:
            raise CoverageError(f"JUnit report repeats testcase {node_id!r}")
        outcomes[node_id] = result
    return outcomes, _sha256(raw)


def _fingerprints(root: Path, schema: Schema, catalog: dict[str, object]) -> dict[str, object]:
    del schema
    source_roots = (
        root / "src",
        root / "tools" / "schema_compiler",
        root / "tools" / "schema_importer",
        root / "tests",
        root / "schema" / "canonical",
        root / "schema" / "sources",
        root / "schema" / "coverage",
        root / "schema" / "overrides",
    )
    source_paths = [
        path
        for folder in source_roots
        for path in sorted(folder.rglob("*"))
        if path.is_file()
        and "__pycache__" not in path.parts
        and ".pytest_cache" not in path.parts
        and ".ruff_cache" not in path.parts
        and path.suffix != ".pyc"
    ]
    source_paths.extend(
        (root / "pyproject.toml", root / "uv.lock", root / "schema" / "schema.lock.json")
    )
    source_hashes = {
        path.relative_to(root).as_posix(): _sha256(path.read_bytes())
        for path in sorted(set(source_paths))
    }
    try:
        lock = json.loads((root / LOCK_RELATIVE_PATH).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CoverageError(f"cannot read schema lock for test-run fingerprints: {exc}") from exc
    lock_hash = _sha256(_json_bytes(lock))
    fingerprints: dict[str, object] = {
        "dtd_sha256": PINNED_DTD_SHA256,
        "schema_hash": schema_hash(root)[0],
        "schema_lock_sha256": lock_hash,
        "feature_case_catalog_sha256": cast(str, catalog["_sha256"]),
        "sdk_extension_case_catalog_sha256": cast(str, catalog["_sdk_extension_sha256"]),
        "files": source_hashes,
    }
    fingerprints["fingerprint_sha256"] = _sha256(_json_bytes(fingerprints))
    return fingerprints


def _test_run_payload(
    *,
    dtd_digest: str,
    fingerprints: dict[str, object],
    outcomes: dict[str, str],
    node_ids: tuple[str, ...],
    junit_digest: str,
) -> dict[str, object]:
    return {
        "format": RUN_FORMAT,
        "format_version": RUN_FORMAT_VERSION,
        "dtd_sha256": dtd_digest,
        "fingerprints": fingerprints,
        "junit_sha256": junit_digest,
        "cases": [
            {"test_id": node_id, "status": outcomes.get(node_id, "not_run")}
            for node_id in sorted(node_ids)
        ],
    }


def run_feature_tests(
    root: Path,
    schema: Schema,
    *,
    run_output: Path,
    pytest_arguments: list[str],
    junit_output: Path | None = None,
) -> int:
    """Run pytest and bind its JUnit outcomes to fingerprints captured before execution."""
    dtd_digest, dtd_elements = _pinned_inventory(root)
    tags = {item.xml_name for item in dtd_elements}
    pairs = {(item.xml_name, attr.name) for item in dtd_elements for attr in item.attributes}
    catalog = _catalog(root, tags, pairs)
    start_fingerprints = _fingerprints(root, schema, catalog)
    if run_output.resolve().is_relative_to(root.resolve()):
        raise CoverageError("test-run evidence output must be outside the fingerprinted repository")
    if run_output.exists():
        raise CoverageError(f"test-run evidence output already exists: {run_output}")
    if junit_output is not None and junit_output.resolve().is_relative_to(root.resolve()):
        raise CoverageError("JUnit output must be outside the fingerprinted repository")
    if junit_output is not None and junit_output.exists():
        raise CoverageError(f"JUnit output already exists: {junit_output}")
    if junit_output is not None and junit_output.resolve() == run_output.resolve():
        raise CoverageError("JUnit output and run evidence must use different paths")
    if junit_output is None:
        with tempfile.TemporaryDirectory(prefix="cdxml-om-feature-tests-") as temp_dir:
            junit_path = Path(temp_dir) / "junit.xml"
            return _run_pytest_and_record(
                root,
                schema,
                catalog,
                dtd_digest,
                start_fingerprints,
                run_output,
                junit_path,
                pytest_arguments,
            )
    return _run_pytest_and_record(
        root,
        schema,
        catalog,
        dtd_digest,
        start_fingerprints,
        run_output,
        junit_output,
        pytest_arguments,
    )


def _run_pytest_and_record(
    root: Path,
    schema: Schema,
    catalog: dict[str, object],
    dtd_digest: str,
    start_fingerprints: dict[str, object],
    run_output: Path,
    junit_path: Path,
    pytest_arguments: list[str],
) -> int:
    if junit_path.exists():
        raise CoverageError(f"JUnit output already exists: {junit_path}")
    if any(argument.startswith("--junitxml") for argument in pytest_arguments):
        raise CoverageError("pass JUnit output using the test-features --junitxml option")
    command = [
        sys.executable,
        "-m",
        "pytest",
        *pytest_arguments,
        f"--junitxml={junit_path}",
    ]
    result = subprocess.run(command, cwd=root, check=False)
    current_fingerprints = _fingerprints(root, schema, catalog)
    if start_fingerprints != current_fingerprints:
        raise CoverageError(
            "source files changed while feature tests were running; run evidence discarded"
        )
    outcomes, junit_digest = _parse_junit(junit_path)
    payload = _test_run_payload(
        dtd_digest=dtd_digest,
        fingerprints=start_fingerprints,
        outcomes=outcomes,
        node_ids=cast(tuple[str, ...], catalog["_node_ids"]),
        junit_digest=junit_digest,
    )
    run_output.parent.mkdir(parents=True, exist_ok=True)
    try:
        with run_output.open("xb") as stream:
            stream.write(_json_bytes(payload))
    except FileExistsError as exc:
        raise CoverageError(f"test-run evidence output already exists: {run_output}") from exc
    return result.returncode


def _run_outcomes(
    root: Path,
    schema: Schema,
    catalog: dict[str, object],
    test_run_path: Path | None,
) -> tuple[dict[str, str], dict[str, object]]:
    if test_run_path is None:
        return {}, {"provided": False, "identity_matches": False, "status": "not_provided"}
    run = _read_json(test_run_path, "feature test-run evidence")
    if run.get("format") != RUN_FORMAT or run.get("format_version") != RUN_FORMAT_VERSION:
        raise CoverageError("feature test-run format or version is unsupported")
    if run.get("dtd_sha256") != PINNED_DTD_SHA256:
        raise CoverageError("feature test-run is bound to a different DTD")
    if catalog.get("_elements_by_tag") is None:
        raise CoverageError("feature catalog was not normalized")
    expected_fingerprints = _fingerprints(root, schema, catalog)
    actual_fingerprints = _mapping(run.get("fingerprints"), "test-run fingerprints")
    if actual_fingerprints != expected_fingerprints:
        raise CoverageError(
            "feature test-run is stale: schema, generated/runtime source, tests, or catalog changed"
        )
    raw_cases = run.get("cases")
    if not isinstance(raw_cases, list):
        raise CoverageError("feature test-run cases must be an array")
    outcomes: dict[str, str] = {}
    for index, raw in enumerate(cast(list[object], raw_cases)):
        item = _mapping(raw, f"test-run cases[{index}]")
        node_id = _string(item.get("test_id"), f"test-run cases[{index}].test_id")
        status = _string(item.get("status"), f"test-run cases[{index}].status")
        if status not in {"passed", "failed", "skipped", "not_run"}:
            raise CoverageError(f"invalid status {status!r} for {node_id!r}")
        if node_id in outcomes:
            raise CoverageError(f"feature test-run repeats node ID {node_id!r}")
        outcomes[node_id] = status
    expected_ids = set(cast(tuple[str, ...], catalog["_node_ids"]))
    if set(outcomes) != expected_ids:
        raise CoverageError(
            "feature test-run case IDs do not match the current feature-case catalog"
        )
    passed = {node for node, status in outcomes.items() if status == "passed"}
    failed = {node for node, status in outcomes.items() if status == "failed"}
    skipped = {node for node, status in outcomes.items() if status == "skipped"}
    return outcomes, {
        "provided": True,
        "identity_matches": True,
        "status": "current",
        "junit_sha256": _string(run.get("junit_sha256"), "test-run junit_sha256"),
        "passed_case_count": len(passed),
        "failed_case_count": len(failed),
        "skipped_case_count": len(skipped),
        "not_run_case_count": len(expected_ids - passed - failed - skipped),
    }


def _summarize(
    rows: list[dict[str, object]], denominator: int, levels: tuple[str, ...]
) -> dict[str, int]:
    summary = {"total": denominator}
    for level in levels:
        summary[level] = sum(bool(row.get(level)) for row in rows)
    return summary


def _contains_pcdata(content_model: object) -> bool:
    if content_model is None:
        return False
    if getattr(content_model, "kind", None) == "pcdata":
        return True
    return any(_contains_pcdata(child) for child in getattr(content_model, "children", ()))


def build_coverage_report(
    root: Path,
    schema: Schema,
    *,
    test_run_path: Path | None = None,
) -> dict[str, object]:
    """Build a deterministic report using the pinned DTD and checked-in feature cases."""
    differences = compare_outputs(compile_outputs(schema, root), root)
    if differences:
        raise CoverageError("generated schema outputs are stale; run the schema compiler build")
    dtd_digest, dtd_elements = _pinned_inventory(root)
    tags = {item.xml_name for item in dtd_elements}
    pairs = {(item.xml_name, attr.name) for item in dtd_elements for attr in item.attributes}
    catalog = _catalog(root, tags, pairs)
    outcomes, run_metadata = _run_outcomes(root, schema, catalog, test_run_path)
    passed = {node for node, status in outcomes.items() if status == "passed"}
    failed = {node for node, status in outcomes.items() if status == "failed"}
    skipped = {node for node, status in outcomes.items() if status == "skipped"}

    element_cases = cast(dict[str, dict[str, object]], catalog["_elements_by_tag"])
    pair_cases = cast(dict[tuple[str, str], dict[str, object]], catalog["_pairs_by_key"])
    character_cases = cast(dict[str, dict[str, object]], catalog["_character_cases_by_tag"])
    sdk_extension_cases = cast(
        dict[tuple[str, str], dict[str, object]], catalog["_sdk_extensions_by_key"]
    )
    element_rows: list[dict[str, object]] = []
    attribute_rows: list[dict[str, object]] = []
    character_data_rows: list[dict[str, object]] = []
    sdk_extension_rows: list[dict[str, object]] = []
    for dtd_element in dtd_elements:
        tag = dtd_element.xml_name
        spec_id, model = _model_for_tag(tag)
        if tag == "CDXML" and model is None:
            mapping = "document-root-facade"
            implemented = True
            typed = False
        elif model is not None and spec_id is not None:
            mapping = "generated-model"
            implemented = True
            typed = getattr(model, "__spec_id__", None) == spec_id
        else:
            mapping = "unmapped"
            implemented = False
            typed = False
        evidence = element_cases.get(tag, {"assertions": (), "chemdraw_evidence": ()})
        tests = _element_operations(tag, evidence)
        tested, test_states = _test_state(
            tests, passed, failed, skipped, required=("dispatch", "mutation")
        )
        round_trip_state, _ = _test_state(tests, passed, failed, skipped, required=("round_trip",))
        chem_evidence = cast(tuple[dict[str, str], ...], evidence["chemdraw_evidence"])
        element_rows.append(
            {
                "xml_name": tag,
                "known": True,
                "canonical_object_known": spec_id is not None,
                "implemented": implemented,
                "typed": typed,
                "tested": tested,
                "test_case_declared": evidence.get("pytest_nodeid") is not None,
                "round_trip_verified": round_trip_state,
                "chemdraw_verified": bool(chem_evidence),
                "mapping": mapping,
                "canonical_object_id": spec_id,
                "feature_case_id": evidence.get("case_id"),
                "pytest_nodeid": evidence.get("pytest_nodeid"),
                "dtd_declaration_type": dtd_element.declaration_type,
                "dtd_children": list(dtd_element.children),
                "dtd_content_model": (
                    asdict(dtd_element.content_model)
                    if dtd_element.content_model is not None
                    else None
                ),
                "operation_applicability": {
                    "element_create_remove": "not_applicable_document_root"
                    if tag == "CDXML"
                    else "required"
                },
                "tests": test_states,
                "chemdraw_evidence": list(chem_evidence),
            }
        )
        for dtd_attribute in dtd_element.attributes:
            name = dtd_attribute.name
            prop_id, prop, descriptor = _property_for_attribute(tag, name)
            runtime_codec: str | None = None
            implemented_attribute = False
            if prop_id is not None and prop is not None and descriptor is not None:
                runtime_codec = "enum" if prop.enum is not None else prop.codec
                implemented_attribute = (
                    supports_property_codec(prop_id)
                    and prop.storage == "attribute"
                    and model is not None
                )
            pair_evidence = pair_cases.get(
                (tag, name), {"assertions": (), "pytest_nodeid": None, "chemdraw_evidence": ()}
            )
            attribute_tests = _attribute_operations(pair_evidence)
            attribute_tested, attribute_states = _test_state(
                attribute_tests,
                passed,
                failed,
                skipped,
                required=("read", "write", "mutation"),
            )
            round_trip_verified, _ = _test_state(
                attribute_tests,
                passed,
                failed,
                skipped,
                required=("round_trip",),
            )
            chem_attribute = cast(tuple[dict[str, str], ...], pair_evidence["chemdraw_evidence"])
            attribute_rows.append(
                {
                    "owner_xml_name": tag,
                    "xml_name": name,
                    "known": True,
                    "canonical_property_known": prop_id is not None,
                    "implemented": implemented_attribute,
                    "typed": descriptor is not None,
                    "tested": attribute_tested,
                    "test_case_declared": pair_evidence.get("pytest_nodeid") is not None,
                    "round_trip_verified": round_trip_verified,
                    "chemdraw_verified": bool(chem_attribute),
                    "dtd_type": dtd_attribute.declared_type,
                    "dtd_required": dtd_attribute.required,
                    "dtd_default_kind": dtd_attribute.default_kind,
                    "dtd_default_value": dtd_attribute.default_value,
                    "dtd_enum_values": list(dtd_attribute.enum_values),
                    "canonical_property_id": prop_id,
                    "runtime_codec": runtime_codec,
                    "feature_case_id": pair_evidence.get("case_id"),
                    "pytest_nodeid": pair_evidence.get("pytest_nodeid"),
                    "tests": attribute_states,
                    "chemdraw_evidence": list(chem_attribute),
                }
            )

    for dtd_element in dtd_elements:
        if not _contains_pcdata(dtd_element.content_model):
            continue
        tag = dtd_element.xml_name
        spec_id, model = _model_for_tag(tag)
        content_property_id: str | None = None
        content_descriptor = False
        content_codec_supported = False
        if spec_id is not None and model is not None:
            metadata = OBJECT_METADATA[spec_id]
            text_properties = [
                (property_id, prop)
                for property_id, prop in metadata.properties.items()
                if prop.storage == "text" and spec_id in prop.owners
            ]
            if len(text_properties) == 1:
                content_property_id, text_property = text_properties[0]
                raw_descriptor = getattr(model, text_property.name, None)
                content_descriptor = (
                    isinstance(raw_descriptor, _FIELD_DESCRIPTORS)
                    and raw_descriptor.property_id == content_property_id
                )
                content_codec_supported = supports_property_codec(content_property_id)
        case = character_cases.get(
            tag,
            {
                "case_id": f"feature-character:{tag}",
                "pytest_nodeid": None,
                "assertions": (),
                "chemdraw_evidence": (),
            },
        )
        character_tests = _character_operations(case)
        tested, test_states = _test_state(
            character_tests, passed, failed, skipped, required=("read", "write", "mutation")
        )
        round_trip_verified, _ = _test_state(
            character_tests, passed, failed, skipped, required=("round_trip",)
        )
        character_evidence = cast(tuple[dict[str, str], ...], case["chemdraw_evidence"])
        character_data_rows.append(
            {
                "xml_name": tag,
                "known": True,
                "canonical_text_storage_known": content_property_id is not None,
                "implemented": content_descriptor and content_codec_supported,
                "typed": content_descriptor,
                "tested": tested,
                "test_case_declared": case.get("pytest_nodeid") is not None,
                "round_trip_verified": round_trip_verified,
                "chemdraw_verified": bool(character_evidence),
                "canonical_property_id": content_property_id,
                "feature_case_id": case.get("case_id"),
                "pytest_nodeid": case.get("pytest_nodeid"),
                "dtd_content_model": asdict(dtd_element.content_model)
                if dtd_element.content_model is not None
                else None,
                "tests": test_states,
                "chemdraw_evidence": list(character_evidence),
            }
        )

    for (owner_tag, xml_name), evidence in sorted(sdk_extension_cases.items()):
        prop_id, prop, descriptor = _property_for_attribute(owner_tag, xml_name)
        implemented = (
            prop_id is not None
            and prop is not None
            and descriptor is not None
            and prop.storage == "attribute"
            and supports_property_codec(prop_id)
        )
        operations = _sdk_extension_operations(evidence)
        tested, test_states = _test_state(
            operations, passed, failed, skipped, required=("read", "write", "mutation")
        )
        round_trip_verified, _ = _test_state(
            operations, passed, failed, skipped, required=("round_trip",)
        )
        raw_node_id = cast(str, evidence["raw_pytest_nodeid"])
        raw_verified = raw_node_id in passed
        sdk_extension_rows.append(
            {
                "owner_xml_name": owner_tag,
                "xml_name": xml_name,
                "known": True,
                "canonical_property_known": prop_id is not None,
                "implemented": implemented,
                "typed": descriptor is not None,
                "test_case_declared": evidence.get("pytest_nodeid") is not None,
                "tested": tested,
                "round_trip_verified": round_trip_verified,
                "raw_preservation_tested": raw_verified,
                "chemdraw_verified": False,
                "canonical_property_id": prop_id,
                "runtime_codec": ("enum" if prop.enum is not None else prop.codec)
                if prop is not None
                else None,
                "feature_case_id": evidence["case_id"],
                "pytest_nodeid": evidence.get("pytest_nodeid"),
                "raw_preservation_nodeid": raw_node_id,
                "tests": test_states,
                "raw_preservation_test": {
                    "passed": raw_verified,
                    "failed": [raw_node_id] if raw_node_id in failed else [],
                    "skipped": [raw_node_id] if raw_node_id in skipped else [],
                    "not_run": [raw_node_id]
                    if raw_node_id not in passed | failed | skipped
                    else [],
                },
            }
        )

    element_levels = (
        "known",
        "canonical_object_known",
        "implemented",
        "typed",
        "test_case_declared",
        "tested",
        "round_trip_verified",
        "chemdraw_verified",
    )
    attribute_levels = (
        "known",
        "canonical_property_known",
        "implemented",
        "typed",
        "test_case_declared",
        "tested",
        "round_trip_verified",
        "chemdraw_verified",
    )
    element_summary = _summarize(element_rows, 53, element_levels)
    attribute_summary = _summarize(attribute_rows, 762, attribute_levels)
    character_summary = _summarize(
        character_data_rows,
        len(character_data_rows),
        (
            "known",
            "canonical_text_storage_known",
            "implemented",
            "typed",
            "test_case_declared",
            "tested",
            "round_trip_verified",
            "chemdraw_verified",
        ),
    )
    sdk_extension_summary = _summarize(
        sdk_extension_rows,
        SDK_EXTENSION_PAIR_COUNT,
        (
            "known",
            "canonical_property_known",
            "implemented",
            "typed",
            "test_case_declared",
            "tested",
            "round_trip_verified",
            "raw_preservation_tested",
            "chemdraw_verified",
        ),
    )

    stage_gaps: dict[str, object] = {}
    for stage in (
        "implemented",
        "typed",
        "test_case_declared",
        "tested",
        "round_trip_verified",
        "chemdraw_verified",
    ):
        stage_gaps[stage] = {
            "elements": [row["xml_name"] for row in element_rows if not bool(row.get(stage))],
            "owner_attribute_pairs": [
                {"owner_xml_name": row["owner_xml_name"], "xml_name": row["xml_name"]}
                for row in attribute_rows
                if not bool(row.get(stage))
            ],
            "character_data": [
                row["xml_name"] for row in character_data_rows if not bool(row.get(stage))
            ],
            "sdk_extension_pairs": [
                {"owner_xml_name": row["owner_xml_name"], "xml_name": row["xml_name"]}
                for row in sdk_extension_rows
                if not bool(row.get(stage))
            ],
        }
    stage_gaps["canonical_schema_mapping"] = {
        "elements": [
            row["xml_name"] for row in element_rows if not bool(row.get("canonical_object_known"))
        ],
        "owner_attribute_pairs": [
            {"owner_xml_name": row["owner_xml_name"], "xml_name": row["xml_name"]}
            for row in attribute_rows
            if not bool(row.get("canonical_property_known"))
        ],
        "character_data": [
            row["xml_name"]
            for row in character_data_rows
            if not bool(row.get("canonical_text_storage_known"))
        ],
        "sdk_extension_pairs": [
            {"owner_xml_name": row["owner_xml_name"], "xml_name": row["xml_name"]}
            for row in sdk_extension_rows
            if not bool(row.get("canonical_property_known"))
        ],
    }

    fingerprints = _fingerprints(root, schema, catalog)
    unresolved_children = [
        {"owner_xml_name": item.xml_name, "child_xml_name": child}
        for item in dtd_elements
        for child in item.children
        if child not in tags
    ]
    return {
        "format": REPORT_FORMAT,
        "format_version": REPORT_FORMAT_VERSION,
        "baseline": {
            "dtd_path": DTD_RELATIVE_PATH,
            "dtd_sha256": dtd_digest,
            "element_count": 53,
            "nonroot_element_count": 52,
            "owner_attribute_pair_count": 762,
        },
        "structure": {
            "unresolved_dtd_child_symbols": unresolved_children,
            "strict_grammar_validation_claimed": False,
        },
        "fingerprints": fingerprints,
        "test_execution": run_metadata,
        "summary": {
            "elements": element_summary,
            "owner_attribute_pairs": attribute_summary,
            "character_data": character_summary,
            "sdk_extension_pairs": sdk_extension_summary,
        },
        "elements": element_rows,
        "owner_attribute_pairs": attribute_rows,
        "character_data": character_data_rows,
        "sdk_extension_pairs": sdk_extension_rows,
        "gaps": stage_gaps,
    }


def report_json(report: dict[str, object]) -> str:
    """Serialize reports with stable key ordering and no source-machine paths."""
    return json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def report_text(report: dict[str, object]) -> str:
    """Render a compact human-readable summary plus exact gaps by stage."""
    summary = cast(dict[str, dict[str, int]], report["summary"])
    execution = cast(dict[str, object], report["test_execution"])
    element_total = summary["elements"]["total"]
    pair_total = summary["owner_attribute_pairs"]["total"]
    sdk_total = summary["sdk_extension_pairs"]["total"]
    lines = [
        "CDXML DTD coverage",
        f"DTD: {cast(dict[str, object], report['baseline'])['dtd_sha256']}",
        (
            f"Elements: {summary['elements']['known']}/{element_total} DTD-known, "
            f"{summary['elements']['implemented']}/{element_total} implemented, "
            f"{summary['elements']['typed']}/{element_total} typed, "
            f"{summary['elements']['test_case_declared']}/{element_total} test cases declared, "
            f"{summary['elements']['tested']}/{element_total} tested, "
            f"{summary['elements']['round_trip_verified']}/{element_total} round-trip verified, "
            f"{summary['elements']['chemdraw_verified']}/{element_total} ChemDraw verified"
        ),
        (
            f"Owner-attribute pairs: {summary['owner_attribute_pairs']['known']}/{pair_total} "
            f"DTD-known, "
            f"{summary['owner_attribute_pairs']['implemented']}/{pair_total} implemented, "
            f"{summary['owner_attribute_pairs']['typed']}/{pair_total} typed, "
            f"{summary['owner_attribute_pairs']['test_case_declared']}/{pair_total} "
            "test cases declared, "
            f"{summary['owner_attribute_pairs']['tested']}/{pair_total} tested, "
            f"{summary['owner_attribute_pairs']['round_trip_verified']}/"
            f"{pair_total} round-trip verified, "
            f"{summary['owner_attribute_pairs']['chemdraw_verified']}/{pair_total} "
            "ChemDraw verified"
        ),
        (
            f"Character data: {summary['character_data']['implemented']}/"
            f"{summary['character_data']['total']} implemented, "
            f"{summary['character_data']['typed']}/{summary['character_data']['total']} typed, "
            f"{summary['character_data']['test_case_declared']}/"
            f"{summary['character_data']['total']} test cases declared, "
            f"{summary['character_data']['tested']}/{summary['character_data']['total']} tested, "
            f"{summary['character_data']['round_trip_verified']}/"
            f"{summary['character_data']['total']} round-trip verified"
        ),
        (
            "SDK extension pairs: "
            f"{summary['sdk_extension_pairs']['typed']}/{sdk_total} typed, "
            f"{summary['sdk_extension_pairs']['test_case_declared']}/{sdk_total} "
            "typed test cases declared, "
            f"{summary['sdk_extension_pairs']['tested']}/{sdk_total} typed tested, "
            f"{summary['sdk_extension_pairs']['round_trip_verified']}/{sdk_total} "
            "typed round-trip verified, "
            f"{summary['sdk_extension_pairs']['raw_preservation_tested']}/{sdk_total} "
            "raw-preservation tested"
        ),
        f"Feature test run: {execution['status']}",
    ]
    gaps = cast(dict[str, dict[str, list[object]]], report["gaps"])
    for stage, entries in gaps.items():
        lines.append(
            f"Gaps at {stage}: {len(entries['elements'])} elements, "
            f"{len(entries['owner_attribute_pairs'])} owner-attribute pairs, "
            f"{len(entries['character_data'])} character-data features, "
            f"{len(entries['sdk_extension_pairs'])} SDK extension pairs"
        )
    return "\n".join(lines) + "\n"
