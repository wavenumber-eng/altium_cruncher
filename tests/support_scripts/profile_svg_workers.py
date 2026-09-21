"""Measure the production whole-board SVG CLI with a chosen worker count.

Run with uv --with psutil to sample aggregate parent/child RSS, CPU and threads.
Example: python tests/support_scripts/profile_svg_workers.py --workers 2
    --report output/profiling/workers-2.json -- toon board.PrjPcb
    --config output/profiling/toon.config -o output/profiling/board

SVG-only; disk caching is opt-in with the profiler --cache-dir. Unique STEP tessellation and
posed illustration+HLR requests run in independent native clients, and normal
production composition consumes them in the original order. Includes project
loading, collection/tessellation, rendering, output writing and worker cleanup.
"""

from __future__ import annotations

import argparse
from importlib.metadata import version
import json
from pathlib import Path
import platform
import sys
import threading
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from altium_monkey.altium_pcbdoc import AltiumPcbDoc
    from altium_cruncher.altium_cruncher_pcb_illustration import (
        IllustrationJob,
        IllustrationComponent,
        IllustrationSymbol,
        PlacedIllustrations,
        Side,
    )
    from altium_cruncher.altium_cruncher_pcb_svg_component_layers import (
        ComponentLayerSession,
    )
    from altium_cruncher.pcb_board_region_envelope_index import (
        BoardRegionEnvelopeIndex,
    )

from profile_pcb_svg import output_inventory, source_fingerprint


class ProcessSamples:
    def __init__(self) -> None:
        import psutil  # Optional profiling dependency, supplied through uv --with.

        self.psutil = psutil
        self.root = psutil.Process()
        self.stop = threading.Event()
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.peak_rss = 0
        self.peak_threads = 0
        self.processes = {}

    def sample(self) -> None:
        rss, threads = 0, 0
        for process in [self.root, *self.root.children(recursive=True)]:
            try:
                memory = process.memory_info().rss
                count = process.num_threads()
                cpu = process.cpu_times()
                self.processes[process.pid] = dict(
                    name=process.name(),
                    cpu_seconds=cpu.user + cpu.system,
                    peak_rss=max(
                        memory, self.processes.get(process.pid, {}).get("peak_rss", 0)
                    ),
                )
                rss += memory
                threads += count
            except self.psutil.Error:
                pass
        self.peak_rss = max(self.peak_rss, rss)
        self.peak_threads = max(self.peak_threads, threads)

    def run(self) -> None:
        while not self.stop.wait(0.25):
            self.sample()

    def finish(self) -> dict[str, object]:
        self.stop.set()
        self.thread.join()
        self.sample()
        return dict(
            peak_aggregate_rss_bytes=self.peak_rss,
            peak_aggregate_threads=self.peak_threads,
            processes=self.processes,
            note="Sampled every 250 ms; RSS sums shared pages and is not private committed memory. Exited processes can lose their final subsecond CPU sample.",
        )


class WorkerProbe:
    def __init__(self, workers: int) -> None:
        self.workers = workers
        self.requests = []
        self.jobs = []
        self.lock = threading.Lock()

    def install(self) -> None:
        from altium_cruncher.altium_cruncher_pcb_illustration import IllustrationJob
        from altium_cruncher.altium_cruncher_pcb_svg_component_layers import (
            ComponentLayerSession,
        )

        native = IllustrationJob._render_native
        materialize = ComponentLayerSession._materialize

        def measured(
            job: IllustrationJob, part: IllustrationComponent, **kwargs: object
        ) -> IllustrationSymbol:
            started = time.perf_counter()
            failed = False
            try:
                return native(job, part, **kwargs)
            except BaseException:
                failed = True
                raise
            finally:
                with self.lock:
                    self.requests.append(
                        dict(
                            designator=part.designator,
                            side=kwargs["side"],
                            seconds=time.perf_counter() - started,
                            failed=failed,
                            meshes=len(part.meshes),
                            thread=threading.get_ident(),
                        )
                    )

        def record(
            session: ComponentLayerSession,
            pcbdoc: AltiumPcbDoc,
            side: Side,
            line_width: float,
            illustrate: bool,
            region_index: BoardRegionEnvelopeIndex | None = None,
        ) -> PlacedIllustrations:
            result = materialize(
                session,
                pcbdoc,
                side,
                line_width,
                illustrate,
                region_index,
            )
            if session.job is not None:
                self.jobs.append(
                    dict(
                        side=side,
                        counts=dict(session.job.counts),
                        warnings=list(session.job.warnings),
                    )
                )
            return result

        IllustrationJob._render_native = measured
        ComponentLayerSession._materialize = record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workers", type=int, choices=(1, 2, 4, 8, 16, 32), required=True
    )
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument(
        "--cache-dir",
        type=Path,
        help="enable the persistent cache for cold/warm comparisons",
    )
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command or command[0] != "toon":
        parser.error("Expected -- toon ...")
    if any(flag in command for flag in ("--cache-dir", "--workers", "--no-cache")):
        parser.error("Profiler controls worker count and cache options")
    command += ["--workers", str(args.workers)]
    command += (
        ["--cache-dir", str(args.cache_dir)] if args.cache_dir else ["--no-cache"]
    )
    if "--timings" not in command:
        command += ["--timings", str(args.report.with_suffix(".timings.json"))]
    args.report.parent.mkdir(parents=True, exist_ok=True)
    samples = ProcessSamples()
    samples.thread.start()
    probe = WorkerProbe(args.workers)
    started = time.perf_counter()
    exit_code = 0
    try:
        probe.install()
        from altium_cruncher._cli import main as cli_main

        sys.argv = ["acr", *command]
        cli_main()
    except SystemExit as error:
        exit_code = int(error.code or 0)
    except BaseException:
        exit_code = 1
        raise
    finally:
        elapsed = time.perf_counter() - started
        memory = samples.finish()
        report = dict(
            command=command,
            workers=args.workers,
            exit_code=exit_code,
            wall_seconds=elapsed,
            platform=platform.platform(),
            python=sys.version,
            versions={
                name: version(name)
                for name in ("altium-cruncher", "altium-monkey", "wn-geometer")
            },
            source_fingerprint=source_fingerprint(),
            outputs=output_inventory(command),
            requests=probe.requests,
            jobs=probe.jobs,
            memory=memory,
            notes=[
                "Full CLI wall time includes tessellation, SVG output and pool cleanup; no PNG. Disk reuse only with explicit --cache-dir.",
                "Independent STEP tessellations and posed HLR/illustrations use the bounded pool. Recorded illustration request times overlap; do not sum as board wall time.",
                "Uses production --workers; instrumentation only times requests and samples resources.",
                "On cancellation queued work is cancelled; running requests drain with their ordinary native timeouts.",
            ],
        )
        args.report.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(
            f"Workers {args.workers}: {elapsed:.3f}s, exit {exit_code}, report {args.report}",
            flush=True,
        )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
