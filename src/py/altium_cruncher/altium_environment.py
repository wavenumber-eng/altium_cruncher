"""Altium Designer install and profile discovery helpers."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

_DEFAULT_INSTALL_ROOTS = (
    Path(r"C:\Program Files\Altium"),
    Path(r"C:\Program Files (x86)\Altium"),
)
_DEFAULT_PROGRAMDATA_ROOT = Path(r"C:\ProgramData\Altium")
_PROFILE_GUID_RE = re.compile(r"\{(?P<guid>[0-9A-Fa-f-]+)\}")
_AD_MAJOR_RE = re.compile(r"^AD(?P<major>\d+)$", re.IGNORECASE)


@dataclass(frozen=True, slots=True)
class AltiumInstall:
    """One discovered Altium Designer installation."""

    name: str
    x2_path: Path
    major: int | None
    source: str
    runtime_tfm: str | None = None
    registry_version: str | None = None
    unique_id: str | None = None

    @property
    def root(self) -> Path:
        """Return the install root directory."""
        return self.x2_path.parent

    @property
    def label(self) -> str:
        """Return a compact human label."""
        if self.major is not None:
            return f"AD{self.major}"
        return self.name

    def to_dict(self) -> dict[str, object]:
        """Return a stable JSON representation."""
        return {
            "name": self.name,
            "label": self.label,
            "major": self.major,
            "root": str(self.root),
            "x2_path": str(self.x2_path),
            "runtime_tfm": self.runtime_tfm,
            "registry_version": self.registry_version,
            "unique_id": self.unique_id,
            "source": self.source,
        }


@dataclass(frozen=True, slots=True)
class AltiumProfile:
    """One Altium ProgramData profile folder."""

    name: str
    guid: str
    path: Path
    extensions_root: Path
    registry_path: Path
    registry_exists: bool
    module_name: str
    module_dir: Path
    module_dir_exists: bool
    registered: bool
    registry_version: str | None
    dll_path: Path
    dll_exists: bool
    last_write_time_utc: str | None

    def to_dict(self) -> dict[str, object]:
        """Return a stable JSON representation."""
        return {
            "name": self.name,
            "guid": self.guid,
            "path": str(self.path),
            "extensions_root": str(self.extensions_root),
            "registry_path": str(self.registry_path),
            "registry_exists": self.registry_exists,
            "module_name": self.module_name,
            "module_dir": str(self.module_dir),
            "module_dir_exists": self.module_dir_exists,
            "registered": self.registered,
            "registry_version": self.registry_version,
            "dll_path": str(self.dll_path),
            "dll_exists": self.dll_exists,
            "last_write_time_utc": self.last_write_time_utc,
        }


def discover_altium_installs(
    *,
    install_roots: list[Path] | None = None,
) -> list[AltiumInstall]:
    """Find Altium Designer installs by scanning known roots and registry rows."""
    discovered: dict[str, AltiumInstall] = {}
    for install in _filesystem_installs(_resolve_install_roots(install_roots)):
        discovered[str(install.x2_path).lower()] = install

    for install in _registry_installs():
        key = str(install.x2_path).lower()
        previous = discovered.get(key)
        if previous is None:
            discovered[key] = install
        else:
            discovered[key] = AltiumInstall(
                name=previous.name,
                x2_path=previous.x2_path,
                major=previous.major,
                source="filesystem,registry",
                runtime_tfm=previous.runtime_tfm or install.runtime_tfm,
                registry_version=install.registry_version,
                unique_id=install.unique_id,
            )

    return sorted(
        discovered.values(),
        key=lambda item: (
            item.major is None,
            -(item.major or -1),
            item.name.lower(),
            str(item.x2_path).lower(),
        ),
    )


def select_altium_install(
    installs: list[AltiumInstall],
    *,
    version: str | None = None,
    altium_path: Path | None = None,
) -> AltiumInstall | None:
    """Select an install by explicit X2 path, AD major, or latest discovered version."""
    explicit_install = _explicit_install(altium_path)
    if explicit_install is not None or altium_path is not None:
        return explicit_install
    if not installs:
        return None
    matching_install = _install_matching_version(installs, version)
    if matching_install is not None or str(version or "").strip():
        return matching_install
    return installs[0]


def launch_altium(
    install: AltiumInstall,
    *,
    file_path: Path | None = None,
    dry_run: bool = False,
) -> list[str]:
    """Launch an Altium install, optionally opening a document."""
    command = [str(install.x2_path)]
    if file_path is not None:
        command.append(str(file_path.resolve()))
    if dry_run:
        return command

    if sys.platform != "win32":
        raise OSError("Launching Altium Designer is supported on Windows only.")

    if file_path is not None:
        from altium_monkey.altium_launcher import AltiumLauncher

        launcher = AltiumLauncher(altium_path=install.x2_path)
        if not launcher.open(file_path):
            raise RuntimeError(f"Altium Designer did not accept file: {file_path}")
        return command

    subprocess.Popen(command)  # noqa: S603
    return command


def discover_altium_profiles(
    *,
    module_name: str = "ad-panel-monkey",
    programdata_root: Path | None = None,
) -> list[AltiumProfile]:
    """Find Altium ProgramData profile folders and selected extension state."""
    root = _resolve_programdata_root(programdata_root)
    if not root.exists():
        return []
    profiles: list[AltiumProfile] = []
    for child in sorted(root.iterdir(), key=lambda item: item.name.lower()):
        if not child.is_dir():
            continue
        if not child.name.lower().startswith("altium designer"):
            continue
        if "_security" in child.name.lower():
            continue
        guid = _profile_guid_from_name(child.name)
        if guid is None:
            continue
        extensions_root = child / "Extensions"
        registry_path = extensions_root / "ExtensionsRegistry.xml"
        module_dir = extensions_root / module_name
        dll_path = module_dir / f"{module_name}.dll"
        registered, version = _read_extension_registry_item(registry_path, module_name)
        profiles.append(
            AltiumProfile(
                name=child.name,
                guid=guid,
                path=child,
                extensions_root=extensions_root,
                registry_path=registry_path,
                registry_exists=registry_path.exists(),
                module_name=module_name,
                module_dir=module_dir,
                module_dir_exists=module_dir.exists(),
                registered=registered,
                registry_version=version,
                dll_path=dll_path,
                dll_exists=dll_path.exists(),
                last_write_time_utc=_mtime_utc(child),
            )
        )
    return profiles


def clean_altium_profiles(
    profiles: list[AltiumProfile],
    *,
    profile_guid: str | None = None,
    all_profiles: bool = False,
    dry_run: bool = False,
) -> list[dict[str, object]]:
    """Remove selected extension directories and registry items from profiles."""
    targets = _select_profiles_for_clean(
        profiles,
        profile_guid=profile_guid,
        all_profiles=all_profiles,
    )
    actions: list[dict[str, object]] = []
    for profile in targets:
        removed_dir = False
        removed_registry = False
        if profile.module_dir.exists():
            _assert_child_path(profile.module_dir, profile.extensions_root)
            if not dry_run:
                shutil.rmtree(profile.module_dir)
            removed_dir = True
        if profile.registry_path.exists():
            removed_registry = _remove_extension_registry_item(
                profile.registry_path,
                profile.module_name,
                dry_run=dry_run,
            )
        actions.append(
            {
                "profile_guid": profile.guid,
                "profile_name": profile.name,
                "profile_path": str(profile.path),
                "module_name": profile.module_name,
                "module_dir": str(profile.module_dir),
                "removed_module_dir": removed_dir,
                "removed_registry_item": removed_registry,
                "dry_run": dry_run,
            }
        )
    return actions


def _resolve_install_roots(install_roots: list[Path] | None) -> list[Path]:
    roots: list[Path] = []
    roots.extend(install_roots or [])
    env_roots = os.environ.get("ALTIUM_CRUNCHER_ALTIUM_INSTALL_ROOTS", "")
    for raw_root in env_roots.split(os.pathsep):
        if raw_root.strip():
            roots.append(Path(raw_root.strip()))
    for name, value in sorted(os.environ.items()):
        if not name.upper().startswith("ALTIUM_AD") or not name.upper().endswith("_ROOT"):
            continue
        if value.strip():
            roots.append(Path(value.strip()).parent)
    roots.extend(_DEFAULT_INSTALL_ROOTS)
    return _dedupe_paths(roots)


def _filesystem_installs(roots: list[Path]) -> list[AltiumInstall]:
    installs: list[AltiumInstall] = []
    for root in roots:
        if not root.exists():
            continue
        for child in sorted(root.iterdir(), key=lambda item: item.name.lower()):
            if not child.is_dir():
                continue
            x2_path = _existing_x2(child)
            if x2_path is not None:
                installs.append(_install_from_x2(x2_path, source="filesystem"))
    return installs


def _explicit_install(altium_path: Path | None) -> AltiumInstall | None:
    if altium_path is None:
        return None
    x2_path = altium_path.resolve()
    if x2_path.is_dir():
        x2_path = x2_path / "X2.exe"
    if not x2_path.exists():
        return None
    return _install_from_x2(x2_path, source="explicit")


def _install_matching_version(
    installs: list[AltiumInstall],
    version: str | None,
) -> AltiumInstall | None:
    requested_major = _parse_ad_major(version)
    if requested_major is not None:
        return next(
            (install for install in installs if install.major == requested_major),
            None,
        )
    requested_name = (version or "").strip().lower()
    if not requested_name:
        return None
    return next(
        (
            install
            for install in installs
            if install.name.lower() == requested_name
            or install.label.lower() == requested_name
        ),
        None,
    )


def _resolve_programdata_root(programdata_root: Path | None) -> Path:
    if programdata_root is not None:
        return programdata_root
    env_root = os.environ.get("ALTIUM_CRUNCHER_ALTIUM_PROGRAMDATA_ROOT") or os.environ.get(
        "ALTIUM_CRUNCHER_ALTIUM_PROGRAMDATA"
    )
    if env_root:
        return Path(env_root)
    return _DEFAULT_PROGRAMDATA_ROOT


def _dedupe_paths(paths: list[Path]) -> list[Path]:
    seen: set[str] = set()
    result: list[Path] = []
    for path in paths:
        key = str(path).lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(path)
    return result


def _existing_x2(root: Path) -> Path | None:
    for name in ("X2.exe", "X2.EXE"):
        candidate = root / name
        if candidate.exists():
            return candidate.resolve()
    return None


def _install_from_x2(
    x2_path: Path,
    *,
    source: str,
    registry_version: str | None = None,
    unique_id: str | None = None,
) -> AltiumInstall:
    root = x2_path.parent
    major = _parse_ad_major(root.name)
    return AltiumInstall(
        name=root.name,
        x2_path=x2_path.resolve(),
        major=major,
        source=source,
        runtime_tfm=_read_runtime_tfm(root),
        registry_version=registry_version,
        unique_id=unique_id,
    )


def _parse_ad_major(value: str | None) -> int | None:
    text = str(value or "").strip()
    if not text:
        return None
    match = _AD_MAJOR_RE.match(text)
    if match:
        return int(match.group("major"))
    lowered = text.lower().removeprefix("ad")
    if lowered.isdigit():
        return int(lowered)
    return None


def _read_runtime_tfm(root: Path) -> str | None:
    runtime_config = root / "X2.runtimeconfig.json"
    if not runtime_config.exists():
        return None
    try:
        import json

        payload = json.loads(runtime_config.read_text(encoding="utf-8"))
        value = payload.get("runtimeOptions", {}).get("tfm")
        return str(value) if value else None
    except Exception:
        return None


def _registry_installs() -> list[AltiumInstall]:
    if sys.platform != "win32":
        return []
    try:
        import winreg
    except Exception:
        return []

    result: list[AltiumInstall] = []
    try:
        root_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"Software\Altium\Builds")
    except OSError:
        return []
    with root_key:
        index = 0
        while True:
            try:
                subkey_name = winreg.EnumKey(root_key, index)
            except OSError:
                break
            index += 1
            try:
                subkey = winreg.OpenKey(root_key, subkey_name)
            except OSError:
                continue
            with subkey:
                install = _registry_install_from_key(subkey, subkey_name)
                if install is not None:
                    result.append(install)
    return result


def _registry_install_from_key(key: object, fallback_name: str) -> AltiumInstall | None:
    try:
        import winreg
    except Exception:
        return None

    def read_value(name: str) -> str | None:
        try:
            value, _kind = winreg.QueryValueEx(key, name)
        except OSError:
            return None
        return str(value) if value is not None else None

    root = read_value("ProgramsInstallPath") or read_value("InstallPath")
    if not root:
        return None
    x2_path = _existing_x2(Path(root))
    if x2_path is None:
        return None
    return _install_from_x2(
        x2_path,
        source="registry",
        registry_version=read_value("Version") or fallback_name,
        unique_id=read_value("UniqueID"),
    )


def _profile_guid_from_name(name: str) -> str | None:
    match = _PROFILE_GUID_RE.search(name)
    if not match:
        return None
    return match.group("guid").lower()


def _read_extension_registry_item(
    registry_path: Path,
    module_name: str,
) -> tuple[bool, str | None]:
    item = _find_extension_registry_item(registry_path, module_name)
    if item is None:
        return False, None
    version = None
    for child in item:
        if _strip_xml_namespace(child.tag).lower() == "version" and child.text:
            version = child.text.strip()
            break
    return True, version


def _find_extension_registry_item(
    registry_path: Path,
    module_name: str,
) -> ET.Element | None:
    if not registry_path.exists():
        return None
    try:
        root = ET.parse(registry_path).getroot()
    except Exception:
        return None
    for item in root.iter():
        if _strip_xml_namespace(item.tag).lower() != "item":
            continue
        if str(item.attrib.get("HRID", "")).lower() == module_name.lower():
            return item
    return None


def _remove_extension_registry_item(
    registry_path: Path,
    module_name: str,
    *,
    dry_run: bool,
) -> bool:
    try:
        tree = ET.parse(registry_path)
    except Exception:
        return False
    root = tree.getroot()
    removed = False
    for parent in root.iter():
        for child in list(parent):
            if _strip_xml_namespace(child.tag).lower() != "item":
                continue
            if str(child.attrib.get("HRID", "")).lower() == module_name.lower():
                if not dry_run:
                    parent.remove(child)
                removed = True
    if removed and not dry_run:
        tree.write(registry_path, encoding="utf-8", xml_declaration=True)
    return removed


def _strip_xml_namespace(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _mtime_utc(path: Path) -> str | None:
    try:
        return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()
    except OSError:
        return None


def _select_profiles_for_clean(
    profiles: list[AltiumProfile],
    *,
    profile_guid: str | None,
    all_profiles: bool,
) -> list[AltiumProfile]:
    if all_profiles:
        return profiles
    requested = str(profile_guid or "").strip("{}").lower()
    if not requested:
        raise ValueError("profiles clean requires --all or --profile-guid")
    return [profile for profile in profiles if profile.guid.lower() == requested]


def _assert_child_path(child: Path, parent: Path) -> None:
    child_resolved = child.resolve()
    parent_resolved = parent.resolve()
    if parent_resolved not in child_resolved.parents:
        raise ValueError(f"Refusing to remove path outside profile Extensions: {child}")
