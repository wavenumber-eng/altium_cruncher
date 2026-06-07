"""Run Altium OutJob files through the altium-monkey launcher."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

from altium_monkey.altium_outjob_runner import AltiumOutJobRunner, OutJobRunResult
from altium_monkey.altium_prjpcb import AltiumPrjPcb

from altium_cruncher.altium_cruncher_common import find_prjpcbs_in_cwd

OUTJOB_RUN_SCHEMA = "altium_cruncher.outjob.run.a0"
_AD_MAJOR_RE = re.compile(r"^(?:AD)?(?P<major>\d+)", re.IGNORECASE)


class OutJobCommandError(ValueError):
    """Raised when the outjob command cannot resolve a project or job."""


def cmd_outjob(args: argparse.Namespace) -> int:
    """Dispatch OutJob subcommands."""
    action = getattr(args, "outjob_action", None)
    if action == "run":
        return _cmd_outjob_run(args)
    print("No outjob subcommand specified; use `outjob run`.", file=sys.stderr)
    return 1


def _cmd_outjob_run(args: argparse.Namespace) -> int:
    try:
        _ensure_windows_runtime()
        project_path, outjob_paths = _resolve_run_inputs(args)
        results = _run_outjobs(args, project_path, outjob_paths)
    except Exception as exc:
        print(f"outjob run failed: {exc}", file=sys.stderr)
        return 1

    payload = _build_run_payload(project_path, results)
    if getattr(args, "json", False):
        print(json.dumps(payload, indent=2))
        return 0 if payload["success"] else 1

    _print_run_summary(results)
    return 0 if payload["success"] else 1


def _resolve_run_inputs(args: argparse.Namespace) -> tuple[Path, list[Path]]:
    project_arg = getattr(args, "project", None)
    target_arg = getattr(args, "target", None)
    trailing_outjobs = [Path(value) for value in getattr(args, "outjobs", [])]

    if project_arg is not None:
        project_path = _resolve_project_path(Path(project_arg))
        explicit_outjobs = []
        if target_arg is not None:
            explicit_outjobs.append(Path(target_arg))
        explicit_outjobs.extend(trailing_outjobs)
    elif target_arg is None:
        project_path = _find_single_project_in_cwd()
        explicit_outjobs = []
    else:
        target_path = Path(target_arg)
        if target_path.suffix.lower() == ".prjpcb":
            project_path = _resolve_project_path(target_path)
            explicit_outjobs = trailing_outjobs
        else:
            project_path = _find_single_project_in_cwd()
            explicit_outjobs = [target_path, *trailing_outjobs]

    project = AltiumPrjPcb(project_path)
    if explicit_outjobs:
        outjobs = [_resolve_explicit_outjob(project, outjob) for outjob in explicit_outjobs]
    else:
        outjobs = project.get_outjob_paths()
        if not outjobs:
            raise OutJobCommandError(
                f"No .OutJob files are referenced by project: {project_path}"
            )
    return project_path, _dedupe_paths(outjobs)


def _resolve_explicit_outjob(project: AltiumPrjPcb, outjob: Path) -> Path:
    if project.filepath is None:
        raise OutJobCommandError("Project has no filepath context")
    if outjob.is_absolute() or outjob.parent != Path("."):
        candidates = [outjob.resolve(), (project.filepath.parent / outjob).resolve()]
        for candidate in candidates:
            if candidate.is_file():
                return candidate
        raise FileNotFoundError(f"OutJob not found: {outjob}")
    return project.outjob(outjob).path


def _resolve_project_path(path: Path) -> Path:
    project = path.resolve()
    if project.suffix.lower() != ".prjpcb":
        raise OutJobCommandError(f"Expected a .PrjPcb project, got: {project}")
    if not project.is_file():
        raise FileNotFoundError(f"Project not found: {project}")
    return project


def _find_single_project_in_cwd() -> Path:
    projects = [project.resolve() for project in find_prjpcbs_in_cwd()]
    if len(projects) == 1:
        return projects[0]
    if not projects:
        raise OutJobCommandError(
            "No .PrjPcb file found in the current directory; pass a project explicitly."
        )
    project_list = "\n".join(f"  {project.name}" for project in projects)
    raise OutJobCommandError(
        "Multiple .PrjPcb files found in the current directory; pass one explicitly "
        f"or use --project with an OutJob:\n{project_list}"
    )


def _dedupe_paths(paths: list[Path]) -> list[Path]:
    seen: set[str] = set()
    deduped: list[Path] = []
    for path in paths:
        resolved = path.resolve()
        key = str(resolved).lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(resolved)
    return deduped


def _run_outjobs(
    args: argparse.Namespace,
    project_path: Path,
    outjob_paths: list[Path],
) -> list[OutJobRunResult]:
    runner = AltiumOutJobRunner(preferred_version=_parse_ad_major(args.ad_version))
    bind_pcbdoc_path = _resolve_bind_pcbdoc(project_path, args)
    results: list[OutJobRunResult] = []
    for outjob_path in outjob_paths:
        if not getattr(args, "json", False):
            print(f"Running {outjob_path.name}...")
        result = _run_one_outjob(
            runner,
            project_path=project_path,
            outjob_path=outjob_path,
            timeout_seconds=float(args.timeout),
            normalize_generated_paths=not bool(args.no_normalize_generated_paths),
            default_generated_output_path=args.default_generated_output_path,
            bind_pcbdoc_path=bind_pcbdoc_path,
            stage_outjob_copy=bool(args.stage_outjob_copy),
            script_directory=args.script_directory,
            keep_script_artifacts=bool(args.keep_script_artifacts),
        )
        results.append(result)
        if bool(args.stop_on_error) and not result.success:
            break
    return results


def _ensure_windows_runtime() -> None:
    if sys.platform != "win32":
        raise OutJobCommandError(
            "outjob run requires Windows with Altium Designer installed."
        )


def _resolve_bind_pcbdoc(project_path: Path, args: argparse.Namespace) -> Path | None:
    explicit = getattr(args, "bind_pcbdoc", None)
    if explicit is not None:
        return _resolve_pcbdoc_path(project_path, Path(explicit))
    if not bool(getattr(args, "auto_bind_pcbdoc", True)):
        return None

    pcbdocs = AltiumPrjPcb(project_path).get_pcbdoc_paths()
    if len(pcbdocs) == 1:
        return pcbdocs[0]
    if not pcbdocs:
        return None
    names = "\n".join(f"  {path.name}" for path in pcbdocs)
    raise OutJobCommandError(
        "Project contains multiple .PcbDoc files; use --bind-pcbdoc to select "
        f"one or --no-auto-bind-pcbdoc to keep OutJob DocumentPath tokens:\n{names}"
    )


def _resolve_pcbdoc_path(project_path: Path, pcbdoc_path: Path) -> Path:
    candidates = [pcbdoc_path]
    if not pcbdoc_path.is_absolute():
        candidates.append(project_path.parent / pcbdoc_path)
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved.is_file():
            return resolved
    raise FileNotFoundError(f"Bind .PcbDoc not found: {pcbdoc_path}")


def _run_one_outjob(
    runner: AltiumOutJobRunner,
    *,
    project_path: Path,
    outjob_path: Path,
    timeout_seconds: float,
    normalize_generated_paths: bool,
    default_generated_output_path: str | None,
    bind_pcbdoc_path: Path | None,
    stage_outjob_copy: bool,
    script_directory: Path | None,
    keep_script_artifacts: bool,
) -> OutJobRunResult:
    original_bytes = None if stage_outjob_copy else outjob_path.read_bytes()
    try:
        return runner.run(
            project_path,
            outjob_path=outjob_path,
            timeout_seconds=timeout_seconds,
            normalize_generated_paths=normalize_generated_paths,
            default_generated_output_path=default_generated_output_path,
            bind_pcbdoc_path=bind_pcbdoc_path,
            auto_bind_pcbdoc=False,
            stage_outjob_copy=stage_outjob_copy,
            script_directory=script_directory,
            keep_script_artifacts=keep_script_artifacts,
        )
    finally:
        if original_bytes is not None and outjob_path.exists():
            if outjob_path.read_bytes() != original_bytes:
                outjob_path.write_bytes(original_bytes)


def _parse_ad_major(value: str | None) -> int | None:
    if value is None or not str(value).strip():
        return None
    match = _AD_MAJOR_RE.match(str(value).strip())
    if match is None:
        raise OutJobCommandError(
            f"Could not parse --ad-version value {value!r}; use AD25, AD26, 25, or 26."
        )
    return int(match.group("major"))


def _build_run_payload(
    project_path: Path,
    results: list[OutJobRunResult],
) -> dict[str, object]:
    return {
        "schema": OUTJOB_RUN_SCHEMA,
        "project": str(project_path),
        "success": all(result.success for result in results),
        "results": [_result_to_dict(result) for result in results],
    }


def _result_to_dict(result: OutJobRunResult) -> dict[str, object]:
    return {
        "project": str(result.project_path),
        "outjob": str(result.outjob_path),
        "success": result.success,
        "launch_code": result.launch_code,
        "timed_out": result.timed_out,
        "error_count": result.error_count,
        "marker_text": result.marker_text,
        "normalized_changed": result.normalized_changed,
        "rebound_document_paths": result.rebound_document_paths,
        "marker_path": str(result.marker_path),
        "log_path": str(result.log_path),
    }


def _print_run_summary(results: list[OutJobRunResult]) -> None:
    for result in results:
        if result.success:
            state = "ok"
        elif result.timed_out:
            state = "timed out"
        else:
            state = f"failed ({result.error_count} errors)"
        changed = " normalized" if result.normalized_changed else ""
        rebound = (
            f" rebound={result.rebound_document_paths}"
            if result.rebound_document_paths
            else ""
        )
        print(f"{state}: {result.outjob_path.name}{changed}{rebound}")


def register_parser(
    subparsers: argparse._SubParsersAction,
) -> argparse.ArgumentParser:
    """Register the outjob command parser."""
    parser = subparsers.add_parser(
        "outjob",
        help="run Altium OutJob files through Altium Designer",
        description=(
            "Run project OutJob files through altium-monkey's Altium launcher. "
            "The runner generates a temporary Pascal script project and calls "
            "Altium's GenerateReport action."
        ),
    )
    action_subparsers = parser.add_subparsers(
        dest="outjob_action",
        metavar="<outjob-action>",
    )

    run_parser = action_subparsers.add_parser(
        "run",
        help="run one or more OutJob files",
        description=(
            "Run OutJobs for a project. With no arguments, the command "
            "auto-detects exactly one .PrjPcb in the current directory and runs "
            "all .OutJob files referenced by that project."
        ),
    )
    run_parser.add_argument(
        "target",
        nargs="?",
        help=(
            "optional .PrjPcb project or .OutJob/name; if an OutJob is provided "
            "without --project, one local .PrjPcb must be auto-detectable"
        ),
    )
    run_parser.add_argument(
        "outjobs",
        nargs="*",
        help="optional additional .OutJob paths or names when target is a project",
    )
    run_parser.add_argument(
        "--project",
        type=Path,
        help="project to use when running explicit OutJob paths or names",
    )
    run_parser.add_argument(
        "--ad-version",
        "--series",
        dest="ad_version",
        help="Altium major series to use, for example AD25, AD26, 25, or 26",
    )
    run_parser.add_argument(
        "--timeout",
        type=float,
        default=300.0,
        help="seconds to wait for each OutJob completion marker (default: 300)",
    )
    run_parser.add_argument(
        "--default-generated-output-path",
        help="relative fallback path for GeneratedFiles output locations",
    )
    run_parser.add_argument(
        "--bind-pcbdoc",
        type=Path,
        help="explicit .PcbDoc to bind into embedded OutJob DocumentPath tokens",
    )
    run_parser.add_argument(
        "--auto-bind-pcbdoc",
        dest="auto_bind_pcbdoc",
        action="store_true",
        default=True,
        help=(
            "auto-bind the project's single PcbDoc into embedded OutJob "
            "DocumentPath tokens (default)"
        ),
    )
    run_parser.add_argument(
        "--no-auto-bind-pcbdoc",
        dest="auto_bind_pcbdoc",
        action="store_false",
        help="keep embedded OutJob DocumentPath tokens unchanged",
    )
    run_parser.add_argument(
        "--stage-outjob-copy",
        action="store_true",
        help=(
            "run a temporary OutJob copy instead of the project-registered file; "
            "normally disabled because Altium output batches are project-sensitive"
        ),
    )
    run_parser.add_argument(
        "--no-normalize-generated-paths",
        action="store_true",
        help="skip GeneratedFiles path normalization before running",
    )
    run_parser.add_argument(
        "--script-directory",
        type=Path,
        help="directory for temporary Pascal script artifacts",
    )
    run_parser.add_argument(
        "--keep-script-artifacts",
        action="store_true",
        help="keep generated .pas/.PrjScr marker and log files for inspection",
    )
    run_parser.add_argument(
        "--stop-on-error",
        action="store_true",
        help="stop after the first failed OutJob in a batch",
    )
    run_parser.add_argument(
        "--json",
        action="store_true",
        help="write machine-readable run results JSON",
    )
    run_parser.set_defaults(handler=cmd_outjob)

    parser.set_defaults(handler=cmd_outjob)
    return parser
