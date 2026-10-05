"""Test-only pytest plugin for exercising feature-run result states."""

from __future__ import annotations

import json
import os

import pytest


def _statuses() -> dict[str, str]:
    raw = os.environ.get("CDXML_OM_FEATURE_STATUSES", "{}")
    value = json.loads(raw)
    assert isinstance(value, dict)
    return {str(node_id): str(status) for node_id, status in value.items()}


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    statuses = _statuses()
    for item in items:
        if statuses.get(item.nodeid) == "skipped":
            item.add_marker(pytest.mark.skip(reason="feature status regression test"))


@pytest.fixture(autouse=True)
def _inject_feature_failure(request: pytest.FixtureRequest) -> None:
    if _statuses().get(request.node.nodeid) == "failed":
        pytest.fail("injected feature-test failure")
