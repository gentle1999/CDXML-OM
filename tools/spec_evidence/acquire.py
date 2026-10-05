"""Acquire pinned SDK snapshots and emit a factual CDXML evidence catalog.

This is an explicit development tool. It is not imported by runtime code and
does not fetch sources unless invoked. The output contains extracted facts,
locators, and source digests; archived SDK HTML is not copied into the repo.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path
from typing import TypedDict, cast
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from lxml import html

from tools.schema_importer.candidate import CandidateDocument, SDKEntryCandidate
from tools.schema_importer.common import PROJECT_ROOT, write_text_output
from tools.schema_importer.dtd_importer import import_dtd
from tools.schema_importer.errors import ImporterError
from tools.schema_importer.sdk_importer import import_sdk_html

_ARCHIVE_ROOT = "https://web.archive.org/web"
_ORIGINAL_ROOT = "http://www.cambridgesoft.com:80/services/documentation/sdk/chemdraw/cdx"
_INDEX_CAPTURE = "20100502023312"
_NEAREST_CAPTURE = "20100502000000"
_INVENTORY_URL = f"{_ORIGINAL_ROOT}/AllCDXObjects.htm"
_OBJECT_ID_URL = f"{_ORIGINAL_ROOT}/DataType/CDXObjectID.htm"
_DTD_PATH = Path("schema/sources/revvity-CDXML.dtd")
_BASE_EVIDENCE_PATH = Path("schema/sources/sdk/evidence.json")


class EvidenceAcquisitionError(RuntimeError):
    """A pinned evidence source could not be retrieved or parsed."""


class SourceRecord(TypedDict):
    id: str
    original_url: str
    snapshot_url: str | None
    captured_at: str | None
    retrieved_at: str
    sha256: str
    bytes: int
    snapshot_kind: str
    redistribution: str


class PinRecord(TypedDict, total=False):
    snapshot_url: str
    sha256: str


class EvidenceRef(TypedDict):
    source_id: str
    locator: str


class SDKFact(TypedDict):
    namespace: str
    relation: str
    display_name: str | None
    value_text: str | None
    cdx_id: int | None
    cdx_constant: str | None
    xml_name: str | None
    sdk_type: str | None
    owner_xml_name: str | None
    locator: str


class SDKMatch(TypedDict):
    cdx_id: int | None
    cdx_constant: str | None
    sdk_type: str | None
    value_text: str | None
    source: EvidenceRef


class SDKNameMatch(TypedDict):
    xml_name: str
    cdx_id: int | None
    cdx_constant: str | None
    sdk_type: str | None
    source: EvidenceRef


class OwnerAttributePair(TypedDict):
    owner_xml_name: str
    xml_name: str
    dtd_type: str
    required: bool
    default_kind: str
    default_value: str | None
    enum_values: list[str]
    dtd_source: EvidenceRef
    sdk_mapping_status: str
    sdk_matches: list[SDKMatch]
    sdk_case_variant_matches: list[SDKNameMatch]
    reference_target: str | None


class SDKOnlyProperty(TypedDict):
    owner_xml_name: str
    xml_name: str
    classification: str
    sdk_facts: list[SDKMatch]


class CDXObjectIDFact(TypedDict):
    datatype: str
    underlying_binary_type: str
    xml_example: str
    id_resolution_statement: str
    locator: str


class FocusedSourceSpec(TypedDict):
    id: str
    path: str
    capture: str


_FOCUSED_SOURCE_SPECS: tuple[FocusedSourceSpec, ...] = (
    {
        "id": "sdk_bond_order",
        "path": "properties/Bond_Order.htm",
        "capture": "20160913174134",
    },
    {
        "id": "sdk_label_style_size",
        "path": "properties/LabelStyleSize.htm",
        "capture": "20190326232657",
    },
    {
        "id": "sdk_caption_style_size",
        "path": "properties/CaptionStyleSize.htm",
        "capture": "20190326232725",
    },
    {
        "id": "sdk_rotation_angle",
        "path": "properties/RotationAngle.htm",
        "capture": "20190121160337",
    },
    {
        "id": "sdk_date_and_time",
        "path": "DataType/DateAndTime.htm",
        "capture": "20100503174608",
    },
    {
        "id": "sdk_int16_list_with_counts",
        "path": "DataType/INT16ListWithCounts.htm",
        "capture": "20100503142223",
    },
    {
        "id": "sdk_generic_list",
        "path": "DataType/CDXGenericList.htm",
        "capture": "20100503174307",
    },
    {
        "id": "sdk_element_list",
        "path": "DataType/CDXElementList.htm",
        "capture": "20100503174256",
    },
    {
        "id": "sdk_formula",
        "path": "DataType/CDXFormula.htm",
        "capture": "20100503174558",
    },
    {
        "id": "sdk_curve_points",
        "path": "DataType/CDXCurvePoints.htm",
        "capture": "20100503174245",
    },
    {
        "id": "sdk_curve_points_3d",
        "path": "DataType/CDXCurvePoints3D.htm",
        "capture": "20100503174250",
    },
    {
        "id": "sdk_curve_points_3d_property",
        "path": "properties/Curve_Points3D.htm",
        "capture": "20190326230613",
    },
    {
        "id": "sdk_node_attachments",
        "path": "properties/Node_Attachments.htm",
        "capture": "20190327221555",
    },
    {
        "id": "sdk_object_tag_value",
        "path": "properties/ObjectTag_Value.htm",
        "capture": "20190326232119",
    },
    {
        "id": "sdk_object_tag_type",
        "path": "properties/ObjectTag_Type.htm",
        "capture": "20190327000022",
    },
    {
        "id": "sdk_unformatted",
        "path": "DataType/Unformatted.htm",
        "capture": "20100503174312",
    },
    {
        "id": "sdk_spectrum_data_point",
        "path": "properties/Spectrum_DataPoint.htm",
        "capture": "20160913174112",
    },
    {
        "id": "sdk_spectrum_y_low",
        "path": "properties/Spectrum_YLow.htm",
        "capture": "20160912170237",
    },
    {
        "id": "sdk_cdx_string",
        "path": "DataType/CDXString.htm",
        "capture": "20100502023322",
    },
    {
        "id": "sdk_cdx_font_table",
        "path": "DataType/CDXFontTable.htm",
        "capture": "20100503174301",
    },
    {
        "id": "sdk_font_table_property",
        "path": "properties/FontTable.htm",
        "capture": "20160911223857",
    },
    {
        "id": "sdk_color_table_property",
        "path": "properties/ColorTable.htm",
        "capture": "20190326231030",
    },
    {
        "id": "sdk_coordinates",
        "path": "DataType/CDXCoordinates.htm",
        "capture": "20100503094142",
    },
    {
        "id": "sdk_geometry_properties",
        "path": "TableOfProperties.htm",
        "capture": "20100503094203",
    },
)


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _fetch_snapshot(
    original_url: str,
    *,
    capture: str,
    pin: PinRecord | None = None,
) -> tuple[bytes, SourceRecord]:
    pinned_url = pin.get("snapshot_url") if pin is not None else None
    requested_url = (
        str(pinned_url)
        if isinstance(pinned_url, str)
        else f"{_ARCHIVE_ROOT}/{capture}id_/{original_url}"
    )
    request = Request(requested_url, headers={"User-Agent": "CDXML-OM-spec-evidence/1"})
    content = b""
    final_url = requested_url
    last_error: Exception | None = None
    memento: str | None = None
    for attempt in range(3):
        try:
            with urlopen(request, timeout=60) as response:
                content = response.read()
                final_url = response.geturl()
                memento = response.headers.get("Memento-Datetime")
            last_error = None
            break
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            last_error = exc
            if attempt < 2:
                time.sleep(0.4 * (attempt + 1))
    else:
        try:
            content, final_url, memento = _curl_snapshot(requested_url)
        except (OSError, subprocess.SubprocessError) as exc:
            raise EvidenceAcquisitionError(
                f"cannot acquire {original_url}: {last_error}; curl fallback: {exc}"
            ) from exc
    if not content:
        raise EvidenceAcquisitionError(f"empty archived response for {original_url}")
    digest = hashlib.sha256(content).hexdigest()
    expected_digest = pin.get("sha256") if pin is not None else None
    if isinstance(expected_digest, str) and digest != expected_digest:
        raise EvidenceAcquisitionError(
            f"pinned SDK snapshot hash mismatch for {original_url}: "
            f"expected {expected_digest}, found {digest}"
        )
    source: SourceRecord = {
        "id": "sdk_objects" if original_url == _INVENTORY_URL else "",
        "original_url": original_url,
        "snapshot_url": final_url,
        "captured_at": memento,
        "retrieved_at": _utc_now(),
        "sha256": digest,
        "bytes": len(content),
        "snapshot_kind": "Internet Archive memento, original HTML bytes",
        "redistribution": "facts extracted; HTML snapshot not redistributed",
    }
    return content, source


def _curl_snapshot(requested_url: str) -> tuple[bytes, str, str | None]:
    """Use curl's retrying transport as a fallback for intermittent Wayback EOFs."""
    with tempfile.TemporaryDirectory(prefix="cdxml-sdk-snapshot-") as temporary:
        directory = Path(temporary)
        content_path = directory / "snapshot.html"
        headers_path = directory / "headers.txt"
        result = subprocess.run(
            [
                "curl",
                "--fail",
                "--location",
                "--silent",
                "--show-error",
                "--retry",
                "5",
                "--retry-all-errors",
                "--retry-delay",
                "1",
                "--dump-header",
                str(headers_path),
                "--output",
                str(content_path),
                "--write-out",
                "%{url_effective}",
                requested_url,
            ],
            capture_output=True,
            check=False,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            raise subprocess.CalledProcessError(
                result.returncode, result.args, result.stdout, result.stderr
            )
        header_text = headers_path.read_text(encoding="latin-1")
        memento_matches = re.findall(r"(?im)^memento-datetime:\s*(.+?)\s*$", header_text)
        return (
            content_path.read_bytes(),
            result.stdout,
            memento_matches[-1] if memento_matches else None,
        )


def _import_bytes(content: bytes, name: str) -> CandidateDocument:
    # The established importer hashes the exact local bytes and applies its
    # external-reference guard before parsing. This temporary file is discarded.
    with tempfile.NamedTemporaryFile(prefix="cdxml-sdk-", suffix=".html") as temporary:
        temporary.write(content)
        temporary.flush()
        try:
            return import_sdk_html(temporary.name)
        except ImporterError as exc:
            raise EvidenceAcquisitionError(f"cannot parse SDK page {name}: {exc}") from exc


def _cell_text(cell: html.HtmlElement) -> str:
    return " ".join(" ".join(cell.itertext()).split())


def _normalized_header(value: str) -> str:
    return " ".join(value.strip().rstrip(":").casefold().split())


def _direct_cells(row: html.HtmlElement) -> list[html.HtmlElement]:
    return [node for node in row.xpath("./th | ./td") if isinstance(node, html.HtmlElement)]


def _direct_rows(table: html.HtmlElement) -> list[html.HtmlElement]:
    rows: list[html.HtmlElement] = []
    for node in table.xpath(".//tr"):
        if not isinstance(node, html.HtmlElement):
            continue
        nearest_table = node.xpath("ancestor::table[1]")
        if nearest_table and nearest_table[0] is table:
            rows.append(node)
    return rows


def _inventory_links(content: bytes) -> dict[str, str]:
    document = html.document_fromstring(
        content, parser=html.HTMLParser(no_network=True, recover=True, default_doctype=False)
    )
    links: dict[str, str] = {}
    for table in document.xpath("//table"):
        if not isinstance(table, html.HtmlElement):
            continue
        rows = _direct_rows(table)
        positions: dict[str, int] | None = None
        for row in rows:
            cells = _direct_cells(row)
            headers = tuple(_normalized_header(_cell_text(cell)) for cell in cells)
            if {"object", "value", "name", "cdxml name"}.issubset(headers):
                positions = {header: index for index, header in enumerate(headers)}
                continue
            if positions is None or len(cells) < len(positions):
                continue
            xml_name = _cell_text(cells[positions["cdxml name"]]).strip()
            if not xml_name:
                continue
            hrefs = cells[positions["object"]].xpath(".//a[1]/@href")
            if hrefs:
                links[xml_name] = hrefs[0]
    return links


def _source_id_for_xml(xml_name: str) -> str:
    if xml_name == "CDXML":
        return "sdk_document"
    normalized = re.sub(r"[^a-z0-9]+", "_", xml_name.casefold()).strip("_")
    return f"sdk_page_{normalized}"


def _entry_fact(entry: SDKEntryCandidate) -> SDKFact:
    return {
        "namespace": entry.namespace,
        "relation": entry.relation,
        "display_name": entry.display_name,
        "value_text": entry.value_text,
        "cdx_id": entry.cdx_id,
        "cdx_constant": entry.cdx_constant,
        "xml_name": entry.xml_name,
        "sdk_type": entry.type_name,
        "owner_xml_name": entry.owner_xml_name,
        "locator": entry.locator,
    }


def _source_ref(source_id: str, locator: str) -> EvidenceRef:
    return {"source_id": source_id, "locator": locator}


def _parse_object_id_fact(content: bytes) -> CDXObjectIDFact:
    document = html.document_fromstring(
        content, parser=html.HTMLParser(no_network=True, recover=True, default_doctype=False)
    )
    text = " ".join(" ".join(document.itertext()).split())
    if "CDXObjectID" not in text or "UINT32" not in text:
        raise EvidenceAcquisitionError("CDXObjectID source no longer states UINT32")
    if "unique within a CDX/CDXML file" not in text:
        raise EvidenceAcquisitionError("CDXObjectID source no longer states file-level uniqueness")
    return {
        "datatype": "CDXObjectID",
        "underlying_binary_type": "UINT32",
        "xml_example": '"1 2 3 4"',
        "id_resolution_statement": (
            "IDs should be unique within a CDX/CDXML file; if ambiguous, the reference "
            "resolves to the closest object with that ID."
        ),
        "locator": "CDXObjectID section; CDXML example",
    }


def _load_pins(path: Path | None) -> dict[str, PinRecord]:
    if path is None:
        return {}
    try:
        payload: object = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceAcquisitionError(f"cannot read pinned source catalog {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise EvidenceAcquisitionError("pinned source catalog root must be an object")
    payload_mapping = cast(dict[str, object], payload)
    sources_value = payload_mapping.get("sources")
    if not isinstance(sources_value, list):
        raise EvidenceAcquisitionError("pinned source catalog has no sources array")
    sources = cast(list[object], sources_value)
    pins: dict[str, PinRecord] = {}
    for source in sources:
        if not isinstance(source, dict):
            continue
        record = cast(dict[str, object], source)
        original = record.get("original_url")
        snapshot_url = record.get("snapshot_url")
        sha256 = record.get("sha256")
        if isinstance(original, str) and isinstance(snapshot_url, str) and isinstance(sha256, str):
            pins[original.replace(":80", "")] = {
                "snapshot_url": snapshot_url,
                "sha256": sha256,
            }
    return pins


def build_evidence(pins: dict[str, PinRecord] | None = None) -> dict[str, object]:
    pin_registry = pins or {}
    retrieved_at = _utc_now()
    dtd_path = PROJECT_ROOT / _DTD_PATH
    dtd_candidate = import_dtd(str(dtd_path))

    inventory_bytes, inventory_source = _fetch_snapshot(
        _INVENTORY_URL,
        capture=_INDEX_CAPTURE,
        pin=pin_registry.get(_INVENTORY_URL.replace(":80", "")),
    )
    inventory_candidate = _import_bytes(inventory_bytes, "AllCDXObjects.htm")
    if inventory_candidate.scope != "inventory":
        raise EvidenceAcquisitionError("AllCDXObjects snapshot was not recognized as inventory")
    links = _inventory_links(inventory_bytes)
    inventory_entries = [
        entry for entry in inventory_candidate.sdk_entries if entry.relation == "inventory"
    ]
    if len(inventory_entries) != 38:
        raise EvidenceAcquisitionError(
            f"expected 38 SDK inventory entries, found {len(inventory_entries)}"
        )

    original_urls: dict[str, str] = {}
    detail_unavailable: dict[str, str] = {}
    for entry in inventory_entries:
        assert entry.xml_name is not None
        href = links.get(entry.xml_name)
        if href is None:
            detail_unavailable[entry.xml_name] = "AllCDXObjects has no page link for this entry."
            continue
        if href.startswith(("http:", "https:")) or ".." in Path(href).parts:
            raise EvidenceAcquisitionError(f"unexpected SDK object-page link {href!r}")
        if entry.xml_name == "arrow":
            detail_unavailable[entry.xml_name] = (
                "AllCDXObjects links Arrow.htm, but the archived page returned 404."
            )
            continue
        original_urls[entry.xml_name] = f"{_ORIGINAL_ROOT}/{href}"
    original_urls["__cdx_object_id_datatype__"] = _OBJECT_ID_URL

    downloaded: dict[str, tuple[bytes, SourceRecord]] = {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {
            pool.submit(
                _fetch_snapshot,
                url,
                capture=_NEAREST_CAPTURE,
                pin=pin_registry.get(url.replace(":80", "")),
            ): key
            for key, url in original_urls.items()
        }
        for future in as_completed(futures):
            key = futures[future]
            downloaded[key] = future.result()

    dtd_sha256 = dtd_candidate.source.sha256
    source_records: list[SourceRecord] = [
        {
            "id": "revvity_dtd",
            "original_url": "https://static.chemistry.revvitycloud.com/cdxml/CDXML.dtd",
            "snapshot_url": None,
            "captured_at": None,
            "retrieved_at": "2026-10-04",
            "sha256": dtd_sha256,
            "bytes": dtd_path.stat().st_size,
            "snapshot_kind": "checked-in primary DTD snapshot; internal header revision 48",
            "redistribution": "source is checked in at schema/sources/revvity-CDXML.dtd",
        }
    ]
    inventory_source["id"] = "sdk_objects"
    inventory_source["original_url"] = _INVENTORY_URL.replace(":80", "")
    source_records.append(inventory_source)

    page_entries_by_tag: dict[str, list[SDKFact]] = defaultdict(list)
    page_subobjects_by_tag: dict[str, list[SDKFact]] = defaultdict(list)
    page_sources: dict[str, SourceRecord] = {}
    for entry in inventory_entries:
        assert entry.xml_name is not None
        if entry.xml_name not in downloaded:
            continue
        raw, source = downloaded[entry.xml_name]
        source_id = _source_id_for_xml(entry.xml_name)
        source["id"] = source_id
        source["original_url"] = original_urls[entry.xml_name].replace(":80", "")
        page_sources[source_id] = source
        candidate = _import_bytes(raw, entry.xml_name)
        for item in candidate.sdk_entries:
            if item.relation == "property" and item.owner_xml_name:
                page_entries_by_tag[item.owner_xml_name].append(_entry_fact(item))
            elif item.relation == "subobject" and item.owner_xml_name:
                page_subobjects_by_tag[item.owner_xml_name].append(_entry_fact(item))
    source_records.extend(page_sources.values())

    object_id_bytes, object_id_source = downloaded["__cdx_object_id_datatype__"]
    object_id_source["id"] = "sdk_object_id"
    object_id_source["original_url"] = _OBJECT_ID_URL.replace(":80", "")
    source_records.append(object_id_source)
    object_id_fact: CDXObjectIDFact = _parse_object_id_fact(object_id_bytes)

    dtd_elements = {element.xml_name: element for element in dtd_candidate.dtd_elements}
    parents_by_tag: dict[str, list[str]] = defaultdict(list)
    for parent in dtd_candidate.dtd_elements:
        for child in parent.children:
            parents_by_tag[child].append(parent.xml_name)
    sdk_by_tag = {
        entry.xml_name: entry for entry in inventory_entries if entry.xml_name is not None
    }
    elements: list[dict[str, object]] = []
    for element in dtd_candidate.dtd_elements:
        sdk_entry = sdk_by_tag.get(element.xml_name)
        if sdk_entry is None:
            mapping: dict[str, object] | None = None
        else:
            mapping = {
                "namespace": sdk_entry.namespace,
                "display_name": sdk_entry.display_name,
                "cdx_id": sdk_entry.cdx_id,
                "cdx_constant": sdk_entry.cdx_constant,
                "inventory_locator": sdk_entry.locator,
                "inventory_source_id": "sdk_objects",
                "detail_source_id": (
                    _source_id_for_xml(element.xml_name)
                    if element.xml_name in page_sources
                    else None
                ),
                "detail_status": detail_unavailable.get(element.xml_name, "captured"),
            }
        elements.append(
            {
                "xml_name": element.xml_name,
                "declaration": element.locator,
                "dtd_children": list(element.children),
                "dtd_parent_xml_names": parents_by_tag.get(element.xml_name, []),
                "attributes": len(element.attributes),
                "sdk_mapping": mapping,
                "sdk_subobject_evidence": page_subobjects_by_tag.get(element.xml_name, []),
            }
        )

    owner_attribute_pairs: list[OwnerAttributePair] = []
    dtd_attr_names: dict[str, set[str]] = {
        name: {attribute.name for attribute in element.attributes}
        for name, element in dtd_elements.items()
    }
    for element in dtd_candidate.dtd_elements:
        sdk_page_source = _source_id_for_xml(element.xml_name)
        sdk_properties = page_entries_by_tag.get(element.xml_name, [])
        properties_by_name: dict[str, list[SDKFact]] = defaultdict(list)
        for property_entry in sdk_properties:
            xml_name = property_entry.get("xml_name")
            if isinstance(xml_name, str):
                properties_by_name[xml_name].append(property_entry)
        for attribute in element.attributes:
            matches = properties_by_name.get(attribute.name, [])
            case_variant_matches = [
                item
                for property_name, entries in properties_by_name.items()
                if property_name.casefold() == attribute.name.casefold()
                and property_name != attribute.name
                for item in entries
            ]
            sdk_matches: list[SDKMatch] = [
                {
                    "cdx_id": item["cdx_id"],
                    "cdx_constant": item["cdx_constant"],
                    "sdk_type": item["sdk_type"],
                    "value_text": item["value_text"],
                    "source": _source_ref(sdk_page_source, str(item.get("locator"))),
                }
                for item in matches
            ]
            sdk_case_variant_matches: list[SDKNameMatch] = [
                {
                    "xml_name": str(item.get("xml_name")),
                    "cdx_id": item["cdx_id"],
                    "cdx_constant": item["cdx_constant"],
                    "sdk_type": item["sdk_type"],
                    "source": _source_ref(sdk_page_source, str(item.get("locator"))),
                }
                for item in case_variant_matches
            ]
            owner_attribute_pairs.append(
                {
                    "owner_xml_name": element.xml_name,
                    "xml_name": attribute.name,
                    "dtd_type": attribute.declared_type,
                    "required": attribute.required,
                    "default_kind": attribute.default_kind,
                    "default_value": attribute.default_value,
                    "enum_values": list(attribute.enum_values),
                    "dtd_source": _source_ref("revvity_dtd", attribute.locator),
                    "sdk_mapping_status": (
                        "matched"
                        if len(matches) == 1
                        else "ambiguous"
                        if matches
                        else "case_variant_only"
                        if sdk_case_variant_matches
                        else "no_exact_sdk_property_entry"
                    ),
                    "sdk_matches": sdk_matches,
                    "sdk_case_variant_matches": sdk_case_variant_matches,
                    "reference_target": None,
                }
            )

    sdk_only_properties: dict[tuple[str, str], SDKOnlyProperty] = {}
    for owner, properties in page_entries_by_tag.items():
        for sdk_fact in properties:
            xml_name = sdk_fact.get("xml_name")
            if not isinstance(xml_name, str) or xml_name in dtd_attr_names.get(owner, set()):
                continue
            dtd_case_matches = [
                candidate
                for candidate in dtd_attr_names.get(owner, set())
                if candidate.casefold() == xml_name.casefold()
            ]
            if xml_name == "(not used)":
                classification = "binary_property_not_used_as_xml_attribute"
            elif owner == "CDXML" and xml_name in {"fonttable", "colortable"}:
                classification = "property_encoded_xml_child_element"
            elif dtd_case_matches:
                classification = "case_variant_of_dtd_xml_attribute"
            else:
                classification = "sdk_documented_xml_attribute_not_in_pinned_dtd"
            sdk_pair_key = (owner, xml_name)
            fact = sdk_only_properties.setdefault(
                sdk_pair_key,
                {
                    "owner_xml_name": owner,
                    "xml_name": xml_name,
                    "classification": classification,
                    "sdk_facts": [],
                },
            )
            fact["sdk_facts"].append(
                {
                    "cdx_id": sdk_fact["cdx_id"],
                    "cdx_constant": sdk_fact["cdx_constant"],
                    "sdk_type": sdk_fact["sdk_type"],
                    "value_text": sdk_fact["value_text"],
                    "source": _source_ref(_source_id_for_xml(owner), str(sdk_fact.get("locator"))),
                }
            )

    sdk_inventory_names = set(sdk_by_tag)
    dtd_names = set(dtd_elements)
    namespace_counts = Counter(entry.namespace for entry in inventory_entries)
    dtd_type_counts = Counter(
        attribute.declared_type
        for element in dtd_candidate.dtd_elements
        for attribute in element.attributes
    )
    undeclared_child_refs = [
        {"owner_xml_name": element.xml_name, "child_xml_name": child}
        for element in dtd_candidate.dtd_elements
        for child in element.children
        if child not in dtd_elements
    ]
    sdk_type_counts = Counter(
        str(match["sdk_type"])
        for pair in owner_attribute_pairs
        for match in pair["sdk_matches"]
        if match["sdk_type"] is not None
    )
    root_attributes = dtd_attr_names.get("CDXML", set())
    node_id_rows = page_entries_by_tag.get("n", [])
    node_id = next((item for item in node_id_rows if item.get("xml_name") == "id"), None)
    if node_id is None:
        raise EvidenceAcquisitionError("Node SDK page lacks its historical id property row")

    evidence: dict[str, object] = {
        "format": "cdxml-om-spec-evidence",
        "format_version": 1,
        "generated_at": retrieved_at,
        "retrieval": {
            "method": "explicit development acquisition against Internet Archive Mementos",
            "archive_timestamp_request": _NEAREST_CAPTURE,
            "sdk_index_timestamp": _INDEX_CAPTURE,
            "raw_html_policy": (
                "raw SDK HTML is hashed and parsed in memory, not copied to the repository"
            ),
            "parser": (
                "tools.schema_importer.sdk_importer.import_sdk_html; "
                "HTML-only recovery diagnostics retained"
            ),
        },
        "sources": source_records,
        "baseline": {
            "dtd_source_id": "revvity_dtd",
            "dtd_sha256": dtd_sha256,
            "dtd_element_count": len(dtd_candidate.dtd_elements),
            "nonroot_element_count": len(dtd_candidate.dtd_elements) - 1,
            "owner_attribute_pair_count": len(owner_attribute_pairs),
            "dtd_attribute_type_counts": dict(sorted(dtd_type_counts.items())),
            "sdk_inventory_count": len(inventory_entries),
            "sdk_inventory_namespace_counts": dict(sorted(namespace_counts.items())),
            "matched_sdk_owner_attribute_pair_count": sum(
                pair["sdk_mapping_status"] == "matched" for pair in owner_attribute_pairs
            ),
            "sdk_type_counts_for_exact_matches": dict(sorted(sdk_type_counts.items())),
        },
        "id_semantics": {
            "xml_root": {
                "xml_name": "CDXML",
                "cdx_object_id": 32768,
                "cdx_constant": "kCDXObj_Document",
                "dtd_declares_id_attribute": "id" in root_attributes,
                "source": _source_ref("sdk_objects", "inventory:CDXML"),
            },
            "generic_object_id": {
                **object_id_fact,
                "source": _source_ref("sdk_object_id", object_id_fact["locator"]),
            },
            "historical_object_id_property": {
                "owner_xml_name": "n",
                "xml_name": "id",
                "sdk_type": node_id.get("sdk_type"),
                "binary_type_value_text": node_id.get("value_text"),
                "source": _source_ref("sdk_page_n", str(node_id.get("locator"))),
            },
            "interpretation": (
                "Preserve the object-page id property type and generic CDXObjectID reference "
                "type as separate source claims; the sources do not explain whether their "
                "UINT16/UINT32 difference is historical object-ID storage versus reference width."
            ),
        },
        "elements": elements,
        "owner_attribute_pairs": owner_attribute_pairs,
        "sdk_only_properties": list(sdk_only_properties.values()),
        "sdk_only_property_classification_counts": dict(
            sorted(Counter(item["classification"] for item in sdk_only_properties.values()).items())
        ),
        "sdk_only_inventory_elements": sorted(sdk_inventory_names - dtd_names),
        "dtd_elements_without_sdk_inventory": sorted(dtd_names - sdk_inventory_names),
        "schema_anomalies": [
            {
                "id": "altgroup_undeclared_bracket_child",
                "status": "unresolved_source_anomaly",
                "owner_xml_name": "altgroup",
                "child_xml_name": "bracket",
                "dtd_content_model": (
                    "<!ELEMENT altgroup (objecttag | annotation | t | fragment | "
                    "group | graphic | bracket)+>"
                ),
                "dtd_child_declaration_present": False,
                "dtd_source": _source_ref(
                    "revvity_dtd", "line 410: <!ELEMENT altgroup (... | bracket)+>"
                ),
                "sdk_subobject_evidence": page_subobjects_by_tag.get("altgroup", []),
                "other_undeclared_child_references": [
                    item
                    for item in undeclared_child_refs
                    if item != {"owner_xml_name": "altgroup", "child_xml_name": "bracket"}
                ],
                "resolution": None,
            },
            {
                "id": "curve_closed_spacing_duplicate_cdx_id",
                "status": "unresolved_source_anomaly",
                "owner_xml_name": "curve",
                "claims": [
                    {
                        "xml_name": "Closed",
                        "cdx_id": 2616,
                        "cdx_constant": "kCDXProp_Closed",
                        "sdk_type": "CDXBoolean",
                        "locator": "Properties table: row 56",
                    },
                    {
                        "xml_name": "CurveSpacing",
                        "cdx_id": 2616,
                        "cdx_constant": "kCDXProp_Curve_Spacing",
                        "sdk_type": "UINT16",
                        "locator": "Properties table: row 59",
                    },
                ],
                "source": _source_ref(
                    "sdk_page_curve",
                    "Properties table: rows 56 and 59 both report 0x0A38",
                ),
                "cross_check": {
                    "source_url": (
                        "http://www.cambridgesoft.com/services/documentation/sdk/"
                        "chemdraw/cdx/TableOfProperties.htm"
                    ),
                    "result": "same_duplicate_assignments",
                    "independent_source": False,
                    "note": (
                        "The archived global property table repeats both assignments; "
                        "it is part of the same SDK source family, not independent "
                        "confirmation. The linked detailed property pages were unavailable."
                    ),
                },
                "resolution": None,
            },
        ],
        "contradictions": [
            {
                "id": "object_id_width_context",
                "status": "unresolved_contextual_difference",
                "claims": [
                    {
                        "claim": "Node object page lists XML id as UINT16",
                        "source": _source_ref("sdk_page_n", str(node_id.get("locator"))),
                    },
                    {
                        "claim": "Generic CDXObjectID datatype is UINT32",
                        "source": _source_ref("sdk_object_id", object_id_fact["locator"]),
                    },
                    {
                        "claim": "DTD id values are CDATA XML attributes, with no id on CDXML root",
                        "source": _source_ref(
                            "revvity_dtd", "id attributes across element declarations"
                        ),
                    },
                ],
                "resolution": None,
            },
            {
                "id": "inventory_namespace_collision",
                "status": "resolved_by_namespace_evidence",
                "claims": [
                    {
                        "claim": (
                            "colortable and fonttable carry kCDXProp constants, "
                            "not object constants"
                        ),
                        "source": _source_ref(
                            "sdk_objects", "inventory rows: colortable/fonttable"
                        ),
                    },
                    {
                        "claim": (
                            "color, font, and s inventory entries have no CDX "
                            "constant or numeric ID"
                        ),
                        "source": _source_ref("sdk_objects", "inventory rows: color/font/s"),
                    },
                ],
                "resolution": (
                    "Keep object, property, and XML-only namespaces distinct; these rows do not "
                    "supply binary object IDs for the XML tags."
                ),
            },
        ],
        "limitations": [
            "A missing exact SDK row is not proof that an XML feature is invalid or unsupported.",
            (
                "SDK page properties are joined only by exact owner XML name and exact "
                "CDXML Name; no alias or semantic type is inferred."
            ),
            (
                "reference_target remains null unless an explicit type or direct statement "
                "supplies it; targets are not inferred from attribute names."
            ),
            "SDK enum ordinals are not synthesized from DTD lexical enumeration tokens.",
        ],
    }
    if len(owner_attribute_pairs) != 762:
        raise EvidenceAcquisitionError("expected 762 DTD owner/attribute pairs")
    if len(elements) != 53:
        raise EvidenceAcquisitionError("expected 53 DTD elements including CDXML root")
    if "CDXML" not in sdk_inventory_names or "id" in root_attributes:
        raise EvidenceAcquisitionError("CDXML root inventory/id assertion failed")
    return evidence


def _focused_page_text(content: bytes) -> str:
    parser = html.HTMLParser(no_network=True, recover=True, default_doctype=False)
    document = html.document_fromstring(content, parser=parser)
    return " ".join(" ".join(document.itertext()).split())


def _bond_order_rows(content: bytes) -> list[dict[str, str | None]]:
    parser = html.HTMLParser(no_network=True, recover=True, default_doctype=False)
    document = html.document_fromstring(content, parser=parser)
    for table in document.xpath("//table"):
        if not isinstance(table, html.HtmlElement):
            continue
        rows = _direct_rows(table)
        headers: dict[str, int] | None = None
        for row in rows:
            cells = _direct_cells(row)
            candidate = [_normalized_header(_cell_text(cell)) for cell in cells]
            if {"value", "cdxml name", "description"}.issubset(candidate):
                headers = {value: index for index, value in enumerate(candidate)}
                break
        if headers is None:
            continue
        result: list[dict[str, str | None]] = []
        for row in rows:
            cells = _direct_cells(row)
            if len(cells) <= max(headers.values()):
                continue
            value_text = _cell_text(cells[headers["value"]]).strip()
            if re.fullmatch(r"0[xX][0-9a-fA-F]+", value_text) is None:
                continue
            xml_token = _cell_text(cells[headers["cdxml name"]]).strip() or None
            result.append({"binary_value": value_text, "xml_token": xml_token})
        if result:
            return result
    raise EvidenceAcquisitionError("Bond_Order page has no parseable value/CDXML Name table")


def _existing_source_records(path: Path) -> dict[str, SourceRecord]:
    try:
        payload: object = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceAcquisitionError(
            f"cannot read baseline evidence catalog {path}: {exc}"
        ) from exc
    if not isinstance(payload, dict):
        raise EvidenceAcquisitionError("baseline evidence root must be an object")
    mapping = cast(dict[str, object], payload)
    source_value = mapping.get("sources")
    if not isinstance(source_value, list):
        raise EvidenceAcquisitionError("baseline evidence has no sources array")
    records: dict[str, SourceRecord] = {}
    for item in cast(list[object], source_value):
        if not isinstance(item, dict):
            continue
        row = cast(dict[str, object], item)
        source_id = row.get("id")
        if isinstance(source_id, str):
            records[source_id] = cast(SourceRecord, row)
    return records


def build_focused_evidence(
    pins: dict[str, PinRecord] | None = None,
    *,
    base_catalog: Path | None = None,
) -> dict[str, object]:
    """Fetch focused detailed SDK pages and record XML/binary-specific facts."""
    pin_registry = pins or {}
    existing_sources = _existing_source_records(
        PROJECT_ROOT / _BASE_EVIDENCE_PATH if base_catalog is None else base_catalog
    )
    original_urls = {
        spec["id"]: f"{_ORIGINAL_ROOT}/{spec['path']}" for spec in _FOCUSED_SOURCE_SPECS
    }
    downloaded: dict[str, tuple[bytes, SourceRecord]] = {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {
            pool.submit(
                _fetch_snapshot,
                original_urls[spec["id"]],
                capture=spec["capture"],
                pin=pin_registry.get(original_urls[spec["id"]].replace(":80", "")),
            ): spec
            for spec in _FOCUSED_SOURCE_SPECS
        }
        for future in as_completed(futures):
            spec = futures[future]
            content, source = future.result()
            source["id"] = spec["id"]
            source["original_url"] = original_urls[spec["id"]].replace(":80", "")
            downloaded[spec["id"]] = (content, source)

    markers_by_source = {
        "sdk_bond_order": ("0xFFFF", "Unspecified order", "treated as a single bond"),
        "sdk_label_style_size": ("LabelSize", "kCDXProp_LabelStyleSize", "INT16"),
        "sdk_caption_style_size": ("CaptionSize", "kCDXProp_CaptionStyleSize", "INT16"),
        "sdk_rotation_angle": ("degrees * 65536", "zero degrees"),
        "sdk_date_and_time": ("14 byte structure", "7 INT16", "UTC"),
        "sdk_int16_list_with_counts": ("series of", "total number of values", "CDXML"),
        "sdk_generic_list": ("CDXString", "NOT", "CDXML"),
        "sdk_element_list": ("UINT16", "NOT", "CDXML"),
        "sdk_formula": ("undefined", "neither reads nor writes"),
        "sdk_curve_points": ("CDXPoint", "UINT16", "CDXML"),
        "sdk_curve_points_3d": ("CDXPoint3D", "UINT16", "CDXML"),
        "sdk_curve_points_3d_property": (
            "CurvePoints3D",
            "kCDXProp_Curve_Points3D",
            "CDXCurvePoints3D",
        ),
        "sdk_node_attachments": (
            "Attachments",
            "kCDXProp_Node_Attachments",
            "CDXObjectIDArrayWithCounts",
            "list of IDs of the nodes",
        ),
        "sdk_object_tag_value": (
            "varies",
            "INT32",
            "FLOAT64",
            "unformatted string",
            "zero",
        ),
        "sdk_object_tag_type": (
            "Unknown",
            "Double",
            "Long",
            "String",
            "Undefined",
        ),
        "sdk_unformatted": ("sequence of bytes", "hex-encoded"),
        "sdk_spectrum_data_point": (
            "temp_SpectrumDataPoint",
            "FLOAT64",
            "#PCDATA",
        ),
        "sdk_spectrum_y_low": ("YLow", "not read", "future compatibility"),
        "sdk_cdx_string": ("20ths of a point", '<s font="3" size="12"'),
        "sdk_cdx_font_table": (
            "character set of this font",
            "UINT16",
            'charset="iso-8859-1"',
        ),
        "sdk_font_table_property": (
            "kCDXProp_FontTable",
            "used only in CDX files",
            "Font Table object",
        ),
        "sdk_color_table_property": (
            "kCDXProp_ColorTable",
            "used only in CDX files",
            "Color Table object",
        ),
        "sdk_coordinates": (
            "CDXPoint3D",
            "decimal values",
            'CDXML: "72 144 216"',
        ),
        "sdk_geometry_properties": (
            "kCDXProp_3DCenter",
            "kCDXProp_3DMajorAxisEnd",
            "kCDXProp_3DMinorAxisEnd",
            "CDXPoint3D",
        ),
    }
    for source_id, markers in markers_by_source.items():
        text = _focused_page_text(downloaded[source_id][0]).casefold()
        missing = [marker for marker in markers if marker.casefold() not in text]
        if missing:
            raise EvidenceAcquisitionError(
                f"focused source {source_id} lacks expected factual markers: {missing}"
            )

    dtd_candidate = import_dtd(str(PROJECT_ROOT / _DTD_PATH))
    bond_element = next(
        element for element in dtd_candidate.dtd_elements if element.xml_name == "b"
    )
    bond_order = next(
        attribute for attribute in bond_element.attributes if attribute.name == "Order"
    )
    font_element = next(
        element for element in dtd_candidate.dtd_elements if element.xml_name == "font"
    )
    font_charset = next(
        attribute for attribute in font_element.attributes if attribute.name == "charset"
    )
    geometry_entries = _import_bytes(
        downloaded["sdk_geometry_properties"][0], "TableOfProperties.htm"
    ).sdk_entries
    geometry_constants = {
        "kCDXProp_3DCenter",
        "kCDXProp_3DMajorAxisEnd",
        "kCDXProp_3DMinorAxisEnd",
    }
    geometry_rows = {
        entry.cdx_constant: entry
        for entry in geometry_entries
        if entry.cdx_constant in geometry_constants
    }
    if set(geometry_rows) != geometry_constants:
        raise EvidenceAcquisitionError("geometry property table lacks one of the expected 3D rows")
    geometry_attributes = {
        name: [
            (element, attribute)
            for element in dtd_candidate.dtd_elements
            for attribute in element.attributes
            if attribute.name == name
        ]
        for name in ("Center3D", "MajorAxisEnd3D", "MinorAxisEnd3D")
    }
    bond_rows = _bond_order_rows(downloaded["sdk_bond_order"][0])
    if len([row for row in bond_rows if row["xml_token"] is not None]) != 16:
        raise EvidenceAcquisitionError("Bond_Order source no longer lists 16 XML value tokens")
    focused_sources = [downloaded[spec["id"]][1] for spec in _FOCUSED_SOURCE_SPECS]
    required_existing_ids = {
        "revvity_dtd",
        "sdk_objects",
        "sdk_document",
        "sdk_object_id",
        "sdk_page_n",
        "sdk_page_t",
        "sdk_page_curve",
        "sdk_page_b",
        "sdk_page_fragment",
        "sdk_page_objecttag",
        "sdk_page_spectrum",
    }
    missing_existing_ids = sorted(required_existing_ids - set(existing_sources))
    if missing_existing_ids:
        raise EvidenceAcquisitionError(
            f"baseline evidence catalog lacks focused source records: {missing_existing_ids}"
        )
    source_records = [existing_sources[source_id] for source_id in sorted(required_existing_ids)]
    source_records.extend(focused_sources)

    def ref(source_id: str, locator: str) -> dict[str, str]:
        return {"source_id": source_id, "locator": locator}

    facts: list[dict[str, object]] = [
        {
            "id": "bond_order_bit_values",
            "kind": "documented_xml_values_and_binary_bitmask",
            "owner_xml_names": ["b"],
            "xml_name": "Order",
            "cdx_constant": "kCDXProp_Bond_Order",
            "cdx_property_id": 0x0600,
            "binary_type": "INT16",
            "source_values": bond_rows,
            "source_statement": {
                "values_may_be_combined": True,
                "absent_property_semantics": "single bond",
                "unspecified_binary_value": "0xFFFF",
                "unspecified_binary_value_xml_representation": "omitted entirely",
                "chem_draw_documentation": (
                    "Ionic, hydrogen, and three-center bonds are documented as defined "
                    "for future compatibility, not currently supported by ChemDraw."
                ),
                "chem_draw_runtime_tested_here": False,
            },
            "pinned_dtd": {
                "declared_type": bond_order.declared_type,
                "required": bond_order.required,
                "default_kind": bond_order.default_kind,
                "default_value": bond_order.default_value,
                "enum_values": list(bond_order.enum_values),
            },
            "interpretation": (
                "Keep the SDK's bit-encoded binary values and CDXML Name tokens distinct; "
                "this is not an ordinal enum. The pinned DTD declares Order as CDATA."
            ),
            "source_refs": [
                ref("sdk_bond_order", "Bond_Order property value table and description"),
                ref("revvity_dtd", bond_order.locator),
                ref("sdk_page_b", "Properties table: Order / kCDXProp_Bond_Order / INT16"),
            ],
        },
        {
            "id": "font_size_encodings",
            "kind": "separate_default_size_and_text_style_run_evidence",
            "properties": [
                {
                    "xml_name": "LabelSize",
                    "cdx_constant": "kCDXProp_LabelStyleSize",
                    "cdx_property_id": 0x081C,
                    "binary_type": "INT16",
                    "source": ref("sdk_label_style_size", "LabelStyleSize property summary"),
                },
                {
                    "xml_name": "CaptionSize",
                    "cdx_constant": "kCDXProp_CaptionStyleSize",
                    "cdx_property_id": 0x081D,
                    "binary_type": "INT16",
                    "source": ref("sdk_caption_style_size", "CaptionStyleSize property summary"),
                },
            ],
            "text_style_run": {
                "xml_element": "s",
                "xml_attribute": "size",
                "example_point_size": 12,
                "cdx_string_font_size_type": "UINT16",
                "cdx_string_font_size_unit": "twentieths of a point",
                "minimum_binary_resolution_points": 0.05,
                "source": ref("sdk_cdx_string", "CDXString Font style run and examples"),
            },
            "scope_note": (
                "The captured LabelSize/CaptionSize property pages state binary INT16 and "
                "that these properties are font-size defaults. The CDXString source defines "
                "20ths-of-a-point units for font style runs. It does not explicitly state "
                "that the separate LabelSize/CaptionSize property values use that same scale."
            ),
            "source_refs": [
                ref("sdk_label_style_size", "LabelStyleSize summary and description"),
                ref("sdk_caption_style_size", "CaptionStyleSize summary and description"),
                ref("sdk_cdx_string", "CDXString XML examples and Font style run table"),
            ],
        },
        {
            "id": "font_table_charset_encodings",
            "kind": "xml_lexical_value_vs_binary_integer",
            "xml_property": {
                "owner_xml_name": "font",
                "xml_name": "charset",
                "dtd_declared_type": font_charset.declared_type,
                "example_value": "iso-8859-1",
                "source": ref("revvity_dtd", "<!ATTLIST font charset CDATA #IMPLIED>"),
            },
            "binary_encoding": {
                "datatype": "CDXFontTable",
                "component_type": "UINT16",
                "component_meaning": "character set of this font",
            },
            "source_refs": [
                ref(
                    "sdk_cdx_font_table",
                    "CDXFontTable charset field and CDXML fonttable example",
                ),
                ref("revvity_dtd", "<!ATTLIST font charset CDATA #IMPLIED>"),
            ],
            "scope_note": (
                "The binary font-table structure stores a UINT16 character-set code, while "
                "the SDK's CDXML example uses the lexical token 'iso-8859-1'. Preserve the "
                "XML attribute as text; the source does not provide an XML-to-binary code map."
            ),
        },
        {
            "id": "point3d_lexical_contract",
            "kind": "xml_point3d_numeric_triple",
            "sdk_datatype": "CDXPoint3D",
            "cdxml_component_order": ["x", "y", "z"],
            "cdxml_components": "three numeric coordinate values",
            "coordinate_unit": "points",
            "decimal_values_allowed": True,
            "example": "72 144 216",
            "source_refs": [
                ref("sdk_coordinates", "CDXPoint3D section and three-component example"),
            ],
            "source_caveat": (
                "The page's CDXPoint3D paragraph calls the XML form CDXPoint2D in one sentence, "
                "but immediately gives three x/y/z values. The three-value lexical example is "
                "recorded without relying on that apparent copy error."
            ),
        },
        {
            "id": "axis_point3d_property_name_reconciliation",
            "kind": "unresolved_sdk_property_name_mismatch",
            "sdk_property_rows": [
                {
                    "cdx_constant": constant,
                    "cdx_id": geometry_rows[constant].cdx_id,
                    "sdk_xml_name": geometry_rows[constant].xml_name,
                    "sdk_type": geometry_rows[constant].type_name,
                    "locator": geometry_rows[constant].locator,
                }
                for constant in (
                    "kCDXProp_3DCenter",
                    "kCDXProp_3DMajorAxisEnd",
                    "kCDXProp_3DMinorAxisEnd",
                )
            ],
            "dtd_attributes": [
                {
                    "xml_name": name,
                    "owners": [element.xml_name for element, _ in attributes],
                    "declared_type": attributes[0][1].declared_type if attributes else None,
                    "source_refs": [
                        ref("revvity_dtd", attribute.locator) for _, attribute in attributes
                    ],
                }
                for name, attributes in geometry_attributes.items()
            ],
            "resolution": None,
            "scope_note": (
                "The global SDK property table types all three records as CDXPoint3D, but gives "
                "all three the CDXML Name Center3D and lists no owning XML object. DTD Center3D "
                "has an exact lexical-name match; MajorAxisEnd3D and MinorAxisEnd3D do not. "
                "Do not infer owner-to-CDX-ID associations or silently correct the SDK name."
            ),
            "source_refs": [
                ref(
                    "sdk_geometry_properties", "Properties table: rows for the three 3D properties"
                ),
                ref("sdk_coordinates", "CDXPoint3D section and three-component example"),
            ],
        },
        {
            "id": "rotation_angle",
            "kind": "fixed_point_angle",
            "xml_name": "RotationAngle",
            "cdx_constant": "kCDXProp_RotationAngle",
            "cdx_property_id": 0x0205,
            "binary_type": "INT32",
            "encoding": "degrees multiplied by 65536",
            "absent_property_semantics": "zero degrees / not rotated",
            "source_refs": [
                ref("sdk_rotation_angle", "RotationAngle property description and absent clause"),
                ref("sdk_page_t", "Text property table: RotationAngle / INT32"),
            ],
        },
        {
            "id": "cdx_date",
            "kind": "binary_datetime_no_xml_lexical_contract",
            "sdk_datatype": "CDXDate",
            "binary_encoding": {
                "length_bytes": 14,
                "components": ["year", "month", "day", "hour", "minute", "second", "milliseconds"],
                "component_type": "INT16",
                "timezone": "UTC",
            },
            "cdxml_lexical_format": None,
            "source_refs": [
                ref("sdk_date_and_time", "CDX Date and Time Data Type description"),
                ref("sdk_document", "Properties table: CreationDate / ModificationDate / CDXDate"),
            ],
            "interpretation": (
                "Do not infer a CDXML date string parser from the binary 14-byte type page; "
                "the cited type page does not define a CDXML lexical form."
            ),
        },
        {
            "id": "attachments_array_with_counts",
            "kind": "typed_object_id_array",
            "owner_xml_name": "n",
            "xml_name": "Attachments",
            "cdx_constant": "kCDXProp_Node_Attachments",
            "cdx_property_id": 0x0432,
            "binary_type": "CDXObjectIDArrayWithCounts",
            "reference_target_xml_name": "n",
            "cdx_encoding": {
                "items": "UINT32 object IDs",
                "count_prefix": "UINT16 before the series of IDs",
            },
            "cdxml_encoding": {
                "same_as": "CDXObjectIDArray",
                "count_prefix": False,
                "example": "1 2 3 4",
            },
            "property_description": (
                "IDs of nodes which are multiply or variably attached to this node"
            ),
            "source_refs": [
                ref("sdk_node_attachments", "Node_Attachments property type and description"),
                ref("sdk_object_id", "CDXObjectIDArrayWithCounts CDX and CDXML descriptions"),
                ref("sdk_page_n", "Properties table: Attachments / CDXObjectIDArrayWithCounts"),
            ],
        },
        {
            "id": "line_starts_counted_list",
            "kind": "typed_integer_list",
            "owner_xml_name": "t",
            "xml_name": "LineStarts",
            "cdx_constant": "kCDXProp_LineStarts",
            "cdx_property_id": 0x0704,
            "binary_type": "INT16ListWithCounts",
            "cdx_encoding": {
                "items": "UINT16 values",
                "count_prefix": "UINT16 before the series of values",
            },
            "cdxml_encoding": {"count_prefix": False, "example": "1 2 3 4"},
            "source_refs": [
                ref("sdk_page_t", "Properties table: LineStarts / INT16ListWithCounts"),
                ref("sdk_int16_list_with_counts", "INT16 List With Counts Data Type"),
            ],
        },
        {
            "id": "curve_point_arrays",
            "kind": "typed_numeric_point_arrays",
            "properties": [
                {
                    "owner_xml_name": "curve",
                    "xml_name": "CurvePoints",
                    "cdx_constant": "kCDXProp_Curve_Points",
                    "cdx_property_id": 0x0A23,
                    "binary_type": "CDXCurvePoints",
                    "dimensions": 2,
                    "cdx_count_prefix": "UINT16 point count",
                    "cdxml_example": "1 2 3 4",
                    "source_refs": [
                        ref("sdk_page_curve", "Properties table: CurvePoints"),
                        ref("sdk_curve_points", "CDX Curve Points Data Type"),
                    ],
                },
                {
                    "owner_xml_name": "curve",
                    "xml_name": "CurvePoints3D",
                    "cdx_constant": "kCDXProp_Curve_Points3D",
                    "cdx_property_id": 0x0A2E,
                    "binary_type": "CDXCurvePoints3D",
                    "dimensions": 3,
                    "cdx_count_prefix": "UINT16 point count",
                    "cdxml_example": "1 2 3 4 5 6",
                    "source_refs": [
                        ref("sdk_curve_points_3d_property", "Curve_Points3D property summary"),
                        ref("sdk_page_curve", "Properties table: CurvePoints3D"),
                        ref("sdk_curve_points_3d", "CDX Curve Points 3D Data Type"),
                    ],
                },
            ],
            "cdxml_count_prefix": False,
        },
        {
            "id": "element_generic_and_formula_lists",
            "kind": "typed_list_family",
            "datatypes": [
                {
                    "name": "CDXElementList",
                    "binary_item_type": "UINT16 atomic-number values",
                    "binary_count_prefix": "signed INT16 count; negative means NOT list",
                    "cdxml_not_prefix": "NOT",
                    "example": "NOT 9 17 35",
                    "source": ref("sdk_element_list", "CDX Element List Data Type"),
                },
                {
                    "name": "CDXGenericList",
                    "binary_item_type": "CDXString values",
                    "binary_count_prefix": "signed INT16 count; negative means NOT list",
                    "cdxml_not_prefix": "NOT",
                    "example": "NOT R X A",
                    "source": ref("sdk_generic_list", "CDX Generic List Data Type"),
                },
                {
                    "name": "CDXFormula",
                    "binary_encoding": None,
                    "meaning": "undefined; declared for future expansion",
                    "chem_draw_reads_or_writes": False,
                    "source": ref("sdk_formula", "CDX Formula Data Type statement"),
                },
            ],
            "source_refs": [
                ref("sdk_page_n", "Properties table: ElementList and GenericList"),
                ref("sdk_page_fragment", "Properties table: Formula"),
            ],
            "caution": (
                "Do not assign formula chemistry semantics or parse an undefined CDXFormula type."
            ),
        },
        {
            "id": "object_tag_value_by_tag_type",
            "kind": "context_dependent_binary_union",
            "owner_xml_name": "objecttag",
            "xml_name": "Value",
            "cdx_constant": "kCDXProp_ObjectTag_Value",
            "cdx_property_id": 0x0D05,
            "binary_type": "varies",
            "tag_type_cases": [
                {"value": 0, "xml_token": "Unknown", "binary_value_type": None},
                {"value": 1, "xml_token": "Double", "binary_value_type": "FLOAT64"},
                {"value": 2, "xml_token": "Long", "binary_value_type": "INT32"},
                {"value": 3, "xml_token": "String", "binary_value_type": "Unformatted"},
            ],
            "absent_tag_type_semantics": "Undefined",
            "absent_value_property_semantics": "zero",
            "empty_xml_value_semantics": None,
            "source_refs": [
                ref("sdk_object_tag_type", "ObjectTag_Type enumeration and absent clause"),
                ref(
                    "sdk_object_tag_value",
                    "ObjectTag_Value type-dependent description and absent clause",
                ),
                ref("sdk_unformatted", "CDX Unformatted Data Type XML representation"),
                ref("sdk_page_objecttag", "ObjectTag properties table"),
            ],
            "caution": (
                "The source specifies omission semantics for the property, not the meaning of "
                "an explicitly present empty Value attribute. Do not hex-decode arbitrary "
                "printable unformatted values based only on byte-oriented cases."
            ),
        },
        {
            "id": "spectrum_data_is_pcdata",
            "kind": "cdx_property_to_xml_character_data",
            "owner_xml_name": "spectrum",
            "cdx_constant": "kCDXProp_Spectrum_DataPoint",
            "cdx_property_id": 0x0A86,
            "binary_type": "FLOAT64 array",
            "sdk_property_page_xml_name": "temp_SpectrumDataPoint",
            "literal_xml_attribute_or_element_name": False,
            "cdxml_representation": "data stored directly within spectrum object as #PCDATA",
            "properties_page_says_used_explicitly_only_for_cdx": True,
            "source_refs": [
                ref("sdk_spectrum_data_point", "Spectrum_DataPoint property description"),
                ref("sdk_page_spectrum", "Properties table: DataPoint shown as not used"),
            ],
        },
        {
            "id": "spectrum_y_low_compatibility",
            "kind": "documented_nonimplemented_compatibility_property",
            "owner_xml_name": "spectrum",
            "xml_name": "YLow",
            "cdx_constant": "kCDXProp_Spectrum_YLow",
            "cdx_property_id": 0x0A88,
            "binary_type": "FLOAT64",
            "first_written_read": False,
            "chem_draw_reads_or_writes": False,
            "description_context": "defined for future compatibility; omission has no consequence",
            "source_refs": [
                ref("sdk_spectrum_y_low", "Spectrum_YLow absent clause"),
                ref("sdk_page_spectrum", "Properties table: YLow"),
            ],
        },
        {
            "id": "xml_child_table_properties",
            "kind": "cdx_property_saved_as_cdxml_child_object",
            "properties": [
                {
                    "xml_tag": "fonttable",
                    "cdx_constant": "kCDXProp_FontTable",
                    "cdx_property_id": 0x0100,
                    "cdx_type": "CDXFontTable",
                    "cdxml_saved_as": "Font Table object",
                    "source": ref(
                        "sdk_font_table_property", "FontTable property CDX/CDXML distinction"
                    ),
                },
                {
                    "xml_tag": "colortable",
                    "cdx_constant": "kCDXProp_ColorTable",
                    "cdx_property_id": 0x0300,
                    "cdx_type": "CDXColorTable",
                    "cdxml_saved_as": "Color Table object",
                    "source": ref(
                        "sdk_color_table_property", "ColorTable property CDX/CDXML distinction"
                    ),
                },
            ],
            "xml_only_inventory_names": ["color", "font", "s"],
            "inventory_source": ref(
                "sdk_objects", "AllCDXObjects rows for fonttable/colortable/color/font/s"
            ),
            "document_source": ref("sdk_document", "Document subobject table"),
        },
    ]
    return {
        "format": "cdxml-om-focused-sdk-evidence",
        "format_version": 1,
        "generated_at": _utc_now(),
        "method": (
            "Explicit development-time fetch of exact Internet Archive Memento URLs; "
            "only factual extractions and SHA-256 provenance are retained, not HTML."
        ),
        "sources": source_records,
        "facts": facts,
        "limitations": [
            "Historical SDK documentation is not a live ChemDraw runtime verification.",
            "SDK binary types and CDXML lexical representations remain separately scoped.",
            (
                "A source page's CDXML Name is not assumed to be a literal XML attribute "
                "when the page says otherwise."
            ),
            (
                "No semantic implementation or enum ordinal is inferred solely from a "
                "binary numeric type."
            ),
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="explicitly fetch primary SDK snapshots from Internet Archive",
    )
    parser.add_argument(
        "--output",
        default="-",
        help="write the extracted factual catalog here, or - for stdout (default: -)",
    )
    parser.add_argument(
        "--pins",
        type=Path,
        help="reacquire exact Memento URLs and verify SHA-256 values from an evidence catalog",
    )
    parser.add_argument(
        "--focused-only",
        action="store_true",
        help="acquire the focused detailed property/datatype evidence catalog",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="replace an existing output file when explicitly requested",
    )
    arguments = parser.parse_args(argv)
    if not arguments.fetch:
        parser.error("source acquisition requires the explicit --fetch flag")
    try:
        pins = _load_pins(arguments.pins)
        evidence = build_focused_evidence(pins) if arguments.focused_only else build_evidence(pins)
    except EvidenceAcquisitionError as exc:
        print(f"spec evidence acquisition failed: {exc}", file=sys.stderr)
        return 2
    content = json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    try:
        if not write_text_output(arguments.output, content, force=arguments.force):
            sys.stdout.write(content)
    except ImporterError as exc:
        print(f"spec evidence output failed: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
