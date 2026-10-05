"""Minimal typed-navigation and structural round-trip tests."""

from __future__ import annotations

from pathlib import Path

import pytest
from lxml import etree

from cdxml_om import (
    MODEL_REGISTRY,
    Bond,
    BondOrder,
    CDXMLDocument,
    CDXMLElement,
    CDXMLRoot,
    CodecError,
    Fragment,
    ModelRegistry,
    Node,
    Page,
    Point2D,
    ReferenceResolutionError,
    UnknownElement,
)

FIXTURE_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "cdxml"
ROUND_TRIP_FIXTURES = (
    "empty.cdxml",
    "page.cdxml",
    "fragment.cdxml",
    "single_node.cdxml",
    "two_nodes_bond.cdxml",
    "charge_isotope.cdxml",
    "unknown_attribute.cdxml",
    "unknown_element.cdxml",
)


def _dom_fingerprint(element: etree.Element) -> tuple[object, ...]:
    tag = element.tag if isinstance(element.tag, str) else type(element).__name__
    return (
        tag,
        tuple(sorted(element.attrib.items())),
        element.text,
        element.tail,
        tuple(_dom_fingerprint(child) for child in element),
    )


def _typed_graph(document: CDXMLDocument) -> tuple[object, ...]:
    return tuple(
        (
            page.id,
            tuple(
                (
                    fragment.id,
                    tuple(
                        (
                            node.id,
                            node.element,
                            node.position,
                            node.charge,
                            node.isotope,
                            tuple(sorted(node.raw_attributes.items())),
                        )
                        for node in fragment.nodes
                    ),
                    tuple(
                        (
                            bond.id,
                            bond.begin.id,
                            bond.end.id,
                            bond.order,
                            bond.display,
                        )
                        for bond in fragment.bonds
                    ),
                )
                for fragment in page.fragments
            ),
        )
        for page in document.pages
    )


@pytest.mark.parametrize("filename", ROUND_TRIP_FIXTURES)
def test_minimal_fixtures_parse_and_round_trip(filename: str) -> None:
    original = CDXMLDocument.from_file(FIXTURE_DIR / filename)
    for page in original.find(Page):
        _ = page.id
    for fragment in original.find(Fragment):
        _ = fragment.id
    for node in original.find(Node):
        _ = (node.id, node.element, node.position, node.charge, node.isotope)
    for bond in original.find(Bond):
        _ = (bond.id, bond.begin, bond.end, bond.order, bond.display)
    original_snapshot = (_typed_graph(original), _dom_fingerprint(original.tree.getroot()))
    serialized = original.to_string()
    restored = CDXMLDocument.from_string(serialized)

    assert restored.root.xml_tag == "CDXML"
    assert len(restored.find(Page)) == len(original.find(Page))
    assert len(restored.find(Fragment)) == len(original.find(Fragment))
    assert len(restored.find(Node)) == len(original.find(Node))
    assert len(restored.find(Bond)) == len(original.find(Bond))
    assert (_typed_graph(restored), _dom_fingerprint(restored.tree.getroot())) == original_snapshot
    assert restored.to_string() == serialized


def test_child_collections_references_and_lookup_share_wrapper_identity() -> None:
    document = CDXMLDocument.from_file(FIXTURE_DIR / "two_nodes_bond.cdxml")
    assert isinstance(document.root, CDXMLElement)
    assert type(document.root) is CDXMLRoot
    assert len(document.pages) == 1

    page = document.pages[0]
    fragment = page.fragments[0]
    nodes = fragment.nodes
    bonds = fragment.bonds
    assert len(nodes) == 2
    assert nodes[0] is nodes.all()[0]
    assert nodes[:] == nodes.all()
    assert tuple(nodes) == tuple(nodes.all())
    assert nodes[0].position == Point2D(1.25, 2.5)
    assert nodes[0].element == 6
    assert nodes[1].element == 8

    bond = bonds[0]
    assert bond.order is BondOrder.TRIPLE
    assert bond.begin is nodes[0]
    assert bond.end is nodes[1]
    assert document.get(3) is nodes[0]
    assert document.get(Node, 3) is nodes[0]
    assert document.get(Bond, 5) is bond
    assert document.objects.wrap(nodes[0].raw_element) is nodes[0]
    assert document.find(Node) == nodes.all()
    assert document.find(UnknownElement) == []


def test_missing_values_use_generated_defaults_without_rewriting_source() -> None:
    source = (
        '<CDXML><page id="1"><fragment id="2">'
        '<n id="3" p="01.000 2.500"/>'
        "</fragment></page></CDXML>"
    )
    document = CDXMLDocument.from_string(source)
    node = document.find(Node)[0]

    assert node.element == 6
    assert node.charge == 0
    assert node.isotope == 0
    assert node.position == Point2D(1, 2.5)
    assert node.raw_attributes["p"] == "01.000 2.500"
    assert 'p="01.000 2.500"' in document.to_string()


def test_bond_uses_generated_single_order_and_solid_display_defaults() -> None:
    document = CDXMLDocument.from_string(
        '<CDXML><page id="1"><fragment id="2"><n id="3"/><n id="4"/>'
        '<b id="5" B="3" E="4"/></fragment></page></CDXML>'
    )
    bond = document.find(Bond)[0]

    assert bond.order is BondOrder.SINGLE
    assert bond.display.name == "SOLID"


def test_to_file_writes_full_parseable_xml_with_matching_declaration(tmp_path: Path) -> None:
    document = CDXMLDocument.from_file(FIXTURE_DIR / "two_nodes_bond.cdxml")
    output = tmp_path / "copy.cdxml"

    document.to_file(output)
    serialized = output.read_bytes()

    assert b"encoding='UTF-8'" in serialized[:80] or b'encoding="UTF-8"' in serialized[:80]
    restored = CDXMLDocument.from_file(output)
    assert _typed_graph(restored) == _typed_graph(document)
    assert _dom_fingerprint(restored.tree.getroot()) == _dom_fingerprint(document.tree.getroot())


def test_charge_and_isotope_fixture_decodes_known_properties() -> None:
    document = CDXMLDocument.from_file(FIXTURE_DIR / "charge_isotope.cdxml")
    node = document.find(Node)[0]

    assert node.charge == -1
    assert node.isotope == 13


def test_unknown_namespaced_tags_and_attributes_remain_navigable_and_opaque() -> None:
    document = CDXMLDocument.from_file(FIXTURE_DIR / "unknown_element.cdxml")
    node = document.find(Node)[0]
    unknown = document.find(UnknownElement)

    assert len(unknown) == 2
    feature = next(item for item in unknown if item.xml_tag == "{urn:vendor}feature")
    assert feature.raw_attributes["key"] == "kept"
    assert feature.parent is document.find(Fragment)[0]
    assert feature.children[0].xml_tag == "nested"

    attribute_document = CDXMLDocument.from_file(FIXTURE_DIR / "unknown_attribute.cdxml")
    assert node.raw_attributes.get("{urn:vendor}hint") is None
    assert attribute_document.find(Node)[0].raw_attributes["{urn:vendor}hint"] == "opaque"
    assert "vendor:feature" in document.to_string()
    assert "{urn:vendor}hint" in str(attribute_document.find(Node)[0].raw_attributes)


def test_namespaced_known_looking_tag_is_not_model_dispatched() -> None:
    document = CDXMLDocument.from_string(
        '<CDXML xmlns:v="urn:vendor"><page id="1"><fragment id="2">'
        '<v:n id="3" Element="8"/></fragment></page></CDXML>'
    )

    assert document.find(Node) == []
    assert len(document.find(UnknownElement)) == 1
    assert document.find(UnknownElement)[0].id == 3
    assert document.get(3) is None
    assert isinstance(MODEL_REGISTRY, ModelRegistry)
    assert MODEL_REGISTRY.for_tag("n") is Node
    assert MODEL_REGISTRY.for_tag("{urn:vendor}n") is None


def test_duplicate_ids_and_dangling_references_fail_only_when_resolved() -> None:
    duplicate = CDXMLDocument.from_file(FIXTURE_DIR / "duplicate_id.cdxml")
    assert len(duplicate.find(Node)) == 2
    with pytest.raises(ReferenceResolutionError, match="ambiguous"):
        duplicate.get(3)
    with pytest.raises(ReferenceResolutionError, match="ambiguous"):
        duplicate.get(Node, 3)
    with pytest.raises(ReferenceResolutionError, match="ambiguous"):
        _ = duplicate.find(Bond)[0].begin

    dangling = CDXMLDocument.from_file(FIXTURE_DIR / "dangling_reference.cdxml")
    assert len(dangling.find(Bond)) == 1
    with pytest.raises(ReferenceResolutionError, match="no Node"):
        _ = dangling.find(Bond)[0].begin


def test_invalid_known_attribute_is_deferred_until_typed_read() -> None:
    document = CDXMLDocument.from_string(
        '<CDXML><page id="1"><fragment id="2"><n id="3"/>'
        '<n id="4"/><b id="5" B="3" E="4" Order="not-an-order"/>'
        "</fragment></page></CDXML>"
    )
    assert len(document.find(Bond)) == 1
    with pytest.raises(CodecError) as error:
        _ = document.find(Bond)[0].order
    assert error.value.property_id == "bond.order"


def test_get_rejects_non_integer_bool_and_out_of_range_ids() -> None:
    document = CDXMLDocument.from_file(FIXTURE_DIR / "page.cdxml")
    with pytest.raises(TypeError):
        document.get(True)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        document.get(Node, True)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        document.get(1.0)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        document.get(-1)


def test_required_reference_attribute_is_reported_as_resolution_error() -> None:
    document = CDXMLDocument.from_string(
        '<CDXML><page id="1"><fragment id="2"><n id="3"/><b id="4" E="3"/>'
        "</fragment></page></CDXML>"
    )

    with pytest.raises(ReferenceResolutionError, match="bond.begin"):
        _ = document.find(Bond)[0].begin


def test_field_mutation_changes_known_attribute_and_preserves_typed_default() -> None:
    document = CDXMLDocument.from_file(FIXTURE_DIR / "single_node.cdxml")
    node = document.find(Node)[0]

    node.charge = 1
    assert node.charge == 1
    assert node.raw_attributes["Charge"] == "1"

    node.charge = None
    assert node.charge == 0
    assert "Charge" not in node.raw_attributes
    with pytest.raises(AttributeError):
        node.chrage = 1  # type: ignore[attr-defined]
