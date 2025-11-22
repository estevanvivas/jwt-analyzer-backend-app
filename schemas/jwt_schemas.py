from marshmallow import Schema, fields, validates, ValidationError, validate, INCLUDE

from domain.signing_algorithm import SigningAlgorithm


class StrictInt(fields.Int):

    def _deserialize(self, value, attr, data, **kwargs):
        if not isinstance(value, int) or isinstance(value, bool):
            raise self.make_error('invalid')
        return super()._deserialize(value, attr, data, **kwargs)


class AudienceField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, str):
            if not value:
                raise ValidationError('El campo "aud" no puede estar vacío.')
            return value
        elif isinstance(value, list):
            if not value:
                raise ValidationError('El campo "aud" no puede ser una lista vacía.')
            for item in value:
                if not isinstance(item, str) or not item:
                    raise ValidationError('Cada elemento de "aud" debe ser una cadena no vacía.')
            return value
        else:
            raise ValidationError('El campo "aud" debe ser una cadena o una lista de cadenas.')


class HeaderSchema(Schema):
    class Meta:
        unknown = INCLUDE

    alg = fields.Str(
        required=True,
        error_messages={
            "required": 'El campo "alg" es obligatorio.',
            "null": 'El campo "alg" no puede ser nulo.',
            "invalid": 'El campo "alg" debe ser una cadena válida.'
        }
    )

    typ = fields.Str(
        required=True,
        error_messages={
            "required": 'El campo "typ" es obligatorio.',
            "null": 'El campo "typ" no puede ser nulo.',
            "invalid": 'El campo "typ" debe ser una cadena válida.'
        }
    )

    @validates("typ")
    def validate_typ(self, value, **kwargs):
        if value.upper() != "JWT":
            raise ValidationError('El tipo debe ser "JWT".')
        return value.upper()

    @validates("alg")
    def validate_alg(self, value, **kwargs):
        valid_algorithms = [a.value.upper() for a in SigningAlgorithm]
        upper_value = value.upper()
        if upper_value not in valid_algorithms:
            raise ValidationError(
                f'El algoritmo "{value}" no está soportado. Algoritmos válidos: {", ".join(valid_algorithms)}.'
            )

        return upper_value


class PayloadSchema(Schema):
    class Meta:
        unknown = INCLUDE

    iss = fields.Str(
        required=False,
        allow_none=False,
        validate=validate.Length(min=1),
        error_messages={
            "invalid": 'El campo "iss" debe ser una cadena válida.',
            "null": 'El campo "iss" no puede ser nulo.',
            "validator_failed": 'El campo "iss" no puede estar vacío.'
        }
    )

    sub = fields.Str(
        required=False,
        allow_none=False,
        validate=validate.Length(min=1),
        error_messages={
            "invalid": 'El campo "sub" debe ser una cadena válida.',
            "null": 'El campo "sub" no puede ser nulo.',
            "validator_failed": 'El campo "sub" no puede estar vacío.'
        }
    )

    aud = AudienceField(
        required=False
    )

    exp = StrictInt(
        required=False,
        validate=validate.Range(min=0),
        error_messages={
            "invalid": 'El campo "exp" debe ser un entero (timestamp).',
            "validator_failed": 'El campo "exp" debe ser un entero mayor o igual a 0.',
            "null": 'El campo "exp" no puede ser nulo.'
        }
    )

    nbf = StrictInt(
        required=False,
        validate=validate.Range(min=0),
        error_messages={
            "invalid": 'El campo "nbf" debe ser un entero (timestamp).',
            "validator_failed": 'El campo "nbf" debe ser un entero mayor o igual a 0.',
            "null": 'El campo "nbf" no puede ser nulo.'
        }
    )

    iat = StrictInt(
        required=False,
        validate=validate.Range(min=0),
        error_messages={
            "invalid": 'El campo "iat" debe ser un entero (timestamp).',
            "validator_failed": 'El campo "iat" debe ser un entero mayor o igual a 0.',
            "null": 'El campo "iat" no puede ser nulo.'
        }
    )

    jti = fields.Str(
        required=False,
        allow_none=False,
        validate=validate.Length(min=1),
        error_messages={
            "invalid": 'El campo "jti" debe ser una cadena válida.',
            "null": 'El campo "jti" no puede ser nulo.',
            "validator_failed": 'El campo "jti" no puede estar vacío.'
        }
    )
