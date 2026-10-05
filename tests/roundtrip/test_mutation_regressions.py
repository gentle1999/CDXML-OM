"""Mutation, ID-allocation, and validation regression coverage."""

from __future__ import annotations

from collections import Counter
from io import BytesIO
from pathlib import Path
from typing import Any

import pytest
from lxml import etree

from cdxml_om import (
    Bond,
    BondOrder,
    CDXMLDocument,
    Fragment,
    Node,
    Page,
    Point2D,
    UnknownElement,
)
from cdxml_om.core.errors import CDXMLError, MutationError, ReferenceResolutionError

ROOT = Path(__file__).resolve().parents[2]
CDXML_FIXTURES = ROOT / "tests" / "fixtures" / "cdxml"
CORPUS_FIXTURES = ROOT / "tests" / "fixtures" / "corpus"
UINT32_MAX = 2**32 - 1

_TWO_NODES = (
    '<CDXML><page id="1"><fragment id="2">'
    '<n id="3" Element="6"/><n id="4" Element="8"/>'
    "</fragment></page></CDXML>"
)

_PRESERVATION_SOURCE = """<?xml version="1.0" encoding="UTF-8"?>
<CDXML VendorRoot="root-value">
  <!-- preserve this comment and child order -->
  <page id="0001" VendorPage="page-value">
    <fragment id="0002" VendorFragment="fragment-value">
      <n id="0003" Element="06" p="001.250 02.500" VendorNode="node-value">
        <v:payload xmlns:v="urn:vendor" key="opaque"><![CDATA[keep <opaque> & lexical]]></v:payload>
      </n>
      <!-- keep the second node after the first -->
      <n id="0004" Element="8" p="3.0 4.0" VendorNode="second-value"/>
      <v:before xmlns:v="urn:vendor"/>
      <b id="0005" B="0003" E="0004" Order="3" VendorBond="bond-value"/>
      <v:after xmlns:v="urn:vendor"/>
    </fragment>
  </page>
</CDXML>"""

_WRONG_TARGET = (
    '<CDXML><page id="1"><fragment id="2"><n id="3"/>'
    '<b id="5" B="4" E="3"/></fragment><fragment id="4"/>'
    "</page></CDXML>"
)

_OPAQUE_AND_DANGLING = (
    '<CDXML xmlns:v="urn:vendor"><page id="1"><fragment id="2">'
    '<n id="3"/><n id="4"/><b id="5" B="4" E="7"/>'
    '<v:opaque id="6" marker="reserve"/>'
    "</fragment></page></CDXML>"
)


def _xml_parser() -> etree.XMLParser:
    return etree.XMLParser(
        resolve_entities=False,
        load_dtd=False,
        no_network=True,
        recover=False,
        remove_blank_text=False,
        remove_comments=False,
        remove_pis=False,
        strip_cdata=False,
    )


def _parse_tree(source: str | bytes) -> Any:
    content = source.encode("utf-8") if isinstance(source, str) else source
    return etree.parse(BytesIO(content), _xml_parser())


def _fingerprint(element: Any) -> tuple[object, ...]:
    if isinstance(element, etree._Comment):  # pyright: ignore[reportPrivateUsage]
        tag = "#comment"
    elif isinstance(
        element,
        etree._ProcessingInstruction,  # pyright: ignore[reportPrivateUsage]
    ):
        tag = f"#pi:{element.target}"
    else:
        tag = element.tag
    attributes = element.attrib  # pyright: ignore[reportDeprecated]
    return (
        tag,
        tuple(attributes.items()),
        element.text,
        element.tail,
        tuple(_fingerprint(child) for child in element),
    )


def _report_has_issue(
    document: CDXMLDocument,
    code: str,
    property_id: str | None = None,
) -> bool:
    return any(
        issue.code == code and (property_id is None or issue.property_id == property_id)
        for issue in document.validate().issues
    )


def _restore_charge(
    tree: Any,
    node_id: str,
    original_value: str | None,
) -> None:
    node = next(element for element in tree.getroot().iter("n") if element.get("id") == node_id)
    if original_value is None:
        node.attrib.pop("Charge", None)
    else:
        node.set("Charge", original_value)


def test_create_typed_graph_assigns_ids_and_reparses_references_by_identity() -> None:
    document = CDXMLDocument.from_string("<CDXML/>")
    pages = document.pages
    page = pages.create()
    fragments = page.fragments
    fragment = fragments.create()
    nodes = fragment.nodes
    bonds = fragment.bonds

    carbon = nodes.create(element=6)
    carbon.charge = 1
    oxygen = nodes.create(element=8, position=(10.0, 20.0))
    bond = bonds.create(begin=carbon, end=oxygen, order=2)

    assert carbon.charge == 1
    assert oxygen.element == 8
    assert oxygen.position == Point2D(10.0, 20.0)
    assert bond.order is BondOrder.DOUBLE
    assert bond.begin is carbon
    assert bond.end is oxygen

    page_id = page.id
    fragment_id = fragment.id
    carbon_id = carbon.id
    oxygen_id = oxygen.id
    bond_id = bond.id
    assert page_id is not None
    assert fragment_id is not None
    assert carbon_id is not None
    assert oxygen_id is not None
    assert bond_id is not None
    ids = (page_id, fragment_id, carbon_id, oxygen_id, bond_id)
    assert len(set(ids)) == len(ids)
    assert all(0 < object_id <= UINT32_MAX for object_id in ids)
    assert document.validate().is_valid

    carbon_references = document.objects.references_to(carbon)
    oxygen_references = document.objects.references_to(oxygen)
    assert len(carbon_references) == 1
    assert carbon_references[0].source is bond
    assert carbon_references[0].property_id == "bond.begin"
    assert carbon_references[0].target_id == carbon_id
    assert len(oxygen_references) == 1
    assert oxygen_references[0].source is bond
    assert oxygen_references[0].property_id == "bond.end"

    restored = CDXMLDocument.from_string(document.to_string())
    restored_page = restored.get(Page, page_id)
    restored_fragment = restored.get(Fragment, fragment_id)
    restored_carbon = restored.get(Node, carbon_id)
    restored_oxygen = restored.get(Node, oxygen_id)
    restored_bond = restored.get(Bond, bond_id)
    assert restored_page is not None
    assert restored_fragment is not None
    assert restored_carbon is not None
    assert restored_oxygen is not None
    assert restored_bond is not None
    assert restored.pages[0] is restored_page
    assert restored_page.fragments[0] is restored_fragment
    assert restored_fragment.nodes[0] is restored_carbon
    assert restored_fragment.nodes[1] is restored_oxygen
    assert restored_fragment.bonds[0] is restored_bond
    assert restored_carbon.charge == 1
    assert restored_oxygen.position == Point2D(10.0, 20.0)
    assert restored_bond.begin is restored_carbon
    assert restored_bond.end is restored_oxygen
    assert restored_bond.order is BondOrder.DOUBLE
    assert restored.validate().is_valid


def test_failed_creates_reject_invalid_foreign_and_wrong_type_references_atomically() -> None:
    document = CDXMLDocument.from_string(_TWO_NODES)
    fragment = document.pages[0].fragments[0]
    local_node = fragment.nodes[0]
    original = document.to_string()

    with pytest.raises(MutationError) as invalid_error:
        fragment.nodes.create(unknown_property=1)
    assert isinstance(invalid_error.value, CDXMLError)
    assert document.to_string() == original

    with pytest.raises(MutationError):
        fragment.nodes.create(element="not-an-integer")
    assert document.to_string() == original

    with pytest.raises(MutationError):
        fragment.nodes.create(element=6, position=(10**400, 2))
    assert document.to_string() == original

    oversized_position = Point2D(10**400, 2)
    with pytest.raises(MutationError):
        local_node.position = oversized_position
    assert document.to_string() == original

    foreign_document = CDXMLDocument.from_string(_TWO_NODES)
    foreign_node = foreign_document.pages[0].fragments[0].nodes[0]
    with pytest.raises(MutationError):
        fragment.bonds.create(begin=local_node, end=foreign_node, order=2)
    assert document.to_string() == original

    with pytest.raises(MutationError):
        fragment.bonds.create(begin=fragment, end=local_node, order=2)
    assert document.to_string() == original
    assert len(fragment.bonds) == 0


def test_collections_are_live_across_create_and_remove() -> None:
    document = CDXMLDocument.from_string("<CDXML/>")
    pages = document.pages
    page = pages.create()
    fragments = page.fragments
    fragment = fragments.create()
    nodes = fragment.nodes
    bonds = fragment.bonds

    first = nodes.create(element=6)
    second = nodes.create(element=8)
    bond = bonds.create(begin=first, end=second, order=2)
    assert len(pages) == 1
    assert len(fragments) == 1
    assert len(nodes) == 2
    assert len(bonds) == 1
    assert nodes[0] is first
    assert bonds.all() == [bond]

    bonds.remove(bond)
    assert len(bonds) == 0
    nodes.remove(second)
    assert len(nodes) == 1
    assert nodes[0] is first
    fragments.remove(fragment)
    assert len(fragments) == 0
    pages.remove(page)
    assert len(pages) == 0
    validation = document.validate()
    page_cardinality_issues = [
        issue
        for issue in validation.errors
        if issue.code == "child-cardinality" and issue.element is document.root
    ]
    assert len(page_cardinality_issues) == 1
    assert "pages contains 0; expected 1..unbounded" in page_cardinality_issues[0].message


def test_detached_subtree_cannot_be_mutated_or_used_as_reference_target() -> None:
    document = CDXMLDocument.from_string("<CDXML/>")
    page = document.pages.create()
    detached_fragment = page.fragments.create()
    detached_nodes = detached_fragment.nodes
    detached_node = detached_nodes.create(element=6)
    attached_fragment = page.fragments.create()
    attached_node = attached_fragment.nodes.create(element=8)
    attached_bonds = attached_fragment.bonds

    page.fragments.remove(detached_fragment)
    original = document.to_string()

    with pytest.raises(MutationError):
        detached_nodes.create(element=7)
    assert document.to_string() == original

    with pytest.raises(MutationError):
        detached_node.charge = 1
    assert document.to_string() == original

    with pytest.raises(MutationError):
        attached_bonds.create(begin=detached_node, end=attached_node, order=2)
    assert document.to_string() == original


def test_id_allocator_skips_removed_opaque_and_dangling_target_ids() -> None:
    document = CDXMLDocument.from_string(_OPAQUE_AND_DANGLING)
    fragment = document.pages[0].fragments[0]
    removed = fragment.nodes[0]
    removed_id = removed.id
    assert removed_id is not None
    fragment.nodes.remove(removed)

    created = fragment.nodes.create(element=8)
    created_id = created.id
    assert created_id is not None
    assert created_id not in {removed_id, 6, 7}
    assert created_id <= UINT32_MAX
    assert document.get(Node, created_id) is created
    raw_ids: list[int] = []
    for element in document.tree.getroot().iter():
        if isinstance(element.tag, str):
            raw_id = element.get("id")
            if raw_id is not None and raw_id.isdigit():
                raw_ids.append(int(raw_id))
    assert Counter(raw_ids)[created_id] == 1
    assert any(item.id == 6 for item in document.find(UnknownElement))
    assert _report_has_issue(document, "dangling-reference", "bond.end")


def test_removing_referenced_node_keeps_bond_and_reports_dangling_reference() -> None:
    document = CDXMLDocument.from_file(CDXML_FIXTURES / "two_nodes_bond.cdxml")
    fragment = document.pages[0].fragments[0]
    node = fragment.nodes[0]
    bond = fragment.bonds[0]
    references = document.objects.references_to(node)
    assert any(item.source is bond and item.property_id == "bond.begin" for item in references)

    fragment.nodes.remove(node)

    assert len(fragment.bonds) == 1
    assert fragment.bonds[0] is bond
    assert any(
        issue.code == "dangling-reference" and issue.property_id == "bond.begin"
        for issue in document.validate().errors
    )
    with pytest.raises(ReferenceResolutionError):
        _ = bond.begin


def test_mutation_preserves_unknown_content_comments_cdata_and_lexical_attributes() -> None:
    source_tree = _parse_tree(_PRESERVATION_SOURCE)
    document = CDXMLDocument.from_string(_PRESERVATION_SOURCE)
    node = document.get(Node, 3)
    assert node is not None
    old_charge = node.raw_attributes.get("Charge")

    node.charge = 1
    assert document.get(Node, 3) is node

    serialized = document.to_string()
    assert 'p="001.250 02.500"' in serialized
    assert 'Element="06"' in serialized
    assert 'Order="3"' in serialized
    assert 'VendorRoot="root-value"' in serialized
    assert 'VendorNode="node-value"' in serialized
    assert "<!-- preserve this comment and child order -->" in serialized
    assert "<!-- keep the second node after the first -->" in serialized
    assert "<![CDATA[keep <opaque> & lexical]]>" in serialized

    output_tree = _parse_tree(serialized.encode("utf-8"))
    _restore_charge(output_tree, "0003", old_charge)
    assert _fingerprint(output_tree.getroot()) == _fingerprint(source_tree.getroot())

    restored = CDXMLDocument.from_string(serialized)
    restored_node = restored.get(Node, 3)
    restored_bond = restored.get(Bond, 5)
    assert restored_node is not None
    assert restored_node.charge == 1
    assert restored_bond is not None
    assert len(restored.pages) == 1
    assert len(restored.pages[0].fragments) == 1
    assert len(restored.pages[0].fragments[0].nodes) == 2
    assert len(restored.pages[0].fragments[0].bonds) == 1
    assert restored_bond.begin is restored.get(Node, 3)
    assert restored_bond.end is restored.get(Node, 4)


@pytest.mark.parametrize("filename", ("atom-query.cdxml", "mol1.cdxml"))
def test_known_corpus_mutation_preserves_fonts_colors_and_unknown_tables(filename: str) -> None:
    source = (CORPUS_FIXTURES / filename).read_bytes()
    source_tree = _parse_tree(source)
    document = CDXMLDocument.from_string(source)
    node = document.find(Node)[0]
    node_id = node.id
    assert node_id is not None
    raw_node_id = node.raw_attributes["id"]
    old_charge = node.raw_attributes.get("Charge")

    node.charge = 1
    assert document.get(Node, node_id) is node

    output = document.to_string()
    output_tree = _parse_tree(output.encode("utf-8"))
    _restore_charge(output_tree, raw_node_id, old_charge)
    assert _fingerprint(output_tree.getroot()) == _fingerprint(source_tree.getroot())

    for tag in ("fonttable", "colortable", "font", "color"):
        before = tuple(_fingerprint(element) for element in source_tree.getroot().iter(tag))
        after = tuple(_fingerprint(element) for element in output_tree.getroot().iter(tag))
        assert after == before

    known_tags = {"CDXML", "page", "fragment", "n", "b"}
    unknown_before = tuple(
        _fingerprint(element)
        for element in source_tree.getroot().iter()
        if isinstance(element.tag, str) and element.tag not in known_tags
    )
    unknown_after = tuple(
        _fingerprint(element)
        for element in output_tree.getroot().iter()
        if isinstance(element.tag, str) and element.tag not in known_tags
    )
    assert unknown_after == unknown_before
    same_node = document.get(Node, node_id)
    assert same_node is not None
    assert same_node.id == node_id

    restored = CDXMLDocument.from_string(output)
    restored_node = restored.get(Node, node_id)
    assert restored_node is not None
    assert restored_node.charge == 1
    assert len(restored.find(Node)) == len(document.find(Node))
    assert len(restored.find(Bond)) == len(document.find(Bond))
    restored_bonds = restored.find(Bond)
    if restored_bonds:
        # The selected corpus fixtures have well-formed typed references; check
        # that endpoint resolution returns the reparsed document's own wrappers.
        representative = restored_bonds[0]
        begin = representative.begin
        end = representative.end
        assert begin is not None
        assert end is not None
        begin_id = begin.id
        end_id = end.id
        assert begin_id is not None
        assert end_id is not None
        assert restored.get(Node, begin_id) is begin
        assert restored.get(Node, end_id) is end


def test_wrong_target_and_duplicate_loaded_documents_remain_preservable_and_validated() -> None:
    wrong_source = _WRONG_TARGET.encode("utf-8")
    wrong_tree = _parse_tree(wrong_source)
    wrong_target = CDXMLDocument.from_string(wrong_source)
    wrong_bond = wrong_target.find(Bond)[0]
    wrong_report = wrong_target.validate()
    assert not wrong_report.is_valid
    assert any(
        issue.code == "wrong-reference-target" and issue.property_id == "bond.begin"
        for issue in wrong_report.errors
    )
    with pytest.raises(ReferenceResolutionError):
        _ = wrong_bond.begin
    wrong_after = _parse_tree(wrong_target.to_string())
    assert _fingerprint(wrong_after.getroot()) == _fingerprint(wrong_tree.getroot())

    duplicate_source = (CDXML_FIXTURES / "duplicate_id.cdxml").read_bytes()
    duplicate_tree = _parse_tree(duplicate_source)
    duplicate = CDXMLDocument.from_string(duplicate_source)
    duplicate_report = duplicate.validate()
    assert not duplicate_report.is_valid
    assert any(
        issue.code == "duplicate-id" and issue.property_id == "common.id"
        for issue in duplicate_report.errors
    )
    duplicate_after = _parse_tree(duplicate.to_string())
    assert _fingerprint(duplicate_after.getroot()) == _fingerprint(duplicate_tree.getroot())
