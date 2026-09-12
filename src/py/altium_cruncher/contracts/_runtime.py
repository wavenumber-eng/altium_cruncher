"""Shared structural transport for TypeSpec-owned config families."""

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from jsonschema.protocols import Validator
    from jsonschema import ValidationError

from copy import deepcopy
from functools import lru_cache
from importlib.resources import files
import json
import math


@lru_cache(maxsize=None)
def config_metadata(stem: str) -> dict[str, object]:
    return json.loads(
        files("altium_cruncher.contracts.generated")
        .joinpath(f"{stem}.metadata.json")
        .read_text(encoding="utf-8")
    )


@lru_cache(maxsize=None)
def _validator(stem: str) -> Validator:
    from jsonschema import Draft202012Validator, validators

    schema = json.loads(
        files("altium_cruncher.contracts.generated")
        .joinpath(f"{stem}.schema.json")
        .read_text(encoding="utf-8")
    )
    validator_type = validators.extend(
        Draft202012Validator, {"x-acr-input": _validate_input_number}
    )
    return validator_type(schema)


def _validate_input_number(
    validator: Validator, kind: object, instance: object, schema: dict,
) -> Iterator[ValidationError]:
    if kind != "number" or not isinstance(instance, (str, bool)):
        return
    from jsonschema import ValidationError

    try:
        numeric = float(instance)
    except ValueError:
        yield ValidationError("must be a numeric spelling")
        return
    if not math.isfinite(numeric):
        yield ValidationError("must be a finite number")
        return
    yield from validator.descend(numeric, schema["anyOf"][0])


def _check_json(value: object, parents: set[int], label: str) -> None:
    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float) and math.isfinite(value):
        return
    if not isinstance(value, (dict, list)) or id(value) in parents:
        raise ValueError(f"{label} config must contain finite JSON values")
    parents.add(id(value))
    if isinstance(value, dict):
        if any(not isinstance(key, str) for key in value):
            raise ValueError(f"{label} config object keys must be strings")
        children = value.values()
    else:
        children = value
    for child in children:
        _check_json(child, parents, label)
    parents.remove(id(value))


def decode_config(value: object, stem: str, label: str) -> object:
    """Validate authored structure without applying defaults, coercion or merging."""
    _check_json(value, set(), label)
    error = next(_validator(stem).iter_errors(value), None)
    if error is not None:
        path = ".".join(str(part) for part in error.absolute_path) or "root"
        raise ValueError(f"{label} config field '{path}': {error.message}")
    return deepcopy(value)
