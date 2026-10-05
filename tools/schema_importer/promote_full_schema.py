"""Promote pinned DTD/SDK evidence into the canonical static schema.

This is an offline source-maintenance command. Runtime document loading consumes
only generated Python metadata. The compiler reads the checked-in evidence
catalogs at build time only to resolve stable provenance source IDs to URIs; all
semantic model and codec decisions are already expressed in canonical YAML.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import cast

import yaml

from tools.schema_compiler.loader import load_schema
from tools.schema_compiler.validate import validate_schema
from tools.schema_importer.errors import ImporterError

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_PATH = ROOT / "schema" / "sources" / "sdk" / "evidence.json"
OVERRIDES_PATH = ROOT / "schema" / "overrides" / "full_schema.yaml"
CANONICAL = ROOT / "schema" / "canonical"
DTDSHA256 = "5311978e514ffe154108540c3634c314dc66031a4f3c877a681fc6dca8e128c2"


def _load_mapping(path: Path) -> dict[str, object]:
    raw: object = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ImporterError("FULL_SCHEMA_INPUT", f"expected mapping in {path}", str(path))
    return cast(dict[str, object], raw)


def _tag_key(owner: str, name: str) -> str:
    return f"{owner}@{name}"


def _snake(value: str) -> str:
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value)
    text = re.sub(r"([A-Z])([A-Z][a-z])", r"\1_\2", text)
    text = re.sub(r"[^A-Za-z0-9_]+", "_", text).strip("_").lower()
    return text or "field"


def _enum_name(values: tuple[str, ...], semantic_name: str) -> str:
    digest = hashlib.sha1("\0".join(values).encode("utf-8")).hexdigest()[:8]
    return f"dtd.{_snake(semantic_name)}.{digest}"


def _pascal(value: str) -> str:
    return "".join(part[:1].upper() + part[1:] for part in _snake(value).split("_"))


def _enum_member(value: str, used: set[str]) -> str:
    name = _snake(value).strip("_").upper()
    if not name or name[0].isdigit():
        name = f"VALUE_{name}"
    if name in {"CLASS", "FROM", "GLOBAL", "NONLOCAL", "TRUE", "FALSE", "NONE"}:
        name = f"VALUE_{name}"
    candidate = name
    suffix = 2
    while candidate in used:
        candidate = f"{name}_{suffix}"
        suffix += 1
    used.add(candidate)
    return candidate


def _raw_rows(value: object, label: str) -> list[dict[str, object]]:
    if not isinstance(value, list):
        raise ImporterError("FULL_SCHEMA_INPUT", f"{label} must be a list", label)
    rows: list[dict[str, object]] = []
    for index, raw in enumerate(cast(list[object], value)):
        if not isinstance(raw, dict):
            raise ImporterError("FULL_SCHEMA_INPUT", f"{label}[{index}] must be a mapping", label)
        rows.append(cast(dict[str, object], raw))
    return rows


def _convert_default(value: object, datatype: str, enum_values: tuple[str, ...]) -> object:
    if value is None:
        return None
    if enum_values == ("yes", "no"):
        return value == "yes"
    if datatype in {"integer", "object_id", "local_id"}:
        try:
            return int(cast(str, value))
        except (TypeError, ValueError):
            return value
    if datatype == "float":
        try:
            return float(cast(str, value))
        except (TypeError, ValueError):
            return value
    return value


def _source_ref(source: dict[str, object]) -> dict[str, str] | None:
    source_id = source.get("source_id")
    locator = source.get("locator")
    if isinstance(source_id, str) and isinstance(locator, str) and source_id and locator:
        return {"source": source_id, "locator": locator}
    return None


def _provenance_entries(value: object) -> list[dict[str, str]]:
    if not isinstance(value, list):
        return []
    entries: list[dict[str, str]] = []
    for raw in cast(list[object], value):
        if not isinstance(raw, dict):
            continue
        row = cast(dict[str, object], raw)
        source = row.get("source")
        locator = row.get("locator")
        if isinstance(source, str) and isinstance(locator, str):
            entries.append({"source": source, "locator": locator})
    return entries


def _merge_provenance(*groups: object) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for group in groups:
        for entry in _provenance_entries(group):
            if entry not in entries:
                entries.append(entry)
    return entries


def _merge_property_provenance(prop: dict[str, object], additions: object) -> None:
    prop["provenance"] = _merge_provenance(prop.get("provenance", []), additions)


def _duplicate_property_exceptions(
    properties: list[dict[str, object]], overrides: dict[str, object]
) -> list[dict[str, object]]:
    """Return only explicitly reviewed aliases; never excuse arbitrary ID reuse."""
    raw = overrides.get("cdx_property_aliases", [])
    aliases = _raw_rows(raw, "cdx_property_aliases") if raw else []
    result: list[dict[str, object]] = []
    by_id = {cast(str, prop["id"]): prop for prop in properties}
    for alias in aliases:
        property_ids = alias.get("property_ids")
        cdx_id = alias.get("cdx_id")
        rationale = alias.get("rationale")
        provenance = alias.get("provenance")
        if (
            not isinstance(property_ids, list)
            or len(cast(list[object], property_ids)) < 2
            or type(cdx_id) is not int
            or not isinstance(rationale, str)
            or not rationale.strip()
            or not isinstance(provenance, list)
            or not provenance
        ):
            raise ImporterError(
                "FULL_SCHEMA_ALIAS_OVERRIDE",
                "each CDX property alias needs property_ids, cdx_id, rationale, and provenance",
                str(OVERRIDES_PATH),
            )
        property_id_rows = cast(list[object], property_ids)
        if any(not isinstance(item, str) for item in property_id_rows):
            raise ImporterError(
                "FULL_SCHEMA_ALIAS_OVERRIDE",
                f"alias {alias.get('id')!r} property_ids must be strings",
                str(OVERRIDES_PATH),
            )
        ids = cast(list[str], property_id_rows)
        if any(item not in by_id or by_id[item].get("cdx_id") != cdx_id for item in ids):
            raise ImporterError(
                "FULL_SCHEMA_ALIAS_OVERRIDE",
                f"alias {alias.get('id')!r} does not match canonical property IDs",
                str(OVERRIDES_PATH),
            )
        for prop_id in ids:
            result.append(
                {
                    "id": f"alias_{_snake(cast(str, alias.get('id', prop_id)))}_{_snake(prop_id)}",
                    "rule": "duplicate_property_cdx_id",
                    "target": f"property:{prop_id}",
                    "rationale": rationale,
                    "provenance": provenance,
                }
            )
    return result


def _render_yaml(value: dict[str, object]) -> str:
    return yaml.safe_dump(value, sort_keys=False, allow_unicode=True, width=100)


def _validate_candidate(
    outputs: dict[str, dict[str, object]],
    expected_elements: int,
    expected_pairs: set[tuple[str, str]],
) -> None:
    with TemporaryDirectory(prefix="cdxml-full-schema-") as temporary:
        candidate_root = Path(temporary)
        candidate_canonical = candidate_root / "schema" / "canonical"
        candidate_canonical.mkdir(parents=True)
        shutil.copyfile(CANONICAL / "datatypes.yaml", candidate_canonical / "datatypes.yaml")
        for filename, content in outputs.items():
            (candidate_canonical / filename).write_text(_render_yaml(content), encoding="utf-8")
        candidate = load_schema(candidate_root)
        issues = validate_schema(candidate)
        if issues:
            details = "\n".join(str(issue) for issue in issues[:30])
            raise ImporterError(
                "FULL_SCHEMA_VALIDATION",
                f"candidate canonical schema has {len(issues)} validation issue(s):\n{details}",
                str(OVERRIDES_PATH),
            )
        if len(candidate.objects) != expected_elements:
            raise ImporterError(
                "FULL_SCHEMA_ELEMENT_COUNT",
                f"candidate has {len(candidate.objects)} models, expected {expected_elements}",
                str(OVERRIDES_PATH),
            )
        property_map = {item.id: item for item in candidate.properties}
        actual_pairs = {
            (obj.xml_tag, property_map[property_id].xml_name)
            for obj in candidate.objects
            for property_id in obj.properties
            if property_map[property_id].storage == "attribute"
        }
        missing_pairs = expected_pairs - actual_pairs
        if missing_pairs:
            raise ImporterError(
                "FULL_SCHEMA_PAIR_COUNT",
                f"candidate omits pinned DTD pairs: {sorted(missing_pairs)[:12]!r}",
                str(OVERRIDES_PATH),
            )


def _write_outputs(outputs: dict[str, dict[str, object]], *, dry_run: bool) -> None:
    rendered = {name: _render_yaml(value) for name, value in outputs.items()}
    # Validate the complete staged result before replacing any checked-in file.
    if dry_run:
        return
    with TemporaryDirectory(prefix="full-schema-candidate-", dir=CANONICAL) as temporary_dir:
        candidate_dir = Path(temporary_dir)
        staged: dict[str, Path] = {}
        for filename, content in rendered.items():
            temporary = candidate_dir / filename
            temporary.write_text(content, encoding="utf-8")
            staged[filename] = temporary
        for filename, temporary in staged.items():
            temporary.replace(CANONICAL / filename)


SdkFact = tuple[str, int, str, str | None, str | None]


def _sdk_fact(
    pair: dict[str, object],
    global_facts: dict[str, SdkFact] | None = None,
) -> tuple[str | None, int | None, str | None, str | None, str | None]:
    matches = pair.get("sdk_matches")
    if isinstance(matches, list) and matches:
        first = cast(dict[str, object], matches[0])
    else:
        variants = pair.get("sdk_case_variant_matches")
        first = (
            cast(dict[str, object], variants[0]) if isinstance(variants, list) and variants else {}
        )
    if not first and global_facts is not None:
        inherited = global_facts.get(cast(str, pair.get("xml_name", "")))
        if inherited is not None:
            return inherited
    sdk_type = first.get("sdk_type")
    cdx_id = first.get("cdx_id")
    constant = first.get("cdx_constant")
    source_raw = first.get("source")
    source = (
        _source_ref(cast(dict[str, object], source_raw)) if isinstance(source_raw, dict) else None
    )
    return (
        sdk_type if isinstance(sdk_type, str) else None,
        cdx_id if type(cdx_id) is int else None,
        constant if isinstance(constant, str) else None,
        source["source"] if source is not None else None,
        source["locator"] if source is not None else None,
    )


def _sdk_extra_fact(row: dict[str, object]) -> tuple[str, int, str, str, str]:
    raw_facts = row.get("sdk_facts")
    if not isinstance(raw_facts, list) or len(cast(list[object], raw_facts)) != 1:
        raise ImporterError(
            "FULL_SCHEMA_SDK_EXTRA",
            f"expected exactly one SDK fact for {row.get('owner_xml_name')}@{row.get('xml_name')}",
            str(EVIDENCE_PATH),
        )
    fact = cast(dict[str, object], cast(list[object], raw_facts)[0])
    sdk_type = fact.get("sdk_type")
    cdx_id = fact.get("cdx_id")
    constant = fact.get("cdx_constant")
    source_raw = fact.get("source")
    source_ref = (
        _source_ref(cast(dict[str, object], source_raw)) if isinstance(source_raw, dict) else None
    )
    if (
        not isinstance(sdk_type, str)
        or type(cdx_id) is not int
        or not isinstance(constant, str)
        or source_ref is None
    ):
        raise ImporterError(
            "FULL_SCHEMA_SDK_EXTRA",
            f"SDK fact is incomplete for {row.get('owner_xml_name')}@{row.get('xml_name')}",
            str(EVIDENCE_PATH),
        )
    return sdk_type, cdx_id, constant, source_ref["source"], source_ref["locator"]


def _add_sdk_case_aliases(
    evidence_rows: list[dict[str, object]],
    overrides: dict[str, object],
    pair_to_property: dict[tuple[str, str], dict[str, object]],
    tag_to_id: dict[str, str],
    signature_index: dict[tuple[object, ...], dict[str, object]],
) -> None:
    alias_rows = _raw_rows(
        overrides.get("sdk_xml_attribute_aliases", []), "sdk_xml_attribute_aliases"
    )
    by_key = {
        _tag_key(cast(str, row.get("owner_xml_name")), cast(str, row.get("xml_name"))): row
        for row in evidence_rows
        if row.get("classification") == "case_variant_of_dtd_xml_attribute"
    }
    if len(alias_rows) != 3 or len(by_key) != 3:
        raise ImporterError(
            "FULL_SCHEMA_SDK_ALIAS",
            "the pinned SDK evidence and explicit alias policy must cover "
            "three curve spelling variants",
            str(EVIDENCE_PATH),
        )
    seen: set[str] = set()
    for alias in alias_rows:
        owner = alias.get("owner_xml_name")
        xml_name = alias.get("xml_name")
        canonical_name = alias.get("canonical_xml_name")
        cdx_id = alias.get("cdx_id")
        constant = alias.get("cdx_constant")
        if (
            not isinstance(owner, str)
            or not isinstance(xml_name, str)
            or not isinstance(canonical_name, str)
            or type(cdx_id) is not int
            or not isinstance(constant, str)
        ):
            raise ImporterError(
                "FULL_SCHEMA_SDK_ALIAS", "malformed explicit SDK alias mapping", str(OVERRIDES_PATH)
            )
        key = _tag_key(owner, xml_name)
        if key in seen or key not in by_key:
            raise ImporterError(
                "FULL_SCHEMA_SDK_ALIAS",
                f"unexpected or duplicate SDK alias {key!r}",
                str(OVERRIDES_PATH),
            )
        seen.add(key)
        evidence = by_key[key]
        sdk_type, evidence_id, evidence_constant, source_id, locator = _sdk_extra_fact(evidence)
        if evidence_id != cdx_id or evidence_constant != constant:
            raise ImporterError(
                "FULL_SCHEMA_SDK_ALIAS", f"SDK alias facts changed for {key!r}", str(EVIDENCE_PATH)
            )
        prop = pair_to_property.get((owner, canonical_name))
        if prop is None or prop.get("cdx_id") != cdx_id or prop.get("cdx_constant") != constant:
            raise ImporterError(
                "FULL_SCHEMA_SDK_ALIAS",
                f"canonical DTD property does not match the SDK alias for {key!r}",
                str(OVERRIDES_PATH),
            )
        if prop.get("enum") is None:
            raise ImporterError(
                "FULL_SCHEMA_SDK_ALIAS",
                f"case alias {key!r} must reuse the DTD enum",
                str(OVERRIDES_PATH),
            )
        raw_owners = prop.get("owners", [prop.get("owner")])
        owners = cast(list[object], raw_owners) if isinstance(raw_owners, list) else [raw_owners]
        if owners != [tag_to_id[owner]]:
            raise ImporterError(
                "FULL_SCHEMA_SDK_ALIAS",
                f"case alias {key!r} must be scoped to its exact XML owner",
                str(OVERRIDES_PATH),
            )
        aliases_raw = prop.get("xml_aliases", [])
        aliases = cast(list[str], aliases_raw) if isinstance(aliases_raw, list) else []
        if xml_name not in aliases:
            aliases.append(xml_name)
        prop["xml_aliases"] = aliases
        _merge_property_provenance(
            prop,
            [
                {
                    "source": source_id,
                    "locator": f"{locator}: {xml_name} / {constant} / 0x{cdx_id:04X} ({sdk_type})",
                }
            ],
        )
        for signature, candidate in list(signature_index.items()):
            if candidate is prop:
                del signature_index[signature]
        signature_index[_property_signature(prop)] = prop
        for signature, candidate in list(signature_index.items()):
            if candidate is prop:
                del signature_index[signature]
        signature_index[_property_signature(prop)] = prop


def _global_sdk_facts(
    pairs: list[dict[str, object]],
) -> dict[str, SdkFact]:
    """Reuse an exact SDK property spelling only when its mapping is unique."""
    candidates: dict[str, set[SdkFact]] = defaultdict(set)
    for pair in pairs:
        matches = pair.get("sdk_matches")
        if not isinstance(matches, list) or not matches:
            continue
        first = cast(dict[str, object], matches[0])
        sdk_type = first.get("sdk_type")
        cdx_id = first.get("cdx_id")
        constant = first.get("cdx_constant")
        source_raw = first.get("source")
        source = (
            _source_ref(cast(dict[str, object], source_raw))
            if isinstance(source_raw, dict)
            else None
        )
        if isinstance(sdk_type, str) and type(cdx_id) is int and isinstance(constant, str):
            candidates[cast(str, pair["xml_name"])].add(
                (
                    sdk_type,
                    cdx_id,
                    constant,
                    source["source"] if source else None,
                    source["locator"] if source else None,
                )
            )
    result: dict[str, SdkFact] = {}
    for xml_name, values in candidates.items():
        identities = {(sdk_type, cdx_id, constant) for sdk_type, cdx_id, constant, _, _ in values}
        if len(identities) != 1:
            continue
        # Multiple owners can cite the same property. Pick a stable citation,
        # independent of set iteration/hash seed.
        result[xml_name] = min(
            values,
            key=lambda item: (item[3] or "", item[4] or "", item[0], item[1], item[2]),
        )
    return result


def _lexical_type(
    owner: str,
    name: str,
    enum_values: tuple[str, ...],
    sdk_type: str | None,
    overrides: dict[str, object],
) -> tuple[str, str, str | None, str | None, str | None, bool]:
    key = _tag_key(owner, name)
    field_aliases = cast(dict[str, object], overrides.get("field_aliases", {}))
    global_aliases = cast(dict[str, object], overrides.get("global_field_aliases", {}))
    name_override = field_aliases.get(key, global_aliases.get(name))
    field_name = name_override if isinstance(name_override, str) else _snake(name)

    lexical_strings = cast(dict[str, object], overrides.get("lexical_string_fields", {}))
    if key in lexical_strings:
        return field_name, "string", "string", None, None, False

    property_families = cast(dict[str, object], overrides.get("property_type_families", {}))
    family = property_families.get(key, property_families.get(name))
    if isinstance(family, dict):
        family_spec = cast(dict[str, object], family)
        return (
            field_name,
            cast(str, family_spec.get("datatype", "string")),
            cast(str, family_spec.get("codec", "string")),
            None,
            None,
            False,
        )

    measurement_fields = cast(dict[str, object], overrides.get("measurement_fields", {}))
    measure = measurement_fields.get(key)
    if measure is None:
        measure = cast(dict[str, object], overrides.get("measurement_property_families", {})).get(
            name
        )
    if isinstance(measure, dict):
        spec = cast(dict[str, object], measure)
        return (
            field_name,
            cast(str, spec.get("datatype", "float")),
            cast(str, spec.get("codec", "float")),
            None,
            None,
            False,
        )

    if enum_values == ("yes", "no"):
        return field_name, "boolean", "bool", None, None, False

    if enum_values:
        return field_name, "string", "enum", None, "@enum", False

    if sdk_type in {"CDXBoolean", "CDXBooleanImplied"}:
        return field_name, "boolean", "bool", None, None, False
    if sdk_type == "CDXCoordinate" or sdk_type == "FLOAT64":
        return field_name, "float", "float", None, None, False
    if sdk_type == "CDXPoint2D":
        return field_name, "point_2d", "point_2d", None, None, False
    if sdk_type == "CDXPoint3D":
        return field_name, "point_3d", "point_3d", None, None, False
    if sdk_type == "CDXRectangle":
        return field_name, "bounding_box", "bounding_box", None, None, False
    if sdk_type == "CDXCurvePoints":
        return field_name, "curve_points_2d", "curve_points2d", None, None, False
    if sdk_type == "CDXCurvePoints3D":
        return field_name, "curve_points_3d", "curve_points3d", None, None, False
    if sdk_type == "INT16ListWithCounts":
        return field_name, "integer_list", "uint16_list", None, None, False
    if sdk_type == "CDXElementList":
        return field_name, "element_list", "element_list", None, None, False
    if sdk_type == "CDXGenericList":
        return field_name, "generic_list", "generic_list", None, None, False
    if sdk_type in {"CDXObjectID", "CDXObjectIDArray", "CDXObjectIDArrayWithCounts"}:
        many = sdk_type != "CDXObjectID"
        data_type = "object_id"
        reference_targets = cast(dict[str, object], overrides.get("reference_targets", {}))
        reviewed_target = reference_targets.get(key)
        reference_target = (
            reviewed_target
            if isinstance(reviewed_target, str)
            else "node"
            if key == "n@Attachments"
            else "*"
        )
        return field_name, data_type, data_type, reference_target, None, many
    contextual_values = set(cast(list[str], overrides.get("contextual_value_fields", [])))
    if sdk_type == "varies" and key in contextual_values:
        return field_name, "object_tag_value", "object_tag_value", None, None, False

    if sdk_type in {"INT8", "INT16", "INT32", "UINT8", "UINT16", "UINT32"}:
        return field_name, "integer", "integer", None, None, False
    return field_name, "string", "string", None, None, False


def _existing_property_map(
    properties: list[dict[str, object]],
    objects: list[dict[str, object]],
) -> dict[tuple[str, str], dict[str, object]]:
    object_tag_by_id = {
        cast(str, item["id"]): cast(str, item["xml_tag"])
        for item in objects
        if isinstance(item.get("id"), str) and isinstance(item.get("xml_tag"), str)
    }
    result: dict[tuple[str, str], dict[str, object]] = {}
    for prop in properties:
        if prop.get("storage", "attribute") != "attribute":
            continue
        owners = prop.get("owners", [prop.get("owner")])
        if not isinstance(owners, list):
            owners = [owners]
        xml_name = prop.get("xml_name")
        if not isinstance(xml_name, str):
            continue
        for owner in cast(list[object], owners):
            if isinstance(owner, str):
                result[(object_tag_by_id.get(owner, owner), xml_name)] = prop
    return result


def _property_signature(prop: dict[str, object]) -> tuple[object, ...]:
    datatype = cast(str, prop.get("datatype", "string"))
    reference = prop.get("reference")
    many = bool(prop.get("reference_many", False))
    if prop.get("enum") is not None:
        codec = "enum"
    elif reference is not None:
        codec = "object_id_list" if many else "integer"
    else:
        codec = cast(
            str,
            prop.get(
                "codec",
                {
                    "string": "string",
                    "integer": "integer",
                    "object_id": "integer",
                    "local_id": "integer",
                    "float": "float",
                    "boolean": "bool",
                    "point_2d": "point_2d",
                    "point_3d": "point_3d",
                    "bounding_box": "bounding_box",
                }.get(datatype, datatype),
            ),
        )
    aliases_raw = prop.get("xml_aliases", [])
    aliases = tuple(cast(list[str], aliases_raw)) if isinstance(aliases_raw, list) else ()
    return (
        prop.get("name"),
        prop.get("xml_name"),
        datatype,
        codec,
        prop.get("cdx_id"),
        prop.get("cdx_constant"),
        bool(prop.get("required", False)),
        prop.get("default"),
        reference,
        many,
        prop.get("enum"),
        aliases,
    )


def _merge_property(
    source: dict[str, object],
    target: dict[str, object],
    properties: list[dict[str, object]],
    existing_by_pair: dict[tuple[str, str], dict[str, object]],
    pair_to_property: dict[tuple[str, str], dict[str, object]],
    signature_index: dict[tuple[object, ...], dict[str, object]],
) -> None:
    source_owners = source.get("owners", [source.get("owner")])
    target_owners = target.get("owners", [target.get("owner")])
    owners = [
        owner
        for owner in [
            *(
                cast(list[object], source_owners)
                if isinstance(source_owners, list)
                else [source_owners]
            ),
            *(
                cast(list[object], target_owners)
                if isinstance(target_owners, list)
                else [target_owners]
            ),
        ]
        if isinstance(owner, str)
    ]
    target.pop("owner", None)
    source.pop("owner", None)
    target["owners"] = sorted(set(owners))
    target["provenance"] = _merge_provenance(
        target.get("provenance", []), source.get("provenance", [])
    )
    for pair_key, prop in list(existing_by_pair.items()):
        if prop is source:
            existing_by_pair[pair_key] = target
    for pair_key, prop in list(pair_to_property.items()):
        if prop is source:
            pair_to_property[pair_key] = target
    for signature, prop in list(signature_index.items()):
        if prop is source:
            signature_index[signature] = target
    if source in properties:
        properties.remove(source)
    # Preserve the old property identifier when a previously-generated row is
    # folded into an established canonical definition.
    signature_index[_property_signature(target)] = target


def _add_property_owner(prop: dict[str, object], owner: str) -> None:
    if "owners" in prop:
        raw_owners = prop["owners"]
        if not isinstance(raw_owners, list):
            raise ImporterError(
                "FULL_SCHEMA_PROPERTY_OWNER",
                "canonical owners must be a list of strings",
                str(CANONICAL / "properties.yaml"),
            )
        owner_values = cast(list[object], raw_owners)
        if any(not isinstance(value, str) for value in owner_values):
            raise ImporterError(
                "FULL_SCHEMA_PROPERTY_OWNER",
                "canonical owners must be a list of strings",
                str(CANONICAL / "properties.yaml"),
            )
        owner_names = cast(list[str], owner_values).copy()
    else:
        raw_owner = prop.get("owner")
        if raw_owner is not None and not isinstance(raw_owner, str):
            raise ImporterError(
                "FULL_SCHEMA_PROPERTY_OWNER",
                "legacy owner must be a string",
                str(CANONICAL / "properties.yaml"),
            )
        owner_names = [raw_owner] if isinstance(raw_owner, str) else []
    if "owner" in prop and not isinstance(prop["owner"], str):
        raise ImporterError(
            "FULL_SCHEMA_PROPERTY_OWNER",
            "legacy owner must be a string when present",
            str(CANONICAL / "properties.yaml"),
        )
    owner_names.append(owner)
    updated_owners = sorted(set(owner_names))
    prop.pop("owner", None)
    prop["owners"] = updated_owners


def _object_sdk_identifiers(tag: str, sdk: dict[str, object]) -> tuple[int | None, str | None]:
    if sdk.get("namespace") != "object":
        return None, None

    raw_cdx_id = sdk.get("cdx_id")
    raw_cdx_constant = sdk.get("cdx_constant")
    if raw_cdx_id is not None and type(raw_cdx_id) is not int:
        raise ImporterError(
            "FULL_SCHEMA_OBJECT_MAPPING",
            f"SDK object ID for {tag!r} must be an integer or null",
            str(EVIDENCE_PATH),
        )
    if raw_cdx_constant is not None and not isinstance(raw_cdx_constant, str):
        raise ImporterError(
            "FULL_SCHEMA_OBJECT_MAPPING",
            f"SDK object constant for {tag!r} must be text or null",
            str(EVIDENCE_PATH),
        )
    return raw_cdx_id, raw_cdx_constant


def _make_enums(
    evidence_pairs: list[dict[str, object]],
    existing_enums: list[dict[str, object]],
    overrides: dict[str, object],
    global_facts: dict[str, SdkFact],
) -> tuple[list[dict[str, object]], dict[tuple[str, str], str]]:
    by_id = {str(item["id"]): item for item in existing_enums}
    pair_enum_ids: dict[tuple[str, str], str] = {}
    enum_type_names = cast(dict[str, object], overrides.get("enum_type_names", {}))
    for pair in evidence_pairs:
        owner = cast(str, pair["owner_xml_name"])
        name = cast(str, pair["xml_name"])
        values_raw = pair.get("enum_values", [])
        values = tuple(cast(list[str], values_raw)) if isinstance(values_raw, list) else ()
        if not values or values == ("yes", "no"):
            continue
        semantic_name_raw = enum_type_names.get(name)
        semantic_name = semantic_name_raw if isinstance(semantic_name_raw, str) else _pascal(name)
        sdk_type, cdx_id, constant, source_id, source_locator = _sdk_fact(pair, global_facts)
        existing_id = None
        # Reuse an existing enum only when its XML lexical values are identical.
        # This preserves the established numeric BondOrder/BondDisplay APIs.
        for item in existing_enums:
            raw_values = item.get("values", [])
            if isinstance(raw_values, list):
                existing_values = tuple(
                    cast(str, cast(dict[str, object], value).get("xml_value"))
                    for value in cast(list[object], raw_values)
                )
                if existing_values == values:
                    existing_id = str(item["id"])
                    # Semantic public names in the reviewed override file are
                    # stronger than provisional token-derived names from this
                    # still-unreleased generated schema.
                    if isinstance(semantic_name_raw, str):
                        item["python_name"] = semantic_name
                    break
        if existing_id is not None:
            pair_enum_ids[(owner, name)] = existing_id
            continue
        enum_id = _enum_name(values, semantic_name)
        if enum_id in by_id:
            pair_enum_ids[(owner, name)] = enum_id
            continue
        used: set[str] = set()
        value_rows = [{"name": _enum_member(value, used), "xml_value": value} for value in values]
        provenance = [
            {"source": "revvity_dtd", "locator": f"<!ATTLIST {owner} {name}> enumeration"}
        ]
        if source_id:
            provenance.append(
                {
                    "source": source_id,
                    "locator": source_locator
                    or f"SDK property mapping {constant or sdk_type or cdx_id}",
                }
            )
        by_id[enum_id] = {
            "id": enum_id,
            "python_name": semantic_name,
            "underlying_datatype": "string",
            "representation": "str",
            "status": "known",
            "provenance": provenance,
            "values": value_rows,
        }
        pair_enum_ids[(owner, name)] = enum_id
    return list(by_id.values()), pair_enum_ids


def promote_full_schema(*, dry_run: bool = False) -> tuple[int, int]:
    evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    if not isinstance(evidence, dict):
        raise ImporterError(
            "FULL_SCHEMA_INPUT", "SDK evidence must be a JSON object", str(EVIDENCE_PATH)
        )
    evidence = cast(dict[str, object], evidence)
    baseline = evidence.get("baseline")
    if (
        not isinstance(baseline, dict)
        or cast(dict[str, object], baseline).get("dtd_sha256") != DTDSHA256
    ):
        raise ImporterError(
            "FULL_SCHEMA_DTD", "SDK evidence is not pinned to the approved DTD", str(EVIDENCE_PATH)
        )
    overrides = _load_mapping(OVERRIDES_PATH)
    if overrides.get("dtd_sha256") != DTDSHA256:
        raise ImporterError(
            "FULL_SCHEMA_DTD",
            "override file is not pinned to the approved DTD",
            str(OVERRIDES_PATH),
        )

    elements = _raw_rows(evidence.get("elements"), "elements")
    pairs = _raw_rows(evidence.get("owner_attribute_pairs"), "owner_attribute_pairs")
    sdk_only_rows = _raw_rows(evidence.get("sdk_only_properties"), "sdk_only_properties")
    sdk_extension_rows = [
        row
        for row in sdk_only_rows
        if row.get("classification") == "sdk_documented_xml_attribute_not_in_pinned_dtd"
    ]
    if len(sdk_extension_rows) != 20:
        raise ImporterError(
            "FULL_SCHEMA_SDK_EXTRA",
            f"expected 20 SDK-only XML attributes, found {len(sdk_extension_rows)}",
            str(EVIDENCE_PATH),
        )
    global_sdk_facts = _global_sdk_facts(pairs)
    dtd_bytes = (ROOT / "schema" / "sources" / "revvity-CDXML.dtd").read_bytes()
    actual_dtd_sha = hashlib.sha256(dtd_bytes).hexdigest()
    if actual_dtd_sha != DTDSHA256:
        raise ImporterError("FULL_SCHEMA_DTD", f"unexpected DTD digest {actual_dtd_sha}", str(ROOT))

    model_overrides = cast(dict[str, object], overrides.get("object_models", {}))
    if set(model_overrides) != {cast(str, item["xml_name"]) for item in elements}:
        raise ImporterError(
            "FULL_SCHEMA_MODELS",
            "model overrides must cover exactly all DTD tags",
            str(OVERRIDES_PATH),
        )

    old_objects_doc = _load_mapping(CANONICAL / "objects.yaml")
    old_properties_doc = _load_mapping(CANONICAL / "properties.yaml")
    old_enums_doc = _load_mapping(CANONICAL / "enums.yaml")
    old_objects = _raw_rows(old_objects_doc.get("objects"), "canonical objects")
    old_properties = _raw_rows(old_properties_doc.get("properties"), "canonical properties")
    old_enums = _raw_rows(old_enums_doc.get("enums"), "canonical enums")
    existing_by_pair = _existing_property_map(old_properties, old_objects)

    tag_to_id = {
        tag: cast(str, cast(dict[str, object], spec)["id"]) for tag, spec in model_overrides.items()
    }
    pairs_by_owner: dict[str, list[dict[str, object]]] = defaultdict(list)
    for pair in pairs:
        pairs_by_owner[cast(str, pair["owner_xml_name"])].append(pair)
    cdx_conflicts: dict[str, dict[str, object]] = {}
    for conflict in _raw_rows(
        overrides.get("sdk_property_conflicts", []), "sdk_property_conflicts"
    ):
        raw_pairs = conflict.get("pairs", [])
        if isinstance(raw_pairs, list):
            for pair_key in cast(list[object], raw_pairs):
                if isinstance(pair_key, str):
                    cdx_conflicts[pair_key] = conflict

    enums_by_id: dict[str, dict[str, object]] = {str(item["id"]): item for item in old_enums}
    enums, enum_by_pair = _make_enums(
        pairs, list(enums_by_id.values()), overrides, global_sdk_facts
    )

    # Map every DTD pair to a canonical property, preserving established names,
    # codecs, and reference APIs before creating the missing static fields.
    pair_to_property: dict[tuple[str, str], dict[str, object]] = {}
    signature_index: dict[tuple[object, ...], dict[str, object]] = {}
    properties = list(old_properties)

    document_id_tags = {
        tag
        for tag, spec_raw in model_overrides.items()
        if cast(dict[str, object], spec_raw).get("id_scope") == "document"
        and any(
            pair.get("owner_xml_name") == tag and pair.get("xml_name") == "id" for pair in pairs
        )
    }
    common_id = next((item for item in old_properties if item.get("id") == "common.id"), None)
    if common_id is None:
        raise ImporterError(
            "FULL_SCHEMA_ID_POLICY", "canonical common.id property is missing", str(CANONICAL)
        )
    common_owners_raw = common_id.get("owners", [common_id.get("owner")])
    common_owners = (
        [value for value in cast(list[object], common_owners_raw) if isinstance(value, str)]
        if isinstance(common_owners_raw, list)
        else []
    )
    common_owners.extend(tag_to_id[tag] for tag in document_id_tags if tag in tag_to_id)
    common_id.pop("owner", None)
    common_id["owners"] = sorted(set(common_owners))

    for pair in pairs:
        owner = cast(str, pair["owner_xml_name"])
        xml_name = cast(str, pair["xml_name"])
        if xml_name == "id" and owner in document_id_tags:
            _, _, _, source_id, source_locator = _sdk_fact(pair, global_sdk_facts)
            id_provenance = [{"source": "revvity_dtd", "locator": f"<!ATTLIST {owner} id>"}]
            if source_id and source_locator:
                id_provenance.append({"source": source_id, "locator": source_locator})
            _merge_property_provenance(common_id, id_provenance)
            pair_to_property[(owner, xml_name)] = common_id
            continue
        existing = existing_by_pair.get((owner, xml_name))
        if existing is not None:
            # Existing canonical property definitions are still subject to
            # reviewed XML-family and public-name overrides.  In particular,
            # a pre-full-schema lexical field must not freeze the weaker
            # inference made before the global CDXML Point3D evidence was
            # registered.
            for signature, indexed_property in list(signature_index.items()):
                if indexed_property is existing:
                    del signature_index[signature]
            enum_values_raw = pair.get("enum_values", [])
            enum_values = (
                tuple(cast(list[str], enum_values_raw)) if isinstance(enum_values_raw, list) else ()
            )
            enum_id = enum_by_pair.get((owner, xml_name))
            if enum_id is not None:
                existing["enum"] = enum_id
                enum = next((item for item in enums if item.get("id") == enum_id), None)
                if enum is not None:
                    existing["datatype"] = cast(str, enum.get("underlying_datatype", "string"))
            if pair.get("required") is True:
                existing["required"] = True
            else:
                existing.pop("required", None)
            dtd_default = pair.get("default_value")
            if dtd_default is not None:
                datatype = cast(str, existing.get("datatype", "string"))
                existing["default"] = _convert_default(dtd_default, datatype, enum_values)
            property_default = cast(dict[str, object], overrides.get("property_defaults", {})).get(
                xml_name
            )
            if isinstance(property_default, dict):
                property_default_mapping = cast(dict[str, object], property_default)
                existing["default"] = property_default_mapping.get("value")
                _merge_property_provenance(existing, property_default_mapping.get("provenance", []))

            sdk_type, cdx_id, cdx_constant, sdk_source_id, sdk_locator = _sdk_fact(
                pair, global_sdk_facts
            )
            owner_field_aliases = cast(dict[str, object], overrides.get("field_aliases", {}))
            global_field_aliases = cast(
                dict[str, object], overrides.get("global_field_aliases", {})
            )
            explicit_field_name = owner_field_aliases.get(_tag_key(owner, xml_name))
            if explicit_field_name is None:
                explicit_field_name = global_field_aliases.get(xml_name)
            if isinstance(explicit_field_name, str):
                existing["name"] = explicit_field_name
            cdx_conflict = cdx_conflicts.get(_tag_key(owner, xml_name))
            if cdx_conflict is not None:
                cdx_id = None
                cdx_constant = None
            if cdx_id is not None:
                old_cdx_id = existing.get("cdx_id")
                old_constant = existing.get("cdx_constant")
                if old_cdx_id not in {None, cdx_id} or old_constant not in {None, cdx_constant}:
                    raise ImporterError(
                        "FULL_SCHEMA_SDK_CONFLICT",
                        f"{owner}@{xml_name} conflicts with canonical SDK mapping",
                        str(CANONICAL / "properties.yaml"),
                    )
                existing["cdx_id"] = cdx_id
                existing["cdx_constant"] = cdx_constant
            inferred_target: str | None = None
            inferred_many = False
            if enum_id is None and sdk_type is not None:
                (
                    _,
                    inferred_type,
                    inferred_codec,
                    inferred_target,
                    _,
                    inferred_many,
                ) = _lexical_type(owner, xml_name, enum_values, sdk_type, overrides)
                existing_target = existing.get("reference")
                if (
                    inferred_target == "*"
                    and isinstance(existing_target, str)
                    and existing_target != "*"
                ):
                    inferred_target = existing_target
                if existing.get("datatype") in {None, "string"} and inferred_type != "string":
                    existing["datatype"] = inferred_type
                    if inferred_codec not in {"string", "integer", "float", "bool"}:
                        existing["codec"] = inferred_codec
                    else:
                        existing.pop("codec", None)
            family_table = cast(dict[str, object], overrides.get("property_type_families", {}))
            property_family = family_table.get(
                _tag_key(owner, xml_name), family_table.get(xml_name)
            )
            if isinstance(property_family, dict):
                family_spec = cast(dict[str, object], property_family)
                family_datatype = family_spec.get("datatype")
                family_codec = family_spec.get("codec")
                if isinstance(family_datatype, str) and isinstance(family_codec, str):
                    existing["datatype"] = family_datatype
                    if family_codec in {
                        "string",
                        "integer",
                        "float",
                        "bool",
                        "point_2d",
                        "point_3d",
                        "bounding_box",
                    }:
                        existing.pop("codec", None)
                    else:
                        existing["codec"] = family_codec
                family_provenance = family_spec.get("provenance", [])
                _merge_property_provenance(existing, family_provenance)
            if sdk_source_id and sdk_locator:
                _merge_property_provenance(
                    existing, [{"source": sdk_source_id, "locator": sdk_locator}]
                )
            if cdx_conflict is not None:
                _merge_property_provenance(existing, cdx_conflict.get("provenance", []))
            lexical_spec = cast(dict[str, object], overrides.get("lexical_string_fields", {})).get(
                _tag_key(owner, xml_name)
            )
            if isinstance(lexical_spec, dict):
                existing["datatype"] = "string"
                existing.pop("codec", None)
                lexical_mapping = cast(dict[str, object], lexical_spec)
                _merge_property_provenance(existing, lexical_mapping.get("provenance", []))
            # The SDK's property datatype describes the target ID, while
            # `reference_many` determines the XML lexical codec. Preserve this
            # distinction on existing canonical properties as well as on new
            # fields: the scalar datatype is still object_id, but arrays are
            # whitespace-separated ID lists.
            existing_target = inferred_target or existing.get("reference")
            if isinstance(existing_target, str):
                many = (
                    inferred_many
                    if inferred_target is not None
                    else bool(existing.get("reference_many", False))
                )
                existing["datatype"] = "object_id"
                existing["reference"] = existing_target
                existing["reference_many"] = many
                existing["cardinality"] = "many" if many else "one"
                if many:
                    existing["codec"] = "object_id_list"
                else:
                    existing.pop("codec", None)
            signature = _property_signature(existing)
            previous = signature_index.get(signature)
            if previous is not None and previous is not existing:
                _merge_property(
                    previous,
                    existing,
                    properties,
                    existing_by_pair,
                    pair_to_property,
                    signature_index,
                )
            signature_index[signature] = existing
            pair_to_property[(owner, xml_name)] = existing
            continue

        sdk_type, cdx_id, cdx_constant, sdk_source_id, sdk_locator = _sdk_fact(
            pair, global_sdk_facts
        )
        cdx_conflict = cdx_conflicts.get(_tag_key(owner, xml_name))
        if cdx_conflict is not None:
            cdx_id = None
            cdx_constant = None
        enum_values_raw = pair.get("enum_values", [])
        enum_values = (
            tuple(cast(list[str], enum_values_raw)) if isinstance(enum_values_raw, list) else ()
        )
        field_name, datatype, codec, reference_target, enum_name, many = _lexical_type(
            owner, xml_name, enum_values, sdk_type, overrides
        )
        if owner == "font" and xml_name == "id":
            datatype, codec = "local_id", "integer"
        if owner in {"colortable", "fonttable"} and xml_name == "id":
            datatype, codec, reference_target, enum_name, many = (
                "string",
                "string",
                None,
                None,
                False,
            )
        if enum_name is not None:
            enum_name = enum_by_pair[(owner, xml_name)]
            enum_spec = next(item for item in enums if item.get("id") == enum_name)
            datatype = cast(str, enum_spec.get("underlying_datatype", "string"))
            codec = "enum"
        if reference_target is not None:
            datatype = "object_id"
            codec = "object_id_list" if many else "integer"

        required = bool(pair.get("required"))
        default_value = pair.get("default_value")
        default = _convert_default(default_value, datatype, enum_values)
        property_default = cast(dict[str, object], overrides.get("property_defaults", {})).get(
            xml_name
        )
        if isinstance(property_default, dict):
            default = cast(dict[str, object], property_default).get("value")
        if owner == "b" and xml_name == "Order":
            existing_order = existing_by_pair.get((owner, xml_name))
            if existing_order is not None:
                pair_to_property[(owner, xml_name)] = existing_order
                continue
            datatype, codec, enum_name, default = "integer", "bond_order", "bond_order", "1"
        if owner == "n" and xml_name == "id":
            datatype, codec = "object_id", "integer"
        if xml_name == "TagType" and owner in {"objecttag", "marker", "plasmidmarker"}:
            # A DTD string enumeration is kept lexical; Value's contextual codec
            # uses the exact XML tag token to select the corresponding Python type.
            datatype, codec, enum_name = "string", "enum", enum_by_pair[(owner, xml_name)]

        provenance = [{"source": "revvity_dtd", "locator": f"<!ATTLIST {owner} {xml_name}>"}]
        if sdk_source_id and sdk_locator:
            provenance.append({"source": sdk_source_id, "locator": sdk_locator})
        sdk_matches = pair.get("sdk_matches")
        if not sdk_source_id and isinstance(sdk_matches, list) and sdk_matches:
            sdk = cast(dict[str, object], cast(list[object], sdk_matches)[0])
            source = sdk.get("source")
            if isinstance(source, dict):
                ref = _source_ref(cast(dict[str, object], source))
                if ref is not None:
                    provenance.append(ref)
        variants = pair.get("sdk_case_variant_matches")
        if (
            not sdk_source_id
            and isinstance(variants, list)
            and variants
            and not (isinstance(sdk_matches, list) and sdk_matches)
        ):
            sdk = cast(dict[str, object], cast(list[object], variants)[0])
            source = sdk.get("source")
            if isinstance(source, dict):
                ref = _source_ref(cast(dict[str, object], source))
                if ref is not None:
                    provenance.append(ref)
        if owner == "b" and xml_name == "Order":
            provenance.append(
                {
                    "source": "sdk_bond_order",
                    "locator": "If this property is absent, it is treated as a single bond",
                }
            )

        measurement_fields = cast(dict[str, object], overrides.get("measurement_fields", {}))
        measurement = measurement_fields.get(_tag_key(owner, xml_name))
        if measurement is None:
            measurement = cast(
                dict[str, object], overrides.get("measurement_property_families", {})
            ).get(xml_name)
        if isinstance(measurement, dict):
            measure_spec = cast(dict[str, object], measurement)
            raw_provenance = measure_spec.get("provenance", [])
            if isinstance(raw_provenance, list):
                provenance.extend(cast(list[dict[str, str]], raw_provenance))
        property_families = cast(dict[str, object], overrides.get("property_type_families", {}))
        property_family = property_families.get(
            _tag_key(owner, xml_name), property_families.get(xml_name)
        )
        if isinstance(property_family, dict):
            raw_provenance = cast(dict[str, object], property_family).get("provenance", [])
            if isinstance(raw_provenance, list):
                provenance.extend(cast(list[dict[str, str]], raw_provenance))
        lexical_spec = cast(dict[str, object], overrides.get("lexical_string_fields", {})).get(
            _tag_key(owner, xml_name)
        )
        if isinstance(lexical_spec, dict):
            raw_provenance = cast(dict[str, object], lexical_spec).get("provenance", [])
            if isinstance(raw_provenance, list):
                provenance.extend(cast(list[dict[str, str]], raw_provenance))
        if cdx_conflict is not None:
            raw_provenance = cdx_conflict.get("provenance", [])
            if isinstance(raw_provenance, list):
                provenance.extend(cast(list[dict[str, str]], raw_provenance))
        if isinstance(property_default, dict):
            raw_provenance = cast(dict[str, object], property_default).get("provenance", [])
            if isinstance(raw_provenance, list):
                provenance.extend(cast(list[dict[str, str]], raw_provenance))

        signature = (
            field_name,
            xml_name,
            datatype,
            codec,
            cdx_id,
            cdx_constant,
            required,
            default,
            reference_target,
            many,
            enum_name,
        )
        prop: dict[str, object] | None = signature_index.get(signature)
        if prop is None:
            prop_id = f"dtd.{owner}.{field_name}"
            if prop_id in {str(item["id"]) for item in properties}:
                prop_id = (
                    f"dtd.{owner}.{field_name}.{hashlib.sha1(xml_name.encode()).hexdigest()[:6]}"
                )
            prop = {
                "id": prop_id,
                "owner": tag_to_id[owner],
                "name": field_name,
                "xml_name": xml_name,
                "datatype": datatype,
                "status": "known",
                "provenance": provenance,
            }
            if cdx_id is not None:
                prop["cdx_id"] = cdx_id
                prop["cdx_constant"] = cdx_constant
            if required:
                prop["required"] = True
            if default is not None:
                prop["default"] = default
            if enum_name is not None:
                prop["enum"] = enum_name
            elif codec not in {
                "integer",
                "string",
                "float",
                "bool",
                "point_2d",
                "point_3d",
                "bounding_box",
                "object_id_list",
            }:
                prop["codec"] = codec
            if reference_target is not None:
                prop["reference"] = reference_target
                prop["reference_many"] = many
            if many and reference_target is not None:
                prop["cardinality"] = "many"
            signature_index[signature] = prop
            properties.append(prop)
        else:
            _add_property_owner(prop, tag_to_id[owner])
            _merge_property_provenance(prop, provenance)
        pair_to_property[(owner, xml_name)] = prop

    # Promote SDK-documented XML attributes outside the pinned DTD inventory.
    # They are modeled features, but remain outside the exact 53/762 DTD counts.
    for extension in sdk_extension_rows:
        raw_owner = extension.get("owner_xml_name")
        raw_xml_name = extension.get("xml_name")
        if (
            not isinstance(raw_owner, str)
            or raw_owner not in tag_to_id
            or not isinstance(raw_xml_name, str)
        ):
            raise ImporterError(
                "FULL_SCHEMA_SDK_EXTRA",
                "SDK-only XML property has an unknown owner",
                str(EVIDENCE_PATH),
            )
        owner = raw_owner
        xml_name = raw_xml_name
        if (owner, xml_name) in {
            (cast(str, pair["owner_xml_name"]), cast(str, pair["xml_name"])) for pair in pairs
        }:
            raise ImporterError(
                "FULL_SCHEMA_SDK_EXTRA",
                f"SDK-only field {owner}@{xml_name} is already declared in the DTD inventory",
                str(EVIDENCE_PATH),
            )
        sdk_type, cdx_id, cdx_constant, sdk_source_id, sdk_locator = _sdk_extra_fact(extension)
        field_name, datatype, codec, reference_target, enum_name, many = _lexical_type(
            owner, xml_name, (), sdk_type, overrides
        )
        if reference_target is not None or enum_name is not None or many:
            raise ImporterError(
                "FULL_SCHEMA_SDK_EXTRA",
                f"SDK-only field {owner}@{xml_name} needs an explicit richer mapping override",
                str(OVERRIDES_PATH),
            )
        provenance = [
            {
                "source": sdk_source_id,
                "locator": (
                    f"{sdk_locator}: {xml_name} / {cdx_constant} / 0x{cdx_id:04X} ({sdk_type})"
                ),
            },
            {
                "source": "revvity_dtd",
                "locator": f"Pinned DTD has no declared {owner}@{xml_name} attribute pair",
            },
        ]
        family = cast(dict[str, object], overrides.get("property_type_families", {})).get(
            _tag_key(owner, xml_name),
            cast(dict[str, object], overrides.get("property_type_families", {})).get(xml_name),
        )
        if family is not None:
            provenance.extend(
                cast(list[dict[str, str]], cast(dict[str, object], family).get("provenance", []))
            )
        measure = cast(dict[str, object], overrides.get("measurement_property_families", {})).get(
            xml_name
        )
        if measure is not None:
            provenance.extend(
                cast(list[dict[str, str]], cast(dict[str, object], measure).get("provenance", []))
            )
        prop_id = f"sdk.{owner}.{field_name}"
        candidate: dict[str, object] = {
            "id": prop_id,
            "owner": tag_to_id[owner],
            "name": field_name,
            "xml_name": xml_name,
            "datatype": datatype,
            "cdx_id": cdx_id,
            "cdx_constant": cdx_constant,
            "status": "known",
            "provenance": provenance,
        }
        if codec not in {
            "integer",
            "string",
            "float",
            "bool",
            "point_2d",
            "point_3d",
            "bounding_box",
        }:
            candidate["codec"] = codec
        prior = existing_by_pair.get((owner, xml_name))
        if prior is not None:
            old_id = prior.get("cdx_id")
            old_constant = prior.get("cdx_constant")
            if old_id not in {None, cdx_id} or old_constant not in {None, cdx_constant}:
                raise ImporterError(
                    "FULL_SCHEMA_SDK_CONFLICT",
                    f"SDK-only field {owner}@{xml_name} conflicts with its canonical mapping",
                    str(CANONICAL / "properties.yaml"),
                )
            prior["cdx_id"] = cdx_id
            prior["cdx_constant"] = cdx_constant
            prior["datatype"] = datatype
            if "codec" in candidate:
                prior["codec"] = candidate["codec"]
            else:
                prior.pop("codec", None)
            _merge_property_provenance(prior, provenance)
            pair_to_property[(owner, xml_name)] = prior
            signature_index[_property_signature(prior)] = prior
            continue
        signature = _property_signature(candidate)
        existing = signature_index.get(signature)
        if existing is None:
            if prop_id in {str(item["id"]) for item in properties}:
                raise ImporterError(
                    "FULL_SCHEMA_SDK_EXTRA",
                    f"SDK-only field identifier collision for {owner}@{xml_name}",
                    str(OVERRIDES_PATH),
                )
            properties.append(candidate)
            signature_index[signature] = candidate
        else:
            _add_property_owner(existing, tag_to_id[owner])
            _merge_property_provenance(existing, provenance)

    _add_sdk_case_aliases(sdk_only_rows, overrides, pair_to_property, tag_to_id, signature_index)

    # Rebuild each object's property links and DTD child metadata. Reuse model
    # specs only for semantic identifiers; the pinned source drives tag, parent,
    # attributes, and declared child relationships.
    objects: list[dict[str, object]] = []
    for element in elements:
        tag = cast(str, element["xml_name"])
        override = cast(dict[str, object], model_overrides[tag])
        object_id = cast(str, override["id"])
        sdk_mapping = element.get("sdk_mapping")
        sdk = cast(dict[str, object], sdk_mapping) if isinstance(sdk_mapping, dict) else {}
        element_cdx_id, element_cdx_constant = _object_sdk_identifiers(tag, sdk)
        props: list[str] = []
        for pair in pairs_by_owner[tag]:
            prop = pair_to_property[(tag, cast(str, pair["xml_name"]))]
            prop_id = cast(str, prop["id"])
            if prop_id not in props:
                props.append(prop_id)
        # Preserve canonical non-attribute text features, currently s PCDATA.
        for prop in old_properties:
            owners = prop.get("owners", [prop.get("owner")])
            if not isinstance(owners, list):
                owners = [owners]
            if object_id in owners and prop.get("storage") == "text":
                prop_id = cast(str, prop["id"])
                if prop_id not in props:
                    props.append(prop_id)

        children: list[dict[str, object]] = []
        raw_children = element.get("dtd_children", [])
        if isinstance(raw_children, list):
            anomaly_pairs = {
                (
                    cast(str, cast(dict[str, object], item).get("parent_xml_tag")),
                    cast(str, cast(dict[str, object], item).get("child_xml_tag")),
                )
                for item in cast(list[object], overrides.get("source_anomalies", []))
                if isinstance(item, dict)
            }
            for child_tag in cast(list[object], raw_children):
                if not isinstance(child_tag, str):
                    raise ImporterError(
                        "FULL_SCHEMA_CHILD", f"non-text child tag {child_tag!r}", tag
                    )
                if child_tag not in tag_to_id:
                    if (tag, child_tag) in anomaly_pairs:
                        continue
                    raise ImporterError(
                        "FULL_SCHEMA_UNDECLARED_CHILD",
                        f"DTD parent {tag!r} references undeclared child {child_tag!r} "
                        "without an explicit anomaly override",
                        str(OVERRIDES_PATH),
                    )
                collection_overrides = cast(dict[str, object], overrides.get("collections", {}))
                collection = cast(str, collection_overrides.get(child_tag, ""))
                if not collection:
                    collection = {
                        "page": "pages",
                        "group": "groups",
                        "fragment": "fragments",
                        "t": "texts",
                        "s": "runs",
                        "n": "nodes",
                        "b": "bonds",
                        "font": "fonts",
                        "color": "colors",
                        "scheme": "schemes",
                        "step": "steps",
                    }.get(child_tag, _snake(child_tag))
                    if not collection.endswith("s"):
                        collection += "s"
                min_occurs, max_occurs = 0, None
                if tag == "CDXML":
                    if child_tag == "page":
                        min_occurs, max_occurs = 1, None
                    elif child_tag in {"colortable", "fonttable", "templategrid"}:
                        max_occurs = 1
                elif (tag, child_tag) in {
                    ("colortable", "color"),
                    ("fonttable", "font"),
                    ("scheme", "step"),
                    ("bracketedgroup", "bracketattachment"),
                }:
                    min_occurs = 1
                children.append(
                    {
                        "object_type": tag_to_id[child_tag],
                        "collection_name": collection,
                        "min_occurs": min_occurs,
                        "max_occurs": max_occurs,
                    }
                )

        parents_raw = element.get("dtd_parent_xml_names", [])
        allowed_parents: list[str] = []
        if isinstance(parents_raw, list):
            for parent_tag in cast(list[object], parents_raw):
                if isinstance(parent_tag, str) and parent_tag in tag_to_id:
                    allowed_parents.append(tag_to_id[parent_tag])
        category = cast(str, override["category"])
        id_scope = cast(str, override["id_scope"])
        if id_scope == "document" and not any(
            pair["xml_name"] == "id" for pair in pairs_by_owner[tag]
        ):
            id_scope = "none"
        if id_scope == "none" and tag in {"fonttable", "colortable"}:
            allowed_parents = [tag_to_id["CDXML"]]
        spec: dict[str, object] = {
            "id": object_id,
            "python_name": cast(str, override["python_name"]),
            "xml_tag": tag,
            "cdx_id": element_cdx_id,
            "cdx_constant": element_cdx_constant,
            "category": category,
            "id_scope": id_scope,
            "allowed_parents": allowed_parents,
            "children": children,
            "properties": props,
            "status": "known",
            "provenance": [
                {
                    "source": "revvity_dtd",
                    "locator": f"<!ELEMENT {tag}> and declared attributes/children",
                }
            ],
        }
        spec_provenance = cast(list[dict[str, str]], spec["provenance"])
        if tag == "font":
            spec_provenance.append(
                {"source": "sdk_font", "locator": "Font properties and table-local identifier"}
            )
        if tag == "color":
            spec_provenance.append(
                {
                    "source": "sdk_color",
                    "locator": "Color RGB components are fractional values from 0 through 1",
                }
            )
        if tag == "CDXML":
            spec_provenance.append(
                {"source": "sdk_objects", "locator": "Document object (kCDXObj_Document)"}
            )
        objects.append(spec)

    # Add every property ID to exactly one owner link, including any existing
    # multi-owner property definitions preserved above.
    for obj in objects:
        linked = set(cast(list[str], obj["properties"]))
        for prop in properties:
            owners = prop.get("owners", [prop.get("owner")])
            if not isinstance(owners, list):
                owners = [owners]
            if obj["id"] in owners and prop.get("id") not in linked:
                cast(list[str], obj["properties"]).append(cast(str, prop["id"]))

    outputs: dict[str, dict[str, object]] = {
        "objects.yaml": {
            "version": 1,
            "objects": objects,
            "exceptions": _duplicate_property_exceptions(properties, overrides),
        },
        "properties.yaml": {"version": 1, "properties": properties},
        "enums.yaml": {"version": 1, "enums": enums},
    }
    expected_dtd_pairs = {
        (cast(str, pair["owner_xml_name"]), cast(str, pair["xml_name"])) for pair in pairs
    }
    if len(expected_dtd_pairs) != 762:
        raise ImporterError(
            "FULL_SCHEMA_PAIR_COUNT",
            f"pinned DTD evidence has {len(expected_dtd_pairs)} unique pairs, expected 762",
            str(EVIDENCE_PATH),
        )
    _validate_candidate(outputs, len(elements), expected_dtd_pairs)
    _write_outputs(outputs, dry_run=dry_run)
    return len(elements), len(pairs)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate and report the candidate without changing canonical YAML",
    )
    args = parser.parse_args()
    count_elements, count_pairs = promote_full_schema(dry_run=args.dry_run)
    action = "Validated" if args.dry_run else "Promoted"
    print(f"{action} {count_elements} DTD elements and {count_pairs} owner-attribute pairs.")
