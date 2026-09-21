"""Run an ACR command and census version-neutral Geometer IPC operations.

The probe wraps the stable ``GeometerClient.execute`` boundary, allowing the
same script to compare Cruncher revisions whose renderer module names differ.
It does not alter requests or responses.
"""

from __future__ import annotations

import argparse
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import platform
import sys
import threading
import time


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--replay-first-model", type=int, default=0)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("Expected -- COMMAND ...")

    import geometer

    original_execute = geometer.GeometerClient.execute
    original_model_illustration = geometer.GeometerClient.model_illustration_geometry
    events: list[dict[str, object]] = []
    lock = threading.Lock()
    first_model_call: list[tuple[object, bytes | None]] = []
    phase = ["command"]

    def capture_model_illustration(
        client: object,
        request: object,
        model: bytes | None = None,
        *,
        timeout: float | None = None,
    ) -> object:
        if not first_model_call:
            first_model_call.append((request, model))
        return original_model_illustration(
            client, request, model, timeout=timeout
        )

    def measured_execute(
        client: object,
        operation: str,
        request: object,
        attachments: tuple[object, ...] = (),
        *,
        timeout: float | None = None,
    ) -> object:
        started = time.perf_counter()
        failed = False
        try:
            return original_execute(
                client, operation, request, attachments, timeout=timeout
            )
        except BaseException:
            failed = True
            raise
        finally:
            row = {
                "operation": operation,
                "seconds": time.perf_counter() - started,
                "attachment_bytes": sum(
                    len(getattr(attachment, "data", b""))
                    for attachment in attachments
                ),
                "failed": failed,
                "thread": threading.get_ident(),
                "phase": phase[0],
                "request_type": type(request).__name__,
                "request_repr_sha256": hashlib.sha256(
                    repr(request).encode("utf-8")
                ).hexdigest().upper(),
                "clipped": getattr(request, "clipping", None) is not None,
            }
            with lock:
                events.append(row)

    geometer.GeometerClient.execute = measured_execute
    geometer.GeometerClient.model_illustration_geometry = capture_model_illustration
    from altium_cruncher._cli import main as cli_main

    original_argv = sys.argv
    sys.argv = ["acr", *command]
    started = time.perf_counter()
    exit_code = 0
    try:
        cli_main()
    except SystemExit as error:
        exit_code = int(error.code or 0)
    finally:
        sys.argv = original_argv
        elapsed = time.perf_counter() - started
        replay: dict[str, object] | None = None
        if args.replay_first_model and first_model_call:
            request, model = first_model_call[0]
            durations = []
            phase[0] = "replay"
            with geometer.GeometerClient() as client:
                for _index in range(args.replay_first_model):
                    replay_started = time.perf_counter()
                    original_model_illustration(
                        client, request, model, timeout=60
                    )
                    durations.append(time.perf_counter() - replay_started)
            replay = {
                "count": len(durations),
                "seconds": durations,
                "request_type": type(request).__name__,
                "request_repr_sha256": hashlib.sha256(
                    repr(request).encode("utf-8")
                ).hexdigest().upper(),
                "model_bytes": len(model or b""),
                "model_sha256": hashlib.sha256(model or b"").hexdigest().upper(),
            }
        args.report.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "command": command,
            "exit_code": exit_code,
            "wall_seconds": elapsed,
            "platform": platform.platform(),
            "python": sys.version,
            "versions": {
                name: version(name)
                for name in ("altium-cruncher", "altium-monkey", "wn-geometer")
            },
            "operations": events,
            "first_model_replay": replay,
            "notes": [
                "Instrumentation wraps GeometerClient.execute without changing requests or responses.",
                "Durations include serialization, IPC, native execution, and response wait.",
            ],
        }
        args.report.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(
            f"Geometer profile: {args.report} "
            f"({len(events)} calls, {elapsed:.3f}s, exit {exit_code})"
        )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
