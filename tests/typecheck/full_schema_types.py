"""Static public-type assertions for the expanded generated CDXML models."""

from typing import assert_type

from cdxml_om import (
    Arrow,
    BioShape,
    Bond,
    CDXMLDocument,
    CDXMLRoot,
    ColorTable,
    Constraint,
    Curve,
    ElementList,
    FontTable,
    GenericList,
    Geometry,
    Graphic,
    Node,
    ObjectTag,
    Page,
    PlasmidRegion,
    Point2D,
    Point3D,
    Spectrum,
    TemplateGrid,
    TLCPlate,
)
from cdxml_om.core.fields import ChildCollection, ElementCollection, Field, RefListField


def expanded_document_types(document: CDXMLDocument, root: CDXMLRoot) -> None:
    assert_type(document.root, CDXMLRoot)
    assert_type(root.color_tables, ElementCollection[ColorTable])
    assert_type(root.font_tables, ElementCollection[FontTable])
    assert_type(root.pages, ElementCollection[Page])
    assert_type(root.template_grids, ElementCollection[TemplateGrid])
    assert_type(CDXMLRoot.color_tables, ChildCollection[ColorTable])
    assert_type(CDXMLRoot.font_tables, ChildCollection[FontTable])
    assert_type(CDXMLRoot.pages, ChildCollection[Page])
    assert_type(CDXMLRoot.template_grids, ChildCollection[TemplateGrid])


def expanded_geometry_types(
    arrow: Arrow,
    bio_shape: BioShape,
    curve: Curve,
    node: Node,
    plasmid_region: PlasmidRegion,
) -> None:
    assert_type(arrow.center_3d, Point3D | None)
    assert_type(arrow.head_3d, Point3D | None)
    assert_type(arrow.tail_3d, Point3D | None)
    assert_type(bio_shape.major_axis_end_3d, Point3D | None)
    assert_type(bio_shape.minor_axis_end_3d, Point3D | None)
    assert_type(curve.curve_points, tuple[Point2D, ...] | None)
    assert_type(curve.curve_points3_d, tuple[Point3D, ...] | None)
    assert_type(node.xyz, Point3D | None)
    assert_type(node.attachments, tuple[Node, ...])
    assert_type(Node.attachments, RefListField[Node])
    assert_type(plasmid_region.center_3d, Point3D | None)
    assert_type(plasmid_region.major_axis_end_3d, Point3D | None)
    assert_type(plasmid_region.minor_axis_end_3d, Point3D | None)


def expanded_irregular_value_types(node: Node) -> None:
    assert_type(node.element_list, ElementList | None)
    assert_type(node.generic_list, GenericList | None)
    assert_type(Node.element_list, Field[ElementList | None])
    assert_type(Node.generic_list, Field[GenericList | None])


def expanded_spectrum_and_value_types(spectrum: Spectrum, object_tag: ObjectTag) -> None:
    assert_type(spectrum.data, str)
    assert_type(Spectrum.data, Field[str])
    assert_type(object_tag.value, int | float | str)
    assert_type(ObjectTag.value, Field[int | float | str])


def sdk_extension_types(
    bond: Bond,
    constraint: Constraint,
    curve: Curve,
    geometry: Geometry,
    graphic: Graphic,
    node: Node,
    plate: TLCPlate,
) -> None:
    assert_type(node.bgcolor, int | None)
    assert_type(bond.bgcolor, int | None)
    assert_type(graphic.bgcolor, int | None)
    assert_type(curve.bgcolor, int | None)
    assert_type(geometry.bond_length, float | None)
    assert_type(geometry.label_font, int | None)
    assert_type(geometry.label_size, float | None)
    assert_type(geometry.label_face, int | None)
    assert_type(geometry.label_color, int | None)
    assert_type(geometry.point_is_directed, bool | None)
    assert_type(constraint.bond_length, float | None)
    assert_type(constraint.label_size, float | None)
    assert_type(constraint.point_is_directed, bool)
    assert_type(plate.bgcolor, int | None)
