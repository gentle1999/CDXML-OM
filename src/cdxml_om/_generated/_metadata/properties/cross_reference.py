# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Properties grouped by logical schema owner: cross_reference."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..provenance.revvity_dtd import (
    P_76bd1f928b74e0f8bff9,
    P_297a12b9999566849a17,
    P_418a9bd27d12d95f908e,
    P_f50651f731d96b9a0d07,
)
from ..provenance.sdk_page_crossreference import (
    P_4c98e65f8793d9eb5a33,
    P_7b81c5ba450721332806,
    P_2108c535fc606d1f4399,
    P_2630f609af8368ef4a04,
)
from ..types import PropertyMetadata

PROPERTY_METADATA_GROUP: Final[Mapping[str, PropertyMetadata]] = MappingProxyType(
    {
        "dtd.crossreference.cross_reference_container": PropertyMetadata(
            owners=("cross_reference",),
            name="cross_reference_container",
            xml_name="CrossReferenceContainer",
            storage="attribute",
            cdx_id=3840,
            cdx_constant="kCDXProp_CrossReference_Container",
            datatype="string",
            codec="string",
            required=False,
            default=None,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_f50651f731d96b9a0d07,
                P_4c98e65f8793d9eb5a33,
            ),
            xml_aliases=(),
        ),
        "dtd.crossreference.cross_reference_document": PropertyMetadata(
            owners=("cross_reference",),
            name="cross_reference_document",
            xml_name="CrossReferenceDocument",
            storage="attribute",
            cdx_id=3841,
            cdx_constant="kCDXProp_CrossReference_Document",
            datatype="string",
            codec="string",
            required=False,
            default=None,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_76bd1f928b74e0f8bff9,
                P_2630f609af8368ef4a04,
            ),
            xml_aliases=(),
        ),
        "dtd.crossreference.cross_reference_identifier": PropertyMetadata(
            owners=("cross_reference",),
            name="cross_reference_identifier",
            xml_name="CrossReferenceIdentifier",
            storage="attribute",
            cdx_id=3842,
            cdx_constant="kCDXProp_CrossReference_Identifier",
            datatype="string",
            codec="string",
            required=True,
            default=None,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_418a9bd27d12d95f908e,
                P_2108c535fc606d1f4399,
            ),
            xml_aliases=(),
        ),
        "dtd.crossreference.cross_reference_sequence": PropertyMetadata(
            owners=("cross_reference",),
            name="cross_reference_sequence",
            xml_name="CrossReferenceSequence",
            storage="attribute",
            cdx_id=3843,
            cdx_constant="kCDXProp_CrossReference_Sequence",
            datatype="string",
            codec="string",
            required=True,
            default=None,
            cardinality="one",
            reference_target=None,
            reference_many=False,
            enum=None,
            status="known",
            provenance=(
                P_297a12b9999566849a17,
                P_7b81c5ba450721332806,
            ),
            xml_aliases=(),
        ),
    }
)
