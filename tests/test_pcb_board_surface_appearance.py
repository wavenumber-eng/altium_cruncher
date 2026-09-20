"""Region-local board surface classification coverage."""

from pathlib import Path
from types import SimpleNamespace

from altium_monkey.altium_layer_stack_document import AltiumStackRegion
from altium_monkey.altium_pcbdoc import AltiumPcbDoc
from altium_monkey.altium_resolved_layer_stack import (
    ResolvedLayer,
    ResolvedStackEnvelope,
)
from altium_monkey.altium_stackupx import StackupXLayerType
import pytest

from altium_cruncher.pcb_board_surface_appearance import (
    BoardSurfaceAppearanceIndex,
    BoardSurfaceKind,
)


ROOT = Path(__file__).resolve().parents[1]
BLUETOOTH = (
    ROOT
    / "tests/assets/projects/bluetooth_sentinel_flex/input/Bluetooth_Sentinel.PcbDoc"
)


def _region() -> AltiumStackRegion:
    return AltiumStackRegion(
        name="Flex",
        layerstack_id="flex",
        outline_vertices=((0, 0), (100000, 0), (100000, 100000), (0, 100000)),
    )


def _layer(
    stack_index: int,
    name: str,
    family: str,
    thickness: float,
    *,
    material: str | None = None,
) -> ResolvedLayer:
    return ResolvedLayer(
        layer_key=f"L{stack_index}",
        display_name=name,
        stack_index=stack_index,
        thickness_mils=thickness,
        material=material,
        family=family,
        registry_ref=f"layer-{stack_index}",
        physical_row=True,
    )


class _Resolved:
    def __init__(
        self,
        layers: tuple[ResolvedLayer, ...],
        *,
        is_flex: bool = True,
    ) -> None:
        self.substack = SimpleNamespace(
            source_stackup_ref="flex",
            name="Flex",
            is_flex=is_flex,
            layers=layers,
        )

    def substack_for_board_region(self, _region: object) -> object:
        return self.substack

    def stack_envelope_for_board_region(self, _region: object) -> ResolvedStackEnvelope:
        thickness = sum(layer.thickness_mils for layer in self.substack.layers)
        return ResolvedStackEnvelope(
            source_stackup_ref="flex",
            substack_name="Flex",
            is_flex=self.substack.is_flex,
            z_zero="substack_midplane",
            total_thickness_mils=thickness,
            top_z_mils=thickness / 2,
            bottom_z_mils=-thickness / 2,
        )


def test_typed_coverlay_is_distinct_from_zero_thickness_overlay():
    layers = (
        _layer(0, "Top Overlay", "overlay", 0),
        _layer(1, "Top Coverlay", "overlay", 1.0, material="Polyimide"),
        _layer(2, "Copper", "copper", 1.4),
        _layer(3, "Core", "dielectric", 2.0, material="Polyimide"),
        _layer(4, "Bottom Copper", "copper", 1.4),
    )
    source_layers = tuple(
        SimpleNamespace(
            registry_ref=f"layer-{index}",
            stackupx_type_id=(
                StackupXLayerType.BIKINI_COVERLAY.value if index == 1 else ""
            ),
            family=family,
            dielectric_type=None,
            dielectric_height_mils=(1.0 if index == 1 else None),
            dielectric_material=("Polyimide" if index in {1, 3} else ""),
            coverlay_expansion="5mil" if index == 1 else "",
            stackupx_properties=(
                (("Material.Color", "Color", "#80D18B28"),) if index == 1 else ()
            ),
            stackupx_substack_properties=(),
        )
        for index, family in enumerate(
            ("overlay", "overlay", "copper", "dielectric", "copper")
        )
    )
    document = SimpleNamespace(
        board_regions=(_region(),),
        physical_stacks=(SimpleNamespace(layers=source_layers),),
    )

    index = BoardSurfaceAppearanceIndex.from_layer_stack_document(
        document,
        _Resolved(layers),
    )

    assert not index.invalid_regions
    appearance = index.regions[0]
    assert appearance.substrate_material == "Polyimide"
    assert appearance.top.kind is BoardSurfaceKind.COVERLAY
    assert appearance.top.material == "Polyimide"
    assert appearance.top.authored_color == "#D18B28"
    assert appearance.bottom.kind is BoardSurfaceKind.EXPOSED_COPPER


def test_flex_substack_does_not_imply_coverlay_without_a_film_row():
    layers = (
        _layer(0, "Top Copper", "copper", 1.4),
        _layer(1, "Core", "dielectric", 2.0, material="Polyimide"),
        _layer(2, "Bottom Copper", "copper", 1.4),
    )
    source_layers = tuple(
        SimpleNamespace(
            registry_ref=f"layer-{index}",
            stackupx_type_id="",
            family=family,
            dielectric_type=None,
            dielectric_height_mils=(2.0 if family == "dielectric" else None),
            dielectric_material=("Polyimide" if family == "dielectric" else ""),
            coverlay_expansion="",
            stackupx_properties=(),
            stackupx_substack_properties=(),
        )
        for index, family in enumerate(("copper", "dielectric", "copper"))
    )
    document = SimpleNamespace(
        board_regions=(_region(),),
        physical_stacks=(SimpleNamespace(layers=source_layers),),
    )

    appearance = BoardSurfaceAppearanceIndex.from_layer_stack_document(
        document,
        _Resolved(layers),
    ).regions[0]

    assert appearance.top.kind is BoardSurfaceKind.EXPOSED_COPPER
    assert appearance.bottom.kind is BoardSurfaceKind.EXPOSED_COPPER
    assert not appearance.top.has_film
    assert not appearance.bottom.has_film


def test_legacy_coverlay_fallback_requires_flex_and_film_or_positive_expansion():
    layers = (
        _layer(0, "Top Solder", "solder_mask", 1.0, material="Polyimide"),
        _layer(1, "Copper", "copper", 1.4),
    )
    source_layers = (
        SimpleNamespace(
            registry_ref="layer-0",
            stackupx_type_id="",
            family="solder_mask",
            dielectric_type=4,
            dielectric_height_mils=1.0,
            dielectric_material="Polyimide",
            coverlay_expansion="5mil",
            stackupx_properties=(),
            stackupx_substack_properties=(),
        ),
        SimpleNamespace(
            registry_ref="layer-1",
            stackupx_type_id="",
            family="copper",
            dielectric_type=None,
            dielectric_height_mils=None,
            dielectric_material="",
            coverlay_expansion="",
            stackupx_properties=(),
            stackupx_substack_properties=(),
        ),
    )
    document = SimpleNamespace(
        board_regions=(_region(),),
        physical_stacks=(SimpleNamespace(layers=source_layers),),
    )

    flex = BoardSurfaceAppearanceIndex.from_layer_stack_document(
        document,
        _Resolved(layers, is_flex=True),
    ).regions[0]
    rigid = BoardSurfaceAppearanceIndex.from_layer_stack_document(
        document,
        _Resolved(layers, is_flex=False),
    ).regions[0]

    assert flex.top.kind is BoardSurfaceKind.COVERLAY
    assert rigid.top.kind is BoardSurfaceKind.SOLDER_MASK


@pytest.mark.slow
def test_bluetooth_sentinel_has_rigid_mask_and_uncoated_flex_surfaces():
    pcbdoc = AltiumPcbDoc.from_file(BLUETOOTH)
    index = BoardSurfaceAppearanceIndex.from_pcbdoc(pcbdoc)

    assert not index.invalid_regions
    by_name = {item.region.name: item for item in index.regions}
    assert set(by_name) == {
        "Layer Stack Region 1",
        "Layer Stack Region 2",
        "Layer Stack Region 3",
    }
    for name in ("Layer Stack Region 1", "Layer Stack Region 2"):
        rigid = by_name[name]
        assert rigid.region.is_flex is False
        assert rigid.top.kind is BoardSurfaceKind.SOLDER_MASK
        assert rigid.bottom.kind is BoardSurfaceKind.SOLDER_MASK
        assert rigid.top.material == "Solder Resist"
        assert rigid.top.copper_layer_key == "L1"
        assert rigid.top.copper_layer_ref.token == "TOP"
        assert rigid.bottom.copper_layer_key == "L32"
        assert rigid.bottom.copper_layer_ref.token == "BOTTOM"
        assert rigid.substrate_material == "FR-4"

    flex = by_name["Layer Stack Region 3"]
    assert flex.region.is_flex is True
    assert flex.substrate_material == "Polyamide"
    assert flex.top.kind is BoardSurfaceKind.EXPOSED_COPPER
    assert flex.bottom.kind is BoardSurfaceKind.EXPOSED_COPPER
    assert flex.top.copper_layer_key == "L3"
    assert flex.top.copper_layer_ref.token == "MID2"
    assert flex.bottom.copper_layer_key == "L32"
    assert flex.bottom.copper_layer_ref.token == "BOTTOM"
    assert not flex.top.has_film
    assert not flex.bottom.has_film
