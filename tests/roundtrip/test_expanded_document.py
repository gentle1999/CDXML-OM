"""Round-trip coverage for text, graphic, reaction, and local resource models."""

from __future__ import annotations

import pytest

from cdxml_om import (
    Arrow,
    BoundingBox,
    CDXMLDocument,
    Color,
    ColorTable,
    Font,
    FontTable,
    Fragment,
    Graphic,
    Group,
    MutationError,
    Node,
    ReactionScheme,
    ReactionStep,
    ReferenceResolutionError,
    Text,
    TextRun,
)

_EXPANDED_SOURCE = """<?xml version="1.0" encoding="UTF-8"?>
<CDXML xmlns:v="urn:vendor" VendorRoot="preserve-root">
  <fonttable VendorTable="font-table">
    <font id="1" name="Aster Sans" charset="204"/>
    <font id="2" name="Aster Symbol" charset="2"/>
  </fonttable>
  <colortable VendorTable="color-table">
    <color r="0" g="0.25" b="1"/>
    <color r="1" g="0" b="0.5"/>
  </colortable>
  <page id="10">
    <group id="20" VendorGroup="keep-group">
      <t id="30" p="001.0 02.0" VendorText="keep-text">
        <s font="1" size="12" face="1" color="0" alpha="0.75">alpha</s>
        <!-- keep text-run order -->
        <v:opaque marker="keep-vendor-child"/>
        <s font="2" size="8.5" face="2"><![CDATA[βeta & preserved]]></s>
      </t>
      <graphic id="40" GraphicType="Rectangle" BoundingBox="1 2 31 42"
        Tail3D="4 5 6" Center3D="7 8 9" Head3D="10 11 12"
        VendorGraphic="keep-graphic"/>
      <arrow id="41" BoundingBox="2 3 22 33" Tail3D="1 2 3"
        Center3D="4 5 6" Head3D="7 8 9" ArrowheadType="Solid"
        ArrowheadHead="Full" VendorArrow="keep-arrow"/>
      <fragment id="60"><n id="1" Element="6"/></fragment>
      <group id="70" VendorNestedGroup="keep-nested-group"/>
      <scheme id="80">
        <step id="81" ReactionStepReactants="60 70"
          ReactionStepProducts="60" ReactionStepArrows="40 41"
          VendorReaction="keep-reaction"/>
      </scheme>
    </group>
  </page>
</CDXML>"""


def _assert_roundtrip_reaction_references(document: CDXMLDocument) -> None:
    fragment = document.get(Fragment, 60)
    group = document.get(Group, 70)
    graphic = document.get(Graphic, 40)
    arrow = document.get(Arrow, 41)
    scheme = document.get(ReactionScheme, 80)
    step = document.get(ReactionStep, 81)
    assert fragment is not None
    assert group is not None
    assert graphic is not None
    assert arrow is not None
    assert scheme is not None
    assert step is not None
    assert scheme.steps[0] is step
    assert step.reactants == (fragment, group)
    assert step.products == (fragment,)
    assert step.arrows == (graphic, arrow)
    assert step.raw_reference_ids("reactants") == (60, 70)
    assert step.raw_reference_ids("arrows") == (40, 41)


def test_expanded_typed_navigation_and_local_resources_roundtrip() -> None:
    document = CDXMLDocument.from_string(_EXPANDED_SOURCE)
    assert document.validate().is_valid

    page = document.pages[0]
    group = page.groups[0]
    text = group.texts[0]
    assert isinstance(group, Group)
    assert document.groups[0] is group
    assert document.texts[0] is text
    runs = text.runs
    assert len(runs) == 2
    assert isinstance(runs[0], TextRun)
    assert runs[0].content == "alpha"
    assert runs[0].font_id == 1
    assert runs[0].size == 12.0
    assert runs[0].face == 1
    assert runs[0].color == 0
    assert runs[0].alpha == pytest.approx(0.75)
    assert runs[1].content == "βeta & preserved"
    assert text.plain_text == "alphaβeta & preserved"

    font_table = document.font_table
    color_table = document.color_table
    assert font_table is not None
    assert color_table is not None
    assert isinstance(font_table, FontTable)
    assert isinstance(color_table, ColorTable)
    assert len(font_table.fonts) == 2
    first_font = font_table.fonts[0]
    assert isinstance(first_font, Font)
    assert first_font.id == 1
    assert first_font.name == "Aster Sans"
    assert first_font.charset == "204"
    assert isinstance(first_font.charset, str)
    first_color = color_table.colors[0]
    assert isinstance(first_color, Color)
    assert first_color.r == pytest.approx(0.0)
    assert first_color.g == pytest.approx(0.25)
    assert first_color.b == pytest.approx(1.0)

    # The first font's table-local ID deliberately overlaps this global Node ID.
    fragment_node = document.get(Node, 1)
    assert fragment_node is not None
    assert fragment_node.element == 6
    assert font_table.raw_attributes.get("id") is None
    assert color_table.raw_attributes.get("id") is None
    assert first_color.raw_attributes.get("id") is None
    assert runs[0].raw_attributes.get("id") is None

    graphic = document.get(Graphic, 40)
    arrow = document.get(Arrow, 41)
    assert graphic is not None
    assert arrow is not None
    assert document.graphics[0] is graphic
    assert document.arrows[0] is arrow
    assert graphic.bounding_box == BoundingBox(1.0, 2.0, 31.0, 42.0)
    assert graphic.tail_3d is not None
    assert (graphic.tail_3d.x, graphic.tail_3d.y, graphic.tail_3d.z) == (4.0, 5.0, 6.0)
    assert graphic.center_3d is not None
    assert (graphic.center_3d.x, graphic.center_3d.y, graphic.center_3d.z) == (
        7.0,
        8.0,
        9.0,
    )
    assert graphic.head_3d is not None
    assert (graphic.head_3d.x, graphic.head_3d.y, graphic.head_3d.z) == (
        10.0,
        11.0,
        12.0,
    )
    assert arrow.bounding_box == BoundingBox(2.0, 3.0, 22.0, 33.0)
    assert arrow.head_3d is not None
    assert (arrow.head_3d.x, arrow.head_3d.y, arrow.head_3d.z) == (7.0, 8.0, 9.0)

    _assert_roundtrip_reaction_references(document)
    assert document.schemes[0] is document.get(ReactionScheme, 80)
    serialized = document.to_string()
    assert 'VendorRoot="preserve-root"' in serialized
    assert 'VendorGraphic="keep-graphic"' in serialized
    assert 'VendorArrow="keep-arrow"' in serialized
    assert 'VendorTable="font-table"' in serialized
    assert 'VendorTable="color-table"' in serialized
    reparsed = CDXMLDocument.from_string(serialized)
    assert reparsed.validate().is_valid
    _assert_roundtrip_reaction_references(reparsed)
    reparsed_text = reparsed.get(Text, 30)
    assert reparsed_text is not None
    assert reparsed_text.plain_text == "alphaβeta & preserved"
    assert reparsed_text.runs[1].content == "βeta & preserved"
    assert reparsed.get(Node, 1) is not None
    assert reparsed.font_table is not None
    assert reparsed.font_table.fonts[0].charset == "204"


def test_text_run_edit_preserves_other_runs_and_opaque_content() -> None:
    document = CDXMLDocument.from_string(_EXPANDED_SOURCE)
    text = document.get(Text, 30)
    assert text is not None
    original_run = text.runs[0]
    assert document.get(Text, 30) is text

    original_run.content = "changed α"
    assert document.validate().is_valid
    assert text.plain_text == "changed αβeta & preserved"
    assert text.runs[1].content == "βeta & preserved"

    serialized = document.to_string()
    assert 'VendorRoot="preserve-root"' in serialized
    assert 'VendorGroup="keep-group"' in serialized
    assert 'VendorText="keep-text"' in serialized
    assert 'marker="keep-vendor-child"' in serialized
    assert "<![CDATA[βeta & preserved]]>" in serialized
    assert "<!-- keep text-run order -->" in serialized
    assert 'p="001.0 02.0"' in serialized
    assert 'BoundingBox="1 2 31 42"' in serialized
    assert '<s font="1" size="12" face="1" color="0" alpha="0.75">changed α</s>' in serialized
    assert serialized.index("changed α") < serialized.index("keep-vendor-child")
    assert serialized.index("keep-vendor-child") < serialized.index("βeta & preserved")
    assert 'font="2" size="8.5" face="2"' in serialized

    reparsed = CDXMLDocument.from_string(serialized)
    reparsed_text = reparsed.get(Text, 30)
    assert reparsed_text is not None
    assert len(reparsed_text.runs) == 2
    assert reparsed_text.runs[0].content == "changed α"
    assert reparsed_text.runs[1].content == "βeta & preserved"
    assert reparsed_text.plain_text == "changed αβeta & preserved"
    serialized_again = reparsed.to_string()
    assert serialized_again.index("changed α") < serialized_again.index("keep-vendor-child")
    assert serialized_again.index("keep-vendor-child") < serialized_again.index("βeta & preserved")
    assert serialized_again.index("keep text-run order") < serialized_again.index(
        "keep-vendor-child"
    )
    assert 'VendorText="keep-text"' in serialized_again
    assert "<![CDATA[βeta & preserved]]>" in serialized_again


def test_reaction_ref_lists_mutate_atomically_and_preserve_legacy_graphic_refs() -> None:
    document = CDXMLDocument.from_string(_EXPANDED_SOURCE)
    fragment = document.get(Fragment, 60)
    group = document.get(Group, 70)
    graphic = document.get(Graphic, 40)
    arrow = document.get(Arrow, 41)
    step = document.get(ReactionStep, 81)
    assert fragment is not None
    assert group is not None
    assert graphic is not None
    assert arrow is not None
    assert step is not None

    step.reactants = (group, fragment)
    step.products = (group,)
    step.arrows = (arrow, graphic)
    after_valid_assignment = document.to_string()
    assert step.raw_reference_ids("reactants") == (70, 60)
    assert step.raw_reference_ids("arrows") == (41, 40)

    foreign = CDXMLDocument.from_string(_EXPANDED_SOURCE)
    foreign_group = foreign.get(Group, 70)
    assert foreign_group is not None
    with pytest.raises(MutationError):
        step.reactants = (fragment, foreign_group)
    assert document.to_string() == after_valid_assignment

    with pytest.raises(MutationError):
        step.arrows = (arrow, object())  # type: ignore[assignment]
    assert document.to_string() == after_valid_assignment

    reparsed = CDXMLDocument.from_string(document.to_string())
    reparsed_step = reparsed.get(ReactionStep, 81)
    reparsed_group = reparsed.get(Group, 70)
    reparsed_fragment = reparsed.get(Fragment, 60)
    reparsed_arrow = reparsed.get(Arrow, 41)
    reparsed_graphic = reparsed.get(Graphic, 40)
    assert reparsed_step is not None
    assert reparsed_group is not None
    assert reparsed_fragment is not None
    assert reparsed_arrow is not None
    assert reparsed_graphic is not None
    assert reparsed_step.reactants == (reparsed_group, reparsed_fragment)
    assert reparsed_step.products == (reparsed_group,)
    assert reparsed_step.arrows == (reparsed_arrow, reparsed_graphic)
    assert 'VendorReaction="keep-reaction"' in reparsed.to_string()


def test_dangling_ref_lists_are_reported_and_source_ids_remain_preserved() -> None:
    source = _EXPANDED_SOURCE.replace(
        'ReactionStepReactants="60 70"', 'ReactionStepReactants="999 70"'
    )
    document = CDXMLDocument.from_string(source)
    step = document.get(ReactionStep, 81)
    assert step is not None
    assert step.raw_reference_ids("reactants") == (999, 70)
    with pytest.raises(ReferenceResolutionError):
        _ = step.reactants

    assert any(issue.code == "dangling-reference" for issue in document.validate().errors)
    serialized = document.to_string()
    assert 'ReactionStepReactants="999 70"' in serialized
    reparsed = CDXMLDocument.from_string(serialized)
    reparsed_step = reparsed.get(ReactionStep, 81)
    assert reparsed_step is not None
    assert reparsed_step.raw_reference_ids("reactants") == (999, 70)


def test_tables_runs_and_resources_create_without_global_object_ids() -> None:
    document = CDXMLDocument.from_string(
        '<CDXML><page id="10"><fragment id="11"><n id="1" Element="6"/></fragment></page></CDXML>'
    )
    font_table = document.create_font_table()
    font = font_table.fonts.create(id=1, name="New Serif", charset="204")
    color_table = document.create_color_table()
    color = color_table.colors.create(r=0.125, g=0.5, b=0.875)
    page = document.pages[0]
    text = page.texts.create()
    run = text.runs.create(content="created", font_id=font.id, size=11.5)

    assert font.id == 1
    assert font.charset == "204"
    assert document.get(Node, 1) is not None
    assert document.get(Font, 1) is None
    assert color.r == pytest.approx(0.125)
    assert color.g == pytest.approx(0.5)
    assert color.b == pytest.approx(0.875)
    assert text.id is not None
    assert run.content == "created"
    assert run.raw_attributes.get("id") is None
    assert color.raw_attributes.get("id") is None
    assert font_table.raw_attributes.get("id") is None
    assert color_table.raw_attributes.get("id") is None
    assert document.validate().is_valid

    output_before_duplicate = document.to_string()
    with pytest.raises(MutationError):
        font_table.fonts.create(id=1, name="Duplicate", charset="0")
    assert document.to_string() == output_before_duplicate

    serialized = document.to_string()
    reparsed = CDXMLDocument.from_string(serialized)
    reparsed_text = reparsed.get(Text, text.id)
    assert reparsed_text is not None
    assert reparsed_text.plain_text == "created"
    assert len(reparsed_text.runs) == 1
    assert reparsed_text.runs[0].font_id == 1
    assert reparsed.font_table is not None
    assert reparsed.font_table.fonts[0].name == "New Serif"
    assert reparsed.color_table is not None
    assert reparsed.color_table.colors[0].g == pytest.approx(0.5)
