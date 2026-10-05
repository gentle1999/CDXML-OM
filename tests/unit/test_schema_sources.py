"""Build-time provenance source identity safeguards."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from tools.schema_compiler.sources import (
    SOURCES,
    _add_catalog_sources,  # pyright: ignore[reportPrivateUsage]
)


def _catalog(path: Path, sources: list[dict[str, str]]) -> Path:
    path.write_text(json.dumps({"sources": sources}), encoding="utf-8")
    return path


def test_source_catalog_rejects_duplicate_ids_before_registry_mutation(tmp_path: Path) -> None:
    source_id = "test_duplicate_source"
    source = {"id": source_id, "original_url": "https://example.test/page"}
    path = _catalog(tmp_path / "duplicate.json", [source, source])

    with pytest.raises(ValueError, match="duplicate provenance source ID"):
        _add_catalog_sources(path)

    assert source_id not in SOURCES


def test_source_catalog_rejects_unapproved_reuse_of_curated_id(tmp_path: Path) -> None:
    path = _catalog(
        tmp_path / "conflict.json",
        [
            {
                "id": "sdk_document",
                "original_url": "https://example.test/unrelated-documentation",
                "snapshot_url": (
                    "https://web.archive.org/web/20200101000000/"
                    "https://example.test/unrelated-documentation"
                ),
            }
        ],
    )

    with pytest.raises(ValueError, match="multiple original pages|conflicts with a different page"):
        _add_catalog_sources(path)


def test_source_catalog_rejects_snapshot_for_a_different_original_page(tmp_path: Path) -> None:
    source_id = "test_mismatched_snapshot"
    path = _catalog(
        tmp_path / "mismatch.json",
        [
            {
                "id": source_id,
                "original_url": "https://example.test/original",
                "snapshot_url": "https://web.archive.org/web/20200101000000/https://evil.test/page",
            }
        ],
    )

    with pytest.raises(ValueError, match="does not identify its original page"):
        _add_catalog_sources(path)

    assert source_id not in SOURCES
