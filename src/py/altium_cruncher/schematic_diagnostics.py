"""Shared schematic font diagnostic reporting for IR and SVG consumers."""

import logging

log = logging.getLogger(__name__)


def _font_diagnostics_from_ir_payload(
    payload: dict[str, object],
) -> list[dict[str, object]]:
    render_hints = payload.get("render_hints")
    if not isinstance(render_hints, dict):
        return []
    font_resolution = render_hints.get("font_resolution")
    if not isinstance(font_resolution, dict):
        return []
    diagnostics = font_resolution.get("diagnostics")
    if not isinstance(diagnostics, list):
        return []
    return [item for item in diagnostics if isinstance(item, dict)]


def _log_font_diagnostics(diagnostics: list[dict[str, object]]) -> None:
    for diagnostic in diagnostics:
        status = str(diagnostic.get("status", "") or "")
        if status == "exact":
            continue
        requested = str(diagnostic.get("requested_family", "") or "")
        resolved = str(diagnostic.get("resolved_family", "") or "")
        source = str(diagnostic.get("source", "") or "")
        if status == "missing":
            log.warning("Font unresolved: %s; using hard fallback metrics", requested)
        elif resolved:
            label = {
                "generic_fallback": "fallback",
                "style_fallback": "style fallback",
                "substituted": "substituted",
            }.get(status, status)
            log.warning(
                "Font %s: %s -> %s (%s)",
                label,
                requested,
                resolved,
                source,
            )


def log_current_font_resolution_diagnostics() -> None:
    """Log process-local Altium Monkey font diagnostics after SVG rendering."""
    from altium_monkey.altium_font_resolver import get_font_resolution_diagnostics

    _log_font_diagnostics(
        [diagnostic.to_dict() for diagnostic in get_font_resolution_diagnostics()]
    )
