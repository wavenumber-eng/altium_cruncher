"""Project variant helpers for Altium PrjPcb files."""

from __future__ import annotations

import re
import uuid
import configparser
from collections.abc import Mapping
from pathlib import Path
from typing import TypedDict

VARIANTS_LIST_SCHEMA = "altium_cruncher.variants.list.a0"

_VARIANT_PREFIX = "ProjectVariant"
_VARIATION_RE = re.compile(r"^Variation(?P<index>\d+)$", re.IGNORECASE)


class ComponentIndexEntry(TypedDict):
    sheet: str
    unique_id: str
    library_ref: str
    value: str
    description: str
    parameters: dict[str, str]


def summarize_project_variants(project_file: Path) -> dict[str, object]:
    """Return project variant rows with schematic sheet hints when available."""
    from altium_monkey.altium_prjpcb import AltiumPrjPcb

    resolved_project = Path(project_file).resolve()
    project = AltiumPrjPcb(resolved_project)
    component_index, index_errors = _schematic_component_index(resolved_project)
    current_variant = project.get_current_variant()
    project_parameters = dict(project.parameters)

    variants: list[dict[str, object]] = []
    all_rows: list[dict[str, object]] = []
    for variant_name, variant_data in project.variants.items():
        if not isinstance(variant_data, dict):
            continue
        variant_rows = _variant_detail_rows(
            str(variant_name),
            variant_data,
            component_index,
            project_parameters,
        )
        variants.append(
            {
                "name": str(variant_name),
                "unique_id": str(variant_data.get("unique_id", "") or ""),
                "allow_fabrication": bool(variant_data.get("allow_fabrication")),
                "current": _same_name(str(variant_name), current_variant),
                "dnp": _sorted_designators(
                    [str(item) for item in variant_data.get("DNP", []) or []]
                ),
                "variation_count": int(variant_data.get("variation_count", 0) or 0),
                "parameter_count": int(variant_data.get("parameter_count", 0) or 0),
                "param_variation_count": int(
                    variant_data.get("param_variation_count", 0) or 0
                ),
                "rows": variant_rows,
            }
        )
        all_rows.extend(variant_rows)

    return {
        "schema": VARIANTS_LIST_SCHEMA,
        "project": str(resolved_project),
        "current_variant": current_variant,
        "variant_count": len(variants),
        "variants": variants,
        "rows": sorted(all_rows, key=_variant_row_sort_key),
        "index_errors": index_errors,
    }


def delete_project_variant(project: object, name: str) -> dict[str, object]:
    """Delete one variant section by description/name."""
    section = _require_variant_section(project, name)
    config = _project_config(project)
    config.remove_section(section)
    current = _project_current_variant(project)
    if _same_name(name, current):
        project.set_current_variant(None)
    return {"name": _clean_name(name), "section": section}


def rename_project_variant(
    project: object,
    name: str,
    new_name: str,
) -> dict[str, object]:
    """Rename one project variant by updating its Description field."""
    section = _require_variant_section(project, name)
    clean_new_name = _clean_variant_name(new_name)
    _require_variant_absent(project, clean_new_name)
    config = _project_config(project)
    old_name = config.get(section, "Description", fallback=_clean_name(name))
    config.set(section, "Description", clean_new_name)
    current = _project_current_variant(project)
    if _same_name(old_name, current):
        project.set_current_variant(clean_new_name)
    return {"name": old_name, "new_name": clean_new_name, "section": section}


def clone_project_variant(
    project: object,
    source_name: str,
    name: str,
    *,
    unique_id: str | None = None,
    allow_fabrication: bool | None = None,
    current: bool = False,
) -> dict[str, object]:
    """Clone an existing variant section under a new Description."""
    source_section = _require_variant_section(project, source_name)
    clean_name = _clean_variant_name(name)
    _require_variant_absent(project, clean_name)
    config = _project_config(project)
    section = _next_numbered_section_name(config, _VARIANT_PREFIX)
    config.add_section(section)
    for key, value in config.items(source_section):
        config.set(section, key, value)
    resolved_unique_id = unique_id or str(uuid.uuid4()).upper()
    config.set(section, "UniqueId", resolved_unique_id)
    config.set(section, "Description", clean_name)
    if allow_fabrication is not None:
        config.set(section, "AllowFabrication", "1" if allow_fabrication else "0")
    _ensure_variant_count_fields(config, section)
    if current:
        project.set_current_variant(clean_name)
    return {
        "source_name": _clean_name(source_name),
        "name": clean_name,
        "unique_id": resolved_unique_id,
        "section": section,
    }


def add_project_variant_dnp(
    project: object,
    project_file: Path,
    *,
    variant: str,
    designator: str,
    unique_id: str | None = None,
    alternate_part: str = "",
) -> dict[str, object]:
    """Add or update a Not Fitted variation row for one designator."""
    section = _require_variant_section(project, variant)
    clean_designator = _clean_designator(designator)
    resolved_unique_id = _resolve_variation_unique_id(
        project_file,
        clean_designator,
        unique_id,
    )
    config = _project_config(project)
    existing_index, existing_row = _find_variation_by_designator(
        config,
        section,
        clean_designator,
    )
    row = {
        **(existing_row or {}),
        "Designator": clean_designator,
        "UniqueId": resolved_unique_id,
        "Kind": "1",
        "AlternatePart": alternate_part,
    }
    if existing_index is None:
        variation_index = _next_variation_index(config, section)
    else:
        variation_index = existing_index
    config.set(section, f"Variation{variation_index}", _format_variant_key_values(row))
    _set_variation_count(config, section, variation_index)
    _ensure_variant_count_fields(config, section)
    return {
        "variant": _clean_name(variant),
        "designator": clean_designator,
        "unique_id": resolved_unique_id,
        "variation": f"Variation{variation_index}",
    }


def toggle_project_variant_dnp(
    project: object,
    project_file: Path,
    *,
    variant: str,
    designator: str,
    unique_id: str | None = None,
    alternate_part: str = "",
) -> dict[str, object]:
    """Toggle one designator between fitted and Not Fitted in a variant."""
    section = _require_variant_section(project, variant)
    clean_designator = _clean_designator(designator)
    config = _project_config(project)
    existing_index, existing_row = _find_variation_by_designator(
        config,
        section,
        clean_designator,
    )
    if existing_index is not None and (existing_row or {}).get("Kind") == "1":
        _remove_variation(config, section, existing_index)
        return {
            "variant": _clean_name(variant),
            "designator": clean_designator,
            "action": "removed",
            "dnp": False,
        }

    added = add_project_variant_dnp(
        project,
        project_file,
        variant=variant,
        designator=clean_designator,
        unique_id=unique_id,
        alternate_part=alternate_part,
    )
    return {**added, "action": "added", "dnp": True}


def _variant_detail_rows(
    variant_name: str,
    variant_data: Mapping[object, object],
    component_index: dict[str, ComponentIndexEntry],
    project_parameters: dict[str, str],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    rows.extend(
        _variation_detail_rows(
            variant_name,
            _mapping_rows(variant_data.get("variations")),
            component_index,
            project_parameters,
        )
    )
    rows.extend(
        _param_variation_detail_rows(
            variant_name,
            _mapping_rows(variant_data.get("param_variations")),
            component_index,
            project_parameters,
        )
    )
    rows.extend(
        _variant_parameter_detail_rows(
            variant_name,
            _mapping_rows(variant_data.get("parameters")),
        )
    )
    return sorted(rows, key=_variant_row_sort_key)


def _variation_detail_rows(
    variant_name: str,
    variations: list[Mapping[object, object]],
    component_index: dict[str, ComponentIndexEntry],
    project_parameters: dict[str, str],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for variation in variations:
        designator = _mapping_text(variation, "Designator")
        if not designator:
            continue
        component = _component_index_lookup(component_index, designator)
        operation, detail, alternate_part, resolved_alternate_part = (
            _variation_operation_detail(
                variation,
                component,
                project_parameters,
                variant_name,
            )
        )
        row = _variant_row_from_component(
            variant_name,
            designator,
            operation,
            detail,
            component,
            component_value=_component_display_value(component, project_parameters, variant_name),
            unique_id=_mapping_text(variation, "UniqueId"),
        )
        if alternate_part:
            row["alternate_part"] = alternate_part
            row["alternate_part_resolved"] = resolved_alternate_part
        rows.append(row)
    return rows


def _param_variation_detail_rows(
    variant_name: str,
    param_variations: list[Mapping[object, object]],
    component_index: dict[str, ComponentIndexEntry],
    project_parameters: dict[str, str],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for param_variation in param_variations:
        designator = _first_mapping_text(
            param_variation,
            ("ParamDesignator", "Designator"),
        )
        parameter_name = _mapping_text(param_variation, "ParameterName")
        raw_value = _mapping_text(param_variation, "VariantValue")
        if not designator and not parameter_name:
            continue
        component = _component_index_lookup(component_index, designator)
        resolved_value = _resolve_variant_expression(
            raw_value,
            component,
            project_parameters,
            variant_name,
        )
        row = _variant_row_from_component(
            variant_name,
            designator or "(unknown)",
            "parameter",
            f"{parameter_name or '?'}={_resolved_value_detail(raw_value, resolved_value)}",
            component,
            component_value=_component_display_value(component, project_parameters, variant_name),
            parameter_name=parameter_name,
            value=resolved_value,
        )
        row["raw_value"] = raw_value
        row["resolved_value"] = resolved_value
        rows.append(row)
    return rows


def _variant_parameter_detail_rows(
    variant_name: str,
    parameters: list[Mapping[object, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for parameter in parameters:
        name = _first_mapping_text(parameter, ("Name", "ParameterName"))
        value = _first_mapping_text(parameter, ("Value", "VariantValue"))
        if not name:
            continue
        rows.append(
            {
                "variant": variant_name,
                "sheet": "(variant)",
                "designator": "",
                "operation": "variant_parameter",
                "detail": f"{name}={value}",
                "parameter_name": name,
                "value": value,
                "unique_id": "",
            }
        )
    return rows


def _variation_operation_detail(
    variation: Mapping[object, object],
    component: ComponentIndexEntry,
    project_parameters: dict[str, str],
    variant_name: str,
) -> tuple[str, str, str, str]:
    kind = _mapping_text(variation, "Kind")
    alternate_part = _mapping_text(variation, "AlternatePart")
    resolved_alternate_part = _resolve_variant_expression(
        alternate_part,
        component,
        project_parameters,
        variant_name,
    )
    operation = "DNP" if kind == "1" else "variation"
    detail = "not fitted" if operation == "DNP" else f"kind={kind or '?'}"
    if alternate_part:
        detail = (
            f"{detail}; alternate_part="
            f"{_resolved_value_detail(alternate_part, resolved_alternate_part)}"
        )
    return operation, detail, alternate_part, resolved_alternate_part


def _mapping_rows(value: object) -> list[Mapping[object, object]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, Mapping)]


def _mapping_text(row: Mapping[object, object], key: str) -> str:
    return str(row.get(key, "") or "").strip()


def _first_mapping_text(
    row: Mapping[object, object],
    keys: tuple[str, ...],
) -> str:
    for key in keys:
        value = _mapping_text(row, key)
        if value:
            return value
    return ""


def _resolve_variant_expression(
    raw_value: str,
    component: ComponentIndexEntry,
    project_parameters: dict[str, str],
    variant_name: str,
) -> str:
    value = str(raw_value or "")
    if not value.startswith("="):
        return value

    expression = value[1:].strip()
    if not expression:
        return value

    parameters = dict(project_parameters)
    parameters["VariantName"] = variant_name
    parameters.update(component.get("parameters", {}))
    base_value = component.get("value", "")
    if base_value:
        parameters.setdefault("Value", base_value)

    if "+" not in expression and "'" not in expression:
        resolved = _lookup_case_insensitive(parameters, expression)
        return resolved if resolved is not None else value

    try:
        from altium_monkey.altium_netlist_common import _evaluate_altium_expression

        return _evaluate_altium_expression(expression, parameters)
    except Exception:  # pragma: no cover - expression fallback only
        return value


def _component_display_value(
    component: ComponentIndexEntry,
    project_parameters: dict[str, str],
    variant_name: str,
) -> str:
    parameters = component.get("parameters", {})
    comment = _lookup_case_insensitive(parameters, "Comment") or ""
    if comment:
        resolved_comment = _resolve_variant_expression(
            comment,
            component,
            project_parameters,
            variant_name,
        )
        if resolved_comment and resolved_comment != comment:
            return resolved_comment
        if not comment.startswith("="):
            return comment
    return _lookup_case_insensitive(parameters, "Value") or component.get("value", "")


def _resolved_value_detail(raw_value: str, resolved_value: str) -> str:
    if not raw_value.startswith("="):
        return raw_value
    if resolved_value == raw_value:
        return f"{raw_value} (unresolved)"
    if resolved_value:
        return f"{resolved_value} (from {raw_value})"
    return f"(empty, from {raw_value})"


def _lookup_case_insensitive(values: Mapping[str, str], name: str) -> str | None:
    name_lower = name.lower()
    for key, value in values.items():
        if key.lower() == name_lower:
            return value
    return None


def _variant_row_from_component(
    variant_name: str,
    designator: str,
    operation: str,
    detail: str,
    component: ComponentIndexEntry,
    *,
    unique_id: str = "",
    parameter_name: str = "",
    value: str = "",
    component_value: str = "",
) -> dict[str, object]:
    return {
        "variant": variant_name,
        "sheet": component.get("sheet", "(unknown sheet)"),
        "designator": designator,
        "operation": operation,
        "detail": detail,
        "component_value": component_value,
        "parameter_name": parameter_name,
        "value": value,
        "unique_id": unique_id or component.get("unique_id", ""),
    }


def _schematic_component_index(
    project_file: Path,
) -> tuple[dict[str, ComponentIndexEntry], list[str]]:
    from altium_monkey.altium_prjpcb import AltiumPrjPcb

    project = AltiumPrjPcb(project_file)
    result: dict[str, ComponentIndexEntry] = {}
    errors: list[str] = []
    schdoc_paths = project.get_reachable_schdoc_paths()
    for schdoc_path in schdoc_paths:
        errors.extend(_add_schematic_components_to_index(schdoc_path, result))
    if schdoc_paths:
        errors.extend(_add_compiled_component_index(project_file, result))
    return result, errors


def _add_schematic_components_to_index(
    schdoc_path: Path,
    result: dict[str, ComponentIndexEntry],
) -> list[str]:
    from altium_monkey import AltiumSchDoc

    try:
        schdoc = AltiumSchDoc(schdoc_path)
    except Exception as exc:  # pragma: no cover - defensive for damaged assets
        return [f"{schdoc_path.name}: {exc}"]
    for component in getattr(schdoc, "components", []) or []:
        designator = _schematic_component_designator(component)
        if designator:
            result[designator.upper()] = _schematic_component_index_entry(
                component,
                schdoc_path.name,
            )
    return []


def _schematic_component_index_entry(
    component: object,
    sheet_name: str,
) -> ComponentIndexEntry:
    unique_id = str(getattr(component, "unique_id", "") or "").strip()
    parameters = _schematic_component_parameters(component)
    return {
        "sheet": sheet_name,
        "unique_id": _normalize_variation_unique_id(unique_id) if unique_id else "",
        "library_ref": str(getattr(component, "lib_reference", "") or ""),
        "value": _lookup_case_insensitive(parameters, "Value") or "",
        "description": _lookup_case_insensitive(parameters, "Description") or "",
        "parameters": parameters,
    }


def _schematic_component_designator(component: object) -> str:
    from altium_monkey.altium_record_sch__designator import AltiumSchDesignator

    for parameter in getattr(component, "parameters", []) or []:
        if isinstance(parameter, AltiumSchDesignator):
            return str(getattr(parameter, "text", "") or "").strip()
    return str(getattr(component, "designator", "") or "").strip()


def _schematic_component_parameters(component: object) -> dict[str, str]:
    from altium_monkey.altium_record_sch__parameter import AltiumSchParameter

    result: dict[str, str] = {}
    for parameter in getattr(component, "parameters", []) or []:
        if not isinstance(parameter, AltiumSchParameter):
            continue
        name = str(getattr(parameter, "name", "") or "").strip()
        if name:
            result[name] = str(getattr(parameter, "text", "") or "")
    return result


def _add_compiled_component_index(
    project_file: Path,
    component_index: dict[str, ComponentIndexEntry],
) -> list[str]:
    netlist, error = _compiled_netlist(project_file)
    if error:
        return [error]
    for component in getattr(netlist, "components", []) or []:
        designator = str(getattr(component, "designator", "") or "").strip()
        if not designator:
            continue
        base = _component_index_lookup(component_index, designator)
        component_index[designator.upper()] = _compiled_component_index_entry(
            component,
            base,
        )
    return []


def _compiled_netlist(project_file: Path) -> tuple[object | None, str]:
    from altium_monkey import AltiumDesign

    try:
        design = AltiumDesign.from_prjpcb(project_file)
        return design.to_netlist(), ""
    except Exception as exc:  # pragma: no cover - defensive for damaged assets
        return None, f"compiled component index: {exc}"


def _compiled_component_index_entry(
    component: object,
    base: ComponentIndexEntry,
) -> ComponentIndexEntry:
    parameters = _compiled_component_parameters(component)
    return {
        "sheet": base.get("sheet", ""),
        "unique_id": base.get("unique_id", ""),
        "library_ref": _compiled_component_library_ref(component, base),
        "value": _compiled_component_value(component, parameters, base),
        "description": _compiled_component_description(component, base),
        "parameters": parameters or dict(base.get("parameters", {})),
    }


def _compiled_component_parameters(component: object) -> dict[str, str]:
    raw_parameters = getattr(component, "parameters", {}) or {}
    return {str(name): str(value) for name, value in dict(raw_parameters).items()}


def _compiled_component_library_ref(
    component: object,
    base: ComponentIndexEntry,
) -> str:
    return str(getattr(component, "library_ref", "") or "") or base.get(
        "library_ref",
        "",
    )


def _compiled_component_value(
    component: object,
    parameters: dict[str, str],
    base: ComponentIndexEntry,
) -> str:
    return (
        str(getattr(component, "value", "") or "")
        or _lookup_case_insensitive(parameters, "Value")
        or base.get("value", "")
    )


def _compiled_component_description(
    component: object,
    base: ComponentIndexEntry,
) -> str:
    return str(getattr(component, "description", "") or "") or base.get(
        "description",
        "",
    )


def _component_index_lookup(
    component_index: dict[str, ComponentIndexEntry],
    designator: str,
) -> ComponentIndexEntry:
    exact = component_index.get(designator.upper())
    if exact is not None:
        return exact
    base = _channel_base_designator(designator)
    if base:
        base_match = component_index.get(base.upper())
        if base_match is not None:
            return base_match
    return _empty_component_index_entry()


def _empty_component_index_entry() -> ComponentIndexEntry:
    return {
        "sheet": "(unknown sheet)",
        "unique_id": "",
        "library_ref": "",
        "value": "",
        "description": "",
        "parameters": {},
    }


def _channel_base_designator(designator: str) -> str | None:
    if "_" not in designator:
        return None
    base, suffix = designator.rsplit("_", 1)
    if base and suffix:
        return base
    return None


def _resolve_variation_unique_id(
    project_file: Path,
    designator: str,
    unique_id: str | None,
) -> str:
    if unique_id is not None:
        return _normalize_variation_unique_id(unique_id)
    component_index, _errors = _schematic_component_index(Path(project_file).resolve())
    component = component_index.get(designator.upper())
    if component and component.get("unique_id"):
        return component["unique_id"]
    raise ValueError(
        "Could not infer variant UniqueId for designator "
        f"{designator!r}; pass unique_id/--unique-id explicitly."
    )


def _project_config(project: object) -> configparser.ConfigParser:
    config = getattr(project, "config", None)
    if config is None:
        raise ValueError("project object has no config")
    return config


def _project_current_variant(project: object) -> str | None:
    getter = getattr(project, "get_current_variant", None)
    if callable(getter):
        return getter()
    return None


def _variant_sections(project: object) -> list[str]:
    config = _project_config(project)
    sections = []
    for section in config.sections():
        index = _numbered_section_index(section, _VARIANT_PREFIX)
        if index is not None:
            sections.append((index, section))
    return [section for _index, section in sorted(sections)]


def _require_variant_section(project: object, name: str) -> str:
    section = _variant_section_by_name(project, name)
    if section is None:
        raise ValueError(f"Project variant not found: {_clean_name(name)}")
    return section


def _variant_section_by_name(project: object, name: str) -> str | None:
    clean_name = _clean_variant_name(name)
    config = _project_config(project)
    for section in _variant_sections(project):
        existing_name = config.get(section, "Description", fallback="")
        if existing_name.lower() == clean_name.lower():
            return section
    return None


def _require_variant_absent(project: object, name: str) -> None:
    if _variant_section_by_name(project, name) is not None:
        raise ValueError(f"Project variant already exists: {_clean_name(name)}")


def _ensure_variant_count_fields(
    config: configparser.ConfigParser,
    section: str,
) -> None:
    for option in ("ParameterCount", "VariationCount", "ParamVariationCount"):
        if not config.has_option(section, option):
            config.set(section, option, "0")


def _find_variation_by_designator(
    config: configparser.ConfigParser,
    section: str,
    designator: str,
) -> tuple[int | None, dict[str, str] | None]:
    for index in _variation_indices(config, section):
        value = config.get(section, f"Variation{index}", fallback="")
        row = _parse_variant_key_values(value)
        if row.get("Designator", "").lower() == designator.lower():
            return index, row
    return None, None


def _variation_indices(
    config: configparser.ConfigParser,
    section: str,
) -> list[int]:
    indices: list[int] = []
    for key, _value in config.items(section):
        match = _VARIATION_RE.match(str(key))
        if match is not None:
            indices.append(int(match.group("index")))
    return sorted(indices)


def _next_variation_index(
    config: configparser.ConfigParser,
    section: str,
) -> int:
    indices = _variation_indices(config, section)
    count = config.getint(section, "VariationCount", fallback=0)
    return max([count, *indices], default=0) + 1


def _set_variation_count(
    config: configparser.ConfigParser,
    section: str,
    variation_index: int,
) -> None:
    existing_count = config.getint(section, "VariationCount", fallback=0)
    config.set(section, "VariationCount", str(max(existing_count, variation_index)))


def _remove_variation(
    config: configparser.ConfigParser,
    section: str,
    remove_index: int,
) -> None:
    kept_values = [
        config.get(section, f"Variation{index}", fallback="")
        for index in _variation_indices(config, section)
        if index != remove_index
    ]
    for index in _variation_indices(config, section):
        config.remove_option(section, f"Variation{index}")
    for new_index, value in enumerate(kept_values, start=1):
        config.set(section, f"Variation{new_index}", value)
    config.set(section, "VariationCount", str(len(kept_values)))
    _ensure_variant_count_fields(config, section)


def _parse_variant_key_values(value: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for pair in str(value or "").split("|"):
        if "=" not in pair:
            continue
        key, parsed_value = pair.split("=", 1)
        result[key] = parsed_value
    return result


def _format_variant_key_values(row: dict[str, str]) -> str:
    preferred = ("Designator", "UniqueId", "Kind", "AlternatePart")
    ordered: list[tuple[str, str]] = []
    for key in preferred:
        if key in row:
            ordered.append((key, row[key]))
    for key, value in row.items():
        if key not in preferred:
            ordered.append((key, value))
    return "|".join(f"{key}={value}" for key, value in ordered)


def _normalize_variation_unique_id(unique_id: str) -> str:
    clean = str(unique_id or "").strip()
    if not clean:
        raise ValueError("variant variation unique_id must not be blank")
    if clean.startswith("\\"):
        return clean
    return f"\\{clean}"


def _numbered_section_index(section: str, prefix: str) -> int | None:
    match = re.fullmatch(rf"{re.escape(prefix)}(\d+)", section)
    if match is None:
        return None
    return int(match.group(1))


def _next_numbered_section_name(
    config: configparser.ConfigParser,
    prefix: str,
) -> str:
    highest_index = 0
    for section in config.sections():
        index = _numbered_section_index(section, prefix)
        if index is not None:
            highest_index = max(highest_index, index)
    return f"{prefix}{highest_index + 1}"


def _clean_variant_name(name: str) -> str:
    clean = _clean_name(name)
    if not clean:
        raise ValueError("variant name must not be blank")
    return clean


def _clean_designator(designator: str) -> str:
    clean = _clean_name(designator)
    if not clean:
        raise ValueError("designator must not be blank")
    return clean


def _clean_name(name: str | None) -> str:
    return str(name or "").strip()


def _same_name(left: str | None, right: str | None) -> bool:
    if left is None or right is None:
        return False
    return left.strip().lower() == right.strip().lower()


def _variant_row_sort_key(row: dict[str, object]) -> tuple[str, tuple, str, str]:
    return (
        str(row.get("sheet", "") or ""),
        _designator_sort_key(str(row.get("designator", "") or "")),
        str(row.get("variant", "") or "").lower(),
        str(row.get("operation", "") or "").lower(),
    )


def _sorted_designators(values: list[str]) -> list[str]:
    return sorted(values, key=_designator_sort_key)


def _designator_sort_key(value: str) -> tuple:
    from altium_cruncher.bom_pnp_model import designator_sort_key

    return designator_sort_key(value)
