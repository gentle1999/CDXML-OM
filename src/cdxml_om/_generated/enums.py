# AUTO-GENERATED. DO NOT EDIT DIRECTLY.
"""Statically generated enums from canonical schema."""

from enum import IntEnum, IntFlag, StrEnum


class BondOrder(IntFlag):
    SINGLE = 1
    DOUBLE = 2
    TRIPLE = 4
    QUADRUPLE = 8
    QUINTUPLE = 16
    SEXTUPLE = 32
    HALF = 64
    AROMATIC = 128
    TWO_AND_HALF = 256
    THREE_AND_HALF = 512
    FOUR_AND_HALF = 1024
    FIVE_AND_HALF = 2048
    DATIVE = 4096
    IONIC = 8192
    HYDROGEN = 16384
    THREE_CENTER = 32768


class BondDisplay(IntEnum):
    SOLID = 0
    DASH = 1
    HASH = 2
    WEDGED_HASH_BEGIN = 3
    WEDGED_HASH_END = 4
    BOLD = 5
    WEDGE_BEGIN = 6
    WEDGE_END = 7
    WAVY = 8
    HOLLOW_WEDGE_BEGIN = 9
    HOLLOW_WEDGE_END = 10
    WAVY_WEDGE_BEGIN = 11
    WAVY_WEDGE_END = 12
    DOT = 13
    DASH_DOT = 14


class GraphicType(StrEnum):
    UNDEFINED = "Undefined"
    LINE = "Line"
    ARC = "Arc"
    RECTANGLE = "Rectangle"
    OVAL = "Oval"
    ORBITAL = "Orbital"
    BRACKET = "Bracket"
    SYMBOL = "Symbol"


class LabelJustification(StrEnum):
    AUTO = "Auto"
    LEFT = "Left"
    CENTER = "Center"
    RIGHT = "Right"
    ABOVE = "Above"
    BELOW = "Below"
    BEST = "Best"


class CaptionJustification(StrEnum):
    AUTO = "Auto"
    LEFT = "Left"
    CENTER = "Center"
    RIGHT = "Right"
    FULL = "Full"


class AminoAcidTermini(StrEnum):
    HOH = "HOH"
    NH2_COOH = "NH2COOH"


class PageDefinition(StrEnum):
    UNDEFINED = "Undefined"
    CENTER = "Center"
    TL4 = "TL4"
    ID_TERM = "IDTerm"
    FLUSH_LEFT = "FlushLeft"
    FLUSH_RIGHT = "FlushRight"
    REACTION1 = "Reaction1"
    REACTION2 = "Reaction2"
    MULTICOLUMN_TL4 = "MulticolumnTL4"
    MULTICOLUMN_NON_TL4 = "MulticolumnNonTL4"
    USER_DEFINED = "UserDefined"


class DrawingSpace(StrEnum):
    POSTER = "poster"
    PAGES = "pages"


class SequenceType(StrEnum):
    UNKNOWN = "Unknown"
    PEPTIDE = "Peptide"
    PEPTIDE1 = "Peptide1"
    PEPTIDE3 = "Peptide3"
    DNA = "DNA"
    RNA = "RNA"


class LabelAlignment(StrEnum):
    AUTO = "Auto"
    LEFT = "Left"
    CENTER = "Center"
    RIGHT = "Right"
    ABOVE = "Above"
    BELOW = "Below"
    BEST = "Best"


class Justification(StrEnum):
    AUTO = "Auto"
    LEFT = "Left"
    CENTER = "Center"
    RIGHT = "Right"
    FULL = "Full"
    ABOVE = "Above"
    BELOW = "Below"
    BEST = "Best"


class UnsaturatedBonds(StrEnum):
    UNSPECIFIED = "Unspecified"
    MUST_BE_ABSENT = "MustBeAbsent"
    MUST_BE_PRESENT = "MustBePresent"


class Translation(StrEnum):
    EQUAL = "Equal"
    BROAD = "Broad"
    NARROW = "Narrow"
    ANY = "Any"


class RxnStereo(StrEnum):
    UNSPECIFIED = "Unspecified"
    INVERSION = "Inversion"
    RETENTION = "Retention"


class RingBondCount(StrEnum):
    SPIRO_OR_HIGHER = "SpiroOrHigher"
    FUSION = "Fusion"
    SIMPLE_RING = "SimpleRing"
    AS_DRAWN = "AsDrawn"
    NO_RING_BONDS = "NoRingBonds"
    UNSPECIFIED = "Unspecified"


class Radical(StrEnum):
    VALUE_NONE = "None"
    SINGLET = "Singlet"
    DOUBLET = "Doublet"
    TRIPLET = "Triplet"


class NodeType(StrEnum):
    UNSPECIFIED = "Unspecified"
    ELEMENT = "Element"
    ELEMENT_LIST = "ElementList"
    ELEMENT_LIST_NICKNAME = "ElementListNickname"
    NICKNAME = "Nickname"
    FRAGMENT = "Fragment"
    FORMULA = "Formula"
    GENERIC_NICKNAME = "GenericNickname"
    ANONYMOUS_ALTERNATIVE_GROUP = "AnonymousAlternativeGroup"
    NAMED_ALTERNATIVE_GROUP = "NamedAlternativeGroup"
    MULTI_ATTACHMENT = "MultiAttachment"
    VARIABLE_ATTACHMENT = "VariableAttachment"
    EXTERNAL_CONNECTION_POINT = "ExternalConnectionPoint"


class LabelDisplay(StrEnum):
    AUTO = "Auto"
    LEFT = "Left"
    CENTER = "Center"
    RIGHT = "Right"
    ABOVE = "Above"
    BELOW = "Below"
    BEST = "Best"


class IsotopicAbundance(StrEnum):
    UNSPECIFIED = "Unspecified"
    ANY = "Any"
    NATURAL = "Natural"
    ENRICHED = "Enriched"
    DEFICIENT = "Deficient"
    NONNATURAL = "Nonnatural"


class NodeGeometry(StrEnum):
    UNKNOWN = "Unknown"
    VALUE_1 = "1"
    LINEAR = "Linear"
    BENT = "Bent"
    TRIGONAL_PLANAR = "TrigonalPlanar"
    TRIGONAL_PYRAMIDAL = "TrigonalPyramidal"
    SQUARE_PLANAR = "SquarePlanar"
    TETRAHEDRAL = "Tetrahedral"
    TRIGONAL_BIPYRAMIDAL = "TrigonalBipyramidal"
    SQUARE_PYRAMIDAL = "SquarePyramidal"
    VALUE_5 = "5"
    OCTAHEDRAL = "Octahedral"
    VALUE_6 = "6"
    VALUE_7 = "7"
    VALUE_8 = "8"
    VALUE_9 = "9"
    VALUE_10 = "10"


class ExternalConnectionType(StrEnum):
    UNSPECIFIED = "Unspecified"
    DIAMOND = "Diamond"
    STAR = "Star"
    POLYMER_BEAD = "PolymerBead"
    WAVY = "Wavy"
    RESIDUE = "Residue"
    PEPTIDE = "Peptide"
    DNA = "DNA"
    RNA = "RNA"
    TERMINUS = "Terminus"
    SULFIDE = "Sulfide"
    NUCLEOTIDE = "Nucleotide"
    UNLINKED_BRANCH = "UnlinkedBranch"


class NodeStereochemistry(StrEnum):
    U = "U"
    N = "N"
    R = "R"
    S = "S"
    R_2 = "r"
    S_2 = "s"
    U_2 = "u"
    M = "M"
    P = "P"
    A = "a"
    FIELD = "+"
    FIELD_2 = "-"
    FIELD_3 = "?"


class Topology(StrEnum):
    UNSPECIFIED = "Unspecified"
    RING = "Ring"
    CHAIN = "Chain"
    RING_OR_CHAIN = "RingOrChain"


class RxnParticipation(StrEnum):
    UNSPECIFIED = "Unspecified"
    REACTION_CENTER = "ReactionCenter"
    MAKE_OR_BREAK = "MakeOrBreak"
    CHANGE_TYPE = "ChangeType"
    MAKE_AND_CHANGE = "MakeAndChange"
    NOT_REACTION_CENTER = "NotReactionCenter"
    NO_CHANGE = "NoChange"
    UNMAPPED = "Unmapped"


class DoublePosition(StrEnum):
    CENTER = "Center"
    RIGHT = "Right"
    LEFT = "Left"


class Connectivity(StrEnum):
    LINEAR = "Linear"
    BRIDGED = "Bridged"
    STAGGERED = "Staggered"
    CYCLIC = "Cyclic"
    UNSPECIFIED = "Unspecified"


class BondStereochemistry(StrEnum):
    U = "U"
    N = "N"
    E = "E"
    Z = "Z"


class SymbolType(StrEnum):
    LONE_PAIR = "LonePair"
    ELECTRON = "Electron"
    RADICAL_CATION = "RadicalCation"
    RADICAL_ANION = "RadicalAnion"
    CIRCLE_PLUS = "CirclePlus"
    CIRCLE_MINUS = "CircleMinus"
    DAGGER = "Dagger"
    DOUBLE_DAGGER = "DoubleDagger"
    PLUS = "Plus"
    MINUS = "Minus"
    RACEMIC = "Racemic"
    ABSOLUTE = "Absolute"
    RELATIVE = "Relative"
    LONE_PAIR_BAR = "LonePairBar"


class PolymerRepeatPattern(StrEnum):
    HEAD_TO_TAIL = "HeadToTail"
    HEAD_TO_HEAD = "HeadToHead"
    EITHER_UNKNOWN = "EitherUnknown"


class PolymerFlipType(StrEnum):
    UNSPECIFIED = "Unspecified"
    NO_FLIP = "NoFlip"
    FLIP = "Flip"


class OrbitalType(StrEnum):
    S = "s"
    P = "p"
    OVAL = "oval"
    LOBE = "lobe"
    HYBRID_PLUS = "hybridPlus"
    HYBRID_MINUS = "hybridMinus"
    DZ2_PLUS = "dz2Plus"
    DZ2_MINUS = "dz2Minus"
    DXY = "dxy"
    S_SHADED = "sShaded"
    S_FILLED = "sFilled"
    OVAL_SHADED = "ovalShaded"
    OVAL_FILLED = "ovalFilled"
    LOBE_SHADED = "lobeShaded"
    P_SHADED = "pShaded"
    LOBE_FILLED = "lobeFilled"
    P_FILLED = "pFilled"
    HYBRID_PLUS_FILLED = "hybridPlusFilled"
    HYBRID_MINUS_FILLED = "hybridMinusFilled"
    DZ2_PLUS_FILLED = "dz2PlusFilled"
    DZ2_MINUS_FILLED = "dz2MinusFilled"
    DXY_FILLED = "dxyFilled"


class LineType(StrEnum):
    SOLID = "Solid"
    DASHED = "Dashed"
    BOLD = "Bold"
    WAVY = "Wavy"


class BracketUsage(StrEnum):
    UNSPECIFIED = "Unspecified"
    ANYPOLYMER = "Anypolymer"
    COMPONENT = "Component"
    COPOLYMER = "Copolymer"
    COPOLYMER_ALTERNATING = "CopolymerAlternating"
    COPOLYMER_BLOCK = "CopolymerBlock"
    COPOLYMER_RANDOM = "CopolymerRandom"
    CROSSLINK = "Crosslink"
    GENERIC = "Generic"
    GRAFT = "Graft"
    MER = "Mer"
    MIXTURE_ORDERED = "MixtureOrdered"
    MIXTURE_UNORDERED = "MixtureUnordered"
    MODIFICATION = "Modification"
    MONOMER = "Monomer"
    MULTIPLE_GROUP = "MultipleGroup"
    SRU = "SRU"


class BracketType(StrEnum):
    ROUND_PAIR = "RoundPair"
    SQUARE_PAIR = "SquarePair"
    CURLY_PAIR = "CurlyPair"
    SQUARE = "Square"
    CURLY = "Curly"
    ROUND = "Round"


class ArrowType(StrEnum):
    NO_HEAD = "NoHead"
    HALF_HEAD = "HalfHead"
    FULL_HEAD = "FullHead"
    RESONANCE = "Resonance"
    EQUILIBRIUM = "Equilibrium"
    HOLLOW = "Hollow"
    RETRO_SYNTHETIC = "RetroSynthetic"
    NO_GO = "NoGo"
    DIPOLE = "Dipole"


class NoGo(StrEnum):
    UNSPECIFIED = "Unspecified"
    VALUE_NONE = "None"
    CROSS = "Cross"
    HASH = "Hash"


class FillType(StrEnum):
    UNSPECIFIED = "Unspecified"
    VALUE_NONE = "None"
    SOLID = "Solid"
    SHADED = "Shaded"


class ArrowheadType(StrEnum):
    SOLID = "Solid"
    HOLLOW = "Hollow"
    ANGLE = "Angle"


class ArrowheadSide(StrEnum):
    UNSPECIFIED = "Unspecified"
    VALUE_NONE = "None"
    FULL = "Full"
    HALF_LEFT = "HalfLeft"
    HALF_RIGHT = "HalfRight"


class GeometricFeature(StrEnum):
    UNKNOWN = "Unknown"
    POINT_FROM_POINT_POINT_DISTANCE = "PointFromPointPointDistance"
    POINT_FROM_POINT_POINT_PERCENTAGE = "PointFromPointPointPercentage"
    POINT_FROM_POINT_NORMAL_DISTANCE = "PointFromPointNormalDistance"
    LINE_FROM_POINTS = "LineFromPoints"
    PLANE_FROM_POINTS = "PlaneFromPoints"
    PLANE_FROM_POINT_LINE = "PlaneFromPointLine"
    CENTROID_FROM_POINTS = "CentroidFromPoints"
    NORMAL_FROM_POINT_PLANE = "NormalFromPointPlane"


class ConstraintType(StrEnum):
    UNKNOWN = "Unknown"
    DISTANCE = "Distance"
    ANGLE = "Angle"
    EXCLUSION_SPHERE = "ExclusionSphere"


class SpectrumYType(StrEnum):
    UNKNOWN = "Unknown"
    ABSORBANCE = "Absorbance"
    TRANSMITTANCE = "Transmittance"
    PERCENT_TRANSMITTANCE = "PercentTransmittance"
    OTHER = "Other"
    ARBITRARY_UNITS = "ArbitraryUnits"


class SpectrumXType(StrEnum):
    UNKNOWN = "Unknown"
    WAVENUMBERS = "Wavenumbers"
    MICRONS = "Microns"
    HERTZ = "Hertz"
    MASS_UNITS = "MassUnits"
    PARTS_PER_MILLION = "PartsPerMillion"
    OTHER = "Other"


class SpectrumClass(StrEnum):
    UNKNOWN = "Unknown"
    CHROMATOGRAM = "Chromatogram"
    INFRARED = "Infrared"
    UV_VIS = "UVVis"
    X_RAY_DIFFRACTION = "XRayDiffraction"
    MASS_SPECTRUM = "MassSpectrum"
    NMR = "NMR"
    RAMAN = "Raman"
    FLUORESCENCE = "Fluorescence"
    ATOMIC = "Atomic"


class TagType(StrEnum):
    UNKNOWN = "Unknown"
    STRING = "String"
    LONG = "Long"
    DOUBLE = "Double"


class PositioningType(StrEnum):
    AUTO = "auto"
    ANGLE = "angle"
    OFFSET = "offset"
    ABSOLUTE = "absolute"


class Side(StrEnum):
    UNDEFINED = "undefined"
    TOP = "top"
    LEFT = "left"
    BOTTOM = "bottom"
    RIGHT = "right"


class BioShapeType(StrEnum):
    UNDEFINED = "Undefined"
    VALUE_1_SUBSTRATE_ENZYME = "1SubstrateEnzyme"
    VALUE_2_SUBSTRATE_ENZYME = "2SubstrateEnzyme"
    RECEPTOR = "Receptor"
    G_PROTEIN_ALPHA = "GProteinAlpha"
    G_PROTEIN_BETA = "GProteinBeta"
    G_PROTEIN_GAMMA = "GProteinGamma"
    IMMUNOGLOBIN = "Immunoglobin"
    ION_CHANNEL = "IonChannel"
    ENDOPLASMIC_RETICULUM = "EndoplasmicReticulum"
    GOLGI = "Golgi"
    MEMBRANE_LINE = "MembraneLine"
    MEMBRANE_ARC = "MembraneArc"
    MEMBRANE_ELLIPSE = "MembraneEllipse"
    MEMBRANE_MICELLE = "MembraneMicelle"
    DNA = "DNA"
    HELIX_PROTEIN = "HelixProtein"
    MITOCHONDRION = "Mitochondrion"
    CLOUD = "Cloud"
    T_RNA = "tRNA"
    RIBOSOME_A = "RibosomeA"
    RIBOSOME_B = "RibosomeB"
