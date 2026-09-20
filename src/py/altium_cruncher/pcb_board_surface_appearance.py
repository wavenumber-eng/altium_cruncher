"""Region-local board surface semantics derived from Altium's resolved stack.

Altium Monkey owns parsing and substack resolution.  This temporary Cruncher
index joins those semantic rows to board regions so the SVG renderer can avoid
painting solder-mask film over flex regions where no such film is authored.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import re
from typing import TYPE_CHECKING, Iterable, Literal, cast

from altium_monkey.altium_stackupx import StackupXLayerType

from .pcb_board_region_envelope_index import (
    BoardRegionEnvelope,
    BoardRegionEnvelopeIndex,
    InvalidBoardRegion,
)

if TYPE_CHECKING:
    from altium_monkey.altium_pcb_layer_ref import PcbLayerRef
    from altium_monkey.altium_layer_stack_document import (
        AltiumLayerStackDocument,
        AltiumStackLayer,
    )
    from altium_monkey.altium_resolved_layer_stack import (
        ResolvedLayer,
        ResolvedLayerStack,
        ResolvedSubstack,
    )


_COLOR_RE = re.compile(r"^#(?P<digits>[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
_POSITIVE_THICKNESS_MILS = 1e-9


class BoardSurfaceKind(StrEnum):
    """Physical material presented at one side of a board region."""

    SOLDER_MASK = "solder_mask"
    COVERLAY = "coverlay"
    EXPOSED_COPPER = "exposed_copper"
    EXPOSED_SUBSTRATE = "exposed_substrate"
    UNSUPPORTED = "unsupported"


@dataclass(frozen=True)
class BoardSurfaceAppearance:
    """One region side's first positive-thickness physical row."""

    side: Literal["top", "bottom"]
    kind: BoardSurfaceKind
    layer_name: str
    layer_key: str
    material: str | None
    authored_color: str | None
    copper_layer_key: str
    copper_layer_ref: PcbLayerRef | None

    @property
    def has_film(self) -> bool:
        return self.kind in {
            BoardSurfaceKind.SOLDER_MASK,
            BoardSurfaceKind.COVERLAY,
        }


@dataclass(frozen=True)
class BoardRegionAppearance:
    """Surface and substrate facts for one valid board region."""

    region: BoardRegionEnvelope
    substrate_material: str | None
    substrate_authored_color: str | None
    top: BoardSurfaceAppearance
    bottom: BoardSurfaceAppearance

    def surface(self, side: Literal["top", "bottom"]) -> BoardSurfaceAppearance:
        return self.top if side == "top" else self.bottom


class BoardSurfaceAppearanceIndex:
    """Immutable source-aware appearance facts for all valid board regions."""

    def __init__(
        self,
        regions: Iterable[BoardRegionAppearance],
        *,
        invalid_regions: Iterable[InvalidBoardRegion] = (),
    ) -> None:
        self.regions = tuple(regions)
        self.invalid_regions = tuple(invalid_regions)

    @classmethod
    def from_pcbdoc(cls, pcbdoc: object) -> "BoardSurfaceAppearanceIndex":
        from altium_monkey.altium_layer_stack_document import AltiumLayerStackDocument

        document = AltiumLayerStackDocument.from_pcbdoc(pcbdoc)
        resolved = cast("ResolvedLayerStack", document.to_resolved_layer_stack())
        return cls.from_layer_stack_document(document, resolved)

    @classmethod
    def from_layer_stack_document(
        cls,
        document: AltiumLayerStackDocument,
        resolved: ResolvedLayerStack,
    ) -> "BoardSurfaceAppearanceIndex":
        envelope_index = BoardRegionEnvelopeIndex.from_layer_stack_document(
            document,
            resolved,
        )
        source_regions = tuple(document.board_regions or ())
        source_layers = _source_layers_by_registry_ref(document)
        appearances: list[BoardRegionAppearance] = []
        invalid = list(envelope_index.invalid_regions)

        for region in envelope_index.regions:
            source = source_regions[region.source_index]
            substack = resolved.substack_for_board_region(source)
            if substack is None or not tuple(substack.layers or ()):
                invalid.append(
                    InvalidBoardRegion(
                        source_index=region.source_index,
                        name=region.name,
                        layerstack_id=region.layerstack_id,
                        reason="region has no enabled physical substack layers",
                        bounds_mils=region.bounds_mils,
                    )
                )
                continue
            substrate_material, substrate_authored_color = _substrate_appearance(
                substack,
                source_layers,
            )
            appearances.append(
                BoardRegionAppearance(
                    region=region,
                    substrate_material=substrate_material,
                    substrate_authored_color=substrate_authored_color,
                    top=_surface_for_side(
                        substack,
                        source_layers,
                        "top",
                    ),
                    bottom=_surface_for_side(
                        substack,
                        source_layers,
                        "bottom",
                    ),
                )
            )
        return cls(appearances, invalid_regions=invalid)


def _source_layers_by_registry_ref(
    document: AltiumLayerStackDocument,
) -> dict[str, AltiumStackLayer]:
    result: dict[str, AltiumStackLayer] = {}
    for stack in tuple(document.physical_stacks or ()):
        for layer in tuple(stack.layers or ()):
            result.setdefault(str(layer.registry_ref or ""), layer)
    return result


def _surface_for_side(
    substack: ResolvedSubstack,
    source_layers: dict[str, AltiumStackLayer],
    side: Literal["top", "bottom"],
) -> BoardSurfaceAppearance:
    ordered = tuple(substack.layers or ())
    if side == "bottom":
        ordered = tuple(reversed(ordered))
    copper = _first_positive_layer(ordered, family="copper")
    layer = _first_positive_layer(ordered)
    copper_key, copper_ref = _copper_identity(copper)
    if layer is None:
        return BoardSurfaceAppearance(
            side=side,
            kind=BoardSurfaceKind.UNSUPPORTED,
            layer_name="",
            layer_key="",
            material=None,
            authored_color=None,
            copper_layer_key=copper_key,
            copper_layer_ref=copper_ref,
        )
    source = source_layers.get(str(layer.registry_ref or ""))
    return BoardSurfaceAppearance(
        side=side,
        kind=_surface_kind(layer, source, is_flex=substack.is_flex is True),
        layer_name=str(layer.display_name or ""),
        layer_key=str(layer.layer_key or ""),
        material=_material_name(layer, source),
        authored_color=_authored_color(source, substack.source_stackup_ref),
        copper_layer_key=copper_key,
        copper_layer_ref=copper_ref,
    )


def _first_positive_layer(
    layers: tuple[ResolvedLayer, ...],
    *,
    family: str | None = None,
) -> ResolvedLayer | None:
    for layer in layers:
        if float(layer.thickness_mils or 0.0) <= _POSITIVE_THICKNESS_MILS:
            continue
        if family is None or str(layer.family or "").strip().lower() == family:
            return layer
    return None


def _copper_identity(
    layer: ResolvedLayer | None,
) -> tuple[str, PcbLayerRef | None]:
    if layer is None:
        return "", None
    return str(layer.layer_key or ""), layer.layer_ref


def _surface_kind(
    layer: ResolvedLayer,
    source: AltiumStackLayer | None,
    *,
    is_flex: bool,
) -> BoardSurfaceKind:
    family = str(layer.family or "").strip().lower()
    if _is_coverlay(source, is_flex=is_flex):
        return BoardSurfaceKind.COVERLAY
    if family == "solder_mask":
        return BoardSurfaceKind.SOLDER_MASK
    if family in {"copper", "surface_finish", "plating"}:
        return BoardSurfaceKind.EXPOSED_COPPER
    if family in {"dielectric", "adhesive", "stiffener"}:
        return BoardSurfaceKind.EXPOSED_SUBSTRATE
    return BoardSurfaceKind.UNSUPPORTED


def _is_coverlay(source: AltiumStackLayer | None, *, is_flex: bool) -> bool:
    if source is None:
        return False
    type_id = str(source.stackupx_type_id or "").strip().strip("{}").casefold()
    if type_id == StackupXLayerType.BIKINI_COVERLAY.value.casefold():
        return True
    if not is_flex or str(source.family or "").strip().lower() not in {
        "overlay",
        "solder_mask",
    }:
        return False
    # This is the AD26 V7 import fallback when no StackupX TypeId was persisted.
    # A normal overlay or solder-mask row is not coverlay merely because the
    # substack is flex.
    return source.dielectric_type == 4 or _positive_length_token(
        source.coverlay_expansion
    )


def _positive_length_token(value: str) -> bool:
    token = str(value or "").strip().lower()
    match = re.match(r"^([+-]?(?:\d+(?:\.\d*)?|\.\d+))", token)
    return match is not None and float(match.group(1)) > 0.0


def _material_name(
    layer: ResolvedLayer,
    source: AltiumStackLayer | None,
) -> str | None:
    value = str(layer.material or "").strip()
    if not value and source is not None:
        value = str(source.dielectric_material or "").strip()
    return value or None


def _substrate_appearance(
    substack: ResolvedSubstack,
    source_layers: dict[str, AltiumStackLayer],
) -> tuple[str | None, str | None]:
    for layer in tuple(substack.layers or ()):
        if str(layer.family or "").strip().lower() != "dielectric":
            continue
        material = str(layer.material or "").strip()
        source = source_layers.get(str(layer.registry_ref or ""))
        color = _authored_color(source, substack.source_stackup_ref)
        if material or color:
            return material or None, color
    return None, None


def _authored_color(
    source: AltiumStackLayer | None,
    source_stackup_ref: str,
) -> str | None:
    if source is None:
        return None
    for name, _type_name, value in _color_properties(source, source_stackup_ref):
        if str(name or "").strip().casefold() in {
            "material.color",
            "materialcolor",
        }:
            color = _normalize_authored_color(value)
            if color is not None:
                return color
    return None


def _color_properties(
    source: AltiumStackLayer,
    source_stackup_ref: str,
) -> list[tuple[str, str, str]]:
    properties = list(source.stackupx_properties or ())
    normalized_ref = str(source_stackup_ref or "").strip().strip("{}").casefold()
    for ref, values in tuple(source.stackupx_substack_properties or ()):
        if str(ref or "").strip().strip("{}").casefold() == normalized_ref:
            return [*values, *properties]
    return properties


def _normalize_authored_color(value: object) -> str | None:
    match = _COLOR_RE.match(str(value or "").strip())
    if match is None:
        return None
    digits = match.group("digits")
    # WPF persists #AARRGGBB. SVG accepts #RRGGBB, while film opacity is a
    # separate public style and therefore remains independently controlled.
    if len(digits) == 8:
        digits = digits[2:]
    return f"#{digits.upper()}"


__all__ = [
    "BoardRegionAppearance",
    "BoardSurfaceAppearance",
    "BoardSurfaceAppearanceIndex",
    "BoardSurfaceKind",
]
