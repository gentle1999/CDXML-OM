"""Build CDXML visual samples and isolated codec probes."""

from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path

from lxml import etree

from cdxml_om import (
    Arrow,
    ArrowheadSide,
    ArrowheadType,
    BondOrder,
    BoundingBox,
    CDXMLDocument,
    ElementList,
    Fragment,
    GenericList,
    GraphicType,
    Node,
    Page,
    Point2D,
    Point3D,
    SpectrumClass,
    SpectrumXType,
    SpectrumYType,
    Text,
    UnknownElement,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = PROJECT_ROOT / "tests" / "fixtures" / "corpus" / "mol1.cdxml"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "examples" / "render_samples"
SAMPLE_NAMES = (
    "01_before_after.cdxml",
    "02_reaction_and_resources.cdxml",
    "03_unknown_preservation.cdxml",
    "probe_curve_points.cdxml",
    "probe_element_generic_lists.cdxml",
    "probe_spectrum_missing_required_fields.cdxml",
    "probe_spectrum_sdk_required_fields.cdxml",
)
_VENDOR_NS = "urn:cdxml-om:render-samples:preservation"


class VisualSampleError(RuntimeError):
    """Raised when a sample cannot be validated or safely written."""


def _styled_page(bounds: BoundingBox) -> tuple[CDXMLDocument, Page]:
    """Reuse accepted mol1 document styles, replacing only its page content."""
    document = CDXMLDocument.from_file(SOURCE_PATH)
    root = document.root
    for page in tuple(document.pages):
        document.pages.remove(page)

    root.creation_program = None
    root.creation_user_name = None
    root.creation_date = None
    root.modification_program = None
    root.modification_user_name = None
    root.modification_date = None
    root.name = None
    root.bounding_box = None
    root.window_position = None
    root.window_size = None
    root.window_is_zoomed = False
    root.mac_print_info = None
    root.win_print_info = None
    root.print_margins = None
    root.bond_length = 30.0
    root.label_font = 3
    root.label_size = 10.0
    root.caption_font = 4
    root.caption_size = 12.0

    font_table = document.font_table
    color_table = document.color_table
    if font_table is None or color_table is None:
        raise VisualSampleError("mol1 style source must contain font and color tables")
    fonts = {font.name: font.id for font in font_table.fonts}
    if fonts.get("Arial") != 3 or fonts.get("Times New Roman") != 4:
        raise VisualSampleError("mol1 font IDs no longer match the documented style baseline")
    if len(color_table.colors) < 4:
        raise VisualSampleError("mol1 color table no longer contains the standard palette")

    page = document.pages.create()
    page.bounding_box = bounds
    page.width_pages = 1
    page.height_pages = 1
    return document, page


def _add_heading(page: Page, content: str, x: float, y: float) -> Text:
    return _add_page_text(page, content, x, y, size=16.0, face=1, z=5)


def _add_page_text(
    page: Page,
    content: str,
    x: float,
    y: float,
    *,
    size: float = 10.0,
    face: int | None = None,
    z: int | None = None,
) -> Text:
    text = page.texts.create(position=Point2D(x, y), z=z)
    text.runs.create(content=content, font_id=3, size=size, face=face, color=3)
    return text


def _add_node_label(node: Node, content: str, x: float, y: float) -> Text:
    text = node.texts.create(position=Point2D(x - 3.0, y - 6.0))
    text.runs.create(content=content, font_id=3, size=10.0, color=3)
    return text


def _add_atom(fragment: Fragment, element: int, x: float, y: float, label: str) -> Node:
    node = fragment.nodes.create(element=element, position=Point2D(x, y))
    _add_node_label(node, label, x, y)
    return node


def _add_arrow(page: Page, tail_x: float, head_x: float, y: float) -> Arrow:
    return page.arrows.create(
        tail_3d=Point3D(tail_x, y, 0.0),
        head_3d=Point3D(head_x, y, 0.0),
        arrowhead_type=ArrowheadType.SOLID,
        arrowhead_head=ArrowheadSide.FULL,
    )


def _validated_bytes(document: CDXMLDocument, name: str) -> bytes:
    report = document.validate()
    if not report.is_valid:
        details = ", ".join(
            f"{issue.code}:{issue.property_id or 'structure'}" for issue in report.errors
        )
        raise VisualSampleError(f"{name} failed current structural validation: {details}")
    return document.to_string(encoding="UTF-8", xml_declaration=True, pretty_print=True).encode(
        "utf-8"
    )


def _build_before_after() -> bytes:
    document, page = _styled_page(BoundingBox(100.0, 205.0, 490.0, 330.0))
    _add_heading(page, "BEFORE", 132.0, 225.0)
    _add_heading(page, "AFTER", 304.0, 225.0)
    _add_page_text(page, "O added; bond order changed", 304.0, 247.0, size=10.0)

    before = page.fragments.create()
    before_a = _add_atom(before, 6, 137.0, 276.0, "C")
    before_b = _add_atom(before, 6, 167.0, 276.0, "C")
    before.bonds.create(begin=before_a, end=before_b, order=BondOrder.SINGLE)

    _add_arrow(page, 208.0, 270.0, 276.0)

    after = page.fragments.create()
    after_a = _add_atom(after, 6, 310.0, 276.0, "C")
    after_b = _add_atom(after, 6, 340.0, 276.0, "C")
    edited_bond = after.bonds.create(begin=after_a, end=after_b, order=BondOrder.SINGLE)
    edited_bond.order = BondOrder.DOUBLE
    added_oxygen = after.nodes.create(element=6, position=Point2D(370.0, 276.0))
    added_oxygen.element = 8
    _add_node_label(added_oxygen, "O", 370.0, 276.0)
    after.bonds.create(begin=after_b, end=added_oxygen, order=BondOrder.SINGLE)

    return _validated_bytes(document, "01_before_after.cdxml")


def _build_reaction_and_resources() -> bytes:
    document, page = _styled_page(BoundingBox(100.0, 190.0, 560.0, 360.0))
    heading = _add_heading(page, "RICH TEXT + REACTION  /  ", 126.0, 210.0)
    heading.runs.create(content="Arial + Times New Roman", font_id=4, size=13.0, face=2, color=4)

    reactant = page.fragments.create()
    reactant_a = _add_atom(reactant, 6, 150.0, 267.0, "C")
    reactant_b = _add_atom(reactant, 6, 180.0, 267.0, "C")
    reactant.bonds.create(begin=reactant_a, end=reactant_b, order=BondOrder.SINGLE)

    arrow = _add_arrow(page, 260.0, 325.0, 267.0)

    product = page.fragments.create()
    product_a = _add_atom(product, 6, 390.0, 267.0, "C")
    product_b = _add_atom(product, 6, 420.0, 267.0, "C")
    product.bonds.create(begin=product_a, end=product_b, order=BondOrder.DOUBLE)

    scheme = page.schemes.create()
    step = scheme.steps.create()
    step.reactants = (reactant,)
    step.products = (product,)
    step.arrows = (arrow,)

    page.graphics.create(
        graphic_type=GraphicType.RECTANGLE,
        bounding_box=BoundingBox(122.0, 305.0, 540.0, 342.0),
    )
    _add_page_text(
        page,
        "Font table: Arial + Times New Roman | color index 3 black, 4 red",
        138.0,
        317.0,
        size=10.0,
        z=6,
    )
    return _validated_bytes(document, "02_reaction_and_resources.cdxml")


def _build_unknown_preservation() -> bytes:
    document, page = _styled_page(BoundingBox(100.0, 200.0, 460.0, 330.0))
    _add_heading(page, "UNKNOWN CONTENT RETENTION", 120.0, 230.0)
    fragment = page.fragments.create()
    carbon = _add_atom(fragment, 6, 248.0, 276.0, "C")
    oxygen = _add_atom(fragment, 8, 278.0, 276.0, "O")
    fragment.bonds.create(begin=carbon, end=oxygen, order=BondOrder.SINGLE)
    oxygen.raw_element.set("VendorNode", "retained")
    extension = etree.SubElement(fragment.raw_element, f"{{{_VENDOR_NS}}}note")
    extension.set("purpose", "preservation-probe")
    extension.text = "Opaque extension; not a ChemDraw display claim"
    if not document.find(UnknownElement):
        raise VisualSampleError("unknown preservation sample lost its vendor element")
    return _validated_bytes(document, "03_unknown_preservation.cdxml")


def _build_curve_probe() -> bytes:
    document, page = _styled_page(BoundingBox(100.0, 190.0, 560.0, 360.0))
    _add_heading(page, "CurvePoints coordinate-array probe", 120.0, 220.0)
    # Point order is based on curve id 80755 in this pinned RDKit specimen;
    # only its 2D point sequence is translated/scaled into this page:
    # https://github.com/rdkit/rdkit/blob/d1985caaa79f6f5d803966a5f4bed69e0c6ef2bc/Code/GraphMol/test_data/CDXML/chemdraw_template5.cdxml
    page.curves.create(
        closed=False,
        curve_points=(
            Point2D(250.0, 306.14),
            Point2D(250.0, 289.30),
            Point2D(250.0, 272.46),
            Point2D(275.26, 250.0),
            Point2D(291.16, 255.62),
            Point2D(299.58, 257.48),
            Point2D(310.82, 262.16),
            Point2D(320.18, 264.04),
            Point2D(329.52, 265.90),
        ),
        bounding_box=BoundingBox(250.0, 250.0, 329.52, 306.14),
        color=3,
        z=6,
    )
    return _validated_bytes(document, "probe_curve_points.cdxml")


def _build_list_probe() -> bytes:
    document, page = _styled_page(BoundingBox(100.0, 190.0, 560.0, 360.0))
    _add_heading(page, "ElementList + GenericList probe", 120.0, 220.0)
    fragment = page.fragments.create()
    carbon = _add_atom(fragment, 6, 220.0, 278.0, "C")
    oxygen = _add_atom(fragment, 8, 250.0, 278.0, "O")
    fragment.bonds.create(begin=carbon, end=oxygen, order=BondOrder.SINGLE)
    carbon.element_list = ElementList(elements=(6, 8), negated=True)
    oxygen.generic_list = GenericList(values=("alpha", "beta"))
    return _validated_bytes(document, "probe_element_generic_lists.cdxml")


def _build_spectrum_probe(*, include_sdk_required_fields: bool) -> bytes:
    document, page = _styled_page(BoundingBox(100.0, 190.0, 560.0, 360.0))
    _add_heading(page, "Spectrum lexical payload differential", 120.0, 220.0)
    spectrum_values: dict[str, object] = {
        "class_name": SpectrumClass.UNKNOWN,
        "x_type": SpectrumXType.OTHER,
        "y_type": SpectrumYType.OTHER,
        "x_low": 0.0,
        "y_low": 0.0,
        "y_scale": 1.0,
        "data": "400 0.2 500 0.5",
    }
    if include_sdk_required_fields:
        spectrum_values["bounding_box"] = BoundingBox(160.0, 250.0, 500.0, 315.0)
        spectrum_values["x_spacing"] = 1.0
    spectrum = page.spectrums.create(**spectrum_values)
    spectrum.annotations.create(content="Same unverified lexical payload in both probes")
    output_name = (
        "probe_spectrum_sdk_required_fields.cdxml"
        if include_sdk_required_fields
        else "probe_spectrum_missing_required_fields.cdxml"
    )
    return _validated_bytes(document, output_name)


def collect_visual_samples() -> dict[str, bytes]:
    """Create three readable scenes and four deliberately narrow probes."""
    samples = {
        SAMPLE_NAMES[0]: _build_before_after(),
        SAMPLE_NAMES[1]: _build_reaction_and_resources(),
        SAMPLE_NAMES[2]: _build_unknown_preservation(),
        SAMPLE_NAMES[3]: _build_curve_probe(),
        SAMPLE_NAMES[4]: _build_list_probe(),
        SAMPLE_NAMES[5]: _build_spectrum_probe(include_sdk_required_fields=False),
        SAMPLE_NAMES[6]: _build_spectrum_probe(include_sdk_required_fields=True),
    }
    return samples


def _preflight(output_dir: Path, *, update: bool) -> Path:
    if output_dir.is_symlink():
        raise VisualSampleError("refusing a symlink output directory")
    resolved = output_dir.resolve()
    if output_dir.exists() and not output_dir.is_dir():
        raise VisualSampleError(f"output path is not a directory: {output_dir}")
    protected = (SOURCE_PATH.parent.resolve(), (PROJECT_ROOT / "examples" / "notebooks").resolve())
    if any(resolved == path or path in resolved.parents for path in protected):
        raise VisualSampleError("choose an output directory outside source inputs")
    linked = [name for name in SAMPLE_NAMES if (resolved / name).is_symlink()]
    if linked:
        raise VisualSampleError("refusing symlink targets: " + ", ".join(linked))
    existing = [name for name in SAMPLE_NAMES if (resolved / name).exists()]
    if existing and not update:
        raise VisualSampleError("refusing to overwrite: " + ", ".join(existing))
    return resolved


def export_visual_samples(
    output_dir: Path = DEFAULT_OUTPUT_DIR, *, update: bool = False
) -> tuple[Path, ...]:
    """Build all bytes, then write or explicitly replace managed output files."""
    resolved = _preflight(output_dir, update=update)
    samples = collect_visual_samples()
    if tuple(samples) != SAMPLE_NAMES:
        raise VisualSampleError("visual sample inventory is inconsistent")
    resolved.mkdir(parents=True, exist_ok=True)
    if update:
        with tempfile.TemporaryDirectory(prefix=".visual-samples-stage-", dir=resolved) as stage:
            staged = Path(stage)
            for name, data in samples.items():
                (staged / name).write_bytes(data)
            for name in SAMPLE_NAMES:
                os.replace(staged / name, resolved / name)
        return tuple(resolved / name for name in SAMPLE_NAMES)

    written: list[Path] = []
    try:
        for name, data in samples.items():
            destination = resolved / name
            with destination.open("xb") as stream:
                written.append(destination)
                stream.write(data)
    except OSError as exc:
        for destination in written:
            destination.unlink(missing_ok=True)
        raise VisualSampleError(f"could not write visual samples: {exc}") from exc
    return tuple(resolved / name for name in SAMPLE_NAMES)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="new or existing directory for the scenes and probes",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="replace this tool's known sample filenames after building all output bytes",
    )
    args = parser.parse_args(argv)
    try:
        paths = export_visual_samples(args.output_dir, update=args.update)
    except (VisualSampleError, OSError) as exc:
        print(f"Visual sample build failed: {exc}", file=sys.stderr)
        return 1
    for path in paths:
        print(path)
    print("User-reported observations and pending retests are recorded in the sample guide.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
