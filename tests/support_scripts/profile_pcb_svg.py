"""Profile the real toon/pcb-svg CLI without changing rendering or saved inputs.

Example (supply an output-local config to avoid creating one beside a fixture)::

    uv run --no-sync python \
        tests/support_scripts/profile_pcb_svg.py --report output/profiling/rt \
        -- toon board.PrjPcb --config output/profiling/toon.config \
        -o output/profiling/boards

Uses --workers 1 for synchronous attribution. Use profile_svg_workers.py for concurrency.
Use --cprofile for Python call stacks; use ordinary runs for wall-time baselines.
--repeat-views measures exact repeated views within the same renderer and checks
byte equality. It is an experiment, not a persistent application cache.
"""

from __future__ import annotations

import argparse
import cProfile
from dataclasses import dataclass
from functools import wraps
import hashlib
import inspect
from importlib.metadata import version
import json
from pathlib import Path
import platform
import pstats
import subprocess
import sys
import time
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from altium_monkey.altium_pcbdoc import AltiumPcbDoc
    from altium_monkey.altium_resolved_layer_stack import ResolvedLayerStack
    from altium_cruncher.altium_cruncher_pcb_illustration import IllustrationJob
    from altium_cruncher.altium_cruncher_pcb_svg_a0_renderer import PcbSvgA0Renderer
import weakref


@dataclass
class Frame:
    started: float
    children: float = 0.0


class Timings:
    """Nested synchronous wall timers; exclusive times do not double count."""

    def __init__(self, repeat_views: int, experiments: list[str]) -> None:
        self.repeat_views = repeat_views
        self.experiments = experiments
        self.stack: list[Frame] = []
        self.stages: dict[str, dict] = {}
        self.events: list[dict] = []
        self.jobs: dict[int, dict] = {}
        self.job_ids: weakref.WeakKeyDictionary = weakref.WeakKeyDictionary()
        self.view_ids: weakref.WeakKeyDictionary = weakref.WeakKeyDictionary()
        self.context: dict = {}

    def _record_job(self, renderer: object) -> None:
        session = renderer.component_layers
        job = session.job
        if job is None:
            return
        if job not in self.job_ids:
            self.job_ids[job] = len(self.jobs) + 1
        self.jobs[self.job_ids[job]] = {
            **job.counts,
            "layer_hits": session.layer_hits,
            "placed_layers": len(session._placed),
            "finished_layers": len(session._layers),
            "tessellation_keys": sorted(job._tessellations),
            "illustration_keys": sorted(job._illustrations),
            "warnings": list(job.warnings),
        }

    def _update_context(self, label: str, args: tuple[object, ...]) -> None:
        if label == "toon.variant":
            self.context = {"board": args[1].board_key, "variant": args[2].name}
        elif label == "svg.view":
            view = args[2]
            self.context.update(
                view=view.name,
                side="bottom" if any("BOTTOM" in t for t in view.layers) else "top",
            )

    def patch(
        self, owner: object, name: str, label: str, *, event: bool = False
    ) -> None:
        original: Callable = getattr(owner, name)

        @wraps(original)
        def measured(*args: object, **kwargs: object) -> object:
            self._update_context(label, args)
            repetitions = self.repeat_views if label == "svg.view" else 1
            first = None
            for repetition in range(repetitions):
                frame = Frame(time.perf_counter())
                self.stack.append(frame)
                failed = False
                try:
                    result = original(*args, **kwargs)
                except BaseException:
                    failed = True
                    raise
                finally:
                    self._finish_measurement(
                        frame, label, args, kwargs, repetition, failed, event
                    )
                if label == "svg.view":
                    if repetition == 0:
                        first = result
                    elif result != first:
                        raise AssertionError(
                            "Repeated SVG view differs from its first render"
                        )
            return result

        descriptor = inspect.getattr_static(owner, name)
        setattr(
            owner,
            name,
            staticmethod(measured)
            if isinstance(descriptor, staticmethod)
            else measured,
        )

    def _finish_measurement(
        self,
        frame: Frame,
        label: str,
        args: tuple[object, ...],
        kwargs: dict[str, object],
        repetition: int,
        failed: bool,
        event: bool,
    ) -> None:
        elapsed = time.perf_counter() - frame.started
        self.stack.pop()
        if self.stack:
            self.stack[-1].children += elapsed
        stage = self.stages.setdefault(
            label,
            {
                "calls": 0,
                "inclusive_s": 0.0,
                "exclusive_s": 0.0,
                "max_s": 0.0,
                "failures": 0,
            },
        )
        stage["calls"] += 1
        stage["inclusive_s"] += elapsed
        stage["exclusive_s"] += elapsed - frame.children
        stage["max_s"] = max(stage["max_s"], elapsed)
        stage["failures"] += int(failed)
        if event:
            self._record_event(label, args, kwargs, repetition, elapsed, failed)

    def _record_event(
        self,
        label: str,
        args: tuple[object, ...],
        kwargs: dict[str, object],
        repetition: int,
        elapsed: float,
        failed: bool,
    ) -> None:
        row = {
            **self.context,
            "stage": label,
            "seconds": elapsed,
            "failed": failed,
        }
        if label == "svg.view":
            renderer, pcbdoc, view = args[:3]
            if renderer not in self.view_ids:
                self.view_ids[renderer] = len(self.events) + 1
            row.update(
                view=view.name,
                renderer=self.view_ids[renderer],
                board=str(pcbdoc.filepath),
                repetition=repetition + 1,
                components=len(pcbdoc.components),
                pads=len(pcbdoc.pads),
                bodies=len(pcbdoc.component_bodies),
            )
            self._record_job(renderer)
        elif label == "components._render_native":
            row.update(
                designator=args[1].designator,
                side=kwargs.get("side"),
                meshes=len(args[1].meshes),
            )
        elif label == "svg.layer":
            row["layer"] = args[3]
        elif label == "component_layer.render":
            row["layer"] = args[4]
        elif label == "geometer.execute":
            attachments = args[3] if len(args) > 3 else kwargs.get("attachments", ())
            row.update(
                operation=args[1],
                attachment_bytes=sum(len(a.data) for a in attachments),
            )
        self.events.append(row)

    def install(self) -> None:
        import geometer
        from altium_cruncher import pcb_illustration_workflow as toon
        from altium_cruncher import altium_cruncher_pcb_svg_a0_renderer as svg
        from altium_cruncher import altium_cruncher_pcb_illustration as illustration
        from altium_cruncher.altium_cruncher_pcb_svg_component_layers import (
            ComponentLayerSession,
        )
        from altium_cruncher.altium_cruncher_pcb_svg_soldermask_film import (
            SoldermaskFilmRenderer,
        )
        from altium_cruncher.altium_cruncher_pcb_svg_substrate import (
            BoardSubstrateRenderer,
        )

        install_experiments(self.experiments)
        for owner in (toon, svg):
            for name, label in (
                ("load_design_for_pcb_input", "input.project"),
                ("iter_pcb_render_inputs", "input.boards"),
            ):
                self.patch(owner, name, label, event=True)
        self.patch(toon, "illustration_variants", "input.variants")
        self.patch(toon, "render_board", "toon.variant", event=True)
        for name in (
            "model_tessellation",
            "mesh_hlr_projection",
            "mesh_illustration",
            "execute",
            "__enter__",
            "__exit__",
        ):
            self.patch(geometer.GeometerClient, name, "geometer." + name, event=True)
        self.patch(geometer, "planar_step", "geometer.planar_step", event=True)
        for name in ("collect", "render", "_render_native", "_tessellate"):
            self.patch(
                illustration.IllustrationJob,
                name,
                "components." + name,
                event=name == "_render_native",
            )
        for name in ("_transform_mesh", "_visible_mesh", "_digest"):
            self.patch(illustration, name, "components." + name)
        self.patch(illustration.IllustrationSymbol, "group", "components.inline_symbol")
        for name in ("_materialize", "_illustrations", "_designators", "render"):
            self.patch(
                ComponentLayerSession,
                name,
                "component_layer." + name,
                event=name == "render",
            )
        for name, label in (
            ("render_view_svg", "svg.view"),
            ("_render_a0_token", "svg.layer"),
            ("_build_context", "svg.context"),
            ("_resolved_layer_stack_safe", "svg.resolve_stack"),
            ("_collect_layer_hole_masks", "svg.hole_masks"),
            ("_collect_a0_overlays", "svg.overlays"),
            ("_append_svg_metadata", "svg.metadata"),
            ("_render_a0_physical_layer", "svg.physical_layer"),
            ("_render_a0_board_cutouts", "svg.cutouts"),
            ("_render_a0_hole_group", "svg.holes"),
        ):
            self.patch(
                svg.PcbSvgA0Renderer,
                name,
                label,
                event=name in {"render_view_svg", "_render_a0_token"},
            )
        self.patch(SoldermaskFilmRenderer, "render_film", "svg.mask_film")
        self.patch(BoardSubstrateRenderer, "render_substrate", "svg.substrate")


def install_experiments(experiments: list[str]) -> None:
    """Process-local hypotheses only; production functions are never edited."""
    from altium_cruncher.altium_cruncher_pcb_illustration import IllustrationJob
    from altium_cruncher.altium_cruncher_pcb_svg_a0_renderer import PcbSvgA0Renderer

    if "variant-model-cache" in experiments:
        original_init = IllustrationJob.__init__
        tessellations: dict = {}
        illustrations: dict = {}

        def init(job: IllustrationJob, *args: object, **kwargs: object) -> None:
            original_init(job, *args, **kwargs)
            job._tessellations = tessellations
            job._illustrations = illustrations

        IllustrationJob.__init__ = init

    if "resolved-stack" in experiments:
        original_stack = PcbSvgA0Renderer._resolved_layer_stack_safe
        stack_is_static = isinstance(
            inspect.getattr_static(PcbSvgA0Renderer, "_resolved_layer_stack_safe"),
            staticmethod,
        )

        def stack(
            renderer: PcbSvgA0Renderer, pcbdoc: AltiumPcbDoc
        ) -> ResolvedLayerStack | None:
            cache = getattr(renderer, "_profile_resolved_stacks", None)
            if cache is None:
                cache = renderer._profile_resolved_stacks = {}
            key = id(pcbdoc)
            if key not in cache:
                cache[key] = (
                    pcbdoc,
                    (
                        original_stack(pcbdoc)
                        if stack_is_static
                        else original_stack(renderer, pcbdoc)
                    ),
                )
            return cache[key][1]

        PcbSvgA0Renderer._resolved_layer_stack_safe = stack


def source_fingerprint() -> dict:
    root = Path(__file__).resolve().parents[2]
    entries = {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted((root / "src/py/altium_cruncher").glob("*.py"))
    }
    return {
        "sha256": hashlib.sha256(
            json.dumps(entries, sort_keys=True).encode()
        ).hexdigest(),
        "files": entries,
    }


def output_inventory(argv: list[str]) -> list[dict]:
    directory = None
    for index, arg in enumerate(argv[:-1]):
        if arg in {"--output", "-o"}:
            directory = Path(argv[index + 1])
    if directory is None or not directory.is_dir():
        return []
    result = []
    for path in sorted(directory.rglob("*")):
        if path.suffix != ".svg":
            continue
        data = path.read_bytes()
        row = {
            "path": str(path),
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        }
        result.append(row)
    return result


def _write_cprofile(profiler: cProfile.Profile | None, report: Path) -> None:
    if profiler:
        profiler.disable()
        profiler.dump_stats(str(report.with_suffix(".prof")))
        with report.with_suffix(".pstats.txt").open("w", encoding="utf-8") as stream:
            pstats.Stats(profiler, stream=stream).strip_dirs().sort_stats(
                "cumulative"
            ).print_stats(75)
            pstats.Stats(profiler, stream=stream).strip_dirs().sort_stats(
                "tottime"
            ).print_stats(50)


def _profile_command(
    parser: argparse.ArgumentParser, raw_command: list[str]
) -> list[str]:
    command = raw_command[1:] if raw_command[:1] == ["--"] else raw_command
    if not command or command[0] not in {"toon", "pcb-svg"}:
        parser.error("Expected -- toon ... or -- pcb-svg ...")
    # Nested synchronous attribution requires serial native calls. The separate
    # worker profiler measures production concurrency without sharing this stack.
    if "--workers" not in command:
        command += ["--workers", "1"]
    elif command[command.index("--workers") + 1] != "1":
        parser.error(
            "Use --workers 1 for synchronous attribution; profile_svg_workers.py measures concurrent renders"
        )
    return command


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--report", type=Path, required=True, help="JSON/profile filename stem"
    )
    parser.add_argument("--cprofile", action="store_true")
    parser.add_argument("--repeat-views", type=int, choices=(1, 2, 3), default=1)
    parser.add_argument(
        "--experiment",
        action="append",
        default=[],
        choices=("variant-model-cache", "resolved-stack"),
    )
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = _profile_command(parser, args.command)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    profiler = cProfile.Profile() if args.cprofile else None
    timings = Timings(args.repeat_views, args.experiment)
    started = time.perf_counter()
    cpu_started = time.process_time()
    if profiler:
        profiler.enable()
    timings.install()
    from altium_cruncher._cli import main as cli_main

    imported = time.perf_counter()
    exit_code = 0
    original_argv = sys.argv
    sys.argv = ["acr", *command]
    try:
        cli_main()
    except SystemExit as error:
        exit_code = int(error.code or 0)
    except BaseException:
        exit_code = 1
        raise
    finally:
        sys.argv = original_argv
        elapsed = time.perf_counter() - started
        cpu_elapsed = time.process_time() - cpu_started
        _write_cprofile(profiler, args.report)
        git_head = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True
        ).strip()
        data = {
            "command": command,
            "exit_code": exit_code,
            "git_head": git_head,
            "versions": {
                name: version(name)
                for name in (
                    "altium-cruncher",
                    "altium-monkey",
                    "wn-geometer",
                )
            },
            "python": sys.version,
            "platform": platform.platform(),
            "profiled": bool(profiler),
            "repeat_views": args.repeat_views,
            "experiments": args.experiment,
            "source_fingerprint": source_fingerprint(),
            "wall_seconds": elapsed,
            "python_process_cpu_seconds": cpu_elapsed,
            "imports_and_instrumentation_seconds": imported - started,
            "stages": timings.stages,
            "events": timings.events,
            "jobs": timings.jobs,
            "outputs": output_inventory(command),
            "notes": [
                "Inclusive stages overlap; exclusive stages subtract measured child stages.",
                "Native API durations include IPC/serialization/wait; they are not native CPU profiles.",
                "Fresh renderer caches; OS and uv caches are uncontrolled. Profiling output is excluded from wall time.",
            ],
        }
        args.report.with_suffix(".json").write_text(
            json.dumps(data, indent=2), encoding="utf-8"
        )
        print(
            f"Profile report: {args.report.with_suffix('.json')} ({elapsed:.3f}s, exit {exit_code})"
        )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
