"""Shared BOM and pick-and-place normalization helpers."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
import re

BOM_RAW_SCHEMA = "wn.altium_cruncher.bom.raw.v1"
BOM_GROUPED_SCHEMA = "wn.altium_cruncher.bom.grouped.v1"
PNP_SCHEMA = "wn.altium_cruncher.pnp.v1"
JLC_BOM_COLUMNS: tuple[str, ...] = (
    "Comment",
    "Designator",
    "Footprint",
    "JLCPCB Part #",
)
JLC_CPL_COLUMNS: tuple[str, ...] = (
    "Designator",
    "Layer",
    "Mid X",
    "Mid Y",
    "Rotation",
)

_DESIGNATOR_TOKEN_RE = re.compile(r"\d+|[A-Za-z]+|[^A-Za-z\d]+")
_LEADING_PREFIX_RE = re.compile(r"^[A-Za-z]+")


def _default_aliases() -> dict[str, tuple[str, ...]]:
    """Return the default canonical field alias mapping."""
    return {
        "manufacturer": (
            "Manufacturer",
            "Mfr",
            "MFG",
            "Manufacturer Name",
            "Mfr Name",
        ),
        "manufacturer_part_number": (
            "Manufacturer Part Number",
            "MPN",
            "Mfr Part Number",
            "Mfr PN",
            "MFG PN",
            "Part Number",
        ),
        "jlcpcb_part_number": (
            "JLCPCB Part #",
            "JLCPCB Part Number",
            "JLC Part #",
            "JLC Part Number",
            "LCSC Part #",
            "LCSC Part Number",
            "LCSC",
        ),
        "value": (
            "Value",
            "Comment",
        ),
        "description": (
            "Description",
            "Desc",
        ),
        "footprint": (
            "Footprint",
            "Pattern",
            "Package",
        ),
    }


@dataclass(frozen=True, slots=True)
class FieldAliasConfig:
    """Canonical parameter aliases used by BOM and PnP normalization."""

    canonical_fields: dict[str, tuple[str, ...]] = field(
        default_factory=_default_aliases
    )

    @classmethod
    def from_mapping(
        cls,
        mapping: Mapping[str, Sequence[str]],
    ) -> "FieldAliasConfig":
        """Build an alias config from JSON-style mappings."""
        return cls(
            {
                _normalize_name(name): tuple(
                    alias.strip() for alias in aliases if alias.strip()
                )
                for name, aliases in mapping.items()
            }
        )

    def aliases_for(self, canonical_name: str) -> tuple[str, ...]:
        """Return aliases for a canonical field, including the canonical name."""
        normalized = _normalize_name(canonical_name)
        aliases = self.canonical_fields.get(normalized, ())
        return (normalized, canonical_name, *aliases)

    def to_json_obj(self) -> dict[str, list[str]]:
        """Return a deterministic JSON-compatible alias mapping."""
        return {
            name: list(aliases)
            for name, aliases in sorted(self.canonical_fields.items())
        }


@dataclass(frozen=True, slots=True)
class NormalizedBomComponent:
    """BOM component with canonical fields and field-source traceability."""

    designator: str
    value: str
    footprint: str
    library_ref: str
    description: str
    sheet: str
    dnp: bool
    parameters: dict[str, str] = field(default_factory=dict)
    canonical_fields: dict[str, str] = field(default_factory=dict)
    field_sources: dict[str, str] = field(default_factory=dict)

    def to_json_obj(self) -> dict[str, object]:
        """Return a JSON-compatible representation of the normalized component."""
        return {
            "designator": self.designator,
            "value": self.value,
            "footprint": self.footprint,
            "library_ref": self.library_ref,
            "description": self.description,
            "sheet": self.sheet,
            "dnp": self.dnp,
            "parameters": dict(sorted(self.parameters.items())),
            "canonical_fields": dict(sorted(self.canonical_fields.items())),
            "field_sources": dict(sorted(self.field_sources.items())),
        }


@dataclass(frozen=True, slots=True)
class GroupedBomLine:
    """Grouped BOM line item derived from normalized BOM components."""

    item: int
    quantity: int
    designators: tuple[str, ...]
    dnp: bool
    fields: dict[str, str] = field(default_factory=dict)

    def to_json_obj(self) -> dict[str, object]:
        """Return a JSON-compatible grouped line item."""
        return {
            "item": self.item,
            "quantity": self.quantity,
            "designators": list(self.designators),
            "dnp": self.dnp,
            "fields": dict(sorted(self.fields.items())),
        }


@dataclass(frozen=True, slots=True)
class NormalizedPlacement:
    """Pick-and-place placement with canonical fields and output units."""

    designator: str
    comment: str
    layer: str
    footprint: str
    center_x: float
    center_y: float
    rotation: float
    units: str
    description: str = ""
    parameters: dict[str, str] = field(default_factory=dict)
    canonical_fields: dict[str, str] = field(default_factory=dict)
    field_sources: dict[str, str] = field(default_factory=dict)

    def to_json_obj(self) -> dict[str, object]:
        """Return a JSON-compatible placement record."""
        return {
            "designator": self.designator,
            "comment": self.comment,
            "layer": self.layer,
            "footprint": self.footprint,
            "center_x": self.center_x,
            "center_y": self.center_y,
            "rotation": self.rotation,
            "units": self.units,
            "description": self.description,
            "parameters": dict(sorted(self.parameters.items())),
            "canonical_fields": dict(sorted(self.canonical_fields.items())),
            "field_sources": dict(sorted(self.field_sources.items())),
        }


def normalize_bom_components(
    bom: Sequence[Mapping[str, object]],
    aliases: FieldAliasConfig | None = None,
) -> list[NormalizedBomComponent]:
    """Normalize raw Altium Monkey BOM dicts into canonical records."""
    alias_config = aliases or FieldAliasConfig()
    return [
        _normalize_bom_component(component, alias_config)
        for component in bom
    ]


def normalize_pnp_entries(
    entries: Sequence[object],
    *,
    units: str,
    aliases: FieldAliasConfig | None = None,
) -> list[NormalizedPlacement]:
    """Normalize Altium Monkey PnP entries into canonical placement records."""
    alias_config = aliases or FieldAliasConfig()
    return [
        _normalize_pnp_entry(entry, units=units, aliases=alias_config)
        for entry in entries
    ]


def sort_designators(
    designators: Sequence[str],
    *,
    prefix_order: Sequence[str] = (),
) -> list[str]:
    """Sort designators naturally, optionally honoring a prefix priority list."""
    return sorted(
        designators,
        key=lambda designator: designator_sort_key(
            designator,
            prefix_order=prefix_order,
        ),
    )


def designator_sort_key(
    designator: str,
    *,
    prefix_order: Sequence[str] = (),
) -> tuple[int, tuple[tuple[int, int | str], ...]]:
    """Return a stable natural-sort key for one designator."""
    prefix_rank = _prefix_rank(designator, prefix_order)
    return (prefix_rank, _tokenize_designator(designator))


def sort_placements(
    placements: Sequence[NormalizedPlacement],
    *,
    layer_order: Sequence[str] = ("top", "bottom"),
    prefix_order: Sequence[str] = (),
) -> list[NormalizedPlacement]:
    """Sort placements by layer and natural designator order."""
    return sorted(
        placements,
        key=lambda placement: (
            _layer_rank(placement.layer, layer_order),
            designator_sort_key(placement.designator, prefix_order=prefix_order),
        ),
    )


def group_bom_components(
    components: Sequence[NormalizedBomComponent],
    *,
    group_fields: Sequence[str] = (
        "manufacturer",
        "manufacturer_part_number",
        "value",
        "footprint",
    ),
    split_dnp: bool = True,
    prefix_order: Sequence[str] = (),
) -> list[GroupedBomLine]:
    """Group normalized BOM components into manufacturable line items."""
    buckets: dict[tuple[str, ...], list[NormalizedBomComponent]] = {}
    for component in components:
        key = _bom_group_key(component, group_fields, split_dnp=split_dnp)
        buckets.setdefault(key, []).append(component)

    sorted_groups = sorted(
        buckets.values(),
        key=lambda group: designator_sort_key(
            _first_designator(group, prefix_order=prefix_order),
            prefix_order=prefix_order,
        ),
    )
    return [
        _grouped_line(index, group, prefix_order=prefix_order)
        for index, group in enumerate(sorted_groups, start=1)
    ]


def bom_raw_payload(
    components: Sequence[NormalizedBomComponent],
    *,
    source: Path,
    variant: str | None,
) -> dict[str, object]:
    """Build the normalized raw BOM JSON payload."""
    return {
        "schema": BOM_RAW_SCHEMA,
        "source": _source_payload(source),
        "variant": variant,
        "component_count": len(components),
        "dnp_count": sum(1 for component in components if component.dnp),
        "components": [component.to_json_obj() for component in components],
    }


def grouped_bom_payload(
    lines: Sequence[GroupedBomLine],
    *,
    source: Path,
    variant: str | None,
) -> dict[str, object]:
    """Build the grouped BOM JSON payload."""
    return {
        "schema": BOM_GROUPED_SCHEMA,
        "source": _source_payload(source),
        "variant": variant,
        "line_count": len(lines),
        "component_count": sum(line.quantity for line in lines),
        "dnp_line_count": sum(1 for line in lines if line.dnp),
        "lines": [line.to_json_obj() for line in lines],
    }


def pnp_payload(
    placements: Sequence[NormalizedPlacement],
    *,
    source: Path,
    variant: str | None,
    units: str,
) -> dict[str, object]:
    """Build the normalized PnP JSON payload."""
    return {
        "schema": PNP_SCHEMA,
        "source": _source_payload(source),
        "variant": variant,
        "units": units,
        "placement_count": len(placements),
        "placements": [
            placement.to_json_obj()
            for placement in sort_placements(placements)
        ],
    }


def jlc_bom_rows(
    lines: Sequence[GroupedBomLine],
    *,
    include_dnp: bool = False,
) -> list[dict[str, str]]:
    """Return JLCPCB BOM rows from grouped BOM lines."""
    rows: list[dict[str, str]] = []
    for line in lines:
        if line.dnp and not include_dnp:
            continue
        rows.append(
            {
                "Comment": _line_comment(line.fields),
                "Designator": ", ".join(line.designators),
                "Footprint": line.fields.get("footprint", ""),
                "JLCPCB Part #": line.fields.get("jlcpcb_part_number", ""),
            }
        )
    return rows


def jlc_cpl_rows(
    placements: Sequence[NormalizedPlacement],
    *,
    layer_order: Sequence[str] = ("top", "bottom"),
    prefix_order: Sequence[str] = (),
) -> list[dict[str, str]]:
    """Return JLCPCB CPL rows from normalized placements."""
    rows: list[dict[str, str]] = []
    for placement in sort_placements(
        placements,
        layer_order=layer_order,
        prefix_order=prefix_order,
    ):
        rows.append(
            {
                "Designator": placement.designator,
                "Layer": _jlc_layer_name(placement.layer),
                "Mid X": _format_decimal(placement.center_x, precision=4),
                "Mid Y": _format_decimal(placement.center_y, precision=4),
                "Rotation": _format_decimal(placement.rotation, precision=2),
            }
        )
    return rows


def _normalize_bom_component(
    component: Mapping[str, object],
    aliases: FieldAliasConfig,
) -> NormalizedBomComponent:
    """Normalize one raw BOM component mapping."""
    parameters = _coerce_str_dict(component.get("parameters"))
    intrinsic = {
        "value": _string_value(component.get("value")),
        "description": _string_value(component.get("description")),
        "footprint": _string_value(component.get("footprint")),
    }
    canonical, sources = _resolve_canonical_fields(parameters, intrinsic, aliases)
    return NormalizedBomComponent(
        designator=_string_value(component.get("designator")),
        value=intrinsic["value"],
        footprint=intrinsic["footprint"],
        library_ref=_string_value(component.get("library_ref")),
        description=intrinsic["description"],
        sheet=_string_value(component.get("sheet")),
        dnp=bool(component.get("dnp")),
        parameters=parameters,
        canonical_fields=canonical,
        field_sources=sources,
    )


def _normalize_pnp_entry(
    entry: object,
    *,
    units: str,
    aliases: FieldAliasConfig,
) -> NormalizedPlacement:
    """Normalize one PnP entry object or mapping."""
    parameters = _coerce_str_dict(_entry_value(entry, "parameters"))
    intrinsic = {
        "value": _string_value(_entry_value(entry, "comment")),
        "description": _string_value(_entry_value(entry, "description")),
        "footprint": _string_value(_entry_value(entry, "footprint")),
    }
    canonical, sources = _resolve_canonical_fields(parameters, intrinsic, aliases)
    return NormalizedPlacement(
        designator=_string_value(_entry_value(entry, "designator")),
        comment=intrinsic["value"],
        layer=_normalize_layer(_string_value(_entry_value(entry, "layer"))),
        footprint=intrinsic["footprint"],
        center_x=_float_value(_entry_value(entry, "center_x")),
        center_y=_float_value(_entry_value(entry, "center_y")),
        rotation=_float_value(_entry_value(entry, "rotation")),
        units=units,
        description=intrinsic["description"],
        parameters=parameters,
        canonical_fields=canonical,
        field_sources=sources,
    )


def _resolve_canonical_fields(
    parameters: Mapping[str, str],
    intrinsic: Mapping[str, str],
    aliases: FieldAliasConfig,
) -> tuple[dict[str, str], dict[str, str]]:
    """Resolve every configured canonical field and source."""
    canonical: dict[str, str] = {}
    sources: dict[str, str] = {}
    lookup = _casefold_parameter_lookup(parameters)
    for name in sorted(aliases.canonical_fields):
        value, source = _resolve_canonical_field(
            name,
            lookup,
            intrinsic.get(name, ""),
            aliases,
        )
        if value:
            canonical[name] = value
            sources[name] = source
    return canonical, sources


def _resolve_canonical_field(
    canonical_name: str,
    lookup: Mapping[str, tuple[str, str]],
    fallback: str,
    aliases: FieldAliasConfig,
) -> tuple[str, str]:
    """Resolve one canonical field from parameters or intrinsic fallback."""
    for alias in aliases.aliases_for(canonical_name):
        found = lookup.get(alias.casefold())
        if found is not None:
            original_name, value = found
            return value, f"parameter:{original_name}"
    if fallback:
        return fallback, f"intrinsic:{canonical_name}"
    return "", ""


def _coerce_str_dict(value: object) -> dict[str, str]:
    """Coerce a mapping-like object into string keys and values."""
    if not isinstance(value, Mapping):
        return {}
    result: dict[str, str] = {}
    for key, item in value.items():
        name = _string_value(key)
        if name:
            result[name] = _string_value(item)
    return result


def _casefold_parameter_lookup(
    parameters: Mapping[str, str],
) -> dict[str, tuple[str, str]]:
    """Build a case-insensitive parameter lookup that preserves source names."""
    lookup: dict[str, tuple[str, str]] = {}
    for name, value in parameters.items():
        key = name.casefold()
        if key not in lookup and value:
            lookup[key] = (name, value)
    return lookup


def _entry_value(entry: object, name: str) -> object:
    """Read a named field from a mapping or object."""
    if isinstance(entry, Mapping):
        return entry.get(name)
    return getattr(entry, name, None)


def _string_value(value: object) -> str:
    """Convert a possibly missing value to stripped text."""
    if value is None:
        return ""
    return str(value).strip()


def _float_value(value: object) -> float:
    """Convert a possibly missing value to float."""
    if value is None:
        return 0.0
    if isinstance(value, int | float):
        return float(value)
    if not isinstance(value, str):
        return 0.0
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _normalize_name(name: str) -> str:
    """Normalize a canonical field name for config lookups."""
    return name.strip().casefold().replace(" ", "_").replace("-", "_")


def _tokenize_designator(designator: str) -> tuple[tuple[int, int | str], ...]:
    """Split a designator into comparable natural-sort tokens."""
    tokens: list[tuple[int, int | str]] = []
    for token in _DESIGNATOR_TOKEN_RE.findall(designator):
        if token.isdigit():
            tokens.append((0, int(token)))
        else:
            tokens.append((1, token.casefold()))
    return tuple(tokens)


def _prefix_rank(designator: str, prefix_order: Sequence[str]) -> int:
    """Return the configured prefix rank for a designator."""
    if not prefix_order:
        return 0
    match = _LEADING_PREFIX_RE.match(designator)
    prefix = match.group(0).casefold() if match else ""
    normalized_order = [item.casefold() for item in prefix_order]
    if prefix in normalized_order:
        return normalized_order.index(prefix)
    return len(normalized_order)


def _layer_rank(layer: str, layer_order: Sequence[str]) -> int:
    """Return the configured layer rank for sorting."""
    normalized_layer = _normalize_layer(layer)
    normalized_order = [_normalize_layer(item) for item in layer_order]
    if normalized_layer in normalized_order:
        return normalized_order.index(normalized_layer)
    return len(normalized_order)


def _normalize_layer(layer: str) -> str:
    """Normalize common Altium layer names into top or bottom."""
    normalized = layer.strip().casefold().replace("layer", "")
    if normalized in {"top", "toplayer"}:
        return "top"
    if normalized in {"bottom", "bottomlayer", "bot"}:
        return "bottom"
    return normalized


def _bom_group_key(
    component: NormalizedBomComponent,
    group_fields: Sequence[str],
    *,
    split_dnp: bool,
) -> tuple[str, ...]:
    """Build the BOM grouping key for one normalized component."""
    values = [
        component.canonical_fields.get(_normalize_name(field), "").casefold()
        for field in group_fields
    ]
    if not any(values):
        values = [
            component.value.casefold(),
            component.footprint.casefold(),
            component.description.casefold(),
        ]
    if split_dnp:
        values.append("dnp" if component.dnp else "fitted")
    return tuple(values)


def _first_designator(
    components: Sequence[NormalizedBomComponent],
    *,
    prefix_order: Sequence[str],
) -> str:
    """Return the first natural-sorted designator from a component group."""
    return sort_designators(
        [component.designator for component in components],
        prefix_order=prefix_order,
    )[0]


def _grouped_line(
    item: int,
    components: Sequence[NormalizedBomComponent],
    *,
    prefix_order: Sequence[str],
) -> GroupedBomLine:
    """Create one grouped BOM line from normalized components."""
    designators = tuple(
        sort_designators(
            [component.designator for component in components],
            prefix_order=prefix_order,
        )
    )
    fields = _line_fields(components)
    return GroupedBomLine(
        item=item,
        quantity=len(components),
        designators=designators,
        dnp=all(component.dnp for component in components),
        fields=fields,
    )


def _line_fields(components: Sequence[NormalizedBomComponent]) -> dict[str, str]:
    """Merge canonical fields for a grouped BOM line."""
    fields: dict[str, str] = {}
    for component in components:
        for name, value in component.canonical_fields.items():
            if value and name not in fields:
                fields[name] = value
    return fields


def _line_comment(fields: Mapping[str, str]) -> str:
    """Return the preferred JLC comment text for a grouped BOM line."""
    for name in ("description", "value"):
        value = fields.get(name, "")
        if value:
            return value
    return ""


def _source_payload(source: Path) -> dict[str, str]:
    """Return common source metadata for JSON payloads."""
    return {
        "path": str(source),
        "name": source.name,
        "stem": source.stem,
    }


def _jlc_layer_name(layer: str) -> str:
    """Return the JLCPCB layer name for a normalized placement layer."""
    normalized = _normalize_layer(layer)
    if normalized == "top":
        return "Top"
    if normalized == "bottom":
        return "Bottom"
    return layer


def _format_decimal(value: float, *, precision: int) -> str:
    """Format a decimal value without unnecessary trailing zeroes."""
    formatted = f"{value:.{precision}f}"
    return formatted.rstrip("0").rstrip(".") if "." in formatted else formatted
