import shutil
from dataclasses import replace
from pathlib import Path

import pytest
from tools.schema_compiler.errors import SchemaError, SchemaIssue
from tools.schema_compiler.ir import ReferenceSpec, SchemaException
from tools.schema_compiler.loader import load_schema
from tools.schema_compiler.validate import validate_schema

ROOT = Path(__file__).resolve().parents[2]


def codes(issues: tuple[SchemaIssue, ...]) -> set[str]:
    return {issue.code for issue in issues}


def test_canonical_schema_is_valid() -> None:
    assert validate_schema(load_schema(ROOT)) == ()


def test_duplicate_object_numeric_ids_are_rejected() -> None:
    schema = load_schema(ROOT)
    duplicate = replace(schema.objects[1], cdx_id=schema.objects[0].cdx_id)
    invalid = replace(schema, objects=(schema.objects[0], duplicate, *schema.objects[2:]))

    assert "DUPLICATE_OBJECT_CDX_ID" in codes(validate_schema(invalid))


def test_duplicate_and_out_of_namespace_property_numeric_ids_are_rejected() -> None:
    schema = load_schema(ROOT)
    property_indexes = {prop.id: index for index, prop in enumerate(schema.properties)}
    begin_index = property_indexes["bond.begin"]
    end_index = property_indexes["bond.end"]
    properties = list(schema.properties)
    properties[end_index] = replace(properties[end_index], cdx_id=properties[begin_index].cdx_id)
    duplicate_schema = replace(schema, properties=tuple(properties))
    properties[end_index] = replace(schema.properties[end_index], cdx_id=0x8000)
    namespace_schema = replace(schema, properties=tuple(properties))

    assert "DUPLICATE_PROPERTY_CDX_ID" in codes(validate_schema(duplicate_schema))
    assert "INVALID_PROPERTY_NAMESPACE" in codes(validate_schema(namespace_schema))


def test_unresolved_datatype_enum_reference_and_child_are_rejected() -> None:
    schema = load_schema(ROOT)
    bad_property = replace(schema.properties[0], datatype="missing_type", enum="missing_enum")
    bad_bond_ref = replace(
        schema.properties[-3], reference=ReferenceSpec(target_type="missing_object")
    )
    bond = replace(
        schema.objects[-1],
        children=(replace(schema.objects[1].children[0], object_type="missing_child"),),
    )
    invalid = replace(
        schema,
        properties=(bad_property, *schema.properties[1:-3], bad_bond_ref, *schema.properties[-2:]),
        objects=(*schema.objects[:-1], bond),
    )

    result = codes(validate_schema(invalid))
    assert {
        "UNRESOLVED_DATATYPE",
        "UNRESOLVED_ENUM",
        "UNRESOLVED_REFERENCE_TARGET",
        "UNRESOLVED_CHILD",
    } <= result


def test_xml_property_name_collision_is_rejected() -> None:
    schema = load_schema(ROOT)
    collision = replace(schema.properties[1], xml_name=schema.properties[0].xml_name)
    invalid = replace(schema, properties=(schema.properties[0], collision, *schema.properties[2:]))

    assert "PROPERTY_XML_NAME_COLLISION" in codes(validate_schema(invalid))


def test_invalid_schema_status_is_rejected() -> None:
    schema = load_schema(ROOT)
    invalid = replace(
        schema, objects=(replace(schema.objects[0], status="mystery"), *schema.objects[1:])
    )

    assert "INVALID_STATUS" in codes(validate_schema(invalid))


def test_object_id_scope_is_explicit_and_validated() -> None:
    schema = load_schema(ROOT)
    invalid = replace(
        schema,
        objects=(replace(schema.objects[0], id_scope="global-ish"), *schema.objects[1:]),
    )

    assert "INVALID_ID_SCOPE" in codes(validate_schema(invalid))


def test_id_datatype_must_match_its_registry_scope() -> None:
    schema = load_schema(ROOT)
    common_id_index = next(
        index for index, prop in enumerate(schema.properties) if prop.id == "common.id"
    )
    common_id = replace(schema.properties[common_id_index], datatype="local_id")
    properties = list(schema.properties)
    properties[common_id_index] = common_id

    assert "DOCUMENT_ID_DATATYPE" in codes(
        validate_schema(replace(schema, properties=tuple(properties)))
    )


def test_many_valued_object_references_require_list_codec() -> None:
    schema = load_schema(ROOT)
    many_index = next(
        index
        for index, prop in enumerate(schema.properties)
        if prop.reference is not None and prop.reference.many
    )
    properties = list(schema.properties)
    properties[many_index] = replace(properties[many_index], codec="object_id")

    issues = validate_schema(replace(schema, properties=tuple(properties)))

    assert "REFERENCE_LIST_CODEC" in codes(issues)


def test_unresolved_object_property_is_rejected_before_generation() -> None:
    schema = load_schema(ROOT)
    invalid = replace(
        schema, objects=(replace(schema.objects[0], properties=("missing",)), *schema.objects[1:])
    )

    assert "UNRESOLVED_PROPERTY" in codes(validate_schema(invalid))


@pytest.mark.parametrize(
    "reserved_name",
    [
        "Field",
        "Final",
        "Mapping",
        "MappingProxyType",
        "MODEL_REGISTRY",
        "OBJECT_BY_SPEC_ID",
        "SCHEMA_HASH",
        "Scalar",
        "PropertyMetadata",
    ],
)
def test_generated_model_import_and_global_names_are_reserved(reserved_name: str) -> None:
    schema = load_schema(ROOT)
    reserved_model = replace(schema.objects[0], python_name=reserved_name)
    model_schema = replace(schema, objects=(reserved_model, *schema.objects[1:]))

    assert "RESERVED_GENERATED_TYPE_NAME" in codes(validate_schema(model_schema))


@pytest.mark.parametrize(
    "reserved_name",
    [
        "Field",
        "IntEnum",
        "IntFlag",
        "StrEnum",
        "Final",
        "Mapping",
        "MappingProxyType",
        "MODEL_REGISTRY",
        "OBJECT_BY_XML_TAG",
        "SCHEMA_HASH",
        "Scalar",
        "EnumMetadata",
    ],
)
def test_generated_enum_import_and_global_names_are_reserved(reserved_name: str) -> None:
    schema = load_schema(ROOT)
    reserved_enum = replace(schema.enums[0], python_name=reserved_name)
    enum_schema = replace(schema, enums=(reserved_enum, *schema.enums[1:]))

    assert "RESERVED_GENERATED_TYPE_NAME" in codes(validate_schema(enum_schema))


def test_generated_property_and_collection_import_names_are_reserved() -> None:
    schema = load_schema(ROOT)
    reserved_property = replace(schema.properties[1], name="raw_element")
    property_schema = replace(
        schema, properties=(schema.properties[0], reserved_property, *schema.properties[2:])
    )
    descriptor_property = replace(schema.properties[1], name="Field")
    descriptor_schema = replace(
        schema, properties=(schema.properties[0], descriptor_property, *schema.properties[2:])
    )

    assert "RESERVED_MODEL_NAME" in codes(validate_schema(property_schema))
    assert "RESERVED_MODEL_NAME" in codes(validate_schema(descriptor_schema))


def test_unresolved_parent_is_rejected() -> None:
    schema = load_schema(ROOT)
    invalid = replace(
        schema,
        objects=(
            replace(schema.objects[0], allowed_parents=("missing_parent",)),
            *schema.objects[1:],
        ),
    )

    assert "UNRESOLVED_PARENT" in codes(validate_schema(invalid))


@pytest.mark.parametrize(
    ("relative_path", "original", "replacement"),
    [
        ("schema/canonical/properties.yaml", "cdx_id: 1026", "cdx_id: '1026'"),
        ("schema/canonical/properties.yaml", "required: true", "required: 'true'"),
        ("schema/canonical/objects.yaml", "min_occurs: 0", "min_occurs: '0'"),
    ],
)
def test_loader_rejects_malformed_numeric_and_boolean_fields(
    tmp_path: Path, relative_path: str, original: str, replacement: str
) -> None:
    shutil.copytree(ROOT / "schema" / "canonical", tmp_path / "schema" / "canonical")
    path = tmp_path / relative_path
    contents = path.read_text(encoding="utf-8")
    assert original in contents
    path.write_text(contents.replace(original, replacement, 1), encoding="utf-8")

    with pytest.raises(SchemaError):
        load_schema(tmp_path)


def test_loader_rejects_duplicate_yaml_mapping_keys(tmp_path: Path) -> None:
    shutil.copytree(ROOT / "schema" / "canonical", tmp_path / "schema" / "canonical")
    path = tmp_path / "schema" / "canonical" / "properties.yaml"
    contents = path.read_text(encoding="utf-8")
    matching_line = next(
        (line for line in contents.splitlines() if line.strip() == "xml_name: Element"),
        None,
    )
    assert matching_line is not None
    indentation = matching_line[: len(matching_line) - len(matching_line.lstrip())]
    original = f"{indentation}xml_name: Element\n"
    duplicate = f"{original}{indentation}xml_name: Alias\n"
    path.write_text(
        contents.replace(original, duplicate, 1),
        encoding="utf-8",
    )

    with pytest.raises(SchemaError, match="duplicate key"):
        load_schema(tmp_path)


def test_collision_exceptions_must_be_scoped_to_each_definition() -> None:
    schema = load_schema(ROOT)
    objects_by_id = {item.id: item for item in schema.objects}
    page = objects_by_id["page"]
    fragment = objects_by_id["fragment"]
    invalid_objects = tuple(
        replace(item, xml_tag=page.xml_tag) if item.id == fragment.id else item
        for item in schema.objects
    )
    invalid = replace(schema, objects=invalid_objects)

    assert "OBJECT_XML_TAG_COLLISION" in codes(validate_schema(invalid))

    exceptions = (
        SchemaException(
            id="legacy-page-tag",
            rule="object_xml_tag_collision",
            target="object:page",
            rationale="Explicit fixture for scoped historical exception validation.",
            provenance=page.provenance,
        ),
        SchemaException(
            id="legacy-fragment-tag",
            rule="object_xml_tag_collision",
            target="object:fragment",
            rationale="Explicit fixture for scoped historical exception validation.",
            provenance=fragment.provenance,
        ),
    )
    preserved = tuple(item for item in schema.exceptions if item.rule != "object_xml_tag_collision")
    with_exceptions = replace(invalid, exceptions=(*preserved, *exceptions))
    assert "OBJECT_XML_TAG_COLLISION" not in codes(validate_schema(with_exceptions))
    assert "UNUSED_EXCEPTION" not in codes(validate_schema(with_exceptions))
