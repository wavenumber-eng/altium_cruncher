"""Authored document-creation contracts; MCO compilation remains domain behavior."""

from copy import deepcopy
import json
from typing import cast

from ._runtime import config_metadata, decode_config
from .generated.schdoc_create_config import SchdocCreateConfigInput
from .generated.pcbdoc_create_config import PcbdocCreateConfigInput
from .generated.project_skeleton_config import ProjectSkeletonConfigInput


def creation_default(name: str) -> object:
    defaults = cast(
        dict[str, object], config_metadata("schdoc_create_config")["resolved-defaults"]
    )
    return deepcopy(defaults[name])


def creation_schema(stem: str) -> str:
    return cast(str, config_metadata(stem)["schema"])


def creation_comments(
    stem: str, *, prefix: tuple[str, ...] = (), child: bool = False
) -> dict[tuple[str, ...] | str, str]:
    comments = cast(dict[str, str], config_metadata(stem)["jsonc-comments"])
    return {
        (*prefix, *path.split(".")): text
        for path, text in comments.items()
        if not (child and path == "schema")
    }


def creation_key_comments() -> dict[str, str]:
    return deepcopy(
        cast(
            dict[str, str],
            config_metadata("pcbdoc_create_config")["jsonc-key-comments"],
        )
    )


def decode_schdoc_create_config(value: object) -> SchdocCreateConfigInput:
    return cast(
        SchdocCreateConfigInput,
        decode_config(value, "schdoc_create_config", "SchDoc create"),
    )


def decode_pcbdoc_create_config(value: object) -> PcbdocCreateConfigInput:
    return cast(
        PcbdocCreateConfigInput,
        decode_config(value, "pcbdoc_create_config", "PcbDoc create"),
    )


def decode_project_skeleton_config(value: object) -> ProjectSkeletonConfigInput:
    return cast(
        ProjectSkeletonConfigInput,
        decode_config(value, "project_skeleton_config", "Project skeleton"),
    )


def encode_schdoc_create_config(value: SchdocCreateConfigInput) -> str:
    return (
        json.dumps(decode_schdoc_create_config(value), ensure_ascii=False, indent=2)
        + "\n"
    )


def encode_pcbdoc_create_config(value: PcbdocCreateConfigInput) -> str:
    return (
        json.dumps(decode_pcbdoc_create_config(value), ensure_ascii=False, indent=2)
        + "\n"
    )


def encode_project_skeleton_config(value: ProjectSkeletonConfigInput) -> str:
    return (
        json.dumps(decode_project_skeleton_config(value), ensure_ascii=False, indent=2)
        + "\n"
    )


def creation_integer(value: object) -> object:
    """Normalize an integral JSON number for native APIs requiring Python int."""
    return int(value) if isinstance(value, float) and value.is_integer() else value
