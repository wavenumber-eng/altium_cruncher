# WN Workspace Installer Integration

Status: implemented locally; package publish and cross-machine validation pending
Last updated: 2026-05-28

## Purpose

`altium-cruncher` is moving from a private `toolz` package to a standalone
public package. Existing WN workspace flows still need a command-line executable
after `wn-hw` setup and update.

The integration is successful only when a normal workspace shell can run the
canonical executable without manually editing PATH:

```powershell
altium-cruncher --version
```

## Required Behavior

- `wn-hw` setup installs or exposes `altium-cruncher`.
- `wn-hw` update refreshes the installed executable when the configured package
  changes.
- Windows, macOS, Linux, and WSL should get equivalent behavior. Current local
  validation covers Windows PowerShell dry runs and POSIX dry runs under WSL.
  Second-PC and macOS manual smoke tests remain pending.
- The public command name is `altium-cruncher`.
- The Python import/module name remains `altium_cruncher`; use
  `python -m altium_cruncher` only as a developer/module fallback, not as a
  second installed executable.
- The install path is visible immediately to workspace activation and documented
  for fresh shells.

## Install Modes

1. Implemented first-release mode: public package install with `uv tool install
   --force altium-cruncher==2026.5.28` for the May 28, 2026 release.
2. Deferred development mode: local source checkout install with `uv tool
   install --force --editable <workspace>/altium_cruncher`.
3. Deferred fallback mode: workspace-local wrapper scripts in a PATH-managed
   `bin` folder for non-Python native tools or unusual installer constraints.

The first release should use `uv tool install`. The installer test must
resolve `altium-cruncher` and check the version.

## Install Test Contract

The `wn-hw` installer test should run after setup and after update:

```powershell
Get-Command altium-cruncher
altium-cruncher --version
```

The version output must match the configured or released package version.

Setup/update also runs `uv tool update-shell` and records the uv tool executable
directory in `wn-hw` install state. PowerShell activation reads the install
state; POSIX setup/update writes `.state/env.sh` for `. ./activate`.

## Implementation Notes

Implemented in `wn-hw` commit `b2b8fbb` on 2026-05-28:

- added a manifest-level `tools` array with `altium-cruncher==2026.5.28`;
- taught `setup.ps1` / `update.ps1` and `setup.sh` / `update.sh` to install and
  verify manifest uv tools;
- updated PowerShell and POSIX activation path handling for uv tool bin paths;
- documented the Windows-first, second-Windows-PC, then macOS validation order.

Local validation used dry runs because the final PyPI package may not exist yet:

- `powershell ... .\setup.ps1 -DryRun -NoPersistUserEnv -SkipClone
  -SkipSiblingSetup -SkipRebuildBin`;
- `powershell ... .\update.ps1 -DryRun -SkipRebuildBin`;
- `bash -n setup.sh update.sh`;
- `bash setup.sh --dry-run --skip-nix-install --skip-clone
  --skip-sibling-setup --skip-rebuild-bin --no-shell-activate`;
- `bash update.sh --dry-run --skip-rebuild-bin`.
