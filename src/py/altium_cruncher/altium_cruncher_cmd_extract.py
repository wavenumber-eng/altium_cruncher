"""Extract command for altium_cruncher."""

import argparse
import logging
from pathlib import Path

from altium_cruncher.altium_cruncher_common import _resolve_output_dir, find_pcbdocs_in_cwd, find_prjpcb_in_cwd

log = logging.getLogger(__name__)


def _cmd_extract_pcbdoc(
    input_file: Path,
    output_dir: Path,
    *,
    split: bool,
    combined: bool,
    verbose: bool,
) -> int:
    from altium_monkey.altium_pcbdoc import AltiumPcbDoc

    log.info(f"Extracting footprints from: {input_file.name}")

    try:
        pcbdoc = AltiumPcbDoc.from_file(input_file)
        pcblib = pcbdoc.extract_pcblib(verbose=verbose)

        if combined:
            combined_path = output_dir / f"{input_file.stem}.PcbLib"
            pcblib.save(combined_path)
            log.info(f"  Created combined PcbLib: {combined_path.name}")

        if split:
            split_dir = output_dir / "split"
            results = pcblib.split(split_dir, verbose=verbose)
            log.info(f"  Created {len(results)} individual PcbLib file(s)")

        if not split and not combined:
            log.warning("No PCB outputs requested; use --split and/or --combined")

        return 0
    except Exception as exc:
        log.error(f"Error processing {input_file.name}: {exc}")
        return 1


def _extract_pcbdocs_to_output(
    pcbdoc_files: list[Path],
    output_dir: Path,
    *,
    split: bool,
    combined: bool,
    verbose: bool,
) -> tuple[int, int]:
    successful = 0
    failed = 0
    multi_board = len(pcbdoc_files) > 1

    for pcbdoc_path in pcbdoc_files:
        board_output_dir = output_dir / pcbdoc_path.stem if multi_board else output_dir
        board_output_dir.mkdir(parents=True, exist_ok=True)
        combined_path = board_output_dir / f"{pcbdoc_path.stem}.PcbLib" if combined else None
        status = _cmd_extract_pcbdoc(
            pcbdoc_path,
            board_output_dir,
            split=split,
            combined=combined,
            verbose=verbose,
        )
        if status == 0:
            successful += 1
            if combined_path is not None:
                log.info(f"  Combined PCB library: {combined_path}")
            if split:
                log.info(f"  Split PCB libraries: {board_output_dir / 'split'}")
        else:
            failed += 1
    return successful, failed


def _extract_schdocs_to_output(
    schdoc_files: list[Path],
    output_dir: Path,
    *,
    split: bool,
    combined: bool,
    debug: bool,
) -> tuple[int, int, dict[str, bool]]:
    from altium_monkey.altium_schdoc import AltiumSchDoc

    total_successful = 0
    total_failed = 0
    all_results: dict[str, bool] = {}

    for schdoc_path in schdoc_files:
        log.info(f"Extracting symbols from: {schdoc_path.name}")

        try:
            schdoc = AltiumSchDoc(schdoc_path)
            results = schdoc.extract_symbols(
                output_dir=output_dir,
                combined_schlib=combined,
                split_schlibs=split,
                debug=debug,
            )

            successful = sum(1 for value in results.values() if value)
            failed = sum(1 for value in results.values() if not value)
            total_successful += successful
            total_failed += failed

            if len(schdoc_files) > 1:
                for name, success in results.items():
                    all_results[f"{schdoc_path.stem}/{name}"] = success
            else:
                all_results.update(results)

            if combined:
                log.info(f"  Created combined SchLib: {schdoc_path.stem}.SchLib")
            if split:
                log.info(f"  Created {successful} individual SchLib files")

        except Exception as exc:
            log.error(f"Error processing {schdoc_path.name}: {exc}")
            total_failed += 1

    if total_failed > 0:
        log.warning(f"Failed to extract {total_failed} symbol(s)")

    log.info("Extracted symbols:")
    for name, success in sorted(all_results.items()):
        status = "OK" if success else "FAILED"
        log.info(f"  [{status}] {name}")

    return total_successful, total_failed, all_results


def cmd_extract(args) -> int:
    """
    Handle extract subcommand.

    Supported inputs:
    - `.SchDoc` / `.PrjPcb` -> `SchLib`
    - `.PcbDoc` -> `PcbLib`
    """
    input_file: Path | None = None

    if args.file:
        input_file = Path(args.file).resolve()
        if not input_file.exists():
            log.error(f"File not found: {input_file}")
            return 1
    else:
        input_file = find_prjpcb_in_cwd()
        if input_file is not None:
            log.info(f"Auto-detected project: {input_file.name}")
        else:
            pcbdocs = find_pcbdocs_in_cwd()
            if len(pcbdocs) == 1:
                input_file = pcbdocs[0]
                log.info(f"Auto-detected PCB: {input_file.name}")
            elif len(pcbdocs) > 1:
                log.error("No file specified and multiple .PcbDoc files found in current directory")
                log.info(
                    "Usage: altium_cruncher extract [file.SchDoc | file.PcbDoc | project.PrjPcb]"
                )
                return 1
            else:
                log.error("No file specified and no .PrjPcb or .PcbDoc found in current directory")
                log.info(
                    "Usage: altium_cruncher extract [file.SchDoc | file.PcbDoc | project.PrjPcb]"
                )
                return 1

    output_dir = _resolve_output_dir(args.output, "extract")
    split = args.split or (not args.combined)
    combined = bool(args.combined)
    debug = bool(getattr(args, "debug", False))

    log.info(f"Output directory: {output_dir}")

    suffix = input_file.suffix.lower()
    if suffix == ".pcbdoc":
        return _cmd_extract_pcbdoc(
            input_file,
            output_dir,
            split=split,
            combined=combined,
            verbose=debug,
        )

    if suffix == ".schdoc":
        successful, failed, _ = _extract_schdocs_to_output(
            [input_file],
            output_dir,
            split=split,
            combined=combined,
            debug=debug,
        )
        log.info(f"Total: {successful} successful, {failed} failed")
        return 0 if failed == 0 else 1

    if suffix == ".prjpcb":
        from altium_monkey.altium_prjpcb import AltiumPrjPcb

        project = AltiumPrjPcb(input_file)
        schdoc_files = project.get_schdoc_paths()
        pcbdoc_files = project.get_pcbdoc_paths()

        if not schdoc_files and not pcbdoc_files:
            log.error(f"No SchDoc or PcbDoc files found in project: {input_file}")
            return 1

        total_successful = 0
        total_failed = 0

        if schdoc_files:
            sch_output_dir = output_dir / "schlib"
            sch_output_dir.mkdir(parents=True, exist_ok=True)
            log.info(f"Found {len(schdoc_files)} SchDoc file(s) in project")
            log.info(f"Schematic output directory: {sch_output_dir}")
            successful, failed, _ = _extract_schdocs_to_output(
                schdoc_files,
                sch_output_dir,
                split=split,
                combined=combined,
                debug=debug,
            )
            total_successful += successful
            total_failed += failed

        if pcbdoc_files:
            pcb_output_dir = output_dir / "pcblib"
            pcb_output_dir.mkdir(parents=True, exist_ok=True)
            log.info(f"Found {len(pcbdoc_files)} PcbDoc file(s) in project")
            log.info(f"PCB output directory: {pcb_output_dir}")
            successful, failed = _extract_pcbdocs_to_output(
                pcbdoc_files,
                pcb_output_dir,
                split=split,
                combined=combined,
                verbose=debug,
            )
            total_successful += successful
            total_failed += failed

        log.info(f"Total: {total_successful} successful, {total_failed} failed")
        return 0 if total_failed == 0 else 1

    log.error(f"Unsupported file type: {suffix}")
    log.info("Supported types: .SchDoc, .PcbDoc, .PrjPcb")
    return 1


def register_parser(subparsers):
    extract_parser = subparsers.add_parser(
        "extract",
        help="extract symbols or footprints from Altium design documents",
        description=(
            "Extract embedded symbols from SchDoc/PrjPcb to SchLib files, "
            "or footprints from PcbDoc to PcbLib files."
        ),
        epilog=(
            "Examples:\n"
            "  altium_cruncher extract schematic.SchDoc\n"
            "  altium_cruncher extract board.PcbDoc\n"
            "  altium_cruncher extract project.PrjPcb\n"
            "  altium_cruncher extract                      # Auto-detect PrjPcb or single PcbDoc in CWD\n"
            "  altium_cruncher extract schematic.SchDoc -o my_symbols/\n"
            "  altium_cruncher extract board.PcbDoc --combined --split -o my_footprints/\n"
            "  altium_cruncher extract project.PrjPcb -o out/extract    # emits schlib/ and pcblib/ subfolders\n"
            "  altium_cruncher extract schematic.SchDoc --combined   # Single multi-symbol SchLib\n"
            "  altium_cruncher extract board.PcbDoc --split          # Individual PcbLib files (default)"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    extract_parser.add_argument(
        "file",
        nargs="?",
        help="SchDoc, PcbDoc, or PrjPcb file (optional if auto-detected in CWD)",
    )
    extract_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output directory (default: ./output/extract)",
    )
    extract_parser.add_argument(
        "--split",
        action="store_true",
        help="create individual SchLib/PcbLib files (default)",
    )
    extract_parser.add_argument(
        "--combined",
        action="store_true",
        help="create a single combined SchLib/PcbLib file",
    )
    extract_parser.add_argument("--debug", action="store_true", help="enable debug output")
    extract_parser.set_defaults(handler=cmd_extract)
    return extract_parser
