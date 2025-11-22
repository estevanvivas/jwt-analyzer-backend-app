from typing import Dict, Union, List

JsonPrimitive = Union[str, int, float, bool, None]

JsonValue = Union[JsonPrimitive, List["JsonValue"], Dict[str, "JsonValue"]]

JsonObject = Dict[str, JsonValue]

ValidationErrorValue = Union[List[str], Dict[str, "ValidationErrorValue"]]
ValidationErrors = Dict[str, ValidationErrorValue]