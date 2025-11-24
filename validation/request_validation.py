from functools import wraps
from http import HTTPStatus
from typing import Type, Callable

from flask import request
from marshmallow import ValidationError, Schema

from type_defs.json_types import JsonObject
from utils.response_factory import error_response


def validate_req_body(schema_class: Type[Schema]):
    from type_defs.http_types import HttpResponse
    def decorator(f: Callable[[JsonObject], HttpResponse]) -> Callable[[], HttpResponse]:
        @wraps(f)
        def wrapper() -> HttpResponse:
            data = request.get_json(silent=True)
            if data is None:
                return error_response(
                    message="Encabezado 'Content-Type' debe ser 'application/json' y el cuerpo debe contener JSON válido.",
                    status=HTTPStatus.BAD_REQUEST
                )

            try:
                schema = schema_class()
                validated = schema.load(data)
            except ValidationError as e:
                return error_response(
                    message="Error de validación en el cuerpo de la solicitud",
                    errors=e.messages,
                    status=HTTPStatus.UNPROCESSABLE_ENTITY
                )

            return f(validated)

        return wrapper

    return decorator
