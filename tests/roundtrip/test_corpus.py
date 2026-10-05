"""Round-trip checks for two real-world RDKit CDXML source fixtures."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

import pytest
from lxml import etree

from cdxml_om import Bond, BondOrder, CDXMLDocument, CDXMLElement, Node, Point2D

CORPUS_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "corpus"


@dataclass(frozen=True, slots=True)
class CorpusCase:
    filename: str
    sha256: str
    page_id: int
    fragment_id: int
    node_ids: tuple[int, ...]
    positions: tuple[tuple[float, float], ...]
    charges: tuple[int, ...]
    bond_ids: tuple[int, ...]
    endpoints: tuple[tuple[int, int], ...]
    bond_orders: tuple[BondOrder, ...]
    unknown_node_attributes: tuple[tuple[int, tuple[tuple[str, str], ...]], ...]
    rich_text: tuple[str, ...]
    extra_unknown_tags: tuple[str, ...]


CASES = (
    CorpusCase(
        filename="atom-query.cdxml",
        sha256="714a012f09e77f7d9adafe90450829e327ddff35ccecc1464eed813eea021f47",
        page_id=14,
        fragment_id=15,
        node_ids=(1, 2, 3, 4, 5, 6),
        positions=(
            (201.02, 207.0),
            (201.02, 237.0),
            (227.0, 252.0),
            (252.98, 237.0),
            (252.98, 207.0),
            (227.0, 192.0),
        ),
        charges=(0, 0, 0, 0, 0, 0),
        bond_ids=(7, 8, 9, 10, 11, 12),
        endpoints=((1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1)),
        bond_orders=(
            BondOrder.DOUBLE,
            BondOrder.SINGLE,
            BondOrder.DOUBLE,
            BondOrder.SINGLE,
            BondOrder.DOUBLE,
            BondOrder.SINGLE,
        ),
        unknown_node_attributes=((6, (("NodeType", "ElementList"), ("ElementList", "6 7"))),),
        rich_text=("[N,C]",),
        extra_unknown_tags=("t", "s"),
    ),
    CorpusCase(
        filename="mol1.cdxml",
        sha256="064b031c9e25bc05fa3f021a7a2d48a1cf596ae6ff55cfa67a21d237f5604817",
        page_id=34,
        fragment_id=35,
        node_ids=(22, 23, 24, 25, 26),
        positions=(
            (131.35, 270.0),
            (131.35, 300.0),
            (159.89, 309.27),
            (177.52, 285.0),
            (159.89, 260.73),
        ),
        charges=(0, 0, 0, 0, -1),
        bond_ids=(27, 28, 29, 30, 31),
        endpoints=((22, 23), (23, 24), (24, 25), (25, 26), (26, 22)),
        bond_orders=(
            BondOrder.DOUBLE,
            BondOrder.SINGLE,
            BondOrder.DOUBLE,
            BondOrder.SINGLE,
            BondOrder.SINGLE,
        ),
        unknown_node_attributes=(
            (
                26,
                (
                    ("NumHydrogens", "1"),
                    ("ImplicitHydrogens", "yes"),
                    ("AS", "N"),
                ),
            ),
        ),
        rich_text=("CH",),
        extra_unknown_tags=("t", "s", "graphic", "represent"),
    ),
)


def _safe_tree(source: bytes) -> etree._ElementTree:
    parser = etree.XMLParser(
        resolve_entities=False,
        load_dtd=False,
        no_network=True,
        recover=False,
        remove_blank_text=False,
        remove_comments=False,
        remove_pis=False,
        strip_cdata=False,
    )
    return etree.parse(BytesIO(source), parser)


def _fingerprint(element: etree._Element) -> tuple[object, ...]:
    if isinstance(element, etree._Comment):
        tag = "#comment"
    elif isinstance(element, etree._ProcessingInstruction):
        tag = f"#pi:{element.target}"
    else:
        tag = element.tag
    return (
        tag,
        tuple(sorted(element.attrib.items())),
        element.text,
        element.tail,
        tuple(_fingerprint(child) for child in element),
    )


def _assert_typed_graph(document: CDXMLDocument, case: CorpusCase) -> None:
    assert len(document.pages) == 1
    page = document.pages[0]
    assert page.id == case.page_id
    assert document.get(type(page), case.page_id) is page

    assert len(page.fragments) == 1
    fragment = page.fragments[0]
    assert fragment.id == case.fragment_id
    assert document.get(type(fragment), case.fragment_id) is fragment

    nodes = fragment.nodes.all()
    bonds = fragment.bonds.all()
    assert len(nodes) == len(case.node_ids)
    assert len(bonds) == len(case.bond_ids)
    assert all(isinstance(node, Node) for node in nodes)
    assert all(isinstance(bond, Bond) for bond in bonds)
    assert tuple(node.id for node in nodes) == case.node_ids
    assert tuple(node.position for node in nodes) == tuple(Point2D(x, y) for x, y in case.positions)
    assert tuple(node.charge for node in nodes) == case.charges

    nodes_by_id = {}
    for node, node_id in zip(nodes, case.node_ids, strict=True):
        assert node.id == node_id
        nodes_by_id[node_id] = node
        assert document.get(Node, node_id) is node

    assert tuple(bond.id for bond in bonds) == case.bond_ids
    assert tuple(bond.order for bond in bonds) == case.bond_orders
    for bond, (begin_id, end_id) in zip(bonds, case.endpoints, strict=True):
        assert bond.begin is nodes_by_id[begin_id]
        assert bond.end is nodes_by_id[end_id]
        assert bond.begin is document.get(Node, begin_id)
        assert bond.end is document.get(Node, end_id)

    root_attributes = document.root.raw_attributes
    assert root_attributes["CreationProgram"] == "ChemDraw 6.0.1"
    assert root_attributes["LabelFont"] == "3"
    assert root_attributes["CaptionFont"] == "4"

    elements = document.find(CDXMLElement)
    element_tags = {element.xml_tag for element in elements}
    assert {"colortable", "color", "fonttable", "font"} <= element_tags
    assert set(case.extra_unknown_tags) <= element_tags
    fonts = [element for element in elements if element.xml_tag == "font"]
    assert tuple(element.raw_attributes["id"] for element in fonts) == ("3", "4")
    assert tuple(element.text for element in elements if element.xml_tag == "s") == case.rich_text

    for node_id, expected_attributes in case.unknown_node_attributes:
        attributes = nodes_by_id[node_id].raw_attributes
        for name, value in expected_attributes:
            assert attributes[name] == value


@pytest.mark.parametrize("case", CASES, ids=lambda case: case.filename)
def test_real_world_corpus_round_trips_without_losing_structure(case: CorpusCase) -> None:
    source_path = CORPUS_DIR / case.filename
    source_bytes = source_path.read_bytes()
    assert hashlib.sha256(source_bytes).hexdigest() == case.sha256

    source_tree = _safe_tree(source_bytes)
    source_fingerprint = _fingerprint(source_tree.getroot())

    document = CDXMLDocument.from_file(source_path)
    _assert_typed_graph(document, case)
    first_output = document.to_string()

    reparsed = CDXMLDocument.from_string(first_output)
    _assert_typed_graph(reparsed, case)
    second_output = reparsed.to_string()

    first_tree = _safe_tree(first_output.encode("utf-8"))
    second_tree = _safe_tree(second_output.encode("utf-8"))
    assert _fingerprint(first_tree.getroot()) == source_fingerprint
    assert _fingerprint(second_tree.getroot()) == source_fingerprint

    for tree in (source_tree, first_tree, second_tree):
        tags = [element.tag for element in tree.getroot().iter() if isinstance(element.tag, str)]
        assert tags.count("fonttable") == 1
        assert tags.count("colortable") == 1
        assert tags.count("font") == 2
        assert tags.count("color") == 8
        assert [element.text for element in tree.xpath(".//s")] == list(case.rich_text)
