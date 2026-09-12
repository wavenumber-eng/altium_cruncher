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


def test_no_fast_outline_default_inserted_into_explicit_legacy_request():
    value = {"global": {"styles": {"assembly_hlr": {"projection_algorithm": "exact"}}}}
    decoded = decode_pcb_svg_config(value)
    assert "outline_algorithm" not in decoded["global"]["styles"]["assembly_hlr"]


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
