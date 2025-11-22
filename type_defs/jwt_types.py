from typing import TypedDict, List, NotRequired, Dict

from type_defs.json_types import JsonObject, ValidationErrors
from utils.json.json_grammar import DerivationResult


class TokenComponents(TypedDict):
    header: str
    payload: str
    signature: str


class TokenCreationResult(TypedDict):
    token: str
    parts: TokenComponents


class TokenSegment(TypedDict):
    value: str
    start: int
    end: int


class TokenSegments(TypedDict):
    header: TokenSegment
    payload: TokenSegment
    signature: TokenSegment


class DecodedComponents(TypedDict):
    header: str
    payload: str


class LexicalAnalysisResult(TypedDict):
    errors: List[str]
    segments: NotRequired[TokenSegments]
    decoded: NotRequired[DecodedComponents]


class JsonComponentError(TypedDict):
    message: str
    line: NotRequired[int]
    column: NotRequired[int]
    position: NotRequired[int]
    context: NotRequired[str]


class SyntacticComponentAnalysisResult(TypedDict):
    parsed: NotRequired[JsonObject]
    error: NotRequired[JsonComponentError]
    derivation: NotRequired[DerivationResult]


class SyntacticAnalysisResult(TypedDict):
    header: SyntacticComponentAnalysisResult
    payload: SyntacticComponentAnalysisResult


class SymbolsTableEntry(TypedDict):
    name: str
    type: str
    value: str


class ComponentSemanticAnalysisResult(TypedDict):
    errors: Dict[str, List[str]]
    symbols: List[SymbolsTableEntry]


class TokenMeta(TypedDict):
    expiration: str
    expired: bool

class SemanticAnalysisResult(TypedDict):
    header: ComponentSemanticAnalysisResult
    payload: ComponentSemanticAnalysisResult
    metadata: NotRequired[TokenMeta]


class AnalyzeTokenResult(TypedDict):
    lexical: LexicalAnalysisResult
    syntactic: NotRequired[SyntacticAnalysisResult]
    semantic: NotRequired[SemanticAnalysisResult]
    cryptographic: NotRequired[bool]


class TokenTestCase(TypedDict):
    token: str
    description: str
    valid: bool
    secret: NotRequired[str]
