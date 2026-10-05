from __future__ import annotations

import hashlib
import math
import re
from pathlib import Path

import pytest
from lxml import etree
from tools import build_visual_samples as visual_samples

from cdxml_om import (
    Arrow,
    Bond,
    BondOrder,
    BoundingBox,
    CDXMLDocument,
    Curve,
    GenericList,
    Graphic,
    Node,
    Page,
    Point2D,
    ReactionScheme,
    Spectrum,
    Text,
    TextRun,
    UnknownElement,
)

ROOT = Path(__file__).resolve().parents[2]
SAMPLE_DIR = ROOT / "examples" / "render_samples"
NOTEBOOK_DIR = ROOT / "examples" / "notebooks"
CORPUS_DIR = ROOT / "tests" / "fixtures" / "corpus"
SAMPLE_NAMES = (
    "01_before_after.cdxml",
    "02_reaction_and_resources.cdxml",
    "03_unknown_preservation.cdxml",
    "probe_curve_points.cdxml",
    "probe_element_generic_lists.cdxml",
    "probe_spectrum_missing_required_fields.cdxml",
    "probe_spectrum_sdk_required_fields.cdxml",
)
USER_REPORTED_STABLE_SAMPLE_SHA256 = {
    "01_before_after.cdxml": ("964a3a13e65ed5b2206deac62467860bac992403853f463ea8b2c3cb7d167715"),
    "02_reaction_and_resources.cdxml": (
        "04438a51a15e4f0e009a1f5765f5b73e76bdd705d5a9ca2b72e1b9b85ac0b1d3"
    ),
    "03_unknown_preservation.cdxml": (
        "420791e8c34b1cdcf602109ba28cecd634f27766f57584a4494aac1c12a65fd7"
    ),
    "probe_element_generic_lists.cdxml": (
        "d4f28d9375ae7ba35a3470256af0c31fe4bc3ef7ce2635950e53124eac8f5234"
    ),
    "probe_spectrum_missing_required_fields.cdxml": (
        "a04e5a5fb96ad2b98c322ea1239b092c1a215575087cb90b738c7722e2edcce9"
    ),
    "probe_spectrum_sdk_required_fields.cdxml": (
        "8495b38484ca2545555cfd21569eada5f5555ec333a74e2168cb3647bf59e8d8"
    ),
}
PREVIOUS_CURVE_PROBE_SHA256 = "abb94c07688e56763deb6a73e57bccc69cc6f60d69758f9b54b60525ef39d28c"
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def _protected_inputs() -> dict[str, bytes]:
    paths = [*NOTEBOOK_DIR.glob("*.ipynb")]
    paths.extend(path for path in CORPUS_DIR.rglob("*") if path.is_file())
    return {path.relative_to(ROOT).as_posix(): path.read_bytes() for path in paths}


def _committed_samples() -> dict[str, bytes]:
    return {name: (SAMPLE_DIR / name).read_bytes() for name in SAMPLE_NAMES}


def _document(samples: dict[str, bytes], name: str) -> CDXMLDocument:
    return CDXMLDocument.from_string(samples[name])


def _within_page(page: Page, x: float, y: float) -> bool:
    bounds = page.bounding_box
    return (
        bounds is not None and bounds.left <= x <= bounds.right and bounds.top <= y <= bounds.bottom
    )


def _assert_text_and_geometry_fit(document: CDXMLDocument) -> None:
    assert len(document.pages) == 1
    page = document.pages[0]
    bounds = page.bounding_box
    assert bounds is not None

    for node in document.find(Node):
        position = node.position
        assert position is not None
        assert _within_page(page, position.x, position.y)
    for arrow in document.find(Arrow):
        for point in (arrow.tail_3d, arrow.head_3d):
            assert point is not None
            assert _within_page(page, point.x, point.y)
    for graphic in document.find(Graphic):
        box = graphic.bounding_box
        assert box is not None
        assert bounds.left <= box.left <= box.right <= bounds.right
        assert bounds.top <= box.top <= box.bottom <= bounds.bottom
    for spectrum in document.find(Spectrum):
        box = spectrum.bounding_box
        if box is not None:
            assert bounds.left <= box.left <= box.right <= bounds.right
            assert bounds.top <= box.top <= box.bottom <= bounds.bottom

    for curve in document.find(Curve):
        box = curve.bounding_box
        assert box is not None
        assert bounds.left <= box.left <= box.right <= bounds.right
        assert bounds.top <= box.top <= box.bottom <= bounds.bottom
        curve_points = curve.curve_points
        assert curve_points is not None
        for curve_point in curve_points:
            assert _within_page(page, curve_point.x, curve_point.y)
            assert box.left <= curve_point.x <= box.right
            assert box.top <= curve_point.y <= box.bottom

    for text in document.find(Text):
        position = text.position
        assert position is not None
        runs = text.runs
        # A conservative layout heuristic, not font measurement or ChemDraw verification.
        text_width = sum(len(run.content or "") * float(run.size or 10.0) * 0.6 for run in runs)
        text_height = max((float(run.size or 10.0) for run in runs), default=10.0)
        assert bounds.left <= position.x
        assert position.x + text_width <= bounds.right
        assert bounds.top <= position.y
        assert position.y + text_height <= bounds.bottom


def _assert_standard_local_resources(document: CDXMLDocument) -> None:
    font_table = document.font_table
    color_table = document.color_table
    assert font_table is not None and color_table is not None
    font_ids = {font.id for font in font_table.fonts}
    assert {3, 4} <= font_ids
    assert {font.name for font in font_table.fonts} >= {"Arial", "Times New Roman"}
    rgb = {(color.r, color.g, color.b) for color in color_table.colors}
    assert {(1.0, 1.0, 1.0), (0.0, 0.0, 0.0), (1.0, 0.0, 0.0)} <= rgb
    palette = color_table.colors
    assert (palette[1].r, palette[1].g, palette[1].b) == (0.0, 0.0, 0.0)
    assert (palette[2].r, palette[2].g, palette[2].b) == (1.0, 0.0, 0.0)
    for run in document.find(TextRun):
        if run.font_id is not None:
            assert run.font_id in font_ids
        if run.color is not None:
            assert 2 <= run.color < len(color_table.colors) + 2


def _assert_bonds_resolve(document: CDXMLDocument) -> None:
    for bond in document.find(Bond):
        begin = bond.begin
        end = bond.end
        assert begin is not None and end is not None
        assert begin.id is not None and end.id is not None
        assert document.get(Node, begin.id) is begin
        assert document.get(Node, end.id) is end
        assert bond.raw_reference_id("bond.begin") == begin.id
        assert bond.raw_reference_id("bond.end") == end.id
        assert begin.position is not None and end.position is not None
        length = math.dist((begin.position.x, begin.position.y), (end.position.x, end.position.y))
        assert length == pytest.approx(30.0, abs=0.05)


def _local_links(path: Path) -> set[Path]:
    result: set[Path] = set()
    for match in MARKDOWN_LINK_RE.finditer(path.read_text(encoding="utf-8")):
        target = match.group(1).split(maxsplit=1)[0].strip("<>")
        if not target or target.startswith(("#", "mailto:")) or "://" in target:
            continue
        linked_path = target.split("#", maxsplit=1)[0]
        if linked_path:
            result.add((path.parent / linked_path).resolve())
    return result


@pytest.fixture(scope="module")
def generated_samples() -> tuple[dict[str, bytes], dict[str, bytes], dict[str, bytes]]:
    before = _protected_inputs()
    samples = visual_samples.collect_visual_samples()
    after = _protected_inputs()
    return samples, before, after


def test_visual_sample_scenes_have_bounded_layout_and_valid_typed_content(
    generated_samples: tuple[dict[str, bytes], dict[str, bytes], dict[str, bytes]],
) -> None:
    samples, protected_before, protected_after = generated_samples
    assert protected_before == protected_after
    assert tuple(samples) == SAMPLE_NAMES
    assert samples == _committed_samples()
    assert {path.name for path in SAMPLE_DIR.glob("*.cdxml")} == set(SAMPLE_NAMES)
    assert all(
        hashlib.sha256(samples[name]).hexdigest() == expected
        for name, expected in USER_REPORTED_STABLE_SAMPLE_SHA256.items()
    )
    assert not (ROOT / "examples" / "render_samples_v2").exists()
    assert not (ROOT / "tools" / "build_visual_samples_v2.py").exists()
    assert not (ROOT / "tools" / "export_render_samples.py").exists()
    assert not (ROOT / "tests" / "unit" / "test_visual_samples.py").exists()

    documents = {name: _document(samples, name) for name in SAMPLE_NAMES}
    for document in documents.values():
        report = document.validate()
        assert report.is_valid, [issue.code for issue in report.errors]
        _assert_standard_local_resources(document)
        _assert_text_and_geometry_fit(document)

    before_after = documents["01_before_after.cdxml"]
    assert before_after.root.bond_length == pytest.approx(30.0)
    page = before_after.pages[0]
    assert len(page.fragments) == 2
    before, after = page.fragments
    assert [node.element for node in before.nodes] == [6, 6]
    assert [node.element for node in after.nodes] == [6, 6, 8]
    assert [bond.order for bond in before.bonds] == [BondOrder.SINGLE]
    assert [bond.order for bond in after.bonds] == [BondOrder.DOUBLE, BondOrder.SINGLE]
    assert before.bonds[0].begin is before.nodes[0]
    assert before.bonds[0].end is before.nodes[1]
    assert after.bonds[0].begin is after.nodes[0]
    assert after.bonds[0].end is after.nodes[1]
    assert after.bonds[1].begin is after.nodes[1]
    assert after.bonds[1].end is after.nodes[2]
    visible_text = {run.content for run in before_after.find(TextRun)}
    assert {"BEFORE", "AFTER", "O added; bond order changed"} <= visible_text
    _assert_bonds_resolve(before_after)

    reaction = documents["02_reaction_and_resources.cdxml"]
    reaction_page = reaction.pages[0]
    assert len(reaction_page.fragments) == 2
    assert [bond.order for bond in reaction_page.fragments[0].bonds] == [BondOrder.SINGLE]
    assert [bond.order for bond in reaction_page.fragments[1].bonds] == [BondOrder.DOUBLE]
    assert not reaction.find(Spectrum)
    assert all(node.element_list is None for node in reaction.find(Node))
    assert all(node.generic_list is None for node in reaction.find(Node))
    assert len(reaction.find(ReactionScheme)) == 1
    step = reaction_page.schemes[0].steps[0]
    assert step.reactants == (reaction_page.fragments[0],)
    assert step.products == (reaction_page.fragments[1],)
    assert step.arrows == (reaction_page.arrows[0],)
    _assert_bonds_resolve(reaction)

    preservation_bytes = samples["03_unknown_preservation.cdxml"]
    preservation = documents["03_unknown_preservation.cdxml"]
    node = preservation.find(Node)[1]
    assert node.raw_attributes["VendorNode"] == "retained"
    assert b"urn:cdxml-om:render-samples:preservation" in preservation_bytes
    assert b"<!ENTITY" not in preservation_bytes
    assert b"file://" not in preservation_bytes
    assert b"/tmp/" not in preservation_bytes
    assert b"sentinel" not in preservation_bytes
    roundtrip = CDXMLDocument.from_string(preservation.to_string())
    unknown = roundtrip.find(UnknownElement)
    assert len(unknown) == 1
    assert unknown[0].raw_attributes["purpose"] == "preservation-probe"
    assert unknown[0].text == "Opaque extension; not a ChemDraw display claim"
    _assert_bonds_resolve(preservation)


def test_codec_probes_are_isolated_and_spectrum_pair_differs_only_by_target_fields(
    generated_samples: tuple[dict[str, bytes], dict[str, bytes], dict[str, bytes]],
) -> None:
    samples, _, _ = generated_samples
    curve_document = _document(samples, "probe_curve_points.cdxml")
    curves = curve_document.find(Curve)
    assert len(curves) == 1
    assert curves[0].curve_points == (
        Point2D(250.0, 306.14),
        Point2D(250.0, 289.3),
        Point2D(250.0, 272.46),
        Point2D(275.26, 250.0),
        Point2D(291.16, 255.62),
        Point2D(299.58, 257.48),
        Point2D(310.82, 262.16),
        Point2D(320.18, 264.04),
        Point2D(329.52, 265.9),
    )
    assert curves[0].curve_points3_d is None
    assert "CurvePoints3D" not in curves[0].raw_attributes
    assert curves[0].bounding_box == BoundingBox(250.0, 250.0, 329.52, 306.14)
    assert curves[0].closed is False
    assert curve_document.pages[0].curves[0] is curves[0]
    assert not curve_document.pages[0].fragments
    curve_id = curves[0].id
    assert curve_id is not None
    reloaded_document = CDXMLDocument.from_string(curve_document.to_string())
    reloaded_curve = reloaded_document.find(Curve)[0]
    assert reloaded_curve.curve_points == curves[0].curve_points
    assert reloaded_curve.curve_points3_d is None
    assert "CurvePoints3D" not in reloaded_curve.raw_attributes
    assert reloaded_curve.bounding_box == curves[0].bounding_box
    assert reloaded_curve.closed is False
    assert reloaded_curve.id == curve_id
    assert reloaded_document.get(Curve, curve_id) is reloaded_curve
    assert not curve_document.find(Node)
    assert not curve_document.find(Bond)
    assert not curve_document.find(Spectrum)

    list_document = _document(samples, "probe_element_generic_lists.cdxml")
    nodes = list_document.find(Node)
    assert len(nodes) == 2
    assert nodes[0].element_list is not None
    assert nodes[0].element_list.elements == (6, 8)
    assert nodes[0].element_list.negated
    assert nodes[1].generic_list == GenericList(values=("alpha", "beta"))
    assert len(list_document.find(Bond)) == 1
    assert not list_document.find(Curve)
    assert not list_document.find(Spectrum)

    missing_xml = etree.fromstring(samples["probe_spectrum_missing_required_fields.cdxml"])
    sdk_xml = etree.fromstring(samples["probe_spectrum_sdk_required_fields.cdxml"])
    missing_spectrum = missing_xml.find(".//spectrum")
    sdk_spectrum = sdk_xml.find(".//spectrum")
    assert missing_spectrum is not None and sdk_spectrum is not None
    assert (
        "BoundingBox" not in missing_spectrum.attrib and "XSpacing" not in missing_spectrum.attrib
    )
    assert sdk_spectrum.attrib["BoundingBox"]
    assert float(sdk_spectrum.attrib["XSpacing"]) == pytest.approx(1.0)
    sdk_spectrum.attrib.pop("BoundingBox")
    sdk_spectrum.attrib.pop("XSpacing")
    assert etree.tostring(missing_xml, method="c14n", with_comments=True) == etree.tostring(
        sdk_xml, method="c14n", with_comments=True
    )

    missing = _document(samples, "probe_spectrum_missing_required_fields.cdxml")
    sdk = _document(samples, "probe_spectrum_sdk_required_fields.cdxml")
    assert missing.find(Spectrum)[0].data == "400 0.2 500 0.5"
    assert sdk.find(Spectrum)[0].data == "400 0.2 500 0.5"


def test_generation_is_deterministic_and_fresh_export_reuses_collected_bytes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    generated_samples: tuple[dict[str, bytes], dict[str, bytes], dict[str, bytes]],
) -> None:
    samples, protected_before, protected_after = generated_samples
    assert protected_before == protected_after

    before_repeat = _protected_inputs()
    repeated = visual_samples.collect_visual_samples()
    assert repeated == samples
    assert _protected_inputs() == before_repeat

    monkeypatch.setattr(visual_samples, "collect_visual_samples", lambda: samples)
    output_dir = tmp_path / "fresh-visual-samples"
    output_paths = visual_samples.export_visual_samples(output_dir)
    assert tuple(path.name for path in output_paths) == SAMPLE_NAMES
    assert {path.name: path.read_bytes() for path in output_paths} == samples
    assert {path.name for path in output_dir.glob("*.cdxml")} == set(SAMPLE_NAMES)

    keep = output_dir / "keep.txt"
    keep.write_text("unmanaged", encoding="utf-8")
    for name in SAMPLE_NAMES:
        (output_dir / name).write_bytes(b"stale sample")
    updated_paths = visual_samples.export_visual_samples(output_dir, update=True)
    assert tuple(path.name for path in updated_paths) == SAMPLE_NAMES
    assert {path.name: path.read_bytes() for path in updated_paths} == samples
    assert keep.read_text(encoding="utf-8") == "unmanaged"


def test_generator_refuses_existing_outputs_before_collecting(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    before = _committed_samples()
    protected_before = _protected_inputs()

    def unexpected_collection() -> dict[str, bytes]:
        pytest.fail("existing outputs must be rejected before generation")

    monkeypatch.setattr(visual_samples, "collect_visual_samples", unexpected_collection)
    with pytest.raises(visual_samples.VisualSampleError, match="refusing to overwrite"):
        visual_samples.export_visual_samples(SAMPLE_DIR)
    for source_directory in (NOTEBOOK_DIR, CORPUS_DIR):
        with pytest.raises(visual_samples.VisualSampleError, match="source inputs"):
            visual_samples.export_visual_samples(source_directory, update=True)
    assert _committed_samples() == before
    assert _protected_inputs() == protected_before


def test_bilingual_entry_points_link_to_the_current_guide_and_samples() -> None:
    entries = (
        (
            ROOT / "README.md",
            ROOT / "docs" / "examples.md",
            SAMPLE_DIR / "README.md",
            SAMPLE_DIR / "README.zh-CN.md",
        ),
        (
            ROOT / "README.zh-CN.md",
            ROOT / "docs" / "zh-CN" / "examples.md",
            SAMPLE_DIR / "README.zh-CN.md",
            SAMPLE_DIR / "README.md",
        ),
    )
    for readme, docs_entry, guide, counterpart in entries:
        assert docs_entry.resolve() in _local_links(readme)
        assert guide.resolve() in _local_links(docs_entry)
        assert counterpart.resolve() in _local_links(guide)
        guide_links = _local_links(guide)
        for filename in SAMPLE_NAMES:
            assert (SAMPLE_DIR / filename).resolve() in guide_links


def test_sample_docs_and_generator_have_no_generation_version_labels() -> None:
    sample_docs = (
        SAMPLE_DIR / "README.md",
        SAMPLE_DIR / "README.zh-CN.md",
        ROOT / "docs" / "examples.md",
        ROOT / "docs" / "zh-CN" / "examples.md",
        ROOT / "docs" / "compatibility.md",
        ROOT / "docs" / "zh-CN" / "compatibility.md",
    )
    for path in sample_docs:
        contents = path.read_text(encoding="utf-8").lower()
        assert "render_samples_v2" not in contents
        assert "build_visual_samples_v2" not in contents
        assert "export_render_samples" not in contents
        assert "probe_spectrum_v1_fields" not in contents
        assert not re.search(r"\bv[12]\b", contents)

    for path in (SAMPLE_DIR / "README.md", SAMPLE_DIR / "README.zh-CN.md"):
        contents = path.read_text(encoding="utf-8")
        assert PREVIOUS_CURVE_PROBE_SHA256 in contents
        assert "d1985caaa79f6f5d803966a5f4bed69e0c6ef2bc" in contents
        assert "25.5.0.5789" in contents
        assert "pending user retest" in contents or "等待用户复验" in contents

    generator = (ROOT / "tools" / "build_visual_samples.py").read_text(encoding="utf-8")
    assert "render-samples:v2" not in generator
    assert "probe_spectrum_v1_fields" not in generator
