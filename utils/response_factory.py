from http import HTTPStatus
from typing import Optional, Union, List

from flask import jsonify

from type_defs.http_types import HttpResponse
from type_defs.json_types import JsonObject, ValidationErrors, JsonValue


def response(data: Optional[Union[JsonObject, List[JsonValue]]] = None,
             message: str = "Operación exitosa.",
             status: HTTPStatus = HTTPStatus.OK) -> HttpResponse:
    response: JsonObject = {
        "message": message,
        "status": status.value
    }

    if data is not None:
        response["data"] = data

    return jsonify(response), status.value


def error_response(message: str = "Ha ocurrido un error.",
                   errors: Optional[ValidationErrors] = None,
                   status: HTTPStatus = HTTPStatus.BAD_REQUEST) -> HttpResponse:
    response: JsonObject = {
        "message": message,
        "status": status.value
    }

    if errors is not None:
        response["details"] = errors

    return jsonify(response), status.value
