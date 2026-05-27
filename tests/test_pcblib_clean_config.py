from pathlib import Path

from altium_cruncher.altium_pcblib_clean import (
    DEFAULT_PCBLIB_CLEAN_CONFIG_FILENAME,
    PcbLibCleanConfig,
    find_workspace_pcblib_clean_config_path,
)


def test_find_workspace_pcblib_clean_config_path_from_project_child(tmp_path: Path) -> None:
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "workspace.json").write_text("{}", encoding="utf-8")

    child_dir = tmp_path / "project" / "board"
    child_dir.mkdir(parents=True)

    assert find_workspace_pcblib_clean_config_path(start_dir=child_dir, env={}) == (
        config_dir / DEFAULT_PCBLIB_CLEAN_CONFIG_FILENAME
    )


def test_find_workspace_pcblib_clean_config_path_from_config_dir(tmp_path: Path) -> None:
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "workspace.json").write_text("{}", encoding="utf-8")

    assert find_workspace_pcblib_clean_config_path(start_dir=config_dir, env={}) == (
        config_dir / DEFAULT_PCBLIB_CLEAN_CONFIG_FILENAME
    )


def test_find_workspace_pcblib_clean_config_path_from_env(tmp_path: Path) -> None:
    workspace_dir = tmp_path / "workspace"

    assert find_workspace_pcblib_clean_config_path(
        env={"ALX_HW_WORKSPACE": str(workspace_dir)}
    ) == (workspace_dir / "config" / DEFAULT_PCBLIB_CLEAN_CONFIG_FILENAME).resolve()


def test_pcblib_clean_config_loader_accepts_jsonc(tmp_path: Path) -> None:
    """Load editable PcbLib clean configs with comments and trailing commas."""
    config_path = tmp_path / DEFAULT_PCBLIB_CLEAN_CONFIG_FILENAME
    config_path.write_text(
        """
        {
          "schema": "wn.altium.pcblib.clean.config.v1",
          "profile": "default",
          // comment out sections while tuning cleanup rules
        }
        """,
        encoding="utf-8",
    )

    config = PcbLibCleanConfig.from_file(config_path)

    assert config.profile == "default"
