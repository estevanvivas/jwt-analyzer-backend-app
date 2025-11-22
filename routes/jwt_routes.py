from http import HTTPStatus

from flask import Blueprint

from schemas.req_body import AnalyzeTokenReqSchema
from schemas.req_body import BuildTokenReqSchema
from services.jwt_service import JwtService
from type_defs.http_types import HttpResponse
from type_defs.json_types import JsonObject
from utils.response_factory import response
from validation.request_validation import validate_req_body

jwt_bp = Blueprint("jwt", __name__)
jwt_service = JwtService()


@jwt_bp.post("/build")
@validate_req_body(BuildTokenReqSchema)
def build_jwt(req_body: JsonObject) -> HttpResponse:
    header = req_body["header"]
    payload = req_body["payload"]
    secret_key = req_body["secret"]

    token_data = jwt_service.build_token(header, payload, secret_key)

    return response(
        data=dict(token_data),
        message="Token creado correctamente.",
        status=HTTPStatus.OK
    )


@jwt_bp.post("/analyze")
@validate_req_body(AnalyzeTokenReqSchema)
def analyze_jwt(req_body):
    token = req_body["token"]
    secret = req_body.get("secret", None)
    analysis_result = jwt_service.analyze_token(token, secret)

    return response(
        data=dict(analysis_result),
        message="Análisis del token completado correctamente.",
        status=HTTPStatus.OK
    )


@jwt_bp.get("/test-cases")
def get_jwt_test_cases() -> HttpResponse:
    data = jwt_service.get_test_cases()
    return response(
        data=[dict(case) for case in data],
        message="Casos de prueba obtenidos correctamente.",
        status=HTTPStatus.OK
    )
