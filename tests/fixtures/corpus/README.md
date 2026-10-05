# RDKit CDXML fixtures

These two documents are unchanged copies of primary fixtures in the RDKit
repository. They are round-trip verified by the library checks in
[`test_corpus.py`](../../roundtrip/test_corpus.py), which compare the complete
retained XML structure and selected typed values across parse, serialization,
and reparse. They have not been independently checked in ChemDraw: the source
files' `CreationProgram="ChemDraw 6.0.1"` attribute is source-authored
metadata. No RDKit package or PyCDXML is needed to use these files.

Retrieved on 2026-10-05 from the URLs below. SHA-256 values are for the exact
retrieved bytes, which are preserved in the adjacent fixture files. The source
links pin upstream commits, and each pinned file was checked to match the
recorded fixture hash.

| File | Source | SHA-256 |
| --- | --- | --- |
| `atom-query.cdxml` | [RDKit `atom-query.cdxml` at `185ec927`](https://raw.githubusercontent.com/rdkit/rdkit/185ec927ab6f1dfe66401644552286dff41fa359/rdkit/Chem/test_data/atom-query.cdxml) | `714a012f09e77f7d9adafe90450829e327ddff35ccecc1464eed813eea021f47` |
| `mol1.cdxml` | [RDKit `mol1.cdxml` at `d1985caa`](https://raw.githubusercontent.com/rdkit/rdkit/d1985caaa79f6f5d803966a5f4bed69e0c6ef2bc/Code/GraphMol/FileParsers/mol1.cdxml) | `064b031c9e25bc05fa3f021a7a2d48a1cf596ae6ff55cfa67a21d237f5604817` |

The applicable RDKit BSD 3-Clause license is included as
[`RDKit-LICENSE.txt`](RDKit-LICENSE.txt). Its source is
[RDKit `license.txt`](https://raw.githubusercontent.com/rdkit/rdkit/master/license.txt);
the retrieved file's SHA-256 is
`daeb8d194502cbcf34c05c39541a0d02be65bc9bada5b891c1974cd24e9fca30`.

## Structural features represented

- `atom-query.cdxml` has six nodes and six bonds, an `ElementList` node with
  `ElementList="6 7"`, and node IDs 3 and 4 that overlap the font IDs 3 and 4.
- `mol1.cdxml` has five nodes and five bonds; node 26 has `Charge="-1"`, and
  the document also contains `NumHydrogens`, `ImplicitHydrogens`, a `graphic`,
  and a `represent` element.
- Both documents carry color and font tables, and both declare
  `CreationProgram="ChemDraw 6.0.1"`.

These details describe the retrieved XML and do not imply that every element
is a typed runtime feature.
