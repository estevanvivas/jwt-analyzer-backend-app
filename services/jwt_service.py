import datetime
import hmac
import json
import re
import time
from typing import List, Type, Optional

from datetime import datetime
from marshmallow import Schema

from domain.signing_algorithm import SigningAlgorithm
from schemas.jwt_schemas import HeaderSchema, PayloadSchema
from services.firebase_client import get_db
from type_defs.json_types import JsonObject, ValidationErrors
from type_defs.jwt_types import TokenCreationResult, LexicalAnalysisResult, TokenSegment, TokenSegments, \
    DecodedComponents, SyntacticComponentAnalysisResult, SyntacticAnalysisResult, SemanticAnalysisResult, \
    ComponentSemanticAnalysisResult, AnalyzeTokenResult, TokenTestCase, TokenMeta
from utils.base64 import encode_base64_url, decode_base64_url
from utils.json import parse_json, analyze_json_grammar
from utils.json.symbol_table import build_symbol_table


class JwtService:

    def create_signature_hmac(self, message: str, secret: str, alg: SigningAlgorithm) -> str:
        hash_function = alg.get_hash_function()
        raw_sig = hmac.new(
            secret.encode(),
            message.encode(),
            hash_function
        ).digest()
        return encode_base64_url(raw_sig)

    def build_token(self, header: JsonObject, payload: JsonObject, secret_key: str) -> TokenCreationResult:
        encoded_header = encode_base64_url(json.dumps(header, separators=(',', ':')))
        encoded_payload = encode_base64_url(json.dumps(payload, separators=(',', ':')))

        algorithm = SigningAlgorithm(header.get("alg"))

        encoded_signature = self.create_signature_hmac(
            message=f"{encoded_header}.{encoded_payload}",
            secret=secret_key,
            alg=algorithm
        )

        return {
            "token": f"{encoded_header}.{encoded_payload}.{encoded_signature}",
            "parts": {
                "header": encoded_header,
                "payload": encoded_payload,
                "signature": encoded_signature
            }
        }

    def analyze_token(self, token: str, secret: Optional[str]) -> AnalyzeTokenResult:
        lexical_analysis = self.lexical_analysis(token)
        analysis_result: AnalyzeTokenResult = {
            "lexical": lexical_analysis
        }
        if lexical_analysis["errors"]:
            return analysis_result

        syntactic_analysis = self.syntactic_analysis(lexical_analysis["decoded"])

        analysis_result["syntactic"] = syntactic_analysis

        if "error" in syntactic_analysis["header"] or "error" in syntactic_analysis["payload"]:
            return analysis_result

        parsed_header = syntactic_analysis["header"]["parsed"]
        parsed_payload = syntactic_analysis["payload"]["parsed"]
        semantic_analysis = self.semantic_analysis(
            parsed_header=parsed_header,
            parsed_payload=parsed_payload
        )

        analysis_result["semantic"] = semantic_analysis

        if not secret or semantic_analysis["header"]["errors"].get("alg", None):
            return analysis_result

        signature_valid = self.check_signature(
            segments=lexical_analysis["segments"],
            alg=SigningAlgorithm(parsed_header["alg"]),
            secret=secret
        )

        analysis_result["cryptographic"] = signature_valid

        return analysis_result

    def syntactic_analysis(self, decoded_components: DecodedComponents) -> SyntacticAnalysisResult:
        header_result = self._parse_segment(decoded_components["header"])
        payload_result = self._parse_segment(decoded_components["payload"])

        return {
            "header": header_result,
            "payload": payload_result
        }

    def _parse_segment(self, json_string: str) -> SyntacticComponentAnalysisResult:
        parse_result = parse_json(text=json_string)
        if not parse_result.valid:
            return {
                "error": {
                    "message": parse_result.error.message,
                    "line": parse_result.error.line,
                    "column": parse_result.error.column,
                    "position": parse_result.error.position,
                    "context": parse_result.error.context
                }
            }

        if not isinstance(parse_result.parsed, dict):
            return {
                "error": {
                    "message": "No es un objeto JSON válido."
                }
            }

        grammar_result = analyze_json_grammar(json_string=json_string)
        return {
            "parsed": parse_result.parsed,
            "derivation": grammar_result
        }

    def lexical_analysis(self, token: str) -> LexicalAnalysisResult:
        errors: List[str] = []

        parts = token.split('.')
        if len(parts) != 3:
            errors.append("El token debe contener exactamente tres segmentos separados por puntos")
            return {"errors": errors}

        header_seg, payload_seg, signature_seg = parts

        start = 0
        end = len(header_seg)
        header_segment: TokenSegment = {"value": header_seg, "start": start, "end": end}

        start = end + 1
        end = start + len(payload_seg)
        payload_segment: TokenSegment = {"value": payload_seg, "start": start, "end": end}

        start = end + 1
        end = start + len(signature_seg)
        signature_segment: TokenSegment = {"value": signature_seg, "start": start, "end": end}

        segments: TokenSegments = {
            "header": header_segment,
            "payload": payload_segment,
            "signature": signature_segment
        }

        base64url_pattern = re.compile(r'^[A-Za-z0-9_-]+$')

        if not base64url_pattern.match(header_seg):
            errors.append("El segmento header contiene caracteres inválidos para base64url")

        if not base64url_pattern.match(payload_seg):
            errors.append("El segmento payload contiene caracteres inválidos para base64url")

        if errors:
            return {"segments": segments, "errors": errors}

        decoded: DecodedComponents = {
            "header": decode_base64_url(header_seg),
            "payload": decode_base64_url(payload_seg)
        }

        print(decoded)

        return {"errors": errors, "segments": segments, "decoded": decoded}

    def semantic_analysis(self, parsed_header: JsonObject, parsed_payload: JsonObject) -> SemanticAnalysisResult:
        result: SemanticAnalysisResult = {
            "header": self._semantic_analysis_segment(parsed_header, schema=HeaderSchema),
            "payload": self._semantic_analysis_segment(parsed_payload, schema=PayloadSchema)
        }

        if parsed_payload.get("exp", None) is not None:
            expiration = datetime.fromtimestamp(parsed_payload["exp"]).strftime("%Y-%m-%d %H:%M:%S")
            expired = int(time.time()) >= parsed_payload["exp"]

            meta: TokenMeta = {
                "expiration": expiration,
                "expired": expired
            }

            result["metadata"] = meta

        return result

    def _semantic_analysis_segment(self, data: JsonObject, schema: Type[Schema]) -> ComponentSemanticAnalysisResult:
        errors = self._validate_fields(data, schema)
        symbols = build_symbol_table(data)

        return {
            "errors": errors,
            "symbols": symbols
        }

    def _validate_fields(self, data: JsonObject, schema: Type[Schema]) -> ValidationErrors:
        schema_instance = schema()
        return schema_instance.validate(data)

    def check_signature(self, segments: TokenSegments, alg: SigningAlgorithm, secret: str) -> bool:
        token_signature = segments["signature"]["value"]
        message = f"{segments['header']['value']}.{segments['payload']['value']}"
        expected_signature = self.create_signature_hmac(
            message=message,
            secret=secret,
            alg=alg
        )

        return hmac.compare_digest(token_signature, expected_signature)

    def get_test_cases(self) -> List[TokenTestCase]:
        db = get_db()
        test_cases_ref = db.collection("test_cases")
        docs = test_cases_ref.stream()

        test_cases: List[TokenTestCase] = []
        for doc in docs:
            test_cases.append(doc.to_dict())

        return test_cases
