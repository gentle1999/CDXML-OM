# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Metadata for the Page ObjectSpec."""

from __future__ import annotations

from types import MappingProxyType

from ..properties import PROPERTY_METADATA
from ..provenance.revvity_dtd import P_d804e630c1b17793a2de
from ..types import ChildMetadata, ObjectMetadata

OBJECT_METADATA_ENTRY = ObjectMetadata(
    python_name="Page",
    xml_tag="page",
    cdx_id=32769,
    cdx_constant="kCDXObj_Page",
    category="drawing_space",
    id_scope="document",
    allowed_parents=("cdxml_root", "table"),
    status="known",
    children=(
        ChildMetadata(
            object_type="text",
            collection_name="texts",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="fragment",
            collection_name="fragments",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="group",
            collection_name="groups",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="graphic",
            collection_name="graphics",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="alt_group",
            collection_name="altgroups",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="curve",
            collection_name="curves",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="reaction_step",
            collection_name="steps",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="reaction_scheme",
            collection_name="schemes",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="spectrum",
            collection_name="spectrums",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="embedded_object",
            collection_name="embeddedobjects",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="sequence",
            collection_name="sequences",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="cross_reference",
            collection_name="crossreferences",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="splitter",
            collection_name="splitters",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="table",
            collection_name="tables",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="bracketed_group",
            collection_name="bracketedgroups",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="border",
            collection_name="borders",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="geometry",
            collection_name="geometrys",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="constraint",
            collection_name="constraints",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="tlc_plate",
            collection_name="tlcplates",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="gep_plate",
            collection_name="gepplates",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="chemical_property",
            collection_name="chemicalpropertys",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="arrow",
            collection_name="arrows",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="bio_shape",
            collection_name="bioshapes",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="stoichiometry_grid",
            collection_name="stoichiometrygrids",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="plasmid_map",
            collection_name="plasmidmaps",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="object_tag",
            collection_name="objecttags",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="annotation",
            collection_name="annotations",
            min_occurs=0,
            max_occurs=None,
        ),
        ChildMetadata(
            object_type="rlogic",
            collection_name="rlogics",
            min_occurs=0,
            max_occurs=None,
        ),
    ),
    properties=MappingProxyType(
        {
            "dtd.CDXML.alpha": PROPERTY_METADATA["dtd.CDXML.alpha"],
            "dtd.page.z": PROPERTY_METADATA["dtd.page.z"],
            "dtd.page.width": PROPERTY_METADATA["dtd.page.width"],
            "dtd.page.splitter_positions": PROPERTY_METADATA["dtd.page.splitter_positions"],
            "dtd.page.print_trim_marks": PROPERTY_METADATA["dtd.page.print_trim_marks"],
            "dtd.page.page_overlap": PROPERTY_METADATA["dtd.page.page_overlap"],
            "dtd.page.page_definition": PROPERTY_METADATA["dtd.page.page_definition"],
            "dtd.page.height_pages": PROPERTY_METADATA["dtd.page.height_pages"],
            "dtd.page.header_position": PROPERTY_METADATA["dtd.page.header_position"],
            "dtd.page.header": PROPERTY_METADATA["dtd.page.header"],
            "dtd.page.width_pages": PROPERTY_METADATA["dtd.page.width_pages"],
            "common.id": PROPERTY_METADATA["common.id"],
            "dtd.page.height": PROPERTY_METADATA["dtd.page.height"],
            "dtd.page.footer_position": PROPERTY_METADATA["dtd.page.footer_position"],
            "dtd.page.footer": PROPERTY_METADATA["dtd.page.footer"],
            "dtd.page.drawing_space": PROPERTY_METADATA["dtd.page.drawing_space"],
            "text_run.color": PROPERTY_METADATA["text_run.color"],
            "dtd.page.bounds_in_parent": PROPERTY_METADATA["dtd.page.bounds_in_parent"],
            "geometry.bounding_box": PROPERTY_METADATA["geometry.bounding_box"],
            "dtd.CDXML.bgcolor": PROPERTY_METADATA["dtd.CDXML.bgcolor"],
            "dtd.CDXML.bgalpha": PROPERTY_METADATA["dtd.CDXML.bgalpha"],
        }
    ),
    provenance=(P_d804e630c1b17793a2de,),
)
