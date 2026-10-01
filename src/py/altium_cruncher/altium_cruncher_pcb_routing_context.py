"""Compact authored PCB routing context for design-review bundles."""

from __future__ import annotations

import json
import math
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import fields, is_dataclass
from enum import Enum
from pathlib import Path

from altium_monkey import PcbNetClassKind
from altium_monkey.altium_pcb_rule import AltiumPcbRule


PCB_ROUTING_CONTEXT_SCHEMA = "altium_cruncher.pcb_routing_context.a0"

_RULE_ENVELOPE_FIELDS = frozenset(field.name for field in fields(AltiumPcbRule))
_NO_JSON_SCALAR = object()
_SCOPE_CLASS_REFERENCE_FUNCTIONS = {
    "innetclass": ("InNetClass", "net_class"),
    "indifferentialpairclass": (
        "InDifferentialPairClass",
        "differential_pair_class",
    ),
}


class _UnsupportedJsonValue(TypeError):
    pass


def build_pcb_routing_context_payload(
    pcbdoc: object,
    *,
    source: str,
    board: str | None,
) -> dict[str, object]:
    """Build deterministic, agent-facing PCB class/pair/rule evidence."""
    if not source:
        raise ValueError("PCB routing-context source must not be empty")

    diagnostics: list[dict[str, object]] = []
    nets = list(getattr(pcbdoc, "nets", ()) or ())
    pairs = list(getattr(pcbdoc, "differential_pairs", ()) or ())
    rules = list(getattr(pcbdoc, "rules", ()) or ())
    mixed_classes = list(getattr(pcbdoc, "net_classes", ()) or ())
    net_classes = [
        (index, item)
        for index, item in enumerate(mixed_classes)
        if _class_kind(item) == int(PcbNetClassKind.NET)
    ]
    differential_pair_classes = [
        (index, item)
        for index, item in enumerate(mixed_classes)
        if _class_kind(item) == int(PcbNetClassKind.DIFF_PAIR)
    ]

    net_name_index = _name_index(nets)
    pair_name_index = _name_index(pairs)
    _append_duplicate_name_diagnostics(
        diagnostics,
        rows=nets,
        name_index=net_name_index,
        source_collection="nets",
        code="duplicate_net_name",
    )
    _append_duplicate_name_diagnostics(
        diagnostics,
        rows=pairs,
        name_index=pair_name_index,
        source_collection="differential_pairs",
        code="duplicate_differential_pair_name",
    )

    net_memberships = [
        {
            "net": _source_name(net),
            "unique_id": _unique_id(net),
            "net_classes": [],
            "differential_pairs": [],
            "differential_pair_classes": [],
        }
        for net in nets
    ]
    pair_rows = [
        {
            "name": _source_name(pair),
            "unique_id": _unique_id(pair),
            "positive_net": str(getattr(pair, "positive_net_name", "") or ""),
            "negative_net": str(getattr(pair, "negative_net_name", "") or ""),
            "stored_classes": [],
        }
        for pair in pairs
    ]

    _join_pairs_to_nets(
        pairs,
        net_name_index=net_name_index,
        net_memberships=net_memberships,
        diagnostics=diagnostics,
    )
    net_class_rows = _build_net_class_rows(
        net_classes,
        net_name_index=net_name_index,
        nets=nets,
        net_memberships=net_memberships,
        diagnostics=diagnostics,
    )
    differential_pair_class_rows = _build_differential_pair_class_rows(
        differential_pair_classes,
        pairs=pairs,
        pair_rows=pair_rows,
        pair_name_index=pair_name_index,
        nets=nets,
        net_name_index=net_name_index,
        net_memberships=net_memberships,
        diagnostics=diagnostics,
    )
    rule_rows = _build_rule_rows(
        rules,
        diagnostics,
        net_classes=[item for _, item in net_classes],
        differential_pair_classes=[item for _, item in differential_pair_classes],
    )
    rule_counts = Counter(str(row["kind"]) for row in rule_rows)

    return {
        "schema": PCB_ROUTING_CONTEXT_SCHEMA,
        "source": source,
        "board": board,
        "evidence": {
            "authored_rules": "included",
            "class_membership": "stored_members_only",
            "rule_applicability": "not_evaluated_by_cruncher",
            "drc_run_by_cruncher": False,
            "drc_violations": "not_included",
        },
        "summary": {
            "net_count": len(nets),
            "net_class_count": len(net_classes),
            "differential_pair_count": len(pairs),
            "differential_pair_class_count": len(differential_pair_classes),
            "rule_count": len(rules),
            "enabled_rule_count": sum(
                getattr(rule, "enabled", None) is True for rule in rules
            ),
            "rules_by_kind": {
                kind: rule_counts[kind]
                for kind in sorted(rule_counts, key=str.casefold)
            },
        },
        "net_classes": net_class_rows,
        "differential_pairs": pair_rows,
        "differential_pair_classes": differential_pair_class_rows,
        "net_memberships": net_memberships,
        "rules": rule_rows,
        "diagnostics": diagnostics,
    }


def _class_kind(value: object) -> int | None:
    try:
        return int(getattr(value, "kind"))
    except AttributeError, TypeError, ValueError:
        return None


def _source_name(value: object) -> str:
    return str(getattr(value, "name", "") or "")


def _name_key(value: object) -> str:
    return str(value or "").strip().casefold()


def _unique_id(value: object) -> str | None:
    unique_id = str(getattr(value, "unique_id", "") or "")
    return unique_id or None


def _name_index(rows: Sequence[object]) -> dict[str, list[int]]:
    result: dict[str, list[int]] = {}
    for index, row in enumerate(rows):
        key = _name_key(_source_name(row))
        if key:
            result.setdefault(key, []).append(index)
    return result


def _append_duplicate_name_diagnostics(
    diagnostics: list[dict[str, object]],
    *,
    rows: Sequence[object],
    name_index: Mapping[str, list[int]],
    source_collection: str,
    code: str,
) -> None:
    for positions in name_index.values():
        if len(positions) < 2:
            continue
        name = _source_name(rows[positions[0]])
        diagnostics.append(
            _diagnostic(
                code,
                f"Name {name!r} occurs {len(positions)} times and cannot be joined uniquely",
                source_collection=source_collection,
                source_index=positions[0],
                identity=name,
            )
        )


def _join_pairs_to_nets(
    pairs: Sequence[object],
    *,
    net_name_index: Mapping[str, list[int]],
    net_memberships: list[dict[str, object]],
    diagnostics: list[dict[str, object]],
) -> None:
    for pair_index, pair in enumerate(pairs):
        pair_name = _source_name(pair)
        for attribute, polarity in (
            ("positive_net_name", "positive"),
            ("negative_net_name", "negative"),
        ):
            net_name = str(getattr(pair, attribute, "") or "")
            resolved = _resolve_unique_reference(
                net_name,
                net_name_index,
                diagnostics,
                source_collection="differential_pairs",
                source_index=pair_index,
                identity=pair_name,
                missing_code="missing_pair_net",
                ambiguous_code="ambiguous_pair_net",
                target_label="net",
            )
            if resolved is None:
                continue
            memberships = net_memberships[resolved]["differential_pairs"]
            assert isinstance(memberships, list)
            memberships.append({"name": pair_name, "polarity": polarity})


def _build_net_class_rows(
    classes: Sequence[tuple[int, object]],
    *,
    net_name_index: Mapping[str, list[int]],
    nets: Sequence[object],
    net_memberships: list[dict[str, object]],
    diagnostics: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for class_index, pcb_class in classes:
        class_name = _source_name(pcb_class)
        stored_members = [
            str(member or "") for member in getattr(pcb_class, "members", ()) or ()
        ]
        resolved_nets: list[str] = []
        unresolved_members: list[str] = []
        for member in stored_members:
            resolved = _resolve_unique_reference(
                member,
                net_name_index,
                diagnostics,
                source_collection="net_classes",
                source_index=class_index,
                identity=class_name,
                missing_code="missing_net_class_member",
                ambiguous_code="ambiguous_net_class_member",
                target_label="net",
            )
            if resolved is None:
                unresolved_members.append(member)
                continue
            resolved_nets.append(_source_name(nets[resolved]))
            memberships = net_memberships[resolved]["net_classes"]
            assert isinstance(memberships, list)
            memberships.append(class_name)
        rows.append(
            {
                "name": class_name,
                "unique_id": _unique_id(pcb_class),
                "enabled": bool(getattr(pcb_class, "enabled", True)),
                "stored_members": stored_members,
                "resolved_nets": resolved_nets,
                "unresolved_members": unresolved_members,
            }
        )
    return rows


def _build_differential_pair_class_rows(
    classes: Sequence[tuple[int, object]],
    *,
    pairs: Sequence[object],
    pair_rows: list[dict[str, object]],
    pair_name_index: Mapping[str, list[int]],
    nets: Sequence[object],
    net_name_index: Mapping[str, list[int]],
    net_memberships: list[dict[str, object]],
    diagnostics: list[dict[str, object]],
) -> list[dict[str, object]]:
    return [
        _build_differential_pair_class_row(
            class_index,
            pcb_class,
            pairs=pairs,
            pair_rows=pair_rows,
            pair_name_index=pair_name_index,
            nets=nets,
            net_name_index=net_name_index,
            net_memberships=net_memberships,
            diagnostics=diagnostics,
        )
        for class_index, pcb_class in classes
    ]


def _build_differential_pair_class_row(
    class_index: int,
    pcb_class: object,
    *,
    pairs: Sequence[object],
    pair_rows: list[dict[str, object]],
    pair_name_index: Mapping[str, list[int]],
    nets: Sequence[object],
    net_name_index: Mapping[str, list[int]],
    net_memberships: list[dict[str, object]],
    diagnostics: list[dict[str, object]],
) -> dict[str, object]:
    class_name = _source_name(pcb_class)
    stored_members = [
        str(member or "") for member in getattr(pcb_class, "members", ()) or ()
    ]
    resolved_pairs: list[str] = []
    resolved_nets: list[str] = []
    unresolved_members: list[str] = []
    for member in stored_members:
        pair_index = _resolve_pair_class_member(
            member,
            pair_name_index=pair_name_index,
            diagnostics=diagnostics,
            class_index=class_index,
            class_name=class_name,
        )
        if pair_index is None:
            unresolved_members.append(member)
            continue
        pair = pairs[pair_index]
        resolved_pairs.append(_source_name(pair))
        _append_class_membership(pair_rows[pair_index], class_name)
        _append_pair_net_class_memberships(
            pair,
            class_name=class_name,
            nets=nets,
            net_name_index=net_name_index,
            net_memberships=net_memberships,
            resolved_nets=resolved_nets,
        )
    return {
        "name": class_name,
        "unique_id": _unique_id(pcb_class),
        "enabled": bool(getattr(pcb_class, "enabled", True)),
        "stored_members": stored_members,
        "resolved_pairs": resolved_pairs,
        "resolved_nets": resolved_nets,
        "unresolved_members": unresolved_members,
    }


def _resolve_pair_class_member(
    member: str,
    *,
    pair_name_index: Mapping[str, list[int]],
    diagnostics: list[dict[str, object]],
    class_index: int,
    class_name: str,
) -> int | None:
    return _resolve_unique_reference(
        member,
        pair_name_index,
        diagnostics,
        source_collection="differential_pair_classes",
        source_index=class_index,
        identity=class_name,
        missing_code="missing_differential_pair_class_member",
        ambiguous_code="ambiguous_differential_pair_class_member",
        target_label="differential pair",
    )


def _append_class_membership(pair_row: dict[str, object], class_name: str) -> None:
    stored_classes = pair_row["stored_classes"]
    assert isinstance(stored_classes, list)
    stored_classes.append(class_name)


def _append_pair_net_class_memberships(
    pair: object,
    *,
    class_name: str,
    nets: Sequence[object],
    net_name_index: Mapping[str, list[int]],
    net_memberships: list[dict[str, object]],
    resolved_nets: list[str],
) -> None:
    for attribute in ("positive_net_name", "negative_net_name"):
        net_name = str(getattr(pair, attribute, "") or "")
        positions = net_name_index.get(_name_key(net_name), [])
        if len(positions) != 1:
            continue
        net_index = positions[0]
        canonical_name = _source_name(nets[net_index])
        if canonical_name not in resolved_nets:
            resolved_nets.append(canonical_name)
        memberships = net_memberships[net_index]["differential_pair_classes"]
        assert isinstance(memberships, list)
        if class_name not in memberships:
            memberships.append(class_name)


def _resolve_unique_reference(
    name: str,
    name_index: Mapping[str, list[int]],
    diagnostics: list[dict[str, object]],
    *,
    source_collection: str,
    source_index: int,
    identity: str,
    missing_code: str,
    ambiguous_code: str,
    target_label: str,
) -> int | None:
    positions = name_index.get(_name_key(name), [])
    if len(positions) == 1:
        return positions[0]
    if positions:
        code = ambiguous_code
        message = (
            f"Referenced {target_label} {name!r} resolves to {len(positions)} rows"
        )
    else:
        code = missing_code
        message = f"Referenced {target_label} {name!r} was not found"
    diagnostics.append(
        _diagnostic(
            code,
            message,
            source_collection=source_collection,
            source_index=source_index,
            identity=identity,
        )
    )
    return None


def _build_rule_rows(
    rules: Sequence[object],
    diagnostics: list[dict[str, object]],
    *,
    net_classes: Sequence[object],
    differential_pair_classes: Sequence[object],
) -> list[dict[str, object]]:
    net_class_name_index = _name_index(net_classes)
    differential_pair_class_name_index = _name_index(differential_pair_classes)
    indexed_rules = sorted(
        enumerate(rules),
        key=lambda item: (_rule_index(item[1], item[0]), item[0]),
    )
    return [
        _build_rule_row(
            rule,
            position=position,
            diagnostics=diagnostics,
            net_classes=net_classes,
            net_class_name_index=net_class_name_index,
            differential_pair_classes=differential_pair_classes,
            differential_pair_class_name_index=differential_pair_class_name_index,
        )
        for position, rule in indexed_rules
    ]


def _rule_index(rule: object, fallback: int) -> int:
    try:
        return int(getattr(rule, "index"))
    except AttributeError, TypeError, ValueError:
        return fallback


def _build_rule_row(
    rule: object,
    *,
    position: int,
    diagnostics: list[dict[str, object]],
    net_classes: Sequence[object],
    net_class_name_index: Mapping[str, list[int]],
    differential_pair_classes: Sequence[object],
    differential_pair_class_name_index: Mapping[str, list[int]],
) -> dict[str, object]:
    index = _rule_index(rule, position)
    name = str(getattr(rule, "name", "") or "")
    first_scope = str(getattr(rule, "scope1_expression", "") or "")
    second_scope = str(getattr(rule, "scope2_expression", "") or "")
    scope_references = _build_scope_reference_rows(
        (("first", first_scope), ("second", second_scope)),
        rule_name=name,
        rule_index=index,
        diagnostics=diagnostics,
        net_classes=net_classes,
        net_class_name_index=net_class_name_index,
        differential_pair_classes=differential_pair_classes,
        differential_pair_class_name_index=differential_pair_class_name_index,
    )
    constraints = _build_rule_constraints(rule, index=index, diagnostics=diagnostics)
    unmodeled_fields = _project_rule_mapping(
        getattr(rule, "extra_fields", {}) or {},
        rule=rule,
        index=index,
        diagnostics=diagnostics,
    )

    return {
        "index": index,
        "unique_id": _unique_id(rule),
        "name": name,
        "kind": str(getattr(rule, "rule_kind", "") or ""),
        "enabled": _nullable_bool(getattr(rule, "enabled", None)),
        "priority": _nullable_int(getattr(rule, "priority", None)),
        "comment": str(getattr(rule, "comment", "") or ""),
        "defined_by_logical_document": _nullable_bool(
            getattr(rule, "defined_by_logical_document", None)
        ),
        "scope": {
            "first": first_scope,
            "second": second_scope,
            "net_relation": str(getattr(rule, "net_scope", "") or ""),
            "layer_relation": str(getattr(rule, "layer_kind", "") or ""),
            "references": scope_references,
            "applicability": "not_evaluated_by_cruncher",
        },
        "constraints": constraints,
        "unmodeled_fields": unmodeled_fields,
    }


def _build_scope_reference_rows(
    expressions: Sequence[tuple[str, str]],
    *,
    rule_name: str,
    rule_index: int,
    diagnostics: list[dict[str, object]],
    net_classes: Sequence[object],
    net_class_name_index: Mapping[str, list[int]],
    differential_pair_classes: Sequence[object],
    differential_pair_class_name_index: Mapping[str, list[int]],
) -> list[dict[str, object]]:
    references: list[dict[str, object]] = []
    for expression_side, expression in expressions:
        for function, kind, name in _extract_scope_class_references(expression):
            if kind == "net_class":
                rows = net_classes
                name_index = net_class_name_index
            else:
                rows = differential_pair_classes
                name_index = differential_pair_class_name_index
            references.append(
                _resolve_scope_class_reference(
                    expression_side=expression_side,
                    function=function,
                    kind=kind,
                    name=name,
                    rows=rows,
                    name_index=name_index,
                    rule_name=rule_name,
                    rule_index=rule_index,
                    diagnostics=diagnostics,
                )
            )
    return references


def _resolve_scope_class_reference(
    *,
    expression_side: str,
    function: str,
    kind: str,
    name: str,
    rows: Sequence[object],
    name_index: Mapping[str, list[int]],
    rule_name: str,
    rule_index: int,
    diagnostics: list[dict[str, object]],
) -> dict[str, object]:
    positions = name_index.get(_name_key(name), [])
    resolution = _scope_reference_resolution(len(positions))
    matched = rows[positions[0]] if resolution == "resolved" else None
    reference = {
        "expression": expression_side,
        "function": function,
        "kind": kind,
        "name": name,
        "resolution": resolution,
        "matched_name": _source_name(matched) if matched is not None else None,
        "matched_unique_id": _unique_id(matched) if matched is not None else None,
    }
    if resolution != "resolved":
        _append_scope_reference_diagnostic(
            diagnostics,
            reference=reference,
            match_count=len(positions),
            rule_name=rule_name,
            rule_index=rule_index,
        )
    return reference


def _scope_reference_resolution(match_count: int) -> str:
    if match_count == 1:
        return "resolved"
    if match_count:
        return "ambiguous"
    return "missing"


def _append_scope_reference_diagnostic(
    diagnostics: list[dict[str, object]],
    *,
    reference: Mapping[str, object],
    match_count: int,
    rule_name: str,
    rule_index: int,
) -> None:
    resolution = str(reference["resolution"])
    expression = str(reference["expression"])
    function = str(reference["function"])
    name = str(reference["name"])
    if resolution == "ambiguous":
        code = "ambiguous_rule_scope_class_reference"
        outcome = f"matched {match_count} exported class rows"
    else:
        code = "missing_rule_scope_class_reference"
        outcome = "was not found in the exported class table"
    diagnostics.append(
        _diagnostic(
            code,
            f"{expression} scope reference {function}({name!r}) {outcome}",
            source_collection="rules",
            source_index=rule_index,
            identity=rule_name,
        )
    )


def _extract_scope_class_references(expression: str) -> list[tuple[str, str, str]]:
    references: list[tuple[str, str, str]] = []
    position = 0
    while position < len(expression):
        if expression[position] == "'":
            position = _skip_scope_string_literal(expression, position)
            continue
        if not _is_scope_identifier_start(expression[position]):
            position += 1
            continue
        identifier_end = _scope_identifier_end(expression, position)
        definition = _SCOPE_CLASS_REFERENCE_FUNCTIONS.get(
            expression[position:identifier_end].casefold()
        )
        if definition is None:
            position = identifier_end
            continue
        call = _parse_scope_literal_call(expression, identifier_end)
        if call is None:
            position = identifier_end
            continue
        name, position = call
        references.append((*definition, name))
    return references


def _is_scope_identifier_start(character: str) -> bool:
    return character.isalpha() or character == "_"


def _scope_identifier_end(expression: str, position: int) -> int:
    position += 1
    while position < len(expression):
        character = expression[position]
        if not (character.isalnum() or character == "_"):
            break
        position += 1
    return position


def _parse_scope_literal_call(
    expression: str,
    position: int,
) -> tuple[str, int] | None:
    position = _skip_scope_whitespace(expression, position)
    if position >= len(expression) or expression[position] != "(":
        return None
    position = _skip_scope_whitespace(expression, position + 1)
    literal = _read_scope_string_literal(expression, position)
    if literal is None:
        return None
    name, position = literal
    position = _skip_scope_whitespace(expression, position)
    if position >= len(expression) or expression[position] != ")":
        return None
    return name, position + 1


def _read_scope_string_literal(
    expression: str,
    position: int,
) -> tuple[str, int] | None:
    if position >= len(expression) or expression[position] != "'":
        return None
    characters: list[str] = []
    position += 1
    while position < len(expression):
        character = expression[position]
        if character != "'":
            characters.append(character)
            position += 1
            continue
        if position + 1 < len(expression) and expression[position + 1] == "'":
            characters.append("'")
            position += 2
            continue
        return "".join(characters), position + 1
    return None


def _skip_scope_string_literal(expression: str, position: int) -> int:
    literal = _read_scope_string_literal(expression, position)
    return literal[1] if literal is not None else len(expression)


def _skip_scope_whitespace(expression: str, position: int) -> int:
    while position < len(expression) and expression[position].isspace():
        position += 1
    return position


def _build_rule_constraints(
    rule: object,
    *,
    index: int,
    diagnostics: list[dict[str, object]],
) -> dict[str, object]:
    constraints = _project_typed_rule_fields(
        rule,
        index=index,
        diagnostics=diagnostics,
    )
    semantic_values = getattr(rule, "semantic_values", {}) or {}
    _extend_rule_mapping(
        constraints,
        semantic_values,
        rule=rule,
        index=index,
        diagnostics=diagnostics,
        preserve_existing=True,
    )
    return constraints


def _project_typed_rule_fields(
    rule: object,
    *,
    index: int,
    diagnostics: list[dict[str, object]],
) -> dict[str, object]:
    constraints: dict[str, object] = {}
    if not is_dataclass(rule):
        return constraints
    raw_record = getattr(rule, "raw_record", {}) or {}
    raw_keys = _raw_rule_keys(raw_record)
    field_specs = {
        str(getattr(spec, "attr_name", "")): str(getattr(spec, "raw_key", ""))
        .strip()
        .upper()
        for spec in getattr(rule, "RULE_FIELDS", ()) or ()
    }
    for field in fields(rule):
        if _skip_typed_rule_field(field.name):
            continue
        value = getattr(rule, field.name)
        if field_specs.get(field.name) not in raw_keys and not _has_semantic_value(
            value
        ):
            continue
        _project_rule_value(
            constraints,
            field.name,
            value,
            rule=rule,
            index=index,
            diagnostics=diagnostics,
        )
    return constraints


def _raw_rule_keys(raw_record: object) -> set[str]:
    if not isinstance(raw_record, Mapping):
        return set()
    return {str(key).strip().upper() for key in raw_record}


def _skip_typed_rule_field(field_name: str) -> bool:
    return field_name in _RULE_ENVELOPE_FIELDS or field_name.startswith("_")


def _project_rule_mapping(
    values: object,
    *,
    rule: object,
    index: int,
    diagnostics: list[dict[str, object]],
) -> dict[str, object]:
    projected: dict[str, object] = {}
    _extend_rule_mapping(
        projected,
        values,
        rule=rule,
        index=index,
        diagnostics=diagnostics,
    )
    return projected


def _extend_rule_mapping(
    target: dict[str, object],
    values: object,
    *,
    rule: object,
    index: int,
    diagnostics: list[dict[str, object]],
    preserve_existing: bool = False,
) -> None:
    if not isinstance(values, Mapping):
        return
    for key in sorted(values, key=lambda value: str(value).casefold()):
        name_key = str(key)
        if preserve_existing and name_key in target:
            continue
        _project_rule_value(
            target,
            name_key,
            values[key],
            rule=rule,
            index=index,
            diagnostics=diagnostics,
        )


def _project_rule_value(
    target: dict[str, object],
    key: str,
    value: object,
    *,
    rule: object,
    index: int,
    diagnostics: list[dict[str, object]],
) -> None:
    try:
        target[key] = _finite_json_value(value, seen=set())
    except (TypeError, ValueError) as exc:
        diagnostics.append(
            _diagnostic(
                "unrepresentable_rule_value",
                f"Rule field {key!r} was omitted: {exc}",
                source_collection="rules",
                source_index=index,
                identity=str(getattr(rule, "name", "") or ""),
            )
        )


def _finite_json_value(value: object, *, seen: set[int]) -> object:
    scalar = _finite_json_scalar(value)
    if scalar is not _NO_JSON_SCALAR:
        return scalar
    identity = id(value)
    if identity in seen:
        raise _UnsupportedJsonValue("cyclic values are not JSON evidence")
    seen.add(identity)
    try:
        return _finite_json_container(value, seen=seen)
    finally:
        seen.remove(identity)


def _finite_json_scalar(value: object) -> object:
    if value is None or isinstance(value, (str, bool)):
        return value
    if isinstance(value, Enum):
        return value.name
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("nonfinite numbers are not JSON evidence")
        return value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, bytes):
        raise _UnsupportedJsonValue("binary values are not compact semantic evidence")
    return _NO_JSON_SCALAR


def _finite_json_container(value: object, *, seen: set[int]) -> object:
    if isinstance(value, Mapping):
        return _finite_json_mapping(value, seen=seen)
    if is_dataclass(value):
        return _finite_json_dataclass(value, seen=seen)
    if isinstance(value, (list, tuple)):
        return [_finite_json_value(item, seen=seen) for item in value]
    if isinstance(value, (set, frozenset)):
        return _finite_json_set(value, seen=seen)
    raise _UnsupportedJsonValue(f"unsupported value type {type(value).__name__}")


def _finite_json_mapping(value: Mapping[object, object], *, seen: set[int]) -> object:
    result: dict[str, object] = {}
    for key in sorted(value, key=lambda item: str(item).casefold()):
        if not isinstance(key, str):
            raise _UnsupportedJsonValue("JSON object keys must be strings")
        result[key] = _finite_json_value(value[key], seen=seen)
    return result


def _finite_json_dataclass(value: object, *, seen: set[int]) -> object:
    return {
        field.name: _finite_json_value(getattr(value, field.name), seen=seen)
        # This helper is reached only after the runtime ``is_dataclass`` guard.
        for field in fields(value)  # pyright: ignore[reportArgumentType]
        if not field.name.startswith("_")
    }


def _finite_json_set(
    value: set[object] | frozenset[object], *, seen: set[int]
) -> object:
    projected = [_finite_json_value(item, seen=seen) for item in value]
    return sorted(
        projected,
        key=lambda item: json.dumps(item, sort_keys=True, ensure_ascii=False),
    )


def _has_semantic_value(value: object) -> bool:
    if value is None or value == "":
        return False
    if isinstance(value, (Mapping, Sequence, set, frozenset)) and not value:
        return False
    return True


def _nullable_bool(value: object) -> bool | None:
    if value is None:
        return None
    return bool(value)


def _nullable_int(value: object) -> int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if not isinstance(value, str):
        return None
    try:
        return int(value)
    except TypeError, ValueError:
        return None


def _diagnostic(
    code: str,
    message: str,
    *,
    source_collection: str,
    source_index: int | None = None,
    identity: str = "",
) -> dict[str, object]:
    row: dict[str, object] = {
        "code": code,
        "severity": "warning",
        "message": message,
        "source_collection": source_collection,
    }
    if source_index is not None:
        row["source_index"] = source_index
    if identity:
        row["identity"] = identity
    return row
