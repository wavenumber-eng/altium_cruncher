"""Internal EasyEDA fixture-wide schematic import review helper."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from altium_cruncher.altium_cruncher_common import _resolve_output_dir
from altium_cruncher.easyeda_altium_preview import (
    make_easyeda_review_row,
    render_altium_library_preview_svgs,
    write_easyeda_review_artifacts,
)
from altium_cruncher.easyeda_altium_symbol import (
    EasyEdaSchematicImportPolicy,
    build_altium_schlib_from_easyeda_symbol,
    load_easyeda_symbol_input,
)

log = logging.getLogger(__name__)


def cmd_easyeda_review(args: argparse.Namespace) -> int:
    """Generate one HTML/SVG review page for many EasyEDA schematic imports."""

    output_dir = _resolve_output_dir(args.output, "easyeda-review")
    input_paths = _collect_input_paths(args)
    if not input_paths:
        log.error("No EasyEDA JSON inputs found")
        return 1

    rows = []
    case_preview_dir = output_dir / "case-previews"
    policy = _policy_from_args(args)

    try:
        for input_path in input_paths:
            easyeda_symbol, source_data = load_easyeda_symbol_input(input_path)
            result = build_altium_schlib_from_easyeda_symbol(
                easyeda_symbol,
                source_data=source_data,
                policy=policy,
            )
            part_id = _part_id(easyeda_symbol.info.lcsc_id, input_path)
            preview_dir = case_preview_dir / _safe_part_id(part_id)
            preview_dir.mkdir(parents=True, exist_ok=True)
            svg_dict = render_altium_library_preview_svgs(
                library=result.library,
                output_dir=preview_dir,
                background="none",
                pin_text_follows_orientation=_preview_pin_text_follows_orientation(policy),
            )
            altium_svg_content = _first_svg_content(svg_dict)
            if not altium_svg_content:
                raise RuntimeError(f"No Altium SVG generated for {input_path}")

            rows.append(
                make_easyeda_review_row(
                    part_id=part_id,
                    easyeda_symbol=easyeda_symbol,
                    altium_svg_content=altium_svg_content,
                    symbol_name=result.report.symbol_name,
                    source_name=input_path.name,
                    report=result.report,
                )
            )

        artifacts = write_easyeda_review_artifacts(
            rows=rows,
            output_dir=output_dir,
            title=args.title,
        )
        log.info("Generated EasyEDA review HTML: %s", artifacts.html)
        log.info("Generated EasyEDA review SVG: %s", artifacts.svg)
        log.info("Included %s case(s)", len(rows))
        return 0
    except Exception as exc:
        log.exception("EasyEDA review generation failed: %s", exc)
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


def _first_svg_content(svg_dict: dict[str, dict[int, str]]) -> str | None:
    for parts in svg_dict.values():
        for svg in parts.values():
            return svg
    return None


def _policy_from_args(args: argparse.Namespace) -> EasyEdaSchematicImportPolicy:
    return EasyEdaSchematicImportPolicy(
        hotspot_grid_mils=getattr(args, "pin_grid_mils", 100.0),
        align_hotspots_to_grid=not getattr(args, "no_align_pin_grid", False),
        use_source_pin_electrical=getattr(args, "use_source_pin_electrical", False),
        use_source_pin_ieee_symbols=getattr(args, "use_source_pin_ieee_symbols", False),
        pin_name_visibility=getattr(args, "pin_name_visibility", "source"),
        pin_designator_visibility=getattr(args, "pin_designator_visibility", "source"),
        pin_text_orientation=getattr(args, "pin_text_orientation", "default"),
        rotate_vertical_pin_text=getattr(args, "rotate_vertical_pin_text", False),
    )


def _preview_pin_text_follows_orientation(policy: EasyEdaSchematicImportPolicy) -> bool:
    return (
        policy.rotate_vertical_pin_text
        or policy.pin_text_orientation.strip().lower() in {"source", "vertical"}
    )
