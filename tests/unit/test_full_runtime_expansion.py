"""Full-schema runtime behavior for the generated document root and irregular fields."""

from __future__ import annotations

from enum import Enum
from typing import Any, cast

import pytest

from cdxml_om._generated import enums as generated_enums
from cdxml_om._generated.models import CDXMLRoot
from cdxml_om._generated.schema_metadata import OBJECT_METADATA, ObjectMetadata
from cdxml_om.core.document import CDXMLDocument
from cdxml_om.core.errors import CodecError, MutationError
from cdxml_om.core.fields import ElementCollection
from cdxml_om.core.models import CDXMLElement


def _metadata_for_tag(xml_tag: str) -> tuple[str, ObjectMetadata]:
    return next(
        (spec_id, metadata)
        for spec_id, metadata in OBJECT_METADATA.items()
        if metadata.xml_tag == xml_tag
    )


def _collection(parent: CDXMLElement, child_xml_tag: str) -> ElementCollection[CDXMLElement]:
    parent_spec_id, parent_metadata = _metadata_for_tag(parent.xml_tag)
    child = next(
        child
        for child in parent_metadata.children
        if OBJECT_METADATA[child.object_type].xml_tag == child_xml_tag
    )
    assert parent_spec_id in OBJECT_METADATA
    return cast(ElementCollection[CDXMLElement], getattr(parent, child.collection_name))


def _property_id(owner_xml_tag: str, property_xml_name: str) -> str:
    _, metadata = _metadata_for_tag(owner_xml_tag)
    return next(
        property_id
        for property_id, prop in metadata.properties.items()
        if prop.xml_name == property_xml_name
    )


def _tag_type(value: str) -> Enum:
    enum_name = "TagType"
    enum_type = cast(type[Enum], getattr(generated_enums, enum_name))
    return enum_type(value)


def _generated(value: CDXMLElement) -> Any:
    """Enable access to generated-only fields while helpers retain base typing."""
    return cast(Any, value)


def test_generated_document_root_is_typed_stable_and_has_no_identity_id() -> None:
    document = CDXMLDocument.from_string("<CDXML><page id='1'/></CDXML>")
    root = document.root

    assert isinstance(root, CDXMLRoot)
    assert document.root is root
    assert document.wrap(root.raw_element) is root
    assert root.parent is None
    assert not hasattr(root, "id")
    assert not any(issue.code == "invalid-parent" for issue in document.validate().errors)
    assert document.validate().is_valid


def test_root_child_creation_uses_schema_routes_order_and_cardinality() -> None:
    document = CDXMLDocument.from_string("<CDXML/>")
    root = document.root
    page_one = _collection(root, "page").create()
    grid = _collection(root, "templategrid").create()
    color_table = _collection(root, "colortable").create()
    font_table = _collection(root, "fonttable").create()
    page_two = document.pages.create()

    _collection(color_table, "color").create(r=0.2, g=0.4, b=0.6)
    _collection(font_table, "font").create(name="Local Font")

    assert document.color_table is color_table
    assert document.font_table is font_table
    assert [child.tag for child in root.raw_element] == [
        "colortable",
        "fonttable",
        "page",
        "page",
        "templategrid",
    ]
    assert document.pages[0] is page_one
    assert document.pages[1] is page_two
    assert document.validate().is_valid

    _collection(root, "page").remove(page_two)
    assert document.pages.all() == [page_one]
    _collection(root, "page").remove(page_one)
    assert document.pages.all() == []
    assert any(
        issue.code == "child-cardinality" and issue.severity == "error"
        for issue in document.validate().issues
    )

    _collection(root, "templategrid").remove(grid)
    assert all(child.tag != "templategrid" for child in root.raw_element)


def test_minimum_cardinality_removals_remain_editable_and_validation_reports_them() -> None:
    document = CDXMLDocument.from_string(
        '<CDXML><colortable><color r="1" g="0" b="0"/></colortable>'
        '<fonttable><font id="3" name="Test Font"/></fonttable><page id="1"/></CDXML>'
    )
    root = document.root
    color_table = document.color_table
    font_table = document.font_table
    assert color_table is not None
    assert font_table is not None

    _collection(color_table, "color").remove(color_table.colors[0])
    _collection(font_table, "font").remove(font_table.fonts[0])
    _collection(root, "page").remove(document.pages[0])

    assert color_table.colors.all() == []
    assert font_table.fonts.all() == []
    assert document.pages.all() == []
    assert document.tree.getroot() is root.raw_element
    assert sum(issue.code == "child-cardinality" for issue in document.validate().errors) == 3


def test_document_root_compatibility_helpers_route_through_generated_children() -> None:
    document = CDXMLDocument.from_string("<CDXML><page id='1'/></CDXML>")

    color_table = document.create_color_table()
    font_table = document.create_font_table()

    assert document.color_table is color_table
    assert document.font_table is font_table
    assert [child.tag for child in document.root.raw_element] == [
        "colortable",
        "fonttable",
        "page",
    ]


@pytest.mark.parametrize(
    ("tag_type", "raw", "expected"),
    [
        ("Unknown", "0x10", "0x10"),
        ("String", "0012", "0012"),
        ("Long", "-2147483648", -(1 << 31)),
        ("Double", "1.25e2", 125.0),
        (None, "0xFE", "0xFE"),
    ],
)
def test_object_tag_value_decodes_by_tag_type_without_string_heuristics(
    tag_type: str | None,
    raw: str,
    expected: object,
) -> None:
    property_id = _property_id("objecttag", "Value")
    document = CDXMLDocument.from_string(
        '<CDXML><page id="1"><objecttag id="2" Name="evidence"'
        + (f' TagType="{tag_type}"' if tag_type is not None else "")
        + f' Value="{raw}"/></page></CDXML>'
    )
    object_tag = _generated(document.wrap(document.tree.xpath("//objecttag")[0]))

    assert document.read_field(object_tag.raw_element, property_id) == expected
    assert object_tag.raw_attributes["Value"] == raw


@pytest.mark.parametrize(
    ("tag_type", "expected"),
    [("Unknown", "0"), ("String", "0"), ("Long", 0), ("Double", 0.0), (None, "0")],
)
def test_missing_object_tag_value_uses_the_contextual_zero_default(
    tag_type: str | None,
    expected: object,
) -> None:
    property_id = _property_id("objecttag", "Value")
    document = CDXMLDocument.from_string(
        '<CDXML><page id="1"><objecttag id="2" Name="default"'
        + (f' TagType="{tag_type}"' if tag_type is not None else "")
        + "/></page></CDXML>"
    )
    object_tag = document.wrap(document.tree.xpath("//objecttag")[0])

    assert document.read_field(object_tag.raw_element, property_id) == expected
    assert "Value" not in object_tag.raw_attributes


def test_object_tag_creation_is_context_order_independent_and_failure_is_atomic() -> None:
    document = CDXMLDocument.from_string("<CDXML><page id='1'/></CDXML>")
    collection = _collection(document.pages[0], "objecttag")

    type_first = collection.create(name="type first", tag_type=_tag_type("Long"), value=12)
    value_first = collection.create(name="value first", value=13, tag_type=_tag_type("Long"))
    assert _generated(type_first).value == 12
    assert _generated(value_first).value == 13
    assert type_first.raw_attributes["Value"] == "12"
    assert value_first.raw_attributes["Value"] == "13"

    before = document.to_string()
    with pytest.raises(MutationError):
        collection.create(name="bad", value=1.5, tag_type=_tag_type("Long"))
    assert document.to_string() == before

    next_valid = collection.create(name="after failure", value=14, tag_type=_tag_type("Long"))
    assert next_valid.raw_attributes.get("id") == "4"


def test_object_tag_typed_mutation_and_invalid_tag_type_change_are_atomic() -> None:
    document = CDXMLDocument.from_string(
        '<CDXML><page id="1"><objecttag id="2" Name="mutable"'
        ' TagType="String" Value="not-a-number"/></page></CDXML>'
    )
    object_tag = _generated(document.wrap(document.tree.xpath("//objecttag")[0]))
    before = dict(object_tag.raw_attributes)

    with pytest.raises(MutationError):
        object_tag.tag_type = _tag_type("Long")
    assert dict(object_tag.raw_attributes) == before
    assert object_tag.value == "not-a-number"

    object_tag.value = "0x10"
    assert object_tag.value == "0x10"
    object_tag.tag_type = _tag_type("String")
    assert object_tag.value == "0x10"

    with pytest.raises(MutationError):
        object_tag.value = 1.5
    assert object_tag.value == "0x10"


@pytest.mark.parametrize("invalid", [True, 1 << 31, -(1 << 31) - 1])
def test_object_tag_long_mutation_rejects_wrong_type_and_out_of_range_values(
    invalid: object,
) -> None:
    document = CDXMLDocument.from_string(
        '<CDXML><page id="1"><objecttag id="2" Name="long"'
        ' TagType="Long" Value="3"/></page></CDXML>'
    )
    object_tag = _generated(document.wrap(document.tree.xpath("//objecttag")[0]))
    before = dict(object_tag.raw_attributes)

    with pytest.raises(MutationError):
        object_tag.value = invalid

    assert dict(object_tag.raw_attributes) == before
    assert object_tag.value == 3


@pytest.mark.parametrize("invalid", [float("nan"), float("inf"), 10**400])
def test_object_tag_double_mutation_rejects_nonfinite_or_unrepresentable_values_atomically(
    invalid: object,
) -> None:
    document = CDXMLDocument.from_string(
        '<CDXML><page id="1"><objecttag id="2" Name="double"'
        ' TagType="Double" Value="1.25"/></page></CDXML>'
    )
    object_tag = _generated(document.wrap(document.tree.xpath("//objecttag")[0]))
    before = dict(object_tag.raw_attributes)

    with pytest.raises(MutationError):
        object_tag.value = invalid

    assert dict(object_tag.raw_attributes) == before
    assert object_tag.value == 1.25


def test_failed_double_creation_does_not_change_dom_or_consume_object_id() -> None:
    document = CDXMLDocument.from_string("<CDXML><page id='1'/></CDXML>")
    collection = _collection(document.pages[0], "objecttag")
    before = document.to_string()

    with pytest.raises(MutationError):
        collection.create(name="unrepresentable", value=10**400, tag_type=_tag_type("Double"))

    assert document.to_string() == before
    created = collection.create(name="valid", value=2.5, tag_type=_tag_type("Double"))
    assert created.raw_attributes.get("id") == "2"


def test_validation_reports_object_tag_value_errors_using_sibling_tag_type() -> None:
    document = CDXMLDocument.from_string(
        '<CDXML><page id="1"><objecttag id="2" Name="invalid"'
        ' TagType="Long" Value="not-an-int"/></page></CDXML>'
    )
    value_property = _property_id("objecttag", "Value")

    report = document.validate()

    assert any(
        issue.code == "invalid-value" and issue.property_id == value_property
        for issue in report.errors
    )
    object_tag = _generated(document.wrap(document.tree.xpath("//objecttag")[0]))
    with pytest.raises(CodecError):
        _ = object_tag.value


def test_spectrum_reads_direct_pcdata_and_mutation_preserves_children() -> None:
    document = CDXMLDocument.from_string(
        '<CDXML><page id="1"><spectrum id="2">left'
        '<objecttag Name="meta" TagType="String" Value="nested"/>middle'
        '<vendor:unknown xmlns:vendor="urn:vendor" keep="yes">opaque</vendor:unknown>'
        "right</spectrum></page></CDXML>"
    )
    spectrum = document.wrap(document.tree.xpath("//spectrum")[0])
    spectrum_metadata = _metadata_for_tag("spectrum")[1]
    data_property = next(
        metadata for metadata in spectrum_metadata.properties.values() if metadata.storage == "text"
    )
    children = tuple(spectrum.raw_element)
    child_snapshots = tuple(
        (child.tag, dict(child.attrib), child.text, tuple(grandchild.tag for grandchild in child))
        for child in children
    )
    wrapper = document.wrap(children[0])

    assert getattr(spectrum, data_property.name) == "leftmiddleright"
    setattr(spectrum, data_property.name, "replacement PCDATA")

    assert getattr(spectrum, data_property.name) == "replacement PCDATA"
    assert tuple(spectrum.raw_element) == children
    assert document.wrap(children[0]) is wrapper
    assert (
        tuple(
            (
                child.tag,
                dict(child.attrib),
                child.text,
                tuple(grandchild.tag for grandchild in child),
            )
            for child in children
        )
        == child_snapshots
    )
    assert all(child.tail is None for child in children)
    assert "nested" in document.to_string() and "opaque" in document.to_string()


def test_spectrum_child_removal_transfers_tail_into_direct_pcdata() -> None:
    document = CDXMLDocument.from_string(
        '<CDXML><page id="1"><spectrum id="2">before'
        '<objecttag id="3" Name="remove" TagType="String" Value="x"/>after'
        "</spectrum></page></CDXML>"
    )
    spectrum = document.wrap(document.tree.xpath("//spectrum")[0])
    object_tag = document.wrap(document.tree.xpath("//objecttag")[0])
    data_property = next(
        metadata
        for metadata in _metadata_for_tag("spectrum")[1].properties.values()
        if metadata.storage == "text"
    )

    assert getattr(spectrum, data_property.name) == "beforeafter"
    _collection(spectrum, "objecttag").remove(object_tag)

    assert getattr(spectrum, data_property.name) == "beforeafter"
    assert len(spectrum.raw_element) == 0
    assert spectrum.raw_element.text == "beforeafter"


def test_spectrum_text_mutation_keeps_comments_entities_and_unknown_children() -> None:
    document = CDXMLDocument.from_string(
        '<!DOCTYPE CDXML [<!ENTITY marker "entity text">'
        '<!ENTITY remote SYSTEM "http://127.0.0.1:9/unrequested.txt">]>'
        '<CDXML><page id="1"><spectrum id="2">before'
        "<!--keep comment-->&marker;&remote;"
        '<objecttag Name="meta" TagType="String" Value="nested">'
        '<t id="4"><s font="1" size="12" face="0">metadata label</s></t>'
        "</objecttag>middle<?retain instruction?>"
        '<vendor:unknown xmlns:vendor="urn:vendor" keep="yes">opaque</vendor:unknown>'
        "after</spectrum></page></CDXML>"
    )
    spectrum = document.wrap(document.tree.xpath("//spectrum")[0])
    data_property = next(
        metadata
        for metadata in _metadata_for_tag("spectrum")[1].properties.values()
        if metadata.storage == "text"
    )
    retained_nodes = tuple(spectrum.raw_element)
    assert len(retained_nodes) == 6
    assert getattr(spectrum, data_property.name) == "beforemiddleafter"
    object_tag = document.wrap(document.tree.xpath("//objecttag")[0])
    assert object_tag.plain_text == "metadata label"

    setattr(spectrum, data_property.name, "replacement")

    assert tuple(spectrum.raw_element) == retained_nodes
    assert not isinstance(retained_nodes[0].tag, str)
    assert retained_nodes[0].text == "keep comment"
    assert not isinstance(retained_nodes[1].tag, str)
    assert retained_nodes[1].text == "&marker;"
    assert not isinstance(retained_nodes[2].tag, str)
    assert retained_nodes[2].text == "&remote;"
    assert retained_nodes[3] is object_tag.raw_element
    assert object_tag.plain_text == "metadata label"
    assert not isinstance(retained_nodes[4].tag, str)
    processing_instruction = cast(Any, retained_nodes[4])
    assert processing_instruction.target == "retain"
    assert processing_instruction.text == "instruction"
    assert retained_nodes[5].tag == "{urn:vendor}unknown"
    assert retained_nodes[5].get("keep") == "yes"
    assert retained_nodes[5].text == "opaque"
    serialized = document.to_string()
    assert '<!ENTITY marker "entity text"' in serialized
    assert '<!ENTITY remote SYSTEM "http://127.0.0.1:9/unrequested.txt"' in serialized
    assert "keep comment" in serialized
    assert "&marker;" in serialized
    assert "&remote;" in serialized
    assert "<?retain instruction?>" in serialized
    assert 'Value="nested"' in serialized
    assert "opaque" in serialized


def test_local_resource_ids_do_not_enter_document_lookup() -> None:
    document = CDXMLDocument.from_string(
        '<CDXML><fonttable><font id="77" name="Local Font"/></fonttable><page id="1"/></CDXML>'
    )

    assert document.get(77) is None
    assert document.font_table is not None
    assert document.font_table.fonts[0].raw_element.get("id") == "77"


@pytest.mark.parametrize(
    ("canonical", "alias", "field_name", "enum_name", "initial", "replacement"),
    [
        ("ArrowheadType", "ArrowHeadType", "arrowhead_type", "ArrowheadType", "Solid", "Hollow"),
        ("ArrowheadHead", "ArrowHeadHead", "arrowhead_head", "ArrowheadSide", "Full", "HalfLeft"),
        ("ArrowheadTail", "ArrowHeadTail", "arrowhead_tail", "ArrowheadSide", "None", "HalfRight"),
    ],
)
@pytest.mark.parametrize("spelling", ["canonical", "alias"])
def test_curve_alias_read_write_clear_and_reload_preserve_source_spelling(
    canonical: str,
    alias: str,
    field_name: str,
    enum_name: str,
    initial: str,
    replacement: str,
    spelling: str,
) -> None:
    xml_name = canonical if spelling == "canonical" else alias
    document = CDXMLDocument.from_string(
        f'<CDXML><page id="1"><curve id="2" {xml_name}="{initial}"/></page></CDXML>'
    )
    raw_curve = document.tree.xpath("//curve")[0]
    curve = _generated(document.wrap(raw_curve))
    enum_type = cast(type[Enum], getattr(generated_enums, enum_name))

    assert getattr(curve, field_name) == enum_type(initial)
    setattr(curve, field_name, enum_type(replacement))
    assert raw_curve.get(xml_name) == replacement
    assert raw_curve.get(alias if xml_name == canonical else canonical) is None

    reloaded = CDXMLDocument.from_string(document.to_string())
    reloaded_raw = reloaded.tree.xpath("//curve")[0]
    reloaded_curve = _generated(reloaded.wrap(reloaded_raw))
    assert getattr(reloaded_curve, field_name) == enum_type(replacement)
    assert reloaded_raw.get(xml_name) == replacement

    setattr(reloaded_curve, field_name, None)
    assert xml_name not in reloaded_raw.attrib
    assert alias not in reloaded_raw.attrib
    assert canonical not in reloaded_raw.attrib
    assert getattr(reloaded_curve, field_name) is None


@pytest.mark.parametrize(
    ("canonical", "alias", "field_name", "enum_name", "canonical_value", "alias_value"),
    [
        (
            "ArrowheadType",
            "ArrowHeadType",
            "arrowhead_type",
            "ArrowheadType",
            "Solid",
            "Hollow",
        ),
        (
            "ArrowheadHead",
            "ArrowHeadHead",
            "arrowhead_head",
            "ArrowheadSide",
            "Full",
            "HalfLeft",
        ),
        (
            "ArrowheadTail",
            "ArrowHeadTail",
            "arrowhead_tail",
            "ArrowheadSide",
            "None",
            "HalfRight",
        ),
    ],
)
def test_curve_dual_alias_spellings_are_lazy_conflicts_and_repairable(
    canonical: str,
    alias: str,
    field_name: str,
    enum_name: str,
    canonical_value: str,
    alias_value: str,
) -> None:
    document = CDXMLDocument.from_string(
        f'<CDXML><page id="1"><curve id="2" {canonical}="{canonical_value}" '
        f'{alias}="{alias_value}"/></page></CDXML>'
    )
    raw_curve = document.tree.xpath("//curve")[0]
    curve = _generated(document.wrap(raw_curve))
    property_id = _property_id("curve", canonical)
    original_attributes = dict(raw_curve.attrib)

    with pytest.raises(CodecError) as read_error:
        _ = getattr(curve, field_name)
    assert read_error.value.property_id == property_id
    assert read_error.value.xml_tag == "curve"
    assert raw_curve.attrib == original_attributes

    report = document.validate()
    conflicts = [
        issue
        for issue in report.issues
        if issue.code == "conflicting-property-alias" and issue.property_id == property_id
    ]
    assert len(conflicts) == 1

    enum_type = cast(type[Enum], getattr(generated_enums, enum_name))
    with pytest.raises(MutationError) as write_error:
        setattr(curve, field_name, enum_type(alias_value))
    assert write_error.value.property_id == property_id
    assert raw_curve.attrib == original_attributes

    reloaded = CDXMLDocument.from_string(document.to_string())
    reloaded_raw_curve = reloaded.tree.xpath("//curve")[0]
    reloaded_curve = _generated(reloaded.wrap(reloaded_raw_curve))
    assert reloaded_raw_curve.attrib == original_attributes
    with pytest.raises(CodecError) as reloaded_read_error:
        _ = getattr(reloaded_curve, field_name)
    assert reloaded_read_error.value.property_id == property_id
    assert any(
        issue.code == "conflicting-property-alias" and issue.property_id == property_id
        for issue in reloaded.validate().issues
    )

    # Parsing and validation never rewrite aliases. A caller may repair the
    # retained raw tree explicitly, after which typed APIs work as usual.
    raw_curve.attrib.pop(canonical)
    assert getattr(curve, field_name) == enum_type(alias_value)
    assert not any(
        issue.code == "conflicting-property-alias" and issue.property_id == property_id
        for issue in document.validate().issues
    )


def test_identical_values_under_both_curve_spellings_remain_a_conflict() -> None:
    document = CDXMLDocument.from_string(
        '<CDXML><page id="1"><curve id="2" ArrowheadType="Solid" '
        'ArrowHeadType="Solid"/></page></CDXML>'
    )
    raw_curve = document.tree.xpath("//curve")[0]
    curve = _generated(document.wrap(raw_curve))
    property_id = _property_id("curve", "ArrowheadType")

    with pytest.raises(CodecError) as error:
        _ = curve.arrowhead_type
    assert error.value.property_id == property_id
    assert any(
        issue.code == "conflicting-property-alias" and issue.property_id == property_id
        for issue in document.validate().issues
    )
    assert raw_curve.attrib["ArrowheadType"] == raw_curve.attrib["ArrowHeadType"] == "Solid"


def test_curve_creation_uses_canonical_arrowhead_property_spellings() -> None:
    document = CDXMLDocument.from_string('<CDXML><page id="1"/></CDXML>')
    page = _generated(document.pages[0])
    arrowhead_type = generated_enums.ArrowheadType.SOLID
    arrowhead_head = generated_enums.ArrowheadSide.FULL
    arrowhead_tail = generated_enums.ArrowheadSide.VALUE_NONE

    curve = page.curves.create(
        arrowhead_type=arrowhead_type,
        arrowhead_head=arrowhead_head,
        arrowhead_tail=arrowhead_tail,
    )

    assert curve.raw_attributes["ArrowheadType"] == "Solid"
    assert curve.raw_attributes["ArrowheadHead"] == "Full"
    assert curve.raw_attributes["ArrowheadTail"] == "None"
    assert "ArrowHeadType" not in curve.raw_attributes
    assert "ArrowHeadHead" not in curve.raw_attributes
    assert "ArrowHeadTail" not in curve.raw_attributes
