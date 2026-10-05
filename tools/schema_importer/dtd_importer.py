"""Import a local CDXML DTD as syntax evidence without semantic guessing."""

from __future__ import annotations

import io
import re
from collections.abc import Iterator
from typing import Protocol, cast

from lxml import etree

from tools.schema_importer.candidate import (
    CandidateDocument,
    ContentModelCandidate,
    DTDAttributeCandidate,
    DTDElementCandidate,
)
from tools.schema_importer.common import read_local_input
from tools.schema_importer.errors import ImporterError

_COMMENT = re.compile(rb"<!--.*?-->", re.DOTALL)
_XML_DECLARATION = re.compile(rb"\A\s*<\?xml\s+([^?]*)\?>", re.IGNORECASE)
_XML_ENCODING = re.compile(r"\bencoding\s*=\s*(['\"])(.*?)\1", re.IGNORECASE)
_ENTITY_DECLARATION = re.compile(rb"\A<!\s*ENTITY\b", re.IGNORECASE)
_DOCTYPE_DECLARATION = re.compile(rb"\A<!\s*DOCTYPE\b", re.IGNORECASE)
_EXTERNAL_KEYWORD = re.compile(rb"\b(?:SYSTEM|PUBLIC)\b", re.IGNORECASE)
_SPECIAL_ENUM_TOKENS: tuple[tuple[bytes, bytes], ...] = (
    (b"+", b"CDXML_IMPORTER_ENUM_PLUS_TOKEN"),
    (b"-", b"CDXML_IMPORTER_ENUM_MINUS_TOKEN"),
    (b"?", b"CDXML_IMPORTER_ENUM_QUESTION_TOKEN"),
)


class _ContentDeclaration(Protocol):
    @property
    def name(self) -> str | None: ...

    @property
    def type(self) -> str | None: ...

    @property
    def occur(self) -> str | None: ...

    @property
    def left(self) -> _ContentDeclaration | None: ...

    @property
    def right(self) -> _ContentDeclaration | None: ...


class _AttributeDeclaration(Protocol):
    @property
    def name(self) -> str | None: ...

    @property
    def type(self) -> str | None: ...

    @property
    def default(self) -> str | None: ...

    @property
    def default_value(self) -> str | None: ...

    def itervalues(self) -> Iterator[str]: ...


class _ElementDeclaration(Protocol):
    @property
    def name(self) -> str | None: ...

    @property
    def type(self) -> str | None: ...

    @property
    def content(self) -> _ContentDeclaration | None: ...

    def iterattributes(self) -> Iterator[object]: ...


def _iter_declarations(raw: bytes) -> tuple[bytes, ...]:
    """Yield quote-aware declaration bytes, skipping comments."""
    source = _COMMENT.sub(b"", raw)
    declarations: list[bytes] = []
    cursor = 0
    while True:
        start = source.find(b"<!", cursor)
        if start < 0:
            break
        quote: int | None = None
        end = start + 2
        while end < len(source):
            char = source[end]
            if quote is not None:
                if char == quote:
                    quote = None
            elif char in {ord('"'), ord("'")}:
                quote = char
            elif char == ord(">"):
                break
            end += 1
        if end >= len(source):
            break
        declarations.append(source[start : end + 1])
        cursor = end + 1
    return tuple(declarations)


def _reject_external_declarations(raw: bytes, source_path: str) -> None:
    # Parameter entities can synthesize declarations during DTD parsing. This
    # offline importer rejects them all, including references hidden in an
    # internal entity value; the pinned project DTD does not use parameter entities.
    source_without_comments = _COMMENT.sub(b"", raw)
    if b"%" in source_without_comments:
        raise ImporterError(
            "DTD_PARAMETER_ENTITY",
            "parameter entity declarations/references are refused by the offline importer",
            source_path,
        )
    for declaration in _iter_declarations(raw):
        if (
            _ENTITY_DECLARATION.match(declaration) or _DOCTYPE_DECLARATION.match(declaration)
        ) and _EXTERNAL_KEYWORD.search(declaration):
            raise ImporterError(
                "EXTERNAL_DTD_REFERENCE",
                "external SYSTEM/PUBLIC DTD and entity declarations are refused offline",
                source_path,
            )


def _normalize_legacy_enum_tokens(raw: bytes, source_path: str) -> tuple[bytes, tuple[str, ...]]:
    normalized = raw
    normalizations: list[str] = []
    for token, placeholder in _SPECIAL_ENUM_TOKENS:
        if placeholder in normalized:
            raise ImporterError(
                "DTD_RESERVED_TOKEN",
                "input already contains a parser-reserved enum token",
                source_path,
            )
        pattern = rb"(\|\s*)" + re.escape(token) + rb"\s*(?=\||\))"

        def replace(match: re.Match[bytes], replacement: bytes = placeholder) -> bytes:
            return match.group(1) + replacement

        normalized, count = re.subn(
            pattern,
            replace,
            normalized,
        )
        if count:
            token_text = token.decode("ascii")
            normalizations.append(
                f"Parser-only DTD enum token escape for {token_text!r}; "
                "candidate values restore the source token."
            )
    return normalized, tuple(normalizations)


def _restore_enum_token(value: str) -> str:
    replacements = {
        placeholder.decode("ascii"): token.decode("ascii")
        for token, placeholder in _SPECIAL_ENUM_TOKENS
    }
    return replacements.get(value, value)


def _model_node(node: _ContentDeclaration) -> ContentModelCandidate:
    children: list[ContentModelCandidate] = []
    for child in (node.left, node.right):
        if child is not None:
            children.append(_model_node(child))
    occurrence = node.occur or "once"
    return ContentModelCandidate(
        kind=node.type or "unknown",
        occurrence=occurrence,
        name=node.name,
        children=tuple(children),
    )


def _child_names(model: ContentModelCandidate | None) -> tuple[str, ...]:
    if model is None:
        return ()
    names: list[str] = []

    def visit(node: ContentModelCandidate) -> None:
        if node.kind == "element" and node.name is not None and node.name not in names:
            names.append(node.name)
        for child in node.children:
            visit(child)

    visit(model)
    return tuple(names)


def _element_candidate(declaration: _ElementDeclaration) -> DTDElementCandidate:
    element_name = declaration.name
    if element_name is None:
        raise ImporterError("DTD_DECLARATION", "element declaration has no name", "DTD")
    content = declaration.content
    model = _model_node(content) if content is not None else None
    attributes: list[DTDAttributeCandidate] = []
    for raw_attribute in declaration.iterattributes():
        attribute = cast(_AttributeDeclaration, raw_attribute)
        attribute_name = attribute.name
        if attribute_name is None:
            raise ImporterError(
                "DTD_DECLARATION", "attribute declaration has no name", f"<!ATTLIST {element_name}>"
            )
        enum_values = tuple(_restore_enum_token(value) for value in attribute.itervalues())
        default_kind = attribute.default or "none"
        attributes.append(
            DTDAttributeCandidate(
                name=attribute_name,
                declared_type=attribute.type or "unknown",
                required=default_kind == "required",
                default_kind=default_kind,
                default_value=attribute.default_value,
                enum_values=enum_values,
                locator=f"<!ATTLIST {element_name} {attribute_name}>",
            )
        )
    return DTDElementCandidate(
        xml_name=element_name,
        declaration_type=declaration.type or "undefined",
        content_model=model,
        children=_child_names(model),
        attributes=tuple(attributes),
        locator=f"<!ELEMENT {element_name}>",
    )


def import_dtd(path_text: str) -> CandidateDocument:
    """Parse an explicitly supplied local DTD and retain declaration evidence."""
    raw, source = read_local_input(path_text, "dtd")
    try:
        decoded = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ImporterError("DTD_ENCODING", "offline DTD inputs must be UTF-8", path_text) from exc
    if "\x00" in decoded:
        raise ImporterError("DTD_ENCODING", "NUL bytes are not permitted in DTD input", path_text)
    declaration_match = _XML_DECLARATION.match(raw)
    normalizations: list[str] = []
    if declaration_match is not None:
        declaration_text = declaration_match.group(1).decode("ascii", errors="ignore")
        encoding_match = _XML_ENCODING.search(declaration_text)
        if encoding_match is not None and encoding_match.group(2).casefold() not in {
            "utf-8",
            "utf8",
        }:
            raise ImporterError("DTD_ENCODING", "offline DTD inputs must declare UTF-8", path_text)
        normalizations.append(
            "XML declaration removed for the external-subset DTD parser; "
            "original bytes remain identified by source.sha256."
        )
    _reject_external_declarations(raw, path_text)
    without_xml_declaration = _XML_DECLARATION.sub(b"", raw, count=1)
    normalized, enum_normalizations = _normalize_legacy_enum_tokens(
        without_xml_declaration, path_text
    )
    normalizations.extend(enum_normalizations)
    try:
        parsed = etree.DTD(io.BytesIO(normalized))
    except (etree.DTDParseError, OSError) as exc:
        log = getattr(exc, "error_log", None)
        detail = str(log if log is not None else exc)
        raise ImporterError("DTD_PARSE", detail, path_text) from exc
    elements = tuple(
        _element_candidate(cast(_ElementDeclaration, item)) for item in parsed.iterelements()
    )
    if not elements:
        raise ImporterError("DTD_EMPTY", "input has no element declarations", path_text)
    return CandidateDocument(
        source=source,
        scope="dtd",
        normalizations=tuple(normalizations),
        dtd_elements=elements,
    )
