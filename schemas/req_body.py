from marshmallow import Schema, fields, validates, ValidationError, validate, EXCLUDE

from schemas.jwt_schemas import HeaderSchema, PayloadSchema


class BuildTokenReqSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    header = fields.Nested(
        HeaderSchema(),
        required=True,
        error_messages={"required": 'El campo "header" es obligatorio.'}
    )

    payload = fields.Nested(
        PayloadSchema(),
        required=True,
        error_messages={"required": 'El campo "payload" es obligatorio.'}
    )

    secret = fields.Str(
        required=True,
        validate=validate.Length(min=8),
        error_messages={
            "required": 'La clave secreta es obligatoria.',
            "validator_failed": 'La clave secreta debe tener al menos 8 caracteres.'
        }
    )

    @validates("payload")
    def validate_payload(self, value, **kwargs):
        if not value:
            raise ValidationError('El payload no puede estar vacío.')

class AnalyzeTokenReqSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    token = fields.Str(
        required=True,
        error_messages={
            "required": 'El campo "token" es obligatorio.',
            "null": 'El campo "token" no puede ser nulo.',
            "invalid": 'El campo "token" debe ser una cadena válida.'
        }
    )

    secret = fields.Str(
        required=False,
    )