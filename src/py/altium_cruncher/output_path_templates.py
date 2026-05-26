"""Shared output path template resolution for command outputs."""

from __future__ import annotations

import re
from collections.abc import Mapping
from pathlib import PurePosixPath
from typing import Literal

TemplateValue = str | int | float | bool | None
MissingPolicy = Literal["error", "empty"]

_IDENTIFIER_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_BRACE_TOKEN_RE = re.compile(r"\{(?P<name>[A-Za-z_][A-Za-z0-9_]*)\}")
_DRIVE_PREFIX_RE = re.compile(r"^[A-Za-z]:")
_INVALID_PATH_CHARS_RE = re.compile(r'[<>:"|?*\x00-\x1f]')
_TRAVERSAL_PARTS = {".", ".."}


class OutputPathTemplateError(ValueError):
    """Base error for output path template resolution failures."""


class MissingOutputPathParameterError(OutputPathTemplateError):
    """Raised when a template references an unknown parameter."""


def resolve_output_expression(
    expression: str,
    project_parameters: Mapping[str, TemplateValue],
    *,
    variant_name: str | None = None,
    tokens: Mapping[str, TemplateValue] | None = None,
    missing: MissingPolicy = "error",
) -> str:
    """Resolve a string expression using project parameters and runtime tokens."""
    lookup = _build_lookup(project_parameters, variant_name=variant_name, tokens=tokens)
    if _uses_concat_expression(expression):
        return _evaluate_concat_expression(expression, lookup, missing=missing)
    return _evaluate_brace_template(expression, lookup, missing=missing)


def resolve_output_relative_path(
    expression: str,
    project_parameters: Mapping[str, TemplateValue],
    *,
    variant_name: str | None = None,
    tokens: Mapping[str, TemplateValue] | None = None,
    missing: MissingPolicy = "error",
) -> PurePosixPath:
    """Resolve a template expression and return a safe relative output path."""
    resolved = resolve_output_expression(
        expression,
        project_parameters,
        variant_name=variant_name,
        tokens=tokens,
        missing=missing,
    )
    return sanitize_relative_output_path(resolved)


def resolve_output_name(
    expression: str,
    project_parameters: Mapping[str, TemplateValue],
    *,
    variant_name: str | None = None,
    tokens: Mapping[str, TemplateValue] | None = None,
    missing: MissingPolicy = "error",
) -> str:
    """Resolve a template expression and return a safe single path component."""
    resolved = resolve_output_expression(
        expression,
        project_parameters,
        variant_name=variant_name,
        tokens=tokens,
        missing=missing,
    )
    if "/" in resolved or "\\" in resolved:
        raise OutputPathTemplateError(f"Output name must not contain path separators: {resolved!r}")
    return _sanitize_path_part(resolved)


def sanitize_relative_output_path(path_text: str) -> PurePosixPath:
    """Normalize and sanitize a generated relative output path."""
    normalized = str(path_text).strip().replace("\\", "/")
    if not normalized:
        raise OutputPathTemplateError("Output path template resolved to an empty path")
    if normalized.startswith("/") or normalized.startswith("//"):
        raise OutputPathTemplateError(f"Output path must be relative: {path_text!r}")
    if _DRIVE_PREFIX_RE.match(normalized):
        raise OutputPathTemplateError(f"Output path must not include a drive prefix: {path_text!r}")

    parts: list[str] = []
    for raw_part in normalized.split("/"):
        part = raw_part.strip()
        if not part:
            continue
        if part in _TRAVERSAL_PARTS:
            raise OutputPathTemplateError(f"Output path must not contain traversal: {path_text!r}")
        parts.append(_sanitize_path_part(part))

    if not parts:
        raise OutputPathTemplateError("Output path template resolved to no usable path parts")
    return PurePosixPath(*parts)


def _build_lookup(
    project_parameters: Mapping[str, TemplateValue],
    *,
    variant_name: str | None,
    tokens: Mapping[str, TemplateValue] | None,
) -> dict[str, str]:
    """Build the case-preserving token lookup used by both expression styles."""
    lookup = {str(name): _stringify_value(value) for name, value in project_parameters.items()}
    if tokens:
        lookup.update({str(name): _stringify_value(value) for name, value in tokens.items()})
    if variant_name is not None:
        lookup["VariantName"] = variant_name
    return lookup


def _stringify_value(value: TemplateValue) -> str:
    """Convert a template value to the text used in generated paths."""
    if value is None:
        return ""
    return str(value)


def _uses_concat_expression(expression: str) -> bool:
    """Return whether a template uses Altium-style `+` concatenation."""
    stripped = expression.strip()
    return stripped.startswith(("'", '"')) or _has_unquoted_plus(stripped)


def _has_unquoted_plus(text: str) -> bool:
    """Return whether text contains a plus sign outside quoted literals."""
    quote: str | None = None
    for char in text:
        if quote is not None:
            if char == quote:
                quote = None
            continue
        if char in ("'", '"'):
            quote = char
            continue
        if char == "+":
            return True
    return False


def _evaluate_brace_template(
    template: str,
    lookup: Mapping[str, str],
    *,
    missing: MissingPolicy,
) -> str:
    """Resolve `{Name}` placeholders in a literal template string."""

    def replace_match(match: re.Match[str]) -> str:
        name = match.group("name")
        return _lookup_token(name, lookup, missing=missing)

    return _BRACE_TOKEN_RE.sub(replace_match, template)


def _evaluate_concat_expression(
    expression: str,
    lookup: Mapping[str, str],
    *,
    missing: MissingPolicy,
) -> str:
    """Evaluate a constrained Altium-style expression with strings and names."""
    parts: list[str] = []
    index = 0
    expect_term = True

    while index < len(expression):
        char = expression[index]
        if char in " \t\r\n":
            index += 1
            continue
        if char == "+":
            if expect_term:
                raise OutputPathTemplateError(f"Unexpected '+' in expression: {expression!r}")
            expect_term = True
            index += 1
            continue
        if not expect_term:
            raise OutputPathTemplateError(f"Expected '+' in expression: {expression!r}")

        part, index = _parse_concat_term(expression, index, lookup, missing=missing)
        parts.append(part)
        expect_term = False

    if expect_term and parts:
        raise OutputPathTemplateError(f"Expression ends with '+': {expression!r}")
    return "".join(parts)


def _parse_concat_term(
    expression: str,
    index: int,
    lookup: Mapping[str, str],
    *,
    missing: MissingPolicy,
) -> tuple[str, int]:
    """Parse one quoted string or identifier term from a concat expression."""
    char = expression[index]
    if char in ("'", '"'):
        return _parse_quoted_literal(expression, index)

    match = _IDENTIFIER_RE.match(expression, index)
    if match is None:
        raise OutputPathTemplateError(
            f"Expected quoted literal or parameter name in expression: {expression!r}"
        )
    name = match.group(0)
    return _lookup_token(name, lookup, missing=missing), match.end()


def _parse_quoted_literal(expression: str, index: int) -> tuple[str, int]:
    """Parse a single- or double-quoted literal from a concat expression."""
    quote = expression[index]
    end = expression.find(quote, index + 1)
    if end == -1:
        raise OutputPathTemplateError(f"Unterminated quoted literal in expression: {expression!r}")
    return expression[index + 1 : end], end + 1


def _lookup_token(
    name: str,
    lookup: Mapping[str, str],
    *,
    missing: MissingPolicy,
) -> str:
    """Look up a token name using exact and case-insensitive matching."""
    if name in lookup:
        return lookup[name]
    lower_name = name.casefold()
    for key, value in lookup.items():
        if key.casefold() == lower_name:
            return value
    if missing == "empty":
        return ""
    raise MissingOutputPathParameterError(f"Unknown output template parameter: {name}")


def _sanitize_path_part(part: str) -> str:
    """Return one safe path component."""
    sanitized = _INVALID_PATH_CHARS_RE.sub("_", part).strip()
    if not sanitized or sanitized in _TRAVERSAL_PARTS:
        raise OutputPathTemplateError(f"Output path component is not usable: {part!r}")
    return sanitized
