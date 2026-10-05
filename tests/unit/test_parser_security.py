"""Security and source-retention checks for public CDXML parsing APIs."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from lxml import etree

from cdxml_om import CDXMLDocument, ParseError
from cdxml_om.io import cdxml as cdxml_io


class _DenyExternalResolution(etree.Resolver):
    def __init__(self) -> None:
        self.attempts: list[tuple[str, str | None]] = []

    def resolve(self, url: str, pubid: str | None, context: object) -> etree._InputDocument:
        self.attempts.append((url, pubid))
        return self.resolve_string("", context)


def _spy_on_configured_parser(monkeypatch: pytest.MonkeyPatch) -> _DenyExternalResolution:
    original_factory = cdxml_io._parser
    resolver = _DenyExternalResolution()

    def parser_with_deny_resolver() -> etree.XMLParser:
        parser = original_factory()
        parser.resolvers.add(resolver)
        return parser

    monkeypatch.setattr(cdxml_io, "_parser", parser_with_deny_resolver)
    return resolver


def _label_text(document: CDXMLDocument) -> str | None:
    children = document.root.children
    assert len(children) == 1
    return children[0].text


def _outside_root_nodes(root: etree._Element, *, before: bool) -> tuple[tuple[str, ...], ...]:
    node = root.getprevious() if before else root.getnext()
    siblings: list[etree._Element] = []
    while node is not None:
        siblings.append(node)
        node = node.getprevious() if before else node.getnext()
    if before:
        siblings.reverse()

    result: list[tuple[str, ...]] = []
    for sibling in siblings:
        if isinstance(sibling, etree._Comment):
            result.append(("comment", sibling.text or ""))
        elif isinstance(sibling, etree._ProcessingInstruction):
            result.append(("pi", sibling.target, sibling.text or ""))
    return tuple(result)


def test_external_local_file_entity_is_not_read_or_expanded(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    secret = "local-entity-secret-content"
    secret_path = tmp_path / "secret.txt"
    secret_path.write_text(secret, encoding="utf-8")
    resolver = _spy_on_configured_parser(monkeypatch)
    source = (
        f'<!DOCTYPE CDXML [<!ENTITY local SYSTEM "{secret_path.as_uri()}">]><CDXML>&local;</CDXML>'
    )

    document = CDXMLDocument.from_string(source)

    assert resolver.attempts == []
    assert document.tree.getroot().text is None
    assert len(document.tree.getroot()) == 1
    assert isinstance(document.tree.getroot()[0], etree._Entity)
    assert document.tree.getroot()[0].name == "local"
    serialized = document.to_string()
    assert "&local;" in serialized
    assert secret not in serialized


def test_remote_external_dtd_is_never_requested(monkeypatch: pytest.MonkeyPatch) -> None:
    resolver = _spy_on_configured_parser(monkeypatch)
    remote_dtd = "http://127.0.0.1:9/blocked-cdxml.dtd"
    document = CDXMLDocument.from_string(f'<!DOCTYPE CDXML SYSTEM "{remote_dtd}"><CDXML/>')

    assert resolver.attempts == []
    assert document.root.xml_tag == "CDXML"
    assert remote_dtd in document.to_string()


def test_internal_entity_declaration_and_reference_remain_opaque() -> None:
    source = '<!DOCTYPE CDXML [<!ENTITY label "internal-entity-marker">]><CDXML>&label;</CDXML>'

    document = CDXMLDocument.from_string(source)

    root = document.tree.getroot()
    assert root.text is None
    assert isinstance(root[0], etree._Entity)
    assert root[0].name == "label"
    serialized = document.to_string()
    assert re.search(
        r'<!ENTITY\s+label\s+[\'"]internal-entity-marker[\'"]\s*>',
        serialized,
    )
    assert "&label;" in serialized

    reparsed = CDXMLDocument.from_string(serialized)
    assert reparsed.tree.getroot().text is None
    assert "&label;" in reparsed.to_string()


def test_external_parameter_entity_is_not_loaded_or_is_rejected_safely(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    external_subset = tmp_path / "parameters.ent"
    external_subset.write_text(
        '<!ENTITY fromParameter "parameter-entity-marker">', encoding="utf-8"
    )
    resolver = _spy_on_configured_parser(monkeypatch)
    source = (
        "<!DOCTYPE CDXML ["
        f'<!ENTITY % definitions SYSTEM "{external_subset.as_uri()}">'
        "%definitions;]><CDXML>&fromParameter;</CDXML>"
    )

    try:
        document = CDXMLDocument.from_string(source)
    except ParseError:
        assert resolver.attempts == []
        return

    assert resolver.attempts == []
    assert document.tree.getroot().text is None
    assert "&fromParameter;" in document.to_string()


def test_exponential_entity_is_not_expanded_or_is_rejected_safely() -> None:
    definitions = ['<!ENTITY e0 "x">']
    for index in range(1, 9):
        references = "".join(f"&e{index - 1};" for _ in range(5))
        definitions.append(f'<!ENTITY e{index} "{references}">')
    source = f"<!DOCTYPE CDXML [{''.join(definitions)}]><CDXML>&e8;</CDXML>"

    try:
        document = CDXMLDocument.from_string(source)
    except ParseError:
        return

    root = document.tree.getroot()
    assert root.text is None
    assert len(root) == 1
    assert isinstance(root[0], etree._Entity)
    assert root[0].name == "e8"
    assert "&e8;" in document.to_string()


def test_comments_processing_instructions_and_cdata_survive_serialization() -> None:
    cdata_text = "CDATA marker with <markup> & punctuation"
    source = (
        "<!--before-root--><?before-root data?>"
        f"<CDXML><label><![CDATA[{cdata_text}]]></label></CDXML>"
        "<!--after-root--><?after-root data?>"
    )
    expected_before = (("comment", "before-root"), ("pi", "before-root", "data"))
    expected_after = (("comment", "after-root"), ("pi", "after-root", "data"))

    document = CDXMLDocument.from_string(source)
    serialized = document.to_string()

    assert _outside_root_nodes(document.tree.getroot(), before=True) == expected_before
    assert _outside_root_nodes(document.tree.getroot(), before=False) == expected_after
    assert document.root.children[0].text == cdata_text
    assert f"<![CDATA[{cdata_text}]]>" in serialized

    reparsed = CDXMLDocument.from_string(serialized)
    assert _outside_root_nodes(reparsed.tree.getroot(), before=True) == expected_before
    assert _outside_root_nodes(reparsed.tree.getroot(), before=False) == expected_after
    assert reparsed.root.children[0].text == cdata_text
    assert f"<![CDATA[{cdata_text}]]>" in reparsed.to_string()


def test_unicode_string_ignores_stale_non_utf8_declaration() -> None:
    source = '<?xml version="1.0" encoding="ISO-8859-1" ?><CDXML><label>café</label></CDXML>'

    document = CDXMLDocument.from_string(source)

    assert _label_text(document) == "café"
    serialized = document.to_string()
    assert "café" in serialized
    assert "encoding='UTF-8'" in serialized or 'encoding="UTF-8"' in serialized


def test_declared_byte_encoding_is_honored_for_string_and_file_inputs(tmp_path: Path) -> None:
    source = (
        '<?xml version="1.0" encoding="ISO-8859-1" ?><CDXML><label>café</label></CDXML>'
    ).encode("iso-8859-1")
    source_path = tmp_path / "latin-1.cdxml"
    source_path.write_bytes(source)

    from_bytes = CDXMLDocument.from_string(source)
    from_file = CDXMLDocument.from_file(source_path)

    assert _label_text(from_bytes) == "café"
    assert _label_text(from_file) == "café"
    serialized = from_file.to_string()
    assert "café" in serialized
    assert CDXMLDocument.from_string(serialized).root.children[0].text == "café"


@pytest.mark.parametrize(
    "source",
    [
        "<CDXML><label></CDXML>",
        "<not-CDXML/>",
        b'<?xml version="1.0" encoding="UTF-8"?><CDXML>\xff</CDXML>',
        "<CDXML>\ud800</CDXML>",
    ],
    ids=("malformed-xml", "invalid-root", "invalid-utf8", "invalid-unicode-string"),
)
def test_malformed_root_and_invalid_unicode_raise_parse_error(
    source: str | bytes,
) -> None:
    with pytest.raises(ParseError):
        CDXMLDocument.from_string(source)
