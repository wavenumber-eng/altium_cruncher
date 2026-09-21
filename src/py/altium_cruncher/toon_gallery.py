"""Toon adapter for the reusable SVG review gallery."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .svg_review_gallery import SvgReviewItem, write_svg_review_gallery


@dataclass(frozen=True, slots=True)
class _ToonGalleryArtifact:
    """Describe one SVG emitted by the current Toon render."""

    path: Path
    project: str
    board: str
    variant: str | None
    view: str
    side: str


def write_toon_gallery(
    output_dir: Path,
    artifacts: list[_ToonGalleryArtifact],
) -> Path:
    """Write the current Toon artifacts with the reusable review experience."""
    items = [
        SvgReviewItem(
            path=artifact.path,
            title=f"{artifact.view} · {artifact.side.title()}",
            group=(
                f"{artifact.project} · {artifact.board} · {artifact.variant or 'Base'}"
            ),
        )
        for artifact in artifacts
    ]
    return write_svg_review_gallery(
        output_dir,
        items,
        title="Toon SVG gallery",
        introduction=(
            "Select a preview to inspect the original SVG with vector-native pan and zoom. "
            "Bottom views are seen from underneath."
        ),
    )


__all__ = ["write_toon_gallery"]
