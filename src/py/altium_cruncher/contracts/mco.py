"""MCO authored transport and reached-operation validation from TypeSpec contracts."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from importlib.resources import files
import json
from typing import TYPE_CHECKING, TypedDict, cast

if TYPE_CHECKING:
    from jsonschema.protocols import Validator


class OperationMetadata(TypedDict):
    name: str
    aliases: list[str]
    args_ref: str


# JSON Schema keyword spellings cannot all be class-syntax field names.
ArgumentSchema = TypedDict("ArgumentSchema", {
    "type": str, "properties": dict[str, "ArgumentSchema"],
    "items": "ArgumentSchema", "anyOf": list["ArgumentSchema"],
    "default": object, "$ref": str, "$defs": dict[str, "ArgumentSchema"],
}, total=False)

from ._runtime import config_metadata, decode_config, _validator
from .generated.mco_input import McoInput


def mco_metadata() -> dict[str, object]:
    return config_metadata("mco_input")


@lru_cache(maxsize=1)
def _schema() -> ArgumentSchema:
    return json.loads(
        files("altium_cruncher.contracts.generated")
        .joinpath("mco_input.schema.json")
        .read_text(encoding="utf-8")
    )


@lru_cache(maxsize=1)
def _operations() -> dict[str, OperationMetadata]:
    return {
        tag: info
        for info in cast(list[OperationMetadata], mco_metadata()["operations"])
        for tag in [info["name"], *info["aliases"]]
    }


def decode_mco(value: object) -> McoInput:
    """Validate all authored operations, preserving fields and omission for editors."""
    return cast(McoInput, decode_config(value, "mco_input", "MCO"))


def encode_mco(value: McoInput) -> str:
    return json.dumps(decode_mco(value), ensure_ascii=False, indent=2) + "\n"


def validate_execution_envelope(value: object) -> None:
    """Check ordering/container fields without inspecting custom or skipped args."""
    error = next(_validator("mco_envelope").iter_errors(value), None)
    if error is not None:
        raise ValueError(f"Invalid MCO envelope: {error.message}")


@lru_cache(maxsize=None)
def _argument_validator(op: str) -> Validator:
    from jsonschema import Draft202012Validator, validators

    # Programmatic MCO callers have always been allowed tuple coordinates.
    checker = Draft202012Validator.TYPE_CHECKER.redefine(
        "array", lambda _, value: isinstance(value, (list, tuple))
    )
    validator_type = validators.extend(Draft202012Validator, type_checker=checker)
    return validator_type(
        {"$ref": _operations()[op]["args_ref"], "$defs": _schema()["$defs"]}
    )


def validate_builtin_args(op: str, args: dict[str, object]) -> dict[str, object]:
    """Validate reached built-in args and copy only native integer representations."""
    validator = _argument_validator(op)
    error = next(validator.iter_errors(args), None)
    if error is not None:
        path = ".".join(str(part) for part in error.absolute_path) or "args"
        raise ValueError(f"{op} field '{path}': {error.message}")

    return cast(dict[str, object], _native_integers(
        args, {"$ref": _operations()[op]["args_ref"]}, validator,
    ))


def _native_integers(value: object, schema: ArgumentSchema, validator: Validator) -> object:
    """Copy only changed paths; custom extension values retain their identity."""
    schema = _resolved_argument_schema(value, schema, validator)
    if schema is None:
        return value
    if schema.get("type") == "integer" and isinstance(value, float):
        return int(value)
    if isinstance(value, dict) and "properties" in schema:
        return _native_object_integers(value, schema["properties"], validator)
    if isinstance(value, (list, tuple)) and "items" in schema:
        return _native_array_integers(value, schema["items"], validator)
    return value


def _resolved_argument_schema(
    value: object, schema: ArgumentSchema, validator: Validator,
) -> ArgumentSchema | None:
    if "$ref" in schema:
        return _resolved_argument_schema(value, _schema()["$defs"][schema["$ref"].split("/")[-1]], validator)
    if "anyOf" in schema:
        for branch in schema["anyOf"]:
            if validator.evolve(schema=branch).is_valid(value):
                return _resolved_argument_schema(value, branch, validator)
        return None
    return schema


def _native_object_integers(
    value: dict[str, object], properties: dict[str, ArgumentSchema], validator: Validator,
) -> dict[str, object]:
    result = {key: _native_integers(item, properties[key], validator)
              if key in properties else item for key, item in value.items()}
    return value if all(result[key] is item for key, item in value.items()) else result


def _native_array_integers(
    value: list[object] | tuple[object, ...], items: ArgumentSchema, validator: Validator,
) -> list[object] | tuple[object, ...]:
    result = [_native_integers(item, items, validator) for item in value]
    if all(a is b for a, b in zip(result, value)):
        return value
    return tuple(result) if isinstance(value, tuple) else result


def mco_default(op: str, name: str) -> object:
    """A static fallback declared on the operation argument; never edits authored input."""
    model = _schema()["$defs"][_operations()[op]["args_ref"].split("/")[-1]]
    return deepcopy(model["properties"][name]["default"])


def mco_model_default(model: str, name: str) -> object:
    """Static fallback shared by a nested argument model."""
    return deepcopy(_schema()["$defs"][model]["properties"][name]["default"])
