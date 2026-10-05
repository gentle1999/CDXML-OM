# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the ConstraintType enum spec."""

from __future__ import annotations

from ..provenance.revvity_dtd import P_f7ab997306e690a17b5f
from ..provenance.sdk_page_constraint import P_4561a1e5bae152c58cf8
from ..types import EnumMetadata, EnumValueMetadata

ENUM_METADATA_ENTRY = EnumMetadata(
    python_name="ConstraintType",
    underlying_datatype="string",
    representation="str",
    values=(
        EnumValueMetadata(
            name="UNKNOWN",
            xml_value="Unknown",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="DISTANCE",
            xml_value="Distance",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="ANGLE",
            xml_value="Angle",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="EXCLUSION_SPHERE",
            xml_value="ExclusionSphere",
            cdx_value=None,
        ),
    ),
    status="known",
    provenance=(
        P_f7ab997306e690a17b5f,
        P_4561a1e5bae152c58cf8,
    ),
)
