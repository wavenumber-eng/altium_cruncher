"""Generated workflow transport with handwritten domain resolution adapters."""

from copy import deepcopy
from typing import cast

from ._runtime import config_metadata, decode_config
from .generated.bom_pnp_config import BomPnpConfigInput
from .generated.clean_config import CleanConfigInput
from .generated.mate_config import MateConfigInput
from .generated.pcb_layer_step_config import PcbLayerStepConfigInput


def workflow_metadata(stem: str, key: str) -> object:
    """Return owned defaults/help without exposing the cached metadata object."""
    return deepcopy(config_metadata(stem)[key])


def workflow_comments(stem: str) -> dict[tuple[str, ...], str | list[str]]:
    return {tuple(k.split(".")): v for k, v in cast(dict[str, str | list[str]], workflow_metadata(stem, "jsonc-comments")).items()}


def domain_default(stem: str, model: str, field: str) -> object:
    """Read an adapter default independently of the first-run template."""
    defaults = cast(dict[str, dict[str, object]], config_metadata(stem)["domain-model-defaults"])
    return deepcopy(defaults[model][field])


def decode_bom_pnp_config(value: object) -> BomPnpConfigInput:
    return cast(BomPnpConfigInput, decode_config(value, "bom_pnp_config", "BOM/PnP"))


def decode_clean_config(value: object) -> CleanConfigInput:
    return cast(CleanConfigInput, decode_config(value, "clean_config", "Clean"))


def decode_mate_config(value: object) -> MateConfigInput:
    return cast(MateConfigInput, decode_config(value, "mate_config", "Mate"))


def decode_pcb_layer_step_config(value: object) -> PcbLayerStepConfigInput:
    return cast(PcbLayerStepConfigInput, decode_config(value, "pcb_layer_step_config", "PCB layer STEP"))
