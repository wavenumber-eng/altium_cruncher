"""Component inventory helpers for generated PCB SVG configs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import TYPE_CHECKING

from altium_cruncher.altium_cruncher_pcb_workflow import (
    iter_pcb_render_inputs,
    load_design_for_pcb_input,
)
from altium_cruncher.altium_cruncher_pcb_svg_pin1 import choose_pin1_pad_designator

if TYPE_CHECKING:
    from altium_monkey.altium_pcbdoc import AltiumPcbDoc


_DESIGNATOR_SORT_RE = re.compile(r"^([A-Za-z]+)(\d+)(.*)$")
_DIODE_PREFIX_RE = re.compile(r"^(D|LED)\d", re.IGNORECASE)
_DIODE_TERMS = ("diode", "schottky", "zener", "tvs", "led")
_CATHODE_PAD_NAMES = ("K", "C")


@dataclass(frozen=True, slots=True)
class PcbSvgComponentInventoryEntry:
    """One component entry used to annotate generated PCB SVG configs."""

    designator: str
    side: str
    footprint: str
    description: str
    pad_designators: tuple[str, ...]
    rotation_degrees: float
    unique_id: str
    diode_candidate: bool
    diode_reason: str
    cathode_pad: str | None
    pin1_pad: str | None

    @property
    def is_two_pin_diode(self) -> bool:
        return self.diode_candidate and len(self.pad_designators) == 2


@dataclass(frozen=True, slots=True)
class PcbSvgComponentInventory:
    """Board component inventory used by PCB SVG config generation."""

    board_key: str
    pcb_path: Path
    components: tuple[PcbSvgComponentInventoryEntry, ...]

    @property
    def diode_candidates(self) -> tuple[PcbSvgComponentInventoryEntry, ...]:
        return tuple(entry for entry in self.components if entry.diode_candidate)


def _designator_sort_key(value: str) -> tuple[str, int, str]:
    match = _DESIGNATOR_SORT_RE.match(value.strip())
    if not match:
        return (value.upper(), -1, "")
    prefix, number, suffix = match.groups()
    return (prefix.upper(), int(number), suffix.upper())


def _component_side(component: object) -> str:
    normalized = getattr(component, "get_layer_normalized", None)
    if callable(normalized):
        side = str(normalized()).strip().lower()
        if side:
            return side
    raw_layer = str(getattr(component, "layer", "") or "").strip().lower()
    if "bottom" in raw_layer:
        return "bottom"
    if "top" in raw_layer:
        return "top"
    return raw_layer or "unknown"


def _component_rotation(component: object) -> float:
    rotation = getattr(component, "get_rotation_degrees", None)
    if callable(rotation):
        try:
            value = rotation()
            if isinstance(value, (int, float, str)):
                return float(value)
        except (TypeError, ValueError):
            return 0.0
    return 0.0


def _parameter_values(component: object) -> list[str]:
    parameters = getattr(component, "parameters", None)
    if not isinstance(parameters, dict):
        return []
    return [str(value) for value in parameters.values() if str(value).strip()]


def _component_search_text(component: object) -> str:
    fields = [
        getattr(component, "designator", ""),
        getattr(component, "footprint", ""),
        getattr(component, "description", ""),
    ]
    raw_record = getattr(component, "raw_record", None)
    if isinstance(raw_record, dict):
        for key in ("SOURCEDESCRIPTION", "SOURCELIBREFERENCE", "COMMENT", "PATTERN"):
            fields.append(raw_record.get(key, ""))
    fields.extend(_parameter_values(component))
    return " ".join(str(field) for field in fields if str(field).strip()).lower()


def _diode_reason(component: object) -> str:
    designator = str(getattr(component, "designator", "") or "")
    has_prefix = bool(_DIODE_PREFIX_RE.match(designator))
    search_text = _component_search_text(component)
    matched_terms = [term for term in _DIODE_TERMS if term in search_text]
    if has_prefix and matched_terms:
        return "designator+text:" + ",".join(matched_terms)
    if has_prefix:
        return "designator"
    if matched_terms:
        return "text:" + ",".join(matched_terms)
    return ""


def _pads_for_component(pcbdoc: "AltiumPcbDoc", component_index: int) -> list[object]:
    pads = getattr(pcbdoc, "pads", []) or []
    return [
        pad
        for pad in pads
        if getattr(pad, "component_index", None) == component_index
    ]


def _pad_designators(pads: list[object]) -> tuple[str, ...]:
    values = {
        str(getattr(pad, "designator", "") or "").strip()
        for pad in pads
        if str(getattr(pad, "designator", "") or "").strip()
    }
    return tuple(sorted(values, key=_designator_sort_key))


def _cathode_pad(pad_designators: tuple[str, ...]) -> str | None:
    by_upper = {value.upper(): value for value in pad_designators}
    for name in _CATHODE_PAD_NAMES:
        if name in by_upper:
            return by_upper[name]
    return None


def build_pcb_svg_component_inventory_from_pcbdoc(
    *,
    board_key: str,
    pcb_path: Path,
    pcbdoc: "AltiumPcbDoc",
) -> PcbSvgComponentInventory:
    """Build a component inventory from a parsed PcbDoc without HLR work."""
    entries: list[PcbSvgComponentInventoryEntry] = []
    components = list(getattr(pcbdoc, "components", []) or [])
    for index, component in enumerate(components):
        designator = str(getattr(component, "designator", "") or "").strip()
        if not designator:
            continue
        pads = _pad_designators(_pads_for_component(pcbdoc, index))
        reason = _diode_reason(component)
        entries.append(
            PcbSvgComponentInventoryEntry(
                designator=designator,
                side=_component_side(component),
                footprint=str(getattr(component, "footprint", "") or ""),
                description=str(getattr(component, "description", "") or ""),
                pad_designators=pads,
                rotation_degrees=_component_rotation(component),
                unique_id=str(getattr(component, "unique_id", "") or ""),
                diode_candidate=bool(reason),
                diode_reason=reason,
                cathode_pad=_cathode_pad(pads),
                pin1_pad=choose_pin1_pad_designator(pads),
            )
        )
    return PcbSvgComponentInventory(
        board_key=board_key,
        pcb_path=Path(pcb_path),
        components=tuple(sorted(entries, key=lambda item: _designator_sort_key(item.designator))),
    )


def load_pcb_svg_component_inventory(
    input_file: Path,
    *,
    pcbdoc_selector: Path | str | None = None,
) -> tuple[PcbSvgComponentInventory, ...]:
    """Load component inventories for a PcbDoc/PrjPcb without invoking Geometer."""
    design, _source_tag = load_design_for_pcb_input(input_file)
    render_inputs = iter_pcb_render_inputs(design, pcbdoc_selector=pcbdoc_selector)
    return tuple(
        build_pcb_svg_component_inventory_from_pcbdoc(
            board_key=render_input.board_key,
            pcb_path=render_input.pcb_path,
            pcbdoc=render_input.pcbdoc,
        )
        for render_input in render_inputs
    )


__all__ = [
    "PcbSvgComponentInventory",
    "PcbSvgComponentInventoryEntry",
    "build_pcb_svg_component_inventory_from_pcbdoc",
    "load_pcb_svg_component_inventory",
]
