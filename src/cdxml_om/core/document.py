"""Secure parser, retained-tree document API, and lazy typed field access."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from enum import Enum
from os import PathLike
from typing import TypeVar, cast, overload

from lxml import etree

from cdxml_om._generated import enums as generated_enums
from cdxml_om._generated.models import (
    Arrow,
    CDXMLRoot,
    ColorTable,
    FontTable,
    Graphic,
    Group,
    Page,
    ReactionScheme,
    Text,
)
from cdxml_om._generated.schema_metadata import (
    DATATYPE_METADATA,
    ENUM_METADATA,
    OBJECT_METADATA,
    PROPERTY_METADATA,
    ObjectMetadata,
    PropertyMetadata,
)
from cdxml_om._generated.schema_registry import OBJECT_BY_SPEC_ID
from cdxml_om.core.attributes import property_xml_names, read_property_attribute
from cdxml_om.core.codecs import decode_property_value, encode_property_value
from cdxml_om.core.collections import XMLBackedCollection
from cdxml_om.core.errors import CodecError, MutationError, ParseError, ReferenceResolutionError
from cdxml_om.core.fields import ElementCollection
from cdxml_om.core.geometry import BoundingBox, Point2D, Point3D
from cdxml_om.core.ids import IdManager
from cdxml_om.core.models import CDXMLElement
from cdxml_om.core.registry import ObjectRegistry
from cdxml_om.io.cdxml import parse_cdxml_file, parse_cdxml_string, serialize_cdxml, write_cdxml
from cdxml_om.validation import ValidationReport

T = TypeVar("T", bound=CDXMLElement)
_SPEC_ID_BY_XML_TAG = {metadata.xml_tag: spec_id for spec_id, metadata in OBJECT_METADATA.items()}


def _direct_mixed_text(element: etree.Element) -> str:
    """Read only an element's own PCDATA, excluding descendant element text."""
    return (element.text or "") + "".join(child.tail or "" for child in element)


class CDXMLDocument:
    """A secure, navigable view over a complete retained CDXML document tree.

    Typed reads are lazy and never rewrite source attributes. The original tree,
    including unknown XML nodes, comments, processing instructions, and DTD
    declaration, remains the serialization source.
    """

    __slots__ = ("_tree", "_objects", "_id_manager", "_local_id_managers")

    def __init__(self, tree: etree.ElementTree) -> None:
        root = tree.getroot()
        if root.tag != "CDXML":
            raise ParseError(f"expected root tag 'CDXML', found {root.tag!r}")
        self._tree = tree
        self._objects = ObjectRegistry(self, tree)
        self._id_manager = IdManager(self._collect_reserved_ids())
        self._local_id_managers: dict[etree.Element, IdManager] = {}

    @classmethod
    def from_string(cls, source: str | bytes | bytearray) -> CDXMLDocument:
        """Parse a Unicode string or original XML bytes without network access."""
        tree = parse_cdxml_string(source)
        return cls(tree)

    @classmethod
    def from_file(cls, source: str | PathLike[str]) -> CDXMLDocument:
        """Parse a local file using its declared byte encoding; URLs are not fetched."""
        tree = parse_cdxml_file(source)
        return cls(tree)

    @property
    def tree(self) -> etree.ElementTree:
        """The retained full lxml tree (including document-level nodes)."""
        return self._tree

    @property
    def root(self) -> CDXMLRoot:
        wrapper = self.wrap(self._tree.getroot())
        if not isinstance(wrapper, CDXMLRoot):
            raise RuntimeError("generated registry mismatch for CDXML document root")
        return wrapper

    @property
    def pages(self) -> ElementCollection[Page]:
        root = self._tree.getroot()
        return self._children_of_tag(root, "page", Page, "page", "pages")

    @property
    def groups(self) -> ElementCollection[Group]:
        return self._all_elements_of_tag("group", Group)

    @property
    def texts(self) -> ElementCollection[Text]:
        return self._all_elements_of_tag("t", Text)

    @property
    def graphics(self) -> ElementCollection[Graphic]:
        return self._all_elements_of_tag("graphic", Graphic)

    @property
    def arrows(self) -> ElementCollection[Arrow]:
        return self._all_elements_of_tag("arrow", Arrow)

    @property
    def schemes(self) -> ElementCollection[ReactionScheme]:
        return self._all_elements_of_tag("scheme", ReactionScheme)

    @property
    def font_table(self) -> FontTable | None:
        return self._root_table("fonttable", FontTable)

    @property
    def color_table(self) -> ColorTable | None:
        return self._root_table("colortable", ColorTable)

    def create_font_table(self) -> FontTable:
        """Insert the optional root FontTable before pages, if absent."""
        return self._create_root_table("fonttable", FontTable)

    def create_color_table(self) -> ColorTable:
        """Insert the optional root ColorTable before fonts and pages, if absent."""
        return self._create_root_table("colortable", ColorTable)

    @property
    def objects(self) -> ObjectRegistry:
        """Identity-preserving registry for modeled object wrappers and IDs."""
        return self._objects

    def to_string(
        self,
        *,
        encoding: str = "unicode",
        xml_declaration: bool = True,
        pretty_print: bool = False,
    ) -> str:
        """Serialize the full tree; structure is preserved, not source bytes."""
        return serialize_cdxml(
            self._tree,
            encoding=encoding,
            xml_declaration=xml_declaration,
            pretty_print=pretty_print,
        )

    def to_file(
        self,
        destination: str | PathLike[str],
        *,
        encoding: str = "UTF-8",
        xml_declaration: bool = True,
        pretty_print: bool = False,
    ) -> None:
        """Write the complete tree with a declaration matching the output bytes."""
        write_cdxml(
            self._tree,
            destination,
            encoding=encoding,
            xml_declaration=xml_declaration,
            pretty_print=pretty_print,
        )

    def find(self, model_type: type[T]) -> list[T]:
        """Return modeled or unknown elements matching a wrapper type in tree order."""
        matches: list[T] = []
        for element in self._tree.iter():
            if not isinstance(element.tag, str):
                continue
            wrapper = self.wrap(element)
            if isinstance(wrapper, model_type):
                matches.append(wrapper)
        return matches

    @overload
    def get(self, key: int) -> CDXMLElement | None: ...

    @overload
    def get(self, key: type[T], object_id: int) -> T | None: ...

    def get(self, key: object, object_id: object = None) -> CDXMLElement | None:
        if isinstance(key, type):
            if not issubclass(key, CDXMLElement):
                raise TypeError("typed lookup requires a CDXMLElement model type")
            if not isinstance(object_id, int) or isinstance(object_id, bool):
                raise TypeError("typed lookup requires an object ID")
            return self._objects.by_id(object_id, key)
        if object_id is not None or isinstance(key, bool) or not isinstance(key, int):
            raise TypeError("get expects an integer ID or a model type and integer ID")
        return self._objects.by_id(key)

    def wrap(self, element: etree.Element) -> CDXMLElement:
        return self._objects.wrap(element)

    def validate(self) -> ValidationReport:
        """Return schema-backed findings without changing or rejecting the tree."""
        from cdxml_om.validation.document import validate_document

        return validate_document(self)

    def _children_of_tag(
        self,
        element: etree.Element,
        tag: str,
        model_type: type[T],
        object_type: str,
        collection_name: str,
    ) -> XMLBackedCollection[T]:
        def load() -> tuple[T, ...]:
            items: list[T] = []
            for child in element:
                if not isinstance(child.tag, str) or child.tag != tag:
                    continue
                wrapper = self.wrap(child)
                if not isinstance(wrapper, model_type):
                    raise RuntimeError(f"registry mismatch for child tag {tag!r}")
                items.append(wrapper)
            return tuple(items)

        return XMLBackedCollection(
            load,
            lambda values: cast(
                T, self.create_child(element, object_type, collection_name, values)
            ),
            lambda value: self.remove_child(element, object_type, value),
        )

    def _all_elements_of_tag(self, tag: str, model_type: type[T]) -> XMLBackedCollection[T]:
        def load() -> tuple[T, ...]:
            result: list[T] = []
            for element in self._tree.iter():
                if not isinstance(element.tag, str) or element.tag != tag:
                    continue
                wrapper = self.wrap(element)
                if isinstance(wrapper, model_type):
                    result.append(wrapper)
            return tuple(result)

        def no_parent_create(values: Mapping[str, object]) -> T:
            del values
            raise MutationError("document-wide collections are navigational; create via parent")

        def no_parent_remove(value: T) -> None:
            del value
            raise MutationError("remove an object through its parent collection")

        return XMLBackedCollection(load, no_parent_create, no_parent_remove)

    def _root_table(self, tag: str, model_type: type[T]) -> T | None:
        elements = [
            child
            for child in self._tree.getroot()
            if isinstance(child.tag, str) and child.tag == tag
        ]
        if len(elements) > 1:
            raise ReferenceResolutionError(f"multiple root {tag!r} tables are ambiguous")
        if not elements:
            return None
        wrapper = self.wrap(elements[0])
        if not isinstance(wrapper, model_type):
            raise RuntimeError(f"generated registry mismatch for root table {tag!r}")
        return wrapper

    def _create_root_table(self, tag: str, model_type: type[T]) -> T:
        if self._root_table(tag, model_type) is not None:
            raise MutationError(f"root {tag!r} table already exists")
        root = self._tree.getroot()
        root_spec_id = _SPEC_ID_BY_XML_TAG.get("CDXML")
        child_spec_id = _SPEC_ID_BY_XML_TAG.get(tag)
        if root_spec_id is not None and child_spec_id is not None:
            root_metadata = OBJECT_METADATA[root_spec_id]
            child_spec = next(
                (child for child in root_metadata.children if child.object_type == child_spec_id),
                None,
            )
            if child_spec is not None:
                wrapper = self.create_child(root, child_spec_id, child_spec.collection_name, {})
                if not isinstance(wrapper, model_type):
                    raise RuntimeError(f"generated registry mismatch for root table {tag!r}")
                return wrapper

        # Compatibility for generated schemas predating a modeled CDXML root.
        element = etree.Element(tag)
        preceding_tags = {"page"} if tag == "fonttable" else {"fonttable", "page"}
        insertion = next(
            (
                index
                for index, child in enumerate(root)
                if isinstance(child.tag, str) and child.tag in preceding_tags
            ),
            len(root),
        )
        root.insert(insertion, element)
        wrapper = self.wrap(element)
        if not isinstance(wrapper, model_type):
            raise RuntimeError(f"generated registry mismatch for root table {tag!r}")
        return wrapper

    def _local_id_manager(self, scope_element: etree.Element) -> IdManager:
        manager = self._local_id_managers.get(scope_element)
        reserved: set[int] = set()
        for child in scope_element:
            if not isinstance(child.tag, str):
                continue
            spec_id = _SPEC_ID_BY_XML_TAG.get(child.tag)
            if spec_id is None or OBJECT_METADATA[spec_id].id_scope != "local":
                continue
            id_property = next(
                (
                    property_id
                    for property_id, prop in OBJECT_METADATA[spec_id].properties.items()
                    if prop.name == "id"
                ),
                None,
            )
            if id_property is None:
                continue
            raw_id = child.get(PROPERTY_METADATA[id_property].xml_name)
            if raw_id is None:
                continue
            try:
                candidate = decode_property_value(id_property, raw_id)
            except CodecError:
                continue
            if isinstance(candidate, int) and not isinstance(candidate, bool):
                reserved.add(candidate)
        if manager is None:
            manager = IdManager(reserved, datatype_id="local_id")
            self._local_id_managers[scope_element] = manager
        else:
            for local_id in reserved:
                manager.reserve(local_id)
        return manager

    def _collect_reserved_ids(self) -> set[int]:
        datatype = DATATYPE_METADATA["object_id"]
        maximum = datatype.maximum
        if not isinstance(maximum, int):
            raise RuntimeError("object_id datatype must have an integer maximum")
        reserved: set[int] = set()

        def add_tokens(raw_value: str) -> None:
            for token in raw_value.split():
                try:
                    candidate = int(token)
                except ValueError:
                    continue
                if 0 <= candidate <= maximum:
                    reserved.add(candidate)

        for element in self._tree.iter():
            raw_id = element.get("id")
            if not isinstance(element.tag, str):
                if raw_id is not None:
                    add_tokens(raw_id)
                continue
            spec_id = _SPEC_ID_BY_XML_TAG.get(element.tag)
            if spec_id is None:
                if raw_id is not None:
                    add_tokens(raw_id)
                continue
            metadata = OBJECT_METADATA[spec_id]
            if metadata.id_scope == "document" and raw_id is not None:
                add_tokens(raw_id)
            for prop in metadata.properties.values():
                if prop.reference_target is not None:
                    for xml_name in property_xml_names(prop):
                        raw_reference = element.get(xml_name)
                        if raw_reference is not None:
                            add_tokens(raw_reference)
        return reserved

    def _refresh_reserved_ids(self) -> None:
        for object_id in self._collect_reserved_ids():
            self._id_manager.reserve(object_id)

    def _metadata_for_element(self, element: etree.Element) -> ObjectMetadata:
        if not isinstance(element.tag, str) or element.tag not in _SPEC_ID_BY_XML_TAG:
            raise MutationError(f"XML tag {element.tag!r} has no generated object metadata")
        return OBJECT_METADATA[_SPEC_ID_BY_XML_TAG[element.tag]]

    def _property_for_element(self, element: etree.Element, property_id: str) -> PropertyMetadata:
        metadata = self._metadata_for_element(element)
        resolved_id = property_id
        prop = metadata.properties.get(resolved_id)
        if prop is None:
            matches = [
                (candidate_id, candidate)
                for candidate_id, candidate in metadata.properties.items()
                if candidate.name == property_id
            ]
            if len(matches) == 1:
                resolved_id, prop = matches[0]
        if prop is None:
            raise MutationError(
                f"property {property_id!r} does not belong to XML tag {element.tag!r}",
                property_id=property_id,
            )
        return prop

    def _ensure_attached(self, element: etree.Element, label: str) -> None:
        ancestor = element
        while ancestor.getparent() is not None:
            parent = ancestor.getparent()
            if parent is None:
                break
            ancestor = parent
        if ancestor is not self._tree.getroot():
            raise MutationError(f"{label} is detached from this document")

    @staticmethod
    def _coerce_mutation_value(value: object, prop: PropertyMetadata) -> object:
        if prop.codec in {"point_2d", "point_3d", "bounding_box"} and isinstance(
            value, (tuple, list)
        ):
            coordinates = cast(Sequence[object], value)
            expected_count = {"point_2d": 2, "point_3d": 3, "bounding_box": 4}[prop.codec]
            if len(coordinates) == expected_count:
                numbers: list[float] = []
                for item in coordinates:
                    if isinstance(item, bool) or not isinstance(item, (int, float)):
                        return cast(object, value)
                    numbers.append(float(item))
                if prop.codec == "point_2d":
                    return Point2D(numbers[0], numbers[1])
                if prop.codec == "point_3d":
                    return Point3D(numbers[0], numbers[1], numbers[2])
                return BoundingBox(numbers[0], numbers[1], numbers[2], numbers[3])
            return cast(object, value)
        if isinstance(value, (tuple, list)):
            value = cast(object, value)
        if prop.enum is None or isinstance(value, Enum):
            return value
        enum_metadata = ENUM_METADATA[prop.enum]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return value
        selected = None
        for member in enum_metadata.values:
            if enum_metadata.representation == "intflag":
                try:
                    matches = float(member.xml_value) == float(value)
                except (OverflowError, ValueError):
                    matches = False
            else:
                matches = member.cdx_value == value
            if matches:
                selected = member
                break
        if selected is None:
            return value
        enum_type = cast(type[Enum], getattr(generated_enums, enum_metadata.python_name))
        if enum_metadata.representation == "str":
            enum_value: str | int = selected.xml_value
        elif selected.cdx_value is not None:
            enum_value = selected.cdx_value
        else:
            return value
        return enum_type(enum_value)

    def _reference_id_for_wrapper(
        self,
        value: object,
        property_id: str,
        target_type: str,
    ) -> int:
        if not isinstance(value, CDXMLElement):
            raise MutationError(
                f"{property_id} requires an attached CDXMLElement reference",
                property_id=property_id,
            )
        if target_type != "*":
            expected_type = OBJECT_BY_SPEC_ID[target_type]
            if type(value) is not expected_type:
                raise MutationError(
                    f"{property_id} requires an exact {expected_type.__name__} wrapper",
                    property_id=property_id,
                )
        if value.document is not self:
            raise MutationError(
                f"{property_id} target belongs to a different document",
                property_id=property_id,
            )
        self._ensure_attached(value.raw_element, f"{property_id} target")
        target_spec_id = _SPEC_ID_BY_XML_TAG.get(value.xml_tag)
        if target_spec_id is None or OBJECT_METADATA[target_spec_id].id_scope != "document":
            raise MutationError(
                f"{property_id} target has no document-scoped ID", property_id=property_id
            )
        target_metadata = OBJECT_METADATA[target_spec_id]
        id_property = next(
            (
                property_id
                for property_id, target_prop in target_metadata.properties.items()
                if target_prop.name == "id" and target_prop.datatype == "object_id"
            ),
            None,
        )
        if id_property is None:
            raise MutationError(f"{property_id} target type has no ID property")
        target_prop = target_metadata.properties[id_property]
        raw_target_id = value.raw_element.get(target_prop.xml_name)
        if raw_target_id is None:
            raise MutationError(f"{property_id} target has no object ID")
        try:
            target_id = decode_property_value(id_property, raw_target_id)
        except CodecError as exc:
            raise MutationError(
                f"{property_id} target has an invalid object ID", property_id=property_id
            ) from exc
        if not isinstance(target_id, int) or isinstance(target_id, bool):
            raise MutationError(
                f"{property_id} target has an invalid object ID", property_id=property_id
            )
        matches = self._objects.elements_by_id(target_id)
        if len(matches) != 1 or matches[0] is not value.raw_element:
            raise MutationError(
                f"{property_id} target ID {target_id} is not unique in this document",
                property_id=property_id,
            )
        return target_id

    def _prepare_field_value(
        self,
        element: etree.Element | None,
        property_id: str,
        value: object,
        *,
        context_attributes: Mapping[str, str] | None = None,
    ) -> str | None:
        prop = PROPERTY_METADATA[property_id]
        if value is None:
            if prop.required:
                raise MutationError(
                    f"required property {property_id!r} cannot be cleared",
                    property_id=property_id,
                )
            return None

        if prop.reference_target is not None:
            if prop.reference_many:
                if not isinstance(value, (tuple, list)):
                    raise MutationError(
                        f"{property_id} requires a sequence of object references",
                        property_id=property_id,
                    )
                values = cast(Sequence[object], value)
                value = tuple(
                    self._reference_id_for_wrapper(item, property_id, prop.reference_target)
                    for item in values
                )
            else:
                value = self._reference_id_for_wrapper(value, property_id, prop.reference_target)
        else:
            try:
                value = self._coerce_mutation_value(value, prop)
            except (OverflowError, ValueError) as exc:
                raise MutationError(
                    "numeric value is outside the finite range", property_id=property_id
                ) from exc

        try:
            raw_value = encode_property_value(
                property_id, value, context_attributes=context_attributes
            )
        except (OverflowError, ValueError) as exc:
            raise MutationError(
                "numeric value is outside the finite range", property_id=property_id
            ) from exc
        except CodecError as exc:
            raise MutationError(str(exc), property_id=property_id) from exc

        if prop.name == "id" and element is not None:
            try:
                object_id = int(raw_value)
            except ValueError as exc:
                raise MutationError("object IDs must be integers", property_id=property_id) from exc
            spec_id = _SPEC_ID_BY_XML_TAG.get(element.tag) if isinstance(element.tag, str) else None
            if spec_id is None:
                raise MutationError(
                    "ID property has no generated object metadata", property_id=property_id
                )
            metadata = OBJECT_METADATA[spec_id]
            if metadata.id_scope == "none":
                raise MutationError("object has no ID scope", property_id=property_id)
            manager = self._id_manager
            if metadata.id_scope == "document":
                self._refresh_reserved_ids()
            elif metadata.id_scope == "local":
                parent = element.getparent()
                if parent is None:
                    raise MutationError(
                        "local ID object has no containing table", property_id=property_id
                    )
                manager = self._local_id_manager(parent)
            old_raw = element.get(prop.xml_name)
            old_id: int | None = None
            if old_raw is not None:
                try:
                    old_id = int(old_raw)
                except ValueError:
                    old_id = None
            if object_id != old_id and manager.is_reserved(object_id):
                raise MutationError(
                    f"object ID {object_id} is already reserved in its scope",
                    property_id=property_id,
                )
        return raw_value

    def create_child(
        self,
        parent: etree.Element,
        object_type: str,
        collection_name: str,
        values: Mapping[str, object],
    ) -> CDXMLElement:
        """Create one generated child after all attributes and references validate."""
        self._ensure_attached(parent, "parent")
        metadata = OBJECT_METADATA.get(object_type)
        if metadata is None:
            raise MutationError(f"object type {object_type!r} is not generated")
        parent_spec_id = (
            _SPEC_ID_BY_XML_TAG.get(parent.tag) if isinstance(parent.tag, str) else None
        )
        parent_metadata = OBJECT_METADATA[parent_spec_id] if parent_spec_id is not None else None
        child_spec = None
        if parent_metadata is not None and parent_spec_id is not None:
            child_spec = next(
                (
                    child
                    for child in parent_metadata.children
                    if child.object_type == object_type and child.collection_name == collection_name
                ),
                None,
            )
            if child_spec is None or parent_spec_id not in metadata.allowed_parents:
                raise MutationError(
                    f"{metadata.python_name} is not available in "
                    f"{parent_metadata.python_name}.{collection_name}"
                )
        elif parent.tag == "CDXML" and "$document" in metadata.allowed_parents:
            # Older schema snapshots did not model the XML document root itself.
            if collection_name != "pages" or object_type != "page":
                raise MutationError(f"{metadata.python_name} is not a child of the CDXML document")
        else:
            raise MutationError("parent has no generated child collection metadata")

        if child_spec is not None:
            parent_name = parent_metadata.python_name if parent_metadata is not None else "CDXML"
            current_count = sum(
                1
                for child in parent
                if isinstance(child.tag, str) and child.tag == metadata.xml_tag
            )
            if child_spec.max_occurs is not None and current_count >= child_spec.max_occurs:
                raise MutationError(
                    f"{parent_name}.{collection_name} reached its maximum cardinality"
                )

        values_by_name: dict[str, tuple[str, object]] = {}
        for property_id, prop in metadata.properties.items():
            values_by_name[prop.name] = (property_id, values.get(prop.name))
            values_by_name[property_id] = (property_id, values.get(property_id))

        supplied: set[str] = set()
        explicit_id: object | None = None
        attribute_values: dict[str, str] = {}
        text_values: dict[str, str] = {}
        contextual_values: dict[str, object] = {}
        for name, value in values.items():
            item = values_by_name.get(name)
            if item is None:
                raise MutationError(f"unknown {metadata.python_name} creation field {name!r}")
            property_id, _ = item
            if property_id in supplied:
                raise MutationError(f"property {property_id!r} was supplied more than once")
            supplied.add(property_id)
            prop = metadata.properties[property_id]
            if prop.name == "id":
                explicit_id = value
                continue
            if prop.codec == "object_tag_value":
                contextual_values[property_id] = value
                continue
            raw_value = self._prepare_field_value(None, property_id, value)
            if raw_value is not None:
                if prop.storage == "text":
                    text_values[property_id] = raw_value
                else:
                    attribute_values[prop.xml_name] = raw_value

        # Context-dependent XML values are encoded only after sibling lexical
        # attributes (notably ObjectTag.TagType) have been staged.
        for property_id, value in contextual_values.items():
            prop = metadata.properties[property_id]
            raw_value = self._prepare_field_value(
                None, property_id, value, context_attributes=attribute_values
            )
            if raw_value is not None:
                if prop.storage == "text":
                    text_values[property_id] = raw_value
                else:
                    attribute_values[prop.xml_name] = raw_value

        for property_id, prop in metadata.properties.items():
            allocator_supplies_id = prop.name == "id" and metadata.id_scope in {
                "document",
                "local",
            }
            if (
                prop.required
                and prop.default is None
                and property_id not in supplied
                and not allocator_supplies_id
            ):
                raise MutationError(
                    f"required creation field {prop.name!r} is missing",
                    property_id=property_id,
                )

        id_property = next(
            (property_id for property_id, prop in metadata.properties.items() if prop.name == "id"),
            None,
        )
        if metadata.id_scope != "none" and id_property is None:
            raise MutationError(f"{metadata.python_name} has no generated ID property")
        manager: IdManager | None = None
        id_value: int | None = None
        if metadata.id_scope == "document":
            self._refresh_reserved_ids()
            manager = self._id_manager
        elif metadata.id_scope == "local":
            manager = self._local_id_manager(parent)
        if id_property is not None:
            if manager is None:
                raise MutationError(f"{metadata.python_name} has no supported ID manager")
            if explicit_id is None:
                id_value = manager.next_available()
            else:
                try:
                    raw_id = encode_property_value(id_property, explicit_id)
                except CodecError as exc:
                    raise MutationError(str(exc), property_id=id_property) from exc
                id_value = int(raw_id)
                if manager.is_reserved(id_value):
                    raise MutationError(
                        f"object ID {id_value} is already reserved in its scope",
                        property_id=id_property,
                    )

        attributes = dict(attribute_values)
        if id_property is not None and id_value is not None:
            id_prop = metadata.properties[id_property]
            attributes[id_prop.xml_name] = str(id_value)
        child = etree.Element(metadata.xml_tag)
        for name, value in attributes.items():
            child.set(name, value)
        for value in text_values.values():
            child.text = value
        if parent.tag == "CDXML" and parent_metadata is not None and child_spec is not None:
            order_by_tag = {
                OBJECT_METADATA[item.object_type].xml_tag: index
                for index, item in enumerate(parent_metadata.children)
            }
            target_order = order_by_tag.get(metadata.xml_tag)
            if target_order is None:
                parent.append(child)
            else:
                insertion_index = next(
                    (
                        index
                        for index, existing in enumerate(parent)
                        if isinstance(existing.tag, str)
                        and (existing_order := order_by_tag.get(existing.tag)) is not None
                        and existing_order > target_order
                    ),
                    len(parent),
                )
                parent.insert(insertion_index, child)
        else:
            parent.append(child)
        if manager is not None and id_value is not None:
            manager.reserve(id_value)
        return self.wrap(child)

    def remove_child(self, parent: etree.Element, object_type: str, value: CDXMLElement) -> None:
        """Detach one direct collection member without cascading references."""
        self._ensure_attached(parent, "parent")
        if value.document is not self:
            raise MutationError("cannot remove an element from a different document")
        expected_type = OBJECT_BY_SPEC_ID[object_type]
        if type(value) is not expected_type:
            raise MutationError(f"collection removal requires a {expected_type.__name__} wrapper")
        child = value.raw_element
        if child.getparent() is not parent:
            raise MutationError("element is detached or is not a direct member of this collection")
        self._refresh_reserved_ids()
        metadata = OBJECT_METADATA[object_type]
        if metadata.id_scope == "local":
            self._local_id_manager(parent)
        tail = child.tail
        if tail is not None:
            index = parent.index(child)
            if index == 0:
                parent.text = (parent.text or "") + tail
            else:
                previous = parent[index - 1]
                previous.tail = (previous.tail or "") + tail
            child.tail = None
        parent.remove(child)

    def raw_reference_id(
        self, element: etree.Element, property_id: str
    ) -> int | tuple[int, ...] | None:
        prop = self._property_for_element(element, property_id)
        metadata = self._metadata_for_element(element)
        canonical_property_id = (
            property_id
            if property_id in metadata.properties
            else next(
                candidate_id
                for candidate_id, candidate in metadata.properties.items()
                if candidate.name == property_id
            )
        )
        if prop.reference_target is None:
            raise MutationError(
                f"{property_id!r} is not a reference property", property_id=property_id
            )
        raw_value, _ = read_property_attribute(element, prop, canonical_property_id)
        if raw_value is None:
            return None
        decoded = self.decode_value(canonical_property_id, raw_value, element)
        if prop.reference_many:
            if not isinstance(decoded, tuple):
                raise CodecError(
                    "reference list did not decode to object IDs", property_id=property_id
                )
            values = cast(tuple[object, ...], decoded)
            ids: list[int] = []
            for item in values:
                if isinstance(item, bool) or not isinstance(item, int):
                    raise CodecError(
                        "reference list contains a non-integer ID", property_id=property_id
                    )
                ids.append(item)
            return tuple(ids)
        if not isinstance(decoded, int) or isinstance(decoded, bool):
            raise CodecError("reference did not decode to an object ID", property_id=property_id)
        return decoded

    def read_field(self, element: etree.Element, property_id: str) -> object:
        prop = PROPERTY_METADATA[property_id]
        raw_value: str | None
        if prop.storage == "text":
            raw_value = (
                _direct_mixed_text(element)
                if element.tag == "spectrum"
                else "".join(element.itertext())
            )
        else:
            raw_value, _ = read_property_attribute(element, prop, property_id)
        if raw_value is None:
            if prop.reference_many:
                return ()
            if prop.default is not None:
                raw_value = str(prop.default)
            elif not prop.required:
                return None
            elif prop.reference_target is not None:
                raise ReferenceResolutionError(
                    f"required reference {property_id!r} has no XML attribute "
                    f"{property_xml_names(prop)!r}"
                )
            else:
                raise CodecError(
                    f"required XML attribute {property_xml_names(prop)!r} is missing",
                    property_id=property_id,
                    xml_tag=element.tag if isinstance(element.tag, str) else None,
                )

        value = self.decode_value(property_id, raw_value, element)
        if prop.reference_target is None:
            return value
        target_type = (
            None if prop.reference_target == "*" else OBJECT_BY_SPEC_ID[prop.reference_target]
        )
        if prop.reference_many:
            if not isinstance(value, tuple):
                raise CodecError(
                    f"reference list {property_id!r} did not decode to an ID tuple",
                    property_id=property_id,
                )
            resolved: list[CDXMLElement] = []
            target_ids = cast(tuple[object, ...], value)
            for target_id in target_ids:
                if not isinstance(target_id, int) or isinstance(target_id, bool):
                    raise CodecError(f"invalid object ID in reference {property_id!r}")
                resolved.append(self._resolve_reference(target_id, target_type, property_id))
            return tuple(resolved)
        if not isinstance(value, int) or isinstance(value, bool):
            raise CodecError(f"invalid object ID for reference {property_id!r}")
        return self._resolve_reference(value, target_type, property_id)

    def _resolve_reference(
        self,
        object_id: int,
        target_type: type[CDXMLElement] | None,
        property_id: str,
    ) -> CDXMLElement:
        try:
            result = self._objects.by_id(object_id, target_type)
        except ReferenceResolutionError as exc:
            raise ReferenceResolutionError(f"{property_id}: {exc}") from exc
        if result is None:
            target_name = target_type.__name__ if target_type is not None else "document object"
            raise ReferenceResolutionError(
                f"{property_id}: no {target_name} with object ID {object_id}"
            )
        return result

    def decode_value(self, property_id: str, raw_value: str, element: etree.Element) -> object:
        try:
            return decode_property_value(
                property_id, raw_value, context_attributes=dict(element.attrib)
            )
        except CodecError as exc:
            if exc.xml_tag is None and isinstance(element.tag, str):
                exc.xml_tag = element.tag
            raise

    def write_field(self, element: etree.Element, property_id: str, value: object) -> None:
        self._ensure_attached(element, "edited element")
        prop = self._property_for_element(element, property_id)
        target_xml_name = prop.xml_name
        if prop.storage != "text":
            try:
                _, existing_xml_name = read_property_attribute(element, prop, property_id)
            except CodecError as exc:
                raise MutationError(str(exc), property_id=property_id) from exc
            if existing_xml_name is not None:
                target_xml_name = existing_xml_name
        is_spectrum_text = prop.storage == "text" and element.tag == "spectrum"
        if prop.storage == "text" and len(element) and not is_spectrum_text:
            raise MutationError(
                f"cannot replace {property_id!r} because the element contains opaque children",
                property_id=property_id,
            )
        raw_value = self._prepare_field_value(
            element, property_id, value, context_attributes=dict(element.attrib)
        )
        if prop.xml_name == "TagType":
            candidate_attributes = dict(element.attrib)
            if raw_value is None:
                candidate_attributes.pop(prop.xml_name, None)
            else:
                candidate_attributes[prop.xml_name] = raw_value
            metadata = self._metadata_for_element(element)
            for value_property_id, value_prop in metadata.properties.items():
                if value_prop.codec != "object_tag_value":
                    continue
                existing_value = element.get(value_prop.xml_name)
                if existing_value is None and value_prop.default is not None:
                    existing_value = str(value_prop.default)
                if existing_value is None:
                    continue
                try:
                    decode_property_value(
                        value_property_id,
                        existing_value,
                        context_attributes=candidate_attributes,
                    )
                except CodecError as exc:
                    raise MutationError(str(exc), property_id=value_property_id) from exc
        if prop.storage == "text":
            element.text = raw_value
            if is_spectrum_text:
                # Replacing the parent PCDATA must not delete or reinterpret its
                # child elements. Store the replacement before children and clear
                # their old tails, which were part of the replaced PCDATA value.
                for child in element:
                    child.tail = None
            return
        if raw_value is None:
            element.attrib.pop(target_xml_name, None)
            return
        element.set(target_xml_name, raw_value)
        if prop.name == "id":
            spec_id = _SPEC_ID_BY_XML_TAG.get(element.tag) if isinstance(element.tag, str) else None
            if spec_id is not None:
                metadata = OBJECT_METADATA[spec_id]
                if metadata.id_scope == "document":
                    self._id_manager.reserve(int(raw_value))
                elif metadata.id_scope == "local":
                    parent = element.getparent()
                    if parent is not None:
                        self._local_id_manager(parent).reserve(int(raw_value))

    def read_collection(
        self,
        element: etree.Element,
        object_type: str,
    ) -> ElementCollection[CDXMLElement]:
        child_type = OBJECT_METADATA[object_type]
        model_type = OBJECT_BY_SPEC_ID[object_type]
        parent_metadata = self._metadata_for_element(element)
        child_spec = next(
            (child for child in parent_metadata.children if child.object_type == object_type),
            None,
        )
        if child_spec is None:
            raise MutationError(
                f"{parent_metadata.python_name} has no generated {object_type!r} collection"
            )
        return self._children_of_tag(
            element,
            child_type.xml_tag,
            model_type,
            object_type,
            child_spec.collection_name,
        )


__all__ = ["CDXMLDocument"]
