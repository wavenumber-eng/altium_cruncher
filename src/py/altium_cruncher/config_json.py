"""Shared JSONC-compatible config loading helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import jsonc  # type: ignore[import-untyped]


def load_json_config(path: Path) -> Any:
    """Load a user-editable JSON/JSONC config file."""
    text = path.read_text(encoding="utf-8-sig")
    return jsonc.loads(text)


__all__ = ["load_json_config"]
