"""Version helpers for Altium Cruncher."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as distribution_version

__version__ = "2026.5.28"

_DISTRIBUTION_NAME = "altium-cruncher"
_CONTROLLED_DEPENDENCIES = (
    "altium-monkey",
    "wn-geometer",
)
_VERSION_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)(?:\.(\d+))?$")


@dataclass(frozen=True, slots=True)
class Version:
    major: int
    minor: int
    patch: int
    string: str
    build: int | None = None

    @property
    def release_date(self) -> date:
        return date(self.major, self.minor, self.patch)


def version() -> Version:
    try:
        raw_version = distribution_version(_DISTRIBUTION_NAME)
    except PackageNotFoundError:
        raw_version = __version__
    return parse_version(raw_version)


def parse_version(raw_version: str) -> Version:
    match = _VERSION_RE.match(raw_version)
    if match is None:
        raise ValueError(f"Unsupported Altium Cruncher version: {raw_version!r}")

    major = int(match.group(1))
    minor = int(match.group(2))
    patch = int(match.group(3))
    build = int(match.group(4)) if match.group(4) is not None else None
    version_string = f"{major}.{minor}.{patch}"
    if build is not None:
        version_string = f"{version_string}.{build}"
    return Version(
        major=major,
        minor=minor,
        patch=patch,
        build=build,
        string=version_string,
    )


def cli_version_text() -> str:
    return f"altium-cruncher {version().string}"


def dependency_version_text(distribution_name: str) -> str:
    try:
        dependency_version = distribution_version(distribution_name)
    except PackageNotFoundError:
        dependency_version = "not installed"
    return f"{distribution_name} {dependency_version}"


def cli_version_report() -> str:
    lines = [cli_version_text()]
    lines.extend(
        dependency_version_text(distribution_name)
        for distribution_name in _CONTROLLED_DEPENDENCIES
    )
    return "\n".join(lines)
