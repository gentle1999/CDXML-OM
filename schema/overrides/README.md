# Schema overrides

`full_schema.yaml` contains the source-reviewed mappings and compatibility
policies used by the static schema compiler. It includes 53 XML-tag-to-model
mappings, public field aliases, explicit reference targets, shared datatype
families, source-backed measurement and contextual-value rules, and XML/CDX
property aliases.

Its top-level groups include `object_models`, `field_aliases`,
`global_field_aliases`, `reference_targets`, `collections`, `enum_type_names`,
`property_type_families`, `measurement_fields`,
`measurement_property_families`, `lexical_string_fields`,
`contextual_value_fields`, `property_defaults`, `sdk_xml_attribute_aliases`,
`sdk_property_conflicts`, `cdx_property_aliases`, and `source_anomalies`.

It also records the XML identity policies for document extensions and local
resource IDs, the DTD `altgroup` to undeclared `bracket` anomaly, and the
historical Curve property-ID conflict between `CurveSpacing` and `Closed`.
These entries preserve explicit uncertainty; they do not resolve unsupported
source claims or assert ChemDraw application compatibility.

When changing an entry, retain its source locators and rationale, then run the
schema compiler checks and source-bound feature tests. See the
[schema guide](../../docs/schema.md) and
[source evidence notes](../sources/README.md) for how overrides relate to
canonical inputs.
