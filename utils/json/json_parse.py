import json
from dataclasses import dataclass, asdict
from typing import Optional, Any, Dict

__all__ = ["JsonParseError", "JsonParseResult", "parse_json"]


@dataclass(frozen=True)
class JsonParseError:
    message: str

    line: int
    column: int
    position: int

    context: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class JsonParseResult:
    valid: bool
    parsed: Optional[Any]
    error: Optional[JsonParseError]

    def to_dict(self) -> dict:
        data: Dict[str, Any] = {
            "valid": self.valid
        }

        if self.parsed is not None:
            data["parsed"] = self.parsed

        if self.error is not None:
            data["error"] = self.error.to_dict()

        return data


_ERROR_TRANSLATIONS = {
    "Expecting property name enclosed in double quotes": "Se esperaba un nombre de propiedad encerrado entre comillas dobles",
    "Expecting value": "Se esperaba un valor",
    "Expecting ',' delimiter": "Se esperaba una coma ',' como delimitador",
    "Expecting ':' delimiter": "Se esperaban dos puntos ':' después de la clave",
    "Extra data": "Se encontró información adicional después del final del JSON",
    "Unterminated string starting at": "Cadena sin terminar que comienza en",
    "Invalid control character": "Carácter de control inválido",
    "Invalid \\escape": "Secuencia de escape inválida",
    "Unterminated string": "Cadena sin terminar",
    "Invalid number": "Número inválido",
    "Expecting ',' or '}'": "Se esperaba ',' o '}'",
    "Illegal trailing comma before end of object": "Hay una coma sobrante justo antes del cierre del objeto",
}


def _translate_error_message(original_message: str) -> str:
    for english, spanish in _ERROR_TRANSLATIONS.items():
        if original_message.startswith(english):
            return original_message.replace(english, spanish)
    return original_message


def _build_error_context(text: str, line: int, column: int, position: int, context_margin: int = 40) -> str:
    lines = text.splitlines()

    if 0 <= line - 1 < len(lines):
        line_text = lines[line - 1]
    else:
        line_text = ""

    pointer = (" " * (column - 1)) + "^"

    start_ctx = max(0, position - context_margin)
    end_ctx = min(len(text), position + context_margin)
    context_snippet = text[start_ctx:end_ctx]

    if start_ctx > 0:
        context_snippet = "..." + context_snippet
    if end_ctx < len(text):
        context_snippet = context_snippet + "..."

    context_parts = [
        f"Contexto: {context_snippet}",
        f"Línea {line}, Columna {column}:",
        line_text,
        pointer
    ]

    return "\n".join(context_parts)


def parse_json(text: str) -> JsonParseResult:
    try:
        value = json.loads(text)
        return JsonParseResult(
            valid=True,
            parsed=value,
            error=None,
        )

    except json.JSONDecodeError as e:
        translated_message = _translate_error_message(e.msg)

        line = e.lineno
        column = e.colno
        position = e.pos

        context = _build_error_context(text, line, column, position)

        error = JsonParseError(
            message=translated_message,
            line=line,
            column=column,
            position=position,
            context=context
        )

        return JsonParseResult(
            valid=False,
            parsed=None,
            error=error,
        )
