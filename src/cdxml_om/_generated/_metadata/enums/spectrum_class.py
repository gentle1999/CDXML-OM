# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the SpectrumClass enum spec."""

from __future__ import annotations

from ..provenance.revvity_dtd import P_8fb81f771a122879181b
from ..provenance.sdk_page_spectrum import P_26efc89fc140f7bef2ae
from ..types import EnumMetadata, EnumValueMetadata

ENUM_METADATA_ENTRY = EnumMetadata(
    python_name="SpectrumClass",
    underlying_datatype="string",
    representation="str",
    values=(
        EnumValueMetadata(
            name="UNKNOWN",
            xml_value="Unknown",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="CHROMATOGRAM",
            xml_value="Chromatogram",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="INFRARED",
            xml_value="Infrared",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="UV_VIS",
            xml_value="UVVis",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="X_RAY_DIFFRACTION",
            xml_value="XRayDiffraction",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="MASS_SPECTRUM",
            xml_value="MassSpectrum",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="NMR",
            xml_value="NMR",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="RAMAN",
            xml_value="Raman",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="FLUORESCENCE",
            xml_value="Fluorescence",
            cdx_value=None,
        ),
        EnumValueMetadata(
            name="ATOMIC",
            xml_value="Atomic",
            cdx_value=None,
        ),
    ),
    status="known",
    provenance=(
        P_8fb81f771a122879181b,
        P_26efc89fc140f7bef2ae,
    ),
)
