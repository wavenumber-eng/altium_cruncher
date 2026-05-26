"""Shared file-level helpers for altium_cruncher command modules."""

from __future__ import annotations

from pathlib import Path


def find_prjpcb_in_cwd() -> Path | None:
    """
    Scan current working directory for a .PrjPcb file.

    Returns:
        Path to PrjPcb file if exactly one found, None otherwise.
    """
    prjpcb_files = list(Path.cwd().glob("*.PrjPcb"))
    if len(prjpcb_files) == 1:
        return prjpcb_files[0]
    return None


def find_prjpcbs_in_cwd() -> list[Path]:
    """Find all .PrjPcb files in current working directory (stable order)."""
    return sorted(
        [
            p
            for p in Path.cwd().iterdir()
            if p.is_file() and p.suffix.lower() == ".prjpcb"
        ],
        key=lambda p: p.name.lower(),
    )


def find_pcbdocs_in_cwd() -> list[Path]:
    """Find all .PcbDoc files in current working directory (stable order)."""
    return sorted(
        [
            p
            for p in Path.cwd().iterdir()
            if p.is_file() and p.suffix.lower() == ".pcbdoc"
        ],
        key=lambda p: p.name.lower(),
    )


def _default_output_dir(command_name: str) -> Path:
    """Return default output root for a command."""
    return (Path.cwd() / "output" / command_name).resolve()


def _resolve_output_dir(output_arg: Path | None, command_name: str) -> Path:
    """Resolve explicit output directory or command default and create it."""
    output_dir = (
        output_arg.resolve() if output_arg else _default_output_dir(command_name)
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir
