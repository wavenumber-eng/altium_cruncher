"""Run a clean installed-console smoke test for a built wheel."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def _run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> None:
    """Run a subprocess and raise with captured context on failure."""
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        cmd_text = " ".join(command)
        raise SystemExit(
            f"Command failed ({completed.returncode}): {cmd_text}\n"
            f"stdout:\n{completed.stdout}\n"
            f"stderr:\n{completed.stderr}"
        )


def _latest_wheel(dist_dir: Path) -> Path:
    """Return the newest wheel in a dist directory."""
    wheels = sorted(dist_dir.glob("altium_cruncher-*.whl"), key=lambda path: path.stat().st_mtime)
    if not wheels:
        raise SystemExit(f"No altium_cruncher wheel found in {dist_dir}")
    return wheels[-1]


def _venv_python(venv_dir: Path) -> Path:
    """Return the Python executable path for a venv."""
    script_dir = "Scripts" if os.name == "nt" else "bin"
    executable = "python.exe" if os.name == "nt" else "python"
    return venv_dir / script_dir / executable


def _console_script(venv_dir: Path, command: str) -> Path:
    """Return a console script path in a venv."""
    script_dir = "Scripts" if os.name == "nt" else "bin"
    suffix = ".exe" if os.name == "nt" else ""
    return venv_dir / script_dir / f"{command}{suffix}"


def _clean_env(venv_dir: Path) -> dict[str, str]:
    """Build an environment that prefers the test venv and avoids source leakage."""
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    script_dir = venv_dir / ("Scripts" if os.name == "nt" else "bin")
    env["PATH"] = str(script_dir) + os.pathsep + env.get("PATH", "")
    return env


def run_install_smoke(wheel: Path) -> None:
    """Install a wheel into a temporary venv and verify the console script."""
    wheel = wheel.resolve()
    if not wheel.exists():
        raise SystemExit(f"Wheel does not exist: {wheel}")

    with tempfile.TemporaryDirectory(prefix="altium_cruncher_install_smoke_") as temp:
        temp_dir = Path(temp)
        venv_dir = temp_dir / "venv"
        sys.stdout.write(f"Creating smoke venv: {venv_dir}\n")
        _run([sys.executable, "-m", "venv", str(venv_dir)], cwd=temp_dir)

        python = _venv_python(venv_dir)
        env = _clean_env(venv_dir)
        _run([str(python), "-m", "pip", "install", str(wheel)], cwd=temp_dir, env=env)

        command = "altium-cruncher"
        executable = _console_script(venv_dir, command)
        if not executable.exists():
            raise SystemExit(f"Missing console script after install: {executable}")
        _run([str(executable), "--version"], cwd=temp_dir, env=env)
        _run([command, "--version"], cwd=temp_dir, env=env)

        legacy_executable = _console_script(venv_dir, "altium_cruncher")
        if legacy_executable.exists():
            raise SystemExit(f"Unexpected legacy console script after install: {legacy_executable}")

        _run([str(python), "-m", "altium_cruncher", "version"], cwd=temp_dir, env=env)
        sys.stdout.write("Installed-console smoke passed.\n")


def main() -> None:
    """Parse arguments and run the install smoke."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--wheel",
        type=Path,
        default=None,
        help="Wheel to install. Defaults to the newest altium_cruncher wheel in dist/.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    wheel = args.wheel or _latest_wheel(repo_root / "dist")
    run_install_smoke(wheel)


if __name__ == "__main__":
    main()
