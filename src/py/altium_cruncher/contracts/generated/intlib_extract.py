"""Generated from src/tsp/altium_cruncher/outputs/commands.tsp. Do not edit."""

from __future__ import annotations

from typing import Literal, Never, NotRequired
from typing_extensions import TypedDict

IntlibExtract = TypedDict("IntlibExtract", {
    "schema": "Literal[\"altium_cruncher.extract.intlib.a0\"]",
    "source": "Source",
    "output_dir": "str",
    "component_count": "Count",
    "component_parse_error": "str | None",
    "source_count": "Count",
    "libpkg_path": "str | None",
    "sources": "list[ExtractedSource]",
}, closed=True)

Source = TypedDict("Source", {
    "path": "str",
    "name": "str",
    "stem": "str",
}, closed=True)

ExtractedSource = TypedDict("ExtractedSource", {
    "kind": "str",
    "stream_path": "str",
    "original_path": "str",
    "suggested_filename": "str",
    "output_path": "str | None",
    "output_relative_path": "str | None",
}, closed=True)

Count = int
