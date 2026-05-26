"""easyeda-footprint-review command for fixture-wide footprint import review."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from altium_cruncher.altium_cruncher_common import _resolve_output_dir
from altium_cruncher.easyeda_altium_footprint import (
    EasyEdaFootprintImportPolicy,
    build_altium_pcblib_from_easyeda_footprint,
    load_easyeda_footprint_input,
    render_easyeda_footprint_source_svg,
)
from altium_cruncher.easyeda_altium_preview import (
    make_easyeda_footprint_review_row,
    write_easyeda_footprint_review_artifacts,
)

log = logging.getLogger(__name__)


def cmd_easyeda_footprint_review(args: argparse.Namespace) -> int:
    """Generate one HTML/SVG review page for many EasyEDA footprint imports."""

    output_dir = _resolve_output_dir(args.output, "easyeda-footprint-review")
    input_paths = _collect_input_paths(args)
    if not input_paths:
        log.error("No EasyEDA JSON inputs found")
        return 1

    rows = []
    case_preview_dir = output_dir / "case-previews"
    policy = _policy_from_args(args)

    try:
        for input_path in input_paths:
            easyeda_footprint, source_data = load_easyeda_footprint_input(input_path)
            result = build_altium_pcblib_from_easyeda_footprint(
                easyeda_footprint,
                source_data=source_data,
                policy=policy,
            )
            part_id = _part_id(easyeda_footprint.info.lcsc_id, input_path)
            preview_dir = case_preview_dir / _safe_part_id(part_id)
            preview_dir.mkdir(parents=True, exist_ok=True)

            source_svg = render_easyeda_footprint_source_svg(
                easyeda_footprint,
                source_data=source_data,
            )
            altium_svg = result.library.footprints[0].to_svg()
            (preview_dir / "easyeda-footprint-source.svg").write_text(
                source_svg,
                encoding="utf-8",
            )
            (preview_dir / "altium-footprint.svg").write_text(
                altium_svg,
                encoding="utf-8",
            )

            rows.append(
                make_easyeda_footprint_review_row(
                    part_id=part_id,
                    easyeda_svg_content=source_svg,
                    altium_svg_content=altium_svg,
                    footprint_name=result.report.footprint_name,
                    source_name=input_path.name,
                    report=result.report,
                )
            )

        artifacts = write_easyeda_footprint_review_artifacts(
            rows=rows,
            output_dir=output_dir,
            title=args.title,
        )
        log.info("Generated EasyEDA footprint review HTML: %s", artifacts.html)
        log.info("Generated EasyEDA footprint review SVG: %s", artifacts.svg)
        log.info("Included %s case(s)", len(rows))
        return 0
    except Exception as exc:
        log.exception("EasyEDA footprint review generation failed: %s", exc)
        return 1


def _collect_input_paths(args: argparse.Namespace) -> list[Path]:
    paths: list[Path] = []
    if args.fixture_dir:
        for fixture_dir in args.fixture_dir:
            paths.extend(sorted(Path(fixture_dir).glob(args.pattern)))
    paths.extend(Path(path) for path in args.inputs)

    selected = _selected_parts(args.only)
    unique: dict[Path, Path] = {}
    for path in paths:
        resolved = path.resolve()
        if not resolved.exists():
            raise FileNotFoundError(f"EasyEDA JSON input not found: {path}")
        if selected and _part_id_from_path(path) not in selected:
            continue
        unique.setdefault(resolved, path)
    return list(unique.values())


def _selected_parts(value: str | None) -> set[str]:
    if not value:
        return set()
    return {_normalize_part_id(part) for part in value.split(",") if part.strip()}


def _part_id(lcsc_id: str, path: Path) -> str:
    if lcsc_id:
        return _normalize_part_id(lcsc_id)
    return _part_id_from_path(path)


def _part_id_from_path(path: Path) -> str:
    return _normalize_part_id(path.stem.split("__", 1)[0])


def _normalize_part_id(value: str) -> str:
    text = str(value or "").strip().upper()
    if text and text[0].isdigit():
        text = f"C{text}"
    return text


def _safe_part_id(value: str) -> str:
    text = _normalize_part_id(value) or "EASYEDA_PART"
    return "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in text)


def _policy_from_args(args: argparse.Namespace) -> EasyEdaFootprintImportPolicy:
    return EasyEdaFootprintImportPolicy(
        curve_approximation_segments=getattr(args, "curve_approximation_segments", 12),
        arc_approximation_max_degrees=getattr(args, "arc_approximation_max_degrees", 15.0),
        include_source_text=getattr(args, "include_source_text", False),
    )


def register_parser(subparsers):
    review_parser = subparsers.add_parser(
        "easyeda-footprint-review",
        help="generate a fixture-wide EasyEDA vs Altium footprint review",
        description=(
            "Generate one self-contained HTML and SVG review with EasyEDA footprint "
            "source on the left and generated Altium footprint output on the right."
        ),
        epilog=(
            "Examples:\n"
            "  altium_cruncher easyeda-footprint-review --fixture-dir "
            "easyeda_monkey/tests/L0_foundation/cases/api_responses --pattern C*.json\n"
            "  altium_cruncher easyeda-footprint-review C963370.json C266603.json "
            "-o output/footprint-review"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    review_parser.add_argument(
        "inputs",
        nargs="*",
        type=Path,
        help="saved EasyEDA API response or EasyEdaFootprint JSON file(s)",
    )
    review_parser.add_argument(
        "--fixture-dir",
        type=Path,
        action="append",
        help="directory of EasyEDA JSON fixtures to include",
    )
    review_parser.add_argument(
        "--pattern",
        default="*.json",
        help="glob pattern used with --fixture-dir (default: *.json)",
    )
    review_parser.add_argument(
        "--only",
        help="comma-separated LCSC IDs to include after fixture discovery",
    )
    review_parser.add_argument(
        "--title",
        default="EasyEDA to Altium Footprint Review",
        help="review page title",
    )
    review_parser.add_argument(
        "--curve-approximation-segments",
        type=int,
        default=12,
        help="segments used for Bezier curve approximation (default: 12)",
    )
    review_parser.add_argument(
        "--arc-approximation-max-degrees",
        type=float,
        default=15.0,
        help="max degrees per segment for non-circular arc approximation (default: 15)",
    )
    review_parser.add_argument(
        "--include-source-text",
        action="store_true",
        help="include supported EasyEDA footprint text objects in generated output",
    )
    review_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output directory (default: ./output/easyeda-footprint-review)",
    )
    review_parser.set_defaults(handler=cmd_easyeda_footprint_review)
    return review_parser
