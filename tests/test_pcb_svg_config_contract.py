"""Authored config presence and shared Python/browser structural vectors."""

from copy import deepcopy
import json
from pathlib import Path

import pytest

from altium_cruncher.contracts.pcb_svg import (
    decode_pcb_svg_config,
    encode_pcb_svg_config,
)
from altium_cruncher.altium_cruncher_pcb_svg_config import PcbSvgConfig
from altium_cruncher.pcb_illustration_config import resolve_illustration_config

VECTORS = json.loads(
    (Path(__file__).parent / "fixtures/pcb-svg-config-vectors.json").read_text()
)
CONTRACTS = Path(__file__).parents[1] / "docs" / "contracts"


@pytest.mark.parametrize("vector", VECTORS, ids=lambda v: v["name"])
def test_config_wire_vector(vector):
    value = deepcopy(vector["value"])
    if not vector["valid"]:
        with pytest.raises(ValueError):
            decode_pcb_svg_config(value)
        return
    decoded = decode_pcb_svg_config(value)
    assert decoded == value == vector["value"]
    assert decoded is not value
    assert json.loads(encode_pcb_svg_config(decoded)) == value
    # The retained behavior adapter must accept every structurally valid fixture.
    PcbSvgConfig.from_dict(decoded)


def test_codec_preserves_inheritance_before_preset_resolution():
    authored = decode_pcb_svg_config(
        {"global": {"styles": {"soldermask_film": {"opacity": 0.5}}}}
    )
    resolved = resolve_illustration_config(authored)
    assert len(resolved.enabled_views()) == 2
    assert authored == {"global": {"styles": {"soldermask_film": {"opacity": 0.5}}}}
    assert resolved.global_options.styles["soldermask_film"]["opacity"] == 0.5
    reset = resolve_illustration_config(
        decode_pcb_svg_config({"global": {"styles": None}})
    )
    assert reset.global_options.styles["soldermask_film"]["opacity"] == 1.0


def test_a0_is_accepted_as_an_additive_predecessor_and_resolves_to_a1():
    authored = decode_pcb_svg_config(
        {
            "schema": "pcb.svg.config.a0",
            "global": {"styles": {"board_substrate": {"color": "#123456"}}},
        }
    )

    resolved = PcbSvgConfig.from_dict(authored)

    assert authored["schema"] == "pcb.svg.config.a0"
    assert resolved.schema == "pcb.svg.config.a1"
    assert resolved.global_options.styles["board_substrate"]["color"] == "#123456"


def test_a0_schema_stays_frozen_while_a1_owns_additive_surface_fields():
    a0 = json.loads((CONTRACTS / "pcb_svg_config.a0.schema.json").read_text())
    a1 = json.loads((CONTRACTS / "pcb_svg_config.a1.schema.json").read_text())

    assert a0["$id"] == "pcb_svg_config.a0.schema.json"
    assert a1["$id"] == "pcb_svg_config.a1.schema.json"
    assert set(a0["$defs"]["BoardSubstrateStyleA0"]["properties"]) == {
        "enabled",
        "color",
    }
    assert "bend_lines" not in a0["$defs"]["StyleTableA0"]["properties"]
    assert "silkscreen_surface" not in a0["$defs"]["StyleTableA0"]["properties"]
    assert "BEND_LINES" not in json.dumps(a0["$defs"]["LayerOutputOptionsA0"])
    assert "SURFACE_COPPER_TOP" not in json.dumps(
        a0["$defs"]["LayerOutputOptionsA0"]
    )
    assert "rigid_color" in a1["$defs"]["BoardSubstrateStyle"]["properties"]
    assert "bend_lines" in a1["$defs"]["StyleTable"]["properties"]
    assert "silkscreen_surface" in a1["$defs"]["StyleTable"]["properties"]


def test_issue67_explicit_colors_override_additive_regional_fallbacks():
    resolved = resolve_illustration_config(
        decode_pcb_svg_config(
            {
                "schema": "pcb.svg.config.a1",
                "global": {
                    "styles": {
                        "board_substrate": {
                            "color": "#102030",
                            "rigid_color": "#405060",
                            "flex_color": "#708090",
                        },
                        "soldermask_film": {
                            "color": "#112233",
                            "coverlay_color": "#445566",
                        },
                    }
                },
            }
        )
    )

    assert resolved.schema == "pcb.svg.config.a1"
    assert resolved.global_options.styles["board_substrate"] == {
        "enabled": True,
        "color": "#102030",
        "rigid_color": "#405060",
        "flex_color": "#708090",
    }
    assert resolved.global_options.styles["soldermask_film"] == {
        "enabled": True,
        "color": "#112233",
        "coverlay_color": "#445566",
        "opacity": 0.75,
    }


def test_no_fast_outline_default_inserted_into_explicit_legacy_request():
    value = {"global": {"styles": {"assembly_hlr": {"projection_algorithm": "exact"}}}}
    decoded = decode_pcb_svg_config(value)
    assert "outline_algorithm" not in decoded["global"]["styles"]["assembly_hlr"]


def test_silkscreen_surface_clip_mode_defaults_to_compatibility_none():
    config = PcbSvgConfig.default()
    assert config.global_options.styles["silkscreen_surface"]["clip_mode"] == "none"
    toon = resolve_illustration_config()
    assert toon.global_options.styles["silkscreen_surface"]["clip_mode"] == "film"
    with pytest.raises(ValueError):
        decode_pcb_svg_config(
            {"global": {"styles": {"silkscreen_surface": {"clip_mode": "invalid"}}}}
        )


def test_nonfinite_extension_values_fail_instead_of_changing_on_save():
    with pytest.raises(ValueError, match="finite JSON"):
        decode_pcb_svg_config(
            {"global": {"styles": {"custom": {"value": float("nan")}}}}
        )


@pytest.mark.parametrize("value", [(1, 2), {1: "numeric", "1": "string"}])
def test_non_json_extension_values_are_rejected(value):
    with pytest.raises(ValueError):
        decode_pcb_svg_config({"global": {"styles": {"custom": {"value": value}}}})


def test_generated_python_record_and_optional_field_types():
    from typing import get_args, get_origin
    from altium_cruncher.contracts.generated.pcb_svg_config import (
        ComponentOverride,
        PcbSvgConfigInput,
        RecordComponentOverride,
    )

    assert get_origin(RecordComponentOverride) is dict
    assert get_args(RecordComponentOverride) == (str, ComponentOverride)
    assert not PcbSvgConfigInput.__required_keys__
    assert "show_designator" in ComponentOverride.__optional_keys__
