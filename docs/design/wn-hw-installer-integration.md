# WN Workspace Installer Integration

Status: draft
Last updated: 2026-05-25

## Purpose

`altium-cruncher` is moving from a private `toolz` package to a standalone
public package. Existing WN workspace flows still need a command-line executable
after `wn-hw` setup and update.

The integration is successful only when a normal workspace shell can run both
entry points without manually editing PATH:

```powershell
altium-cruncher --version
altium_cruncher --version
```

## Required Behavior

- `wn-hw` setup installs or exposes `altium-cruncher`.
- `wn-hw` update refreshes the installed executable when the configured package
  or source checkout changes.
- Windows, macOS, Linux, and WSL get equivalent behavior.
- The public command name is `altium-cruncher`.
- The compatibility command name is `altium_cruncher`.
- The install path is visible immediately to workspace activation and documented
  for fresh shells.

## Candidate Install Modes

1. Public package install with `pipx install --force altium-cruncher`.
2. Local source checkout install with `pipx install --force --editable
   <workspace>/altium_cruncher`.
3. Workspace-local wrapper scripts in a PATH-managed `bin` folder.

The first release can choose one mode, but the installer smoke test must be the
same: resolve both commands and check the version.

## Smoke Test Contract

The `wn-hw` installer test should run after setup and after update:

```powershell
Get-Command altium-cruncher
Get-Command altium_cruncher
altium-cruncher --version
altium_cruncher --version
```

The version output must match the configured or released package version.
