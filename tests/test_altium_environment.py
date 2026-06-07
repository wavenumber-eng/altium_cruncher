"""Tests for Altium install/profile discovery helpers."""

from __future__ import annotations

from pathlib import Path

from altium_cruncher.altium_environment import (
    clean_altium_profiles,
    discover_altium_installs,
    discover_altium_profiles,
    select_altium_install,
)


def test_discover_altium_installs_sorts_latest_major_first(tmp_path: Path) -> None:
    """Scan fake AD roots and select newest or requested major series."""
    root = tmp_path / "Altium"
    ad25 = root / "AD25"
    ad26 = root / "AD26"
    ad25.mkdir(parents=True)
    ad26.mkdir(parents=True)
    (ad25 / "X2.exe").write_text("", encoding="utf-8")
    (ad26 / "X2.exe").write_text("", encoding="utf-8")

    installs = [
        install
        for install in discover_altium_installs(install_roots=[root])
        if root.resolve() in install.x2_path.parents
    ]

    assert [install.label for install in installs[:2]] == ["AD26", "AD25"]
    assert select_altium_install(installs).label == "AD26"
    assert select_altium_install(installs, version="ad25").label == "AD25"


def test_profiles_list_and_clean_extension_state(tmp_path: Path) -> None:
    """Discover profile extension state and dry-run/remove selected module state."""
    profile = tmp_path / "Altium Designer {11111111-2222-3333-4444-555555555555}"
    extensions = profile / "Extensions"
    module_dir = extensions / "ad-panel-monkey"
    module_dir.mkdir(parents=True)
    (module_dir / "ad-panel-monkey.dll").write_text("", encoding="utf-8")
    registry = extensions / "ExtensionsRegistry.xml"
    registry.write_text(
        (
            "<?xml version='1.0' encoding='utf-8'?>\n"
            "<Extensions><Item HRID='ad-panel-monkey'><Version>1.2.3</Version></Item></Extensions>"
        ),
        encoding="utf-8",
    )

    profiles = discover_altium_profiles(programdata_root=tmp_path)

    assert len(profiles) == 1
    assert profiles[0].registered is True
    assert profiles[0].registry_version == "1.2.3"
    assert profiles[0].module_dir_exists is True
    dry_run_actions = clean_altium_profiles(
        profiles,
        all_profiles=True,
        dry_run=True,
    )
    assert dry_run_actions[0]["removed_module_dir"] is True
    assert module_dir.exists()

    actions = clean_altium_profiles(profiles, all_profiles=True, dry_run=False)

    assert actions[0]["removed_module_dir"] is True
    assert actions[0]["removed_registry_item"] is True
    assert not module_dir.exists()
    refreshed = discover_altium_profiles(programdata_root=tmp_path)
    assert refreshed[0].registered is False
