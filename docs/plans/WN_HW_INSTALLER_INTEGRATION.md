# WN Workspace Installer Integration

Status: draft planning note
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
  or source checkout changes.
- Windows, macOS, Linux, and WSL get equivalent behavior.
- The public command name is `altium-cruncher`.
- The Python import/module name remains `altium_cruncher`; use
  `python -m altium_cruncher` only as a developer/module fallback, not as a
  second installed executable.
- The install path is visible immediately to workspace activation and documented
  for fresh shells.

## Install Modes

1. Public package install with `uv tool install --force
   altium-cruncher==2026.5.28` for the May 28, 2026 release.
2. Local source checkout install with `uv tool install --force --editable
   <workspace>/altium_cruncher`.
3. Workspace-local wrapper scripts in a PATH-managed `bin` folder only as a
   fallback for non-Python native tools or unusual installer constraints.

The first release should use `uv tool install`. The installer test must
resolve `altium-cruncher` and check the version.

## Install Test Contract

The `wn-hw` installer test should run after setup and after update:

```powershell
Get-Command altium-cruncher
altium-cruncher --version
```

The version output must match the configured or released package version.

Setup/update should also run `uv tool update-shell` or otherwise ensure the uv
tool executable directory is visible to fresh workspace shells.
