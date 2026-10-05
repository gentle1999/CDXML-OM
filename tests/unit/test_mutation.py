"""Unit coverage for atomic XML-backed mutation and document IDs."""

from __future__ import annotations

import pytest

from cdxml_om import Bond, BondDisplay, BondOrder, CDXMLDocument, MutationError, Node, Point2D
from cdxml_om.core.errors import ReferenceResolutionError

_GRAPH = (
    '<CDXML xmlns:v="urn:vendor"><page id="1"><fragment id="2">'
    '<n id="3" Element="6" p="01.000 2.000"/><n id="4" Element="8"/>'
    '<b id="5" B="3" E="4" Order="1"/>'
    '<v:resource id="6"/><b id="7" B="3" E="429"/>'
    "</fragment></page></CDXML>"
)


def test_field_setters_encode_values_and_preserve_unmodified_lexical_data() -> None:
    document = CDXMLDocument.from_string(_GRAPH)
    fragment = document.pages[0].fragments[0]
    node = fragment.nodes[0]
    bond = fragment.bonds[0]

    node.position = (1.25, 2.5)
    node.charge = -1
    bond.order = BondOrder.TRIPLE
    bond.display = BondDisplay.BOLD

    assert node.position == Point2D(1.25, 2.5)
    assert node.raw_attributes["Charge"] == "-1"
    assert bond.order is BondOrder.TRIPLE
    assert bond.raw_attributes["Order"] == "3"
    assert bond.raw_attributes["Display"] == "Bold"
    assert fragment.nodes[1].raw_attributes.get("p") is None
    assert 'Element="6"' in document.to_string()
    assert 'p="1.25 2.5"' in document.to_string()


def test_invalid_field_and_reference_updates_are_atomic() -> None:
    document = CDXMLDocument.from_string(_GRAPH)
    fragment = document.pages[0].fragments[0]
    node = fragment.nodes[0]
    bond = fragment.bonds[0]
    original_node = dict(node.raw_attributes)
    original_bond = dict(bond.raw_attributes)

    with pytest.raises(MutationError, match="expected int"):
        node.charge = "not-an-integer"  # type: ignore[assignment]
    with pytest.raises(MutationError) as overflow_error:
        node.position = (10**400, 2)
    assert overflow_error.value.property_id == "node.position"
    with pytest.raises(MutationError, match="exact Node wrapper"):
        bond.begin = bond  # type: ignore[assignment]

    foreign_document = CDXMLDocument.from_string(_GRAPH)
    with pytest.raises(MutationError, match="different document"):
        bond.begin = foreign_document.find(Node)[0]

    assert dict(node.raw_attributes) == original_node
    assert dict(bond.raw_attributes) == original_bond
    assert bond.begin is node


def test_id_rename_updates_lookup_but_does_not_rewrite_raw_references() -> None:
    document = CDXMLDocument.from_string(_GRAPH)
    node = document.find(Node)[0]
    bond = document.find(Bond)[0]

    node.id = 9

    assert document.get(Node, 9) is node
    assert document.get(Node, 3) is None
    assert bond.raw_reference_id("bond.begin") == 3
    assert bond.raw_attributes["B"] == "3"
    with pytest.raises(ReferenceResolutionError):
        _ = bond.begin
    assert any(
        issue.code == "dangling-reference" and issue.property_id == "bond.begin"
        for issue in document.validate().errors
    )


def test_auto_ids_reserve_unknown_ids_dangling_refs_and_removed_ids() -> None:
    document = CDXMLDocument.from_string(_GRAPH)
    fragment = document.pages[0].fragments[0]
    first = fragment.nodes.create(element=6)

    assert first.id == 8
    fragment.nodes.remove(first)
    second = fragment.nodes.create(position=(5, 6))

    assert second.id == 9
    assert document.get(Node, 8) is None
    assert document.get(Node, 9) is second
    assert second.position == Point2D(5.0, 6.0)


def test_remove_preserves_mixed_content_after_the_removed_element() -> None:
    document = CDXMLDocument.from_string(
        "<CDXML><page id='1'><fragment id='2'><n id='3'/>OPAQUE-TAIL"
        "<future/></fragment></page></CDXML>"
    )
    fragment = document.pages[0].fragments[0]
    node = fragment.nodes[0]

    fragment.nodes.remove(node)

    assert len(fragment.nodes) == 0
    assert "OPAQUE-TAIL" in document.to_string()
    assert document.to_string().index("OPAQUE-TAIL") < document.to_string().index("<future")
    assert node.tail is None


@pytest.mark.parametrize("invalid_text", ["bad\x00text", "bad\x01text", "bad\ud800text"])
def test_invalid_xml_characters_cannot_mutate_text_run(invalid_text: str) -> None:
    document = CDXMLDocument.from_string(
        '<CDXML><page id="1"><t id="2"><s>old text</s></t></page></CDXML>'
    )
    run = document.pages[0].texts[0].runs[0]
    before = document.to_string()

    with pytest.raises(MutationError) as error:
        run.content = invalid_text

    assert error.value.property_id == "text_run.content"
    assert run.content == "old text"
    assert document.to_string() == before


@pytest.mark.parametrize("invalid_text", ["bad\x00name", "bad\x01name", "bad\ud800name"])
def test_invalid_xml_characters_cannot_mutate_font_name(invalid_text: str) -> None:
    document = CDXMLDocument.from_string(
        '<CDXML><page id="1"/><fonttable><font id="1" name="Old"/></fonttable></CDXML>'
    )
    table = document.font_table
    assert table is not None
    font = table.fonts[0]
    before = document.to_string()

    with pytest.raises(MutationError) as error:
        font.name = invalid_text

    assert error.value.property_id == "font.name"
    assert font.name == "Old"
    assert document.to_string() == before


@pytest.mark.parametrize("invalid_text", ["bad\x00name", "bad\x01name", "bad\ud800name"])
def test_invalid_font_creation_is_atomic_and_does_not_consume_local_id(
    invalid_text: str,
) -> None:
    document = CDXMLDocument.from_string(
        '<CDXML><page id="1"/><fonttable><font id="1" name="Old"/></fonttable></CDXML>'
    )
    table = document.font_table
    assert table is not None
    before = document.to_string()

    with pytest.raises(MutationError) as error:
        table.fonts.create(name=invalid_text)

    assert error.value.property_id == "font.name"
    assert document.to_string() == before
    created = table.fonts.create(name="New Font")
    assert created.id == 2


def test_valid_unicode_text_and_font_values_round_trip() -> None:
    document = CDXMLDocument.from_string(
        '<CDXML><page id="1"><t id="2"><s>old text</s></t></page>'
        '<fonttable><font id="1" name="Old"/></fonttable></CDXML>'
    )
    run = document.pages[0].texts[0].runs[0]
    table = document.font_table
    assert table is not None
    font = table.fonts[0]

    run.content = "café ☃"
    font.name = "字体 Ω"
    added = table.fonts.create(name="書体")

    restored = CDXMLDocument.from_string(document.to_string())
    assert restored.pages[0].texts[0].runs[0].content == "café ☃"
    restored_table = restored.font_table
    assert restored_table is not None
    assert restored_table.fonts[0].name == "字体 Ω"
    assert restored_table.fonts[1].id == added.id == 2
    assert restored_table.fonts[1].name == "書体"


def test_node_may_contain_a_generated_fragment_per_the_pinned_dtd() -> None:
    document = CDXMLDocument.from_string(
        '<CDXML><page id="1"><fragment id="2"><n id="3"/></fragment></page></CDXML>'
    )
    node = document.pages[0].fragments[0].nodes[0]

    nested = node.fragments.create()

    assert nested.parent is node
    assert node.fragments[0] is nested
    assert document.validate().is_valid
