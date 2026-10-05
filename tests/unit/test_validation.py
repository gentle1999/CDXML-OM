"""Structured validation tests independent from lazy wrapper access."""

from __future__ import annotations

from cdxml_om import CDXMLDocument


def test_validation_reports_duplicate_ids_dangling_refs_and_invalid_values() -> None:
    document = CDXMLDocument.from_string(
        '<CDXML><page id="1"><fragment id="2"><n id="3" Charge="not-int"/>'
        '<n id="3"/><b id="4" B="3" Order="not-an-order"/>'
        "</fragment></page></CDXML>"
    )

    report = document.validate()
    found = {(issue.code, issue.property_id) for issue in report.errors}

    assert not report.is_valid
    assert {
        ("duplicate-id", "common.id"),
        ("invalid-value", "node.charge"),
        ("missing-required-property", "bond.end"),
        ("invalid-value", "bond.order"),
        ("ambiguous-reference", "bond.begin"),
    } <= found


def test_validation_reports_wrong_reference_target_and_invalid_parent() -> None:
    document = CDXMLDocument.from_string(
        '<CDXML><page id="1"><fragment id="2"><n id="3"/>'
        '<b id="5" B="4" E="3"/></fragment><fragment id="4">'
        "</fragment></page></CDXML>"
    )
    wrong_target = document.validate()

    assert any(
        issue.code == "wrong-reference-target" and issue.property_id == "bond.begin"
        for issue in wrong_target.errors
    )

    invalid_parent = CDXMLDocument.from_string('<CDXML><n id="3"/></CDXML>').validate()
    assert any(issue.code == "invalid-parent" for issue in invalid_parent.errors)


def test_valid_document_has_an_empty_immutable_report() -> None:
    document = CDXMLDocument.from_string(
        '<CDXML><page id="1"><fragment id="2"><n id="3"/><n id="4"/>'
        '<b id="5" B="3" E="4"/></fragment></page></CDXML>'
    )

    report = document.validate()
    assert report.is_valid
    assert report.issues == ()
    assert report.errors == ()
    assert report.warnings == ()
