# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Properties grouped by logical schema owner: object_tag."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..provenance.revvity_dtd import P_067365a99946881b27f2
from ..provenance.sdk_page_objecttag import P_7eb5bf86db3fa8f3b08e
from ..types import PropertyMetadata

PROPERTY_METADATA_GROUP: Final[Mapping[str, PropertyMetadata]] = MappingProxyType(
    {
        "dtd.objecttag.tracking": PropertyMetadata(
            owners=("object_tag",),
            name="tracking",
            xml_name="Tracking",
            storage="attribute",
            cdx_id=3331,
            cdx_constant="kCDXProp_ObjectTag_Tracking",
            datatype="boolean",
            codec="bool",
            required=False,
            default=True,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_067365a99946881b27f2,
                P_7eb5bf86db3fa8f3b08e,
            ),
            xml_aliases=(),
        ),
    }
)
