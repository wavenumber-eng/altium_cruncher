"""Tests for the release-artifact identity and content policy."""

from __future__ import annotations

import io
from pathlib import Path
import tarfile

import pytest

from support_scripts import package_artifacts


def _write_dist(
    dist_dir: Path,
    *,
    extra_sdist_member: str | None = None,
) -> tuple[Path, Path]:
    dist_dir.mkdir()
    wheel = dist_dir / "altium_cruncher-1-py3-none-any.whl"
    wheel.write_bytes(b"wheel")
    sdist = dist_dir / "altium_cruncher-1.tar.gz"
    members = {
        "altium_cruncher-1/pyproject.toml": b"[build-system]\n",
        "altium_cruncher-1/src/py/altium_cruncher/__init__.py": b"",
    }
    if extra_sdist_member is not None:
        members[f"altium_cruncher-1/{extra_sdist_member}"] = b"not public"
    with tarfile.open(sdist, mode="w:gz") as archive:
        for name, payload in members.items():
            info = tarfile.TarInfo(name)
            info.size = len(payload)
            archive.addfile(info, io.BytesIO(payload))
    return wheel, sdist


def test_manifest_names_exact_artifacts_and_detects_tampering(tmp_path: Path) -> None:
    dist_dir = tmp_path / "dist"
    wheel, _sdist = _write_dist(dist_dir)

    package_artifacts.write_manifest(dist_dir)
    package_artifacts.verify_manifest(dist_dir)

    wheel.write_bytes(b"changed")
    with pytest.raises(SystemExit, match="digest mismatch"):
        package_artifacts.verify_manifest(dist_dir)


@pytest.mark.parametrize(
    "row",
    [
        "not-a-digest  altium_cruncher-1-py3-none-any.whl",
        "0x" + "0" * 62 + "  altium_cruncher-1-py3-none-any.whl",
        "0" * 64 + " altium_cruncher-1-py3-none-any.whl",
    ],
)
def test_manifest_rejects_malformed_rows(tmp_path: Path, row: str) -> None:
    dist_dir = tmp_path / "dist"
    _write_dist(dist_dir)
    (dist_dir / "SHA256SUMS").write_text(f"{row}\n", encoding="ascii")

    with pytest.raises(SystemExit, match="Malformed artifact manifest row"):
        package_artifacts.verify_manifest(dist_dir)


def test_manifest_rejects_duplicate_and_missing_names(tmp_path: Path) -> None:
    dist_dir = tmp_path / "dist"
    wheel, _sdist = _write_dist(dist_dir)
    duplicate = f"{'0' * 64}  {wheel.name}\n" * 2
    (dist_dir / "SHA256SUMS").write_text(duplicate, encoding="ascii")

    with pytest.raises(SystemExit, match="Malformed artifact manifest row"):
        package_artifacts.verify_manifest(dist_dir)

    (dist_dir / "SHA256SUMS").write_text(
        f"{'0' * 64}  {wheel.name}\n", encoding="ascii"
    )
    with pytest.raises(SystemExit, match="manifest names differ"):
        package_artifacts.verify_manifest(dist_dir)


def test_exactly_one_wheel_and_one_sdist_are_required(tmp_path: Path) -> None:
    dist_dir = tmp_path / "dist"
    _write_dist(dist_dir)
    (dist_dir / "altium_cruncher-2-py3-none-any.whl").write_bytes(b"second")

    with pytest.raises(SystemExit, match="one wheel and one sdist"):
        package_artifacts.write_manifest(dist_dir)


@pytest.mark.parametrize(
    "member_name",
    ["altium_cruncher-1/../escape.py", "/etc/passwd", "loose-root-file"],
)
def test_unsafe_or_unrooted_sdist_members_are_rejected(
    tmp_path: Path,
    member_name: str,
) -> None:
    dist_dir = tmp_path / "dist"
    _wheel, sdist = _write_dist(dist_dir)
    with tarfile.open(sdist, mode="w:gz") as archive:
        for name in ("altium_cruncher-1/pyproject.toml", member_name):
            info = tarfile.TarInfo(name)
            payload = b"data"
            info.size = len(payload)
            archive.addfile(info, io.BytesIO(payload))

    with pytest.raises(SystemExit):
        package_artifacts.validate_contents(dist_dir)


def test_sdist_allowlist_accepts_runtime_source_and_metadata(tmp_path: Path) -> None:
    dist_dir = tmp_path / "dist"
    # Hatchling force-includes the VCS ignore file in every sdist.
    _write_dist(dist_dir, extra_sdist_member=".gitignore")

    package_artifacts.validate_contents(dist_dir)


@pytest.mark.parametrize(
    "member",
    [
        "tests/assets/private.PcbDoc",
        "docs/plans/internal/plan.md",
        "docs/research/internal.md",
        "output/private.txt",
        "src/py/altium_cruncher/__pycache__/module.pyc",
    ],
)
def test_sdist_allowlist_rejects_private_or_unowned_members(
    tmp_path: Path,
    member: str,
) -> None:
    dist_dir = tmp_path / "dist"
    _write_dist(dist_dir, extra_sdist_member=member)

    with pytest.raises(SystemExit):
        package_artifacts.validate_contents(dist_dir)
