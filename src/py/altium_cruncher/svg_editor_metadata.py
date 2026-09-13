"""SVG editor metadata helpers."""

from __future__ import annotations

import html
import re


def decorate_editor_layer(lines: list[str], token: str) -> list[str]:
    """Give a rendered top-level group a useful SVG-editor layer identity."""
    if not lines:
        return lines
    label = token.replace("_", " ").title()
    for line in lines:
        match = re.search(r'data-layer-display-name="([^"]+)"', line)
        if match:
            label = html.unescape(match.group(1))
            break
    attrs = (
        ' inkscape:groupmode="layer"'
        f' inkscape:label="{html.escape(label)}"'
        f' aria-label="{html.escape(label)}"'
    )
    decorated = list(lines)
    for index, line in enumerate(decorated):
        group_end = line.find(">", line.find("<g")) if "<g" in line else -1
        if group_end >= 0:
            decorated[index] = line[:group_end] + attrs + line[group_end:]
            break
    return decorated
