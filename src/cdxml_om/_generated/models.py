# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Statically generated classes for the canonical CDXML schema subset."""

from __future__ import annotations

from typing import ClassVar

from cdxml_om.core.fields import ChildCollection, Field, RefField, RefListField
from cdxml_om.core.geometry import BoundingBox, Point2D, Point3D
from cdxml_om.core.models import CDXMLElement
from cdxml_om.core.values import ElementList, GenericList

from .enums import (
    AminoAcidTermini,
    ArrowheadSide,
    ArrowheadType,
    ArrowType,
    BioShapeType,
    BondDisplay,
    BondOrder,
    BondStereochemistry,
    BracketType,
    BracketUsage,
    CaptionJustification,
    Connectivity,
    ConstraintType,
    DoublePosition,
    DrawingSpace,
    ExternalConnectionType,
    FillType,
    GeometricFeature,
    GraphicType,
    IsotopicAbundance,
    Justification,
    LabelJustification,
    LineType,
    NodeGeometry,
    NodeStereochemistry,
    NodeType,
    NoGo,
    OrbitalType,
    PageDefinition,
    PolymerFlipType,
    PolymerRepeatPattern,
    PositioningType,
    Radical,
    RingBondCount,
    RxnParticipation,
    RxnStereo,
    SequenceType,
    Side,
    SpectrumClass,
    SpectrumXType,
    SpectrumYType,
    SymbolType,
    TagType,
    Topology,
    Translation,
    UnsaturatedBonds,
)


class Color(CDXMLElement):
    __spec_id__: ClassVar[str] = "color"
    __slots__ = ()
    r: Field[float] = Field(property_id="color.r")
    b: Field[float] = Field(property_id="color.b")
    g: Field[float] = Field(property_id="color.g")


class ColorTable(CDXMLElement):
    __spec_id__: ClassVar[str] = "color_table"
    __slots__ = ()
    xml_id: Field[int | None] = Field(property_id="dtd.colortable.xml_id")
    colors: ChildCollection[Color] = ChildCollection(
        object_type="color",
        collection_name="colors",
    )


class Font(CDXMLElement):
    __spec_id__: ClassVar[str] = "font"
    __slots__ = ()
    charset: Field[str | None] = Field(property_id="font.charset")
    name: Field[str] = Field(property_id="font.name")
    id: Field[int] = Field(property_id="font.id")


class FontTable(CDXMLElement):
    __spec_id__: ClassVar[str] = "font_table"
    __slots__ = ()
    xml_id: Field[int | None] = Field(property_id="dtd.colortable.xml_id")
    fonts: ChildCollection[Font] = ChildCollection(
        object_type="font",
        collection_name="fonts",
    )


class TextRun(CDXMLElement):
    __spec_id__: ClassVar[str] = "text_run"
    __slots__ = ()
    alpha: Field[float | None] = Field(property_id="text_run.alpha")
    size: Field[float | None] = Field(property_id="text_run.size")
    font_id: Field[int | None] = Field(property_id="text_run.font_id")
    face: Field[int | None] = Field(property_id="text_run.face")
    color: Field[int | None] = Field(property_id="text_run.color")
    content: Field[str] = Field(property_id="text_run.content")


class ObjectTag(CDXMLElement):
    __spec_id__: ClassVar[str] = "object_tag"
    __slots__ = ()
    display_name: Field[str | None] = Field(property_id="dtd.objecttag.display_name")
    visible: Field[bool] = Field(property_id="common.visible")
    value: Field[int | float | str] = Field(property_id="dtd.objecttag.value")
    tracking: Field[bool] = Field(property_id="dtd.objecttag.tracking")
    tag_type: Field[TagType | None] = Field(property_id="dtd.objecttag.tag_type")
    positioning_type: Field[PositioningType] = Field(property_id="dtd.objecttag.positioning_type")
    positioning_offset: Field[Point2D | None] = Field(
        property_id="dtd.objecttag.positioning_offset"
    )
    positioning_angle: Field[int | None] = Field(property_id="dtd.objecttag.positioning_angle")
    persistent: Field[bool] = Field(property_id="dtd.objecttag.persistent")
    name: Field[str] = Field(property_id="dtd.objecttag.name")
    id: Field[int | None] = Field(property_id="common.id")
    texts: ChildCollection[Text] = ChildCollection(
        object_type="text",
        collection_name="texts",
    )


class Annotation(CDXMLElement):
    __spec_id__: ClassVar[str] = "annotation"
    __slots__ = ()
    content: Field[str | None] = Field(property_id="dtd.annotation.content")
    keyword: Field[str | None] = Field(property_id="dtd.annotation.keyword")
    id: Field[int | None] = Field(property_id="common.id")


class Text(CDXMLElement):
    __spec_id__: ClassVar[str] = "text"
    __slots__ = ()
    alpha: Field[str | None] = Field(property_id="dtd.CDXML.alpha")
    z: Field[int | None] = Field(property_id="dtd.page.z")
    word_wrap_width: Field[int | None] = Field(property_id="dtd.t.word_wrap_width")
    warning: Field[str | None] = Field(property_id="dtd.t.warning")
    visible: Field[bool] = Field(property_id="common.visible")
    superseded_by: RefField[CDXMLElement | None] = RefField(property_id="dtd.t.superseded_by")
    rotation_angle: Field[float | None] = Field(property_id="dtd.t.rotation_angle")
    position: Field[Point2D | None] = Field(property_id="node.position")
    line_height: Field[int | None] = Field(property_id="dtd.t.line_height")
    line_starts: Field[tuple[int, ...] | None] = Field(property_id="dtd.t.line_starts")
    label_size: Field[float | None] = Field(property_id="dtd.CDXML.label_size")
    label_line_height: Field[int | None] = Field(property_id="dtd.CDXML.label_line_height")
    label_justification: Field[LabelJustification] = Field(
        property_id="dtd.CDXML.label_justification"
    )
    label_font: Field[int | None] = Field(property_id="dtd.CDXML.label_font")
    label_face: Field[int | None] = Field(property_id="dtd.CDXML.label_face")
    label_color: Field[int | None] = Field(property_id="dtd.CDXML.label_color")
    label_alignment: Field[LabelJustification] = Field(property_id="dtd.t.label_alignment")
    justification: Field[Justification] = Field(property_id="dtd.t.justification")
    interpret_chemically: Field[bool] = Field(property_id="dtd.CDXML.interpret_chemically")
    ignore_warnings: Field[bool] = Field(property_id="text.ignore_warnings")
    id: Field[int | None] = Field(property_id="common.id")
    color: Field[int | None] = Field(property_id="text_run.color")
    caption_size: Field[float | None] = Field(property_id="dtd.CDXML.caption_size")
    caption_line_height: Field[int | None] = Field(property_id="dtd.CDXML.caption_line_height")
    caption_justification: Field[CaptionJustification] = Field(
        property_id="dtd.CDXML.caption_justification"
    )
    caption_font: Field[int | None] = Field(property_id="dtd.CDXML.caption_font")
    caption_face: Field[int | None] = Field(property_id="dtd.CDXML.caption_face")
    caption_color: Field[int | None] = Field(property_id="dtd.CDXML.caption_color")
    bounding_box: Field[BoundingBox | None] = Field(property_id="geometry.bounding_box")
    runs: ChildCollection[TextRun] = ChildCollection(
        object_type="text_run",
        collection_name="runs",
    )
    objecttags: ChildCollection[ObjectTag] = ChildCollection(
        object_type="object_tag",
        collection_name="objecttags",
    )
    annotations: ChildCollection[Annotation] = ChildCollection(
        object_type="annotation",
        collection_name="annotations",
    )


class Node(CDXMLElement):
    __spec_id__: ClassVar[str] = "node"
    __slots__ = ()
    abnormal_valence: Field[bool] = Field(property_id="dtd.n.abnormal_valence")
    z: Field[int | None] = Field(property_id="dtd.page.z")
    xyz: Field[Point3D | None] = Field(property_id="dtd.n.xyz")
    warning: Field[str | None] = Field(property_id="dtd.t.warning")
    visible: Field[bool] = Field(property_id="common.visible")
    unsaturated_bonds: Field[UnsaturatedBonds] = Field(property_id="dtd.n.unsaturated_bonds")
    translation: Field[Translation] = Field(property_id="dtd.n.translation")
    superseded_by: RefField[CDXMLElement | None] = RefField(property_id="dtd.t.superseded_by")
    substituents_up_to: Field[int | None] = Field(property_id="dtd.n.substituents_up_to")
    substituents_exactly: Field[int | None] = Field(property_id="dtd.n.substituents_exactly")
    show_terminal_carbon_labels: Field[bool] = Field(
        property_id="dtd.CDXML.show_terminal_carbon_labels"
    )
    show_non_terminal_carbon_labels: Field[bool] = Field(
        property_id="dtd.CDXML.show_non_terminal_carbon_labels"
    )
    show_atom_stereo: Field[bool] = Field(property_id="dtd.CDXML.show_atom_stereo")
    show_atom_query: Field[bool] = Field(property_id="dtd.CDXML.show_atom_query")
    show_atom_number: Field[bool] = Field(property_id="dtd.CDXML.show_atom_number")
    show_atom_id: Field[bool] = Field(property_id="dtd.n.show_atom_id")
    show_atom_enhanced_stereo: Field[bool] = Field(
        property_id="dtd.CDXML.show_atom_enhanced_stereo"
    )
    rxn_stereo: Field[RxnStereo] = Field(property_id="dtd.n.rxn_stereo")
    rxn_change: Field[bool] = Field(property_id="dtd.n.rxn_change")
    ring_bond_count: Field[RingBondCount] = Field(property_id="dtd.n.ring_bond_count")
    radical: Field[Radical] = Field(property_id="dtd.n.radical")
    position: Field[Point2D | None] = Field(property_id="node.position")
    node_type: Field[NodeType] = Field(property_id="dtd.n.node_type")
    num_hydrogens: Field[int | None] = Field(property_id="dtd.n.num_hydrogens")
    needs_clean: Field[bool] = Field(property_id="dtd.n.needs_clean")
    margin_width: Field[float | None] = Field(property_id="dtd.CDXML.margin_width")
    link_count_low: Field[int | None] = Field(property_id="dtd.n.link_count_low")
    link_count_high: Field[int | None] = Field(property_id="dtd.n.link_count_high")
    line_width: Field[float | None] = Field(property_id="dtd.CDXML.line_width")
    label_size: Field[float | None] = Field(property_id="dtd.CDXML.label_size")
    label_font: Field[int | None] = Field(property_id="dtd.CDXML.label_font")
    label_face: Field[int | None] = Field(property_id="dtd.CDXML.label_face")
    label_display: Field[LabelJustification] = Field(property_id="dtd.n.label_display")
    isotopic_abundance: Field[IsotopicAbundance] = Field(property_id="dtd.n.isotopic_abundance")
    isotope: Field[int] = Field(property_id="node.isotope")
    implicit_hydrogens: Field[bool] = Field(property_id="dtd.n.implicit_hydrogens")
    ignore_warnings: Field[bool] = Field(property_id="text.ignore_warnings")
    id: Field[int | None] = Field(property_id="common.id")
    hide_implicit_hydrogens: Field[bool] = Field(property_id="dtd.CDXML.hide_implicit_hydrogens")
    h_dot: Field[bool] = Field(property_id="dtd.n.h_dot")
    h_dash: Field[bool] = Field(property_id="dtd.n.h_dash")
    generic_nickname: Field[str | None] = Field(property_id="dtd.n.generic_nickname")
    generic_list: Field[GenericList | None] = Field(property_id="dtd.n.generic_list")
    geometry: Field[NodeGeometry] = Field(property_id="dtd.n.geometry")
    free_sites: Field[int | None] = Field(property_id="dtd.n.free_sites")
    formula: Field[str | None] = Field(property_id="dtd.n.formula")
    alpha: Field[str | None] = Field(property_id="dtd.CDXML.alpha")
    external_connection_num: Field[str | None] = Field(property_id="dtd.n.external_connection_num")
    external_connection_type: Field[ExternalConnectionType] = Field(
        property_id="dtd.n.external_connection_type"
    )
    enhanced_stereo_type: Field[int | None] = Field(property_id="dtd.n.enhanced_stereo_type")
    enhanced_stereo_group_num: Field[int | None] = Field(
        property_id="dtd.n.enhanced_stereo_group_num"
    )
    element_list: Field[ElementList | None] = Field(property_id="dtd.n.element_list")
    element: Field[int] = Field(property_id="node.element")
    color: Field[int | None] = Field(property_id="text_run.color")
    charge: Field[int] = Field(property_id="node.charge")
    bond_ordering: RefListField[CDXMLElement] = RefListField(property_id="dtd.n.bond_ordering")
    attachments: RefListField[Node] = RefListField(property_id="dtd.n.attachments")
    atom_number: Field[str | None] = Field(property_id="dtd.n.atom_number")
    atom_id: Field[str | None] = Field(property_id="dtd.n.atom_id")
    as_value: Field[NodeStereochemistry] = Field(property_id="dtd.n.as_value")
    alt_group_id: RefField[CDXMLElement | None] = RefField(property_id="dtd.n.alt_group_id")
    bgcolor: Field[int | None] = Field(property_id="dtd.CDXML.bgcolor")
    objecttags: ChildCollection[ObjectTag] = ChildCollection(
        object_type="object_tag",
        collection_name="objecttags",
    )
    annotations: ChildCollection[Annotation] = ChildCollection(
        object_type="annotation",
        collection_name="annotations",
    )
    texts: ChildCollection[Text] = ChildCollection(
        object_type="text",
        collection_name="texts",
    )
    fragments: ChildCollection[Fragment] = ChildCollection(
        object_type="fragment",
        collection_name="fragments",
    )


class Bond(CDXMLElement):
    __spec_id__: ClassVar[str] = "bond"
    __slots__ = ()
    alpha: Field[str | None] = Field(property_id="dtd.CDXML.alpha")
    z: Field[int | None] = Field(property_id="dtd.page.z")
    warning: Field[str | None] = Field(property_id="dtd.t.warning")
    visible: Field[bool] = Field(property_id="common.visible")
    topology: Field[Topology] = Field(property_id="dtd.b.topology")
    superseded_by: RefField[CDXMLElement | None] = RefField(property_id="dtd.t.superseded_by")
    show_bond_stereo: Field[bool] = Field(property_id="dtd.CDXML.show_bond_stereo")
    show_bond_rxn: Field[bool] = Field(property_id="dtd.CDXML.show_bond_rxn")
    show_bond_query: Field[bool] = Field(property_id="dtd.CDXML.show_bond_query")
    rxn_participation: Field[RxnParticipation] = Field(property_id="dtd.b.rxn_participation")
    order: Field[BondOrder] = Field(property_id="bond.order")
    margin_width: Field[float | None] = Field(property_id="dtd.CDXML.margin_width")
    line_width: Field[float | None] = Field(property_id="dtd.CDXML.line_width")
    label_size: Field[float | None] = Field(property_id="dtd.CDXML.label_size")
    label_font: Field[int | None] = Field(property_id="dtd.CDXML.label_font")
    label_face: Field[int | None] = Field(property_id="dtd.CDXML.label_face")
    ignore_warnings: Field[bool] = Field(property_id="text.ignore_warnings")
    id: Field[int | None] = Field(property_id="common.id")
    hash_spacing: Field[float | None] = Field(property_id="dtd.CDXML.hash_spacing")
    end_external_num: Field[str | None] = Field(property_id="dtd.b.end_external_num")
    end_attach: Field[int | None] = Field(property_id="dtd.b.end_attach")
    end: RefField[Node] = RefField(property_id="bond.end")
    double_position: Field[DoublePosition | None] = Field(property_id="dtd.b.double_position")
    display2: Field[BondDisplay] = Field(property_id="dtd.b.display2")
    display: Field[BondDisplay] = Field(property_id="bond.display")
    crossing_bondss: Field[str | None] = Field(property_id="dtd.b.crossing_bondss")
    crossing_bonds: RefListField[CDXMLElement] = RefListField(property_id="dtd.b.crossing_bonds")
    connectivity: Field[Connectivity] = Field(property_id="dtd.b.connectivity")
    color: Field[int | None] = Field(property_id="text_run.color")
    bs: Field[BondStereochemistry] = Field(property_id="dtd.b.bs")
    bond_spacing_abs: Field[float | None] = Field(property_id="dtd.CDXML.bond_spacing_abs")
    bond_spacing: Field[int | None] = Field(property_id="dtd.CDXML.bond_spacing")
    bond_length: Field[float | None] = Field(property_id="dtd.CDXML.bond_length")
    bond_circular_ordering: RefListField[CDXMLElement] = RefListField(
        property_id="dtd.b.bond_circular_ordering"
    )
    bold_width: Field[float | None] = Field(property_id="dtd.CDXML.bold_width")
    begin_external_num: Field[str | None] = Field(property_id="dtd.b.begin_external_num")
    begin_attach: Field[int | None] = Field(property_id="dtd.b.begin_attach")
    begin: RefField[Node] = RefField(property_id="bond.begin")
    bgcolor: Field[int | None] = Field(property_id="dtd.CDXML.bgcolor")
    objecttags: ChildCollection[ObjectTag] = ChildCollection(
        object_type="object_tag",
        collection_name="objecttags",
    )
    annotations: ChildCollection[Annotation] = ChildCollection(
        object_type="annotation",
        collection_name="annotations",
    )


class Represent(CDXMLElement):
    __spec_id__: ClassVar[str] = "represent"
    __slots__ = ()
    attribute_id: Field[int] = Field(property_id="dtd.represent.attribute_id")
    object_reference: RefField[CDXMLElement] = RefField(
        property_id="dtd.represent.object_reference"
    )


class Graphic(CDXMLElement):
    __spec_id__: ClassVar[str] = "graphic"
    __slots__ = ()
    alpha: Field[str | None] = Field(property_id="dtd.CDXML.alpha")
    z: Field[int | None] = Field(property_id="dtd.page.z")
    warning: Field[str | None] = Field(property_id="dtd.t.warning")
    visible: Field[bool] = Field(property_id="common.visible")
    tail_3d: Field[Point3D | None] = Field(property_id="arrow.tail_3d")
    symbol_type: Field[SymbolType | None] = Field(property_id="dtd.graphic.symbol_type")
    superseded_by: RefField[CDXMLElement | None] = RefField(property_id="dtd.t.superseded_by")
    rectangle_type: Field[int | None] = Field(property_id="dtd.graphic.rectangle_type")
    shadow_size: Field[str | None] = Field(property_id="dtd.graphic.shadow_size")
    polymer_repeat_pattern: Field[PolymerRepeatPattern | None] = Field(
        property_id="dtd.graphic.polymer_repeat_pattern"
    )
    polymer_flip_type: Field[PolymerFlipType | None] = Field(
        property_id="dtd.graphic.polymer_flip_type"
    )
    oval_type: Field[int | None] = Field(property_id="dtd.graphic.oval_type")
    orbital_type: Field[OrbitalType | None] = Field(property_id="dtd.graphic.orbital_type")
    minor_axis_end_3d: Field[Point3D | None] = Field(property_id="dtd.arrow.minor_axis_end3_d")
    major_axis_end_3d: Field[Point3D | None] = Field(property_id="dtd.arrow.major_axis_end3_d")
    lip_size: Field[int | None] = Field(property_id="dtd.graphic.lip_size")
    line_type: Field[LineType | None] = Field(property_id="dtd.graphic.line_type")
    line_width: Field[float | None] = Field(property_id="dtd.CDXML.line_width")
    ignore_warnings: Field[bool] = Field(property_id="text.ignore_warnings")
    id: Field[int | None] = Field(property_id="common.id")
    head_size: Field[float | None] = Field(property_id="arrow.head_size")
    head_3d: Field[Point3D | None] = Field(property_id="arrow.head_3d")
    hash_spacing: Field[float | None] = Field(property_id="dtd.CDXML.hash_spacing")
    graphic_type: Field[GraphicType] = Field(property_id="graphic.graphic_type")
    frame_type: Field[int | None] = Field(property_id="dtd.graphic.frame_type")
    fade_percent: Field[str | None] = Field(property_id="dtd.graphic.fade_percent")
    corner_radius: Field[int | None] = Field(property_id="dtd.graphic.corner_radius")
    color: Field[int | None] = Field(property_id="text_run.color")
    center_3d: Field[Point3D | None] = Field(property_id="dtd.plasmidregion.center3_d")
    caption_size: Field[float | None] = Field(property_id="dtd.CDXML.caption_size")
    caption_font: Field[int | None] = Field(property_id="dtd.CDXML.caption_font")
    caption_face: Field[int | None] = Field(property_id="dtd.CDXML.caption_face")
    bracket_usage: Field[BracketUsage | None] = Field(property_id="dtd.graphic.bracket_usage")
    bracket_type: Field[BracketType | None] = Field(property_id="dtd.graphic.bracket_type")
    bounding_box: Field[BoundingBox | None] = Field(property_id="geometry.bounding_box")
    bold_width: Field[float | None] = Field(property_id="dtd.CDXML.bold_width")
    arrow_type: Field[ArrowType | None] = Field(property_id="dtd.graphic.arrow_type")
    angular_size: Field[int | None] = Field(property_id="dtd.graphic.angular_size")
    bgcolor: Field[int | None] = Field(property_id="dtd.CDXML.bgcolor")
    objecttags: ChildCollection[ObjectTag] = ChildCollection(
        object_type="object_tag",
        collection_name="objecttags",
    )
    annotations: ChildCollection[Annotation] = ChildCollection(
        object_type="annotation",
        collection_name="annotations",
    )
    represents: ChildCollection[Represent] = ChildCollection(
        object_type="represent",
        collection_name="represents",
    )
    texts: ChildCollection[Text] = ChildCollection(
        object_type="text",
        collection_name="texts",
    )


class Curve(CDXMLElement):
    __spec_id__: ClassVar[str] = "curve"
    __slots__ = ()
    alpha: Field[str | None] = Field(property_id="dtd.CDXML.alpha")
    z: Field[int | None] = Field(property_id="dtd.page.z")
    warning: Field[str | None] = Field(property_id="dtd.t.warning")
    visible: Field[bool] = Field(property_id="common.visible")
    superseded_by: RefField[CDXMLElement | None] = RefField(property_id="dtd.t.superseded_by")
    line_width: Field[float | None] = Field(property_id="dtd.CDXML.line_width")
    line_type: Field[LineType | None] = Field(property_id="dtd.graphic.line_type")
    ignore_warnings: Field[bool] = Field(property_id="text.ignore_warnings")
    id: Field[int | None] = Field(property_id="common.id")
    head_width: Field[int | None] = Field(property_id="dtd.curve.head_width")
    head_size: Field[float | None] = Field(property_id="arrow.head_size")
    head_center_size: Field[int | None] = Field(property_id="dtd.curve.head_center_size")
    hash_spacing: Field[float | None] = Field(property_id="dtd.CDXML.hash_spacing")
    fill_type: Field[FillType | None] = Field(property_id="arrow.fill_type")
    fade_percent: Field[str | None] = Field(property_id="dtd.graphic.fade_percent")
    curve_type: Field[int | None] = Field(property_id="dtd.curve.curve_type")
    curve_spacing: Field[int | None] = Field(property_id="dtd.curve.curve_spacing")
    curve_points3_d: Field[tuple[Point3D, ...] | None] = Field(
        property_id="dtd.curve.curve_points3_d"
    )
    curve_points: Field[tuple[Point2D, ...] | None] = Field(property_id="dtd.curve.curve_points")
    closed: Field[bool] = Field(property_id="dtd.curve.closed")
    color: Field[int | None] = Field(property_id="text_run.color")
    bounding_box: Field[BoundingBox | None] = Field(property_id="geometry.bounding_box")
    bold_width: Field[float | None] = Field(property_id="dtd.CDXML.bold_width")
    arrowhead_type: Field[ArrowheadType | None] = Field(property_id="dtd.curve.arrowhead_type")
    arrowhead_tail: Field[ArrowheadSide | None] = Field(property_id="dtd.curve.arrowhead_tail")
    arrowhead_head: Field[ArrowheadSide | None] = Field(property_id="dtd.curve.arrowhead_head")
    bgcolor: Field[int | None] = Field(property_id="dtd.CDXML.bgcolor")
    objecttags: ChildCollection[ObjectTag] = ChildCollection(
        object_type="object_tag",
        collection_name="objecttags",
    )
    annotations: ChildCollection[Annotation] = ChildCollection(
        object_type="annotation",
        collection_name="annotations",
    )


class RegistryNumber(CDXMLElement):
    __spec_id__: ClassVar[str] = "registry_number"
    __slots__ = ()
    id: Field[int | None] = Field(property_id="common.id")
    registry_number: Field[str] = Field(property_id="dtd.regnum.registry_number")
    registry_authority: Field[str] = Field(property_id="dtd.regnum.registry_authority")


class ColoredMolecularArea(CDXMLElement):
    __spec_id__: ClassVar[str] = "colored_molecular_area"
    __slots__ = ()
    id: Field[int | None] = Field(property_id="common.id")
    basis_objects: RefListField[CDXMLElement] = RefListField(
        property_id="dtd.geometry.basis_objects"
    )
    bgcolor: Field[int | None] = Field(property_id="dtd.CDXML.bgcolor")


class Fragment(CDXMLElement):
    __spec_id__: ClassVar[str] = "fragment"
    __slots__ = ()
    absolute: Field[bool] = Field(property_id="dtd.fragment.absolute")
    z: Field[int | None] = Field(property_id="dtd.page.z")
    weight: Field[float | None] = Field(property_id="dtd.fragment.weight")
    sequence_type: Field[SequenceType] = Field(property_id="dtd.fragment.sequence_type")
    racemic: Field[bool] = Field(property_id="dtd.fragment.racemic")
    relative: Field[bool] = Field(property_id="dtd.fragment.relative")
    id: Field[int | None] = Field(property_id="common.id")
    formula: Field[str | None] = Field(property_id="dtd.fragment.formula")
    connection_order: RefListField[CDXMLElement] = RefListField(
        property_id="dtd.fragment.connection_order"
    )
    bounding_box: Field[BoundingBox | None] = Field(property_id="geometry.bounding_box")
    nodes: ChildCollection[Node] = ChildCollection(
        object_type="node",
        collection_name="nodes",
    )
    bonds: ChildCollection[Bond] = ChildCollection(
        object_type="bond",
        collection_name="bonds",
    )
    texts: ChildCollection[Text] = ChildCollection(
        object_type="text",
        collection_name="texts",
    )
    graphics: ChildCollection[Graphic] = ChildCollection(
        object_type="graphic",
        collection_name="graphics",
    )
    curves: ChildCollection[Curve] = ChildCollection(
        object_type="curve",
        collection_name="curves",
    )
    objecttags: ChildCollection[ObjectTag] = ChildCollection(
        object_type="object_tag",
        collection_name="objecttags",
    )
    annotations: ChildCollection[Annotation] = ChildCollection(
        object_type="annotation",
        collection_name="annotations",
    )
    regnums: ChildCollection[RegistryNumber] = ChildCollection(
        object_type="registry_number",
        collection_name="regnums",
    )
    coloredmolecularareas: ChildCollection[ColoredMolecularArea] = ChildCollection(
        object_type="colored_molecular_area",
        collection_name="coloredmolecularareas",
    )


class AltGroup(CDXMLElement):
    __spec_id__: ClassVar[str] = "alt_group"
    __slots__ = ()
    alpha: Field[str | None] = Field(property_id="dtd.CDXML.alpha")
    z: Field[int | None] = Field(property_id="dtd.page.z")
    warning: Field[str | None] = Field(property_id="dtd.t.warning")
    visible: Field[bool] = Field(property_id="common.visible")
    valence: Field[int | None] = Field(property_id="dtd.altgroup.valence")
    text_frame: Field[BoundingBox | None] = Field(property_id="dtd.altgroup.text_frame")
    superseded_by: RefField[CDXMLElement | None] = RefField(property_id="dtd.t.superseded_by")
    position: Field[Point2D | None] = Field(property_id="node.position")
    ignore_warnings: Field[bool] = Field(property_id="text.ignore_warnings")
    id: Field[int | None] = Field(property_id="common.id")
    group_frame: Field[BoundingBox | None] = Field(property_id="dtd.altgroup.group_frame")
    color: Field[int | None] = Field(property_id="text_run.color")
    bounding_box: Field[BoundingBox | None] = Field(property_id="geometry.bounding_box")
    bgcolor: Field[int | None] = Field(property_id="dtd.CDXML.bgcolor")
    objecttags: ChildCollection[ObjectTag] = ChildCollection(
        object_type="object_tag",
        collection_name="objecttags",
    )
    annotations: ChildCollection[Annotation] = ChildCollection(
        object_type="annotation",
        collection_name="annotations",
    )
    texts: ChildCollection[Text] = ChildCollection(
        object_type="text",
        collection_name="texts",
    )
    fragments: ChildCollection[Fragment] = ChildCollection(
        object_type="fragment",
        collection_name="fragments",
    )
    groups: ChildCollection[Group] = ChildCollection(
        object_type="group",
        collection_name="groups",
    )
    graphics: ChildCollection[Graphic] = ChildCollection(
        object_type="graphic",
        collection_name="graphics",
    )


class ReactionStep(CDXMLElement):
    __spec_id__: ClassVar[str] = "reaction_step"
    __slots__ = ()
    id: Field[int | None] = Field(property_id="common.id")
    reactants: RefListField[CDXMLElement] = RefListField(property_id="reaction_step.reactants")
    products: RefListField[CDXMLElement] = RefListField(property_id="reaction_step.products")
    reaction_step_plusses: RefListField[CDXMLElement] = RefListField(
        property_id="dtd.step.reaction_step_plusses"
    )
    reaction_step_objects_below_arrow: RefListField[CDXMLElement] = RefListField(
        property_id="dtd.step.reaction_step_objects_below_arrow"
    )
    reaction_step_objects_above_arrow: RefListField[CDXMLElement] = RefListField(
        property_id="dtd.step.reaction_step_objects_above_arrow"
    )
    reaction_step_atom_map_manual: RefListField[CDXMLElement] = RefListField(
        property_id="dtd.step.reaction_step_atom_map_manual"
    )
    reaction_step_atom_map_auto: RefListField[CDXMLElement] = RefListField(
        property_id="dtd.step.reaction_step_atom_map_auto"
    )
    reaction_step_atom_map: RefListField[CDXMLElement] = RefListField(
        property_id="dtd.step.reaction_step_atom_map"
    )
    arrows: RefListField[CDXMLElement] = RefListField(property_id="reaction_step.arrows")


class ReactionScheme(CDXMLElement):
    __spec_id__: ClassVar[str] = "reaction_scheme"
    __slots__ = ()
    id: Field[int | None] = Field(property_id="common.id")
    steps: ChildCollection[ReactionStep] = ChildCollection(
        object_type="reaction_step",
        collection_name="steps",
    )


class Spectrum(CDXMLElement):
    __spec_id__: ClassVar[str] = "spectrum"
    __slots__ = ()
    alpha: Field[str | None] = Field(property_id="dtd.CDXML.alpha")
    z: Field[int | None] = Field(property_id="dtd.page.z")
    warning: Field[str | None] = Field(property_id="dtd.t.warning")
    visible: Field[bool] = Field(property_id="common.visible")
    y_type: Field[SpectrumYType] = Field(property_id="dtd.spectrum.y_type")
    y_scale: Field[float] = Field(property_id="dtd.spectrum.y_scale")
    y_low: Field[float] = Field(property_id="dtd.spectrum.y_low")
    y_axis_label: Field[str | None] = Field(property_id="dtd.spectrum.y_axis_label")
    x_type: Field[SpectrumXType] = Field(property_id="dtd.spectrum.x_type")
    x_spacing: Field[float | None] = Field(property_id="dtd.spectrum.x_spacing")
    x_low: Field[float | None] = Field(property_id="dtd.spectrum.x_low")
    x_axis_label: Field[str | None] = Field(property_id="dtd.spectrum.x_axis_label")
    superseded_by: RefField[CDXMLElement | None] = RefField(property_id="dtd.t.superseded_by")
    line_width: Field[float | None] = Field(property_id="dtd.CDXML.line_width")
    label_size: Field[float | None] = Field(property_id="dtd.CDXML.label_size")
    label_font: Field[int | None] = Field(property_id="dtd.CDXML.label_font")
    label_face: Field[int | None] = Field(property_id="dtd.CDXML.label_face")
    ignore_warnings: Field[bool] = Field(property_id="text.ignore_warnings")
    id: Field[int | None] = Field(property_id="common.id")
    color: Field[int | None] = Field(property_id="text_run.color")
    class_name: Field[SpectrumClass] = Field(property_id="dtd.spectrum.class_name")
    bounding_box: Field[BoundingBox | None] = Field(property_id="geometry.bounding_box")
    bold_width: Field[float | None] = Field(property_id="dtd.CDXML.bold_width")
    data: Field[str] = Field(property_id="spectrum.data")
    bgcolor: Field[int | None] = Field(property_id="dtd.CDXML.bgcolor")
    objecttags: ChildCollection[ObjectTag] = ChildCollection(
        object_type="object_tag",
        collection_name="objecttags",
    )
    annotations: ChildCollection[Annotation] = ChildCollection(
        object_type="annotation",
        collection_name="annotations",
    )


class PlasmidMarker(CDXMLElement):
    __spec_id__: ClassVar[str] = "plasmid_marker"
    __slots__ = ()
    caption_justification: Field[CaptionJustification] = Field(
        property_id="dtd.CDXML.caption_justification"
    )
    value: Field[int | float | str] = Field(property_id="dtd.objecttag.value")
    tag_type: Field[TagType | None] = Field(property_id="dtd.objecttag.tag_type")
    persistent: Field[bool] = Field(property_id="dtd.objecttag.persistent")
    name: Field[str] = Field(property_id="dtd.objecttag.name")
    marker_offset: Field[str | None] = Field(property_id="dtd.marker.marker_offset")
    marker_angle: Field[str | None] = Field(property_id="dtd.marker.marker_angle")
    id: Field[int | None] = Field(property_id="common.id")
    display_name: Field[str | None] = Field(property_id="dtd.objecttag.display_name")
    color: Field[int | None] = Field(property_id="text_run.color")
    objecttags: ChildCollection[ObjectTag] = ChildCollection(
        object_type="object_tag",
        collection_name="objecttags",
    )
    annotations: ChildCollection[Annotation] = ChildCollection(
        object_type="annotation",
        collection_name="annotations",
    )
    texts: ChildCollection[Text] = ChildCollection(
        object_type="text",
        collection_name="texts",
    )
    curves: ChildCollection[Curve] = ChildCollection(
        object_type="curve",
        collection_name="curves",
    )


class PlasmidRegion(CDXMLElement):
    __spec_id__: ClassVar[str] = "plasmid_region"
    __slots__ = ()
    alpha: Field[str | None] = Field(property_id="dtd.CDXML.alpha")
    z: Field[int | None] = Field(property_id="dtd.page.z")
    tail_3d: Field[Point3D | None] = Field(property_id="arrow.tail_3d")
    region_start: Field[str | None] = Field(property_id="dtd.plasmidregion.region_start")
    region_offset: Field[str | None] = Field(property_id="dtd.plasmidregion.region_offset")
    region_end: Field[str | None] = Field(property_id="dtd.plasmidregion.region_end")
    minor_axis_end_3d: Field[Point3D | None] = Field(property_id="dtd.arrow.minor_axis_end3_d")
    major_axis_end_3d: Field[Point3D | None] = Field(property_id="dtd.arrow.major_axis_end3_d")
    line_type: Field[LineType | None] = Field(property_id="dtd.graphic.line_type")
    id: Field[int | None] = Field(property_id="common.id")
    head_size: Field[float | None] = Field(property_id="arrow.head_size")
    head_3d: Field[Point3D | None] = Field(property_id="arrow.head_3d")
    fill_type: Field[FillType | None] = Field(property_id="arrow.fill_type")
    fade_percent: Field[str | None] = Field(property_id="dtd.graphic.fade_percent")
    color: Field[int | None] = Field(property_id="text_run.color")
    center_3d: Field[Point3D | None] = Field(property_id="dtd.plasmidregion.center3_d")
    bounding_box: Field[BoundingBox | None] = Field(property_id="geometry.bounding_box")
    arrow_shaft_spacing: Field[str | None] = Field(property_id="dtd.arrow.arrow_shaft_spacing")
    arrowhead_width: Field[str | None] = Field(property_id="dtd.plasmidregion.arrowhead_width")
    arrowhead_type: Field[ArrowheadType | None] = Field(property_id="arrow.arrowhead_type")
    arrowhead_tail: Field[ArrowheadSide | None] = Field(property_id="arrow.arrowhead_tail")
    arrowhead_head: Field[ArrowheadSide | None] = Field(property_id="arrow.arrowhead_head")
    arrowhead_center_size: Field[str | None] = Field(property_id="dtd.arrow.arrowhead_center_size")
    angular_size: Field[int | None] = Field(property_id="dtd.graphic.angular_size")
    objecttags: ChildCollection[ObjectTag] = ChildCollection(
        object_type="object_tag",
        collection_name="objecttags",
    )
    annotations: ChildCollection[Annotation] = ChildCollection(
        object_type="annotation",
        collection_name="annotations",
    )
    plasmidmarkers: ChildCollection[PlasmidMarker] = ChildCollection(
        object_type="plasmid_marker",
        collection_name="plasmidmarkers",
    )


class PlasmidMap(CDXMLElement):
    __spec_id__: ClassVar[str] = "plasmid_map"
    __slots__ = ()
    alpha: Field[str | None] = Field(property_id="dtd.CDXML.alpha")
    z: Field[int | None] = Field(property_id="dtd.page.z")
    visible: Field[bool] = Field(property_id="common.visible")
    superseded_by: RefField[CDXMLElement | None] = RefField(property_id="dtd.t.superseded_by")
    ring_radius: Field[str | None] = Field(property_id="dtd.plasmidmap.ring_radius")
    position: Field[Point2D | None] = Field(property_id="node.position")
    number_base_pairs: Field[str | None] = Field(property_id="dtd.plasmidmap.number_base_pairs")
    margin_width: Field[float | None] = Field(property_id="dtd.CDXML.margin_width")
    line_width: Field[float | None] = Field(property_id="dtd.CDXML.line_width")
    label_size: Field[float | None] = Field(property_id="dtd.CDXML.label_size")
    label_font: Field[int | None] = Field(property_id="dtd.CDXML.label_font")
    label_face: Field[int | None] = Field(property_id="dtd.CDXML.label_face")
    id: Field[int | None] = Field(property_id="common.id")
    color: Field[int | None] = Field(property_id="text_run.color")
    bounding_box: Field[BoundingBox | None] = Field(property_id="geometry.bounding_box")
    bold_width: Field[float | None] = Field(property_id="dtd.CDXML.bold_width")
    objecttags: ChildCollection[ObjectTag] = ChildCollection(
        object_type="object_tag",
        collection_name="objecttags",
    )
    annotations: ChildCollection[Annotation] = ChildCollection(
        object_type="annotation",
        collection_name="annotations",
    )
    plasmidregions: ChildCollection[PlasmidRegion] = ChildCollection(
        object_type="plasmid_region",
        collection_name="plasmidregions",
    )
    plasmidmarkers: ChildCollection[PlasmidMarker] = ChildCollection(
        object_type="plasmid_marker",
        collection_name="plasmidmarkers",
    )
    texts: ChildCollection[Text] = ChildCollection(
        object_type="text",
        collection_name="texts",
    )
    graphics: ChildCollection[Graphic] = ChildCollection(
        object_type="graphic",
        collection_name="graphics",
    )


class RLogicItem(CDXMLElement):
    __spec_id__: ClassVar[str] = "rlogic_item"
    __slots__ = ()
    id: Field[int | None] = Field(property_id="common.id")
    r_logic_rest_h: Field[bool] = Field(property_id="dtd.rlogicitem.r_logic_rest_h")
    r_logic_occurrence: Field[str | None] = Field(property_id="dtd.rlogicitem.r_logic_occurrence")
    r_logic_if_then_group: Field[str | None] = Field(
        property_id="dtd.rlogicitem.r_logic_if_then_group"
    )
    r_logic_group: Field[str | None] = Field(property_id="dtd.rlogicitem.r_logic_group")


class RLogic(CDXMLElement):
    __spec_id__: ClassVar[str] = "rlogic"
    __slots__ = ()
    alpha: Field[str | None] = Field(property_id="dtd.CDXML.alpha")
    z: Field[int | None] = Field(property_id="dtd.page.z")
    position: Field[Point2D | None] = Field(property_id="node.position")
    line_height: Field[int | None] = Field(property_id="dtd.t.line_height")
    id: Field[int | None] = Field(property_id="common.id")
    color: Field[int | None] = Field(property_id="text_run.color")
    bounding_box: Field[BoundingBox | None] = Field(property_id="geometry.bounding_box")
    runs: ChildCollection[TextRun] = ChildCollection(
        object_type="text_run",
        collection_name="runs",
    )
    rlogicitems: ChildCollection[RLogicItem] = ChildCollection(
        object_type="rlogic_item",
        collection_name="rlogicitems",
    )


class Arrow(CDXMLElement):
    __spec_id__: ClassVar[str] = "arrow"
    __slots__ = ()
    alpha: Field[str | None] = Field(property_id="dtd.CDXML.alpha")
    z: Field[int | None] = Field(property_id="dtd.page.z")
    warning: Field[str | None] = Field(property_id="dtd.t.warning")
    visible: Field[bool] = Field(property_id="common.visible")
    tail_3d: Field[Point3D | None] = Field(property_id="arrow.tail_3d")
    superseded_by: RefField[CDXMLElement | None] = RefField(property_id="dtd.t.superseded_by")
    no_go: Field[NoGo | None] = Field(property_id="dtd.arrow.no_go")
    minor_axis_end_3d: Field[Point3D | None] = Field(property_id="dtd.arrow.minor_axis_end3_d")
    major_axis_end_3d: Field[Point3D | None] = Field(property_id="dtd.arrow.major_axis_end3_d")
    line_width: Field[float | None] = Field(property_id="dtd.CDXML.line_width")
    line_type: Field[LineType | None] = Field(property_id="dtd.graphic.line_type")
    ignore_warnings: Field[bool] = Field(property_id="text.ignore_warnings")
    id: Field[int | None] = Field(property_id="common.id")
    head_size: Field[float | None] = Field(property_id="arrow.head_size")
    head_3d: Field[Point3D | None] = Field(property_id="arrow.head_3d")
    hash_spacing: Field[float | None] = Field(property_id="dtd.CDXML.hash_spacing")
    fill_type: Field[FillType | None] = Field(property_id="arrow.fill_type")
    fade_percent: Field[str | None] = Field(property_id="dtd.graphic.fade_percent")
    dipole: Field[bool] = Field(property_id="dtd.arrow.dipole")
    color: Field[int | None] = Field(property_id="text_run.color")
    center_3d: Field[Point3D | None] = Field(property_id="dtd.plasmidregion.center3_d")
    caption_size: Field[float | None] = Field(property_id="dtd.CDXML.caption_size")
    caption_font: Field[int | None] = Field(property_id="dtd.CDXML.caption_font")
    caption_face: Field[int | None] = Field(property_id="dtd.CDXML.caption_face")
    bounding_box: Field[BoundingBox | None] = Field(property_id="geometry.bounding_box")
    bold_width: Field[float | None] = Field(property_id="dtd.CDXML.bold_width")
    arrow_target: Field[str | None] = Field(property_id="dtd.arrow.arrow_target")
    arrow_source: Field[str | None] = Field(property_id="dtd.arrow.arrow_source")
    arrow_shaft_spacing: Field[str | None] = Field(property_id="dtd.arrow.arrow_shaft_spacing")
    arrowhead_type: Field[ArrowheadType | None] = Field(property_id="arrow.arrowhead_type")
    arrowhead_tail: Field[ArrowheadSide | None] = Field(property_id="arrow.arrowhead_tail")
    arrowhead_width: Field[str | None] = Field(property_id="dtd.plasmidregion.arrowhead_width")
    arrowhead_head: Field[ArrowheadSide | None] = Field(property_id="arrow.arrowhead_head")
    arrowhead_center_size: Field[str | None] = Field(property_id="dtd.arrow.arrowhead_center_size")
    arrow_equilibrium_ratio: Field[str | None] = Field(
        property_id="dtd.arrow.arrow_equilibrium_ratio"
    )
    angular_size: Field[int | None] = Field(property_id="dtd.graphic.angular_size")
    objecttags: ChildCollection[ObjectTag] = ChildCollection(
        object_type="object_tag",
        collection_name="objecttags",
    )
    annotations: ChildCollection[Annotation] = ChildCollection(
        object_type="annotation",
        collection_name="annotations",
    )


class BioShape(CDXMLElement):
    __spec_id__: ClassVar[str] = "bio_shape"
    __slots__ = ()
    alpha: Field[str | None] = Field(property_id="dtd.CDXML.alpha")
    z: Field[int | None] = Field(property_id="dtd.page.z")
    xyz: Field[Point3D | None] = Field(property_id="dtd.n.xyz")
    visible: Field[bool] = Field(property_id="common.visible")
    superseded_by: RefField[CDXMLElement | None] = RefField(property_id="dtd.t.superseded_by")
    pipe_width: Field[str | None] = Field(property_id="dtd.bioshape.pipe_width")
    neck_width: Field[str | None] = Field(property_id="dtd.bioshape.neck_width")
    neck_height: Field[str | None] = Field(property_id="dtd.bioshape.neck_height")
    minor_axis_end_3d: Field[Point3D | None] = Field(property_id="dtd.arrow.minor_axis_end3_d")
    membrane_start_angle: Field[str | None] = Field(property_id="dtd.bioshape.membrane_start_angle")
    membrane_minor_axis_size: Field[str | None] = Field(
        property_id="dtd.bioshape.membrane_minor_axis_size"
    )
    membrane_major_axis_size: Field[str | None] = Field(
        property_id="dtd.bioshape.membrane_major_axis_size"
    )
    membrane_end_angle: Field[str | None] = Field(property_id="dtd.bioshape.membrane_end_angle")
    membrane_element_size: Field[str | None] = Field(
        property_id="dtd.bioshape.membrane_element_size"
    )
    major_axis_end_3d: Field[Point3D | None] = Field(property_id="dtd.arrow.major_axis_end3_d")
    line_width: Field[float | None] = Field(property_id="dtd.CDXML.line_width")
    line_type: Field[LineType | None] = Field(property_id="dtd.graphic.line_type")
    immunoglobin_width: Field[str | None] = Field(property_id="dtd.bioshape.immunoglobin_width")
    immunoglobin_height: Field[str | None] = Field(property_id="dtd.bioshape.immunoglobin_height")
    id: Field[int | None] = Field(property_id="common.id")
    helix_protein_extra: Field[str | None] = Field(property_id="dtd.bioshape.helix_protein_extra")
    hash_spacing: Field[float | None] = Field(property_id="dtd.CDXML.hash_spacing")
    golgi_width: Field[str | None] = Field(property_id="dtd.bioshape.golgi_width")
    golgi_length: Field[str | None] = Field(property_id="dtd.bioshape.golgi_length")
    golgi_height: Field[str | None] = Field(property_id="dtd.bioshape.golgi_height")
    gprotein_upper_height: Field[str | None] = Field(
        property_id="dtd.bioshape.gprotein_upper_height"
    )
    gprotein_lower_height: Field[str | None] = Field(
        property_id="dtd.bioshape.gprotein_lower_height"
    )
    fill_type: Field[FillType | None] = Field(property_id="arrow.fill_type")
    fade_percent: Field[str | None] = Field(property_id="dtd.graphic.fade_percent")
    enzyme_width: Field[str | None] = Field(property_id="dtd.bioshape.enzyme_width")
    enzyme_receptor_size: Field[str | None] = Field(property_id="dtd.bioshape.enzyme_receptor_size")
    enzyme_height: Field[str | None] = Field(property_id="dtd.bioshape.enzyme_height")
    dna_wave_width: Field[str | None] = Field(property_id="dtd.bioshape.dna_wave_width")
    dna_wave_offset: Field[str | None] = Field(property_id="dtd.bioshape.dna_wave_offset")
    dna_wave_length: Field[str | None] = Field(property_id="dtd.bioshape.dna_wave_length")
    dna_wave_height: Field[str | None] = Field(property_id="dtd.bioshape.dna_wave_height")
    cylinder_width: Field[str | None] = Field(property_id="dtd.bioshape.cylinder_width")
    cylinder_height: Field[str | None] = Field(property_id="dtd.bioshape.cylinder_height")
    cylinder_distance: Field[str | None] = Field(property_id="dtd.bioshape.cylinder_distance")
    color: Field[int | None] = Field(property_id="text_run.color")
    bounding_box: Field[BoundingBox | None] = Field(property_id="geometry.bounding_box")
    bold_width: Field[float | None] = Field(property_id="dtd.CDXML.bold_width")
    bio_shape_type: Field[BioShapeType | None] = Field(property_id="dtd.bioshape.bio_shape_type")
    objecttags: ChildCollection[ObjectTag] = ChildCollection(
        object_type="object_tag",
        collection_name="objecttags",
    )
    annotations: ChildCollection[Annotation] = ChildCollection(
        object_type="annotation",
        collection_name="annotations",
    )
    curves: ChildCollection[Curve] = ChildCollection(
        object_type="curve",
        collection_name="curves",
    )


class Group(CDXMLElement):
    __spec_id__: ClassVar[str] = "group"
    __slots__ = ()
    bounding_box: Field[BoundingBox | None] = Field(property_id="geometry.bounding_box")
    z: Field[int | None] = Field(property_id="dtd.page.z")
    integral: Field[bool] = Field(property_id="group.integral")
    id: Field[int | None] = Field(property_id="common.id")
    texts: ChildCollection[Text] = ChildCollection(
        object_type="text",
        collection_name="texts",
    )
    fragments: ChildCollection[Fragment] = ChildCollection(
        object_type="fragment",
        collection_name="fragments",
    )
    groups: ChildCollection[Group] = ChildCollection(
        object_type="group",
        collection_name="groups",
    )
    graphics: ChildCollection[Graphic] = ChildCollection(
        object_type="graphic",
        collection_name="graphics",
    )
    altgroups: ChildCollection[AltGroup] = ChildCollection(
        object_type="alt_group",
        collection_name="altgroups",
    )
    curves: ChildCollection[Curve] = ChildCollection(
        object_type="curve",
        collection_name="curves",
    )
    steps: ChildCollection[ReactionStep] = ChildCollection(
        object_type="reaction_step",
        collection_name="steps",
    )
    schemes: ChildCollection[ReactionScheme] = ChildCollection(
        object_type="reaction_scheme",
        collection_name="schemes",
    )
    spectrums: ChildCollection[Spectrum] = ChildCollection(
        object_type="spectrum",
        collection_name="spectrums",
    )
    objecttags: ChildCollection[ObjectTag] = ChildCollection(
        object_type="object_tag",
        collection_name="objecttags",
    )
    annotations: ChildCollection[Annotation] = ChildCollection(
        object_type="annotation",
        collection_name="annotations",
    )
    plasmidmaps: ChildCollection[PlasmidMap] = ChildCollection(
        object_type="plasmid_map",
        collection_name="plasmidmaps",
    )
    rlogics: ChildCollection[RLogic] = ChildCollection(
        object_type="rlogic",
        collection_name="rlogics",
    )
    arrows: ChildCollection[Arrow] = ChildCollection(
        object_type="arrow",
        collection_name="arrows",
    )
    bioshapes: ChildCollection[BioShape] = ChildCollection(
        object_type="bio_shape",
        collection_name="bioshapes",
    )


class EmbeddedObject(CDXMLElement):
    __spec_id__: ClassVar[str] = "embedded_object"
    __slots__ = ()
    alpha: Field[str | None] = Field(property_id="dtd.CDXML.alpha")
    z: Field[int | None] = Field(property_id="dtd.page.z")
    windows_metafile: Field[str | None] = Field(property_id="dtd.embeddedobject.windows_metafile")
    uncompressed_windows_metafile_size: Field[str | None] = Field(
        property_id="dtd.embeddedobject.uncompressed_windows_metafile_size"
    )
    uncompressed_ole_object_size: Field[str | None] = Field(
        property_id="dtd.embeddedobject.uncompressed_ole_object_size"
    )
    uncompressed_enhanced_metafile_size: Field[str | None] = Field(
        property_id="dtd.embeddedobject.uncompressed_enhanced_metafile_size"
    )
    tiff: Field[str | None] = Field(property_id="dtd.embeddedobject.tiff")
    superseded_by: RefField[CDXMLElement | None] = RefField(property_id="dtd.t.superseded_by")
    rotation_angle: Field[float | None] = Field(property_id="dtd.t.rotation_angle")
    png: Field[str | None] = Field(property_id="dtd.embeddedobject.png")
    pdf: Field[str | None] = Field(property_id="dtd.embeddedobject.pdf")
    ole_object: Field[str | None] = Field(property_id="dtd.embeddedobject.ole_object")
    mac_pict: Field[str | None] = Field(property_id="dtd.embeddedobject.mac_pict")
    jpeg: Field[str | None] = Field(property_id="dtd.embeddedobject.jpeg")
    id: Field[int | None] = Field(property_id="common.id")
    gif: Field[str | None] = Field(property_id="dtd.embeddedobject.gif")
    enhanced_metafile: Field[str | None] = Field(property_id="dtd.embeddedobject.enhanced_metafile")
    edition_alias: Field[str | None] = Field(property_id="dtd.embeddedobject.edition_alias")
    edition: Field[str | None] = Field(property_id="dtd.embeddedobject.edition")
    compressed_windows_metafile: Field[str | None] = Field(
        property_id="dtd.embeddedobject.compressed_windows_metafile"
    )
    compressed_ole_object: Field[str | None] = Field(
        property_id="dtd.embeddedobject.compressed_ole_object"
    )
    compressed_enhanced_metafile: Field[str | None] = Field(
        property_id="dtd.embeddedobject.compressed_enhanced_metafile"
    )
    color: Field[int | None] = Field(property_id="text_run.color")
    bounding_box: Field[BoundingBox | None] = Field(property_id="geometry.bounding_box")
    bmp: Field[str | None] = Field(property_id="dtd.embeddedobject.bmp")
    bgcolor: Field[int | None] = Field(property_id="dtd.CDXML.bgcolor")
    objecttags: ChildCollection[ObjectTag] = ChildCollection(
        object_type="object_tag",
        collection_name="objecttags",
    )
    annotations: ChildCollection[Annotation] = ChildCollection(
        object_type="annotation",
        collection_name="annotations",
    )


class Sequence(CDXMLElement):
    __spec_id__: ClassVar[str] = "sequence"
    __slots__ = ()
    sequence_identifier: Field[str] = Field(property_id="dtd.sequence.sequence_identifier")
    texts: ChildCollection[Text] = ChildCollection(
        object_type="text",
        collection_name="texts",
    )


class CrossReference(CDXMLElement):
    __spec_id__: ClassVar[str] = "cross_reference"
    __slots__ = ()
    cross_reference_container: Field[str | None] = Field(
        property_id="dtd.crossreference.cross_reference_container"
    )
    cross_reference_sequence: Field[str] = Field(
        property_id="dtd.crossreference.cross_reference_sequence"
    )
    cross_reference_identifier: Field[str] = Field(
        property_id="dtd.crossreference.cross_reference_identifier"
    )
    cross_reference_document: Field[str | None] = Field(
        property_id="dtd.crossreference.cross_reference_document"
    )
    texts: ChildCollection[Text] = ChildCollection(
        object_type="text",
        collection_name="texts",
    )


class Splitter(CDXMLElement):
    __spec_id__: ClassVar[str] = "splitter"
    __slots__ = ()
    position: Field[Point2D | None] = Field(property_id="node.position")
    page_definition: Field[PageDefinition] = Field(property_id="dtd.page.page_definition")


class Table(CDXMLElement):
    __spec_id__: ClassVar[str] = "table"
    __slots__ = ()
    alpha: Field[str | None] = Field(property_id="dtd.CDXML.alpha")
    z: Field[int | None] = Field(property_id="dtd.page.z")
    visible: Field[bool] = Field(property_id="common.visible")
    superseded_by: RefField[CDXMLElement | None] = RefField(property_id="dtd.t.superseded_by")
    margin_width: Field[float | None] = Field(property_id="dtd.CDXML.margin_width")
    line_width: Field[float | None] = Field(property_id="dtd.CDXML.line_width")
    label_size: Field[float | None] = Field(property_id="dtd.CDXML.label_size")
    label_font: Field[int | None] = Field(property_id="dtd.CDXML.label_font")
    label_face: Field[int | None] = Field(property_id="dtd.CDXML.label_face")
    id: Field[int | None] = Field(property_id="common.id")
    color: Field[int | None] = Field(property_id="text_run.color")
    bounding_box: Field[BoundingBox | None] = Field(property_id="geometry.bounding_box")
    bold_width: Field[float | None] = Field(property_id="dtd.CDXML.bold_width")
    bgcolor: Field[int | None] = Field(property_id="dtd.CDXML.bgcolor")
    pages: ChildCollection[Page] = ChildCollection(
        object_type="page",
        collection_name="pages",
    )
    objecttags: ChildCollection[ObjectTag] = ChildCollection(
        object_type="object_tag",
        collection_name="objecttags",
    )
    annotations: ChildCollection[Annotation] = ChildCollection(
        object_type="annotation",
        collection_name="annotations",
    )


class CrossingBond(CDXMLElement):
    __spec_id__: ClassVar[str] = "crossing_bond"
    __slots__ = ()
    bond_id: RefField[Bond] = RefField(property_id="dtd.crossingbond.bond_id")
    inner_atom_id: RefField[Node] = RefField(property_id="dtd.crossingbond.inner_atom_id")
    id: Field[int | None] = Field(property_id="common.id")


class BracketAttachment(CDXMLElement):
    __spec_id__: ClassVar[str] = "bracket_attachment"
    __slots__ = ()
    graphic_id: RefField[CDXMLElement | None] = RefField(
        property_id="dtd.bracketattachment.graphic_id"
    )
    id: Field[int | None] = Field(property_id="common.id")
    crossingbonds: ChildCollection[CrossingBond] = ChildCollection(
        object_type="crossing_bond",
        collection_name="crossingbonds",
    )


class BracketedGroup(CDXMLElement):
    __spec_id__: ClassVar[str] = "bracketed_group"
    __slots__ = ()
    bracketed_object_i_ds: RefListField[CDXMLElement] = RefListField(
        property_id="dtd.bracketedgroup.bracketed_object_i_ds"
    )
    sru_label: Field[str | None] = Field(property_id="dtd.bracketedgroup.sru_label")
    repeat_count: Field[float | None] = Field(property_id="dtd.bracketedgroup.repeat_count")
    polymer_repeat_pattern: Field[PolymerRepeatPattern | None] = Field(
        property_id="dtd.graphic.polymer_repeat_pattern"
    )
    polymer_flip_type: Field[PolymerFlipType | None] = Field(
        property_id="dtd.graphic.polymer_flip_type"
    )
    id: Field[int | None] = Field(property_id="common.id")
    component_order: Field[int | None] = Field(property_id="dtd.bracketedgroup.component_order")
    bracket_usage: Field[BracketUsage | None] = Field(property_id="dtd.graphic.bracket_usage")
    bracketattachments: ChildCollection[BracketAttachment] = ChildCollection(
        object_type="bracket_attachment",
        collection_name="bracketattachments",
    )
    bracketedgroups: ChildCollection[BracketedGroup] = ChildCollection(
        object_type="bracketed_group",
        collection_name="bracketedgroups",
    )


class Border(CDXMLElement):
    __spec_id__: ClassVar[str] = "border"
    __slots__ = ()
    alpha: Field[str | None] = Field(property_id="dtd.CDXML.alpha")
    z: Field[int | None] = Field(property_id="dtd.page.z")
    side: Field[Side] = Field(property_id="dtd.border.side")
    line_width: Field[float | None] = Field(property_id="dtd.CDXML.line_width")
    line_type: Field[LineType | None] = Field(property_id="dtd.graphic.line_type")
    id: Field[int | None] = Field(property_id="common.id")
    color: Field[int | None] = Field(property_id="text_run.color")


class Geometry(CDXMLElement):
    __spec_id__: ClassVar[str] = "geometry"
    __slots__ = ()
    alpha: Field[str | None] = Field(property_id="dtd.CDXML.alpha")
    z: Field[int | None] = Field(property_id="dtd.page.z")
    superseded_by: RefField[CDXMLElement | None] = RefField(property_id="dtd.t.superseded_by")
    relation_value: Field[float | None] = Field(property_id="dtd.geometry.relation_value")
    name: Field[str | None] = Field(property_id="dtd.CDXML.name")
    line_width: Field[float | None] = Field(property_id="dtd.CDXML.line_width")
    id: Field[int | None] = Field(property_id="common.id")
    geometric_feature: Field[GeometricFeature] = Field(property_id="dtd.geometry.geometric_feature")
    color: Field[int | None] = Field(property_id="text_run.color")
    bounding_box: Field[BoundingBox | None] = Field(property_id="geometry.bounding_box")
    basis_objects: RefListField[CDXMLElement] = RefListField(
        property_id="dtd.geometry.basis_objects"
    )
    label_size: Field[float | None] = Field(property_id="dtd.CDXML.label_size")
    label_font: Field[int | None] = Field(property_id="dtd.CDXML.label_font")
    label_face: Field[int | None] = Field(property_id="dtd.CDXML.label_face")
    label_color: Field[int | None] = Field(property_id="dtd.CDXML.label_color")
    bond_length: Field[float | None] = Field(property_id="dtd.CDXML.bond_length")
    point_is_directed: Field[bool | None] = Field(property_id="sdk.geometry.point_is_directed")
    objecttags: ChildCollection[ObjectTag] = ChildCollection(
        object_type="object_tag",
        collection_name="objecttags",
    )
    annotations: ChildCollection[Annotation] = ChildCollection(
        object_type="annotation",
        collection_name="annotations",
    )


class Constraint(CDXMLElement):
    __spec_id__: ClassVar[str] = "constraint"
    __slots__ = ()
    alpha: Field[str | None] = Field(property_id="dtd.CDXML.alpha")
    z: Field[int | None] = Field(property_id="dtd.page.z")
    superseded_by: RefField[CDXMLElement | None] = RefField(property_id="dtd.t.superseded_by")
    point_is_directed: Field[bool] = Field(property_id="dtd.constraint.point_is_directed")
    name: Field[str | None] = Field(property_id="dtd.CDXML.name")
    line_width: Field[float | None] = Field(property_id="dtd.CDXML.line_width")
    ignore_unconnected_atoms: Field[bool] = Field(
        property_id="dtd.constraint.ignore_unconnected_atoms"
    )
    id: Field[int | None] = Field(property_id="common.id")
    hash_spacing: Field[float | None] = Field(property_id="dtd.CDXML.hash_spacing")
    dihedral_is_chiral: Field[bool] = Field(property_id="dtd.constraint.dihedral_is_chiral")
    constraint_type: Field[ConstraintType] = Field(property_id="dtd.constraint.constraint_type")
    constraint_min: Field[float | None] = Field(property_id="dtd.constraint.constraint_min")
    constraint_max: Field[float | None] = Field(property_id="dtd.constraint.constraint_max")
    color: Field[int | None] = Field(property_id="text_run.color")
    bounding_box: Field[BoundingBox | None] = Field(property_id="geometry.bounding_box")
    basis_objects: RefListField[CDXMLElement] = RefListField(
        property_id="dtd.geometry.basis_objects"
    )
    label_size: Field[float | None] = Field(property_id="dtd.CDXML.label_size")
    label_font: Field[int | None] = Field(property_id="dtd.CDXML.label_font")
    label_face: Field[int | None] = Field(property_id="dtd.CDXML.label_face")
    label_color: Field[int | None] = Field(property_id="dtd.CDXML.label_color")
    bond_length: Field[float | None] = Field(property_id="dtd.CDXML.bond_length")
    objecttags: ChildCollection[ObjectTag] = ChildCollection(
        object_type="object_tag",
        collection_name="objecttags",
    )
    annotations: ChildCollection[Annotation] = ChildCollection(
        object_type="annotation",
        collection_name="annotations",
    )


class TLCSpot(CDXMLElement):
    __spec_id__: ClassVar[str] = "tlc_spot"
    __slots__ = ()
    alpha: Field[str | None] = Field(property_id="dtd.CDXML.alpha")
    z: Field[int | None] = Field(property_id="dtd.page.z")
    width: Field[float | None] = Field(property_id="dtd.page.width")
    visible: Field[bool] = Field(property_id="common.visible")
    tail_value: Field[float | None] = Field(property_id="dtd.tlcspot.tail_value")
    show_rf: Field[bool] = Field(property_id="dtd.tlcspot.show_rf")
    rf: Field[float | None] = Field(property_id="dtd.tlcspot.rf")
    id: Field[int | None] = Field(property_id="common.id")
    height: Field[float | None] = Field(property_id="dtd.page.height")
    curve_type: Field[int | None] = Field(property_id="dtd.curve.curve_type")
    color: Field[int | None] = Field(property_id="text_run.color")
    objecttags: ChildCollection[ObjectTag] = ChildCollection(
        object_type="object_tag",
        collection_name="objecttags",
    )
    annotations: ChildCollection[Annotation] = ChildCollection(
        object_type="annotation",
        collection_name="annotations",
    )
    embeddedobjects: ChildCollection[EmbeddedObject] = ChildCollection(
        object_type="embedded_object",
        collection_name="embeddedobjects",
    )


class TLCLane(CDXMLElement):
    __spec_id__: ClassVar[str] = "tlc_lane"
    __slots__ = ()
    id: Field[int | None] = Field(property_id="common.id")
    visible: Field[bool] = Field(property_id="common.visible")
    objecttags: ChildCollection[ObjectTag] = ChildCollection(
        object_type="object_tag",
        collection_name="objecttags",
    )
    annotations: ChildCollection[Annotation] = ChildCollection(
        object_type="annotation",
        collection_name="annotations",
    )
    tlcspots: ChildCollection[TLCSpot] = ChildCollection(
        object_type="tlc_spot",
        collection_name="tlcspots",
    )


class TLCPlate(CDXMLElement):
    __spec_id__: ClassVar[str] = "tlc_plate"
    __slots__ = ()
    alpha: Field[str | None] = Field(property_id="dtd.CDXML.alpha")
    z: Field[int | None] = Field(property_id="dtd.page.z")
    visible: Field[bool] = Field(property_id="common.visible")
    transparent: Field[bool] = Field(property_id="dtd.tlcplate.transparent")
    top_right: Field[Point2D | None] = Field(property_id="dtd.tlcplate.top_right")
    top_left: Field[Point2D | None] = Field(property_id="dtd.tlcplate.top_left")
    superseded_by: RefField[CDXMLElement | None] = RefField(property_id="dtd.t.superseded_by")
    solvent_front_fraction: Field[float | None] = Field(
        property_id="dtd.tlcplate.solvent_front_fraction"
    )
    show_solvent_front: Field[bool] = Field(property_id="dtd.tlcplate.show_solvent_front")
    show_side_ticks: Field[bool] = Field(property_id="dtd.tlcplate.show_side_ticks")
    show_origin: Field[bool] = Field(property_id="dtd.tlcplate.show_origin")
    show_borders: Field[bool] = Field(property_id="dtd.tlcplate.show_borders")
    origin_fraction: Field[float | None] = Field(property_id="dtd.tlcplate.origin_fraction")
    margin_width: Field[float | None] = Field(property_id="dtd.CDXML.margin_width")
    line_width: Field[float | None] = Field(property_id="dtd.CDXML.line_width")
    label_size: Field[float | None] = Field(property_id="dtd.CDXML.label_size")
    label_font: Field[int | None] = Field(property_id="dtd.CDXML.label_font")
    label_face: Field[int | None] = Field(property_id="dtd.CDXML.label_face")
    id: Field[int | None] = Field(property_id="common.id")
    hash_spacing: Field[float | None] = Field(property_id="dtd.CDXML.hash_spacing")
    color: Field[int | None] = Field(property_id="text_run.color")
    bounding_box: Field[BoundingBox | None] = Field(property_id="geometry.bounding_box")
    bottom_right: Field[Point2D | None] = Field(property_id="dtd.tlcplate.bottom_right")
    bottom_left: Field[Point2D | None] = Field(property_id="dtd.tlcplate.bottom_left")
    bold_width: Field[float | None] = Field(property_id="dtd.CDXML.bold_width")
    bgcolor: Field[int | None] = Field(property_id="dtd.CDXML.bgcolor")
    objecttags: ChildCollection[ObjectTag] = ChildCollection(
        object_type="object_tag",
        collection_name="objecttags",
    )
    annotations: ChildCollection[Annotation] = ChildCollection(
        object_type="annotation",
        collection_name="annotations",
    )
    tlclanes: ChildCollection[TLCLane] = ChildCollection(
        object_type="tlc_lane",
        collection_name="tlclanes",
    )


class Marker(CDXMLElement):
    __spec_id__: ClassVar[str] = "marker"
    __slots__ = ()
    caption_justification: Field[CaptionJustification] = Field(
        property_id="dtd.CDXML.caption_justification"
    )
    value: Field[int | float | str] = Field(property_id="dtd.objecttag.value")
    tag_type: Field[TagType | None] = Field(property_id="dtd.objecttag.tag_type")
    persistent: Field[bool] = Field(property_id="dtd.objecttag.persistent")
    name: Field[str] = Field(property_id="dtd.objecttag.name")
    marker_offset: Field[str | None] = Field(property_id="dtd.marker.marker_offset")
    marker_angle: Field[str | None] = Field(property_id="dtd.marker.marker_angle")
    id: Field[int | None] = Field(property_id="common.id")
    display_name: Field[str | None] = Field(property_id="dtd.objecttag.display_name")
    color: Field[int | None] = Field(property_id="text_run.color")
    annotations: ChildCollection[Annotation] = ChildCollection(
        object_type="annotation",
        collection_name="annotations",
    )
    texts: ChildCollection[Text] = ChildCollection(
        object_type="text",
        collection_name="texts",
    )
    curves: ChildCollection[Curve] = ChildCollection(
        object_type="curve",
        collection_name="curves",
    )


class GEPBand(CDXMLElement):
    __spec_id__: ClassVar[str] = "gep_band"
    __slots__ = ()
    alpha: Field[str | None] = Field(property_id="dtd.CDXML.alpha")
    z: Field[int | None] = Field(property_id="dtd.page.z")
    width: Field[float | None] = Field(property_id="dtd.page.width")
    visible: Field[bool] = Field(property_id="common.visible")
    show_value: Field[bool] = Field(property_id="dtd.gepband.show_value")
    id: Field[int | None] = Field(property_id="common.id")
    height: Field[float | None] = Field(property_id="dtd.page.height")
    curve_type: Field[int | None] = Field(property_id="dtd.curve.curve_type")
    color: Field[int | None] = Field(property_id="text_run.color")
    band_value: Field[str | None] = Field(property_id="dtd.gepband.band_value")
    annotations: ChildCollection[Annotation] = ChildCollection(
        object_type="annotation",
        collection_name="annotations",
    )
    embeddedobjects: ChildCollection[EmbeddedObject] = ChildCollection(
        object_type="embedded_object",
        collection_name="embeddedobjects",
    )
    markers: ChildCollection[Marker] = ChildCollection(
        object_type="marker",
        collection_name="markers",
    )


class GEPLane(CDXMLElement):
    __spec_id__: ClassVar[str] = "gep_lane"
    __slots__ = ()
    id: Field[int | None] = Field(property_id="common.id")
    visible: Field[bool] = Field(property_id="common.visible")
    label_text: Field[str | None] = Field(property_id="dtd.gepplate.label_text")
    annotations: ChildCollection[Annotation] = ChildCollection(
        object_type="annotation",
        collection_name="annotations",
    )
    gepbands: ChildCollection[GEPBand] = ChildCollection(
        object_type="gep_band",
        collection_name="gepbands",
    )
    texts: ChildCollection[Text] = ChildCollection(
        object_type="text",
        collection_name="texts",
    )


class GEPPlate(CDXMLElement):
    __spec_id__: ClassVar[str] = "gep_plate"
    __slots__ = ()
    axis_width: Field[str | None] = Field(property_id="dtd.gepplate.axis_width")
    z: Field[int | None] = Field(property_id="dtd.page.z")
    visible: Field[bool] = Field(property_id="common.visible")
    unit_id: Field[str | None] = Field(property_id="dtd.gepplate.unit_id")
    transparent: Field[bool] = Field(property_id="dtd.tlcplate.transparent")
    top_right: Field[Point2D | None] = Field(property_id="dtd.tlcplate.top_right")
    top_left: Field[Point2D | None] = Field(property_id="dtd.tlcplate.top_left")
    superseded_by: RefField[CDXMLElement | None] = RefField(property_id="dtd.t.superseded_by")
    start_range: Field[str | None] = Field(property_id="dtd.gepplate.start_range")
    show_scale: Field[bool] = Field(property_id="dtd.gepplate.show_scale")
    show_borders: Field[bool] = Field(property_id="dtd.tlcplate.show_borders")
    margin_width: Field[float | None] = Field(property_id="dtd.CDXML.margin_width")
    line_width: Field[float | None] = Field(property_id="dtd.CDXML.line_width")
    label_text: Field[str | None] = Field(property_id="dtd.gepplate.label_text")
    label_size: Field[float | None] = Field(property_id="dtd.CDXML.label_size")
    labels_angle: Field[str | None] = Field(property_id="dtd.gepplate.labels_angle")
    label_font: Field[int | None] = Field(property_id="dtd.CDXML.label_font")
    label_face: Field[int | None] = Field(property_id="dtd.CDXML.label_face")
    id: Field[int | None] = Field(property_id="common.id")
    hash_spacing: Field[float | None] = Field(property_id="dtd.CDXML.hash_spacing")
    end_range: Field[str | None] = Field(property_id="dtd.gepplate.end_range")
    color: Field[int | None] = Field(property_id="text_run.color")
    bounding_box: Field[BoundingBox | None] = Field(property_id="geometry.bounding_box")
    bottom_right: Field[Point2D | None] = Field(property_id="dtd.tlcplate.bottom_right")
    bottom_left: Field[Point2D | None] = Field(property_id="dtd.tlcplate.bottom_left")
    bold_width: Field[float | None] = Field(property_id="dtd.CDXML.bold_width")
    alpha: Field[str | None] = Field(property_id="dtd.CDXML.alpha")
    annotations: ChildCollection[Annotation] = ChildCollection(
        object_type="annotation",
        collection_name="annotations",
    )
    geplanes: ChildCollection[GEPLane] = ChildCollection(
        object_type="gep_lane",
        collection_name="geplanes",
    )


class ChemicalProperty(CDXMLElement):
    __spec_id__: ClassVar[str] = "chemical_property"
    __slots__ = ()
    basis_objects: RefListField[CDXMLElement] = RefListField(
        property_id="dtd.geometry.basis_objects"
    )
    external_bonds: Field[str | None] = Field(property_id="dtd.chemicalproperty.external_bonds")
    positioning_type: Field[PositioningType] = Field(property_id="dtd.objecttag.positioning_type")
    positioning_offset: Field[Point2D | None] = Field(
        property_id="dtd.objecttag.positioning_offset"
    )
    positioning_angle: Field[int | None] = Field(property_id="dtd.objecttag.positioning_angle")
    name: Field[str | None] = Field(property_id="dtd.CDXML.name")
    id: Field[int | None] = Field(property_id="common.id")
    chemical_property_type: Field[int | None] = Field(
        property_id="dtd.chemicalproperty.chemical_property_type"
    )
    chemically_significant: Field[bool] = Field(
        property_id="dtd.chemicalproperty.chemically_significant"
    )
    chemical_property_is_active: Field[bool] = Field(
        property_id="dtd.chemicalproperty.chemical_property_is_active"
    )
    chemical_property_display_id: RefField[CDXMLElement | None] = RefField(
        property_id="dtd.chemicalproperty.chemical_property_display_id"
    )


class SGDatum(CDXMLElement):
    __spec_id__: ClassVar[str] = "sg_datum"
    __slots__ = ()
    id: Field[int | None] = Field(property_id="common.id")
    visible: Field[bool] = Field(property_id="common.visible")
    sg_property_type: Field[str | None] = Field(property_id="dtd.sgdatum.sg_property_type")
    sg_data_value: Field[str | None] = Field(property_id="dtd.sgdatum.sg_data_value")
    sg_data_type: Field[str | None] = Field(property_id="dtd.sgdatum.sg_data_type")
    is_read_only: Field[bool] = Field(property_id="dtd.sgdatum.is_read_only")
    is_hidden: Field[bool] = Field(property_id="dtd.sgdatum.is_hidden")
    is_edited: Field[bool] = Field(property_id="dtd.sgdatum.is_edited")
    objecttags: ChildCollection[ObjectTag] = ChildCollection(
        object_type="object_tag",
        collection_name="objecttags",
    )
    embeddedobjects: ChildCollection[EmbeddedObject] = ChildCollection(
        object_type="embedded_object",
        collection_name="embeddedobjects",
    )


class SGComponent(CDXMLElement):
    __spec_id__: ClassVar[str] = "sg_component"
    __slots__ = ()
    component_is_header: Field[bool] = Field(property_id="dtd.sgcomponent.component_is_header")
    width: Field[float | None] = Field(property_id="dtd.page.width")
    visible: Field[bool] = Field(property_id="common.visible")
    id: Field[int | None] = Field(property_id="common.id")
    component_reference_id: Field[str | None] = Field(
        property_id="dtd.sgcomponent.component_reference_id"
    )
    component_is_reactant: Field[bool] = Field(property_id="dtd.sgcomponent.component_is_reactant")
    objecttags: ChildCollection[ObjectTag] = ChildCollection(
        object_type="object_tag",
        collection_name="objecttags",
    )
    sgdatums: ChildCollection[SGDatum] = ChildCollection(
        object_type="sg_datum",
        collection_name="sgdatums",
    )


class StoichiometryGrid(CDXMLElement):
    __spec_id__: ClassVar[str] = "stoichiometry_grid"
    __slots__ = ()
    alpha: Field[str | None] = Field(property_id="dtd.CDXML.alpha")
    z: Field[int | None] = Field(property_id="dtd.page.z")
    visible: Field[bool] = Field(property_id="common.visible")
    superseded_by: RefField[CDXMLElement | None] = RefField(property_id="dtd.t.superseded_by")
    position: Field[Point2D | None] = Field(property_id="node.position")
    margin_width: Field[float | None] = Field(property_id="dtd.CDXML.margin_width")
    line_width: Field[float | None] = Field(property_id="dtd.CDXML.line_width")
    label_size: Field[float | None] = Field(property_id="dtd.CDXML.label_size")
    label_font: Field[int | None] = Field(property_id="dtd.CDXML.label_font")
    label_face: Field[int | None] = Field(property_id="dtd.CDXML.label_face")
    id: Field[int | None] = Field(property_id="common.id")
    color: Field[int | None] = Field(property_id="text_run.color")
    bounding_box: Field[BoundingBox | None] = Field(property_id="geometry.bounding_box")
    bold_width: Field[float | None] = Field(property_id="dtd.CDXML.bold_width")
    objecttags: ChildCollection[ObjectTag] = ChildCollection(
        object_type="object_tag",
        collection_name="objecttags",
    )
    annotations: ChildCollection[Annotation] = ChildCollection(
        object_type="annotation",
        collection_name="annotations",
    )
    sgcomponents: ChildCollection[SGComponent] = ChildCollection(
        object_type="sg_component",
        collection_name="sgcomponents",
    )


class Page(CDXMLElement):
    __spec_id__: ClassVar[str] = "page"
    __slots__ = ()
    alpha: Field[str | None] = Field(property_id="dtd.CDXML.alpha")
    z: Field[int | None] = Field(property_id="dtd.page.z")
    width: Field[float | None] = Field(property_id="dtd.page.width")
    splitter_positions: RefListField[CDXMLElement] = RefListField(
        property_id="dtd.page.splitter_positions"
    )
    print_trim_marks: Field[bool] = Field(property_id="dtd.page.print_trim_marks")
    page_overlap: Field[float | None] = Field(property_id="dtd.page.page_overlap")
    page_definition: Field[PageDefinition] = Field(property_id="dtd.page.page_definition")
    height_pages: Field[int] = Field(property_id="dtd.page.height_pages")
    header_position: Field[float | None] = Field(property_id="dtd.page.header_position")
    header: Field[str | None] = Field(property_id="dtd.page.header")
    width_pages: Field[int] = Field(property_id="dtd.page.width_pages")
    id: Field[int | None] = Field(property_id="common.id")
    height: Field[float | None] = Field(property_id="dtd.page.height")
    footer_position: Field[float | None] = Field(property_id="dtd.page.footer_position")
    footer: Field[str | None] = Field(property_id="dtd.page.footer")
    drawing_space: Field[DrawingSpace] = Field(property_id="dtd.page.drawing_space")
    color: Field[int | None] = Field(property_id="text_run.color")
    bounds_in_parent: Field[BoundingBox | None] = Field(property_id="dtd.page.bounds_in_parent")
    bounding_box: Field[BoundingBox | None] = Field(property_id="geometry.bounding_box")
    bgcolor: Field[int | None] = Field(property_id="dtd.CDXML.bgcolor")
    bgalpha: Field[str | None] = Field(property_id="dtd.CDXML.bgalpha")
    texts: ChildCollection[Text] = ChildCollection(
        object_type="text",
        collection_name="texts",
    )
    fragments: ChildCollection[Fragment] = ChildCollection(
        object_type="fragment",
        collection_name="fragments",
    )
    groups: ChildCollection[Group] = ChildCollection(
        object_type="group",
        collection_name="groups",
    )
    graphics: ChildCollection[Graphic] = ChildCollection(
        object_type="graphic",
        collection_name="graphics",
    )
    altgroups: ChildCollection[AltGroup] = ChildCollection(
        object_type="alt_group",
        collection_name="altgroups",
    )
    curves: ChildCollection[Curve] = ChildCollection(
        object_type="curve",
        collection_name="curves",
    )
    steps: ChildCollection[ReactionStep] = ChildCollection(
        object_type="reaction_step",
        collection_name="steps",
    )
    schemes: ChildCollection[ReactionScheme] = ChildCollection(
        object_type="reaction_scheme",
        collection_name="schemes",
    )
    spectrums: ChildCollection[Spectrum] = ChildCollection(
        object_type="spectrum",
        collection_name="spectrums",
    )
    embeddedobjects: ChildCollection[EmbeddedObject] = ChildCollection(
        object_type="embedded_object",
        collection_name="embeddedobjects",
    )
    sequences: ChildCollection[Sequence] = ChildCollection(
        object_type="sequence",
        collection_name="sequences",
    )
    crossreferences: ChildCollection[CrossReference] = ChildCollection(
        object_type="cross_reference",
        collection_name="crossreferences",
    )
    splitters: ChildCollection[Splitter] = ChildCollection(
        object_type="splitter",
        collection_name="splitters",
    )
    tables: ChildCollection[Table] = ChildCollection(
        object_type="table",
        collection_name="tables",
    )
    bracketedgroups: ChildCollection[BracketedGroup] = ChildCollection(
        object_type="bracketed_group",
        collection_name="bracketedgroups",
    )
    borders: ChildCollection[Border] = ChildCollection(
        object_type="border",
        collection_name="borders",
    )
    geometrys: ChildCollection[Geometry] = ChildCollection(
        object_type="geometry",
        collection_name="geometrys",
    )
    constraints: ChildCollection[Constraint] = ChildCollection(
        object_type="constraint",
        collection_name="constraints",
    )
    tlcplates: ChildCollection[TLCPlate] = ChildCollection(
        object_type="tlc_plate",
        collection_name="tlcplates",
    )
    gepplates: ChildCollection[GEPPlate] = ChildCollection(
        object_type="gep_plate",
        collection_name="gepplates",
    )
    chemicalpropertys: ChildCollection[ChemicalProperty] = ChildCollection(
        object_type="chemical_property",
        collection_name="chemicalpropertys",
    )
    arrows: ChildCollection[Arrow] = ChildCollection(
        object_type="arrow",
        collection_name="arrows",
    )
    bioshapes: ChildCollection[BioShape] = ChildCollection(
        object_type="bio_shape",
        collection_name="bioshapes",
    )
    stoichiometrygrids: ChildCollection[StoichiometryGrid] = ChildCollection(
        object_type="stoichiometry_grid",
        collection_name="stoichiometrygrids",
    )
    plasmidmaps: ChildCollection[PlasmidMap] = ChildCollection(
        object_type="plasmid_map",
        collection_name="plasmidmaps",
    )
    objecttags: ChildCollection[ObjectTag] = ChildCollection(
        object_type="object_tag",
        collection_name="objecttags",
    )
    annotations: ChildCollection[Annotation] = ChildCollection(
        object_type="annotation",
        collection_name="annotations",
    )
    rlogics: ChildCollection[RLogic] = ChildCollection(
        object_type="rlogic",
        collection_name="rlogics",
    )


class TemplateGrid(CDXMLElement):
    __spec_id__: ClassVar[str] = "template_grid"
    __slots__ = ()
    extent: Field[Point2D | None] = Field(property_id="dtd.templategrid.extent")
    pane_height: Field[float | None] = Field(property_id="dtd.templategrid.pane_height")
    num_rows: Field[int | None] = Field(property_id="dtd.templategrid.num_rows")
    num_columns: Field[int | None] = Field(property_id="dtd.templategrid.num_columns")


class CDXMLRoot(CDXMLElement):
    __spec_id__: ClassVar[str] = "cdxml_root"
    __slots__ = ()
    alpha: Field[str | None] = Field(property_id="dtd.CDXML.alpha")
    show_residue_id: Field[bool] = Field(property_id="dtd.CDXML.show_residue_id")
    rxn_autonumber_style: Field[str | None] = Field(property_id="dtd.CDXML.rxn_autonumber_style")
    rxn_autonumber_start: Field[str | None] = Field(property_id="dtd.CDXML.rxn_autonumber_start")
    rxn_autonumber_format: Field[str | None] = Field(property_id="dtd.CDXML.rxn_autonumber_format")
    rxn_autonumber_conditions: Field[str | None] = Field(
        property_id="dtd.CDXML.rxn_autonumber_conditions"
    )
    residue_wrap_count: Field[str | None] = Field(property_id="dtd.CDXML.residue_wrap_count")
    residue_block_count: Field[str | None] = Field(property_id="dtd.CDXML.residue_block_count")
    chem_prop_p_ka: Field[str | None] = Field(property_id="dtd.CDXML.chem_prop_p_ka")
    chem_prop_log_s: Field[str | None] = Field(property_id="dtd.CDXML.chem_prop_log_s")
    chem_prop_fragment_label: Field[str | None] = Field(
        property_id="dtd.CDXML.chem_prop_fragment_label"
    )
    chem_prop_id: Field[str | None] = Field(property_id="dtd.CDXML.chem_prop_id")
    win_print_info: Field[str | None] = Field(property_id="dtd.CDXML.win_print_info")
    window_size: Field[Point2D | None] = Field(property_id="dtd.CDXML.window_size")
    window_position: Field[Point2D | None] = Field(property_id="dtd.CDXML.window_position")
    window_is_zoomed: Field[bool] = Field(property_id="dtd.CDXML.window_is_zoomed")
    show_terminal_carbon_labels: Field[bool] = Field(
        property_id="dtd.CDXML.show_terminal_carbon_labels"
    )
    show_sequence_unlinked_branches: Field[bool] = Field(
        property_id="dtd.CDXML.show_sequence_unlinked_branches"
    )
    show_sequence_termini: Field[bool] = Field(property_id="dtd.CDXML.show_sequence_termini")
    show_sequence_bonds: Field[bool] = Field(property_id="dtd.CDXML.show_sequence_bonds")
    show_non_terminal_carbon_labels: Field[bool] = Field(
        property_id="dtd.CDXML.show_non_terminal_carbon_labels"
    )
    show_bond_stereo: Field[bool] = Field(property_id="dtd.CDXML.show_bond_stereo")
    show_bond_rxn: Field[bool] = Field(property_id="dtd.CDXML.show_bond_rxn")
    show_bond_query: Field[bool] = Field(property_id="dtd.CDXML.show_bond_query")
    show_atom_stereo: Field[bool] = Field(property_id="dtd.CDXML.show_atom_stereo")
    show_atom_query: Field[bool] = Field(property_id="dtd.CDXML.show_atom_query")
    show_atom_number: Field[bool] = Field(property_id="dtd.CDXML.show_atom_number")
    show_atom_enhanced_stereo: Field[bool] = Field(
        property_id="dtd.CDXML.show_atom_enhanced_stereo"
    )
    print_margins: Field[BoundingBox | None] = Field(property_id="dtd.CDXML.print_margins")
    name: Field[str | None] = Field(property_id="dtd.CDXML.name")
    modification_user_name: Field[str | None] = Field(
        property_id="dtd.CDXML.modification_user_name"
    )
    modification_program: Field[str | None] = Field(property_id="dtd.CDXML.modification_program")
    modification_date: Field[str | None] = Field(property_id="dtd.CDXML.modification_date")
    margin_width: Field[float | None] = Field(property_id="dtd.CDXML.margin_width")
    magnification: Field[int | None] = Field(property_id="dtd.CDXML.magnification")
    mac_print_info: Field[str | None] = Field(property_id="dtd.CDXML.mac_print_info")
    line_width: Field[float | None] = Field(property_id="dtd.CDXML.line_width")
    label_size: Field[float | None] = Field(property_id="dtd.CDXML.label_size")
    label_line_height: Field[int | None] = Field(property_id="dtd.CDXML.label_line_height")
    label_justification: Field[LabelJustification] = Field(
        property_id="dtd.CDXML.label_justification"
    )
    label_font: Field[int | None] = Field(property_id="dtd.CDXML.label_font")
    label_face: Field[int | None] = Field(property_id="dtd.CDXML.label_face")
    label_color: Field[int | None] = Field(property_id="dtd.CDXML.label_color")
    interpret_chemically: Field[bool] = Field(property_id="dtd.CDXML.interpret_chemically")
    hide_implicit_hydrogens: Field[bool] = Field(property_id="dtd.CDXML.hide_implicit_hydrogens")
    hash_spacing: Field[float | None] = Field(property_id="dtd.CDXML.hash_spacing")
    fractional_widths: Field[bool] = Field(property_id="dtd.CDXML.fractional_widths")
    fix_in_place_gap: Field[Point2D | None] = Field(property_id="dtd.CDXML.fix_in_place_gap")
    fix_in_place_extent: Field[Point2D | None] = Field(property_id="dtd.CDXML.fix_in_place_extent")
    creation_user_name: Field[str | None] = Field(property_id="dtd.CDXML.creation_user_name")
    creation_program: Field[str | None] = Field(property_id="dtd.CDXML.creation_program")
    creation_date: Field[str | None] = Field(property_id="dtd.CDXML.creation_date")
    comment: Field[str | None] = Field(property_id="dtd.CDXML.comment")
    color: Field[int | None] = Field(property_id="text_run.color")
    chem_propt_psa: Field[str | None] = Field(property_id="dtd.CDXML.chem_propt_psa")
    chem_prop_name: Field[str | None] = Field(property_id="dtd.CDXML.chem_prop_name")
    chem_prop_mr: Field[str | None] = Field(property_id="dtd.CDXML.chem_prop_mr")
    chem_prop_m_over_z: Field[str | None] = Field(property_id="dtd.CDXML.chem_prop_m_over_z")
    chem_prop_mol_wt: Field[str | None] = Field(property_id="dtd.CDXML.chem_prop_mol_wt")
    chem_prop_melting_pt: Field[str | None] = Field(property_id="dtd.CDXML.chem_prop_melting_pt")
    chem_prop_log_p: Field[str | None] = Field(property_id="dtd.CDXML.chem_prop_log_p")
    chem_prop_henry: Field[str | None] = Field(property_id="dtd.CDXML.chem_prop_henry")
    chem_prop_gibbs: Field[str | None] = Field(property_id="dtd.CDXML.chem_prop_gibbs")
    chem_prop_formula: Field[str | None] = Field(property_id="dtd.CDXML.chem_prop_formula")
    chem_prop_exact_mass: Field[str | None] = Field(property_id="dtd.CDXML.chem_prop_exact_mass")
    chem_prop_e_form: Field[str | None] = Field(property_id="dtd.CDXML.chem_prop_e_form")
    chem_prop_crit_vol: Field[str | None] = Field(property_id="dtd.CDXML.chem_prop_crit_vol")
    chem_prop_crit_temp: Field[str | None] = Field(property_id="dtd.CDXML.chem_prop_crit_temp")
    chem_prop_crit_pres: Field[str | None] = Field(property_id="dtd.CDXML.chem_prop_crit_pres")
    chem_prop_cmr: Field[str | None] = Field(property_id="dtd.CDXML.chem_prop_cmr")
    chem_prop_c_log_p: Field[str | None] = Field(property_id="dtd.CDXML.chem_prop_c_log_p")
    chem_prop_boiling_pt: Field[str | None] = Field(property_id="dtd.CDXML.chem_prop_boiling_pt")
    chem_prop_analysis: Field[str | None] = Field(property_id="dtd.CDXML.chem_prop_analysis")
    chain_angle: Field[int | None] = Field(property_id="dtd.CDXML.chain_angle")
    cartridge_data: Field[str | None] = Field(property_id="dtd.CDXML.cartridge_data")
    caption_size: Field[float | None] = Field(property_id="dtd.CDXML.caption_size")
    caption_line_height: Field[int | None] = Field(property_id="dtd.CDXML.caption_line_height")
    caption_justification: Field[CaptionJustification] = Field(
        property_id="dtd.CDXML.caption_justification"
    )
    caption_font: Field[int | None] = Field(property_id="dtd.CDXML.caption_font")
    caption_face: Field[int | None] = Field(property_id="dtd.CDXML.caption_face")
    caption_color: Field[int | None] = Field(property_id="dtd.CDXML.caption_color")
    bounding_box: Field[BoundingBox | None] = Field(property_id="geometry.bounding_box")
    bond_spacing_abs: Field[float | None] = Field(property_id="dtd.CDXML.bond_spacing_abs")
    bond_spacing: Field[int | None] = Field(property_id="dtd.CDXML.bond_spacing")
    bond_length: Field[float | None] = Field(property_id="dtd.CDXML.bond_length")
    bold_width: Field[float | None] = Field(property_id="dtd.CDXML.bold_width")
    bgcolor: Field[int | None] = Field(property_id="dtd.CDXML.bgcolor")
    bgalpha: Field[str | None] = Field(property_id="dtd.CDXML.bgalpha")
    amino_acid_termini: Field[AminoAcidTermini] = Field(property_id="dtd.CDXML.amino_acid_termini")
    color_tables: ChildCollection[ColorTable] = ChildCollection(
        object_type="color_table",
        collection_name="color_tables",
    )
    font_tables: ChildCollection[FontTable] = ChildCollection(
        object_type="font_table",
        collection_name="font_tables",
    )
    pages: ChildCollection[Page] = ChildCollection(
        object_type="page",
        collection_name="pages",
    )
    template_grids: ChildCollection[TemplateGrid] = ChildCollection(
        object_type="template_grid",
        collection_name="template_grids",
    )
