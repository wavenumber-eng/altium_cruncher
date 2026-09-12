"""Generated from src/tsp/altium_cruncher/outputs/pcb-svg-timings.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

PcbSvgTimings = TypedDict("PcbSvgTimings", {
    "schema": "Literal[\"pcb.svg.timings.a0\"]",
    "clock": "Literal[\"wall\"]",
    "workers": NotRequired["int"],
    "notes": "str",
    "model_cache": NotRequired["PcbSvgTimingsModelCacheObject | None"],
    "events": "list[PcbSvgTimingsEventsItem]",
}, closed=True)

PcbSvgTimingsModelCacheObject = TypedDict("PcbSvgTimingsModelCacheObject", {
    "directory": "str",
    "counts": "PcbSvgTimingsModelCacheObjectCounts",
    "read_seconds": "float",
    "write_seconds": "float",
}, closed=True)

PcbSvgTimingsEventsItem = TypedDict("PcbSvgTimingsEventsItem", {
    "id": "int",
    "parent_id": "int | None",
    "stage": "str",
    "command": NotRequired["str"],
    "board": NotRequired["str"],
    "variant": NotRequired["str"],
    "view": NotRequired["str"],
    "side": NotRequired["Literal[\"top\"] | Literal[\"bottom\"] | Literal[\"both\"] | Literal[\"board\"]"],
    "layer": NotRequired["str"],
    "part": NotRequired["str"],
    "cache": "Literal[\"none\"] | Literal[\"built\"] | Literal[\"hit\"] | Literal[\"assembled\"] | Literal[\"disabled\"]",
    "failed": "bool",
    "seconds": "float",
    "exclusive_seconds": "float",
}, closed=True)

PcbSvgTimingsModelCacheObjectCounts = TypedDict("PcbSvgTimingsModelCacheObjectCounts", {
    "hits": "int",
    "misses": "int",
    "writes": "int",
    "invalid": "int",
    "evictions": "int",
}, closed=True)
