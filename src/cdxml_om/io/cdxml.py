"""Secure full-tree CDXML parsing and serialization using lxml."""

from __future__ import annotations

import re
from io import BytesIO
from os import PathLike
from pathlib import Path

from lxml import etree

from cdxml_om.core.errors import ParseError

_XML_ENCODING = re.compile(r"(\bencoding\s*=\s*)(['\"])[^'\"]*\2", re.IGNORECASE)


def _parser() -> etree.XMLParser:
    return etree.XMLParser(
        resolve_entities=False,
        load_dtd=False,
        no_network=True,
        recover=False,
        remove_blank_text=False,
        remove_comments=False,
        remove_pis=False,
        strip_cdata=False,
    )


def _unicode_source_bytes(source: str) -> bytes:
    """Encode decoded text as UTF-8 without trusting a stale declaration."""
    prefix = "\ufeff" if source.startswith("\ufeff") else ""
    text = source[len(prefix) :]
    if text.startswith("<?xml"):
        declaration_end = text.find("?>")
        if declaration_end >= 0:
            declaration = text[: declaration_end + 2]
            declaration = _XML_ENCODING.sub(r'\1"UTF-8"', declaration, count=1)
            text = declaration + text[declaration_end + 2 :]
    return (prefix + text).encode("utf-8")


def parse_cdxml_string(source: str | bytes | bytearray) -> etree.ElementTree:
    """Parse bytes as declared or Unicode text as UTF-8, without external access."""
    try:
        raw = _unicode_source_bytes(source) if isinstance(source, str) else bytes(source)
        return etree.parse(BytesIO(raw), parser=_parser())
    except (etree.XMLSyntaxError, ValueError, OSError, UnicodeError) as exc:
        raise ParseError(f"could not parse CDXML input: {exc}") from exc


def parse_cdxml_file(source: str | PathLike[str] | Path) -> etree.ElementTree:
    """Parse a local file, letting lxml decode its original byte encoding."""
    path = Path(source)
    try:
        with path.open("rb") as stream:
            return etree.parse(stream, parser=_parser())
    except (etree.XMLSyntaxError, ValueError, OSError, UnicodeError) as exc:
        raise ParseError(f"could not parse CDXML file {path}: {exc}") from exc


def serialize_cdxml(
    tree: etree.ElementTree,
    *,
    encoding: str = "unicode",
    xml_declaration: bool = True,
    pretty_print: bool = False,
) -> str:
    """Serialize the full tree; this is structural, not byte-identical output."""
    if encoding == "unicode" and not xml_declaration:
        return etree.tostring(
            tree,
            encoding="unicode",
            pretty_print=pretty_print,
        )
    if encoding == "unicode":
        result = etree.tostring(
            tree,
            encoding="UTF-8",
            xml_declaration=True,
            pretty_print=pretty_print,
        )
        return result.decode("utf-8")
    result = etree.tostring(
        tree,
        encoding=encoding,
        xml_declaration=xml_declaration,
        pretty_print=pretty_print,
    )
    return result.decode(encoding)


def write_cdxml(
    tree: etree.ElementTree,
    destination: str | PathLike[str] | Path,
    *,
    encoding: str = "UTF-8",
    xml_declaration: bool = True,
    pretty_print: bool = False,
) -> None:
    """Write a full tree with an XML declaration matching the output bytes."""
    if encoding == "unicode":
        raise ValueError("file output requires a concrete XML encoding")
    path = Path(destination)
    result = etree.tostring(
        tree,
        encoding=encoding,
        xml_declaration=xml_declaration,
        pretty_print=pretty_print,
    )
    path.write_bytes(result)


__all__ = ["parse_cdxml_file", "parse_cdxml_string", "serialize_cdxml", "write_cdxml"]
