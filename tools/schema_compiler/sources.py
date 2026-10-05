"""Canonical provenance source registry."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import cast
from urllib.parse import urlsplit


@dataclass(frozen=True, slots=True)
class Source:
    id: str
    uri: str


SOURCES = {
    "sdk_objects": Source(
        "sdk_objects", "https://chemapps.stolaf.edu/iupac/cdx/sdk/AllCDXObjects.htm"
    ),
    "sdk_document": Source(
        "sdk_document", "https://chemapps.stolaf.edu/iupac/cdx/sdk/Document.htm"
    ),
    "sdk_object_id": Source(
        "sdk_object_id",
        "https://chemapps.stolaf.edu/iupac/cdx/sdk/DataType/CDXObjectID.htm",
    ),
    "sdk_coordinates": Source(
        "sdk_coordinates",
        "https://chemapps.stolaf.edu/iupac/cdx/sdk/DataType/CDXCoordinates.htm",
    ),
    "sdk_intro": Source(
        "sdk_intro", "https://iupac.github.io/IUPAC-FAIRSpec/cdx_sdk/IntroCDXML.htm"
    ),
    "sdk_fragment": Source(
        "sdk_fragment", "https://chemapps.stolaf.edu/iupac/cdx/sdk/Fragment.htm"
    ),
    "sdk_node": Source("sdk_node", "https://chemapps.stolaf.edu/iupac/cdx/sdk/Node.htm"),
    "sdk_bond": Source("sdk_bond", "https://chemapps.stolaf.edu/iupac/cdx/sdk/Bond.htm"),
    "sdk_bond_order": Source(
        "sdk_bond_order",
        "https://chemapps.stolaf.edu/iupac/cdx/sdk/properties/Bond_Order.htm",
    ),
    "sdk_font_charset_xml": Source(
        "sdk_font_charset_xml",
        "https://chemapps.stolaf.edu/iupac/cdx/sdk/DataType/CDXFontTable.htm",
    ),
    "sdk_node_element": Source(
        "sdk_node_element",
        "https://chemapps.stolaf.edu/iupac/cdx/sdk/properties/Node_Element.htm",
    ),
    "sdk_atom_charge": Source(
        "sdk_atom_charge",
        "https://chemapps.stolaf.edu/iupac/cdx/sdk/properties/Atom_Charge.htm",
    ),
    "sdk_atom_isotope": Source(
        "sdk_atom_isotope",
        "https://chemapps.stolaf.edu/iupac/cdx/sdk/properties/Atom_Isotope.htm",
    ),
    "sdk_bond_display": Source(
        "sdk_bond_display",
        "https://chemapps.stolaf.edu/iupac/cdx/sdk/properties/Bond_Display.htm",
    ),
    "sdk_group": Source("sdk_group", "https://chemapps.stolaf.edu/iupac/cdx/sdk/Group.htm"),
    "sdk_text": Source("sdk_text", "https://chemapps.stolaf.edu/iupac/cdx/sdk/Text.htm"),
    "sdk_graphic": Source("sdk_graphic", "https://chemapps.stolaf.edu/iupac/cdx/sdk/Graphic.htm"),
    "sdk_arrow": Source("sdk_arrow", "https://chemapps.stolaf.edu/iupac/cdx/sdk/Arrow.htm"),
    "sdk_scheme": Source(
        "sdk_scheme", "https://chemapps.stolaf.edu/iupac/cdx/sdk/ReactionScheme.htm"
    ),
    "sdk_step": Source("sdk_step", "https://chemapps.stolaf.edu/iupac/cdx/sdk/ReactionStep.htm"),
    "sdk_font": Source("sdk_font", "https://chemapps.stolaf.edu/iupac/cdx/sdk/Font.htm"),
    "sdk_color": Source("sdk_color", "https://chemapps.stolaf.edu/iupac/cdx/sdk/Color.htm"),
    "revvity_dtd": Source(
        "revvity_dtd", "https://static.chemistry.revvitycloud.com/cdxml/CDXML.dtd"
    ),
}

# These five curated HTTPS mirrors intentionally coexist with the archived
# CambridgeSDK source pages in the checked-in factual catalogs.  Match both
# the curated URI and the exact original page identity; a reused ID pointing
# at any other page is an error, not a generic “curated source wins” case.
_CURATED_ARCHIVE_PAGE_ALIASES: dict[str, tuple[str, str]] = {
    "sdk_objects": (
        "https://chemapps.stolaf.edu/iupac/cdx/sdk/AllCDXObjects.htm",
        "http://www.cambridgesoft.com/services/documentation/sdk/chemdraw/cdx/AllCDXObjects.htm",
    ),
    "sdk_document": (
        "https://chemapps.stolaf.edu/iupac/cdx/sdk/Document.htm",
        "http://www.cambridgesoft.com/services/documentation/sdk/chemdraw/cdx/Document.htm",
    ),
    "sdk_object_id": (
        "https://chemapps.stolaf.edu/iupac/cdx/sdk/DataType/CDXObjectID.htm",
        "http://www.cambridgesoft.com/services/documentation/sdk/chemdraw/cdx/DataType/CDXObjectID.htm",
    ),
    "sdk_bond_order": (
        "https://chemapps.stolaf.edu/iupac/cdx/sdk/properties/Bond_Order.htm",
        "http://www.cambridgesoft.com/services/documentation/sdk/chemdraw/cdx/properties/Bond_Order.htm",
    ),
    "sdk_coordinates": (
        "https://chemapps.stolaf.edu/iupac/cdx/sdk/DataType/CDXCoordinates.htm",
        "http://www.cambridgesoft.com/services/documentation/sdk/chemdraw/cdx/DataType/CDXCoordinates.htm",
    ),
}
_CATALOG_ORIGINAL_URLS: dict[str, str] = {}


def _normalized_url(value: str) -> str:
    parsed = urlsplit(value)
    scheme = parsed.scheme.lower()
    host = (parsed.hostname or "").lower()
    try:
        port = parsed.port
    except ValueError as exc:
        raise ValueError(f"invalid source URI {value!r}") from exc
    if (scheme, port) in {("http", 80), ("https", 443)}:
        port = None
    netloc = host if port is None else f"{host}:{port}"
    return parsed._replace(scheme=scheme, netloc=netloc).geturl()


def _source_page_identity(value: str) -> str:
    parsed = urlsplit(value)
    if (parsed.hostname or "").lower() in {"web.archive.org", "www.web.archive.org"}:
        path_parts = parsed.path.split("/", 3)
        if len(path_parts) == 4 and path_parts[1] == "web":
            archived_url = path_parts[3]
            if archived_url.startswith(("http://", "https://")):
                return _normalized_url(archived_url)
    return _normalized_url(value)


def _add_catalog_sources(path: Path) -> None:
    if not path.is_file():
        return
    try:
        payload_object: object = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read provenance source catalog {path}") from exc
    if not isinstance(payload_object, dict):
        raise ValueError(f"provenance source catalog {path} must contain an object")
    payload = cast(dict[str, object], payload_object)
    raw_sources = payload.get("sources")
    if not isinstance(raw_sources, list):
        raise ValueError(f"provenance source catalog {path} has no sources list")
    seen_ids: set[str] = set()
    parsed_sources: list[tuple[str, str, str]] = []
    for index, raw_source in enumerate(cast(list[object], raw_sources)):
        if not isinstance(raw_source, dict):
            raise ValueError(f"provenance source row {index} in {path} is not an object")
        source = cast(dict[str, object], raw_source)
        source_id = source.get("id")
        original_url = source.get("original_url")
        snapshot_url = source.get("snapshot_url")
        uri = snapshot_url if isinstance(snapshot_url, str) and snapshot_url else original_url
        if not isinstance(source_id, str) or not source_id:
            raise ValueError(f"provenance source row {index} in {path} has no id")
        if not isinstance(uri, str) or not uri:
            raise ValueError(f"provenance source {source_id!r} in {path} has no URI")
        if source_id in seen_ids:
            raise ValueError(f"duplicate provenance source ID {source_id!r} in {path}")
        seen_ids.add(source_id)
        if not isinstance(original_url, str) or not original_url:
            raise ValueError(f"provenance source {source_id!r} in {path} has no original URL")
        if _source_page_identity(uri) != _normalized_url(original_url):
            raise ValueError(
                f"provenance source {source_id!r} URI does not identify its original page in {path}"
            )
        parsed_sources.append((source_id, original_url, uri))

    staged_originals = dict(_CATALOG_ORIGINAL_URLS)
    staged_sources = dict(SOURCES)
    for source_id, original_url, uri in parsed_sources:
        prior_original = staged_originals.get(source_id)
        if prior_original is not None and _normalized_url(prior_original) != _normalized_url(
            original_url
        ):
            raise ValueError(
                f"provenance source ID {source_id!r} names multiple original pages in {path}"
            )
        current = staged_sources.get(source_id)
        if current is not None and current.uri != uri:
            approved_alias = _CURATED_ARCHIVE_PAGE_ALIASES.get(source_id)
            if (
                approved_alias is None
                or current.uri != approved_alias[0]
                or _normalized_url(original_url) != _normalized_url(approved_alias[1])
            ):
                raise ValueError(
                    f"provenance source ID {source_id!r} conflicts with a different page in {path}"
                )
        staged_originals[source_id] = original_url
        staged_sources.setdefault(source_id, Source(source_id, uri))

    # Validate the complete catalog before mutating process-wide registry state.
    _CATALOG_ORIGINAL_URLS.update(staged_originals)
    SOURCES.update(staged_sources)


_schema_root = Path(__file__).resolve().parents[2]
for _catalog_name in ("evidence.json", "focused-properties.json"):
    _add_catalog_sources(_schema_root / "schema" / "sources" / "sdk" / _catalog_name)
