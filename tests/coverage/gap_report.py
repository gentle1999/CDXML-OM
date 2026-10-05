"""Report DTD pairs and element lifecycles without execution evidence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import cast

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CATALOG_PATH = PROJECT_ROOT / "tests" / "coverage" / "feature_cases.json"
DTD_PATH = PROJECT_ROOT / "schema" / "sources" / "revvity-CDXML.dtd"


def build_gap_report() -> dict[str, object]:
    """Build a source-derived gap inventory; declarations are never counted as passes."""
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    from tools.schema_importer.dtd_importer import import_dtd

    from cdxml_om._generated.schema_metadata import OBJECT_METADATA

    dtd = import_dtd(str(DTD_PATH))
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    if not isinstance(catalog, dict):
        raise ValueError("feature case catalog must be a JSON object")

    dtd_pairs = {
        (element.xml_name, attribute.name)
        for element in dtd.dtd_elements
        for attribute in element.attributes
    }
    mapped_pairs = {
        (metadata.xml_tag, prop.xml_name)
        for metadata in OBJECT_METADATA.values()
        for prop in metadata.properties.values()
        if prop.storage == "attribute"
    }
    recipe_rows = cast(list[dict[str, object]], catalog.get("cases", []))
    recipe_pairs = {
        (cast(str, row["owner_tag"]), cast(str, row["xml_attribute"])) for row in recipe_rows
    }
    element_rows = cast(list[dict[str, object]], catalog.get("element_cases", []))
    element_cases = {cast(str, row["xml_name"]): row for row in element_rows}
    child_lifecycle_assertions = {"element_creation", "element_removal", "element_round_trip"}
    root_lifecycle_assertions = {"root_creation", "root_mutation", "element_round_trip"}

    unmodeled_pairs = sorted(dtd_pairs - mapped_pairs)
    mapped_without_recipe = sorted(mapped_pairs - recipe_pairs)
    recipes_outside_dtd = sorted(recipe_pairs - dtd_pairs)
    dtd_tags = {element.xml_name for element in dtd.dtd_elements}
    modeled_tags = {metadata.xml_tag for metadata in OBJECT_METADATA.values()}
    unmodeled_elements = sorted(dtd_tags - modeled_tags)
    elements_without_case = sorted(dtd_tags - set(element_cases))
    elements_without_lifecycle = sorted(
        tag
        for tag in dtd_tags
        if not (root_lifecycle_assertions if tag == "CDXML" else child_lifecycle_assertions)
        <= set(cast(list[str], element_cases.get(tag, {}).get("assertions", [])))
    )

    return {
        "format": "cdxml-om-full-schema-gap-report",
        "format_version": 1,
        "dtd_sha256": dtd.source.sha256,
        "evidence_status": "declarations are not execution evidence",
        "inventory": {
            "elements": len(dtd_tags),
            "owner_attribute_pairs": len(dtd_pairs),
            "root_cdxml_attributes": sum(1 for owner, _ in dtd_pairs if owner == "CDXML"),
        },
        "declared_cases": {
            "mapped_owner_attribute_recipes": len(recipe_pairs),
            "element_case_rows": len(element_cases),
            "element_create_remove_round_trip_rows": sum(
                child_lifecycle_assertions <= set(cast(list[str], row.get("assertions", [])))
                for row in element_rows
                if row.get("xml_name") != "CDXML"
            ),
            "root_create_mutate_round_trip_rows": sum(
                root_lifecycle_assertions <= set(cast(list[str], row.get("assertions", [])))
                for row in element_rows
                if row.get("xml_name") == "CDXML"
            ),
        },
        "unverified_gaps": {
            "unmodeled_elements": unmodeled_elements,
            "elements_without_case_row": elements_without_case,
            "elements_without_create_remove_round_trip_case": elements_without_lifecycle,
            "unmapped_owner_attribute_pairs": [
                {"owner_xml_name": owner, "xml_name": name} for owner, name in unmodeled_pairs
            ],
            "mapped_pairs_without_recipe": [
                {"owner_xml_name": owner, "xml_name": name} for owner, name in mapped_without_recipe
            ],
            "recipes_outside_dtd": [
                {"owner_xml_name": owner, "xml_name": name} for owner, name in recipes_outside_dtd
            ],
        },
        "execution_evidence": {
            "provided": False,
            "verified_owner_attribute_pairs": None,
            "verified_element_lifecycles": None,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--summary",
        action="store_true",
        help="omit the explicit list of DTD pairs without a static typed mapping",
    )
    arguments = parser.parse_args()
    report = build_gap_report()
    if arguments.summary:
        gaps = cast(dict[str, object], report["unverified_gaps"])
        report["unverified_gaps"] = {
            key: len(value) if isinstance(value, list) else value for key, value in gaps.items()
        }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
