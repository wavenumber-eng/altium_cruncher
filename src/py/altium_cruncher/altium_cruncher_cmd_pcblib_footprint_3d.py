"""pcblib-footprint-3d command for standalone footprint preview bundles."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
import re
import webbrowser

from altium_cruncher.altium_cruncher_common import _resolve_output_dir
from altium_monkey.altium_pcblib import AltiumPcbLib

log = logging.getLogger(__name__)

DEFAULT_FOOTPRINT_PREVIEW_MARGIN_MM = 5.0
DEFAULT_FOOTPRINT_PREVIEW_THICKNESS_MM = 1.6


def cmd_pcblib_footprint_3d(args: argparse.Namespace) -> int:
    """Generate a 3D reference-board preview for one PcbLib footprint."""

    input_path = Path(args.input).resolve()
    output_dir = _resolve_output_dir(args.output, "pcblib-footprint-3d")
    try:
        from data_models.converters.altium_pcblib import (
            pcb_footprint_from_altium_pcblib,
            preview_pcb_from_footprint,
        )
        from viz.altium_pcb_workflow import compose_board_only_design_a0_payload
        from viz.three_d_viz_bundler import bundle_3d_viz_with_metrics
        from viz.three_d_viz_cli import _sidecar_payload_from_pcb_a0_design

        pcblib = AltiumPcbLib.from_file(input_path)
        footprint = pcb_footprint_from_altium_pcblib(
            pcblib,
            footprint_name=args.footprint,
            footprint_index=args.footprint_index,
            source_path=input_path,
        )
        pcb = preview_pcb_from_footprint(
            footprint,
            board_margin_mm=args.board_margin_mm,
            board_thickness_mm=args.board_thickness_mm,
            source={
                "pcblib_path": str(input_path),
                "pcblib_file": input_path.name,
                "footprint_name": footprint.name,
            },
        )

        stem = _safe_artifact_stem(f"{input_path.stem}-{footprint.name}")
        pcb_path = output_dir / f"{stem}.pcb_a0.json"
        design_path = output_dir / f"{stem}.design_a0.json"
        sidecar_path = output_dir / f"{stem}.3d-viz-sidecar.json"
        html_path = output_dir / f"{stem}.3d.html"
        manifest_path = output_dir / f"{stem}.manifest.json"

        pcb_payload = pcb.to_json()
        design_payload = compose_board_only_design_a0_payload(
            pcb_payload=pcb_payload,
            source={
                "cad": "synthetic",
                "source_kind": "pcblib_footprint_3d",
                "pcblib_file": input_path.name,
                "footprint_name": footprint.name,
            },
            metadata={
                "preview_kind": "footprint_reference_board",
                "source_footprint_id": footprint.id,
            },
            name=stem,
        )
        sidecar_payload = _sidecar_payload_from_pcb_a0_design(
            design_a0_payload=design_payload,
            render_metadata={
                "source_kind": "pcblib_footprint_3d",
                "geometry_mode": "semantic",
                "footprint": {
                    "id": footprint.id,
                    "name": footprint.name,
                    "model_status": footprint.metadata.get("model_status", ""),
                },
            },
            design_source="pcblib-footprint-3d",
        )

        _write_json(pcb_path, pcb_payload)
        _write_json(design_path, design_payload)
        _write_json(sidecar_path, sidecar_payload)
        bundle_result = bundle_3d_viz_with_metrics(
            glb_bytes=b"",
            sidecar_payload=sidecar_payload,
            output_path=html_path,
            title=args.title or f"{footprint.name} Footprint 3D Preview",
        )
        manifest = {
            "command": "pcblib-footprint-3d",
            "input": str(input_path),
            "footprint": {
                "id": footprint.id,
                "name": footprint.name,
                "pad_count": len(footprint.pads),
                "hole_count": len(footprint.holes),
                "model_count": len(footprint.models_3d),
                "model_status": footprint.metadata.get("model_status", ""),
            },
            "artifacts": {
                "pcb_a0": str(pcb_path),
                "design_a0": str(design_path),
                "sidecar": str(sidecar_path),
                "html": str(bundle_result.path),
            },
            "packaging_metrics": bundle_result.packaging_metrics,
            "timings_ms": bundle_result.timings_ms,
        }
        _write_json(manifest_path, manifest)

        log.info("Generated footprint pcb_a0: %s", pcb_path)
        log.info("Generated footprint 3D HTML: %s", bundle_result.path)
        if args.open:
            webbrowser.open(bundle_result.path.resolve().as_uri())
        return 0
    except Exception as exc:
        log.exception("PcbLib footprint 3D preview generation failed: %s", exc)
        return 1


def _write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _safe_artifact_stem(value: str) -> str:
    stem = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(value or "").strip())
    return stem.strip("._-") or "footprint"


def register_parser(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> argparse.ArgumentParser:
    preview_parser = subparsers.add_parser(
        "pcblib-footprint-3d",
        help="generate a standalone 3D preview for one Altium PcbLib footprint",
        description=(
            "Convert one Altium PcbLib footprint into generic PcbFootprint, "
            "place it on a synthetic reference PCB, and bundle the existing "
            "3D viewer as standalone HTML."
        ),
    )
    preview_parser.add_argument(
        "input",
        type=Path,
        help="Altium .PcbLib file",
    )
    preview_parser.add_argument(
        "--footprint",
        help="footprint name to select; defaults to --footprint-index",
    )
    preview_parser.add_argument(
        "--footprint-index",
        type=int,
        default=0,
        help="zero-based footprint index when --footprint is not supplied (default: 0)",
    )
    preview_parser.add_argument(
        "--board-margin-mm",
        type=float,
        default=DEFAULT_FOOTPRINT_PREVIEW_MARGIN_MM,
        help=f"reference board margin around footprint (default: {DEFAULT_FOOTPRINT_PREVIEW_MARGIN_MM})",
    )
    preview_parser.add_argument(
        "--board-thickness-mm",
        type=float,
        default=DEFAULT_FOOTPRINT_PREVIEW_THICKNESS_MM,
        help=(
            "reference board thickness "
            f"(default: {DEFAULT_FOOTPRINT_PREVIEW_THICKNESS_MM})"
        ),
    )
    preview_parser.add_argument(
        "--title",
        default="",
        help="HTML page title",
    )
    preview_parser.add_argument(
        "--open",
        action="store_true",
        help="open the generated HTML in the default browser",
    )
    preview_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output directory (default: ./output/pcblib-footprint-3d)",
    )
    preview_parser.set_defaults(handler=cmd_pcblib_footprint_3d)
    return preview_parser
