"""Focused coverage for Phase 3 schema/runtime extensions."""

from __future__ import annotations

import pytest

from cdxml_om import (
    Arrow,
    CDXMLDocument,
    CodecError,
    Color,
    Font,
    Graphic,
    GraphicType,
    Group,
    MutationError,
    Page,
    Point3D,
    ReactionStep,
    Text,
)


def test_generated_models_and_children_follow_pinned_dtd_routes() -> None:
    document = CDXMLDocument.from_string("<CDXML><page id='1'/></CDXML>")
    page = document.pages[0]

    group = page.groups.create(bounding_box=(1, 2, 30, 40))
    fragment = group.fragments.create()
    node = fragment.nodes.create(element=6, position=(3, 4))
    nested_group = group.groups.create()
    text = nested_group.texts.create()
    run = text.runs.create(content="nested")
    graphic = fragment.graphics.create(
        bounding_box=(0, 0, 8, 9),
        tail_3d=(1, 2, 3),
        graphic_type=GraphicType.SYMBOL,
    )
    arrow = group.arrows.create(bounding_box=(4, 5, 6, 7), head_3d=(8, 9, 10))

    assert isinstance(group, Group)
    assert isinstance(page, Page)
    assert isinstance(node.parent, type(fragment))
    assert isinstance(text, Text)
    assert text.plain_text == "nested"
    assert isinstance(graphic, Graphic)
    assert graphic.tail_3d == Point3D(1.0, 2.0, 3.0)
    assert graphic.graphic_type.value == "Symbol"
    assert isinstance(arrow, Arrow)
    assert arrow.head_3d == Point3D(8.0, 9.0, 10.0)
    assert document.groups.all() == [group, nested_group]
    assert document.texts.all() == [text]
    assert document.graphics.all() == [graphic]
    assert document.arrows.all() == [arrow]
    assert document.validate().is_valid

    reloaded = CDXMLDocument.from_string(document.to_string())
    assert reloaded.validate().is_valid
    assert reloaded.groups[0].fragments[0].nodes[0].position == node.position
    assert reloaded.texts[0].plain_text == "nested"
    assert reloaded.graphics[0].tail_3d == Point3D(1.0, 2.0, 3.0)
    assert reloaded.arrows[0].head_3d == Point3D(8.0, 9.0, 10.0)
    assert run.content == "nested"


def test_documentation_graph_mutation_example_is_executable() -> None:
    document = CDXMLDocument.from_string("<CDXML/>")
    fragment = document.pages.create().fragments.create()
    fragment.nodes.create(element=6, position=(0.0, 0.0))
    oxygen = fragment.nodes.create(element=8, position=(10.0, 20.0))
    bond = fragment.bonds.create(begin=fragment.nodes[0], end=oxygen, order=2)
    oxygen.charge = 1

    assert bond.begin is fragment.nodes[0]
    assert bond.end is oxygen
    assert bond.order.value == 2
    assert oxygen.charge == 1
    assert CDXMLDocument.from_string(document.to_string()).validate().is_valid


def test_reaction_step_reference_lists_are_optional_and_empty_by_default() -> None:
    document = CDXMLDocument.from_string("<CDXML><page id='1'><step id='2'/></page></CDXML>")
    step = document.get(ReactionStep, 2)

    assert step is not None
    assert step.reactants == ()
    assert step.products == ()
    assert step.arrows == ()
    assert step.raw_reference_ids("reactants") is None
    assert document.validate().is_valid


def test_text_run_content_edit_rejects_opaque_mixed_children_atomically() -> None:
    document = CDXMLDocument.from_string(
        '<CDXML><page id="1"><t id="2"><s>before<v:part xmlns:v="urn:v">opaque</v:part>'
        "after</s></t></page></CDXML>"
    )
    run = document.get(Text, 2)
    assert run is not None
    text_run = run.runs[0]
    original = document.to_string()

    with pytest.raises(MutationError):
        text_run.content = "replacement"

    assert document.to_string() == original
    assert "opaque" in text_run.content


def test_unmodeled_parent_is_a_warning_not_a_false_schema_error() -> None:
    document = CDXMLDocument.from_string(
        '<CDXML><page id="1"><vendor:container xmlns:vendor="urn:vendor">'
        '<group id="2"/></vendor:container></page></CDXML>'
    )

    report = document.validate()
    assert report.is_valid
    assert any(issue.code == "unvalidated-parent" for issue in report.warnings)


def test_local_font_duplicates_and_color_range_are_scoped_and_validated() -> None:
    document = CDXMLDocument.from_string(
        '<CDXML><fonttable><font id="4" name="A"/><font id="4" name="B"/></fonttable>'
        '<colortable><color r="0.5" g="0.25" b="1.0"/></colortable>'
        '<page id="4"><fragment id="5"><n id="6"/></fragment></page></CDXML>'
    )
    table = document.font_table
    colors = document.color_table
    assert table is not None
    assert colors is not None
    assert isinstance(table.fonts[0], Font)
    assert isinstance(colors.colors[0], Color)
    assert document.get(4) is not None
    assert any(issue.code == "duplicate-local-id" for issue in document.validate().errors)

    invalid_color = CDXMLDocument.from_string(
        '<CDXML><colortable><color r="2" g="0" b="1"/></colortable><page id="1"/></CDXML>'
    )
    invalid = invalid_color.color_table
    assert invalid is not None
    with pytest.raises(CodecError):
        _ = invalid.colors[0].r
    assert any(issue.code == "invalid-value" for issue in invalid_color.validate().errors)


def test_text_run_and_color_creation_do_not_allocate_document_ids() -> None:
    document = CDXMLDocument.from_string("<CDXML><page id='1'/></CDXML>")
    font_table = document.create_font_table()
    font = font_table.fonts.create(name="Local", charset="iso-8859-1")
    color_table = document.create_color_table()
    color = color_table.colors.create(r=0.1, g=0.2, b=0.3)
    text = document.pages[0].texts.create()
    run = text.runs.create(content="run", font_id=font.id)
    another_page = document.pages.create()
    auto_font = font_table.fonts.create(name="Auto")

    assert font.id == 1
    assert auto_font.id == 2
    assert color.raw_attributes.get("id") is None
    assert run.raw_attributes.get("id") is None
    assert text.id is not None
    assert text.id == 2
    assert another_page.id == 3
    assert document.get(Font, font.id) is None
    assert document.get(Font, auto_font.id) is None
    assert document.validate().is_valid
    reloaded = CDXMLDocument.from_string(document.to_string())
    reloaded_table = reloaded.font_table
    assert reloaded_table is not None
    assert reloaded_table.fonts[1].id == 2
    assert reloaded_table.fonts[1].name == "Auto"
    assert reloaded.get(Font, 2) is None


def test_local_font_allocator_refreshes_ids_after_raw_tree_edits() -> None:
    document = CDXMLDocument.from_string(
        '<CDXML><fonttable><font id="1" name="A"/><font id="2" name="B"/></fonttable>'
        '<page id="10"/></CDXML>'
    )
    table = document.font_table
    assert table is not None
    first, second = table.fonts.all()
    allocated = table.fonts.create(name="C")
    assert allocated.id == 3

    first.raw_element.set("id", "4")
    before = document.to_string()
    with pytest.raises(MutationError):
        table.fonts.create(id=4, name="Duplicate raw edit")
    with pytest.raises(MutationError):
        second.id = 4
    assert document.to_string() == before
    after_raw_edit = table.fonts.create(name="D")
    assert after_raw_edit.id == 5
    reloaded = CDXMLDocument.from_string(document.to_string())
    reloaded_table = reloaded.font_table
    assert reloaded_table is not None
    assert [font.id for font in reloaded_table.fonts] == [4, 2, 3, 5]
