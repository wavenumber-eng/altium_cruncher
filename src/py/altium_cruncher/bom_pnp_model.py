"""Shared BOM and pick-and-place normalization helpers."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
import json
from pathlib import Path
import re

from altium_monkey.altium_pnp_position import (
    PNP_POSITION_MODE_ALTIUM_PICK_PLACE,
    PNP_POSITION_MODES,
    PnpPositionMode,
    normalize_pnp_position_mode,
)

from altium_cruncher.output_path_templates import (
    TemplateValue,
    resolve_output_name,
    resolve_output_expression,
    resolve_output_relative_path,
)

BOM_PNP_DEFAULT_CONFIG_NAME = "bom.config"
BOM_PNP_FALLBACK_CONFIG_NAME = "bom.config.json"
BOM_PNP_CONFIG_SCHEMA = "wn.altium_cruncher.bom.config.v1"
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
BOM_GROUPED_DEFAULT_COLUMNS: tuple[str, ...] = (
    "item",
    "quantity",
    "designators",
    "dnp",
    "manufacturer",
    "manufacturer_part_number",
    "value",
    "footprint",
    "description",
    "jlcpcb_part_number",
)
PNP_DEFAULT_COLUMNS: tuple[str, ...] = (
    "designator",
    "comment",
    "layer",
    "footprint",
    "center_x",
    "center_y",
    "rotation",
    "description",
)
_BOM_OUTPUT_KINDS = frozenset(
    {
        "raw-json",
        "legacy-json",
        "grouped-json",
        "grouped-csv",
        "grouped-xlsx",
        "jlc-csv",
        "jlc-xlsx",
    }
)
_PNP_OUTPUT_KINDS = frozenset({"json", "csv", "xlsx", "jlc-cpl", "jlc-cpl-xlsx"})
_BOM_SOURCE_MODES = frozenset({"schematic", "pcb", "merged"})
_PNP_POSITION_MODES = frozenset(PNP_POSITION_MODES)
_DNP_PLACEMENTS = frozenset({"inline", "end", "separate"})
_VARIANT_MODES = frozenset({"base", "all", "named"})

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
        mapping: Mapping[str, object],
    ) -> "FieldAliasConfig":
        """Build an alias config from JSON-style mappings."""
        return cls(
            {
                _normalize_name(name): _string_tuple(aliases)
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
class BomPnpConfig:
    """Versioned BOM/PnP command configuration."""

    schema: str = BOM_PNP_CONFIG_SCHEMA
    field_aliases: FieldAliasConfig = field(default_factory=FieldAliasConfig)
    variant_mode: str = "base"
    variant_names: tuple[str, ...] = ()
    include_base_variant: bool = True
    bom_source_mode: str = "schematic"
    bom_outputs: tuple[str, ...] = (
        "raw-json",
        "grouped-json",
        "grouped-xlsx",
    )
    bom_group_fields: tuple[str, ...] = (
        "manufacturer",
        "manufacturer_part_number",
        "value",
        "footprint",
    )
    bom_output_fields: tuple[str, ...] = BOM_GROUPED_DEFAULT_COLUMNS
    include_dnp: bool = True
    split_dnp: bool = True
    dnp_placement: str = "inline"
    highlight_dnp_rows: bool = True
    pcb_line_item_enabled: bool = False
    pcb_line_item_designator: str = "PCB"
    pcb_line_item_fields: dict[str, str] = field(default_factory=dict)
    pnp_outputs: tuple[str, ...] = ("json", "csv")
    pnp_output_fields: tuple[str, ...] = PNP_DEFAULT_COLUMNS
    pnp_units: str = "mm"
    pnp_position_mode: PnpPositionMode = PNP_POSITION_MODE_ALTIUM_PICK_PLACE
    pnp_exclude_no_bom: bool = False
    layer_order: tuple[str, ...] = ("top", "bottom")
    prefix_order: tuple[str, ...] = ()
    output_dir_template: str = "{Command}"
    output_name_template: str = "{SourceStem}_{VariantName}_{OutputKind}"

    @classmethod
    def from_mapping(cls, payload: Mapping[str, object]) -> "BomPnpConfig":
        """Build a config from a JSON-style mapping."""
        if payload.get("schema") not in {None, BOM_PNP_CONFIG_SCHEMA}:
            raise ValueError(
                f"Unsupported BOM/PnP config schema: {payload.get('schema')}"
            )
        variants = _mapping_value(payload.get("variants"))
        bom = _mapping_value(payload.get("bom"))
        pnp = _mapping_value(payload.get("pnp"))
        output = _mapping_value(payload.get("output"))
        pcb_line_item = _mapping_value(bom.get("pcb_line_item"))
        aliases = _mapping_value(payload.get("field_aliases"))

        return cls(
            field_aliases=FieldAliasConfig.from_mapping(aliases)
            if aliases
            else FieldAliasConfig(),
            variant_mode=_choice(
                _string_value(variants.get("mode") or "base"),
                _VARIANT_MODES,
                "variant mode",
            ),
            variant_names=_string_tuple(variants.get("names")),
            include_base_variant=_bool_value(
                variants.get("include_base"),
                default=True,
            ),
            bom_source_mode=_choice(
                _string_value(bom.get("source_mode") or "schematic"),
                _BOM_SOURCE_MODES,
                "BOM source mode",
            ),
            bom_outputs=_choices_tuple(
                bom.get("outputs"),
                _BOM_OUTPUT_KINDS,
                ("raw-json", "grouped-json", "grouped-xlsx"),
                "BOM output",
            ),
            bom_group_fields=_string_tuple(
                bom.get("group_fields"),
                default=(
                    "manufacturer",
                    "manufacturer_part_number",
                    "value",
                    "footprint",
                ),
            ),
            bom_output_fields=_string_tuple(
                bom.get("output_fields"),
                default=BOM_GROUPED_DEFAULT_COLUMNS,
            ),
            include_dnp=_bool_value(bom.get("include_dnp"), default=True),
            split_dnp=_bool_value(bom.get("split_dnp"), default=True),
            dnp_placement=_choice(
                _string_value(bom.get("dnp_placement") or "inline"),
                _DNP_PLACEMENTS,
                "DNP placement",
            ),
            highlight_dnp_rows=_bool_value(
                bom.get("highlight_dnp_rows"),
                default=True,
            ),
            pcb_line_item_enabled=_bool_value(
                pcb_line_item.get("enabled"),
                default=False,
            ),
            pcb_line_item_designator=_string_value(
                pcb_line_item.get("designator") or "PCB"
            ),
            pcb_line_item_fields=_string_mapping(pcb_line_item.get("fields")),
            pnp_outputs=_choices_tuple(
                pnp.get("outputs"),
                _PNP_OUTPUT_KINDS,
                ("json", "csv"),
                "PnP output",
            ),
            pnp_output_fields=_string_tuple(
                pnp.get("output_fields"),
                default=PNP_DEFAULT_COLUMNS,
            ),
            pnp_units=_choice(
                _string_value(pnp.get("units") or "mm"),
                frozenset({"mm", "mils"}),
                "PnP units",
            ),
            pnp_position_mode=_pnp_position_mode_from_config(pnp),
            pnp_exclude_no_bom=_bool_value(
                pnp.get("exclude_no_bom"),
                default=False,
            ),
            layer_order=_string_tuple(
                pnp.get("layer_order"),
                default=("top", "bottom"),
            ),
            prefix_order=_string_tuple(
                pnp.get("prefix_order"),
                default=_string_tuple(bom.get("prefix_order")),
            ),
            output_dir_template=_string_value(
                output.get("dir_template") or "{Command}"
            ),
            output_name_template=_string_value(
                output.get("name_template")
                or "{SourceStem}_{VariantName}_{OutputKind}"
            ),
        )

    def to_json_obj(self) -> dict[str, object]:
        """Return a deterministic JSON-compatible config object."""
        return {
            "schema": self.schema,
            "field_aliases": self.field_aliases.to_json_obj(),
            "variants": {
                "mode": self.variant_mode,
                "names": list(self.variant_names),
                "include_base": self.include_base_variant,
            },
            "bom": {
                "source_mode": self.bom_source_mode,
                "outputs": list(self.bom_outputs),
                "group_fields": list(self.bom_group_fields),
                "output_fields": list(self.bom_output_fields),
                "include_dnp": self.include_dnp,
                "split_dnp": self.split_dnp,
                "dnp_placement": self.dnp_placement,
                "highlight_dnp_rows": self.highlight_dnp_rows,
                "prefix_order": list(self.prefix_order),
                "pcb_line_item": {
                    "enabled": self.pcb_line_item_enabled,
                    "designator": self.pcb_line_item_designator,
                    "fields": dict(sorted(self.pcb_line_item_fields.items())),
                },
            },
            "pnp": {
                "outputs": list(self.pnp_outputs),
                "output_fields": list(self.pnp_output_fields),
                "units": self.pnp_units,
                "position_mode": self.pnp_position_mode,
                "exclude_no_bom": self.pnp_exclude_no_bom,
                "layer_order": list(self.layer_order),
                "prefix_order": list(self.prefix_order),
            },
            "output": {
                "dir_template": self.output_dir_template,
                "name_template": self.output_name_template,
            },
        }


def find_bom_pnp_config_path(start_dir: Path | None = None) -> Path | None:
    """Return the first default BOM/PnP config path found in a directory."""
    root = (start_dir or Path.cwd()).resolve()
    for name in (BOM_PNP_DEFAULT_CONFIG_NAME, BOM_PNP_FALLBACK_CONFIG_NAME):
        candidate = root / name
        if candidate.exists():
            return candidate
    return None


def load_bom_pnp_config(path: Path) -> BomPnpConfig:
    """Load a BOM/PnP JSON config file."""
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, Mapping):
        raise ValueError(f"BOM/PnP config must be a JSON object: {path}")
    return BomPnpConfig.from_mapping(payload)


def _pnp_position_mode_from_config(pnp: Mapping[str, object]) -> PnpPositionMode:
    """Return the configured PnP position mode."""
    raw_mode = _string_value(
        pnp.get("position_mode") or PNP_POSITION_MODE_ALTIUM_PICK_PLACE
    )
    return normalize_pnp_position_mode(
        _choice(raw_mode, _PNP_POSITION_MODES, "PnP position mode")
    )


def write_bom_pnp_config(
    path: Path,
    config: BomPnpConfig | None = None,
) -> None:
    """Write a default BOM/PnP config template."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps((config or BomPnpConfig()).to_json_obj(), indent=2) + "\n",
        encoding="utf-8",
    )


def select_variant_names(
    available_variants: Sequence[str],
    config: BomPnpConfig,
    *,
    cli_variant: str | None = None,
    cli_all_variants: bool = False,
) -> list[str | None]:
    """Select variant names from CLI overrides and config policy."""
    available = list(available_variants)
    if cli_all_variants:
        return [None, *available]
    if cli_variant:
        return [cli_variant]
    if config.variant_mode == "all":
        variants: list[str | None] = []
        if config.include_base_variant:
            variants.append(None)
        variants.extend(available)
        return variants or [None]
    if config.variant_mode == "named":
        variants = []
        if config.include_base_variant:
            variants.append(None)
        variants.extend(config.variant_names)
        return variants or [None]
    return [None]


def configured_output_file(
    output_root: Path,
    config: BomPnpConfig,
    *,
    source: Path,
    command: str,
    output_kind: str,
    extension: str,
    project_parameters: Mapping[str, TemplateValue],
    variant_name: str | None,
) -> Path:
    """Resolve a safe configured output path for one generated artifact."""
    variant_label = variant_name or "base"
    tokens: dict[str, TemplateValue] = {
        "Command": command,
        "OutputKind": output_kind,
        "SourceName": source.name,
        "SourceStem": source.stem,
        "VariantName": variant_label,
    }
    relative_dir = resolve_output_relative_path(
        config.output_dir_template,
        project_parameters,
        variant_name=variant_label,
        tokens=tokens,
        missing="empty",
    )
    filename_stem = resolve_output_name(
        config.output_name_template,
        project_parameters,
        variant_name=variant_label,
        tokens=tokens,
        missing="empty",
    )
    suffix = f".{extension.lstrip('.')}"
    filename = (
        filename_stem
        if filename_stem.casefold().endswith(suffix.casefold())
        else f"{filename_stem}{suffix}"
    )
    output_dir = output_root.joinpath(*relative_dir.parts)
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / filename


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


def ordered_bom_lines(
    lines: Sequence[GroupedBomLine],
    *,
    dnp_placement: str = "inline",
) -> list[GroupedBomLine]:
    """Order grouped BOM lines according to DNP placement policy."""
    placement = _choice(dnp_placement, _DNP_PLACEMENTS, "DNP placement")
    if placement in {"end", "separate"}:
        return _renumber_bom_lines(_bom_lines_with_dnp_at_end(lines))
    return _renumber_bom_lines(_bom_lines_with_matching_dnp(lines))


def _bom_lines_with_dnp_at_end(
    lines: Sequence[GroupedBomLine],
) -> list[GroupedBomLine]:
    """Return fitted BOM lines followed by DNP BOM lines."""
    fitted, dnp = _split_bom_lines_by_dnp(lines)
    return [*fitted, *dnp]


def _bom_lines_with_matching_dnp(
    lines: Sequence[GroupedBomLine],
) -> list[GroupedBomLine]:
    """Return DNP BOM lines immediately after matching fitted lines."""
    fitted, dnp = _split_bom_lines_by_dnp(lines)
    dnp_by_key: dict[tuple[tuple[str, str], ...], list[GroupedBomLine]] = {}
    for line in dnp:
        dnp_by_key.setdefault(_bom_line_match_key(line), []).append(line)

    ordered: list[GroupedBomLine] = []
    used_dnp: set[int] = set()
    for line in fitted:
        ordered.append(line)
        for dnp_line in dnp_by_key.get(_bom_line_match_key(line), []):
            if id(dnp_line) not in used_dnp:
                ordered.append(dnp_line)
                used_dnp.add(id(dnp_line))
    for line in dnp:
        if id(line) not in used_dnp:
            ordered.append(line)
            used_dnp.add(id(line))
    return ordered


def _split_bom_lines_by_dnp(
    lines: Sequence[GroupedBomLine],
) -> tuple[list[GroupedBomLine], list[GroupedBomLine]]:
    """Split BOM lines into fitted and DNP lists without changing order."""
    return (
        [line for line in lines if not line.dnp],
        [line for line in lines if line.dnp],
    )


def filter_bom_components(
    components: Sequence[NormalizedBomComponent],
    *,
    include_dnp: bool,
) -> list[NormalizedBomComponent]:
    """Apply BOM inclusion policy to normalized components."""
    if include_dnp:
        return list(components)
    return [component for component in components if not component.dnp]


def grouped_bom_table_rows(
    lines: Sequence[GroupedBomLine],
    *,
    fields: Sequence[str] = BOM_GROUPED_DEFAULT_COLUMNS,
    dnp_placement: str | None = "inline",
) -> list[dict[str, str]]:
    """Return configured table rows for grouped BOM outputs."""
    rows: list[dict[str, str]] = []
    ordered_lines = (
        list(lines)
        if dnp_placement is None
        else ordered_bom_lines(lines, dnp_placement=dnp_placement)
    )
    for line in ordered_lines:
        rows.append({field: _grouped_line_field(line, field) for field in fields})
    return rows


def pnp_table_rows(
    placements: Sequence[NormalizedPlacement],
    *,
    fields: Sequence[str] = PNP_DEFAULT_COLUMNS,
    layer_order: Sequence[str] = ("top", "bottom"),
    prefix_order: Sequence[str] = (),
) -> list[dict[str, str]]:
    """Return configured table rows for PnP outputs."""
    return [
        {field: _placement_field(placement, field) for field in fields}
        for placement in sort_placements(
            placements,
            layer_order=layer_order,
            prefix_order=prefix_order,
        )
    ]


def make_pcb_line_item(
    config: BomPnpConfig,
    project_parameters: Mapping[str, TemplateValue],
    *,
    variant_name: str | None,
) -> NormalizedBomComponent | None:
    """Create the optional configured PCB BOM line item."""
    if not config.pcb_line_item_enabled:
        return None
    canonical_fields = {
        _normalize_name(name): resolve_output_expression(
            template,
            project_parameters,
            variant_name=variant_name,
            tokens={"VariantName": variant_name or "base"},
            missing="empty",
        )
        for name, template in config.pcb_line_item_fields.items()
    }
    canonical_fields = {
        name: value for name, value in canonical_fields.items() if value
    }
    return NormalizedBomComponent(
        designator=config.pcb_line_item_designator,
        value=canonical_fields.get("value", ""),
        footprint=canonical_fields.get("footprint", "PCB"),
        library_ref="PCB",
        description=canonical_fields.get("description", ""),
        sheet="",
        dnp=False,
        parameters=dict(canonical_fields),
        canonical_fields=canonical_fields,
        field_sources={
            name: "config:pcb_line_item.fields" for name in canonical_fields
        },
    )


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


def flat_raw_bom_payload(bom: Sequence[Mapping[str, object]]) -> list[dict[str, object]]:
    """Return flat raw BOM components before aliases or grouping are applied."""
    return [
        {
            str(name): _json_compatible_value(value)
            for name, value in component.items()
        }
        for component in bom
    ]


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
    position_mode: str = PNP_POSITION_MODE_ALTIUM_PICK_PLACE,
    layer_order: Sequence[str] = ("top", "bottom"),
    prefix_order: Sequence[str] = (),
) -> dict[str, object]:
    """Build the normalized PnP JSON payload."""
    return {
        "schema": PNP_SCHEMA,
        "source": _source_payload(source),
        "variant": variant,
        "units": units,
        "position_mode": normalize_pnp_position_mode(position_mode),
        "placement_count": len(placements),
        "placements": [
            placement.to_json_obj()
            for placement in sort_placements(
                placements,
                layer_order=layer_order,
                prefix_order=prefix_order,
            )
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


def _grouped_line_field(line: GroupedBomLine, field_name: str) -> str:
    """Return one configured grouped BOM field as text."""
    normalized = _normalize_name(field_name)
    if normalized == "item":
        return str(line.item)
    if normalized == "quantity":
        return str(line.quantity)
    if normalized == "designators":
        return ", ".join(line.designators)
    if normalized == "dnp":
        return "Yes" if line.dnp else "No"
    return line.fields.get(normalized, "")


def _placement_field(placement: NormalizedPlacement, field_name: str) -> str:
    """Return one configured placement field as text."""
    normalized = _normalize_name(field_name)
    if normalized == "designator":
        return placement.designator
    if normalized == "comment":
        return placement.comment
    if normalized == "layer":
        return placement.layer
    if normalized == "footprint":
        return placement.footprint
    if normalized == "center_x":
        return _format_decimal(placement.center_x, precision=4)
    if normalized == "center_y":
        return _format_decimal(placement.center_y, precision=4)
    if normalized == "rotation":
        return _format_decimal(placement.rotation, precision=2)
    if normalized == "description":
        return placement.description
    return placement.canonical_fields.get(
        normalized,
        placement.parameters.get(field_name, ""),
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


def _mapping_value(value: object) -> Mapping[str, object]:
    """Return a mapping value or an empty mapping."""
    if isinstance(value, Mapping):
        return value
    return {}


def _string_tuple(
    value: object,
    *,
    default: Sequence[str] = (),
) -> tuple[str, ...]:
    """Return a tuple of non-empty string values from config input."""
    if value is None:
        return tuple(default)
    if isinstance(value, str):
        text = value.strip()
        return (text,) if text else tuple(default)
    if not isinstance(value, Sequence):
        return tuple(default)
    result = tuple(_string_value(item) for item in value if _string_value(item))
    return result or tuple(default)


def _string_mapping(value: object) -> dict[str, str]:
    """Return a string mapping from config input."""
    if not isinstance(value, Mapping):
        return {}
    return {
        _string_value(key): _string_value(item)
        for key, item in value.items()
        if _string_value(key)
    }


def _bool_value(value: object, *, default: bool) -> bool:
    """Return a bool value from config input."""
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().casefold() in {"1", "true", "yes", "on"}
    return bool(value)


def _choice(value: str, allowed: frozenset[str], label: str) -> str:
    """Validate a normalized config choice."""
    normalized = value.strip().casefold()
    if normalized not in allowed:
        raise ValueError(f"Unsupported {label}: {value}")
    return normalized


def _choices_tuple(
    value: object,
    allowed: frozenset[str],
    default: Sequence[str],
    label: str,
) -> tuple[str, ...]:
    """Validate a sequence of config choices."""
    choices = _string_tuple(value, default=default)
    return tuple(_choice(choice, allowed, label) for choice in choices)


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


def _renumber_bom_lines(lines: Sequence[GroupedBomLine]) -> list[GroupedBomLine]:
    """Return BOM lines with display item numbers matching row order."""
    return [
        GroupedBomLine(
            item=index,
            quantity=line.quantity,
            designators=line.designators,
            dnp=line.dnp,
            fields=dict(line.fields),
        )
        for index, line in enumerate(lines, start=1)
    ]


def _bom_line_match_key(line: GroupedBomLine) -> tuple[tuple[str, str], ...]:
    """Return the manufacturable identity key used to pair fitted and DNP rows."""
    return tuple(sorted(line.fields.items()))


def _line_fields(components: Sequence[NormalizedBomComponent]) -> dict[str, str]:
    """Merge canonical fields for a grouped BOM line."""
    fields: dict[str, str] = {}
    for component in components:
        for name, value in component.canonical_fields.items():
            if value and name not in fields:
                fields[name] = value
    return fields


def _json_compatible_value(value: object) -> object:
    """Return a JSON-compatible value while preserving raw field names."""
    if isinstance(value, Mapping):
        return {
            str(name): _json_compatible_value(item)
            for name, item in value.items()
        }
    if isinstance(value, list | tuple):
        return [_json_compatible_value(item) for item in value]
    if value is None or isinstance(value, str | int | float | bool):
        return value
    return str(value)


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
