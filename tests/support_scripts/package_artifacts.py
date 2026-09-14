"""Validate, identify, and rebuild Altium Cruncher release artifacts."""

from __future__ import annotations

import argparse
import hashlib
from email.message import Message
from email.parser import BytesParser
from email.policy import compat32
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tarfile
import tempfile
import zipfile


MAX_SDIST_COMPRESSED_BYTES = 25 * 1024 * 1024
MAX_SDIST_UNPACKED_BYTES = 40 * 1024 * 1024
MAX_WHEEL_BYTES = 5 * 1024 * 1024
SDIST_ROOT_FILES = {
    # Hatchling force-includes the VCS ignore file so sdist rebuilds
    # reproduce its file selection.
    ".gitignore",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "PKG-INFO",
    "README.md",
    "package-lock.json",
    "package.json",
    "pyproject.toml",
    "tsconfig.contracts.json",
    "tspconfig.yaml",
}
SDIST_ROOT_DIRECTORIES = {"docs", "examples", "scripts", "src"}


def _artifacts(dist_dir: Path) -> tuple[Path, Path]:
    wheels = sorted(dist_dir.glob("altium_cruncher-*.whl"))
    sdists = sorted(dist_dir.glob("altium_cruncher-*.tar.gz"))
    if len(wheels) != 1 or len(sdists) != 1:
        raise SystemExit(
            f"Expected one wheel and one sdist in {dist_dir}; "
            f"found {len(wheels)} wheel(s) and {len(sdists)} sdist(s)"
        )
    return wheels[0], sdists[0]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_manifest(dist_dir: Path) -> None:
    """Write hashes for the exact wheel and sdist produced by the build job."""
    artifacts = _artifacts(dist_dir)
    lines = [f"{_sha256(path)}  {path.name}\n" for path in artifacts]
    (dist_dir / "SHA256SUMS").write_text("".join(lines), encoding="ascii")


def verify_manifest(dist_dir: Path) -> None:
    """Verify that SHA256SUMS names and hashes exactly the available artifacts."""
    artifacts = _artifacts(dist_dir)
    manifest = dist_dir / "SHA256SUMS"
    rows = manifest.read_text(encoding="ascii").splitlines()
    expected_names = {path.name for path in artifacts}
    observed: dict[str, str] = {}
    for row in rows:
        digest, separator, filename = row.partition("  ")
        digest_is_hex = len(digest) == 64 and all(
            character in "0123456789abcdef" for character in digest
        )
        if not separator or not digest_is_hex or filename in observed:
            raise SystemExit(f"Malformed artifact manifest row: {row!r}")
        observed[filename] = digest
    if set(observed) != expected_names:
        raise SystemExit(
            f"Artifact manifest names differ: {set(observed)!r} != {expected_names!r}"
        )
    for path in artifacts:
        actual = _sha256(path)
        if observed[path.name] != actual:
            raise SystemExit(f"Artifact digest mismatch: {path.name}")


def _sdist_member_payload(member: tarfile.TarInfo) -> PurePosixPath | None:
    path = PurePosixPath(member.name)
    if path.is_absolute() or ".." in path.parts:
        raise SystemExit(f"Unsafe or unrooted sdist member: {member.name}")
    if len(path.parts) == 1:
        if member.isdir():
            return None
        raise SystemExit(f"Unsafe or unrooted sdist member: {member.name}")
    payload = PurePosixPath(*path.parts[1:])
    return payload if payload.parts else None


def _check_sdist_member_policy(payload: PurePosixPath, member_name: str) -> None:
    """Reject sdist members outside the reviewed public-source allowlist."""
    first = payload.parts[0]
    if first not in SDIST_ROOT_FILES | SDIST_ROOT_DIRECTORIES:
        raise SystemExit(f"Sdist member is outside the allowlist: {member_name}")
    if payload.parts[:2] in {("docs", "plans"), ("docs", "research")}:
        raise SystemExit(f"Private working documentation is packaged: {member_name}")
    if first == "tests" or "__pycache__" in payload.parts:
        raise SystemExit(f"Test/private cache material is packaged: {member_name}")
    if payload.suffix in {".pyc", ".pyo"}:
        raise SystemExit(f"Compiled Python cache is packaged: {member_name}")


def validate_contents(dist_dir: Path) -> None:
    """Enforce release-artifact count, size budgets, and the sdist allowlist."""
    wheel, sdist = _artifacts(dist_dir)
    if wheel.stat().st_size > MAX_WHEEL_BYTES:
        raise SystemExit(
            f"Wheel exceeds {MAX_WHEEL_BYTES} bytes: {wheel.stat().st_size}"
        )
    if sdist.stat().st_size > MAX_SDIST_COMPRESSED_BYTES:
        raise SystemExit(
            f"Sdist exceeds {MAX_SDIST_COMPRESSED_BYTES} compressed bytes: "
            f"{sdist.stat().st_size}"
        )

    unpacked_size = 0
    with tarfile.open(sdist, mode="r:gz") as archive:
        members = archive.getmembers()
        roots = {PurePosixPath(member.name).parts[0] for member in members}
        if len(roots) != 1:
            raise SystemExit(f"Sdist must have one root directory; found {roots!r}")
        for member in members:
            payload = _sdist_member_payload(member)
            if payload is None:
                continue
            unpacked_size += member.size
            _check_sdist_member_policy(payload, member.name)
    if unpacked_size > MAX_SDIST_UNPACKED_BYTES:
        raise SystemExit(
            f"Sdist exceeds {MAX_SDIST_UNPACKED_BYTES} unpacked bytes: {unpacked_size}"
        )


def _wheel_metadata(path: Path) -> Message:
    with zipfile.ZipFile(path) as archive:
        names = [
            name for name in archive.namelist() if name.endswith(".dist-info/METADATA")
        ]
        if len(names) != 1:
            raise SystemExit(f"Expected one METADATA file in {path}; found {names!r}")
        return BytesParser(policy=compat32).parsebytes(archive.read(names[0]))


def _metadata_contract(metadata: Message) -> tuple[str, str, tuple[str, ...]]:
    name = metadata.get("Name")
    version = metadata.get("Version")
    if name is None or version is None:
        raise SystemExit("Wheel metadata is missing Name or Version")
    requirements = tuple(sorted(metadata.get_all("Requires-Dist", [])))
    return name, version, requirements


def rebuild_from_sdist(dist_dir: Path) -> None:
    """Build a wheel from the sdist and compare its dependency metadata."""
    validate_contents(dist_dir)
    wheel, sdist = _artifacts(dist_dir)
    with tempfile.TemporaryDirectory(prefix="altium_cruncher_sdist_") as temporary:
        temporary_path = Path(temporary)
        source_dir = temporary_path / "source"
        output_dir = temporary_path / "dist"
        source_dir.mkdir()
        with tarfile.open(sdist, mode="r:gz") as archive:
            archive.extractall(source_dir, filter="data")
        roots = [path for path in source_dir.iterdir() if path.is_dir()]
        if len(roots) != 1:
            raise SystemExit(f"Expected one extracted sdist root; found {roots!r}")
        subprocess.run(
            [
                sys.executable,
                "-m",
                "build",
                "--wheel",
                "--outdir",
                str(output_dir),
                str(roots[0]),
            ],
            check=True,
        )
        rebuilt = sorted(output_dir.glob("altium_cruncher-*.whl"))
        if len(rebuilt) != 1:
            raise SystemExit(f"Expected one rebuilt wheel; found {rebuilt!r}")
        if _metadata_contract(_wheel_metadata(wheel)) != _metadata_contract(
            _wheel_metadata(rebuilt[0])
        ):
            raise SystemExit("Direct and sdist-rebuilt wheel metadata differ")


def main() -> None:
    """Run the requested release-artifact policy operation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "operation", choices=("manifest", "verify", "validate", "rebuild")
    )
    parser.add_argument("--dist", type=Path, default=Path("dist"))
    arguments = parser.parse_args()
    dist_dir = arguments.dist.resolve()
    operations = {
        "manifest": write_manifest,
        "verify": verify_manifest,
        "validate": validate_contents,
        "rebuild": rebuild_from_sdist,
    }
    operations[arguments.operation](dist_dir)


if __name__ == "__main__":
    main()
