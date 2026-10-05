from typing import assert_type

from cdxml_om import (
    Arrow,
    Bond,
    BondOrder,
    CDXMLDocument,
    CDXMLElement,
    Color,
    ColorTable,
    Font,
    FontTable,
    Fragment,
    Graphic,
    Group,
    Node,
    ObjectReference,
    Page,
    Point2D,
    Point3D,
    ReactionScheme,
    ReactionStep,
    Text,
    TextRun,
    ValidationIssue,
    ValidationReport,
)
from cdxml_om.core.fields import (
    ChildCollection,
    ElementCollection,
    Field,
    RefField,
    RefListField,
)


def public_model_types(document: CDXMLDocument, bond: Bond, fragment: Fragment, node: Node) -> None:
    assert_type(node.element, int)
    assert_type(node.position, Point2D | None)
    assert_type(node.charge, int)
    assert_type(bond.begin, Node)
    assert_type(bond.order, BondOrder)
    assert_type(fragment.nodes, ElementCollection[Node])
    assert_type(fragment.nodes.create(position=(1.0, 2.0)), Node)
    assert_type(node.fragments, ElementCollection[Fragment])
    assert_type(document.objects.references_to(node), tuple[ObjectReference, ...])
    assert_type(bond.raw_reference_id("bond.begin"), int | tuple[int, ...] | None)
    assert_type(Node.element, Field[int])
    assert_type(Bond.begin, RefField[Node])
    assert_type(Fragment.nodes, ChildCollection[Node])


def public_document_types(document: CDXMLDocument) -> None:
    assert_type(document.pages, ElementCollection[Page])
    assert_type(document.groups, ElementCollection[Group])
    assert_type(document.texts, ElementCollection[Text])
    assert_type(document.graphics, ElementCollection[Graphic])
    assert_type(document.arrows, ElementCollection[Arrow])
    assert_type(document.schemes, ElementCollection[ReactionScheme])
    assert_type(document.find(Node), list[Node])
    assert_type(document.get(1), CDXMLElement | None)
    assert_type(document.get(Node, 1), Node | None)
    assert_type(document.pages.create(), Page)
    assert_type(document.validate(), ValidationReport)
    assert_type(document.validate().issues, tuple[ValidationIssue, ...])
    assert_type(document.font_table, FontTable | None)
    assert_type(document.color_table, ColorTable | None)


def public_expanded_types(
    document: CDXMLDocument,
    arrow: Arrow,
    color: Color,
    font: Font,
    graphic: Graphic,
    group: Group,
    step: ReactionStep,
    text: Text,
) -> None:
    assert_type(arrow.head_3d, Point3D | None)
    assert_type(graphic.tail_3d, Point3D | None)
    assert_type(group.fragments, ElementCollection[Fragment])
    assert_type(text.runs, ElementCollection[TextRun])
    assert_type(text.runs.create(content="x"), TextRun)
    assert_type(step.reactants, tuple[CDXMLElement, ...])
    assert_type(step.products, tuple[CDXMLElement, ...])
    assert_type(step.arrows, tuple[CDXMLElement, ...])
    assert_type(step.raw_reference_ids("reactants"), tuple[int, ...] | None)
    assert_type(font.id, int)
    assert_type(font.charset, str | None)
    assert_type(color.r, float)
    assert_type(document.create_font_table(), FontTable)
    assert_type(document.create_color_table(), ColorTable)
    assert_type(Group.fragments, ChildCollection[Fragment])
    assert_type(ReactionStep.reactants, RefListField[CDXMLElement])
