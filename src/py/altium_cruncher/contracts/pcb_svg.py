"""Presence-preserving PCB SVG config transport, separate from preset resolution."""

from copy import deepcopy
from functools import lru_cache
from importlib.resources import files
import json
from typing import cast

from .generated.pcb_svg_config import PcbSvgConfigInput
from ._runtime import decode_config


@lru_cache(maxsize=1)
def config_metadata() -> dict[str, object]:
    """Return generated config annotations for runtime defaults and JSONC help."""
    return json.loads(
        files("altium_cruncher.contracts.generated")
        .joinpath("pcb_svg_config.metadata.json")
        .read_text(encoding="utf-8")
    )


def config_default(*path: str) -> object:
    """Copy a resolved default without inserting it into an authored override."""
    value = config_metadata()["resolved-defaults"]
    for key in path:
        value = cast(dict[str, object], value)[key]
    return deepcopy(value)


def decode_pcb_svg_config(value: object) -> PcbSvgConfigInput:
    """Validate authored structure without applying defaults, coercion or merging."""
    return cast(PcbSvgConfigInput, decode_config(value, "pcb_svg_config", "pcb-svg"))


def encode_pcb_svg_config(value: PcbSvgConfigInput) -> str:
    """Serialize authored fields only; inheritance and extension data survive."""
    return json.dumps(decode_pcb_svg_config(value), ensure_ascii=False, indent=2) + "\n"
