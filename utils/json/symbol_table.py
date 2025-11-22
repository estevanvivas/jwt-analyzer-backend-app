from typing import List

from type_defs.json_types import JsonObject, JsonValue
from type_defs.jwt_types import SymbolsTableEntry


def build_symbol_table(data: JsonObject, prefix: str = "") -> List[SymbolsTableEntry]:
    symbols: List[SymbolsTableEntry] = []

    if isinstance(data, dict):
        for key, value in data.items():
            path = f"{prefix}.{key}" if prefix else key
            symbols.extend(_process_value(value, path))
    elif isinstance(data, list):
        for i, item in enumerate(data):
            path = f"{prefix}[{i}]"
            symbols.extend(_process_value(item, path))
    else:
        if prefix:
            symbols.extend(_process_value(data, prefix))

    return symbols


def _process_value(value: JsonValue, path: str) -> List[SymbolsTableEntry]:
    symbols: List[SymbolsTableEntry] = []

    if value is None:
        symbols.append({
            "name": path,
            "type": "null",
            "value": "null",
        })
    elif isinstance(value, bool):
        symbols.append({
            "name": path,
            "type": "boolean",
            "value": "true" if value else "false",
        })
    elif isinstance(value, (int, float)):
        symbols.append({
            "name": path,
            "type": "number",
            "value": str(value),
        })
    elif isinstance(value, str):
        symbols.append({
            "name": path,
            "type": "string",
            "value": value
        })
    elif isinstance(value, dict):
        symbols.append({
            "name": path,
            "type": "object",
            "value": f"{{...}} ({len(value)} claves)",
        })
        symbols.extend(build_symbol_table(value, path))
    elif isinstance(value, list):
        symbols.append({
            "name": path,
            "type": "array",
            "value": f"[...] ({len(value)} elementos)",
        })

        for i, item in enumerate(value):
            item_path = f"{path}[{i}]"
            symbols.extend(_process_value(item, item_path))

    return symbols

__all__ = ['build_symbol_table']